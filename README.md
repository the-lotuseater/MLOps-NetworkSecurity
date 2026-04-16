# Network Security MLOps Pipeline

## Project Overview
This project establishes a comprehensive MLOps framework designed to automate the end-to-end lifecycle of a network security **Sensor Model**. The pipeline handles everything from multi-source data ingestion and statistical validation to automated model training and cloud-based deployment. By integrating robust feature engineering and CI/CD practices, the system ensures that the predictive model remains accurate and highly available in production environments.

## Key Features
* **Modular Pipeline Architecture:** Implements a component-based structure including Ingestion, Validation, Transformation, Trainer, Evaluation, and Pusher modules.
* **Automated Data Validation:** Features built-in schema checking and statistical **Data Drift** detection to maintain model integrity against evolving network traffic patterns.
* **Advanced Feature Engineering:** Utilizes **KNN Imputation** for missing values, **Robust Scaling** for normalization, and **SMOTE** for addressing class imbalances.
* **Automated Model Factory:** Systematically evaluates multiple model configurations to select and "push" the best-performing iteration to production.
* **Enterprise CI/CD:** Uses **Docker** for containerization and **GitHub Actions** for automated deployment to AWS infrastructure.

## Technology Stack
* **Languages:** Java, JavaScript, Golang, Python (Scikit-learn, NumPy, Pandas, Flask).
* **Databases:** MongoDB (Atlas), Snowflake, OracleDB, Redis, AWS S3.
* **Infrastructure:** AWS (EC2, ECR, App Runner, CloudFormation), Azure.
* **DevOps:** Docker, Kubernetes, GitHub Actions, Git.

## Pipeline Workflow
1.  **Ingestion:** Extracts raw data from local CSVs, S3 buckets, or APIs into MongoDB.
2.  **Validation:** Compares data against established schemas and generates drift reports.
3.  **Transformation:** Performs cleaning, handling of missing values, and feature scaling.
4.  **Training:** Executes the **Model Factory** to find the highest-performing Sensor Model.
5.  **Deployment:** Containerizes the accepted model and deploys it to **AWS EC2** via a CI/CD pipeline.
