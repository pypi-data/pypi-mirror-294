from abc import ABC, abstractmethod
from api_processor.interface.rest_ws_delegate import RestWebServiceDelegate


class RestWebServiceHandler(ABC):

    @abstractmethod
    def delegate(self) -> RestWebServiceDelegate:
        pass

    def prepare_request(self, rest_ws_map, *objects):
        return None

    def process_response(self, request, response, rest_ws_map, *objects):
        pass

    def web_service_name(self):
        return None

    def print_logs(self):
        return True

    def empty_payload(self):
        return False
