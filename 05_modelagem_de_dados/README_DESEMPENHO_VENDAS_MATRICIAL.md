# Desempenho de Vendas - Matricial

Relatório interativo em Python para análise comercial do projeto **DW Comercial Lakehouse com Microsoft Fabric**.

O objetivo é simular uma experiência parecida com um relatório Power BI, usando Python, Streamlit e Plotly.

## Local recomendado no projeto

```text
05_modelagem_de_dados/
├── desempenho_vendas_matricial.py
├── requirements_modelagem.txt
└── README_DESEMPENHO_VENDAS_MATRICIAL.md
```

## Entrada esperada

O relatório espera os arquivos CSV fictícios em:

```text
data/sample/csv/
```

Arquivos usados:

```text
fato_vendas.csv
fato_metas.csv
dim_tempo.csv
dim_produto.csv
dim_loja.csv
dim_canalvenda.csv
dim_categoria.csv
dim_marca.csv
dim_fornecedor.csv
```

## Principais análises

- visão executiva de faturamento, margem, ticket médio e meta;
- matriz loja x categoria;
- evolução mensal de faturamento e margem;
- top produtos;
- desempenho por categoria;
- meta versus realizado;
- base analítica filtrável e exportável.

## Como executar

Instale as dependências:

```bash
pip install -r requirements_modelagem.txt
```

Execute o relatório:

```bash
streamlit run desempenho_vendas_matricial.py
```

## Relação com a camada Gold

O relatório segue as decisões analíticas da Gold:

- produto conformado com categoria, marca e fornecedor;
- fato vendas enriquecida com margem e desconto;
- meta versus realizado por mês, loja, canal e categoria;
- visão matricial para análise comercial;
- uso de filtros dinâmicos para exploração de negócio.

## Nome do relatório

```text
Desempenho de Vendas - Matricial
```
