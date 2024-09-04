from SparkCleaner.Strategies.base import BaseCleaningStrategy, DataFrame

class FilteringStrategy(BaseCleaningStrategy):
    """
    A strategy for filtering rows in a DataFrame based on specified conditions.

    Inherits from:
        BaseCleaningStrategy

    Args:
        conditions (list of pyspark.sql.Column, optional): List of conditions to apply for filtering.
            Each condition should be a PySpark Column expression that evaluates to a boolean.

    Example:
        conditions = [
            col("Price") > 10,
            col("Product").isNotNull()
        ]
        This example will filter rows where the "Price" is greater than 10 and "Product" is not null.

    Methods:
        clean(df: DataFrame) -> DataFrame:
            Applies the filtering conditions to the provided DataFrame.
    """
    def __init__(self, conditions: list = None):
        super().__init__(conditions)
        self.conditions = conditions if conditions else []

    def clean(self, df: DataFrame) -> DataFrame:
        combined_condition = None        
        for condition in self.conditions:
            if (condition is not None) and (combined_condition is None):
                combined_condition = condition
            if (condition is not None) and (combined_condition is not None):
                combined_condition = combined_condition & condition 
            if (condition is None) and (combined_condition is None):
                return df
        
        df = df.filter(condition=combined_condition)
        return df
