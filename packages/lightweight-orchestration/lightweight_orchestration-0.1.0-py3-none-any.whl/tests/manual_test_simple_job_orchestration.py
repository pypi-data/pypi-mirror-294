import os
import sys
import time
import logging


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lightweight_orchestration import SimpleJobOrchestrator


# Define some example functions for testing
def test_function_a(**kwargs):
    print(f'Function A is running: {kwargs}')
    time.sleep(1)
    return f"Result from A with {kwargs['param1']}, {kwargs['param2']}"

def test_function_b(**kwargs):
    print(f'Function B is running: {kwargs}')
    time.sleep(2)
    return f"Result from B with {kwargs['param1']}, {kwargs['param2']}"

def test_function_c(**kwargs):
    print(f'Function C is running: {kwargs}')
    time.sleep(3)
    return f"Result from C with {kwargs['param1']}, {kwargs['param2']}"

def test_function_fails(**kwargs):
    print(f'Function Fails is running: {kwargs}')
    time.sleep(2)
    raise ValueError("Intentional failure in function")


# Define DAG for testing
task_dag = {
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


if __name__ == "__main__":
    orchestrator = SimpleJobOrchestrator(   task_dag,
                                            log_level_to_console = logging.DEBUG,
                                            log_level_to_file = logging.DEBUG,
                                            log_to_file = 'orchestration.log',
                                            )            
    success_results, exception_results = orchestrator.run_job(param1="value1", param2="value2")
    for i in success_results:
        print(f"Success: {i}")
    for i in exception_results:
        print(f"Exeption: {i}")

