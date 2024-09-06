from pyspark.sql import SparkSession
from pyspark.sql.functions import *

from easy_spark.easy_delta import EasyDeltaPath
from easy_spark.easy_df import EasyDF


def create_container(spark: SparkSession) -> tuple[
    Callable[[DataFrame | None], EasyDF], Callable[[None], EasyDeltaPath]]:
    _spark = spark

    def create_easy_df(df: DataFrame = None):
        return EasyDF(df, _spark)

    def create_easy_delta(delta_path=None):
        return EasyDeltaPath(delta_path, _spark)

    return (
        create_easy_df,
        create_easy_delta
    )
