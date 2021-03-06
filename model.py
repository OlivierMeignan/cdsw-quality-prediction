from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.ml import PipelineModel

spark = SparkSession.builder \
      .appName("quality-model") \
      .master("local[*]") \
      .getOrCreate()
    
model = PipelineModel.load("file:///home/cdsw/models/spark")


schema = StructType([StructField("fixedAcidity", DoubleType(), True),     
  StructField("volatileAcidity", DoubleType(), True),     
  StructField("citricAcid", DoubleType(), True),     
  StructField("residualSugar", DoubleType(), True),     
  StructField("chlorides", DoubleType(), True),     
  StructField("freeSulfurDioxide", DoubleType(), True),     
  StructField("totalSulfurDioxide", DoubleType(), True),     
  StructField("density", DoubleType(), True),     
  StructField("pH", DoubleType(), True),     
  StructField("sulphates", DoubleType(), True),     
  StructField("Alcohol", DoubleType(), True)
])


def predict(args):
  split=args["feature"].split(";")
  features=[list(map(float,split[:11]))]
  features_df = spark.createDataFrame(features, schema)
  result=model.transform(features_df).collect()[0].prediction
  if result == 1.0:
    return {"result": "Bad"}
  else:
    return {"result" : "Good"}
  
# pre-heat the model
predict({"feature": "7.4;0.7;0;1.9;0.076;11;34;0.9978;3.51;0.56;9.4"})