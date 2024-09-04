from typing import Optional


class RetryExecutorException(Exception):
    def __init__(self, original_exception: Optional[Exception] = None, retry_executor_message: str = "",
                 exception_message: str = ""):
        super().__init__(exception_message)
        self.original_exception = original_exception
        self.retry_executor_message = retry_executor_message
        self.exception_message = exception_message

    def __str__(self):
        if self.original_exception:
            return f"{self.retry_executor_message}: {self.exception_message} (Caused by {self.original_exception})"
        return self.exception_message
