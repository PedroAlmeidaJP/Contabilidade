# 📊 Sistema de Contabilidade com Streamlit

Este projeto é um sistema completo de **gestão contábil** desenvolvido em **Python** com **Streamlit**, ideal para controle financeiro e análise de patrimônio, produtos, clientes e fornecedores. Ele oferece uma interface moderna, com suporte a modo escuro e claro.

## ✅ Funcionalidades

- 💼 Painel de Administração com abas (Capital Social, Patrimônio, Fornecedores, etc)
- 🛒 Gestão de Estoque e Produtos
- 👤 Cadastro de Clientes e Fornecedores
- 📈 Relatórios Contábeis:
  - Demonstração do Resultado do Exercício (DRE)
  - Balanço Patrimonial
  - Contas a Pagar e Receber
- 💾 Banco de dados local (SQLite)
- 🌗 Alternância entre **modo escuro** e **modo claro**

---

## 🖥️ Tecnologias Utilizadas

- Python 3.11+
- Streamlit
- Pandas
- SQLite3
- XlsxWriter (para exportar relatórios)

---

## ⚙️ Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/PedroAlmeidaJP/Contabilidade.git
cd Contabilidade
2. (Opcional) Crie um ambiente virtual
bash
Copiar
Editar
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
3. Instale as dependências
bash
Copiar
Editar
pip install -r requirements.txt
4. Execute o sistema
bash
Copiar
Editar
streamlit run Dashboard.py
O sistema abrirá automaticamente no navegador:
🔗 http://localhost:8501

📁 Estrutura de Pastas
bash
Copiar
Editar
├── Dashboard.py                 # Tela principal com o resumo
├── logic.py                    # Funções de cálculo dos relatórios
├── database.py                 # Conexão e operações com o banco
├── gestor.db                   # Banco de dados SQLite
├── requirements.txt            # Lista de dependências
├── style.css                   # Estilos customizados (opcional)
├── /pages/
│   ├── Administracao.py
│   ├── Diagnostico.py
│   ├── Loja_Virtual.py
│   ├── Relatorios.py
│   └── Relatorios_Contabeis.py
