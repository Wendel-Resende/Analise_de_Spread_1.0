import streamlit as st
import pandas as pd
import plotly.express as px
from itertools import combinations
from datetime import datetime, timedelta
from utils.stock_data import get_stock_data
from utils.spread_analysis import analyze_pair

def render_ranking():
    st.subheader("🏆 Ranking dos Melhores Pares")
    
    suggested_stocks = [
        'PETR3', 'PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3', 'BBAS3',
        'ELET3', 'ELET6', 'GGBR4', 'ITSA4', 'MGLU3', 'RENT3', 'SUZB3'
    ]
    
    col1, col2, col3 = st.columns(3)
    start_date = col1.date_input("Data Inicial (Ranking)", datetime.now() - timedelta(days=365))
    end_date = col2.date_input("Data Final (Ranking)", datetime.now())
    spread_min = col3.number_input("Spread Mínimo (Ranking)", min_value=0.1, value=1.0, step=0.1)
    
    col1, col2 = st.columns(2)
    num_stocks = col1.number_input("Número de ações para análise", min_value=2, max_value=len(suggested_stocks), value=5)
    ranking_criteria = col2.selectbox(
        "Critério de Ranking",
        ["Retorno Total", "Retorno Médio", "Número de Oportunidades"]
    )
    
    if st.button("Gerar Ranking"):
        try:
            with st.spinner('Analisando pares...'):
                pairs = list(combinations(suggested_stocks[:num_stocks], 2))
                results = []
                
                for stock_a, stock_b in pairs:
                    stock_data_a = get_stock_data(stock_a, start_date, end_date)
                    stock_data_b = get_stock_data(stock_b, start_date, end_date)
                    
                    analysis = analyze_pair(stock_data_a, stock_data_b, spread_min)
                    analysis['Pair'] = f"{stock_a}/{stock_b}"
                    results.append(analysis)
                
                if results:
                    df_ranking = pd.DataFrame(results)
                    
                    criteria_map = {
                        "Retorno Total": "Total_Return",
                        "Retorno Médio": "Average_Return",
                        "Número de Oportunidades": "Total_Opportunities"
                    }
                    
                    df_ranking = df_ranking.sort_values(
                        criteria_map[ranking_criteria],
                        ascending=False
                    )
                    
                    st.dataframe(df_ranking)
                    
                    fig = px.bar(
                        df_ranking,
                        x='Pair',
                        y=criteria_map[ranking_criteria],
                        title=f'Comparação de Pares por {ranking_criteria}'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Erro ao gerar ranking: {str(e)}")