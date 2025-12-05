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
