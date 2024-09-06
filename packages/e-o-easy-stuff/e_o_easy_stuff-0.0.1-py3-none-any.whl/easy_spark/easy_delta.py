from pyspark.sql import SparkSession
from easy_spark.table_path import TablePath
from delta.tables import *


class EasyDeltaPath:
    _spark: SparkSession = None

    def __init__(self, delta_path=None, spark: SparkSession = None):
        self._delta_path = delta_path
        self.hadoop_conf = None
        self.fs = None
        if spark is not None:
            EasyDeltaPath._spark = spark
            self.init_values()
        pass

    def init_values(self) -> 'EasyDeltaPath':
        self.hadoop_conf = EasyDeltaPath._spark._jsc.hadoopConfiguration()
        self.fs = EasyDeltaPath._spark._jvm.FileSystem.get(self.hadoop_conf)
        full_path = self._delta_path.toString()
        path = EasyDeltaPath._spark._jvm.Path(full_path)
        return self

    @property
    def delta_path(self):
        return self._delta_path

    def from_path(self, path: TablePath) -> 'EasyDeltaPath':
        self._delta_path = DeltaTable.forPath(EasyDeltaPath._spark, path.path)
        return self
