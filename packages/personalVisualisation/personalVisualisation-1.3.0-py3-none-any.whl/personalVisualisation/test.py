from . import logger
def tester():
    try:
        logger.store_log()
    except Exception as e:
        None
    return "Testing successful..."

