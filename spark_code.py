#Code to load dataset to Spark:

%spark
val csvDF = spark.read.option("header", "true")
                      .option("inferSchema", "true")
                      .csv("hdfs://namenode:8020/iot_data/quakes-cleaned.csv")
csvDF.show(truncate = false)

#Code to perform filter:

%spark
import org.apache.spark.sql.functions.avg
 
val aggDF = csvDF.groupBy("place")
  .agg(avg("mag").alias("avg_mag"))
aggDF.show(truncate = false)

#Save the processed data back to HDFS:

%spark
aggDF.write.option("header", "true").csv("hdfs://namenode:8020/iot_data/aggregated_quakes_data")
