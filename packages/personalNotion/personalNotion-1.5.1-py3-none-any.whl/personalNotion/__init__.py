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

import os

headers = {
    'Authorization': f"Bearer {os.getenv('api_key')}",
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

from .database import *
from .page import *
from .test import *
from .table import *