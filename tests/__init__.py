import unittest

from pylib.testutil import postgres


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
        # Stops the Postgres container
        postgres.stop()