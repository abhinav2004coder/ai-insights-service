"""
Tests for income and expenditure prediction services
"""
import pytest
from app.services.income_prediction import income_prediction_service
from app.services.expenditure_prediction import expenditure_prediction_service


def test_income_prediction_with_sample_data():
    """Test income prediction using generated sample data"""
    result = income_prediction_service.predict_income(
        historical_data=None,
        forecast_months=6
    )
    
    assert 'predictions' in result
    assert len(result['predictions']) == 6
    assert 'historical_average' in result
    assert 'predicted_average' in result
    assert 'insights' in result
    assert len(result['insights']) > 0
    assert result['sample_data_used'] == True
    
    # Check prediction structure
    first_prediction = result['predictions'][0]
    assert 'month' in first_prediction
    assert 'predicted_income' in first_prediction
    assert 'confidence_interval' in first_prediction
    assert 'lower' in first_prediction['confidence_interval']
    assert 'upper' in first_prediction['confidence_interval']


def test_income_prediction_growth_trend():
    """Test that income prediction calculates growth trend"""
    result = income_prediction_service.predict_income(
        historical_data=None,
        forecast_months=3
    )
    
    assert 'growth_trend' in result
    assert isinstance(result['growth_trend'], (int, float))


def test_expenditure_prediction_with_sample_data():
    """Test expenditure prediction using generated sample data"""
    result = expenditure_prediction_service.predict_expenditure(
        historical_data=None,
        forecast_months=6,
        by_category=True
    )
    
    assert 'category_predictions' in result
    assert 'overall_predictions' in result
    assert len(result['overall_predictions']) == 6
    assert 'insights' in result
    assert len(result['insights']) > 0
    
    # Check category predictions
    assert len(result['category_predictions']) > 0
    for category, data in result['category_predictions'].items():
        assert 'predictions' in data
        assert 'historical_average' in data
        assert 'predicted_average' in data
        assert 'trend' in data
        assert data['trend'] in ['increasing', 'stable', 'decreasing']


def test_expenditure_prediction_categories():
    """Test that expenditure prediction includes all categories"""
    result = expenditure_prediction_service.predict_expenditure(
        historical_data=None,
        forecast_months=6,
        by_category=True
    )
    
    expected_categories = ['food', 'transport', 'entertainment', 'utilities', 'healthcare', 'shopping', 'other']
    
    for category in expected_categories:
        assert category in result['category_predictions']


def test_sample_data_generation_income():
    """Test sample income data generation"""
    sample_data = income_prediction_service.generate_sample_income_data(months=12)
    
    assert len(sample_data) == 12
    assert 'date' in sample_data.columns
    assert 'total_income' in sample_data.columns
    assert 'base_salary' in sample_data.columns
    assert 'bonuses' in sample_data.columns
    assert all(sample_data['total_income'] > 0)


def test_sample_data_generation_expenditure():
    """Test sample expenditure data generation"""
    sample_data = expenditure_prediction_service.generate_sample_expenditure_data(months=12)
    
    assert len(sample_data) > 0
    assert 'date' in sample_data.columns
    assert 'category' in sample_data.columns
    assert 'amount' in sample_data.columns
    assert all(sample_data['amount'] >= 0)
    
    # Should have data for all categories
    categories = sample_data['category'].unique()
    assert len(categories) >= 7


def test_income_prediction_confidence_score():
    """Test that confidence score is within valid range"""
    result = income_prediction_service.predict_income(
        historical_data=None,
        forecast_months=6
    )
    
    assert 'confidence_score' in result
    assert 0 <= result['confidence_score'] <= 1


def test_expenditure_prediction_confidence_score():
    """Test that confidence score is within valid range"""
    result = expenditure_prediction_service.predict_expenditure(
        historical_data=None,
        forecast_months=6,
        by_category=True
    )
    
    assert 'confidence_score' in result
    assert 0 <= result['confidence_score'] <= 1
