import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server.authentication import ClientAuthentication
from src.server.task_manager import TaskManager

class TestServerComponents(unittest.TestCase):
    def setUp(self):
        self.auth_manager = ClientAuthentication()
        self.task_manager = TaskManager()

    def test_authentication(self):
        # Test valid credentials
        self.assertTrue(
            self.auth_manager.validate_credentials('client1', 'password1')
        )
        
        # Test invalid credentials
        self.assertFalse(
            self.auth_manager.validate_credentials('invalid', 'wrong')
        )

    def test_task_processing(self):
        # Test compute task
        compute_task = {
            'type': 'compute', 
            'data': [1, 2, 3, 4, 5]
        }
        result = self.task_manager.execute_task(compute_task)
        self.assertEqual(result['result'], 15)

        # Test sort task
        sort_task = {
            'type': 'sort', 
            'data': [5, 2, 8, 1, 9]
        }
        result = self.task_manager.execute_task(sort_task)
        self.assertEqual(result['result'], [1, 2, 5, 8, 9])

    def test_task_distribution(self):
        tasks = [
            {'type': 'compute', 'data': [1, 2, 3]},
            {'type': 'sort', 'data': [5, 2, 8]},
            {'type': 'multiply', 'data': [1, 2, 3]}
        ]
        results = self.task_manager.distribute_tasks(tasks)
        self.assertEqual(len(results), 3)

if __name__ == '__main__':
    unittest.main()