import io
import rawpy
from PIL import Image
from typing import Any
from pillow_heif import register_heif_opener
from . import Resource
register_heif_opener()



class ImageResource(Resource):
  """
  Image resource.
  """
  @property
  def image(self) -> Image.Image:
    return self._image

  def __init__(self, source: Any, *args, **kwargs) -> None:
    super().__init__(source, *args, **kwargs)
    buffer = io.BytesIO(self.data)
    try:
      self._image = Image.open(buffer)
    except:
      buffer.seek(0)
      try:
        with rawpy.imread(buffer) as raw:
          thumb = raw.extract_thumb()
        if thumb.format == rawpy.ThumbFormat.JPEG:
          buffer = io.BytesIO(thumb.data)
          self._image = Image.open(buffer)
        elif thumb.format == rawpy.ThumbFormat.BITMAP:
          self._image = Image.fromarray(thumb.data)
      except:
        raise AssertionError(f'Cannot load image asset from {str(source):20s}')  
