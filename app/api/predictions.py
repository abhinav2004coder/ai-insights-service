from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    IncomePredictionRequest,
    IncomePredictionResponse,
    ExpenditurePredictionRequest,
    ExpenditurePredictionResponse,
)
from app.services.income_prediction import income_prediction_service
from app.services.expenditure_prediction import expenditure_prediction_service
from app.core.logger import logger

router = APIRouter()


@router.post("/predictions/income", response_model=IncomePredictionResponse)
async def predict_income(request: IncomePredictionRequest):
    """
    Predict future income based on historical patterns
    
    This endpoint provides:
    - Monthly income predictions for the specified forecast period
    - Historical average income
    - Growth trend analysis
    - Confidence intervals
    - Actionable insights
    
    If use_sample_data is True, generates demo data for testing.
    """
    try:
        logger.info(
            f"Received income prediction request for user {request.userId} "
            f"with forecast_months={request.forecast_months}"
        )
        
        # Use sample data if requested
        historical_data = None if request.use_sample_data else None
        
        result = income_prediction_service.predict_income(
            historical_data=historical_data,
            forecast_months=request.forecast_months
        )
        
        logger.info(f"Successfully generated income predictions for user {request.userId}")
        return IncomePredictionResponse(**result)
        
    except Exception as e:
        logger.error(f"Error predicting income: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to predict income: {str(e)}"
        )


@router.post("/predictions/expenditure", response_model=ExpenditurePredictionResponse)
async def predict_expenditure(request: ExpenditurePredictionRequest):
    """
    Predict future expenditures based on historical spending patterns
    
    This endpoint provides:
    - Category-wise expenditure predictions (if by_category=True)
    - Overall monthly expenditure predictions
    - Historical vs predicted averages
    - Spending trends by category
    - Actionable insights for budget management
    
    If use_sample_data is True, generates demo data for testing.
    """
    try:
        logger.info(
            f"Received expenditure prediction request for user {request.userId} "
            f"with forecast_months={request.forecast_months}, by_category={request.by_category}"
        )
        
        # Use sample data if requested
        historical_data = None if request.use_sample_data else None
        
        result = expenditure_prediction_service.predict_expenditure(
            historical_data=historical_data,
            forecast_months=request.forecast_months,
            by_category=request.by_category
        )
        
        logger.info(f"Successfully generated expenditure predictions for user {request.userId}")
        return ExpenditurePredictionResponse(**result)
        
    except Exception as e:
        logger.error(f"Error predicting expenditure: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to predict expenditure: {str(e)}"
        )


@router.get("/predictions/demo")
async def get_demo_predictions():
    """
    Get demo predictions for both income and expenditure
    
    Returns sample predictions using generated data to demonstrate
    the prediction capabilities without requiring historical data.
    """
    try:
        logger.info("Generating demo predictions")
        
        # Generate income predictions
        income_result = income_prediction_service.predict_income(
            historical_data=None,
            forecast_months=6
        )
        
        # Generate expenditure predictions
        expenditure_result = expenditure_prediction_service.predict_expenditure(
            historical_data=None,
            forecast_months=6,
            by_category=True
        )
        
        return {
            "income_predictions": income_result,
            "expenditure_predictions": expenditure_result,
            "message": "Demo predictions generated using sample data"
        }
        
    except Exception as e:
        logger.error(f"Error generating demo predictions: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate demo predictions: {str(e)}"
        )
