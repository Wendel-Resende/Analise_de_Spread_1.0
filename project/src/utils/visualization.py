"""
Visualization utilities for creating charts and plots
"""
import matplotlib.pyplot as plt

def create_spread_chart(df, spread_min, stock_a, stock_b):
    """
    Create a spread chart using matplotlib
    
    Args:
        df (pd.DataFrame): DataFrame with Data and Spread columns
        spread_min (float): Minimum spread value for horizontal line
        stock_a (str): First stock ticker
        stock_b (str): Second stock ticker
        
    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['Data'], df['Spread'])
    ax.axhline(y=spread_min, color='r', linestyle='--')
    ax.set_title(f'Spread {stock_a}/{stock_b}')
    ax.set_xlabel('Data')
    ax.set_ylabel('Spread (R$)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig