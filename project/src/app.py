import streamlit as st
from config.settings import PROJECT_ROOT, SRC_DIR
import sys

# Adiciona os diretórios necessários ao PYTHONPATH
sys.path.extend([PROJECT_ROOT, SRC_DIR])

from src.pages.pair_analysis import render_pair_analysis
from src.pages.ranking import render_ranking

def main():
    st.set_page_config(
        page_title="Análise de Spread entre Ações",
        layout="wide"
    )
    
    st.title("📈 Análise de Spread entre Ações")
    
    tab1, tab2 = st.tabs(["Análise de Par", "Ranking"])
    
    with tab1:
        render_pair_analysis()
    
    with tab2:
        render_ranking()

if __name__ == "__main__":
    main()