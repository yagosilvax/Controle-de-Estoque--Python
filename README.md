# Controle de Estoque - Python

Sistema robusto de gerenciamento e controle de estoque desenvolvido em **Python**, utilizando o banco de dados relacional **PostgreSQL** para persistência física dos dados. O projeto adota práticas recomendadas de segurança de infraestrutura, utilizando variáveis de ambiente para mascarar credenciais de acesso.

## Funcionalidades do Sistema:

O sistema disponibiliza um menu interativo via terminal com operações completas de manipulação de dados:

1. **Visualização Completa (`[1] - VER ESTOQUE`):** Consulta e renderização de todos os itens cadastrados.
2. **Inserção de Registros (`[2] - CADASTRAR PRODUTO`):** Captura automática da data/hora do sistema (`datetime`) e inserção de novos produtos.
3. **Exclusão Avançada (`[3] - REMOVER PRODUTO`):** Busca produtos por aproximação (`ILIKE`), exibe as opções e permite a exclusão segura filtrando pelo ID único.
4. **Busca Customizada (`[4] - BUSCAR PRODUTO`):** Filtro inteligente utilizando operadores coringa (`%`) para buscas parciais de texto de forma insensível a maiúsculas/minúsculas.
5. **Movimentação de Estoque (`[5] - REGISTRAR SAIDA`):** Atualização (`UPDATE`) da volumetria em estoque com validação de consistência (impede saídas maiores do que o saldo disponível).
6. **Módulo de Auditoria (`[7] - VERIFICAR STATUS`):** Análise preditiva que identifica automaticamente produtos em estado crítico (quantidade igual ou inferior a 5 unidades) necessitando de reposição.

## Tecnologias:

- **Linguagem Principal:** Python 3.x
- **Banco de Dados:** PostgreSQL (Gerenciado via schemas customizados)
- **Drivers de Conexão:** `psycopg2`
- **Segurança:** `python-dotenv` (Gerenciador de variáveis de ambiente)

---

## Configuração da Infraestrutura (PostgreSQL):

O script foi desenhado para atuar sob isolamento de escopo (Schema). Antes de executar o programa, crie a estrutura de tabelas executando o script SQL abaixo no seu banco de dados:

```sql
-- Criação do Schema isolado para o projeto
CREATE SCHEMA estoque;

-- Criação da tabela com constraints de integridade
CREATE TABLE estoque.produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    quantidade_estoque INT NOT NULL,
    preco_un NUMERIC(10, 2) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
