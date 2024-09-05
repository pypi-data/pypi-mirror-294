from attrs import define
from pinecore.utils import logging


@define()
class BaseObj:
  """
  Naive do nothing but logs.
  """

  @property
  def classname(self) -> str:
    return self.__class__.__name__
  
  @property
  def modulename(self) -> str:
    return self.__module__
  
  @property
  def logger(self) -> logging.Logger:
    return self.__logger

  def __init__(self, *args, **kwds) -> None:
    super().__init__()
    self.__logger = logging.getLogger(f'{__name__}.{self.classname}')
