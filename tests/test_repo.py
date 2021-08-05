import psycopg2
import uuid

from src import repo
from tests import ServiceTestCase

from pylib.testutil import postgres
from pylib.proto.threads_pb2 import Thread, ThreadType


class TestThreadsRepo(ServiceTestCase):
    def setUp(self):
        # Calls the setUp() method from the ServiceTestCase class
        super().setUp()

        # Adds a new project so we can add threads into it
        with postgres.repo() as cursor:
            project_name = uuid.uuid4().hex
            cursor.execute(
                "insert into projects(project_name, tagline) values (%s, %s) RETURNING project_id",
                [project_name, "i am a test"])
            self.project_id = cursor.fetchone()[0]

    def test_update_threads(self):
        # Add threads to the given project by calling repo.update_threads()
        repo.update_threads(self.project_id, [
            Thread(thread_type=ThreadType.COMMENT, message="hello"),
            Thread(thread_type=ThreadType.PROBLEM, message="x+1")
        ])

        # Get all the threads from the database
        with postgres.repo() as cursor:
            cursor.execute("select * from threads")
            threads = cursor.fetchall()

        # Check that the threads match what we expected
        self.assertEqual(threads, [
            (1, 1, None, 'COMMENT', 'hello'),
            (2, 1, None, 'PROBLEM', 'x+1'),
        ])

    def test_update_threads_error(self):
        # Call repo.update_threads() and expect it to raise an exception
        self.assertRaises(AttributeError, repo.update_threads, self.project_id, [None])

        # Ensure that no threads are added to the database
        with postgres.repo() as cursor:
            cursor.execute("select * from threads")
            threads = cursor.fetchall()
        self.assertEqual(threads, [])