# # Load the data
# 
# We need to load data from a file in to a Spark DataFrame.
# Each row is a test, and each column contains
# attributes of that test.
#
#     Fields:
#     fixedAcidity: numeric
#     volatileAcidity: numeric
#     citricAcid: numeric
#     residualSugar: numeric
#     chlorides: numeric
#     freeSulfurDioxide: numeric
#     totalSulfurDioxide: numeric
#     density: numeric
#     pH: numeric
#     sulphates: numeric
#     Alcohol: numeric
#     Quality: discrete
#     
#     

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *

conf = SparkConf().setAppName("quality-prediction")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

#set path to data
data_path = "/user/olivier.meignan"
data_file = "NewGBTDataSet.csv"


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
  StructField("Alcohol", DoubleType(), True),     
  StructField("Quality", StringType(), True)
])

data_raw = sqlContext.read.format('com.databricks.spark.csv').option("delimiter",";").load(data_path +'/'+data_file, schema = schema)
data_raw.head()

# # Basic DataFrame operations
# 
# Dataframes essentially allow you to express sql-like statements. We can filter, count, and so on. [DataFrame Operations documentation.](http://spark.apache.org/docs/latest/sql-programming-guide.html#dataframe-operations)

count = data_raw.count()

data_raw.createOrReplaceTempView("data_raw")


qualities = sqlContext.sql("select distinct(Quality), count(*) from data_raw GROUP BY Quality")
qualities.show()


# Remove unvalid data
valid_data = data_raw.filter(data_raw.Quality != "1")

correct = valid_data.filter(valid_data.Quality == 'correct').count()
failed = valid_data.filter(valid_data.Quality == 'failed').count()

"total: %d, corrects: %d, failed: %d " % (count, correct, failed)



# # Seaborn
# 
# Seaborn is a library for statistical visualization that is built on matplotlib.
# 
# Great support for:
# * plotting distributions
# * regression analyses
# * plotting with categorical splitting
# 
# 
# ## Feature Visualization
# 
# The data vizualization workflow for large data sets is usually:
# 
# * Sample data so it fits in memory on a single machine.
# * Examine single variable distributions.
# * Examine joint distributions and correlations.
# * Look for other types of relationships.
# 
# [DataFrame#sample() documentation](http://people.apache.org/~pwendell/spark-releases/spark-1.5.0-rc1-docs/api/python/pyspark.sql.html#pyspark.sql.DataFrame.sample)

# Note: toPandas() => brings data localy !!!
sample_data = valid_data.sample(False, 0.5, 83).toPandas()
sample_data.transpose().head(21)

sc.stop()



# ## Feature Distributions
# 
# We want to examine the distribution of our features, so start with them one at a time.
# 
# Seaborn has a standard function called [dist()](http://stanford.edu/~mwaskom/software/seaborn/generated/seaborn.distplot.html#seaborn.distplot) that allows us to easily examine the distribution of a column of a pandas dataframe or a numpy array.

get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
import seaborn as sb

sb.distplot(sample_data['Alcohol'], kde=False)

# We can examine feature differences in the distribution of our features when we condition (split) our data.
# 
# [BoxPlot docs](http://stanford.edu/~mwaskom/software/seaborn/generated/seaborn.boxplot.html)


sb.boxplot(x="Quality", y="Alcohol", data=sample_data)

# ## Joint Distributions
# 
# Looking at joint distributions of data can also tell us a lot, particularly about redundant features. [Seaborn's PairPlot](http://stanford.edu/~mwaskom/software/seaborn/generated/seaborn.pairplot.html#seaborn.pairplot) let's us look at joint distributions for many variables at once.


example_numeric_data = sample_data[["fixedAcidity", "volatileAcidity",
                                       "citricAcid", "residualSugar", "Quality"]]
sb.pairplot(example_numeric_data, hue="Quality")

sc.stop()