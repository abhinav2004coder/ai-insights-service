# API Documentation

## Base URL

- Development: `http://localhost:8000`
- Production: `https://your-domain.com`

## API Version

All endpoints are prefixed with `/api/v1`

---

## Endpoints

### Health Check

**GET** `/api/v1/health`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "ai-insights-service",
  "version": "1.0.0"
}
```

---

### Get Transaction Categories

**GET** `/api/v1/insights/categories`

Get list of available transaction categories.

**Response:**
```json
{
  "categories": [
    "food",
    "transport",
    "entertainment",
    "utilities",
    "healthcare",
    "shopping",
    "other"
  ]
}
```

---

### Analyze Transactions

**POST** `/api/v1/insights/analyze`

Analyze a batch of transactions and generate comprehensive insights.

**Request Body:**
```json
{
  "userId": "string",
  "transactions": [
    {
      "id": "string (optional)",
      "amount": 0.0,
      "category": "food|transport|entertainment|utilities|healthcare|shopping|other",
      "description": "string (optional)",
      "date": "2025-11-26T10:00:00Z",
      "userId": "string"
    }
  ]
}
```

**Response:**
```json
{
  "userId": "string",
  "spendingPatterns": [
    {
      "category": "string",
      "totalAmount": 0.0,
      "transactionCount": 0,
      "averageAmount": 0.0,
      "percentage": 0.0
    }
  ],
  "budgetRecommendations": [
    {
      "category": "string",
      "recommendedAmount": 0.0,
      "currentSpending": 0.0,
      "reason": "string",
      "priority": "high|medium|low"
    }
  ],
  "anomalies": [
    {
      "transactionId": "string",
      "amount": 0.0,
      "category": "string",
      "date": "2025-11-26T10:00:00Z",
      "anomalyScore": 0.0,
      "reason": "string"
    }
  ],
  "totalSpending": 0.0,
  "averageDailySpending": 0.0,
  "projectedMonthlySpending": 0.0,
  "savingsOpportunities": ["string"]
}
```

---

### Quick Analyze

**POST** `/api/v1/insights/quick-analyze`

Simplified analysis endpoint that accepts just a list of transactions.

**Request Body:**
```json
[
  {
    "id": "string (optional)",
    "amount": 0.0,
    "category": "food",
    "description": "string (optional)",
    "date": "2025-11-26T10:00:00Z",
    "userId": "string"
  }
]
```

**Response:** Same as `/analyze` endpoint

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Error message describing the validation error"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to analyze transactions: error details"
}
```

---

## Data Models

### Transaction
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | No | Unique transaction ID |
| amount | float | Yes | Transaction amount (must be > 0) |
| category | string | Yes | Transaction category (enum) |
| description | string | No | Transaction description |
| date | datetime | Yes | Transaction date (ISO 8601) |
| userId | string | Yes | User ID |

### TransactionCategory (Enum)
- `food`
- `transport`
- `entertainment`
- `utilities`
- `healthcare`
- `shopping`
- `other`

---

## Integration Examples

### JavaScript/TypeScript
```typescript
const analyzeTransactions = async (transactions) => {
  const response = await fetch('http://localhost:8000/api/v1/insights/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      userId: 'user123',
      transactions: transactions,
    }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to analyze transactions');
  }
  
  return await response.json();
};
```

### Python
```python
import requests

def analyze_transactions(user_id, transactions):
    response = requests.post(
        'http://localhost:8000/api/v1/insights/analyze',
        json={
            'userId': user_id,
            'transactions': transactions,
        }
    )
    response.raise_for_status()
    return response.json()
```

### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/insights/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "transactions": [
      {
        "amount": 50.0,
        "category": "food",
        "date": "2025-11-26T10:00:00Z",
        "userId": "user123"
      }
    ]
  }'
```

---

### Predict Income

**POST** `/api/v1/predictions/income`

Predict future income based on historical patterns using machine learning.

**Request Body:**
```json
{
  "userId": "string",
  "forecast_months": 6,
  "use_sample_data": true
}
```

**Parameters:**
- `userId` (required): User identifier
- `forecast_months` (optional, default=6): Number of months to forecast (1-12)
- `use_sample_data` (optional, default=true): Use generated sample data for demo

**Response:**
```json
{
  "predictions": [
    {
      "month": "2026-05",
      "predicted_income": 5423.45,
      "linear_prediction": 5400.00,
      "rf_prediction": 5446.90,
      "confidence_interval": {
        "lower": 5123.45,
        "upper": 5723.45
      }
    }
  ],
  "historical_average": 5200.00,
  "predicted_average": 5450.00,
  "growth_trend": 2.5,
  "total_predicted_income": 32700.00,
  "confidence_score": 0.85,
  "insights": [
    "Expected income increase of 4.8% in the coming months. Great opportunity to increase savings!",
    "Income shows stable patterns, making budgeting easier."
  ],
  "sample_data_used": true
}
```

---

### Predict Expenditure

**POST** `/api/v1/predictions/expenditure`

Predict future expenditures by category based on historical spending patterns.

**Request Body:**
```json
{
  "userId": "string",
  "forecast_months": 6,
  "by_category": true,
  "use_sample_data": true
}
```

**Parameters:**
- `userId` (required): User identifier
- `forecast_months` (optional, default=6): Number of months to forecast (1-12)
- `by_category` (optional, default=true): Include category-wise predictions
- `use_sample_data` (optional, default=true): Use generated sample data for demo

**Response:**
```json
{
  "category_predictions": {
    "food": {
      "predictions": [
        {
          "month": "2026-05",
          "amount": 650.50
        }
      ],
      "historical_average": 620.00,
      "predicted_average": 645.00,
      "total_predicted": 3870.00,
      "trend": "increasing"
    },
    "transport": {
      "predictions": [...],
      "historical_average": 210.00,
      "predicted_average": 215.00,
      "total_predicted": 1290.00,
      "trend": "stable"
    }
  },
  "overall_predictions": [
    {
      "month": "2026-05",
      "total_expenditure": 2145.75
    }
  ],
  "historical_average_total": 2100.00,
  "predicted_average_total": 2150.00,
  "total_predicted_expenditure": 12900.00,
  "insights": [
    "Spending is expected to remain stable.",
    "'food' is predicted to be your highest expense category at $3870.00 total.",
    "Categories showing increasing trend: food, shopping. Monitor these for potential savings.",
    "Consider seasonal variations in entertainment and shopping expenses, especially during holiday months."
  ],
  "confidence_score": 0.80,
  "sample_data_used": true
}
```

---

### Get Demo Predictions

**GET** `/api/v1/predictions/demo`

Get demonstration predictions for both income and expenditure using sample data.

**Response:**
```json
{
  "income_predictions": {
    "predictions": [...],
    "historical_average": 5200.00,
    "predicted_average": 5450.00,
    "insights": [...]
  },
  "expenditure_predictions": {
    "category_predictions": {...},
    "overall_predictions": [...],
    "insights": [...]
  },
  "message": "Demo predictions generated using sample data"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. Consider adding rate limiting for production deployments.

## Authentication

Currently, the API is open. For production, consider implementing:
- API key authentication
- JWT tokens
- OAuth 2.0

## CORS

Configure allowed origins in `.env`:
```
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.com
```
