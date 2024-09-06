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

    def from_table_path(self, path: TablePath, df_format="delta") -> 'EasyDF':
        self._df = EasyDF._spark.read.format(df_format).load(path.path)
        return self

    def from_path(self, path: str, df_format="delta") -> 'EasyDF':
        self._df = EasyDF._spark.read.format(df_format).load(path)
        return self

    def from_dict(self, records: dict, schema: StructType = None) -> 'EasyDF':
        self._df = EasyDF._spark.createDataFrame([Row(**records)], schema)
        return self

    def from_list(self, records: list[dict], schema: StructType = None) -> 'EasyDF':
        self._df = EasyDF._spark.createDataFrame(records, schema)
        return self

    def from_lh_name_path(self, name: str, table_name: str, limt: int = None, df_format="delta") -> 'EasyDF':
        if limt:
            self._df = EasyDF._spark.sql(f"SELECT * FROM {name}.{table_name} LIMIT {limt}")
        else:
            self._df = EasyDF._spark.sql(f"SELECT * FROM {name}.{table_name}")

        return self

    def append_from_dict(self, record: dict) -> 'EasyDF':
        self._df = self._df.union(EasyDF._spark.createDataFrame([Row(**record)], self._df.schema))
        return self

    def save_from_table_path(self, path: TablePath, df_format="delta", mode="overwrite",
                             merge_option: str = "overwriteSchema") -> 'EasyDF':
        self._df.write.format(df_format).mode(mode).option(merge_option, "true").save(path.path)
        return self

    def save_as_table(self, path: str, df_format="delta", mode="overwrite",
                      merge_option: str = "overwriteSchema") -> 'EasyDF':
        self._df.write.format(df_format).mode(mode).option(merge_option, "true").saveAsTable(path)
        return self
