# Big Data Infrastructure - Proof of Concept

## Overview
This repository demonstrates a scalable and fault-tolerant **Big Data Infrastructure**. It integrates key tools from the Hadoop ecosystem, including **HDFS**, **Spark**, and **Zeppelin**, to ingest, process, and visualize data efficiently. The infrastructure is designed to handle distributed data processing across multiple nodes, ensuring performance and fault tolerance.

## Architecture
The infrastructure is built with the following components:

1. **HDFS (Hadoop Distributed File System):**
   - Used for distributed storage of large datasets.
   - Configured with one Namenode and two Datanodes.
   - Default replication factor ensures data redundancy across nodes.

2. **Spark:**
   - Handles distributed data processing.
   - Configured to utilize multiple workers (datanodes) for parallel computation.
   - Supports complex queries, aggregations, and data transformations.

3. **Zeppelin:**
   - Provides an interactive environment for querying and visualizing processed data.
   - Integrated with Spark for interactive data analysis.

## Features
- **Data Ingestion:** Ingest CSV data from the local file system into HDFS.
- **Data Storage:** Store data in HDFS with configurable replication for fault tolerance.
- **Data Processing:** Use Spark to query and transform data distributed across multiple nodes.
- **Data Visualization:** Utilize Zeppelin for interactive data exploration and visualization.
- **Scalability:** Scales horizontally by adding more datanodes.
- **Fault Tolerance:** Ensures data availability even if a node fails.

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed on the host machine.
- Basic understanding of Hadoop and Spark.

### Step 1: Start the Infrastructure
1. Clone this repository:
   ```bash
   git clone [repository_url](https://github.com/SETU-IFBD/ca3-GokulT01.git)
   cd big_data_infrastructure
   ```

2. Start the services using Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Verify the services are running:
   ```bash
   docker ps
   ```
   Ensure that the Namenode, Datanodes, Spark Master, Spark Workers, and Zeppelin containers are running.

### Step 2: Upload Data to HDFS
1. Copy your CSV file (e.g., `quakes-cleaned.csv`) into the Namenode container:
   ```bash
   docker cp /path/to/quakes-cleaned.csv namenode:/quakes-cleaned.csv
   ```

2. Exec into the Namenode container:
   ```bash
   docker exec -it namenode bash
   ```

3. Upload the file to HDFS:
   ```bash
   hdfs dfs -mkdir -p /iot_data
   hdfs dfs -put /quakes-cleaned.csv /iot_data/
   ```

4. Verify the file is in HDFS:
   ```bash
   hdfs dfs -ls /iot_data
   ```

### Step 3: Process Data with Spark
1. Open Zeppelin in your browser:
   ```
   http://localhost:8085
   ```

2. Create a new notebook and execute the following code to load data:
   ```python
   %spark
   val csvDF = spark.read.option("header", "true")
                         .option("inferSchema", "true")
                         .csv("hdfs://namenode:8020/iot_data/quakes-cleaned.csv")

   csvDF.printSchema()
   csvDF.show(truncate = false)
   ```

3. Perform aggregations (e.g., average magnitude by location):
   ```python
   %spark
   import org.apache.spark.sql.functions.avg

   val aggDF = csvDF.groupBy("place")
     .agg(
       avg("mag").alias("avg_mag")
     )

   aggDF.show(truncate = false)
   ```

### Step 4: Visualize Data in Zeppelin
1. Use Zeppelin's visualization tools to create charts:
   - Click the "Visualize" icon next to the table output.
   - Choose a chart type (e.g., Bar Chart).
   - Set **X-axis** to `place` and **Y-axis** to `avg_mag`.

### Step 5: Save Processed Data Back to HDFS
1. Save the aggregated data to HDFS:
   ```python
   %spark
   aggDF.write.option("header", "true").csv("hdfs://namenode:8020/iot_data/aggregated_quakes_data")
   ```

2. Verify the saved data:
   ```bash
   hdfs dfs -ls /iot_data/aggregated_quakes_data
   ```

## Monitoring and Fault Tolerance
- **HDFS Web UI:** `http://localhost:9000` (Monitor HDFS and datanode status).
- **Spark Web UI:** `http://localhost:8088` (Monitor Spark jobs and workers).

## Scaling the Infrastructure
To add more datanodes:
1. Update the `docker-compose.yml` file to add more datanodes.
2. Restart the infrastructure:
   ```bash
   docker-compose up -d --scale datanode=<number_of_datanodes>
   ```
3. Verify the new nodes are added in the HDFS Web UI.

## Troubleshooting
- **Permission Issues:** Ensure proper permissions are set on HDFS directories:
  ```bash
  hdfs dfs -chmod -R 775 /iot_data
  ```
- **Replication Issues:** Check and set the replication factor:
  ```bash
  hdfs dfs -setrep -R 2 /iot_data
  ```

## Video presentation link
The link takes to the demostration of my BIG DATA INFRASTRUCTURE [Videolink](https://setuo365-my.sharepoint.com/:v:/g/personal/c00313519_setu_ie/ESM0W-GYop9Etl6GTiV5JBAB186cHhyyzus9nG1rrhIx6w?e=kvy24P&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)

## Conclusion
This repository demonstrates a complete Big Data Infrastructure that integrates HDFS for storage, Spark for processing, and Zeppelin for visualization. It is designed to handle distributed workloads efficiently while ensuring fault tolerance and scalability.



