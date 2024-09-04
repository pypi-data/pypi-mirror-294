from abc import ABC, abstractmethod
from typing import List, Dict, Any
from enum import Enum


# Enum for TimeUnit similar to Java's TimeUnit
class TimeUnit(Enum):
    SECONDS = 'seconds'
    MINUTES = 'minutes'
    HOURS = 'hours'


class RestWebServiceDelegate(ABC):

    @abstractmethod
    def invoke(self, request, rest_ws_map: Dict[str, Any], *objects):
        pass

    def retry(self) -> bool:
        return False

    def white_listed_exceptions(self) -> List[str]:
        return []

    def delay(self) -> int:
        return 1

    def max_retries(self) -> int:
        return 3

    def delay_time_unit(self) -> TimeUnit:
        return TimeUnit.MINUTES
