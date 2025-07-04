import streamlit as st
import logic
import pandas as pd
import io

st.set_page_config(page_title="Relatórios Contábeis", page_icon="📚", layout="wide")
st.title("📚 Relatórios Contábeis")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
import streamlit as st
from utils import aplicar_tema




aba_dre, aba_balanco, aba_contas = st.tabs([
    "DRE - Demonstração de Resultados",
    "Balanço Patrimonial",
    "Contas a Pagar e a Receber"
])

# --- DRE ---
with aba_dre:
    st.subheader("Demonstração de Resultados do Exercício (DRE)")
    dre_data = logic.calcular_dre()
    df_dre = pd.DataFrame(dre_data.items(), columns=["Descrição", "Valor"])
    st.dataframe(df_dre, hide_index=True)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_dre.to_excel(writer, index=False, sheet_name="DRE")
    output.seek(0)

    st.download_button(
        label="📥 Exportar DRE para Excel",
        data=output,
        file_name="dre.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- Balanço Patrimonial ---
with aba_balanco:
    st.subheader("Balanço Patrimonial")
    balanco = logic.calcular_balanco_patrimonial()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Ativo")
        for k, v in balanco["ativo"].items():
            st.write(f"{k}: R$ {v:,.2f}")

    with col2:
        st.markdown("### Passivo + Patrimônio Líquido")
        for k, v in balanco["passivo_pl"].items():
            st.write(f"{k}: R$ {v:,.2f}")

    df_ativo = pd.DataFrame(balanco["ativo"].items(), columns=["Descrição", "Valor"])
    df_passivo = pd.DataFrame(balanco["passivo_pl"].items(), columns=["Descrição", "Valor"])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_ativo.to_excel(writer, sheet_name="Ativo", index=False)
        df_passivo.to_excel(writer, sheet_name="Passivo+PL", index=False)
    output.seek(0)

    st.download_button(
        label="📥 Exportar Balanço Patrimonial",
        data=output,
        file_name="balanco_patrimonial.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- Contas a Pagar e a Receber ---
with aba_contas:
    st.subheader("Contas a Pagar e a Receber")
    df_contas = logic.relatorio_contas()
    if df_contas.empty:
        st.warning("Nenhuma conta registrada.")
    else:
        st.dataframe(df_contas, hide_index=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_contas.to_excel(writer, sheet_name="Contas", index=False)
        output.seek(0)

        st.download_button(
            label="📥 Exportar Contas Pagar/Receber",
            data=output,
            file_name="contas_pagar_receber.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
