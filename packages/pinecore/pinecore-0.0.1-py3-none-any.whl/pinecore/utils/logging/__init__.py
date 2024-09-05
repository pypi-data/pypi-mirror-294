import logging
from logging import *

root = logging.getLogger()
from .stdout import add_stdout_handler, add_file_handler

add_stdout_handler()
