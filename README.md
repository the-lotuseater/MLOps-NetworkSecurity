# Network Security MLOps Pipeline

## Project Overview
This project establishes a comprehensive MLOps framework designed to automate the end-to-end lifecycle of a network security **Sensor Model**[cite: 5, 320, 321]. [cite_start]The pipeline handles everything from multi-source data ingestion and statistical validation to automated model training and cloud-based deployment[cite: 14, 115, 261, 328]. [cite_start]By integrating robust feature engineering and CI/CD practices, the system ensures that the predictive model remains accurate and highly available in production environments[cite: 19, 22, 189].

## Key Features
* **Modular Pipeline Architecture:** Implements a component-based structure including Ingestion, Validation, Transformation, Trainer, Evaluation, and Pusher modules[cite: 59, 115, 144, 199, 261].
* **Automated Data Validation:** Features built-in schema checking and statistical **Data Drift** detection to maintain model integrity against evolving network traffic patterns[cite: 144, 145, 159, 191].
* **Advanced Feature Engineering:** Utilizes **KNN Imputation** for missing values, **Robust Scaling** for normalization, and **SMOTE** for addressing class imbalances[cite: 215, 228, 254, 277].
* **Automated Model Factory:** Systematically evaluates multiple model configurations to select and "push" the best-performing iteration to production[cite: 301, 307, 315].
* **Enterprise CI/CD:** Uses **Docker** for containerization and **GitHub Actions** for automated deployment to AWS infrastructure[cite: 22, 331, 333, 336].

## Technology Stack
* **Languages:** Java, JavaScript, Golang, Python (Scikit-learn, NumPy, Pandas, Flask)[cite: 8, 43, 46, 248].
* **Databases:** MongoDB (Atlas), Snowflake, OracleDB, Redis, AWS S3[cite: 8, 9, 20, 89, 96].
* **Infrastructure:** AWS (EC2, ECR, App Runner, CloudFormation), Azure[cite: 10, 17, 36, 335, 336, 340].
* **DevOps:** Docker, Kubernetes, GitHub Actions, Git[cite: 10, 22, 41, 333].

## Pipeline Workflow
1.  **Ingestion:** Extracts raw data from local CSVs, S3 buckets, or APIs into MongoDB[cite: 83, 86, 89, 127].
2.  **Validation:** Compares data against established schemas and generates drift reports[cite: 152, 159, 184].
3.  **Transformation:** Performs cleaning, handling of missing values, and feature scaling[cite: 199, 212, 214].
4.  **Training:** Executes the **Model Factory** to find the highest-performing Sensor Model[cite: 301, 307, 321].
5.  **Deployment:** Containerizes the accepted model and deploys it to **AWS EC2** via a CI/CD pipeline[cite: 328, 331, 336, 339].
