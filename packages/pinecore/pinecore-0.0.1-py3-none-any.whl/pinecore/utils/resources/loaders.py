import io
import base64
import urllib
from typing import Any
from pathlib import Path
from abc import ABC, abstractmethod
from pinecore import BaseObj
from pinecore.patterns.creational import Singleton



class IResourceLoader(ABC, BaseObj, metaclass=Singleton):
  """
  Interface of all inherited resource loader.
  """
  @abstractmethod
  def load(self, source: Any, *args, **kwds) -> bytes:
    raise NotImplemented()



class ResourceLoader(IResourceLoader):
  """
  Basic resource loader that can load resource from file, URL, base64 or raw bytes.
  """
  def load(self, source: Any, *args, **kwds) -> bytes:
    try:
      return Path(source).expanduser().resolve().read_bytes()
    except:
      self.logger.debug(f"Cannot load {str(source):20s} as file.")
    try:
      return urllib.request.urlopen(source).read()
    except:
      self.logger.debug(f"Cannot load {str(source):20s} from internet.")
    try:
      return base64.b64decode(source, validate=True)
    except:
      self.logger.debug(f"Cannot load {str(source):20s} as base64.")
    try:
      return bytes(source)
    except:
      self.logger.debug(f"Cannot load {str(source):20s} as bytes.")
    raise AssertionError(f"Cannot load resource {str(source):20s}.")



class ResourceLoaders(IResourceLoader):
  """
  Manage all available resource loaders.
  """
  __loaders = list[IResourceLoader]([ResourceLoader()])

  def load(self, source: Any, *args, **kwds) -> bytes:
    for loader in self.__loaders:
      try:
        return loader.load(source, *args, **kwds)
      except:
        continue
    raise AssertionError(f"Cannot load resource {str(source):20s}")
