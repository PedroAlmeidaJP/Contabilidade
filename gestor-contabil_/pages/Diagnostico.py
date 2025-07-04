import streamlit as st
import database as db

st.set_page_config(page_title="Diagnóstico do Banco de Dados", page_icon="🧪", layout="wide")
st.title("🧪 Diagnóstico de Dados")
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
import streamlit as st
from utils import aplicar_tema


# Produtos com preco_compra negativo
st.subheader("Produtos com preço de compra negativo")
prod_neg = db.df_from_sql("SELECT * FROM produtos WHERE preco_compra < 0")
if prod_neg.empty:
    st.success("Nenhum produto com preço de compra negativo.")
else:
    st.dataframe(prod_neg)

# Vendas com quantidade negativa
st.subheader("Vendas com quantidade negativa")
vendas_neg = db.df_from_sql("SELECT * FROM vendas WHERE quantidade < 0")
if vendas_neg.empty:
    st.success("Nenhuma venda com quantidade negativa.")
else:
    st.dataframe(vendas_neg)
