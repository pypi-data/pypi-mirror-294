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