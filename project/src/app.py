import streamlit as st
import os
import sys

# Adiciona o diretório raiz do projeto ao PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

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