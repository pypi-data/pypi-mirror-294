from pyspark.sql import SparkSession
from easy_spark.easy_df import EasyDF
from easy_spark.table_path import TablePath
from pyspark.sql.functions import *
from delta.tables import *


class EasyDeltaPath:
    _spark: SparkSession = None

    def __init__(self, path: str = None, spark: SparkSession = None):
        EasyDeltaPath._spark = spark
        self._delta_path = None

        self.path = path
        self.hadoop_conf = None
        self.fs = None

        if spark and path:
            self._delta_path = DeltaTable.forPath(EasyDeltaPath._spark, self.path)
            self.init_values()

    def init_values(self) -> 'EasyDeltaPath':
        self.hadoop_conf = EasyDeltaPath._spark._jsc.hadoopConfiguration()
        self.fs = EasyDeltaPath._spark._jvm.FileSystem.get(self.hadoop_conf)
        # full_path = self._delta_path.toString()
        # path = EasyDeltaPath._spark._jvm.Path(full_path)
        return self

    @property
    def delta_path(self):
        return self._delta_path

    def to_easy_df(self) -> EasyDF:
        return EasyDF(self._delta_path.toDF(), EasyDeltaPath._spark)

    def from_table_path(self, path: TablePath) -> 'EasyDeltaPath':
        self.path = path.path
        self._delta_path = DeltaTable.forPath(EasyDeltaPath._spark, self.path)
        self.init_values()
        return self

    def update(self, keys: dict[str, any], values: dict[str, any]) -> 'EasyDeltaPath':
        conditions = ""
        for key, value in keys.items():
            if conditions == "":
                conditions += f"col('{key}') == '{value}'"
            else:
                conditions += f" & col('{key}') == '{value}'"

        sets = {k: lit(v) for k, v in values.items()}

        self._delta_path.update(
            condition=conditions,
            set=sets
        )
        return self

    def update_by_condition(self, condition: str, values: dict[str, any]) -> 'EasyDeltaPath':
        sets = {k: lit(v) for k, v in values.items()}
        self._delta_path.update(
            condition=condition,
            set=sets
        )
        return self

    def delete(self, keys: dict[str, any] = None,
               multiple_keys: list[tuple[str, list]] = None) -> 'EasyDeltaPath':
        conditions = ""

        if keys:
            for key, value in keys.items():
                if conditions == "":
                    conditions += f"col('{key}') == '{value}'"
                else:
                    conditions += f" & col('{key}') == '{value}'"

        if multiple_keys:
            for key in multiple_keys:
                if conditions == "":
                    conditions += f"{key[0]} in {tuple(key[1])}"
                else:
                    conditions += f" and {key[0]} in {tuple(key[1])}"

        self._delta_path.delete(condition=conditions)
        return self

    def delete_by_multiple_keys(self, key: str, key_values: list) -> 'EasyDeltaPath':
        self._delta_path.delete(f"{key} in {tuple(key_values)}")
        return self

    def delete_by_condition(self, condition: str) -> 'EasyDeltaPath':
        self._delta_path.delete(condition)
        return self

    def merge(self, keys: list[str], df: DataFrame, add_missing_coloumns=True,
              add_missing_coloumns_to_current=False) -> 'EasyDeltaPath':
        current_df = self._delta_path.toDF()
        df_coloumns = df.columns
        current_coloumns = current_df.columns

        if add_missing_coloumns:
            for current_coloumn in current_coloumns:
                if current_coloumn not in df_coloumns:
                    df = df.withColumn(current_coloumn, lit(None).cast(current_df.schema[current_coloumn].dataType))

        if add_missing_coloumns_to_current:
            current_df_has_new_columns = False
            for df_colomn in df_coloumns:
                if df_colomn not in current_coloumns:
                    current_df = current_df.withColumn(df_colomn, lit(None).cast(df.schema[df_colomn].dataType))
                    current_df_has_new_columns = True

            if current_df_has_new_columns:
                #TODO: Fix this
                current_df.write.format("delta").mode("overwrite").option('mergeSchema', "true").save(self.path)
                self._delta_path = DeltaTable.forPath(EasyDeltaPath._spark, self.path)

        merge_relationships = [f"A.`{key}` = B.`{key}` and " for key in keys]
        merge_relationships = "".join(merge_relationships)[:-4]

        self._delta_path.alias('A').merge(
            df.alias('B'),
            merge_relationships
        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

        return self
