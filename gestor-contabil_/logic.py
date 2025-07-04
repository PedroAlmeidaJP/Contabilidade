import database as db
import pandas as pd

def calcular_dre():
    """Calcula a Demonstração do Resultado do Exercício (DRE)."""
    query = """
    SELECT 
        SUM(V.total_venda) as receita_bruta,
        SUM(P.preco_compra * V.quantidade) as cmv
    FROM vendas V
    JOIN produtos P ON V.id_produto = P.id
    """
    df = db.df_from_sql(query)

    if df.empty or df['receita_bruta'].iloc[0] is None:
        return {"Receita de Vendas": 0, "CMV": 0, "Lucro do Período": 0}

    receita = df['receita_bruta'].iloc[0]
    cmv = df['cmv'].iloc[0]
    lucro = receita - cmv

    return {
        "Receita de Vendas": receita,
        "CMV": cmv,  # agora positivo
        "Lucro do Período": lucro
    }

def calcular_balanco_patrimonial():
    """Calcula todos os componentes do Balanço Patrimonial."""
    dre = calcular_dre()
    lucro_acumulado = dre["Lucro do Período"]

    caixa = db.get_conta_geral("caixa")
    total_estoque = db.df_from_sql("SELECT SUM(preco_compra * estoque) as total FROM produtos")['total'].iloc[0] or 0
    total_contas_a_receber = db.df_from_sql("SELECT SUM(valor) as total FROM contas_a_receber")['total'].iloc[0] or 0
    total_bens = db.df_from_sql("SELECT SUM(valor) as total FROM bens")['total'].iloc[0] or 0

    ativo_circulante = caixa + total_estoque + total_contas_a_receber
    ativo_nao_circulante = total_bens
    total_ativo = ativo_circulante + ativo_nao_circulante

    total_contas_a_pagar = db.df_from_sql("SELECT SUM(valor) as total FROM contas_a_pagar")['total'].iloc[0] or 0
    capital_social = db.get_conta_geral("capital_social")
    total_passivo = total_contas_a_pagar
    patrimonio_liquido = capital_social + lucro_acumulado
    total_passivo_pl = total_passivo + patrimonio_liquido

    balanco = {
        "ativo": {
            "Caixa": caixa,
            "Estoque de Mercadorias": total_estoque,
            "Contas a Receber": total_contas_a_receber,
            "Bens (Imobilizado)": total_bens,
            "TOTAL ATIVO": total_ativo
        },
        "passivo_pl": {
            "Contas a Pagar": total_contas_a_pagar,
            "Capital Social": capital_social,
            "Lucros Acumulados": lucro_acumulado,
            "TOTAL PASSIVO + PL": total_passivo_pl
        }
    }

    return balanco

def exportar_balanco_excel(caminho="balanco_patrimonial.xlsx"):
    """Exporta o balanço patrimonial para um arquivo Excel com duas abas."""
    dados = calcular_balanco_patrimonial()
    ativo = dados["ativo"]
    passivo = dados["passivo_pl"]

    df_ativo = pd.DataFrame(ativo.items(), columns=["Descrição", "Valor"])
    df_passivo = pd.DataFrame(passivo.items(), columns=["Descrição", "Valor"])

    with pd.ExcelWriter(caminho) as writer:
        df_ativo.to_excel(writer, sheet_name="Ativo", index=False)
        df_passivo.to_excel(writer, sheet_name="Passivo+PL", index=False)

def relatorio_contas():
    """Une contas a pagar e a receber em um único DataFrame."""
    query = """
        SELECT origem AS descricao, valor, 'Pagar' AS tipo, NULL AS data_vencimento
        FROM contas_a_pagar
        UNION ALL
        SELECT origem AS descricao, valor, 'Receber' AS tipo, NULL AS data_vencimento
        FROM contas_a_receber
        ORDER BY tipo
    """
    return db.df_from_sql(query)
