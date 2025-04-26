# Dijkstra-s-Algorithm

This project implements Dijkstra's algorithm on a Spark cluster using the Hadoop Distributed File System (HDFS).

Dijkstra's algorithm is a well-known method for finding the shortest paths from a source node to all other nodes in a weighted graph with non-negative edge weights.

## Technologies Used:

- Hadoop (HDFS): Used for distributed data storage, allowing all nodes in the cluster to access the input graph data.

- Apache Spark: Used for parallel processing. Spark reads the graph data from HDFS, partitions it across worker nodes, and performs iterative relaxation steps in parallel to compute the shortest paths


## Microsoft Azure Setup

The project was tested using three virtual machines

    All machines must be on the same network, since Spark communicates internally using hostnames or private IP addresses.

Ensure the following ports are open for inbound traffic
    
    8080 - to access the spark web ui
    7077 - for workers to connect master

Each VM was configured with:

    2 GiB RAM
    2 Data disks

## Java Installation

Search for latest package

    apt search openjdk

Install Java

    sudo apt install openjdk-21-jdk -y

## Spark Installation
Documentation 

    https://spark.apache.org/docs/latest/spark-standalone.html#installing-spark-standalone-to-a-cluster

Download spark - visit (https://downloads.apache.org/spark) for latest version

    wget https://downloads.apache.org/spark/spark-3.x.x/spark-3.x.x-bin-hadoop3.tgz

Extract the package

    tar -xvzf spark-3.x.x-bin-hadoop3.tgz

Rename for simplicity

    mv spark-3.x.x-bin-hadoop3 ~/spark

## Hadoop Installation 

Documentation

    https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/ClusterSetup.html

Download Hadoop - visit (https://downloads.apache.org/hadoop) for latest version

    wget https://downloads.apache.org/hadoop/common/hadoop-3.x.x/hadoop-3.x.x.tar.gz

Extract the package

    tar -xzf hadoop-3.x.x.tar.gz

Rename for simplicity

    mv hadoop-3.x.x ~/hadoop


## Enviroment Configuration

In each VM:

    #java
    export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac)))) 
    export PATH=$PATH:$JAVA_HOME/bin
    
    #spark
    export SPARK_HOME=~/spark
    export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

    #hadoop
    export HADOOP_HOME=~/hadoop
    export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

Edit config files for hadoop

    cd $HADOOP_HOME/etc/hadoop

    #Add to files:

    core-site.xml
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://<private-ip >:9000</value>
    </property>

    hdfs-site.xml
    <property>
        <name>dfs.replication</name>
        <value>2</value>  <!-- or 1 for testing -->
    </property>

    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/VM_USER/hadoop_data/hdfs/namenode</value>
    </property>

    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/VM_USER/hadoop_data/hdfs/datanode</value>
    </property>

## Start Spark&Hadoop Manually

In Master: 

    $SPARK_HOME/sbin/start-master.sh
    hdfs --daemon start namenode

In Workers:

    $SPARK_HOME/sbin/start-worker.sh spark:<master-public-ip>:7077
    hdfs --daemon start datanode

## To run file

Clone repo

    git clone https://github.com/iKeiNagai/Dijkstra-s-Algorithm.git

Navigate into folder

    cd Dijkstra-s-Algorithm

move weighted_graph.txt to hdfs:

    hdfs dfs -put weighted_graph.txt /graph/weighted_graph.txt

Submit the job using spark

    $SPARK_HOME/bin/spark-submit \
    --master spark://<master-public-ip>:7077 \
    dijkstras_algorithm.py

## Debugging

To check env variable are set

    echo $PATH
    echo $SPARK_HOME
    echo $HADOOP_HOME

To check hadoop datanodes details

    hdfs dfsadmin -report

To check spark workers and monitor jobs

    http://<master-public-ip>:8080

To check running processes

    jps 
