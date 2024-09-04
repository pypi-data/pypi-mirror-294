import time
import logging
from typing import Callable, List, Optional

from api_processor.helper.retry.retry_executor_ex import RetryExecutorException


# class RetryExecutor:
#     def __init__(self):
#         self.max_retries = 0
#         self.delay = 0
#         self.white_listed_exceptions: Optional[List[str]] = []
#
#     def max_retries(self, retries: int):
#         self.max_retries = retries
#         return self
#
#     def delay(self, delay: int, time_unit: str):
#         if time_unit == 'MINUTES':
#             self.delay = delay * 60 * 1000  # Convert minutes to milliseconds
#         else:
#             self.delay = delay
#         return self
#
#     def configure(self, exceptions: List[str]):
#         if self.white_listed_exceptions is None:
#             self.white_listed_exceptions = []
#         if exceptions:
#             self.white_listed_exceptions.extend(exceptions)
#         return self
#
#     def execute(self, func: Callable[[], any]) -> any:
#         try:
#             return func()
#         except Exception as e:
#             if self.white_listed_exceptions:
#                 if not any(exc in str(e) for exc in self.white_listed_exceptions):
#                     retry_executor_msg = "FAILED will not be retried as the exception is not whitelisted"
#                     logging.error(f"{retry_executor_msg} ex: {e}")
#                     raise RetryExecutorException(original_exception=e, retry_executor_message=retry_executor_msg,
#                                                  exception_message=str(e))
#
#             logging.error(str(e))
#             logging.error(
#                 f"FAILED will be retried {self.max_retries} times after a delay of {self.delay / 1000} seconds.")
#             return self.retry(func)
#
#     def retry(self, func: Callable[[], any]) -> any:
#         exception = None
#         retry_counter = 0
#         while retry_counter < self.max_retries:
#             try:
#                 if self.delay > 0:
#                     time.sleep(self.delay / 1000)  # Convert milliseconds to seconds
#                 return func()
#             except Exception as ex:
#                 retry_counter += 1
#                 logging.error(str(ex))
#                 logging.error(f"FAILED on retry {retry_counter} of {self.max_retries}")
#                 if retry_counter >= self.max_retries:
#                     logging.error("Max retries exceeded.")
#                     exception = ex
#                     break
#         if exception is None:
#             raise RetryExecutorException(exception_message=f"FAILED on all of {self.max_retries} retries")
#         else:
#             raise RetryExecutorException(original_exception=exception,
#                                          exception_message=f"FAILED on all of {self.max_retries} retries",
#                                          retry_executor_message=str(exception))


class RetryExecutor:
    def __init__(self):
        self._max_retries = 0
        self._delay = 0
        self._white_listed_exceptions: Optional[List[str]] = []
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)  # Set the logging level to INFO
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(console_handler)

    def max_retries(self, retries: int):
        self._max_retries = retries
        return self

    def delay(self, delay: int, time_unit: str):
        if time_unit == 'minutes':
            self._delay = delay * 60 * 1000  # Convert minutes to milliseconds
        elif time_unit == 'hours':
            self._delay = delay * 60 * 60 * 1000  # Convert minutes to milliseconds
        else:
            self._delay = delay * 1000
        return self

    def configure(self, exceptions: List[str]):
        if self._white_listed_exceptions is None:
            self._white_listed_exceptions = []
        if exceptions:
            self._white_listed_exceptions.extend(exceptions)
        return self

    def execute(self, func: Callable[[], any]) -> any:
        try:
            return func()
        except Exception as e1:
            if self._white_listed_exceptions:
                if not any(exc in str(e1) for exc in self._white_listed_exceptions):
                    retry_executor_msg = "FAILED will not be retried as the exception is not whitelisted"
                    self.logger.error(f"{retry_executor_msg} ex: {e1}")
                    raise RetryExecutorException(original_exception=e1, retry_executor_message=retry_executor_msg,
                                                 exception_message=str(e1))

            self.logger.error(str(e1))
            self.logger.error(
                f"FAILED will be retried {self._max_retries} times after a delay of {self._delay / 1000} seconds.")
            return self._retry(func)

    def _retry(self, func: Callable[[], any]) -> any:
        exception = None
        retry_counter = 0
        while retry_counter < self._max_retries:
            try:
                if self._delay > 0:
                    time.sleep(self._delay / 1000)  # Convert milliseconds to seconds
                return func()
            except Exception as ex:
                retry_counter += 1
                self.logger.error(str(ex))
                self.logger.error(f"FAILED on retry {retry_counter} of {self._max_retries}")
                if retry_counter >= self._max_retries:
                    self.logger.error("Max retries exceeded.")
                    exception = ex
                    break
        if exception is None:
            raise RetryExecutorException(exception_message=f"FAILED on all of {self._max_retries} retries")
        else:
            raise RetryExecutorException(original_exception=exception,
                                         exception_message=f"FAILED on all of {self._max_retries} retries",
                                         retry_executor_message=str(exception))


# Example usage
if __name__ == "__main__":
    def faulty_function():
        raise RuntimeError("This is a test exception")


    retry_executor = RetryExecutor()
    retry_executor.max_retries(3).delay(2, 'SECONDS').configure(['test exception'])

    try:
        result = retry_executor.execute(faulty_function)
        print(result)
    except RetryExecutorException as e:
        print(f"Operation failed: {e}")
