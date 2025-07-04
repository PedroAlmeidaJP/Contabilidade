import streamlit as st
import database as db
from utils import aplicar_tema

st.set_page_config(page_title="Administração", page_icon="⚙️")
st.title("⚙️ Painel de Administração")
st.write("Aqui você gerencia os dados operacionais e contábeis do seu sistema.")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

tab_capital, tab_bens, tab_fornecedores, tab_clientes, tab_produtos, tab_estoque = st.tabs([
    "Capital e Caixa", "Bens (Patrimônio)", "Fornecedores", "Clientes", "Cadastro de Produtos", "Entrada de Estoque"
])

with tab_capital:
    st.header("Capital Social e Caixa")
    st.info("O Capital Social é o investimento inicial dos sócios. Ele entra diretamente no Caixa.")
    caixa_atual = db.get_conta_geral("caixa")
    capital_atual = db.get_conta_geral("capital_social")
    st.metric("Saldo Atual em Caixa", f"R$ {caixa_atual:,.2f}")
    st.metric("Capital Social Registrado", f"R$ {capital_atual:,.2f}")
    with st.form("form_capital"):
        valor_aporte = st.number_input("Valor do Aporte de Capital", min_value=0.01, format="%.2f")
        if st.form_submit_button("Realizar Aporte"):
            db.update_conta_geral("caixa", caixa_atual + valor_aporte)
            db.update_conta_geral("capital_social", capital_atual + valor_aporte)
            st.success("Aporte realizado com sucesso!")
            st.rerun()

with tab_bens:
    st.header("Compra de Bens para a Empresa")
    st.info("Bens para uso da empresa, como computadores, veículos. Não geram crédito de ICMS.")
    with st.form("form_bens"):
        nome_bem = st.text_input("Nome do Bem", placeholder="Ex: Notebook Dell para escritório")
        valor_bem = st.number_input("Valor do Bem", min_value=0.01, format="%.2f")
        tipo_pagamento = st.selectbox("Forma de Pagamento", ["À Vista (do Caixa)", "A Prazo"])
        if st.form_submit_button("Registrar Compra de Bem"):
            if nome_bem and valor_bem > 0:
                db.adicionar_bem(nome_bem, valor_bem)
                if tipo_pagamento == "À Vista (do Caixa)":
                    caixa_atual = db.get_conta_geral("caixa")
                    if caixa_atual >= valor_bem:
                        db.update_conta_geral("caixa", caixa_atual - valor_bem)
                        st.success("Compra de bem à vista registrada!")
                    else:
                        st.error("Caixa insuficiente!")
                else:
                    db.adicionar_conta_a_pagar(f"Compra de {nome_bem}", valor_bem, "Bem")
                    st.success("Compra de bem a prazo registrada!")
                st.rerun()
            else:
                st.warning("Por favor, preencha o nome e o valor do bem.")
    st.subheader("Bens Registrados")
    st.dataframe(db.df_from_sql("SELECT * FROM bens"), hide_index=True)

with tab_fornecedores:
    st.header("Gerenciar Fornecedores")
    with st.form("form_fornecedor", clear_on_submit=True):
        st.write("Cadastre um novo fornecedor")
        nome_fornecedor = st.text_input("Nome do Fornecedor", placeholder="Ex: InfoDistribuidora LTDA")
        cnpj_fornecedor = st.text_input("CNPJ", placeholder="00.000.000/0001-00")
        cidade_fornecedor = st.text_input("Cidade", placeholder="São Paulo")
        estado_fornecedor = st.text_input("Estado", placeholder="SP")
        if st.form_submit_button("Adicionar Fornecedor"):
            if not nome_fornecedor:
                st.warning("O nome do fornecedor é obrigatório.")
            else:
                db.adicionar_fornecedor(nome_fornecedor, cnpj_fornecedor, cidade_fornecedor, estado_fornecedor)
                st.success(f"Fornecedor '{nome_fornecedor}' adicionado com sucesso!")
    st.subheader("Fornecedores Cadastrados")
    st.dataframe(db.df_from_sql("SELECT id, nome, cnpj, cidade, estado FROM fornecedores"), hide_index=True, use_container_width=True)

with tab_clientes:
    st.header("Gerenciar Clientes")
    with st.form("form_cliente", clear_on_submit=True):
        st.write("Cadastre um novo cliente")
        nome_cliente = st.text_input("Nome do Cliente", placeholder="Ex: João da Silva")
        cpf_cnpj_cliente = st.text_input("CPF/CNPJ", placeholder="123.456.789-00")
        cidade_cliente = st.text_input("Cidade", placeholder="Santa Maria")
        estado_cliente = st.text_input("Estado", placeholder="RS")
        if st.form_submit_button("Adicionar Cliente"):
            if not nome_cliente:
                st.warning("O nome do cliente é obrigatório.")
            else:
                db.adicionar_cliente(nome_cliente, cpf_cnpj_cliente, cidade_cliente, estado_cliente)
                st.success(f"Cliente '{nome_cliente}' adicionado com sucesso!")
    st.subheader("Clientes Cadastrados")
    st.dataframe(db.df_from_sql("SELECT id, nome, cpf_cnpj, cidade, estado FROM clientes"), hide_index=True, use_container_width=True)

with tab_produtos:
    st.header("Cadastrar Novos Produtos")
    fornecedores = db.executar_query("SELECT id, nome FROM fornecedores", fetch="all")
    if not fornecedores:
        st.warning("Nenhum fornecedor cadastrado. Por favor, adicione um na aba 'Fornecedores'.")
    else:
        with st.form("form_produto", clear_on_submit=True):
            st.write("Cadastre um novo produto de informática")
            nome_produto = st.text_input("Nome do Produto")
            marca_produto = st.text_input("Marca do Produto")
            origem_produto = st.selectbox("Origem do Produto", ["Nacional", "Importado"])
            preco_compra = st.number_input("Preço de Compra (R$)", min_value=0.01, format="%.2f")
            preco_venda = st.number_input("Preço de Venda (R$)", min_value=0.01, format="%.2f")
            opcoes_fornecedores = {f[0]: f[1] for f in fornecedores}
            id_fornecedor = st.selectbox("Selecione o Fornecedor", options=list(opcoes_fornecedores.keys()), format_func=lambda x: opcoes_fornecedores[x])
            estoque_inicial = st.number_input("Quantidade de Estoque Inicial Comprada", min_value=0, step=1)

            if st.form_submit_button("Adicionar Produto"):
                if origem_produto == "Nacional":
                    aliq_credito = 0.12
                    aliq_debito = 0.18
                else:
                    aliq_credito = 0.04
                    aliq_debito = 0.04

                icms_credito = preco_compra * aliq_credito
                icms_debito = preco_venda * aliq_debito

                if not nome_produto or not marca_produto:
                    st.warning("Preencha todos os campos do produto.")
                else:
                    db.adicionar_produto(nome_produto, marca_produto, origem_produto, preco_compra, preco_venda, icms_credito, icms_debito, id_fornecedor, estoque_inicial)
                    st.success(f"Produto '{nome_produto}' adicionado com sucesso!")

    st.subheader("Produtos Cadastrados")
    query_produtos = """
        SELECT P.id, P.nome, P.marca, P.origem, P.preco_venda, P.estoque, F.nome AS fornecedor
        FROM produtos P
        LEFT JOIN fornecedores F ON P.id_fornecedor = F.id
    """
    st.dataframe(db.df_from_sql(query_produtos), hide_index=True, use_container_width=True)

with tab_estoque:
    st.header("Adicionar Estoque a um Produto Existente")
    produtos = db.executar_query("SELECT id, nome, estoque, preco_compra FROM produtos", fetch="all")
    if not produtos:
        st.warning("Nenhum produto cadastrado para adicionar estoque.")
    else:
        opcoes_produtos = {p[0]: f"{p[1]} (Estoque atual: {p[2]})" for p in produtos}

        with st.form("form_add_estoque", clear_on_submit=True):
            id_produto_selecionado = st.selectbox("Selecione o Produto", options=list(opcoes_produtos.keys()), format_func=lambda x: opcoes_produtos[x])
            quantidade_adicionada = st.number_input("Quantidade a Adicionar", min_value=1, step=1)
            tipo_pagamento_estoque = st.selectbox("Forma de Pagamento da Compra", ["À Vista (do Caixa)", "A Prazo"])

            parcelas_disabled = tipo_pagamento_estoque == "À Vista (do Caixa)"
            num_parcelas = st.number_input("Número de Parcelas", min_value=1, max_value=12, value=1, step=1, disabled=parcelas_disabled)

            if st.form_submit_button("Confirmar Entrada de Estoque"):
                produto_selecionado = next(p for p in produtos if p[0] == id_produto_selecionado)
                custo_unitario = produto_selecionado[3]
                custo_total = custo_unitario * quantidade_adicionada

                if tipo_pagamento_estoque == "À Vista (do Caixa)":
                    caixa_atual = db.get_conta_geral("caixa")
                    if caixa_atual >= custo_total:
                        db.update_conta_geral("caixa", caixa_atual - custo_total)
                        db.adicionar_estoque(id_produto_selecionado, quantidade_adicionada)
                        st.success("Estoque adicionado e pago à vista!")
                    else:
                        st.error("Caixa insuficiente para comprar este estoque!")
                else:
                    db.adicionar_conta_a_pagar(
                        f"Compra parcelada de {quantidade_adicionada}x {produto_selecionado[1]}",
                        custo_total,
                        "Mercadoria"
                    )
                    db.adicionar_estoque(id_produto_selecionado, quantidade_adicionada)
                    st.success("Estoque adicionado! Conta a pagar foi gerada.")
                st.rerun()
