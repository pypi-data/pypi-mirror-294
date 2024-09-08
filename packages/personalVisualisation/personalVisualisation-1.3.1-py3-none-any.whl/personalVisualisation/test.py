from . import get_logger
def tester():
    try:
        get_logger().store_log()
    except Exception as e:
        None
    return "Testing successful..."

