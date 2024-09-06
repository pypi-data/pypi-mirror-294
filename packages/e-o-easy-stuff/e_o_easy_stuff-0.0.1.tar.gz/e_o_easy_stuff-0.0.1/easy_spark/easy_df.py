from pyspark.sql import Row
from pyspark.sql.functions import *
from easy_spark.table_path import TablePath
from pyspark.sql import SparkSession


class EasyDF:
    _spark: SparkSession = None

    # Constructor
    def __init__(self, df: DataFrame = None, spark: SparkSession = None):
        self._df: DataFrame = df
        if spark is not None:
            EasyDF._spark = spark

    @property
    def df(self) -> DataFrame:
        return self._df

    def from_path(self, path: TablePath, df_format="delta") -> 'EasyDF':
        self._df = EasyDF._spark.read.format(df_format).load(path.path)
        return self

    def from_relative_path(self, path: str, df_format="delta") -> 'EasyDF':
        self._df = EasyDF._spark.read.format(df_format).load(path)
        return self

    def append_from_dict(self, record: dict) -> 'EasyDF':
        self._df = self._df.union(EasyDF._spark.createDataFrame([Row(**record)], self._df.schema))
        return self
