# Retail Inventory Transparency - Data Engineering Final Project

## Project Overview

This project addresses a fundamental problem in traditional retail store operations: the discrepancy between inventory data recorded in Point of Sales (PoS) systems and actual physical stock conditions. This data platform performs automated ETL (Extract, Transform, Load) processes, cleans raw transaction data, and presents accurate inventory data through interactive dashboards.

## Tech Stack & Architecture

This data pipeline architecture uses modern technologies running in Docker containers:

**Tech Stack:**
* **Containerization**: Docker & Docker Compose
* **Workflow Orchestration**: Apache Airflow
* **Data Processing**: Apache Spark (PySpark)
* **Data Storage**: PostgreSQL
* **Data Visualization**: Metabase

**Architecture Flow:**
The workflow begins with Airflow scheduling and triggering Spark jobs. Spark processes raw data from CSV files, performs transformations, then stores results in PostgreSQL. Finally, Metabase connects to PostgreSQL to present data in dashboard format.

## Project Structure
```
final-project-inventory/
├── dags/
│   └── inventory_pipeline_dag.py
├── spark_jobs/
│   └── transform_job.py
├── data/
│   └── online_retail_II.csv
├── docker-compose.yml
├── Dockerfile.airflow
└── README.md
```

## Setup & Installation

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your machine

### Configuration Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/arifnrsk/Inventory-Transparency-in-Retail.git
   cd Inventory-Transparency-in-Retail
   ```

2. **Place Dataset**
   Download the `Online Retail II UCI` dataset from [Kaggle](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci) and place the `online_retail_II.csv` file in the `./data/` folder.

3. **Generate Secret Key**
   Airflow requires a consistent secret key. Generate one using:
   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```

4. **Update docker-compose.yml**
   Replace the `AIRFLOW__WEBSERVER__SECRET_KEY` value with your generated key in all Airflow services.

## How to Run

1. **Start All Services**
   ```bash
   docker-compose up -d --build
   ```

2. **Access Services**
   * **Apache Airflow**: `http://localhost:8080` (admin/admin)
   * **Spark Master UI**: `http://localhost:8081`
   * **Metabase**: `http://localhost:3000`

3. **Run the Pipeline**
   * Open Airflow UI
   * Find DAG: `inventory_transformation_pipeline`
   * Activate the DAG and trigger manually

## Verify Results

Access PostgreSQL to check processed data:
```bash
docker exec -it postgres_db psql -U airflow
```

Query the results:
```sql
SELECT * FROM inventory_stock ORDER BY final_stock DESC LIMIT 10;
```

## Stop Environment

```bash
docker-compose down
```

## Features

- **Automated ETL Pipeline**: Scheduled data processing with Airflow
- **Data Quality Checks**: Filters invalid stock codes and handles negative quantities
- **Scalable Processing**: Spark for efficient large dataset handling
- **Interactive Dashboards**: Metabase for data visualization
- **Containerized Deployment**: Easy setup with Docker Compose

## Data Processing

The pipeline processes retail transaction data by:
1. Loading raw CSV data
2. Filtering valid product codes (regex pattern)
3. Converting negative quantities to zero
4. Aggregating stock by product
5. Storing clean data in PostgreSQL

## Additional Resources

- **Video Presentation**: [Watch the project presentation](https://drive.google.com/file/d/1s5n1j9nDuxk7G-aoqfdeOboRlNvcQ_Bc/view?usp=sharing)
- **Dataset**: [Download Online Retail II dataset](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci)
