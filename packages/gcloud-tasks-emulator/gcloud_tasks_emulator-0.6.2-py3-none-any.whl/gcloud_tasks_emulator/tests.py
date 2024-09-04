import datetime
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest import mock, TestCase as BaseTestCase

import grpc
import sleuth
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import NotFound
from google.api_core.retry import Retry
from google.cloud.tasks_v2 import CloudTasksClient, Queue, CreateTaskRequest
from google.cloud.tasks_v2.services.cloud_tasks.transports import CloudTasksGrpcTransport
from google.protobuf.timestamp_pb2 import Timestamp

from server import _make_task_request, QueueState, create_server

mock_calls = []


def _create_queue(
    client: CloudTasksClient,
    name: str,
    project='[PROJECT]',
    location='[LOCATION]',
) -> Queue:
    return client.create_queue({
        "queue": {"name": name},
        "parent": client.common_location_path(project, location),
    }, retry=Retry(initial=1e-6, maximum=5))


class MockRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def _handle_request(self):
        mock_calls.append({
            'method': self.command,
            'path': self.path,
            'headers': dict(self.headers),
        })
        self.send_response(200)
        self.end_headers()


class MockServer(threading.Thread):
    def __init__(self, port, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._port = port
        self.is_running = threading.Event()
        self._httpd = None

    def run(self):
        self._httpd = HTTPServer(("localhost", self._port), MockRequestHandler)
        self.is_running.set()
        self._httpd.serve_forever()

    def join(self, timeout=None):
        self.is_running.clear()
        if self._httpd:
            self._httpd.shutdown()
            self._httpd.server_close()


class TestCase(BaseTestCase):
    def setUp(self):
        mock_calls.clear()
        self._server = create_server("localhost", 9022)
        self._server.start()

        transport = CloudTasksGrpcTransport(channel=grpc.insecure_channel("127.0.0.1:9022"))

        self._client = CloudTasksClient(
            transport=transport,
            client_options=ClientOptions(api_endpoint="127.0.0.1:9022")
        )

        self._parent = self._client.common_location_path('[PROJECT]', '[LOCATION]')

        # Create default queue
        self._queue = _create_queue(self._client, f"{self._parent}/queues/default")

    def tearDown(self):
        self._server.stop()

    def test_create_queue(self):
        queue1_path = f"{self._parent}/queues/test_queue1"
        queue2_path = f"{self._parent}/queues/test_queue2"

        ret = _create_queue(self._client, queue1_path)
        self.assertEqual(ret.name, queue1_path)

        ret = _create_queue(self._client, queue2_path)
        self.assertEqual(ret.name, queue2_path)

        return queue1_path, queue2_path

    def test_update_queue(self):
        queue1_path = f"{self._parent}/queues/test_queue1"
        _create_queue(self._client, queue1_path)
        queue1 = self._client.get_queue(name=queue1_path)
        queue1.rate_limits.max_dispatches_per_second = 23
        ret = self._client.update_queue(queue=queue1)
        self.assertEqual(ret.name, queue1_path)

        ret = self._client.update_queue(
            queue=queue1, update_mask={}
        )
        self.assertEqual(ret.name, queue1_path)

    def test_list_queues(self):
        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "default")
        self._client.delete_queue(name=path)

        self.test_create_queue()  # Create a couple of queues

        queues = self._client.list_queues(parent=self._parent)
        self.assertEqual(len(list(queues)), 2)

    def test_get_queue(self):
        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        queue = self._client.get_queue(name=path)
        self.assertEqual(queue.name, path)

    def test_delete_queue(self):
        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "default")
        self._client.delete_queue(name=path)

        self.test_create_queue()  # Create a couple of queues

        queues = self._client.list_queues(parent=self._parent)
        self.assertEqual(len(list(queues)), 2)

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        self._client.delete_queue(name=path)

        queues = self._client.list_queues(parent=self._parent)
        self.assertEqual(len(list(queues)), 1)

    def test_pause_queue(self):
        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "default")
        self._client.delete_queue(name=path)

        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        response = self._client.pause_queue(name=path)
        self.assertEqual(response.state, 2)

    def test_resume_queue(self):
        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "default")
        self._client.delete_queue(name=path)

        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        response = self._client.pause_queue(name=path)
        self.assertEqual(response.state, 2)

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        response = self._client.resume_queue(name=path)
        self.assertEqual(response.state, 1)

    def test_purge_queue(self):
        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")

        # Pause the queue as we don't want tasks to be processed
        self._client.pause_queue(name=path)

        payload = "Hello World!"

        task = {
            'app_engine_http_request': {  # Specify the type of request.
                'http_method': 'POST',
                'relative_uri': '/example_task_handler',
                'body': payload.encode()
            }
        }

        # Create 3 tasks
        self._client.create_task(parent=path, task=task)
        self._client.create_task(parent=path, task=task)
        self._client.create_task(parent=path, task=task)

        tasks = [x for x in self._client.list_tasks(parent=path)]
        self.assertEqual(len(tasks), 3)

        # Check again, make sure list_tasks didn't do anything
        tasks = [x for x in self._client.list_tasks(parent=path)]
        self.assertEqual(len(tasks), 3)

        self._client.purge_queue(name=path)

        tasks = [x for x in self._client.list_tasks(parent=path)]
        self.assertEqual(len(tasks), 0)

    def test_create_task(self):
        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")

        self._client.pause_queue(name=path)
        payload = "Hello World!"

        task = {
            'app_engine_http_request': {  # Specify the type of request.
                'http_method': 'POST',
                'relative_uri': '/example_task_handler',
                'body': payload.encode()
            }
        }

        response = self._client.create_task(parent=path, task=task)
        self.assertTrue(response.name.startswith(path))

    def test_queue_state_submit_task(self):
        """ This runs the code in `QueueState.submit_task`.
            In other tests, this code never gets run because we call `self._server.stop() in
            `tearDown` before it runs. So this test makes a QueueState instance to test directly.
        """
        # This is just making a `Task` object which we can pass to `QueueState.create_task`.
        task_spec = {
            'app_engine_http_request': {  # Specify the type of request.
                'http_method': 'POST',
                'relative_uri': '/example_task_handler',
                'body': "Hello world!".encode(),
            },
            'schedule_time': Timestamp(),
        }
        task = self._client.create_task(parent=self._queue.name, task=task_spec)

        # Now make a QueueState object and test that it doesn't die
        queue_state = QueueState("localhost", 8000, max_retries=1)
        queue_state.create_queue(self._parent, self._queue)
        queue_state.create_task(self._queue.name, task)
        queue_state.submit_task(task.name)

    def test_create_task_without_http_method(self):
        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")

        self._client.pause_queue(name=path)
        payload = "Hello World!"

        task = {
            'app_engine_http_request': {  # Specify the type of request.
                'relative_uri': '/example_task_handler',
                'body': payload.encode()
            }
        }

        response = self._client.create_task(parent=path, task=task)
        self.assertTrue(response.name.startswith(path))

    def test_run_task(self):
        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path(
            '[PROJECT]', '[LOCATION]', "test_queue2"
        )

        self._client.pause_queue(name=path)  # Don't run any tasks while testing

        payload = "Hello World!"

        task = {
            'app_engine_http_request': {  # specify the type of request.
                'http_method': 'POST',
                'relative_uri': '/example_task_handler',
                'body': payload.encode()
            }
        }
        req = CreateTaskRequest({
            "parent": path,
            "task": task,
        })
        response = self._client.create_task(req)
        self.assertTrue(response.name.startswith(path))

        class FakeResponse:
            status = 200

        with sleuth.fake("server._make_task_request", return_value=FakeResponse()):
            self._client.run_task(name=response.name)

        # Should return NOT_FOUND
        self.assertRaises(
            NotFound,
            self._client.run_task,
            {"name": f"{path}/tasks/1119129292929292929"},  # Not a valid task
        )

    def test_default_queue_name(self):
        server = create_server("localhost", 9023, "localhost", 10124, ["projects/[P]/locations/[L]/queues/[Q]"])
        server.start()

        transport = CloudTasksGrpcTransport(channel=grpc.insecure_channel("127.0.0.1:9023"))
        client = CloudTasksClient(
            transport=transport,
            client_options=ClientOptions(api_endpoint="127.0.0.1:9023")
        )

        queues = list(client.list_queues(parent="projects/[P]/locations/[L]"))
        self.assertEqual(len(queues), 1)

        queue = queues[0]
        self.assertEqual(queue.name, "projects/[P]/locations/[L]/queues/[Q]")

        server.stop()

    def test_multiple_default_queue_names(self):
        server = create_server(
            "localhost", 9023, "localhost", 10124,
            ["projects/[P]/locations/[L]/queues/[Q]", "projects/[P]/locations/[L]/queues/[Q2]"]
        )
        server.start()

        transport = CloudTasksGrpcTransport(channel=grpc.insecure_channel("127.0.0.1:9023"))
        client = CloudTasksClient(
            transport=transport,
            client_options=ClientOptions(api_endpoint="127.0.0.1:9023")
        )

        queues = list(client.list_queues(parent="projects/[P]/locations/[L]"))
        self.assertEqual(len(queues), 2)

        self.assertEqual(queues[0].name, "projects/[P]/locations/[L]/queues/[Q]")
        self.assertEqual(queues[1].name, "projects/[P]/locations/[L]/queues/[Q2]")

        server.stop()

    def test_custom_headers(self):
        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")

        self._client.pause_queue(name=path)

        payload = "Hello World!"

        task = {
            'app_engine_http_request': {
                'http_method': 'POST',
                'relative_uri': '/example_task_handler',
                'body': payload.encode(),
                'headers': {'custom': 'custom'}
            }
        }

        self._client.create_task(parent=path, task=task)
        parent = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        task_ = [x for x in self._client.list_tasks(parent=parent)][-1]

        def noop(req): return req

        with mock.patch('urllib.request.urlopen', noop):
            req = _make_task_request('test_queue2', task_, "localhost", 9009)
        assert req.headers['Custom'] == 'custom'


class CustomPortTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls._server = MockServer(10123)
        cls._server.start()
        cls._server.is_running.wait()

    @classmethod
    def tearDownClass(cls):
        cls._server.join(timeout=1)

    def setUp(self):
        mock_calls.clear()

        self._server = create_server("localhost", 9022, "localhost", 10123)
        self._server.start()

        transport = CloudTasksGrpcTransport(channel=grpc.insecure_channel("127.0.0.1:9022"))

        self._client = CloudTasksClient(
            transport=transport,
            client_options=ClientOptions(api_endpoint="127.0.0.1:9022")
        )

        self._parent = self._client.common_location_path('[PROJECT]', '[LOCATION]')

        # Create default queue
        _create_queue(self._client, f"{self._parent}/queues/default")

    def tearDown(self):
        self._server.stop()

    def test_create_queue(self):
        path1 = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue1")
        ret = _create_queue(self._client, path1)
        self.assertEqual(ret.name, path1)

        path2 = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        ret = _create_queue(self._client, path2)
        self.assertEqual(ret.name, path2)

    def test_custom_target_host(self):
        # Override the target host so we can check that works
        self._server._state._target_host = "www.example.com"

        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        self._client.pause_queue(name=path)  # Don't run any tasks while testing

        payload = "Hello World!"

        task = {
            'app_engine_http_request': {  # Specify the type of request.
                'relative_uri': '/example_task_handler',
                'body': payload.encode(),
                'headers': {
                    'Content-Type': 'text/plain'
                },
            }
        }

        response = self._client.create_task(parent=path, task=task)

        class FakeResponse:
            status = 200

        with sleuth.fake("server._make_task_request", return_value=FakeResponse()) as fake:
            self._client.run_task(name=response.name)
            self.assertEqual(fake.calls[0].args[2], "www.example.com")

    def test_run_app_engine_http_request_task(self):
        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        self._client.pause_queue(name=path)  # Don't run any tasks while testing

        payload = "Hello World!"

        task = {
            'app_engine_http_request': {  # Specify the type of request.
                'relative_uri': '/example_task_handler',
                'body': payload.encode(),
                'headers': {
                    'Content-Type': 'text/plain'
                },
            }
        }

        response = self._client.create_task(parent=path, task=task)
        self.assertTrue(response.name.startswith(path))

        self._client.run_task(name=response.name)
        self.assertEqual(len(mock_calls), 1)
        self.assertEqual(mock_calls[0]['method'], 'POST')
        self.assertEqual(mock_calls[0]['path'], '/example_task_handler')
        self.assertEqual(mock_calls[0]['headers']['X-Appengine-Queuename'], path)
        self.assertEqual(mock_calls[0]['headers']['Content-Type'], 'text/plain')

    def test_run_app_engine_http_request_task_with_custom_method(self):
        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        self._client.pause_queue(name=path)  # Don't run any tasks while testing

        task = {
            'app_engine_http_request': {  # Specify the type of request.
                'http_method': 'GET',
                'relative_uri': '/example_task_handler',
            }
        }

        response = self._client.create_task(parent=path, task=task)
        self.assertTrue(response.name.startswith(path))

        self._client.run_task(name=response.name)
        self.assertEqual(len(mock_calls), 1)
        self.assertEqual(mock_calls[0]['method'], 'GET')
        self.assertEqual(mock_calls[0]['path'], '/example_task_handler')
        self.assertEqual(mock_calls[0]['headers']['X-Appengine-Queuename'], path)

    def test_run_http_request_task(self):
        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        self._client.pause_queue(name=path)  # Don't run any tasks while testing

        payload = "Hello World!"

        task = {
            'http_request': {  # Specify the type of request.
                'url': 'http://localhost:10123/http_request_task_handler',
                'body': payload.encode(),
                'headers': {
                    'Content-Type': 'text/plain'
                },
            }
        }

        response = self._client.create_task(parent=path, task=task)
        self.assertTrue(response.name.startswith(path))

        self._client.run_task(name=response.name)
        self.assertEqual(len(mock_calls), 1)
        self.assertEqual(mock_calls[0]['method'], 'POST')
        self.assertEqual(mock_calls[0]['path'], '/http_request_task_handler')
        self.assertEqual(mock_calls[0]['headers']['X-Cloudtasks-Queuename'], path)
        self.assertEqual(mock_calls[0]['headers']['Content-Type'], 'text/plain')

    def test_run_http_request_task_with_custom_method(self):
        self.test_create_queue()  # Create a couple of queues

        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        self._client.pause_queue(name=path)  # Don't run any tasks while testing

        task = {
            'http_request': {  # Specify the type of request.
                'http_method': 'GET',
                'url': 'http://localhost:10123/http_request_task_handler',
            }
        }

        response = self._client.create_task(parent=path, task=task)
        self.assertTrue(response.name.startswith(path))

        self._client.run_task(name=response.name)
        self.assertEqual(len(mock_calls), 1)
        self.assertEqual(mock_calls[0]['method'], 'GET')
        self.assertEqual(mock_calls[0]['path'], '/http_request_task_handler')
        self.assertEqual(mock_calls[0]['headers']['X-Cloudtasks-Queuename'], path)

    def test_run_scheduled_task(self):
        self.test_create_queue()
        path = self._client.queue_path('[PROJECT]', '[LOCATION]', "test_queue2")
        self._client.pause_queue(name=path)  # Don't run any tasks while testing
        schedule_time = Timestamp()
        schedule_time.FromDatetime(datetime.datetime.utcnow() + datetime.timedelta(minutes=1))

        task = {
            'http_request': {  # Specify the type of request.
                'http_method': 'GET',
                'url': 'http://localhost:10123/http_request_task_handler',
            },
            "schedule_time": schedule_time,
        }

        response = self._client.create_task(parent=path, task=task)
        self._client.run_task(name=response.name)
        self.assertEqual(len(mock_calls), 1)


if __name__ == '__main__':
    unittest.main()
