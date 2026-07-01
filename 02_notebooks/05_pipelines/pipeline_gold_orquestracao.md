# Pipeline Gold - Orquestração

## Objetivo

Construir a camada Gold do projeto, aplicando decisões de inteligência de negócios para consumo em modelos semânticos e dashboards de BI.

A Gold utiliza as tabelas Silver como origem e gera:

- dimensões conformadas;
- fatos modeladas para análise;
- KPIs comerciais;
- análises de estoque;
- análises de ruptura;
- meta versus realizado;
- mart executivo consolidado.

## Notebooks

```text
00_config_gold.py
01_gold_dimensoes_conformadas.py
02_gold_fatos_modeladas.py
03_gold_kpis_comerciais.py
04_gold_mart_resumo_executivo.py
05_validacao_gold.py
06_gold_consultas_bi_exemplos.sql
```

## Fluxo recomendado

```text
1. Executar 00_config_gold.py
2. Executar 01_gold_dimensoes_conformadas.py
3. Executar 02_gold_fatos_modeladas.py
4. Executar 03_gold_kpis_comerciais.py
5. Executar 04_gold_mart_resumo_executivo.py
6. Executar 05_validacao_gold.py
```

## Principais saídas Gold

```text
gold.dim_tempo
gold.dim_cliente
gold.dim_produto
gold.dim_loja
gold.dim_canal_venda
gold.dim_forma_pagamento
gold.dim_promocao
gold.dim_motivo_ruptura

gold.fato_vendas
gold.fato_estoque
gold.fato_ruptura_estoque
gold.fato_metas

gold.kpi_vendas_mensal
gold.kpi_meta_vs_realizado
gold.kpi_estoque_atual
gold.kpi_ruptura_mensal
gold.mart_resumo_executivo
```

## Ideia de modelo semântico no Power BI

Modelo recomendado:

```text
Dimensões:
- dim_tempo
- dim_cliente
- dim_produto
- dim_loja
- dim_canal_venda
- dim_forma_pagamento
- dim_promocao
- dim_motivo_ruptura

Fatos:
- fato_vendas
- fato_estoque
- fato_ruptura_estoque
- fato_metas

Marts/KPIs:
- kpi_vendas_mensal
- kpi_meta_vs_realizado
- kpi_estoque_atual
- kpi_ruptura_mensal
- mart_resumo_executivo
```

## Páginas sugeridas no dashboard

1. Visão Executiva
   - faturamento líquido;
   - margem bruta;
   - ticket médio;
   - meta versus realizado;
   - venda perdida por ruptura.

2. Vendas
   - vendas por mês;
   - vendas por loja;
   - vendas por categoria;
   - vendas por canal;
   - top produtos.

3. Estoque
   - estoque atual;
   - estoque baixo;
   - excesso de estoque;
   - valor parado em estoque.

4. Ruptura
   - ruptura por loja;
   - ruptura por categoria;
   - motivo de ruptura;
   - venda perdida estimada.

5. Metas
   - percentual de atingimento;
   - lojas acima e abaixo da meta;
   - meta por canal e categoria.
