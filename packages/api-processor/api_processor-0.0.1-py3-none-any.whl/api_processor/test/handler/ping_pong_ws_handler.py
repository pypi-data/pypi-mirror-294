from api_processor.interface.rest_ws_handler import RestWebServiceHandler
from api_processor.test.delegate.ping_pong_ws_delegate import PingPongWSDelegate
from api_processor.test.model.ping_pong_request import PingPongRequest
from api_processor.test.model.ping_pong_response import PingPongResponse


class PingPongWsHandler(RestWebServiceHandler):
    def delegate(self):
        return PingPongWSDelegate()

    def prepare_request(self, rest_ws_map, *objects):
        request = PingPongRequest(data="Ping")
        return request

    def process_response(self, request, response, rest_ws_map, *objects):
        response_data: PingPongResponse = response
        print(response_data.data)

    def web_service_name(self):
        return "PingPongApi"
