from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class TransactionCategory(str, Enum):
    """Transaction categories"""
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    SHOPPING = "shopping"
    OTHER = "other"


class Transaction(BaseModel):
    """Transaction model"""
    id: Optional[str] = None
    amount: float = Field(..., gt=0)
    category: TransactionCategory
    description: Optional[str] = None
    date: datetime
    userId: str
    type: Optional[str] = None  # INCOME or EXPENSE
    
    class Config:
        extra = 'allow'


class TransactionBatch(BaseModel):
    """Batch of transactions for analysis"""
    transactions: List[Transaction]
    userId: str


class SpendingPattern(BaseModel):
    """Spending pattern analysis result"""
    category: str
    totalAmount: float
    transactionCount: int
    averageAmount: float
    percentage: float


class BudgetRecommendation(BaseModel):
    """Budget recommendation"""
    category: str
    recommendedAmount: float
    currentSpending: float
    reason: str
    priority: str  # high, medium, low


class AnomalyDetection(BaseModel):
    """Anomaly detection result"""
    transactionId: str
    amount: float
    category: str
    date: datetime
    anomalyScore: float
    reason: str


class CategoryHealth(BaseModel):
    """Category health assessment"""
    category: str
    status: str  # good, warning, bad
    reason: str
    spending: float
    recommendation: str


class IncomeVsExpense(BaseModel):
    """Income vs Expense comparison"""
    totalIncome: float
    totalExpense: float
    netBalance: float
    savingsRate: float  # percentage
    status: str  # healthy, concerning, critical


class InsightsResponse(BaseModel):
    """Complete insights response"""
    userId: str
    incomeVsExpense: IncomeVsExpense
    spendingPatterns: List[SpendingPattern]
    categoryHealth: List[CategoryHealth]
    budgetRecommendations: List[BudgetRecommendation]
    anomalies: List[AnomalyDetection]
    totalSpending: float
    averageDailySpending: float
    projectedMonthlySpending: float
    savingsOpportunities: List[str]


class PredictionRequest(BaseModel):
    """Request for spending prediction"""
    userId: str
    category: Optional[str] = None
    daysAhead: int = 30


class PredictionResponse(BaseModel):
    """Spending prediction response"""
    userId: str
    category: Optional[str]
    predictedAmount: float
    confidence: float
    period: str


class ConfidenceInterval(BaseModel):
    """Confidence interval for predictions"""
    lower: float
    upper: float


class MonthlyPrediction(BaseModel):
    """Monthly prediction data"""
    month: str
    predicted_income: Optional[float] = None
    predicted_expenditure: Optional[float] = None
    linear_prediction: Optional[float] = None
    rf_prediction: Optional[float] = None
    confidence_interval: Optional[ConfidenceInterval] = None
    amount: Optional[float] = None  # For expenditure


class CategoryExpenditurePrediction(BaseModel):
    """Category-wise expenditure prediction"""
    predictions: List[MonthlyPrediction]
    historical_average: float
    predicted_average: float
    total_predicted: float
    trend: str


class IncomePredictionRequest(BaseModel):
    """Request for income prediction"""
    userId: str
    forecast_months: int = Field(default=6, ge=1, le=12)
    use_sample_data: bool = True


class IncomePredictionResponse(BaseModel):
    """Income prediction response"""
    predictions: List[MonthlyPrediction]
    historical_average: float
    predicted_average: float
    growth_trend: float
    total_predicted_income: float
    confidence_score: float
    insights: List[str]
    sample_data_used: bool


class ExpenditurePredictionRequest(BaseModel):
    """Request for expenditure prediction"""
    userId: str
    forecast_months: int = Field(default=6, ge=1, le=12)
    by_category: bool = True
    use_sample_data: bool = True


class OverallExpenditurePrediction(BaseModel):
    """Overall expenditure prediction"""
    month: str
    total_expenditure: float


class ExpenditurePredictionResponse(BaseModel):
    """Expenditure prediction response"""
    category_predictions: Optional[Dict[str, CategoryExpenditurePrediction]] = None
    overall_predictions: List[OverallExpenditurePrediction]
    historical_average_total: float
    predicted_average_total: float
    total_predicted_expenditure: float
    insights: List[str]
    confidence_score: float
    sample_data_used: bool
