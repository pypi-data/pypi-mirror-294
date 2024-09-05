import os
import logging
from pathlib import Path
from datetime import datetime
from logging import Logger, Formatter, StreamHandler, FileHandler


datefmt = "%d/%m/%Y %H:%M:%S"
logfmt = "%(levelname)s pid(%(process)d) %(asctime)s.%(msecs)03d %(qualifiedFuncName)s() %(message)s"
logfmt = Formatter(fmt=logfmt, datefmt=datefmt)
logdir = os.path.join(os.getcwd(), 'logs')


def logfilter(record) -> bool:
  record.qualifiedFuncName = '.' + record.funcName if record.name == 'root' else record.name + '.' + record.funcName
  return True


def add_stdout_handler(logger = logging.getLogger(), level: int = logging.DEBUG, fmt: str = logfmt, filter = logfilter) -> Logger:
  handler = StreamHandler()
  handler.setLevel(level)
  handler.setFormatter(fmt)
  handler.addFilter(filter)
  logger.addHandler(handler)
  return logger


def add_file_handler(logger = logging.getLogger(), level: int = logging.DEBUG, fmt: str = logfmt, filter = logfilter, dir: str = logdir, file: str = 'log.txt') -> Logger:
  name, ext = os.path.splitext(file)
  name = f"{name}-{datetime.now().strftime(datefmt)}.{ext if len(ext) > 0 else 'txt'}"
  logfile = Path(dir)
  logfile.mkdir(parents=True, exist_ok=True)
  logfile = logfile.joinpath(name)
  handler = FileHandler(str(logfile))
  handler.setLevel(level)
  handler.addFilter(filter)
  handler.setFormatter(fmt)
  logger.addHandler(handler)
