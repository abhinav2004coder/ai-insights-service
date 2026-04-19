# Income and Expenditure Prediction Modules

## Overview

Two new ML-powered prediction modules have been added to the AI Insights Service:

1. **Income Prediction Module** - Forecasts future income based on historical patterns
2. **Expenditure Prediction Module** - Predicts future spending by category

Both modules use machine learning algorithms and can work with real user data or generate sample data for demonstration.

## Features

### Income Prediction
- **Multi-model Ensemble**: Uses both Linear Regression and Random Forest for robust predictions
- **Trend Analysis**: Identifies income growth or decline patterns
- **Confidence Intervals**: Provides 95% confidence intervals for predictions
- **Actionable Insights**: Generates personalized recommendations based on predictions
- **Sample Data**: Built-in sample data generation for testing and demos

### Expenditure Prediction
- **Category-wise Forecasting**: Predicts spending for each category (food, transport, etc.)
- **Seasonal Patterns**: Accounts for seasonal variations in spending
- **Trend Detection**: Identifies which categories are increasing or stable
- **Ensemble Methods**: Uses Random Forest and Gradient Boosting for accuracy
- **Budget Insights**: Provides spending alerts and optimization suggestions

## Architecture

```
app/
├── services/
│   ├── income_prediction.py       # Income forecasting service
│   └── expenditure_prediction.py  # Expenditure forecasting service
├── api/
│   └── predictions.py              # API endpoints for predictions
└── models/
    └── schemas.py                  # Pydantic models for requests/responses
```

## API Endpoints

### 1. Predict Income
```http
POST /api/v1/predictions/income
```

**Request:**
```json
{
  "userId": "user123",
  "forecast_months": 6,
  "use_sample_data": true
}
```

**Response:**
```json
{
  "predictions": [
    {
      "month": "2026-05",
      "predicted_income": 5423.45,
      "confidence_interval": {
        "lower": 5123.45,
        "upper": 5723.45
      }
    }
  ],
  "historical_average": 5200.00,
  "predicted_average": 5450.00,
  "growth_trend": 2.5,
  "insights": [
    "Expected income increase of 4.8%...",
    "Income shows stable patterns..."
  ]
}
```

### 2. Predict Expenditure
```http
POST /api/v1/predictions/expenditure
```

**Request:**
```json
{
  "userId": "user123",
  "forecast_months": 6,
  "by_category": true,
  "use_sample_data": true
}
```

**Response:**
```json
{
  "category_predictions": {
    "food": {
      "predictions": [...],
      "historical_average": 620.00,
      "predicted_average": 645.00,
      "trend": "increasing"
    }
  },
  "overall_predictions": [...],
  "insights": [...]
}
```

### 3. Demo Predictions
```http
GET /api/v1/predictions/demo
```

Returns both income and expenditure predictions using sample data.

## Machine Learning Models

### Income Prediction Models
1. **Linear Regression**: Captures overall trend
2. **Random Forest Regressor**: Handles non-linear patterns and seasonality
3. **Ensemble**: Averages predictions from both models

### Expenditure Prediction Models
1. **Random Forest Regressor**: Per-category predictions with seasonal features
2. **Gradient Boosting Regressor**: Alternative model for validation
3. **Ensemble**: Combines predictions for improved accuracy

## Sample Data Generation

Both modules include sophisticated sample data generators:

### Income Sample Data
- 12 months of historical data
- Base salary with upward trend
- Seasonal variations
- Random bonuses
- Realistic noise and volatility

### Expenditure Sample Data
- Category-wise spending patterns
- 7 expense categories (food, transport, entertainment, utilities, healthcare, shopping, other)
- Seasonal effects (higher spending in holidays)
- Trend components
- Realistic variations

## Usage Examples

### Python Client
```python
import requests

# Predict income
response = requests.post(
    'http://localhost:8000/api/v1/predictions/income',
    json={
        'userId': 'user123',
        'forecast_months': 6,
        'use_sample_data': True
    }
)
income_predictions = response.json()

# Predict expenditure
response = requests.post(
    'http://localhost:8000/api/v1/predictions/expenditure',
    json={
        'userId': 'user123',
        'forecast_months': 6,
        'by_category': True,
        'use_sample_data': True
    }
)
expenditure_predictions = response.json()
```

### JavaScript/TypeScript
```typescript
// Predict income
const incomeResponse = await fetch(
  'http://localhost:8000/api/v1/predictions/income',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      userId: 'user123',
      forecast_months: 6,
      use_sample_data: true
    })
  }
);
const incomePredictions = await incomeResponse.json();

// Predict expenditure
const expResponse = await fetch(
  'http://localhost:8000/api/v1/predictions/expenditure',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      userId: 'user123',
      forecast_months: 6,
      by_category: true,
      use_sample_data: true
    })
  }
);
const expenditurePredictions = await expResponse.json();
```

## Testing

Run the test suite:
```bash
pytest tests/test_predictions.py -v
```

Tests include:
- Sample data generation
- Prediction accuracy
- Confidence interval validation
- Category-wise predictions
- Trend detection
- Insight generation

## Integration with FinVision

These modules can be integrated into the FinVision frontend:

1. **Dashboard**: Display income and expenditure forecasts
2. **Budget Planning**: Use predictions for budget recommendations
3. **Insights Page**: Show trends and actionable insights
4. **Alerts**: Notify users of predicted spending increases

### Example Integration
```typescript
// In your FinVision dashboard component
const fetchPredictions = async () => {
  const [income, expenditure] = await Promise.all([
    fetch('/api/predictions/income', {
      method: 'POST',
      body: JSON.stringify({
        userId: currentUser.id,
        forecast_months: 6
      })
    }).then(r => r.json()),
    fetch('/api/predictions/expenditure', {
      method: 'POST',
      body: JSON.stringify({
        userId: currentUser.id,
        forecast_months: 6,
        by_category: true
      })
    }).then(r => r.json())
  ]);
  
  setIncomePredictions(income);
  setExpenditurePredictions(expenditure);
};
```

## Configuration

No additional configuration needed! The modules work out-of-the-box with:
- Existing scikit-learn dependency
- Standard pandas/numpy for data processing
- FastAPI for API endpoints

## Future Enhancements

Potential improvements:
1. **Deep Learning Models**: LSTM/GRU for time series
2. **Real User Data**: Connect to transaction database
3. **External Factors**: Consider economic indicators
4. **Personalization**: User-specific model training
5. **Explainability**: SHAP values for predictions
6. **Alerts**: Proactive notifications for anomalies

## Dependencies

All dependencies are already in `requirements.txt`:
- `scikit-learn>=1.5.0`
- `pandas>=2.2.0`
- `numpy>=1.26.4`

## License

Part of the FinVision AI Insights Service.
