import database as db
import os
from datetime import date, timedelta

DB_FILE = "gestor.db"

def popular_dados():
    print("Iniciando o povoamento do banco de dados...")

    # --- Dados Iniciais ---
    fornecedores = [("TechData Distribuição", "12.345.678/0001-99", "São Paulo", "SP"),
                    ("Allied Tecnologia", "98.765.432/0001-11", "Rio de Janeiro", "RJ"),
                    ("Pichau Informática", "11.222.333/0001-44", "Joinville", "SC")]
    
    clientes = [("João da Silva", "123.456.789-00", "Santa Maria", "RS"),
                ("Maria Souza", "987.654.321-00", "Porto Alegre", "RS"),
                ("Inova Soluções TI", "55.444.333/0001-22", "Canoas", "RS"),
                ("Pedro Almeida", "111.222.333-44", "Santa Cruz do Sul", "RS")]
    
    produtos = [
        ("Processador Intel Core i7-13700K", "Intel", "Importado", 2100.00, 2899.99, 1, 10),
        ("Processador AMD Ryzen 7 7800X3D", "AMD", "Importado", 2350.00, 3199.90, 2, 8),
        ("Placa de Vídeo NVIDIA RTX 4070", "NVIDIA", "Importado", 3800.00, 4999.00, 1, 5),
        ("Placa de Vídeo AMD RX 7800 XT", "AMD", "Importado", 3200.00, 4199.90, 2, 7),
        ("Memória RAM Kingston Fury 16GB DDR5", "Kingston", "Nacional", 350.00, 549.90, 1, 30),
        ("SSD NVMe Samsung 980 Pro 1TB", "Samsung", "Nacional", 550.00, 899.00, 2, 25),
        ("Licença Windows 11 Pro", "Microsoft", "Nacional", 400.00, 849.90, 1, 50),
        ("Mouse Gamer Logitech G502 Hero", "Logitech", "Importado", 210.00, 349.90, 3, 40),
        ("Teclado Mecânico Redragon Kumara", "Redragon", "Nacional", 180.00, 299.00, 3, 35)
    ]

    for f in fornecedores:
        db.adicionar_fornecedor(*f)
    print(f"  - {len(fornecedores)} fornecedores adicionados.")

    for c in clientes:
        db.adicionar_cliente(*c)
    print(f"  - {len(clientes)} clientes adicionados.")

    for p in produtos:
        origem = p[2]
        if origem == "Nacional":
            icms_credito, icms_debito = p[3] * 0.12, p[4] * 0.18
        else:
            icms_credito, icms_debito = p[3] * 0.04, p[4] * 0.04
        db.adicionar_produto(p[0], p[1], p[2], p[3], p[4], icms_credito, icms_debito, p[5], p[6])
    print(f"  - {len(produtos)} produtos adicionados.")

    db.update_conta_geral("capital_social", 150000)
    db.update_conta_geral("caixa", 150000)
    print("  - Aporte de Capital Social de R$ 150.000,00 realizado.")

    db.adicionar_bem("Veículo de Entregas Fiat Fiorino", 85000)
    db.update_conta_geral("caixa", db.get_conta_geral("caixa") - 85000)
    print("  - Compra de Bem (Veículo) à vista realizada.")

    today = date.today()
    db.adicionar_venda(1, 1, 1, 2899.99, "À Vista", today - timedelta(days=10))
    db.adicionar_venda(3, 2, 1, 4999.00, "A Prazo", today - timedelta(days=5))
    db.adicionar_venda(8, 1, 2, 699.80, "À Vista", today - timedelta(days=2))
    db.adicionar_venda(7, 3, 10, 8499.00, "A Prazo", today)
    print("  - 4 vendas de exemplo adicionadas.")

    # --- Contas Contábeis (Pagar e Receber) ---
    db.executar_query("""
    CREATE TABLE IF NOT EXISTS contas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL CHECK(tipo IN ('A Pagar', 'A Receber')),
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        data_vencimento TEXT NOT NULL
    )
    """)
    
    db.executar_query("""
    INSERT INTO contas (tipo, descricao, valor, data_vencimento)
    VALUES (?, ?, ?, ?)
    """, ("A Pagar", "Compra de insumos", 1500.00, str(today + timedelta(days=5))))
    
    db.executar_query("""
    INSERT INTO contas (tipo, descricao, valor, data_vencimento)
    VALUES (?, ?, ?, ?)
    """, ("A Receber", "Venda parcelada", 2800.00, str(today + timedelta(days=3))))
    
    db.executar_query("""
    INSERT INTO contas (tipo, descricao, valor, data_vencimento)
    VALUES (?, ?, ?, ?)
    """, ("A Pagar", "Energia elétrica", 350.00, str(today + timedelta(days=2))))
    
    db.executar_query("""
    INSERT INTO contas (tipo, descricao, valor, data_vencimento)
    VALUES (?, ?, ?, ?)
    """, ("A Receber", "Contrato de serviço", 1200.00, str(today + timedelta(days=10))))
    
    print("  - Contas a pagar e a receber adicionadas.")

    print("\n✅ Povoamento concluído com sucesso!")

if __name__ == "__main__":
    if os.path.exists(DB_FILE):
        print(f"Apagando banco de dados antigo '{DB_FILE}' para um novo começo.")
        os.remove(DB_FILE)
    db.criar_tabelas()
    popular_dados()
