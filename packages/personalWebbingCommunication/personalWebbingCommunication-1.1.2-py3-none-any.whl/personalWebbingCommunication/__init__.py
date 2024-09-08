logger = None

def insert_logger(logging_class_instance):
    global logger
    name_of_class = logging_class_instance.__class__.__name__
    if name_of_class != "custom_logger":
        return False
    logger = logging_class_instance
    return True

def get_logger():
    return logger

from .multipart import *
from .test import *

