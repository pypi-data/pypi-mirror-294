from pyspark.sql import SparkSession
from pyspark.sql.functions import *

from easy_spark.easy_delta import EasyDeltaPath
from easy_spark.easy_df import EasyDF


def easy_create_container(spark: SparkSession) -> tuple[
    Callable[[DataFrame | None], EasyDF], Callable[[str], EasyDeltaPath]]:
    _spark = spark

    def create_easy_df(df: DataFrame = None):
        return EasyDF(df, _spark)

    def create_easy_delta(path: str):
        return EasyDeltaPath(path, _spark)

    return (
        create_easy_df,
        create_easy_delta
    )
