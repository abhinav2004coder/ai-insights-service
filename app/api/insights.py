from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.schemas import (
    TransactionBatch,
    InsightsResponse,
    PredictionRequest,
    PredictionResponse,
    Transaction,
    TransactionCategory,
)
from app.services.insights_service import insights_service
from app.core.logger import logger
from app.core.database import get_db, TransactionModel, TransactionTypeEnum

router = APIRouter()


@router.post("/insights/analyze", response_model=InsightsResponse)
async def analyze_transactions(batch: TransactionBatch):
    """
    Analyze a batch of transactions and generate comprehensive insights
    
    This endpoint provides:
    - Spending patterns by category
    - Budget recommendations
    - Anomaly detection
    - Savings opportunities
    - Spending projections
    """
    try:
        logger.info(f"Received analysis request for user {batch.userId} with {len(batch.transactions)} transactions")
        
        insights = insights_service.analyze_transactions(
            transactions=batch.transactions,
            userId=batch.userId
        )
        
        logger.info(f"Successfully generated insights for user {batch.userId}")
        return insights
        
    except Exception as e:
        logger.error(f"Error analyzing transactions: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze transactions: {str(e)}"
        )


@router.post("/insights/predict", response_model=PredictionResponse)
async def predict_spending(request: PredictionRequest):
    """
    Predict future spending based on historical transaction data
    
    Requires historical transactions to be sent in the request body.
    Can predict overall spending or category-specific spending.
    """
    try:
        logger.info(f"Received prediction request for user {request.userId}")
        
        # Note: In a real implementation, you would fetch historical transactions
        # from a database. For now, this endpoint expects transactions in the body.
        # You may want to modify this to accept transactions or fetch from a DB.
        
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Prediction endpoint requires integration with transaction storage"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error predicting spending: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to predict spending: {str(e)}"
        )


@router.post("/insights/quick-analyze")
async def quick_analyze(transactions: List[Transaction]):
    """
    Quick analysis endpoint for a simple list of transactions
    
    This is a simplified version that accepts just a list of transactions
    without requiring the TransactionBatch wrapper.
    """
    try:
        if not transactions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No transactions provided"
            )
        
        # Extract userId from first transaction
        userId = transactions[0].userId
        
        logger.info(f"Received quick analysis request with {len(transactions)} transactions")
        
        insights = insights_service.analyze_transactions(
            transactions=transactions,
            userId=userId
        )
        
        return insights
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in quick analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze transactions: {str(e)}"
        )


@router.get("/insights/categories")
async def get_categories():
    """
    Get list of available transaction categories
    """
    from app.models.schemas import TransactionCategory
    
    return {
        "categories": [cat.value for cat in TransactionCategory]
    }


@router.get("/insights/user/{user_id}", response_model=InsightsResponse)
async def get_user_insights(user_id: str, db: Session = Depends(get_db)):
    """
    Get AI-powered insights for a specific user by fetching their transactions
    
    This endpoint:
    1. Fetches all transactions for the user from the database
    2. Filters for EXPENSE transactions only
    3. Analyzes spending patterns and generates insights
    4. Returns personalized recommendations
    """
    try:
        logger.info(f"Fetching insights for user: {user_id}")
        
        # Fetch all user transactions from database (both income and expense)
        db_transactions = db.query(TransactionModel).filter(
            TransactionModel.userId == user_id
        ).all()
        
        if not db_transactions:
            logger.info(f"No transactions found for user {user_id}")
            from app.models.schemas import IncomeVsExpense
            return InsightsResponse(
                userId=user_id,
                incomeVsExpense=IncomeVsExpense(
                    totalIncome=0.0,
                    totalExpense=0.0,
                    netBalance=0.0,
                    savingsRate=0.0,
                    status="healthy"
                ),
                spendingPatterns=[],
                categoryHealth=[],
                budgetRecommendations=[],
                anomalies=[],
                totalSpending=0.0,
                averageDailySpending=0.0,
                projectedMonthlySpending=0.0,
                savingsOpportunities=["Start tracking your expenses to get personalized insights!"],
            )
        
        logger.info(f"Found {len(db_transactions)} transactions for user {user_id}")
        
        # Convert database models to schema models
        transactions = []
        for db_tx in db_transactions:
            try:
                # Map category to TransactionCategory enum
                category = db_tx.category.lower()
                if category not in [cat.value for cat in TransactionCategory]:
                    category = "other"
                
                # Create transaction with type information
                tx = Transaction(
                    id=db_tx.id,
                    amount=db_tx.amount,
                    category=TransactionCategory(category),
                    description=db_tx.description or "",
                    date=db_tx.date,
                    userId=db_tx.userId
                )
                # Add type as extra attribute for analysis
                tx.type = db_tx.type.value if hasattr(db_tx.type, 'value') else str(db_tx.type)
                transactions.append(tx)
            except Exception as e:
                logger.warning(f"Skipping transaction {db_tx.id}: {str(e)}")
                continue
        
        if not transactions:
            logger.warning(f"No valid transactions for user {user_id} after conversion")
            from app.models.schemas import IncomeVsExpense
            return InsightsResponse(
                userId=user_id,
                incomeVsExpense=IncomeVsExpense(
                    totalIncome=0.0,
                    totalExpense=0.0,
                    netBalance=0.0,
                    savingsRate=0.0,
                    status="healthy"
                ),
                spendingPatterns=[],
                categoryHealth=[],
                budgetRecommendations=[],
                anomalies=[],
                totalSpending=0.0,
                averageDailySpending=0.0,
                projectedMonthlySpending=0.0,
                savingsOpportunities=["Start tracking your expenses to get personalized insights!"],
            )
        
        # Generate insights
        insights = insights_service.analyze_transactions(
            transactions=transactions,
            userId=user_id
        )
        
        logger.info(f"Successfully generated insights for user {user_id}")
        return insights
        
    except Exception as e:
        logger.error(f"Error fetching insights for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch insights: {str(e)}"
        )
