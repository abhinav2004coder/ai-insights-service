"""
Demo script to test the income and expenditure prediction modules
Run this to see the predictions in action!
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.income_prediction import income_prediction_service
from app.services.expenditure_prediction import expenditure_prediction_service
import json


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def demo_income_prediction():
    """Demonstrate income prediction"""
    print_section("INCOME PREDICTION DEMO")
    
    print("Generating 6-month income predictions using sample data...\n")
    
    result = income_prediction_service.predict_income(
        historical_data=None,
        forecast_months=6
    )
    
    print(f"Historical Average Income: ${result['historical_average']:.2f}")
    print(f"Predicted Average Income:  ${result['predicted_average']:.2f}")
    print(f"Growth Trend:              {result['growth_trend']:.2f}%")
    print(f"Total Predicted (6 months): ${result['total_predicted_income']:.2f}")
    print(f"Confidence Score:          {result['confidence_score']:.0%}\n")
    
    print("Monthly Predictions:")
    print("-" * 80)
    for pred in result['predictions']:
        print(f"  {pred['month']}: ${pred['predicted_income']:>8.2f} "
              f"(Range: ${pred['confidence_interval']['lower']:.2f} - "
              f"${pred['confidence_interval']['upper']:.2f})")
    
    print("\nInsights:")
    print("-" * 80)
    for i, insight in enumerate(result['insights'], 1):
        print(f"  {i}. {insight}")


def demo_expenditure_prediction():
    """Demonstrate expenditure prediction"""
    print_section("EXPENDITURE PREDICTION DEMO")
    
    print("Generating 6-month expenditure predictions by category using sample data...\n")
    
    result = expenditure_prediction_service.predict_expenditure(
        historical_data=None,
        forecast_months=6,
        by_category=True
    )
    
    print(f"Historical Average Total: ${result['historical_average_total']:.2f}")
    print(f"Predicted Average Total:  ${result['predicted_average_total']:.2f}")
    print(f"Total Predicted (6 months): ${result['total_predicted_expenditure']:.2f}")
    print(f"Confidence Score:          {result['confidence_score']:.0%}\n")
    
    print("Category-wise Summary:")
    print("-" * 80)
    for category, data in sorted(result['category_predictions'].items()):
        trend_symbol = "↑" if data['trend'] == "increasing" else "→"
        print(f"  {category.capitalize():15} | "
              f"Avg: ${data['predicted_average']:>7.2f} | "
              f"Total: ${data['total_predicted']:>8.2f} | "
              f"Trend: {trend_symbol} {data['trend']}")
    
    print("\nMonthly Total Predictions:")
    print("-" * 80)
    for pred in result['overall_predictions']:
        print(f"  {pred['month']}: ${pred['total_expenditure']:>8.2f}")
    
    print("\nInsights:")
    print("-" * 80)
    for i, insight in enumerate(result['insights'], 1):
        print(f"  {i}. {insight}")


def demo_comparison():
    """Compare income vs expenditure predictions"""
    print_section("INCOME vs EXPENDITURE COMPARISON")
    
    income_result = income_prediction_service.predict_income(
        historical_data=None,
        forecast_months=6
    )
    
    expenditure_result = expenditure_prediction_service.predict_expenditure(
        historical_data=None,
        forecast_months=6,
        by_category=True
    )
    
    print("6-Month Financial Forecast:")
    print("-" * 80)
    
    total_income = income_result['total_predicted_income']
    total_expenditure = expenditure_result['total_predicted_expenditure']
    net_savings = total_income - total_expenditure
    savings_rate = (net_savings / total_income) * 100
    
    print(f"  Predicted Income:       ${total_income:>10.2f}")
    print(f"  Predicted Expenditure:  ${total_expenditure:>10.2f}")
    print(f"  Net Savings:            ${net_savings:>10.2f}")
    print(f"  Savings Rate:           {savings_rate:>9.1f}%\n")
    
    if savings_rate > 20:
        status = "Excellent! ✓"
    elif savings_rate > 10:
        status = "Good ✓"
    elif savings_rate > 0:
        status = "Fair ~"
    else:
        status = "Concerning ✗"
    
    print(f"  Financial Health Status: {status}\n")
    
    print("Month-by-Month Breakdown:")
    print("-" * 80)
    print(f"{'Month':<10} {'Income':>10} {'Expenditure':>12} {'Net':>10}")
    print("-" * 80)
    
    for i in range(6):
        month = income_result['predictions'][i]['month']
        income = income_result['predictions'][i]['predicted_income']
        expenditure = expenditure_result['overall_predictions'][i]['total_expenditure']
        net = income - expenditure
        
        print(f"{month:<10} ${income:>9.2f} ${expenditure:>11.2f} ${net:>9.2f}")


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "AI INSIGHTS - PREDICTION MODULES DEMO" + " "*21 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        demo_income_prediction()
        demo_expenditure_prediction()
        demo_comparison()
        
        print_section("DEMO COMPLETE")
        print("✓ All prediction modules working successfully!")
        print("\nTo test via API, start the server with: uvicorn app.main:app --reload")
        print("Then visit: http://localhost:8000/docs for interactive API documentation\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
