# SPARK JOB FOR INVENTORY DATA TRANSFORMATION

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, when

def run_spark_job():
    """
    Main function to run the Spark job.
    Added logic to handle non-product items and negative final stock.
    """
    # --- 1. Initialize Spark Session ---
    spark = SparkSession.builder \
        .appName("RetailInventoryTransform") \
        .master("local[*]") \
        .getOrCreate()
    
    print("Spark Session created successfully")

    # --- 2. Load Data ---
    data_path = "/opt/bitnami/spark/data/online_retail_II.csv"
    df = spark.read.csv(data_path, header=True, inferSchema=True)
    print(f"Dataset loaded successfully from {data_path}")
    df.cache()

    # --- 3. Data Transformation ---
    print("Starting data transformation process...")

    # Filter out non-product codes (heuristic: must contain at least one digit)
    # Also filter records with null values and zero/negative price
    cleaned_df = df.filter(col("Price") > 0) \
                   .filter(col("StockCode").isNotNull()) \
                   .filter(col("StockCode").rlike(".*[0-9].*")) \
                   .filter(col("Description").isNotNull())

    # Calculate net stock
    inventory_df = cleaned_df.groupBy("StockCode", "Description") \
                               .agg(_sum("Quantity").alias("net_stock"))

    # Correct negative stock to 0, as physical stock cannot be negative
    final_inventory_df = inventory_df.withColumn(
        "final_stock",
        when(col("net_stock") < 0, 0).otherwise(col("net_stock"))
    ).select("StockCode", "Description", "final_stock")
    
    print("Data transformation complete. Sample result:")
    final_inventory_df.show(5)

    # --- 4. Save Result to PostgreSQL ---
    print("Starting to save data to PostgreSQL...")
    
    postgres_url = "jdbc:postgresql://postgres_db:5432/airflow"
    postgres_properties = {
        "user": "airflow",
        "password": "airflow",
        "driver": "org.postgresql.Driver"
    }

    final_inventory_df.write.jdbc(
        url=postgres_url,
        table="inventory_stock",
        mode="overwrite",
        properties=postgres_properties
    )

    print("Data successfully saved to 'inventory_stock' table in PostgreSQL")

    spark.stop()

if __name__ == "__main__":
    run_spark_job()