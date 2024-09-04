from pyspark.sql import DataFrame
from SparkCleaner.logger.logger import Logger 

class BaseCleaningStrategy:
    def __init__(self, columns: list = None):
        self.columns = columns
        self.errors = []
        self.logger = Logger()

    def clean(self, df: DataFrame) -> DataFrame:
        raise NotImplementedError

    def get_report(self) -> str:
        return self.logger.get_logs()

    def whoami(self)->str:
        return self.__class__.__name__ 