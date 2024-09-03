import queue
import threading
import logging
import inspect
import types
import json
import time
import uuid
from datetime import datetime, timezone

class SimpleJobOrchestrator:
    INITIAL_TASK = '_START_'

    def __init__(self, 
                 task_dag = {INITIAL_TASK: None},
                 task_execution_threads = 3,
                 task_wait_timeout = 1,
                 log_level_to_console = logging.INFO,
                 log_level_to_file = logging.DEBUG,
                 log_to_file = None,
                 ):
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(min(log_level_to_console, log_level_to_file))

        # Console logging
        if log_level_to_console is not None:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level_to_console)
            console_formatter = logging.Formatter('%(levelname)s: %(message)s')
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

        # File logging with a timestamp and thread ID
        if log_to_file and log_level_to_file is not None:
            file_handler = logging.FileHandler(log_to_file)
            file_handler.setLevel(log_level_to_file)
            file_formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S') # Already included in message [%(threadName)s] 
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

        # Initialize class variables
        self.task_dag = task_dag
        self.task_execution_threads = task_execution_threads
        self.task_wait_timeout = task_wait_timeout 
        self.task_queue = queue.Queue()
        self.successful_result_queue = queue.Queue()
        self.exception_queue = queue.Queue()

        self.logger.debug(f"SimpleJobOrchestrator: Initializing instance with {self.task_execution_threads} threads, {self.task_wait_timeout} timeout, and the following Task DAG:")
        for key, value in self.task_dag.items():
            self.logger.debug(f"\t Task {key} ==> {value}")

        # Map task names to actual callable functions available in all namespaces in the stack (only one type of task exists for now: function calling)
        self.callable_functions = {name: func
                                   for frame_info in inspect.stack()
                                   for name, func in frame_info.frame.f_globals.items()
                                   if isinstance(func, types.FunctionType) and name in task_dag.keys()}

        # Check if all functions in the DAG are callable
        missing_functions = [func for func in task_dag.keys() if func != self.INITIAL_TASK and func not in self.callable_functions]
        if missing_functions:
            self.logger.critical(f"Missing callable functions: {missing_functions}.")
            raise ValueError(f"Missing callable functions: {missing_functions}.")
        
        # Check that DAG contains a _START_ key.
        if self.INITIAL_TASK not in task_dag:
            message = f"{self.INITIAL_TASK} key is missing from the task DAG."
            self.logger.critical(message)
            raise KeyError(message)
        
        # Check that every item in ["next_tasks"] is also a key in the DAG (not an error, warning only).
        for key, value in task_dag.items():
            if value and 'next_tasks' in value:
                for next_func in value['next_tasks']:
                    if next_func not in task_dag:
                        self.logger.warning(f"Task '{next_func}' in 'next_tasks' of '{key}' is not defined in the DAG.")


    def run_job(self, **kwargs):
        job_start_timestamp = datetime.now(timezone.utc).isoformat()
        job_uuid = str(uuid.uuid4())
        self.logger.debug(f"SimpleJobOrchestrator job {job_uuid} starting at {job_start_timestamp} UTC.")
        
        # Add job_start_timestamp and job_uuid to the parameters
        kwargs = kwargs.copy()  # Make a shallow copy of the parameters before adding anything to them
        kwargs['_orchestrator_job_start_timestamp_'] = job_start_timestamp
        kwargs['_orchestrator_job_uuid_'] = job_uuid
        serialized_params = json.dumps(kwargs)

        # Enqueue the initial functions from the _START_ node
        if self.task_dag[self.INITIAL_TASK] and self.task_dag[self.INITIAL_TASK]["next_tasks"]:
            for next_func in self.task_dag[self.INITIAL_TASK]["next_tasks"]:
                initial_task_info = (next_func, serialized_params)
                self.task_queue.put(initial_task_info)
                self.logger.debug(f"SimpleJobOrchestrator job {job_uuid} enqueued task: {next_func}")

        # Start threads to process the queue
        threads = []
        for i in range(self.task_execution_threads):
            thread = threading.Thread(target=self.run_job_thread, name=f"Job-{job_uuid}-Thread-{i+1}")
            thread.start()
            threads.append(thread)
            self.logger.debug(f"SimpleJobOrchestrator job {job_uuid} starting new thread: {thread.name}")

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Collect results from queues and return as lists
        success_result_list = []
        exception_result_list = []
        
        while not self.successful_result_queue.empty():
            success_result_list.append(self.successful_result_queue.get())

        while not self.exception_queue.empty():
            exception_result_list.append(self.exception_queue.get())

        # Wrap up
        self.logger.debug(f"SimpleJobOrchestrator job {job_uuid} completed!")
        return success_result_list, exception_result_list


    def run_job_thread(self):
        time.sleep(0.1)
        while True:
            try:
                # Initialize variables so they always exist
                current_thread = threading.current_thread()
                task_info = None

                # Retrieve the next item from the queue
                task_info = self.task_queue.get(timeout = self.task_wait_timeout) # seconds

                # Determine the type of task and execute it (for now, there is only one: function calling)
                self.logger.debug(f"SimpleJobOrchestrator {current_thread.name}: New task found.")
                self.run_task_function_call(task_info)

                # Mark task as complete
                self.task_queue.task_done()

            except queue.Empty:
                self.logger.debug(f"SimpleJobOrchestrator {current_thread.name}: task queue is empty. Exiting thread.")
                break

            except Exception as e:
                exception_message = f"SimpleJobOrchestrator {current_thread.name}: Unexpected error: {str(e)}. Ending Thread."
                self.exception_queue.put((task_info, exception_message, None))
                self.logger.error(exception_message)
                break # End thread but do not raise error


    def run_task_function_call(self, task_info):
        # Initialize variables so they always exist
        current_thread = threading.current_thread()
        function_call_start_timestamp = None
        function_call_end_timestamp = None
        function_call_duration = None
        execution_details = None

        # Pre-process function call
        try:
            function_name, serialized_params = task_info  # Function calls must have 2 items
            func = self.callable_functions[function_name]
            params = json.loads(serialized_params)
            params['_orchestrator_thread_name_'] = current_thread.name
            self.logger.debug(f"SimpleJobOrchestrator {current_thread.name}: task processing function: {function_name}")
        except Exception as e:
            exception_message = f"SimpleJobOrchestrator {current_thread.name}: task failed to retrieve or parse item from queue: {str(e)}"
            self.exception_queue.put((task_info, exception_message, execution_details))
            self.logger.error(exception_message)
            return False

        # Execute function call
        try:
            function_call_start_timestamp = datetime.now(timezone.utc).isoformat()
            start_time = time.time()
            function_result = func(**params)
            function_call_end_timestamp = datetime.now(timezone.utc).isoformat()
            function_call_duration = (time.time() - start_time) * 1000  # Duration in milliseconds
        except Exception as e:
            exception_message = f"SimpleJobOrchestrator {current_thread.name}: Execution of task {function_name} failed: {str(e)}"
            execution_details = json.dumps({
                "function_call_start_timestamp" : function_call_start_timestamp,
                "function_call_end_timestamp"   : function_call_end_timestamp,
                "function_call_duration"        : function_call_duration,
            })
            self.exception_queue.put((task_info, exception_message, execution_details))
            self.logger.error(exception_message)
            return False

        # Post-process successful function call
        try:
            # Save the results
            execution_details = json.dumps({
                "function_call_start_timestamp" : function_call_start_timestamp,
                "function_call_end_timestamp"   : function_call_end_timestamp,
                "function_call_duration"        : function_call_duration,
            })
            self.successful_result_queue.put((task_info, function_result, execution_details))
            # Enqueue the next functions
            if self.task_dag[function_name] and self.task_dag[function_name]["next_tasks"]:
                next_tasks = self.task_dag[function_name]["next_tasks"]
                for next_func in next_tasks:
                    new_task_info = (next_func, serialized_params)
                    self.task_queue.put(new_task_info)
                    self.logger.debug(f"SimpleJobOrchestrator {current_thread.name}: Enqueued {next_func} as next task after {function_name}")
        except Exception as e:
            exception_message = f"SimpleJobOrchestrator {current_thread.name}: Post-processing failed for task {function_name}: {str(e)}"
            self.exception_queue.put((task_info, exception_message, execution_details))
            self.logger.error(exception_message)
            return False

        # Success!
        self.logger.debug(f"SimpleJobOrchestrator {current_thread.name}: Task {function_name} succesfully completed in {function_call_duration:.2f} ms.")
        return True

