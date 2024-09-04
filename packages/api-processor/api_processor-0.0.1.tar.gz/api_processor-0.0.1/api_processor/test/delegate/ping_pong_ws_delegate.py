import requests
from typing import Dict, Any, List
from api_processor.interface.rest_ws_delegate import RestWebServiceDelegate, TimeUnit
from api_processor.test.model.ping_pong_response import PingPongResponse


class PingPongWSDelegate(RestWebServiceDelegate):

    def invoke(self, request, rest_ws_map: Dict[str, Any], *objects):
        url = "http://localhost:8888/ping"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=request.__dict__, headers=headers)
        return PingPongResponse(**response.json())

    def retry(self) -> bool:
        return True

    def delay_time_unit(self) -> TimeUnit:
        return TimeUnit.SECONDS

    def delay(self) -> int:
        return 10

    def white_listed_exceptions(self) -> List[str]:
        return ["ConnectionError"]
