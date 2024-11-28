import unittest
from server.authentication import authenticate_client

class TestServer(unittest.TestCase):
    def test_authentication(self):
        # Mock client socket for testing
        class MockSocket:
            def recv(self, _):
                return "admin:password".encode()

            def send(self, _):
                pass

        mock_socket = MockSocket()
        self.assertTrue(authenticate_client(mock_socket))

if __name__ == "__main__":
    unittest.main()
