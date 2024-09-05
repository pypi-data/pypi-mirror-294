import io
import pandas as pd
from typing import Any
from . import Resource


READERS = (
  pd.read_csv,
  pd.read_excel,
  pd.read_json,
  pd.read_xml,
  pd.read_sql,
  pd.read_stata,
  pd.read_sql_query,
  pd.read_sql_table,
  pd.read_spss,
  pd.read_html,
  pd.read_parquet,
  pd.read_hdf,
  pd.read_pickle,
  pd.read_gbq,
  pd.read_fwf,
  pd.read_orc,
  pd.read_feather,
  pd.read_sas,
  pd.read_table
)


class DataResource(Resource):
  """
  Dataframe resource.
  """
  @property
  def dataframe(self) -> pd.DataFrame:
    return self._dataframe

  def __init__(self, source: Any, *args, **kwargs) -> None:
    super().__init__(source, *args, **kwargs)
    for reader in READERS:
      buffer = io.BytesIO(self.data)
      try:
        self._dataframe = reader(buffer)
        return
      except:
        continue
    raise AssertionError(f"Cannot load dataframe: {str(source):20s}")
