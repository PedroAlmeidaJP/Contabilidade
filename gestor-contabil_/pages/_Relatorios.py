import streamlit as st
import database as db
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Relatórios", page_icon="📊", layout="wide")
st.title("📊 Relatórios")
import streamlit as st
from utils import aplicar_tema


with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


tab_vendas, tab_clientes, tab_inventario = st.tabs(["Relatório de Vendas", "Relatório de Clientes", "Relatório de Inventário"])

with tab_vendas:
    st.header("Análise de Vendas")

    col1, col2 = st.columns(2)
    with col1:
        marcas_disponiveis = ["Todas"] + [m[0] for m in db.executar_query("SELECT DISTINCT marca FROM produtos ORDER BY marca", fetch="all")]
        marca_selecionada = st.selectbox("Filtrar por Marca", options=marcas_disponiveis)
    with col2:
        tipo_visao_vendas = st.radio("Visão", ["Analítica (Detalhada)", "Sintética (Resumida)"], horizontal=True)

    query = """
        SELECT V.data_venda, P.nome as produto, P.marca, C.nome as cliente, V.quantidade, V.total_venda, (V.total_venda - (P.preco_compra * V.quantidade)) as lucro
        FROM vendas V
        JOIN produtos P ON V.id_produto = P.id
        JOIN clientes C ON V.id_cliente = C.id
    """
    params = []
    if marca_selecionada != "Todas":
        query += " WHERE P.marca = ?"
        params.append(marca_selecionada)

    df_vendas = db.df_from_sql(query, tuple(params))

    if df_vendas.empty:
        st.warning("Nenhuma venda encontrada para os filtros selecionados.")
    elif tipo_visao_vendas == "Analítica (Detalhada)":
        st.dataframe(df_vendas, hide_index=True)
    else:
        st.subheader("Vendas Agrupadas por Produto")
        df_vendas = df_vendas.copy()
        df_vendas = df_vendas.groupby('produto').agg(
            quantidade_vendida=('quantidade', 'sum'),
            faturamento_total=('total_venda', 'sum'),
            lucro_total=('lucro', 'sum')
        ).reset_index()
        st.dataframe(df_vendas, hide_index=True)

    if not df_vendas.empty:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_vendas.to_excel(writer, sheet_name="Relatorio_Vendas", index=False)
        output.seek(0)

        st.download_button(
            label="📥 Exportar Relatório de Vendas",
            data=output,
            file_name="relatorio_vendas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with tab_clientes:
    st.header("Análise de Clientes")
    query = """
        SELECT C.nome, C.cidade, C.estado,
        COUNT(V.id) as total_compras,
        SUM(V.total_venda) as valor_gasto
        FROM clientes C
        LEFT JOIN vendas V ON C.id = V.id_cliente
        GROUP BY C.id
    """
    df_clientes = db.df_from_sql(query)
    st.dataframe(df_clientes, hide_index=True)

    if not df_clientes.empty:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_clientes.to_excel(writer, sheet_name="Relatorio_Clientes", index=False)
        output.seek(0)

        st.download_button(
            label="📥 Exportar Relatório de Clientes",
            data=output,
            file_name="relatorio_clientes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with tab_inventario:
    st.header("Análise de Inventário (Estoque)")
    query_inventario = """
        SELECT nome, marca, estoque, preco_compra,
               (estoque * preco_compra) as valor_total_em_estoque
        FROM produtos
        WHERE estoque > 0
        ORDER BY valor_total_em_estoque DESC
    """
    df_inventario = db.df_from_sql(query_inventario)
    st.dataframe(df_inventario, hide_index=True)

    valor_total_inventario = db.df_from_sql("SELECT SUM(estoque * preco_compra) as total FROM produtos")['total'].iloc[0] or 0
    st.metric("Valor Total do Inventário", f"R$ {valor_total_inventario:,.2f}")

    if not df_inventario.empty:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_inventario.to_excel(writer, sheet_name="Relatorio_Inventario", index=False)
        output.seek(0)

        st.download_button(
            label="📥 Exportar Relatório de Inventário",
            data=output,
            file_name="relatorio_inventario.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
