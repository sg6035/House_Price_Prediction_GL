import os
import warnings
import configparser

import pyspark
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql import functions as F

from pyspark.ml.regression import  GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator

warnings.filterwarnings("ignore")

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

configParser = configparser.RawConfigParser()   
configParser.read(r'./configurations.txt')
config_dict = dict(configParser.items('feature_process'))

preprocessed_data_csv = config_dict['preprocessed_data_csv']
feature_scaled_pipeline_path = config_dict['feature_scaled_pipeline']

sc= pyspark.SparkContext()
spark = SparkSession.builder.getOrCreate()
df = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferSchema", "true") \
                .load(preprocessed_data_csv)

feature_process_model = PipelineModel.load(feature_scaled_pipeline_path)
scaled_df = feature_process_model.transform(df)

data = scaled_df.select(
    F.col("scaledfeatures").alias("features"),
    F.col("SalePrice").alias("label"),
)

trainDF, testDF =  data.randomSplit([0.8, 0.2], seed = 22)

modelName = 'GBTRegressor'

regression_model = GBTRegressor(maxDepth=3, maxIter=100)
reg_model_fit = regression_model.fit(trainDF)
predictionDF = reg_model_fit.transform(testDF)

rmse_evaluator = RegressionEvaluator(predictionCol="prediction", labelCol="label", metricName="rmse")
rmse = rmse_evaluator.evaluate(predictionDF)
print("RMSE: " + str(rmse))

r2_evaluator = RegressionEvaluator(predictionCol="prediction", labelCol="label", metricName="r2")
r2 = r2_evaluator.evaluate(predictionDF)
print("R2 Score: " + str(r2))