import unittest

from pylib.testutil import postgres
from pylib.postgres import PostgresClient


class ServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Starts the Postgres container
        cls.test_cfg, cls.container = postgres.run()

    def setUp(self):
        # Removes the threads data everytime we run a new test
        with postgres.repo() as cursor:
            cursor.execute("truncate threads cascade")
    
    @classmethod
    def tearDownClass(cls):
        # Stops the connection to the Postgres container
        PostgresClient.stop()
        # Stops the Postgres container itself
        postgres.stop(cls.container)