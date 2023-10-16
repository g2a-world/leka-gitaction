# Databricks notebook source
# MAGIC %md
# MAGIC ###Ingest race.csv File

# COMMAND ----------

# MAGIC %md
# MAGIC #####Step 1 - Read the CSV file using the spark dataframe reader

# COMMAND ----------

from pyspark.sql.types import *
from pyspark.sql.functions import *

# COMMAND ----------

race_schema = StructType(fields = [StructField("raceId", IntegerType(), False),
                                      StructField("year", StringType(), True),
                                      StructField("round", IntegerType(), True),
                                      StructField("circuitId", IntegerType(), True),
                                      StructField("name", StringType(), True),
                                      StructField("date", StringType(), True),
                                      StructField("time", StringType(), True),
                                      StructField("url", StringType(), True)
                                    ]
                            )


# COMMAND ----------

race_df = spark.read \
    .option("header", True) \
        .schema(race_schema) \
            .csv("/mnt/formula1dlg2a/raw/races.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC #####Step 2 - Select only the required columns

# COMMAND ----------

race_selected_df = race_df.select(col('raceId'), col('year'), col('round'), col('circuitId'), col('name'), col('date'), col('time'))

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 3 - Renaming columns

# COMMAND ----------

race_renamed_df = race_selected_df.withColumnRenamed("raceId", "race_id") \
                                  .withColumnRenamed("year", "race_year") \
                                  .withColumnRenamed("circuitId", "circuit_id") \
                                  .withColumn("race_timestamp", to_timestamp(concat(col("date"), lit(' '), col("time")), 'yyyy-MM-dd HH:mm:ss')) \
                                  .withColumn("ingestion_data", current_timestamp())


# COMMAND ----------

race_renamed_select = race_renamed_df.select(col("race_id"), col("race_year"), col("round"), col("name"), col("race_timestamp"), col("ingestion_data"))

# COMMAND ----------

# MAGIC %md
# MAGIC #####Step 5 - Write the final data to ADLS storage

# COMMAND ----------

race_renamed_select.write.mode('overwrite').parquet("/mnt/formula1dlg2a/processed/races")

# COMMAND ----------

display(spark.read.parquet("/mnt/formula1dlg2a/processed/races"))

# COMMAND ----------


