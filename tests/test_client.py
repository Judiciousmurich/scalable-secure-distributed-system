import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client.task_handler import process_task, parallel_task_execution

class TestClientComponents(unittest.TestCase):
    def test_single_task_processing(self):
        # Test compute task
        compute_task = {'type': 'compute', 'data': [1, 2, 3, 4, 5]}
        result = process_task(compute_task)
        self.assertEqual(result, 15)

        # Test sort task
        sort_task = {'type': 'sort', 'data': [5, 2, 8, 1, 9]}
        result = process_task(sort_task)
        self.assertEqual(result, [1, 2, 5, 8, 9])

    def test_parallel_task_execution(self):
        tasks = [
            {'type': 'compute', 'data': [1, 2, 3]},
            {'type': 'sort', 'data': [5, 2, 8]},
            {'type': 'multiply', 'data': [1, 2, 3]}
        ]
        results = parallel_task_execution(tasks)
        self.assertEqual(len(results), 3)

if __name__ == '__main__':
    unittest.main()