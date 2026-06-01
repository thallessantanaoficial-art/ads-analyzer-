import pandas as pd
import numpy as np
from typing import Dict, List, Any

class AdsAnalyzer:
    """Analyze Google Ads and Meta Ads metrics from CSV files"""
    
    def __init__(self, csv_file_path: str):
        self.df = pd.read_csv(csv_file_path)
        self.metrics = {}
        self.insights = []
        
    def get_column_mapping(self) -> Dict[str, str]:
        """Map common column names to standard metrics"""
        columns_lower = {col.lower().strip(): col for col in self.df.columns}
        
        mapping = {}
        
        # Impressions
        for key in columns_lower:
            if 'impression' in key:
                mapping['impressions'] = columns_lower[key]
                break
        
        # Clicks
        for key in columns_lower:
            if 'click' in key and 'clickthrough' not in key:
                mapping['clicks'] = columns_lower[key]
                break
        
        # Cost/Spend
        for key in columns_lower:
            if 'cost' in key or 'spend' in key:
                mapping['cost'] = columns_lower[key]
                break
        
        # Conversions
        for key in columns_lower:
            if 'conversion' in key and 'rate' not in key:
                mapping['conversions'] = columns_lower[key]
                break
        
        # Conversion Value
        for key in columns_lower:
            if 'conversion value' in key or 'revenue' in key:
                mapping['conversion_value'] = columns_lower[key]
                break
        
        return mapping
    
    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate key performance metrics"""
        mapping = self.get_column_mapping()
        metrics = {
            'total_rows': len(self.df),
            'date_range': f"{self.df.iloc[0, 0]} to {self.df.iloc[-1, 0]}" if len(self.df) > 0 else "N/A"
        }
        
        # Total Impressions
        if 'impressions' in mapping:
            col = mapping['impressions']
            metrics['total_impressions'] = int(pd.to_numeric(self.df[col], errors='coerce').sum())
        
        # Total Clicks
        if 'clicks' in mapping:
            col = mapping['clicks']
            metrics['total_clicks'] = int(pd.to_numeric(self.df[col], errors='coerce').sum())
        
        # Total Cost/Spend
        if 'cost' in mapping:
            col = mapping['cost']
            cost_values = pd.to_numeric(self.df[col], errors='coerce')
            metrics['total_cost'] = round(cost_values.sum(), 2)
        
        # Total Conversions
        if 'conversions' in mapping:
            col = mapping['conversions']
            metrics['total_conversions'] = int(pd.to_numeric(self.df[col], errors='coerce').sum())
        
        # Total Conversion Value/Revenue
        if 'conversion_value' in mapping:
            col = mapping['conversion_value']
            revenue = pd.to_numeric(self.df[col], errors='coerce')
            metrics['total_revenue'] = round(revenue.sum(), 2)
        
        # CTR (Click-Through Rate)
        if 'impressions' in mapping and 'clicks' in mapping:
            impr_col = mapping['impressions']
            click_col = mapping['clicks']
            impressions = pd.to_numeric(self.df[impr_col], errors='coerce').sum()
            clicks = pd.to_numeric(self.df[click_col], errors='coerce').sum()
            if impressions > 0:
                metrics['ctr'] = round((clicks / impressions) * 100, 2)
        
        # CPC (Cost Per Click)
        if 'cost' in mapping and 'clicks' in mapping:
            cost_col = mapping['cost']
            click_col = mapping['clicks']
            cost = pd.to_numeric(self.df[cost_col], errors='coerce').sum()
            clicks = pd.to_numeric(self.df[click_col], errors='coerce').sum()
            if clicks > 0:
                metrics['cpc'] = round(cost / clicks, 2)
        
        # CPM (Cost Per Mille/Thousand Impressions)
        if 'cost' in mapping and 'impressions' in mapping:
            cost_col = mapping['cost']
            impr_col = mapping['impressions']
            cost = pd.to_numeric(self.df[cost_col], errors='coerce').sum()
            impressions = pd.to_numeric(self.df[impr_col], errors='coerce').sum()
            if impressions > 0:
                metrics['cpm'] = round((cost / impressions) * 1000, 2)
        
        # CPA (Cost Per Acquisition)
        if 'cost' in mapping and 'conversions' in mapping:
            cost_col = mapping['cost']
            conv_col = mapping['conversions']
            cost = pd.to_numeric(self.df[cost_col], errors='coerce').sum()
            conversions = pd.to_numeric(self.df[conv_col], errors='coerce').sum()
            if conversions > 0:
                metrics['cpa'] = round(cost / conversions, 2)
        
        # Conversion Rate
        if 'clicks' in mapping and 'conversions' in mapping:
            click_col = mapping['clicks']
            conv_col = mapping['conversions']
            clicks = pd.to_numeric(self.df[click_col], errors='coerce').sum()
            conversions = pd.to_numeric(self.df[conv_col], errors='coerce').sum()
            if clicks > 0:
                metrics['conversion_rate'] = round((conversions / clicks) * 100, 2)
        
        # ROAS (Return On Ad Spend)
        if 'conversion_value' in mapping and 'cost' in mapping:
            rev_col = mapping['conversion_value']
            cost_col = mapping['cost']
            revenue = pd.to_numeric(self.df[rev_col], errors='coerce').sum()
            cost = pd.to_numeric(self.df[cost_col], errors='coerce').sum()
            if cost > 0:
                metrics['roas'] = round(revenue / cost, 2)
        
        # Average CPC
        if 'cost' in mapping and 'clicks' in mapping:
            cost_col = mapping['cost']
            click_col = mapping['clicks']
            avg_cost = pd.to_numeric(self.df[cost_col], errors='coerce').mean()
            metrics['avg_daily_cost'] = round(avg_cost, 2)
        
        self.metrics = metrics
        return metrics
    
    def generate_insights(self) -> List[Dict[str, str]]:
        """Generate actionable insights based on metrics"""
        insights = []
        
        if not self.metrics:
            self.calculate_metrics()
        
        # CTR Analysis
        if 'ctr' in self.metrics:
            ctr = self.metrics['ctr']
            if ctr < 1:
                insights.append({
                    'type': 'warning',
                    'title': 'Low Click-Through Rate',
                    'message': f'Your CTR is {ctr}%, which is below average. Consider improving your ad copy and targeting.'
                })
            elif ctr > 5:
                insights.append({
                    'type': 'success',
                    'title': 'Excellent CTR',
                    'message': f'Your CTR of {ctr}% shows strong ad relevance and engagement.'
                })
        
        # CPC Analysis
        if 'cpc' in self.metrics:
            cpc = self.metrics['cpc']
            if cpc > 5:
                insights.append({
                    'type': 'warning',
                    'title': 'High Cost Per Click',
                    'message': f'Your CPC is ${cpc}, which is high. Review your bidding strategy and keyword quality score.'
                })
        
        # Conversion Rate Analysis
        if 'conversion_rate' in self.metrics:
            conv_rate = self.metrics['conversion_rate']
            if conv_rate < 0.5:
                insights.append({
                    'type': 'warning',
                    'title': 'Low Conversion Rate',
                    'message': f'Your conversion rate is {conv_rate}%. Optimize landing pages and improve user experience.'
                })
            elif conv_rate > 3:
                insights.append({
                    'type': 'success',
                    'title': 'Strong Conversion Rate',
                    'message': f'Your conversion rate of {conv_rate}% indicates excellent campaign performance.'
                })
        
        # ROAS Analysis
        if 'roas' in self.metrics:
            roas = self.metrics['roas']
            if roas < 2:
                insights.append({
                    'type': 'warning',
                    'title': 'Low Return on Ad Spend',
                    'message': f'Your ROAS is {roas}x. To be profitable, aim for at least 3-4x ROAS.'
                })
            elif roas >= 4:
                insights.append({
                    'type': 'success',
                    'title': 'Excellent ROAS',
                    'message': f'Your ROAS of {roas}x is excellent! Your campaigns are highly profitable.'
                })
        
        # Cost Analysis
        if 'total_cost' in self.metrics and 'total_clicks' in self.metrics:
            if self.metrics['total_clicks'] > 0:
                avg_daily_cost = self.metrics['total_cost'] / max(self.metrics['total_rows'], 1)
                if avg_daily_cost > 100:
                    insights.append({
                        'type': 'info',
                        'title': 'High Daily Spend',
                        'message': f'Your average daily spend is ${avg_daily_cost:.2f}. Monitor ROI closely.'
                    })
        
        # Impressions Analysis
        if 'total_impressions' in self.metrics:
            impressions = self.metrics['total_impressions']
            if impressions > 100000:
                insights.append({
                    'type': 'info',
                    'title': 'High Impression Volume',
                    'message': f'You\'ve achieved {impressions:,} impressions. Ensure your conversion funnel is optimized.'
                })
        
        self.insights = insights
        return insights
    
    def get_daily_performance(self) -> List[Dict]:
        """Get daily performance data for charts"""
        try:
            date_col = self.df.columns[0]
            mapping = self.get_column_mapping()
            
            daily_data = []
            for idx, row in self.df.iterrows():
                day_data = {'date': str(row[date_col])}
                
                if 'impressions' in mapping:
                    day_data['impressions'] = int(pd.to_numeric(row[mapping['impressions']], errors='coerce') or 0)
                if 'clicks' in mapping:
                    day_data['clicks'] = int(pd.to_numeric(row[mapping['clicks']], errors='coerce') or 0)
                if 'cost' in mapping:
                    day_data['cost'] = round(pd.to_numeric(row[mapping['cost']], errors='coerce') or 0, 2)
                if 'conversions' in mapping:
                    day_data['conversions'] = int(pd.to_numeric(row[mapping['conversions']], errors='coerce') or 0)
                
                daily_data.append(day_data)
            
            return daily_data
        except:
            return []
