# Databricks notebook source
# Ingesting student records - temp file.

csv_student = spark.read \
    .option("inferSchema", True) \
        .option("header", True) \
            .csv("/mnt/formula1dlg2a/student/student_day_1.csv")

display(csv_student)
