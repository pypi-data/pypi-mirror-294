from SparkCleaner.Strategies.base import BaseCleaningStrategy, DataFrame

class FillNAStrategy(BaseCleaningStrategy):
    def __init__(self, fill_values: dict = None):
        self.fill_values = fill_values if fill_values else {}

    def clean(self, df: DataFrame) -> DataFrame:
        return df.fillna(self.fill_values)
