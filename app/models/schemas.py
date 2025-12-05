from pydantic import BaseModel, Field
from typing import List, Optional
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
