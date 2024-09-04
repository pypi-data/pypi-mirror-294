# SparkCleaner Documentation

## Overview          
**Disclaimer: this software is not stable yet**
--------------     
SparkCleaner is a Python library for data cleaning using PySpark. It provides various cleaning strategies, a pipeline for applying these strategies, and a logging mechanism for tracking errors and issues.

## Cleaning Strategies

1. **DropDuplicatesStrategy**
   - **Purpose**: Removes duplicate rows based on specified columns.
   - **Method**: `clean(df: DataFrame) -> DataFrame`
   - **Logs**: Logs errors for rows identified as duplicates.

2. **DropMissingValuesStrategy**
   - **Purpose**: Removes rows with missing values in specified columns.
   - **Method**: `clean(df: DataFrame) -> DataFrame`
   - **Logs**: Logs errors for missing values in specified columns.

3. **FilterNegativeValuesStrategy**
   - **Purpose**: Filters out rows where specified columns have non-positive values.
   - **Method**: `clean(df: DataFrame) -> DataFrame`
   - **Logs**: Logs errors for negative values in specified columns.

4. **ValidateColumnTypesStrategy**
   - **Purpose**: Ensures columns have the expected data types.
   - **Method**: `clean(df: DataFrame) -> DataFrame`
   - **Logs**: Logs errors for type mismatches.

5. **ValidateDatesStrategy**
   - **Purpose**: Validates dates in specified columns against a given format.
   - **Method**: `clean(df: DataFrame) -> DataFrame`
   - **Logs**: Logs errors for invalid dates.

6. **ValidateRegexStrategy**
   - **Purpose**: Ensures column values match specified regex patterns.
   - **Method**: `clean(df: DataFrame) -> DataFrame`
   - **Logs**: Logs errors for values not matching the regex.

7. **FilteringStrategy**
   - **Purpose**: Filters rows based on specified boolean conditions.
   - **Method**: `clean(df: DataFrame) -> DataFrame`

8. **FillNaStrategy**
   - **Purpose**: Replaces missing values with specified default values.
   - **Method**: `clean(df: DataFrame) -> DataFrame`

## Cleaning Pipeline

- **Class**: `CleaningPipeline`
- **Methods**:
  - `add_strategy(strategy: BaseCleaningStrategy | list[BaseCleaningStrategy])`: Adds a cleaning strategy or list of strategies.
  - `set_dataframe(df: DataFrame)`: Sets the DataFrame to be cleaned and adds an `__index` column.
  - `run() -> DataFrame`: Applies all strategies to the DataFrame and returns the cleaned DataFrame.
  - `get_report() -> str`: Returns a JSON report of all logged errors.

## Logging
- **Class**: `Logger`
- **Purpose**: Records errors encountered during the cleaning process.
- **Method**: `log_error(index, column, message)`: Logs errors with details.

### Usage Example

```python
from SparkCleaner import *
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType

data = [
    (1, "Alice", 30, "2024-07-01", "alice@example.com"),
    (2, "Bob", None, "2024-07/02", "bob@example"), # null in age col
    (3, "Charlie", 25, "invalid_date", None), # empty email and invalid date
    (4, "David", -5, "2024-07-04", "david@example.com"),
    (5, "Eve", 22, "2024-07-05", "eve@example.com"),
    (5, "Eve", 22, "2024-07-05", "eve@example.com"),
    (5, "Eve", '22', "05-07-2024", "eve@example.com"),  #string value in age column
]
schema = ["id", "name", "age", "date", "email"]

spark = SparkSession.builder \
    .appName("DataCleaningTests") \
    .master("local[*]") \
    .getOrCreate()

df = spark.createDataFrame(data, schema=schema)
cleaning_pipeline = CleaningPipeline()
strategies_pipeline =[
    DropDuplicatesStrategy(columns=df.columns),
    ValidateRegexStrategy(columns=["email"], patterns={'email': '^[\\w.%+-]+@[\\w.-]+\\.[a-zA-Z]{2,}$'}),
    DropMissingValuesStrategy(columns=["age"]),
    FilterNegativeValuesStrategy(columns=["age"]),
    ValidateColumnTypesStrategy(columns=df.columns, 
            expected_types={
                'age': IntegerType(), 
                'email': StringType()
                # add more if needed
    }),
    ValidateDatesStrategy(columns=["date"], date_format='yyyy-MM-dd'),
]


cleaning_pipeline.add_strategy(strategy=strategies_pipeline)
cleaning_pipeline.set_dataframe(df = df)

cleaned_df = cleaning_pipeline.run()
errors_report = cleaning_pipeline.get_report()
```