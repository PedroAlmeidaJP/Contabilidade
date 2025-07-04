# 📊 Sistema de Contabilidade com Streamlit

Este projeto é um sistema completo de **gestão contábil** desenvolvido em **Python** com **Streamlit**, ideal para controle financeiro, bens patrimoniais, contas a pagar e a receber, produtos, clientes e fornecedores. Possui interface moderna com suporte a modo **escuro** e **claro**, painel administrativo e relatórios contábeis prontos para exportação.

---

## ✅ Funcionalidades

- 💼 Painel de Administração com abas:
  - Capital Social
  - Bens (Patrimônio)
  - Fornecedores
  - Clientes
  - Produtos
  - Entrada de Estoque
- 📦 Cadastro de Produtos com valor e estoque
- 🛒 Registro de Vendas com cálculo de lucro e custo (CMV)
- 📈 Relatórios Contábeis:
  - DRE (Demonstração do Resultado do Exercício)
  - Balanço Patrimonial
  - Contas a Pagar e Receber
- 💾 Banco de dados local (SQLite)
- 📤 Exportação de relatórios para Excel

---

## 🖥️ Tecnologias Utilizadas

- Python 3.11+
- Streamlit
- Pandas
- SQLite3 (banco de dados leve e embutido)
- XlsxWriter (para exportar Excel)

---

## ⚙️ Como Executar o Projeto

### 🔁 Passo a passo para rodar em qualquer máquina:

#### 1. Clone o repositório

```bash
git clone https://github.com/PedroAlmeidaJP/Contabilidade.git
cd Contabilidade
2. (Opcional, mas recomendado) Crie um ambiente virtual
bash
Copiar
Editar
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
3. Instale as dependências do projeto
bash
Copiar
Editar
pip install -r requirements.txt
Isso vai instalar todos os pacotes usados, como streamlit, pandas, etc.

4. Execute a aplicação
bash
Copiar
Editar
streamlit run Dashboard.py
O sistema será aberto no navegador padrão em:
http://localhost:8501

📁 Estrutura de Pastas e Arquivos
bash
Copiar
Editar
Contabilidade/
├── Dashboard.py                 # Tela inicial com resumo e dashboard
├── logic.py                    # Regras de negócio e cálculos dos relatórios
├── database.py                 # Funções para interagir com o banco SQLite
├── gestor.db                   # Banco de dados local
├── requirements.txt            # Lista de bibliotecas usadas no projeto
├── style.css                   # Estilo visual customizado (modo dark/clear)
├── README.md                   # Este manual
├── /pages                      # Páginas do sistema (Streamlit multipage)
│   ├── Administracao.py
│   ├── Diagnostico.py
│   ├── Loja_Virtual.py
│   ├── Relatorios.py
│   └── Relatorios_Contabeis.py
📦 Exportação de Relatórios
Todos os relatórios podem ser exportados com um clique, no formato .xlsx. Isso inclui:

Demonstração do Resultado do Exercício (DRE)

Contas a Pagar e a Receber

Balanço Patrimonial completo

