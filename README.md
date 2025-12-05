# FinVision AI Insights Service

A microservice that provides AI-powered financial insights for the FinVision personal finance application. This service analyzes transaction data to generate spending patterns, budget recommendations, anomaly detection, and savings opportunities.

## Features

- **Spending Pattern Analysis**: Categorize and analyze spending habits
- **Budget Recommendations**: AI-driven budget suggestions based on the 50/30/20 rule
- **Anomaly Detection**: Identify unusual transactions using machine learning
- **Savings Opportunities**: Personalized recommendations for reducing expenses
- **Spending Predictions**: Forecast future spending based on historical data
- **RESTful API**: Easy integration with any frontend application

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Pandas & NumPy**: Data processing and analysis
- **Scikit-learn**: Machine learning for anomaly detection
- **Uvicorn**: ASGI server for running the application
- **Docker**: Containerization for easy deployment

## Project Structure

```
ai-insights-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── health.py        # Health check endpoint
│   │   └── insights.py      # Insights endpoints
│   ├── core/                # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py        # Application settings
│   │   └── logger.py        # Logging configuration
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   └── services/            # Business logic
│       ├── __init__.py
│       └── insights_service.py  # AI insights logic
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── test_api.py
│   └── test_insights.py
├── .env.example             # Environment variables template
├── .gitignore
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Python dependencies
├── pytest.ini               # Pytest configuration
└── README.md
```

## Installation

### Prerequisites

- Python 3.11+
- pip

### Local Development Setup

1. **Clone the repository** (or navigate to the ai-insights-service directory)

```powershell
cd ai-insights-service
```

2. **Create a virtual environment**

```powershell
python -m venv venv
```

3. **Activate the virtual environment**

```powershell
.\venv\Scripts\Activate.ps1
```

4. **Install dependencies**

```powershell
pip install -r requirements.txt
```

5. **Set up environment variables**

```powershell
cp .env.example .env
# Edit .env with your configuration
```

6. **Run the application**

```powershell
python -m app.main
```

Or use uvicorn directly:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Main Endpoints

#### Health Check
```
GET /api/v1/health
```

#### Analyze Transactions
```
POST /api/v1/insights/analyze
```

Request body:
```json
{
  "userId": "user123",
  "transactions": [
    {
      "id": "tx1",
      "amount": 50.0,
      "category": "food",
      "description": "Grocery shopping",
      "date": "2025-11-26T10:00:00Z",
      "userId": "user123"
    }
  ]
}
```

Response includes:
- Spending patterns by category
- Budget recommendations
- Anomaly detection results
- Total spending metrics
- Savings opportunities

#### Quick Analyze (Simplified)
```
POST /api/v1/insights/quick-analyze
```

Accepts a simple array of transactions without the wrapper.

#### Get Categories
```
GET /api/v1/insights/categories
```

Returns available transaction categories.

## Docker Deployment

### Build and Run with Docker

```powershell
docker build -t finvision-ai-insights .
docker run -p 8000:8000 --env-file .env finvision-ai-insights
```

### Using Docker Compose

```powershell
docker-compose up -d
```

## Integration with Next.js Frontend

### Example API Call from Next.js

```typescript
// app/api/ai-insights/route.ts
export async function POST(request: Request) {
  const transactions = await request.json();
  
  const response = await fetch('http://localhost:8000/api/v1/insights/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      userId: 'current-user-id',
      transactions: transactions,
    }),
  });
  
  const insights = await response.json();
  return Response.json(insights);
}
```

### Environment Variables for Next.js

Add to your Next.js `.env.local`:

```
AI_INSIGHTS_API_URL=http://localhost:8000
# Or for production:
# AI_INSIGHTS_API_URL=https://your-ai-service-domain.com
```

## Testing

Run tests with pytest:

```powershell
pytest
```

Run with coverage:

```powershell
pytest --cov=app tests/
```

## Deployment Options

### 1. Railway
- Connect your GitHub repository
- Set environment variables
- Deploy automatically

### 2. Render
- Create a new Web Service
- Connect repository
- Use Docker deployment

### 3. AWS ECS/Fargate
- Push Docker image to ECR
- Create ECS task definition
- Deploy to Fargate

### 4. Google Cloud Run
- Build container image
- Push to Google Container Registry
- Deploy to Cloud Run

### 5. DigitalOcean App Platform
- Connect GitHub repository
- Configure build settings
- Deploy

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `ENVIRONMENT` | Environment (development/production) | `development` |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | `http://localhost:3000` |
| `MODEL_CACHE_DIR` | Directory for caching models | `./models` |
| `LOG_LEVEL` | Logging level | `INFO` |

## AI/ML Features Explained

### Spending Pattern Analysis
- Aggregates transactions by category
- Calculates total, average, and percentage for each category
- Identifies spending trends

### Budget Recommendations
- Based on 50/30/20 budgeting rule
- Compares actual spending to recommended allocations
- Prioritizes categories that need attention

### Anomaly Detection
- Uses Isolation Forest algorithm
- Detects unusual transaction amounts
- Provides anomaly scores and explanations

### Savings Opportunities
- Identifies overspending categories
- Suggests consolidation of small purchases
- Provides actionable recommendations

## Performance Considerations

- The service is stateless and can be horizontally scaled
- Consider caching frequently accessed data with Redis
- For large datasets, implement pagination
- Use async database queries if storing transaction history

## Future Enhancements

- [ ] Add more ML models (LSTM for time series prediction)
- [ ] Implement caching layer (Redis)
- [ ] Add authentication/API keys
- [ ] Store transaction history in database
- [ ] Add more sophisticated prediction models
- [ ] Implement rate limiting
- [ ] Add webhook support for real-time insights

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - feel free to use this in your projects!

## Support

For issues or questions, please open an issue on GitHub.

## API Response Examples

### Analyze Transactions Response

```json
{
  "userId": "user123",
  "spendingPatterns": [
    {
      "category": "food",
      "totalAmount": 450.0,
      "transactionCount": 15,
      "averageAmount": 30.0,
      "percentage": 35.0
    }
  ],
  "budgetRecommendations": [
    {
      "category": "food",
      "recommendedAmount": 350.0,
      "currentSpending": 450.0,
      "reason": "Spending is 28% over recommended budget",
      "priority": "high"
    }
  ],
  "anomalies": [
    {
      "transactionId": "tx123",
      "amount": 500.0,
      "category": "entertainment",
      "date": "2025-11-20T10:00:00Z",
      "anomalyScore": 0.85,
      "reason": "Amount is $450.00 away from average entertainment spending"
    }
  ],
  "totalSpending": 1285.0,
  "averageDailySpending": 42.83,
  "projectedMonthlySpending": 1285.0,
  "savingsOpportunities": [
    "Reduce food spending by $100.00/month to meet budget goals",
    "Consolidate small shopping purchases to save up to $50.00/month"
  ]
}
```

## Notes

- This service is designed to be stateless and doesn't persist data
- Transaction data is passed with each request
- For production, consider adding a database layer
- Update CORS settings in `.env` to match your frontend URL
- The service uses scikit-learn's Isolation Forest for anomaly detection
- Budget recommendations follow industry-standard allocation guidelines
