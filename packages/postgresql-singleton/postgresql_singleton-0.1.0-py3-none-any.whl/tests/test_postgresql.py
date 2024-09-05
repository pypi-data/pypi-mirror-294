import unittest

from postgresql_singleton.config import PostgresConfig
from postgresql_singleton.db import PostgresClient


class TestPostgresClient(unittest.TestCase):

    def setUp(self):
        self.config = PostgresConfig(
            host="localhost",
            user="testuser",
            password="testpassword",
            database="testdb",
            port=5432
        )

    def test_initialize_pool(self):
        PostgresClient.initialize_pool(self.config)
        self.assertIsNotNone(PostgresClient._connection_pool)

    def test_get_connection(self):
        with PostgresClient.get_connection(self.config) as connection:
            self.assertIsNotNone(connection)

    def test_close_all_connections(self):
        PostgresClient.initialize_pool(self.config)
        PostgresClient.close_all_connections()
        self.assertIsNone(PostgresClient._connection_pool)