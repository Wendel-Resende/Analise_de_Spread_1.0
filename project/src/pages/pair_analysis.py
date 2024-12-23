import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from ..utils.stock_data import get_stock_data
from ..utils.spread_analysis import analyze_pair, calculate_potential_returns

def render_pair_analysis():
    st.subheader("📊 Análise de Par Específico")
    
    col1, col2 = st.columns(2)
    stock_a = col1.text_input("Ação A", value="PETR3").upper()
    stock_b = col2.text_input("Ação B", value="PETR4").upper()
    
    col1, col2, col3 = st.columns(3)
    start_date = col1.date_input("Data Inicial", datetime.now() - timedelta(days=365))
    end_date = col2.date_input("Data Final", datetime.now())
    spread_min = col3.number_input("Spread Mínimo (R$)", min_value=0.1, value=1.0, step=0.1)
    
    operational_cost = st.number_input("Custo Operacional por Operação (R$)", min_value=0.0, value=5.0, step=0.5)
    
    if st.button("Analisar Par"):
        try:
            with st.spinner('Analisando par de ações...'):
                stock_data_a = get_stock_data(stock_a, start_date, end_date)
                stock_data_b = get_stock_data(stock_b, start_date, end_date)
                
                analysis = analyze_pair(stock_data_a, stock_data_b, spread_min)
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Spread Médio", f"R$ {analysis['Spread_Mean']:.2f}")
                col2.metric("Total de Oportunidades", analysis['Total_Opportunities'])
                col3.metric("Retorno Total", f"R$ {analysis['Total_Return']:.2f}")
                col4.metric("Correlação", f"{analysis['Correlation']:.2f}")
                
                # Plot spread chart
                df = pd.DataFrame({
                    'Data': stock_data_a.index,
                    'Spread': (stock_data_a - stock_data_b).abs()
                })
                
                fig = px.line(
                    df,
                    x='Data',
                    y='Spread',
                    title=f'Spread {stock_a}/{stock_b}'
                )
                fig.add_hline(y=spread_min, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Erro na análise: {str(e)}")