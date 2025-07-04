import streamlit as st
import database as db
import logic
import pandas as pd
import io

st.set_page_config(page_title="Gestor Financeiro", page_icon="🏠", layout="wide")

st.title("🏠 Dashboard Principal")
st.markdown("Bem-vindo.")
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    dre_data = logic.calcular_dre()
    lucro = dre_data.get("Lucro do Período", 0)

    df_faturamento = db.df_from_sql("SELECT SUM(total_venda) as total FROM vendas")
    total_vendas = df_faturamento['total'].iloc[0] if not df_faturamento.empty and df_faturamento['total'].iloc[0] is not None else 0
    df_produtos = db.df_from_sql("SELECT COUNT(*) as count FROM produtos")
    num_produtos = df_produtos['count'].iloc[0] if not df_produtos.empty else 0
    df_clientes = db.df_from_sql("SELECT COUNT(*) as count FROM clientes")
    num_clientes = df_clientes['count'].iloc[0] if not df_clientes.empty else 0

    st.header("Resumo Geral")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Faturamento Total", f"R$ {total_vendas:,.2f}")
    col2.metric("📈 Lucro do Período", f"R$ {lucro:,.2f}")
    col3.metric("📦 Produtos Cadastrados", num_produtos)
    col4.metric("👥 Clientes Cadastrados", num_clientes)

    st.info("Use o menu na barra lateral para navegar.")

    st.subheader("Últimas Vendas")
    ultimas_vendas_query = """
    SELECT V.id, P.nome as produto, C.nome as cliente, V.quantidade, V.total_venda, V.data_venda
    FROM vendas V
    JOIN produtos P ON V.id_produto = P.id
    JOIN clientes C ON V.id_cliente = C.id
    ORDER BY V.data_venda DESC
    LIMIT 10
    """
    df_vendas = db.df_from_sql(ultimas_vendas_query)
    if df_vendas.empty:
        st.warning("Nenhuma venda registrada ainda.")
    else:
        st.dataframe(df_vendas, hide_index=True, use_container_width=True)

    st.subheader("📊 Balanço Patrimonial")

    if st.button("Exibir Balanço Patrimonial"):
        balanco = logic.calcular_balanco_patrimonial()
        st.markdown("### Ativo")
        for k, v in balanco["ativo"].items():
            st.write(f"{k}: R$ {v:,.2f}")
        st.markdown("### Passivo + Patrimônio Líquido")
        for k, v in balanco["passivo_pl"].items():
            st.write(f"{k}: R$ {v:,.2f}")

    if st.button("Exportar para Excel"):
        balanco = logic.calcular_balanco_patrimonial()
        df_ativo = pd.DataFrame(balanco["ativo"].items(), columns=["Descrição", "Valor"])
        df_passivo = pd.DataFrame(balanco["passivo_pl"].items(), columns=["Descrição", "Valor"])

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_ativo.to_excel(writer, sheet_name="Ativo", index=False)
            df_passivo.to_excel(writer, sheet_name="Passivo+PL", index=False)
        output.seek(0)

        st.download_button(
            label="📥 Baixar Excel do Balanço",
            data=output,
            file_name="balanco_patrimonial.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

except Exception as e:
    st.error(f"Ocorreu um erro ao carregar o dashboard: {e}")
