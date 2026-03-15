# Global Terrorism Database Casualty Analysis

# Hadoop MapReduce Big Data Project

[![Hadoop](https://img.shields.io/badge/Hadoop-3.3.6-yellow)](https://hadoop.apache.org/docs/r3.3.6/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://docs.python.org/3.8/)
[![Java](https://img.shields.io/badge/Java-17-orange)](https://docs.oracle.com/en/java/javase/17/)
[![Dataset](https://img.shields.io/badge/Dataset-GTD-red)](https://www.kaggle.com/datasets/START-UMD/gtd)
[![Platform](https://img.shields.io/badge/Platform-HDFS-lightgrey)](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)

Cloud Computing Assignment
University of Ruhuna – Faculty of Engineering
EC7204 | Semester 7 | 2026

---

# Table of Contents

1. Project Overview
2. Dataset Description
3. System Architecture
4. MapReduce Workflow
5. Project Structure
6. Installation Requirements
7. Running the Project
8. Example Output
9. Key Insights
10. Performance Observations
11. Future Improvements
---

# 1. Project Overview

This project performs **large-scale terrorism casualty analysis** using the **Hadoop MapReduce distributed computing framework**.

The system processes the **Global Terrorism Database (GTD)** to analyze how different **attack types affect casualties worldwide**.

The MapReduce job calculates:

* Total incidents per attack type
* Total number of people killed
* Total number of people wounded
* Average kills per incident
* Average wounds per incident

This demonstrates how **Big Data technologies can process real-world datasets efficiently**.

---

# 2. Dataset Description

Dataset: Global Terrorism Database (GTD)

Source
https://www.kaggle.com/datasets/START-UMD/gtd

Dataset statistics

| Property      | Value       |
| ------------- | ----------- |
| Total Records | 181,691     |
| Time Range    | 1970 – 2017 |
| Columns       | 135         |
| Dataset Size  | ~162MB      |

Important fields used in the analysis:

| Column          | Meaning        |
| --------------- | -------------- |
| attacktype1_txt | Attack type    |
| nkill           | Number killed  |
| nwound          | Number wounded |

---

# 3. System Architecture
The system processes the Global Terrorism Dataset using the Hadoop MapReduce framework in a pseudo-distributed environment. The pipeline begins by storing the dataset in the Hadoop Distributed File System (HDFS), which manages data blocks locally while simulating a distributed environment.

Big Data Pipeline

```mermaid
flowchart TD
    subgraph Execution_Flow [MapReduce Pipeline for GTD Analysis]
    A[Raw GTD Dataset] --> B[Upload to HDFS]

    B --> C1[Mapper Task 1]
    B --> C2[Mapper Task 2]

    C1 --> D[Shuffle and Sort]
    C2 --> D

    D --> E[Reducer Task]

    E --> F[Final Aggregated Results]

    F --> G[results_clean.txt]
    end

    %% Style definitions
    style A fill:#ffffff,stroke:#333,stroke-width:2px,color:#000
    style B fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    style C1 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    style C2 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    style D fill:#fffde7,stroke:#fbc02d,stroke-width:2px,color:#000
    style E fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#000
    style F fill:#ffffff,stroke:#333,stroke-width:2px,color:#000
    style G fill:#f5f5f5,stroke:#333,stroke-width:2px,color:#000
```

The dataset is stored in HDFS across a single-node cluster. The MapReduce job splits the dataset into input splits (based on HDFS block size), which are processed as individual Mapper Tasks on the same machine. Following the mapper phase, intermediate key-value pairs are Shuffled and Sorted automatically by the framework before being aggregated in the Reducer Phase. While this setup runs on a single physical node, it accurately simulates the logic of a multi-node cluster where tasks would run on separate DataNodes in parallel to provide linear scalability.

---

# 4. MapReduce Workflow

## Mapper Phase

Each CSV row is processed and emits:

AttackType → (kills, wounds, incident_count)

Example:

Bombing → (3,10,1)
Bombing → (1,5,1)
Bombing → (0,2,1)
---

## Shuffle and Sort

Hadoop groups records by **Attack Type**.

Example grouped records:

Bombing → [(3,10,1), (1,5,1), (0,2,1)]
---

## Reducer Phase

The reducer calculates:

Total Incidents
Total Kills
Total Wounds
Average Kills per Incident
Average Wounds per Incident

Final output format:

AttackType | Incidents | TotalKilled | TotalWounded | AvgKilled | AvgWounded

Example grouped records:

Bombing → Incidents:3
           TotalKilled:4
           TotalWounded:17
           AvgKilled:1.33
           AvgWounded:5.67
---

# 5. Project Structure

```text
gtd_mapreduce_project
│
│
├── src
│   ├── mapper.py
│   └── reducer.py
│
├── results
│   └── results.txt
│   └── result_cleans.txt
│
├── Evidences of Execution.zip
│
├── report
│   └── Take Home Assignment_23rd-Group10.pdf
│
└── README.md
```

---

## 6. Installation Requirements

Install the following:

- Hadoop 3.3.6
- Python 3.8+
- Java 17
- Ubuntu / WSL

Check installations:

```bash
java -version
hadoop version
python3 --version
```

---

## 7. Running the Project

### Step 1: Start Hadoop

```bash
start-dfs.sh
start-yarn.sh
jps
```

Expected processes:

- NameNode
- DataNode
- ResourceManager
- NodeManager
- SecondaryNameNode

---

### Step 2: Upload Dataset

```bash
hdfs dfs -mkdir -p /user/gtd/input
hdfs dfs -put dataset/globalterrorismdb_0718dist.csv /user/gtd/input/
```

---

### Step 3: Run Hadoop Streaming Job

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
-input /user/gtd/input/globalterrorismdb_0718dist.csv \
-output /user/gtd/output \
-mapper "python3 mapper.py" \
-reducer "python3 reducer.py" \
-file mapper.py \
-file reducer.py
```

---

### Step 4: View Output

```bash
hdfs dfs -cat /user/gtd/output/part-00000
```

Save results:

```bash
hdfs dfs -get /user/gtd/output/part-00000 results.txt
```

---
## 8. Example Output

| Attack Type | Incidents | TotalKilled | TotalWounded | AvgKilled | AvgWounded |
|:---|:---:|:---:|:---:|:---:|:---:|
| Bombing/Explosion | 88,255 | 157,321 | 2,503 | 1.78 | 0.03 |
| Armed Assault | 42,669 | 160,297 | 482 | 3.76 | 0.01 |
| Assassination | 19,312 | 24,920 | 78 | 1.29 | 0.00 |
| Facility/Infrastructure Attack | 10,355 | 3,642 | 342 | 0.35 | 0.03 |
| Hijacking | 659 | 3,718 | 48 | 5.64 | 0.07 |
| Hostage Taking (Barricade Incident) | 991 | 4,478 | 149 | 4.52 | 0.15 |
| Hostage Taking (Kidnapping) | 11,158 | 24,231 | 45 | 2.17 | 0.00 |
| Unarmed Assault | 1,015 | 880 | 876 | 0.87 | 0.86 |
| Unknown | 7,276 | 32,381 | 33 | 4.45 | 0.00 |
| **All** | **181,690** | **411,868** | **4,956** | **2.27** | **0.03** |
---

## 9. Key Insights

- **Bombing attacks dominate the dataset** with the highest incident count.
- **Armed assaults show the highest lethality per attack**.
- **Assassination attacks show a high kill-to-wound ratio**, indicating targeted operations.
- **Infrastructure attacks produce minimal casualties**.

---

## 10. Performance Observations

- **Dataset processed**: 181,690 records
- **Cluster**: Hadoop pseudo-distributed (single node)
- **Execution time**: approximately 4–6 minutes
- **Mapper stage** consumed most processing time due to CSV parsing
- In a multi-node cluster, Hadoop would distribute mappers across nodes, providing **linear scalability**.

---


## 11. Future Improvements

Possible improvements include:

- Add time-series analysis (casualties per year)
- Analyze attacks by country or region
- Deploy the job on AWS EMR or Google Dataproc
- Replace MapReduce with Apache Spark for faster processing
- Build a visualization dashboard for policymakers

---







