import json
import logging
from typing import Dict, Any

from api_processor.exception.rest_ws_exception import RestWebServiceException
from api_processor.interface.rest_ws_handler import RestWebServiceHandler
from api_processor.helper.retry.retry_executor import RetryExecutor, RetryExecutorException
from dataclasses import asdict


class RestWebServiceFacade:
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)  # Set the logging level to INFO
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(console_handler)

    def initiate(self, handler: RestWebServiceHandler, rest_ws_map: Dict[str, Any], *objects):
        if handler is None:
            raise RestWebServiceException("Cannot initiate webservice call without a proper handler class")

        request = None
        if not handler.empty_payload():
            request = handler.prepare_request(rest_ws_map, *objects)
            if handler.print_logs():
                self.print_logs(request_response=request, handler=handler, log_type=self.REQUEST)

        delegate = handler.delegate()
        if delegate is None:
            raise RestWebServiceException(
                f"Cannot initiate webservice call without a proper client delegate bean for the handler {handler.web_service_name()}")

        response = None
        if delegate.retry():
            try:
                response = RetryExecutor() \
                            .max_retries(delegate.max_retries()) \
                            .delay(delegate.delay(), delegate.delay_time_unit().value) \
                            .configure(delegate.white_listed_exceptions()) \
                            .execute(lambda: delegate.invoke(request, rest_ws_map, *objects))
            except RetryExecutorException as e:
                raise RestWebServiceException(f"Failed to execute retries for {handler.web_service_name()}") from e
        else:
            response = delegate.invoke(request, rest_ws_map, *objects)

        if handler.print_logs():
            self.print_logs(request_response=response, handler=handler, log_type=self.RESPONSE)

        handler.process_response(request, response, rest_ws_map, *objects)

    def print_logs(self, request_response: Any, handler: RestWebServiceHandler, log_type: str):
        web_service_name = handler.web_service_name()
        try:
            json_string = json.dumps(asdict(request_response), default=str)
        except Exception as ex:
            self.logger.error(f"RestWebServiceFacade>>print_logs>>caught exception: {ex}")
            json_string = "{}"

        self.logger.info(
            f"==================================================== {web_service_name} {log_type} BEGINS"
            f" =================================================")
        self.logger.info(json_string)
        self.logger.info(
            f"==================================================== {web_service_name} {log_type} ENDS"
            f" =================================================")
