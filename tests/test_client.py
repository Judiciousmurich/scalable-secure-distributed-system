import unittest
from client.task_handler import create_task

class TestClient(unittest.TestCase):
    def test_ping_task(self):
        self.assertEqual(create_task("PING"), "PING")

    def test_echo_task(self):
        self.assertEqual(create_task("ECHO", "Hello"), "ECHO:Hello")

if __name__ == "__main__":
    unittest.main()
