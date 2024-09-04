from dataclasses import dataclass

from api_processor.model.rest_ws_request import RestWebServiceRequest


@dataclass
class PingPongRequest(RestWebServiceRequest):
    data: str = None
