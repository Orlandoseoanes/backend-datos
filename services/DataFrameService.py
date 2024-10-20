from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import regexp_replace, col
from pyspark.sql.types import FloatType
import os

class DataFrameService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataFrameService, cls).__new__(cls)
            cls._instance.spark = SparkSession.builder \
                .appName("FastAPI_PySpark_DataAnalysis") \
                .config("spark.jars.packages", "com.crealytics:spark-excel_2.12:0.13.7") \
                .getOrCreate()
            cls._instance.df = None
        return cls._instance

    def load_data(self, file_path: str):
        """Loads the data into a DataFrame based on the file type."""
        self._validate_file(file_path)
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.csv':
            self._load_csv(file_path)
        elif file_extension in ['.xls', '.xlsx']:
            self._load_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

        # Clean data after loading
        self._clean_data()

    def _validate_file(self, file_path: str):
        """Validates whether the file exists."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

    def _load_csv(self, file_path: str):
        """Loads a CSV file into a DataFrame."""
        self.df = self.spark.read \
            .option("delimiter", ";") \
            .option("header", True) \
            .csv(file_path)

    def _load_excel(self, file_path: str):
        """Loads an Excel file into a DataFrame."""
        self.df = self.spark.read \
            .format("com.crealytics.spark.excel") \
            .option("header", True) \
            .option("inferSchema", True) \
            .load(file_path)

    def _clean_data(self):
        """Cleans up data in the DataFrame, fixing number formats."""
        if self.df is None:
            raise ValueError("DataFrame has not been loaded yet.")

        columns_to_fix = [col_name for col_name in self.df.columns if col_name not in ["ASIGNATURA", "CICLOS", "AREAS"]]

        for column in columns_to_fix:
            self.df = self.df.withColumn(column, regexp_replace(col(column), "%", ""))
            self.df = self.df.withColumn(column, regexp_replace(col(column), ",", "."))
            self.df = self.df.withColumn(column, col(column).cast(FloatType()))

    def get_dataframe(self) -> DataFrame:
        """Returns the loaded DataFrame."""
        if self.df is None:
            raise ValueError("DataFrame has not been loaded yet.")
        return self.df

    def analyze_data(self):
        """Performs basic data analysis on the DataFrame."""
        if self.df is None:
            raise ValueError("DataFrame has not been loaded yet.")
        
        # Example analysis: Generating a summary of the data
        summary = self.df.describe()
        return summary

    def save_dataframe(self, save_path: str):
        """Saves the DataFrame to the specified path."""
        if self.df is None:
            raise ValueError("DataFrame has not been loaded yet.")
        self.df.write.csv(save_path, header=True)

data_frame_service = DataFrameService()
