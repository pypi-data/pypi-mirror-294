from typing import Optional


class RestWebServiceException(Exception):
    def __init__(self, message=None, original_exception: Optional[Exception] = None, cause=None, webservice_name=None):
        super().__init__(message)
        self.cause = cause
        self.original_exception = original_exception
        self.webservice_name = webservice_name

    def get_webservice_name(self):
        return self.webservice_name

    def set_webservice_name(self, webservice_name):
        self.webservice_name = webservice_name

    def __str__(self):
        base_message = super().__str__()
        if self.webservice_name:
            return f"{base_message} [Webservice: {self.webservice_name}]"
        return base_message
