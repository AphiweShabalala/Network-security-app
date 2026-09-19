# Network Security Phishing Detection

An end-to-end machine-learning project that classifies websites as legitimate or phishing from URL and domain-security signals. The project demonstrates a production-minded ML workflow: data ingestion, schema validation, drift reporting, feature preprocessing, model selection, experiment tracking, and API-based batch inference.

## Portfolio highlights

- Designed a modular training pipeline with separate ingestion, validation, transformation, and model-training components.
- Validates 30 expected security features and generates a Kolmogorov-Smirnov data-drift report before training.
- Evaluates several classifiers with cross-validation and selects the best model by F1 score for the binary classification task.
- Exposes documented FastAPI endpoints for retraining and CSV batch predictions.
- Includes MLflow/DagsHub tracking hooks, Docker packaging, and a GitHub Actions test workflow.

## Technology

Python, FastAPI, scikit-learn, pandas, NumPy, SciPy, MongoDB, MLflow, DagsHub, Docker, and GitHub Actions.

## Project layout

```text
Network_Security/          Training pipeline, components, configuration, and utilities
Network_Data/              Local phishing dataset used to seed MongoDB
data_schema/schema.yaml    Expected feature schema
main.py                    Command-line training entry point
app.py                     FastAPI application
PushData.py                Optional CSV-to-MongoDB loader
```

## Dataset and target

The model uses 30 URL, domain, and page-behavior features, including SSL state, URL length, redirects, domain age, and search-index signals. The target is `Result`; its `-1` label is converted to `0` for binary classification.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:

   ```env
   MONGO_DB_URL=your_mongodb_connection_string
   ```

4. Optionally seed MongoDB from the included dataset:

   ```bash
   python PushData.py
   ```

5. Train and run the API:

   ```bash
   python main.py
   uvicorn app:app --reload
   ```

Open `http://127.0.0.1:8000/docs` for interactive API documentation. Upload a feature CSV to `POST /predict`; use `POST /train` to start a new training run.

## Container

```bash
docker build -t phishing-detector .
docker run --env-file .env -p 8000:8000 phishing-detector
```

## Production considerations

This portfolio project intentionally keeps synchronous training and development CORS settings simple. A production deployment should use a background job queue for training, restrict allowed origins, store model artifacts in managed object storage, and keep secrets in a secret manager.
