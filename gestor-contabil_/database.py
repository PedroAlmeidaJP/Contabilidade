import sqlite3
import pandas as pd

DB_NAME = "gestor.db"

def conectar():
    """Cria uma conexão com o banco de dados."""
    return sqlite3.connect(DB_NAME)

def criar_tabelas():
    """Cria TODAS as tabelas do banco de dados se elas não existirem."""
    conn = conectar()
    cursor = conn.cursor()
    
    # --- Tabela de Produtos com a nova coluna 'origem' ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL UNIQUE, marca TEXT, origem TEXT,
        preco_compra REAL NOT NULL, preco_venda REAL NOT NULL, icms_credito REAL NOT NULL,
        icms_debito REAL NOT NULL, id_fornecedor INTEGER, estoque INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (id_fornecedor) REFERENCES fornecedores (id)
    )""")
    
    # --- Outras tabelas (sem alterações) ---
    cursor.execute("CREATE TABLE IF NOT EXISTS fornecedores (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL UNIQUE, cnpj TEXT, cidade TEXT, estado TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, cpf_cnpj TEXT UNIQUE, cidade TEXT, estado TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS vendas (id INTEGER PRIMARY KEY AUTOINCREMENT, id_produto INTEGER NOT NULL, id_cliente INTEGER NOT NULL, quantidade INTEGER NOT NULL, total_venda REAL NOT NULL, tipo_pagamento TEXT, data_venda DATE, FOREIGN KEY (id_produto) REFERENCES produtos (id), FOREIGN KEY (id_cliente) REFERENCES clientes (id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS contas_gerais (nome_conta TEXT PRIMARY KEY, valor REAL NOT NULL DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS bens (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, valor REAL NOT NULL, data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cursor.execute("CREATE TABLE IF NOT EXISTS contas_a_pagar (id INTEGER PRIMARY KEY AUTOINCREMENT, origem TEXT NOT NULL, valor REAL NOT NULL, tipo TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS contas_a_receber (id INTEGER PRIMARY KEY AUTOINCREMENT, id_venda INTEGER, origem TEXT NOT NULL, valor REAL NOT NULL)")

    conn.commit()
    conn.close()

def executar_query(query, params=(), fetch=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetch == "all": resultado = cursor.fetchall()
    elif fetch == "one": resultado = cursor.fetchone()
    else:
        resultado = None
        conn.commit()
    conn.close()
    return resultado

def df_from_sql(query, params=()):
    conn = conectar()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# --- Funções de Adicionar Dados (com 'origem') ---
def adicionar_produto(nome, marca, origem, preco_compra, preco_venda, icms_credito, icms_debito, id_fornecedor, estoque_inicial):
    query = "INSERT INTO produtos (nome, marca, origem, preco_compra, preco_venda, icms_credito, icms_debito, id_fornecedor, estoque) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    executar_query(query, (nome, marca, origem, preco_compra, preco_venda, icms_credito, icms_debito, id_fornecedor, estoque_inicial))

# --- Funções existentes (sem alterações) ---
def adicionar_fornecedor(nome, cnpj, cidade, estado):
    executar_query("INSERT INTO fornecedores (nome, cnpj, cidade, estado) VALUES (?, ?, ?, ?)", (nome, cnpj, cidade, estado))
def adicionar_cliente(nome, cpf_cnpj, cidade, estado):
    executar_query("INSERT INTO clientes (nome, cpf_cnpj, cidade, estado) VALUES (?, ?, ?, ?)", (nome, cpf_cnpj, cidade, estado))
def adicionar_venda(id_produto, id_cliente, quantidade, total_venda, tipo_pagamento, data_venda):
    executar_query("INSERT INTO vendas (id_produto, id_cliente, quantidade, total_venda, tipo_pagamento, data_venda) VALUES (?, ?, ?, ?, ?, ?)", (id_produto, id_cliente, quantidade, total_venda, tipo_pagamento, data_venda))
def adicionar_estoque(id_produto, quantidade_adicionada):
    estoque_atual = executar_query("SELECT estoque FROM produtos WHERE id = ?", (id_produto,), fetch="one")[0]
    novo_estoque = estoque_atual + quantidade_adicionada
    executar_query("UPDATE produtos SET estoque = ? WHERE id = ?", (novo_estoque, id_produto))
def get_conta_geral(nome_conta):
    resultado = executar_query("SELECT valor FROM contas_gerais WHERE nome_conta = ?", (nome_conta,), fetch="one")
    return resultado[0] if resultado else 0
def update_conta_geral(nome_conta, valor):
    executar_query("INSERT OR REPLACE INTO contas_gerais (nome_conta, valor) VALUES (?, ?)", (nome_conta, valor))
def adicionar_bem(nome, valor):
    executar_query("INSERT INTO bens (nome, valor) VALUES (?, ?)", (nome, valor))
def adicionar_conta_a_pagar(origem, valor, tipo):
    executar_query("INSERT INTO contas_a_pagar (origem, valor, tipo) VALUES (?, ?, ?)", (origem, valor, tipo))
def adicionar_conta_a_receber(id_venda, origem, valor):
    executar_query("INSERT INTO contas_a_receber (id_venda, origem, valor) VALUES (?, ?, ?)", (id_venda, origem, valor))

# --- Execução Inicial ---
criar_tabelas()