import logging
import sys

def log(msg, debug=False):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger("es_logger")
    # handler = logging.StreamHandler(sys.stdout)
    # logger.addHandler(handler)
    if debug:
        logger.debug(10, msg)
    else:
        logger.log(20, msg)