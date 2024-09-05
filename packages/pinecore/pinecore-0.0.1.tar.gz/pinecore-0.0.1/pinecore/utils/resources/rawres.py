import base64
import hashlib
from typing import Any
from pinecore import BaseObj
from pinecore.utils.resources import ResourceLoaders


MB = 1024^2


class Resource(BaseObj):
  """
  Raw bytes resource.
  """
  @property
  def data(self) -> bytes:
    return self._data
  
  @property
  def hash(self) -> str:
    return hashlib.md5(self.data).hexdigest()
  
  @property
  def base64(self) -> str:
    return str(base64.b64encode(self.data))
  
  @property
  def size(self) -> float:
    return len(self.data) / MB

  def __init__(self, source: Any, *args, **kwargs) -> None:
    self._data = ResourceLoaders().load(source, *args, **kwargs)
