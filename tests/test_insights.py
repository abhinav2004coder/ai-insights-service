import pytest
from datetime import datetime
from app.models.schemas import Transaction, TransactionCategory
from app.services.insights_service import insights_service


def test_empty_transactions():
    """Test insights with empty transaction list"""
    insights = insights_service.analyze_transactions([], "user123")
    
    assert insights.userId == "user123"
    assert insights.totalSpending == 0.0
    assert len(insights.spendingPatterns) == 0


def test_single_transaction():
    """Test insights with single transaction"""
    transactions = [
        Transaction(
            id="1",
            amount=50.0,
            category=TransactionCategory.FOOD,
            date=datetime.now(),
            userId="user123"
        )
    ]
    
    insights = insights_service.analyze_transactions(transactions, "user123")
    
    assert insights.totalSpending == 50.0
    assert len(insights.spendingPatterns) == 1
    assert insights.spendingPatterns[0].category == "food"


def test_multiple_categories():
    """Test insights with multiple categories"""
    transactions = [
        Transaction(
            id="1",
            amount=50.0,
            category=TransactionCategory.FOOD,
            date=datetime.now(),
            userId="user123"
        ),
        Transaction(
            id="2",
            amount=100.0,
            category=TransactionCategory.TRANSPORT,
            date=datetime.now(),
            userId="user123"
        ),
    ]
    
    insights = insights_service.analyze_transactions(transactions, "user123")
    
    assert insights.totalSpending == 150.0
    assert len(insights.spendingPatterns) == 2
