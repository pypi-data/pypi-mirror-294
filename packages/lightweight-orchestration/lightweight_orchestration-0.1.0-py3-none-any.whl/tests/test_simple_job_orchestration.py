# python -m unittest discover -s tests

import unittest
from lightweight_orchestration import SimpleJobOrchestrator


# Define some example functions for testing
def test_function_a(**kwargs):
    return f"Result from A with {kwargs['param1']}, {kwargs['param2']}"

def test_function_b(**kwargs):
    return f"Result from B with {kwargs['param1']}, {kwargs['param2']}"

def test_function_c(**kwargs):
    return f"Result from C with {kwargs['param1']}, {kwargs['param2']}"

def test_function_fails(**kwargs):
    raise ValueError("Intentional failure in function")


# Define test cases
class TestSimpleJobOrchestrator(unittest.TestCase):

    def setUp(self):
        # Example task DAG for testing
        self.task_dag = {
            SimpleJobOrchestrator.INITIAL_TASK: {
                "task_description": "Start of the DAG",
                "next_tasks": ["test_function_a", "test_function_b"]
            },
            "test_function_a": {
                "task_description": "This is function A",
                "next_tasks": ["test_function_c"]
            },
            "test_function_b": {
                "task_description": "This is function B",
                "next_tasks": ["test_function_c"]
            },
            "test_function_c": {
                "task_description": "This is function C",
                "next_tasks": []
            },
            "test_function_fails": {
                "task_description": "This function will fail",
                "next_tasks": ["test_function_c"]
            }
        }


    def test_successful_execution(self):
        orchestrator = SimpleJobOrchestrator(self.task_dag)
        
        # Run the job
        success_results, exception_results = orchestrator.run_job(param1="value1", param2="value2")

        # Test success results
        self.assertEqual(len(success_results), 4)
        self.assertIn("Result from A", success_results[0][1])
        self.assertIn("Result from B", success_results[1][1])
        self.assertIn("Result from C", success_results[2][1])
        self.assertIn("Result from C", success_results[3][1])

        # Test no exceptions occurred
        self.assertEqual(len(exception_results), 0)


    def test_failed_execution(self):
        # Update the DAG to include a function that fails
        self.task_dag[SimpleJobOrchestrator.INITIAL_TASK]['next_tasks'] = ['test_function_fails']

        orchestrator = SimpleJobOrchestrator(self.task_dag)
        
        # Run the job
        success_results, exception_results = orchestrator.run_job(param1="value1", param2="value2")

        # Test no successful results
        self.assertEqual(len(success_results), 0)

        # Test one exception result
        self.assertEqual(len(exception_results), 1)
        self.assertIn("Intentional failure in function", exception_results[0][1])


    def test_mixed_execution(self):
        # Update the DAG to include both successful and failing functions
        self.task_dag[SimpleJobOrchestrator.INITIAL_TASK]['next_tasks'] = ['test_function_a', 'test_function_fails']

        orchestrator = SimpleJobOrchestrator(self.task_dag)
        
        # Run the job
        success_results, exception_results = orchestrator.run_job(param1="value1", param2="value2")

        # Test mixed results
        self.assertEqual(len(success_results), 2)  # test_function_a and test_function_c should succeed
        self.assertEqual(len(exception_results), 1)  # test_function_fails should fail

        # Ensure correct functions were executed
        self.assertIn("Result from A", success_results[0][1])
        self.assertIn("Result from C", success_results[1][1])
        self.assertIn("Intentional failure in function", exception_results[0][1])

if __name__ == "__main__":
    unittest.main()
