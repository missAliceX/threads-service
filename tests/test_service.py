import mock
import random
import grpc
from src import service
from tests import ServiceTestCase
from pylib.proto.threads_pb2 import Thread, ThreadType, UpdateThreadsRequest


class TestThreadsService(ServiceTestCase):
    @mock.patch("src.service.PostgresClient.migrate")
    @mock.patch("src.service.PostgresClient.connect")
    def test_new_service(self, connect, migrate):
        # Creates a new service
        service.Service(self.test_cfg)

        # Asserts that it migrated and connect to Postgres
        connect.assert_called_with(self.test_cfg)
        migrate.assert_called_with('up')

    @mock.patch("src.service.repo.update_threads")
    def test_update_threads(self, update_threads):
        # Creates a new service
        svc = service.Service(self.test_cfg)

        # Add threads for the given project id
        project_id = random.randint(1, 100)
        threads = [Thread(thread_type=ThreadType.COMMENT, message="hello")]
        svc.UpdateThreads(UpdateThreadsRequest(
            project_id=project_id,
            threads=threads,
        ), None), 
        
        # Asserts that it called update_threads() with appropriate parameters
        actual_project_id, actual_threads = update_threads.call_args_list[0][0]
        self.assertEqual(project_id, actual_project_id)
        self.assertEqual(len(actual_threads), 1)
        self.assertEqual(threads[0], actual_threads[0])
