import streamlit as st
import database as db
import pandas as pd
from datetime import date

st.set_page_config(page_title="Loja Tech", page_icon="🛍️", layout="wide")
st.title("🛍️ Bem-vindo à Loja Virtual Tech")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    df_produtos = db.df_from_sql("SELECT * FROM produtos WHERE estoque > 0")

    if df_produtos.empty:
        st.warning("Nenhum produto em estoque no momento. Volte mais tarde!")
    else:
        st.info("Navegue por nossos produtos e faça sua compra.")

        cols = st.columns(3)
        for index, produto in df_produtos.iterrows():
            col = cols[index % 3]
            with col:
                with st.container(border=True):
                    st.subheader(produto['nome'])
                    st.markdown(f"**Preço:** R$ {produto['preco_venda']:,.2f}")
                    st.markdown(f"**Em estoque:** {produto['estoque']} unidades")

                    with st.expander("Comprar este item"):
                        with st.form(key=f"form_compra_{produto['id']}", clear_on_submit=True):
                            clientes = db.executar_query("SELECT id, nome FROM clientes", fetch="all")
                            opcoes_clientes = {c[0]: c[1] for c in clientes}

                            if not opcoes_clientes:
                                st.error("Nenhum cliente cadastrado. Por favor, cadastre um cliente no painel de Administração.")
                            else:
                                id_cliente = st.selectbox(
                                    "Selecione o Cliente",
                                    options=list(opcoes_clientes.keys()),
                                    format_func=lambda x: opcoes_clientes[x],
                                    key=f"cliente_{produto['id']}"
                                )

                                quantidade = st.number_input(
                                    "Quantidade",
                                    min_value=1,
                                    max_value=int(produto['estoque']),
                                    step=1,
                                    key=f"qtd_{produto['id']}"
                                )

                                tipo_pagamento = st.selectbox(
                                    "Forma de Pagamento",
                                    ["À Vista", "A Prazo"],
                                    key=f"pagamento_{produto['id']}"
                                )

                                if tipo_pagamento == "A Prazo":
                                    parcelas = st.number_input(
                                        "Número de Parcelas",
                                        min_value=1,
                                        max_value=12,
                                        step=1,
                                        key=f"parcelas_{produto['id']}"
                                    )
                                else:
                                    parcelas = 1

                                submitted = st.form_submit_button("Finalizar Compra")

                                if submitted:
                                    total_venda = produto['preco_venda'] * quantidade
                                    data_venda = date.today()

                                    db.adicionar_venda(
                                        produto['id'],
                                        id_cliente,
                                        quantidade,
                                        total_venda,
                                        tipo_pagamento,
                                        data_venda,
                                        parcelas
                                    )

                                    novo_estoque = produto['estoque'] - quantidade
                                    db.executar_query(
                                        "UPDATE produtos SET estoque = ? WHERE id = ?",
                                        (novo_estoque, produto['id'])
                                    )

                                    if tipo_pagamento == "À Vista":
                                        caixa_atual = db.get_conta_geral("caixa")
                                        db.update_conta_geral("caixa", caixa_atual + total_venda)
                                    else:
                                        id_venda = db.executar_query("SELECT last_insert_rowid()", fetch="one")[0]
                                        db.adicionar_conta_a_receber(id_venda, f"Venda de {produto['nome']}", total_venda)

                                    st.success(f"Compra realizada com sucesso! Total: R$ {total_venda:,.2f}")
                                    st.rerun()

except Exception as e:
    st.error(f"Ocorreu um erro ao carregar a loja: {e}")
