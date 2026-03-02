---
description: Comprehensive workflow for developing production-ready LLM and ML applications from prototype to production for the dashboard.
---

# ML Development Workflow (Dashboard)

This workflow defines the lifecycle for ML models used in the statistical dashboard.

## Steps

1. **Environment & Data**
   - Verify conda environment `cursor-factory`.
   - Load baseline data from `data/processed/`.

2. **Experimentation**
   - Define model architecture (Scikit-learn, XGBoost, etc.).
   - Perform hyperparameter optimization (Grid/Random Search).
   - Log metrics (RMSE, MAE, R2) to `experiments/model_history.json`.

3. **Evaluation**
   - Run cross-validation.
   - Generate lift/gain charts using the `visualization` workflow.
   - Perform residual analysis.

4. **Persistence**
   - Save models to `models/dashboard/` using joblib/pickle.
   - Document model performance in `MODEL_CARD.md`.
