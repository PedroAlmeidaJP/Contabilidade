📊 Sistema de Gestão Contábil e Operacional
Bem-vindo ao Sistema de Gestão Contábil, um projeto completo desenvolvido em Python com Streamlit para a disciplina de Contabilidade Aplicada à Informática.

Este sistema simula o ambiente operacional e financeiro de uma loja de hardware e software, integrando funcionalidades de vendas, controle de stock e relatórios contábeis essenciais como o Balanço Patrimonial e a DRE.

✅ Funcionalidades Principais
O sistema está dividido em módulos claros e intuitivos, acessíveis através de um menu de navegação lateral:

🏠 Dashboard Principal: Uma visão geral da saúde financeira da empresa com os principais indicadores (KPIs) como Faturamento, Lucro, número de Clientes e Produtos.

🛍️ Loja Virtual: Uma interface de e-commerce onde os clientes podem visualizar produtos com stock disponível e realizar compras (à vista ou a prazo).

📈 Relatórios Contábeis: O coração financeiro do sistema, onde é possível visualizar:

Balanço Patrimonial (BP): Demonstra a posição de Ativos, Passivos e Património Líquido da empresa.

Demonstração do Resultado do Exercício (DRE): Detalha as receitas, custos, impostos (ICMS) e o lucro final.

Exportação para Excel: Todos os relatórios contábeis podem ser exportados com um clique.

📊 Relatórios Operacionais: Análises detalhadas do dia a dia da operação, com filtros avançados:

Relatório de Vendas: Filtre por período, marca ou forma de pagamento.

Relatório de Clientes: Veja o histórico de compras e o valor gasto por cada cliente.

Relatório de Inventário: Análise do stock atual e o seu valor a preço de custo.

⚙️ Painel de Administração: A área de gestão onde o utilizador pode:

Realizar aportes de Capital Social.

Comprar Bens para o património da empresa (ex: veículos, computadores de escritório).

Gerir Fornecedores, Clientes e Produtos (com controle de stock e origem Nacional/Importado).

Dar Entrada de Estoque para produtos já existentes.

🖥️ Tecnologias Utilizadas
Linguagem: Python 3.11+

Interface Web: Streamlit

Manipulação de Dados: Pandas

Base de Dados: SQLite3 (embutido, não requer instalação)

Exportação: OpenPyXL

⚙️ Como Executar o Projeto
Para executar este projeto na sua máquina local, siga os passos abaixo.

1. Clonar o Repositório
Abra o seu terminal e clone este repositório:

git clone https://github.com/PedroAlmeidaJP/Contabilidade.git
cd Contabilidade

2. (Recomendado) Criar um Ambiente Virtual
Isto isola as dependências do projeto.

macOS / Linux:

python3 -m venv .venv
source .venv/bin/activate

Windows:

python -m venv .venv
.venv\Scripts\activate

3. Instalar as Dependências
Este comando irá instalar todas as bibliotecas necessárias que estão listadas no ficheiro requirements.txt.

pip install -r requirements.txt

4. (Opcional) Popular a Base de Dados com Dados de Exemplo
Para iniciar o sistema com dados realistas (clientes, produtos, vendas), execute o script seed.py uma vez.

python3 seed.py

5. Executar a Aplicação
Este é o comando final para ligar o servidor e abrir o sistema no seu navegador.

streamlit run Dashboard.py

O sistema estará acessível em http://localhost:8501.

