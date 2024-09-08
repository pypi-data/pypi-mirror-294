# from .popup import *
# from .visualise import *

logger = None

def insert_logger(logging_class_instance):
    global logger
    name_of_class = logging_class_instance.__class__.__name__
    if name_of_class != "custom_logger":
        return False
    logger = logging_class_instance
    return True

from .images import *
from .popup import *