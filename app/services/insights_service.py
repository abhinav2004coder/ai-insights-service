import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from collections import defaultdict
from sklearn.ensemble import IsolationForest
from app.models.schemas import (
    Transaction,
    SpendingPattern,
    BudgetRecommendation,
    AnomalyDetection,
    InsightsResponse,
)
from app.core.logger import logger


class InsightsService:
    """Service for generating AI-powered financial insights"""
    
    def __init__(self):
        self.anomaly_detector = IsolationForest(
            contamination=0.1,
            random_state=42
        )
    
    def analyze_transactions(
        self,
        transactions: List[Transaction],
        userId: str,
        include_income: bool = True
    ) -> InsightsResponse:
        """
        Analyze transactions and generate comprehensive insights
        
        Args:
            transactions: List of user transactions (both income and expense)
            userId: User ID
            include_income: Whether to include income analysis
            
        Returns:
            InsightsResponse with patterns, recommendations, and anomalies
        """
        logger.info(f"Analyzing {len(transactions)} transactions for user {userId}")
        
        if not transactions:
            return self._empty_insights(userId)
        
        # Convert to DataFrame for analysis
        df = self._transactions_to_dataframe(transactions)
        
        # Analyze income vs expense
        income_vs_expense = self._analyze_income_vs_expense(df)
        
        # Generate insights (only for expenses)
        expense_df = df[df['type'] == 'EXPENSE']
        spending_patterns = self._analyze_spending_patterns(expense_df)
        category_health = self._assess_category_health(expense_df, spending_patterns, income_vs_expense)
        budget_recommendations = self._generate_budget_recommendations(expense_df, spending_patterns)
        anomalies = self._detect_anomalies(expense_df, [t for t in transactions if hasattr(t, 'userId')])
        
        # Calculate aggregates
        total_spending = float(expense_df['amount'].sum()) if not expense_df.empty else 0.0
        
        # Calculate average daily spending
        date_range = (df['date'].max() - df['date'].min()).days
        avg_daily_spending = total_spending / max(date_range, 1)
        
        # Project monthly spending
        projected_monthly = avg_daily_spending * 30
        
        # Generate savings opportunities
        savings_opportunities = self._identify_savings_opportunities(
            spending_patterns,
            budget_recommendations
        )
        
        return InsightsResponse(
            userId=userId,
            incomeVsExpense=income_vs_expense,
            spendingPatterns=spending_patterns,
            categoryHealth=category_health,
            budgetRecommendations=budget_recommendations,
            anomalies=anomalies,
            totalSpending=total_spending,
            averageDailySpending=avg_daily_spending,
            projectedMonthlySpending=projected_monthly,
            savingsOpportunities=savings_opportunities,
        )
    
    def predict_spending(
        self,
        transactions: List[Transaction],
        category: str = None,
        days_ahead: int = 30
    ) -> Tuple[float, float]:
        """
        Predict future spending based on historical data
        
        Args:
            transactions: Historical transactions
            category: Optional category filter
            days_ahead: Number of days to predict
            
        Returns:
            Tuple of (predicted_amount, confidence)
        """
        if not transactions:
            return 0.0, 0.0
        
        df = self._transactions_to_dataframe(transactions)
        
        if category:
            df = df[df['category'] == category]
        
        if df.empty:
            return 0.0, 0.0
        
        # Simple moving average prediction
        daily_spending = df.groupby(df['date'].dt.date)['amount'].sum()
        avg_daily = daily_spending.mean()
        std_daily = daily_spending.std()
        
        predicted_amount = avg_daily * days_ahead
        
        # Calculate confidence based on variance
        cv = std_daily / avg_daily if avg_daily > 0 else 1.0
        confidence = max(0.0, min(1.0, 1.0 - cv))
        
        return float(predicted_amount), float(confidence)
    
    def _transactions_to_dataframe(self, transactions: List[Transaction]) -> pd.DataFrame:
        """Convert transactions to pandas DataFrame"""
        data = []
        for t in transactions:
            # Determine type from context - if it has type attribute use it, otherwise assume EXPENSE
            tx_type = getattr(t, 'type', 'EXPENSE')
            data.append({
                'id': t.id,
                'type': tx_type,
                'amount': t.amount,
                'category': t.category.value,
                'description': t.description or '',
                'date': pd.to_datetime(t.date),
                'userId': t.userId,
            })
        return pd.DataFrame(data)
    
    def _analyze_spending_patterns(self, df: pd.DataFrame) -> List[SpendingPattern]:
        """Analyze spending patterns by category"""
        total = df['amount'].sum()
        
        patterns = []
        for category in df['category'].unique():
            cat_data = df[df['category'] == category]
            cat_total = cat_data['amount'].sum()
            cat_count = len(cat_data)
            cat_avg = cat_total / cat_count
            
            patterns.append(SpendingPattern(
                category=category,
                totalAmount=float(cat_total),
                transactionCount=int(cat_count),
                averageAmount=float(cat_avg),
                percentage=float((cat_total / total) * 100) if total > 0 else 0.0,
            ))
        
        # Sort by total amount descending
        patterns.sort(key=lambda x: x.totalAmount, reverse=True)
        return patterns
    
    def _generate_budget_recommendations(
        self,
        df: pd.DataFrame,
        patterns: List[SpendingPattern]
    ) -> List[BudgetRecommendation]:
        """Generate budget recommendations based on spending patterns"""
        recommendations = []
        
        # Standard budget allocations (50/30/20 rule adapted)
        budget_guidelines = {
            'food': 0.15,  # 15% of income
            'utilities': 0.10,
            'transport': 0.10,
            'healthcare': 0.05,
            'entertainment': 0.05,
            'shopping': 0.10,
            'other': 0.05,
        }
        
        total_spending = df['amount'].sum()
        
        for pattern in patterns:
            category = pattern.category
            current_spending = pattern.totalAmount
            guideline_pct = budget_guidelines.get(category, 0.05)
            recommended = total_spending * guideline_pct
            
            # Determine priority based on overspending
            if current_spending > recommended * 1.5:
                priority = "high"
                reason = f"Spending is {((current_spending/recommended - 1) * 100):.0f}% over recommended budget"
            elif current_spending > recommended * 1.2:
                priority = "medium"
                reason = f"Spending is slightly above recommended budget"
            else:
                priority = "low"
                reason = f"Spending is within recommended range"
            
            recommendations.append(BudgetRecommendation(
                category=category,
                recommendedAmount=float(recommended),
                currentSpending=float(current_spending),
                reason=reason,
                priority=priority,
            ))
        
        return recommendations
    
    def _detect_anomalies(
        self,
        df: pd.DataFrame,
        transactions: List[Transaction]
    ) -> List[AnomalyDetection]:
        """Detect anomalous transactions using Isolation Forest"""
        if len(df) < 10:  # Not enough data for anomaly detection
            return []
        
        # Prepare features for anomaly detection
        features = df[['amount']].values
        
        # Fit and predict
        predictions = self.anomaly_detector.fit_predict(features)
        scores = self.anomaly_detector.score_samples(features)
        
        anomalies = []
        for idx, (pred, score) in enumerate(zip(predictions, scores)):
            if pred == -1:  # Anomaly detected
                transaction = transactions[idx]
                
                # Calculate category average for comparison
                cat_avg = df[df['category'] == transaction.category.value]['amount'].mean()
                
                reason = f"Amount is ${abs(transaction.amount - cat_avg):.2f} away from average {transaction.category.value} spending"
                
                anomalies.append(AnomalyDetection(
                    transactionId=transaction.id or f"tx_{idx}",
                    amount=transaction.amount,
                    category=transaction.category.value,
                    date=transaction.date,
                    anomalyScore=float(abs(score)),
                    reason=reason,
                ))
        
        return anomalies
    
    def _identify_savings_opportunities(
        self,
        patterns: List[SpendingPattern],
        recommendations: List[BudgetRecommendation]
    ) -> List[str]:
        """Identify potential savings opportunities"""
        opportunities = []
        
        # Find high-priority budget recommendations
        high_priority = [r for r in recommendations if r.priority == "high"]
        
        for rec in high_priority[:3]:  # Top 3 opportunities
            excess = rec.currentSpending - rec.recommendedAmount
            if excess > 0:
                opportunities.append(
                    f"Reduce {rec.category} spending by ${excess:.2f}/month to meet budget goals"
                )
        
        # Check for frequent small transactions
        for pattern in patterns:
            if pattern.transactionCount > 20 and pattern.averageAmount < 10:
                total_saved = pattern.transactionCount * pattern.averageAmount * 0.3
                opportunities.append(
                    f"Consolidate small {pattern.category} purchases to save up to ${total_saved:.2f}/month"
                )
        
        if not opportunities:
            opportunities.append("Your spending is well-balanced. Keep up the good work!")
        
        return opportunities[:5]  # Return top 5 opportunities
    
    def _analyze_income_vs_expense(self, df: pd.DataFrame) -> 'IncomeVsExpense':
        """Analyze income vs expense comparison"""
        from app.models.schemas import IncomeVsExpense
        
        total_income = float(df[df['type'] == 'INCOME']['amount'].sum()) if 'type' in df.columns else 0.0
        total_expense = float(df[df['type'] == 'EXPENSE']['amount'].sum()) if 'type' in df.columns else float(df['amount'].sum())
        net_balance = total_income - total_expense
        savings_rate = (net_balance / total_income * 100) if total_income > 0 else 0.0
        
        # Determine status
        if savings_rate >= 20:
            status = "healthy"
        elif savings_rate >= 10:
            status = "concerning"
        else:
            status = "critical"
        
        return IncomeVsExpense(
            totalIncome=total_income,
            totalExpense=total_expense,
            netBalance=net_balance,
            savingsRate=savings_rate,
            status=status
        )
    
    def _assess_category_health(self, df: pd.DataFrame, patterns: List['SpendingPattern'], income_data: 'IncomeVsExpense') -> List['CategoryHealth']:
        """Assess health of each spending category"""
        from app.models.schemas import CategoryHealth
        
        category_health = []
        total_expense = df['amount'].sum() if not df.empty else 1
        
        # Recommended percentages for each category
        recommended_pct = {
            'food': 15,
            'utilities': 10,
            'transport': 10,
            'healthcare': 5,
            'entertainment': 5,
            'shopping': 10,
            'other': 5,
        }
        
        for pattern in patterns:
            category = pattern.category
            current_pct = pattern.percentage
            recommended = recommended_pct.get(category, 5)
            
            # Determine status
            if current_pct <= recommended:
                status = "good"
                reason = f"Spending is within healthy limits ({current_pct:.1f}% of total)"
                recommendation = f"Great job managing your {category} expenses!"
            elif current_pct <= recommended * 1.5:
                status = "warning"
                reason = f"Spending is {((current_pct / recommended - 1) * 100):.0f}% over recommended"
                recommendation = f"Try to reduce {category} spending by ${pattern.totalAmount * 0.2:.2f}"
            else:
                status = "bad"
                reason = f"Spending is significantly over recommended ({current_pct:.1f}% vs {recommended}%)"
                recommendation = f"Priority: Cut {category} expenses by ${pattern.totalAmount * 0.3:.2f} or more"
            
            category_health.append(CategoryHealth(
                category=category,
                status=status,
                reason=reason,
                spending=pattern.totalAmount,
                recommendation=recommendation
            ))
        
        # Sort by status (bad first, then warning, then good)
        status_order = {"bad": 0, "warning": 1, "good": 2}
        category_health.sort(key=lambda x: status_order[x.status])
        
        return category_health
    
    def _empty_insights(self, userId: str) -> InsightsResponse:
        """Return empty insights when no transactions are available"""
        from app.models.schemas import IncomeVsExpense
        
        return InsightsResponse(
            userId=userId,
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


# Singleton instance
insights_service = InsightsService()
