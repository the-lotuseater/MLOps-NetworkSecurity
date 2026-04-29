# Network Security — Phishing Detection MLOps Pipeline

An end-to-end MLOps pipeline for detecting phishing URLs, covering data ingestion from MongoDB, validation, transformation, model training with experiment tracking, and deployment via a FastAPI service on AWS EC2 with CI/CD through GitHub Actions.

## Architecture

```
MongoDB Atlas
     │
     ▼
Data Ingestion ──► Feature Store (CSV) ──► Train/Test Split
     │
     ▼
Data Validation
  - Schema column check
  - Data drift detection (Kolmogorov-Smirnov test)
     │
     ▼
Data Transformation
  - KNN Imputation (missing value handling)
  - Preprocessor saved as preprocessor.pkl
     │
     ▼
Model Training
  - 5 models evaluated: Random Forest, Gradient Boosting,
    Decision Tree, Logistic Regression, AdaBoost
  - Hyperparameter tuning via GridSearchCV
  - Best model selected automatically
  - Metrics logged to MLflow + DagShub
     │
     ▼
FastAPI Serving
  - POST /predict  → batch CSV prediction
  - GET  /train    → trigger retraining
     │
     ▼
Docker → AWS ECR → AWS EC2
  CI/CD via GitHub Actions (push to main)
```

## Model Results

| Metric    | Score  |
|-----------|--------|
| F1 Score  | 0.9923 |
| Precision | 0.9884 |
| Recall    | 0.9962 |

Experiment runs tracked on DagShub via MLflow.

## Pipeline Components

| Component | What it does |
|---|---|
| `data_ingestion.py` | Pulls phishing dataset from MongoDB, exports to CSV feature store, splits train/test |
| `data_validation.py` | Validates schema column count, runs KS test per feature to detect drift between train and test |
| `data_transformation.py` | Applies KNN imputation, fits preprocessor on train, transforms both sets, saves preprocessor |
| `model_trainer.py` | Trains 5 classifiers, selects best by test score, logs metrics + model artifact to MLflow |

## API Endpoints

**Trigger retraining:**
```
GET /train
```

**Batch prediction (upload CSV):**
```
POST /predict
Content-Type: multipart/form-data
Body: file=<csv_file>
```
Returns an HTML table with predictions appended as a `predicted_column`.

## Setup

### 1. MongoDB
Push the phishing dataset to MongoDB Atlas:
```bash
python push_data.py
```

### 2. Environment variables
Create a `.env` file:
```
MONGODB_URL_KEY=mongodb+srv://<user>:<pass>@<cluster>.mongodb.net
```

### 3. Run locally
```bash
pip install -r requirements.txt
python app.py
```
App runs at `http://localhost:8080`. Visit `/docs` for the Swagger UI.

### 4. Run with Docker
```bash
docker build -t networksecurity .
docker run -p 8080:8080 networksecurity
```

## CI/CD Pipeline

On every push to `main`, GitHub Actions:
1. Builds the Docker image
2. Pushes it to **AWS ECR**
3. Pulls and runs it on a **self-hosted EC2 runner**

Required GitHub secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `ECR_REPOSITORY_NAME`, `AWS_ECR_LOGIN_URI`

## Tech Stack

- **Data store:** MongoDB Atlas
- **ML:** scikit-learn (Random Forest, Gradient Boosting, AdaBoost, Logistic Regression, Decision Tree)
- **Experiment tracking:** MLflow + DagShub
- **Serving:** FastAPI + Uvicorn
- **Containerisation:** Docker
- **Cloud:** AWS ECR, AWS EC2
- **CI/CD:** GitHub Actions
