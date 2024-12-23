import pandas as pd

def calculate_potential_returns(df: pd.DataFrame, spread_min: float, operational_cost: float = 5.0) -> pd.DataFrame:
    """Calculate potential returns based on spread opportunities"""
    opportunities = df[df['Difference'] >= spread_min].copy()
    
    if len(opportunities) == 0:
        return pd.DataFrame()
    
    opportunities['Gross_Return'] = opportunities['Difference'] - (spread_min / 2)
    opportunities['Total_Cost'] = operational_cost * 2  # Entry and exit costs
    opportunities['Net_Return'] = opportunities['Gross_Return'] - opportunities['Total_Cost']
    opportunities['Return_Percentage'] = (opportunities['Net_Return'] / opportunities['Total_Cost']) * 100
    
    return opportunities

def analyze_pair(stock_data_a: pd.Series, stock_data_b: pd.Series, spread_min: float) -> dict:
    """Analyze a stock pair and return key metrics"""
    df = pd.DataFrame({
        'Stock_A': stock_data_a,
        'Stock_B': stock_data_b
    })
    
    df['Difference'] = (df['Stock_A'] - df['Stock_B']).abs().round(2)
    opportunities = calculate_potential_returns(df, spread_min)
    
    return {
        'Spread_Mean': df['Difference'].mean(),
        'Spread_Max': df['Difference'].max(),
        'Total_Opportunities': len(opportunities),
        'Average_Return': opportunities['Net_Return'].mean() if len(opportunities) > 0 else 0,
        'Total_Return': opportunities['Net_Return'].sum() if len(opportunities) > 0 else 0,
        'Correlation': df['Stock_A'].corr(df['Stock_B'])
    }