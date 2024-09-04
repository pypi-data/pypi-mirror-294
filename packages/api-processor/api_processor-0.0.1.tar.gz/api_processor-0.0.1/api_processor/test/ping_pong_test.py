import logging
from api_processor.facade.rest_ws_facade import RestWebServiceFacade
from api_processor.test.handler.ping_pong_ws_handler import PingPongWsHandler

if __name__ == "__main__":
    logger = logging.getLogger(__name__)


    def init_loggers():
        logger.setLevel(logging.INFO)  # Set the logging level to INFO
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(console_handler)


    try:
        init_loggers()
        facade = RestWebServiceFacade()
        handler = PingPongWsHandler()
        facade.initiate(handler=handler, rest_ws_map={})
    except Exception as e:
        logger.error(f"Operation failed: {e}")
