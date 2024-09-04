from SparkCleaner.Strategies.base import BaseCleaningStrategy, DataFrame

class DropMissingValuesStrategy(BaseCleaningStrategy):
    def clean(self, df: DataFrame) -> DataFrame:
        initial_count = df.count()
        df_cleaned = df.dropna(subset=self.columns)
        final_count = df_cleaned.count()
        
        if initial_count > final_count:
            for column in self.columns:
                missing = df.filter(df[column].isNull())
                for row in missing.collect():
                    self.logger.log_error(row['__index'], column, f'missing_value: {row[column]}')
        
        return df_cleaned
    
    