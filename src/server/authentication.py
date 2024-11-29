import json
import secrets
import hashlib
import logging

class ClientAuthentication:
    def __init__(self):
        # Simulated user database (in real-world, use proper database)
        self.users = {
            'client1': self._hash_password('password1'),
            'client2': self._hash_password('password2')
        }
        self.active_tokens = {}
        self.logger = logging.getLogger(__name__)

    def _hash_password(self, password):
        """Create a secure hash of the password"""
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_token(self, client_id):
        """Generate a secure authentication token"""
        token = secrets.token_hex(16)
        self.active_tokens[client_id] = token
        return token

    def validate_credentials(self, client_id, password):
        """Validate client credentials"""
        if client_id not in self.users:
            self.logger.warning(f"Authentication attempt for unknown client: {client_id}")
            return False
        return self._hash_password(password) == self.users.get(client_id)

    def authenticate_client(self, client_socket):
        """Authenticate incoming client connection"""
        try:
            # Receive authentication data
            auth_data = client_socket.recv(1024).decode('utf-8')
            auth_info = json.loads(auth_data)
            
            client_id = auth_info.get('client_id')
            auth_token = auth_info.get('auth_token')

            # Validate token
            if self.validate_token(client_id, auth_token):
                response = {
                    'status': 'success',
                    'message': 'Authentication successful'
                }
                client_socket.send(json.dumps(response).encode('utf-8'))
                self.logger.info(f"Client {client_id} authenticated successfully")
                return True
            else:
                response = {
                    'status': 'failed',
                    'message': 'Authentication failed'
                }
                client_socket.send(json.dumps(response).encode('utf-8'))
                self.logger.warning(f"Authentication failed for client: {client_id}")
                return False
        except Exception as e:
            self.logger.error(f"Authentication error: {e}")
            return False

    def validate_token(self, client_id, token):
        """Check if the provided token is valid"""
        stored_token = self.active_tokens.get(client_id)
        return stored_token == token

# Global authentication instance
auth_manager = ClientAuthentication()

def authenticate_client(client_socket):
    """Wrapper function for client authentication"""
    return auth_manager.authenticate_client(client_socket)