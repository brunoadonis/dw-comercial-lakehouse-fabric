# Notebook: 01_gold_dimensoes_conformadas
# Objetivo: criar dimensoes conformadas para consumo em BI.
# Premissa: executar previamente 00_config_gold.py.

from pyspark.sql import functions as F

spark.sql(f"CREATE DATABASE IF NOT EXISTS {GOLD_SCHEMA}")

# DIM_TEMPO: dimensao calendario padronizada para BI
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_TABLES['dim_tempo']} AS
SELECT
    SK_TEMPO,
    DATA_COMPLETA,
    DIA,
    MES,
    ANO,
    ANO_MES,
    NOME_MES,
    TRIMESTRE,
    SEMESTRE,
    NUM_DIA_SEMANA,
    NOME_DIA_SEMANA,
    FL_FIM_SEMANA,
    FL_FERIADO,
    NOME_FERIADO,
    current_timestamp() AS gold_data_processamento
FROM {SILVER_DIMS['tempo']}
""")

# DIM_CLIENTE: foco em segmentacao e localidade
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_TABLES['dim_cliente']} AS
SELECT
    SK_CLIENTE,
    ID_CLIENTE_ORIGEM,
    NOME_CLIENTE,
    TIPO_CLIENTE,
    SEXO,
    FAIXA_ETARIA,
    CIDADE,
    ESTADO,
    PAIS,
    SEGMENTO_CLIENTE,
    DATA_CADASTRO,
    FL_ATIVO,
    FL_REGISTRO_ATUAL,
    DATA_INICIO_VIGENCIA,
    DATA_FIM_VIGENCIA,
    current_timestamp() AS gold_data_processamento
FROM {SILVER_DIMS['cliente']}
""")

# DIM_PRODUTO: produto enriquecido com categoria, marca e fornecedor
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_TABLES['dim_produto']} AS
SELECT
    p.SK_PRODUTO,
    p.ID_PRODUTO_ORIGEM,
    p.NOME_PRODUTO,
    p.SKU,
    p.CODIGO_BARRAS,
    p.UNIDADE_MEDIDA,
    p.FL_PERECIVEL,
    p.FL_ATIVO,
    p.FL_REGISTRO_ATUAL,
    p.CUSTO_UNITARIO,
    p.PRECO_LISTA,
    p.DATA_INICIO_VIGENCIA,
    p.DATA_FIM_VIGENCIA,
    c.SK_CATEGORIA,
    c.NOME_CATEGORIA,
    c.NOME_DEPARTAMENTO,
    m.SK_MARCA,
    m.NOME_MARCA,
    m.FL_MARCA_PROPRIA,
    f.SK_FORNECEDOR,
    f.NOME_FORNECEDOR,
    f.TIPO_FORNECEDOR,
    f.CIDADE AS CIDADE_FORNECEDOR,
    f.ESTADO AS ESTADO_FORNECEDOR,
    current_timestamp() AS gold_data_processamento
FROM {SILVER_DIMS['produto']} p
LEFT JOIN {SILVER_DIMS['categoria']} c
    ON p.SK_CATEGORIA = c.SK_CATEGORIA
LEFT JOIN {SILVER_DIMS['marca']} m
    ON p.SK_MARCA = m.SK_MARCA
LEFT JOIN {SILVER_DIMS['fornecedor']} f
    ON p.SK_FORNECEDOR = f.SK_FORNECEDOR
""")

# DIM_LOJA: estrutura comercial e regional
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_TABLES['dim_loja']} AS
SELECT
    SK_LOJA,
    ID_LOJA_ORIGEM,
    NOME_LOJA,
    TIPO_LOJA,
    CIDADE,
    ESTADO,
    REGIONAL,
    PAIS,
    DATA_ABERTURA,
    FL_ATIVO,
    current_timestamp() AS gold_data_processamento
FROM {SILVER_DIMS['loja']}
""")

# DIM_CANAL_VENDA
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_TABLES['dim_canal_venda']} AS
SELECT
    SK_CANALVENDA,
    ID_CANALVENDA_ORIGEM,
    NOME_CANALVENDA,
    TIPO_CANAL,
    DESCRICAO_CANAL,
    FL_ATIVO,
    current_timestamp() AS gold_data_processamento
FROM {SILVER_DIMS['canal_venda']}
""")

# DIM_FORMA_PAGAMENTO
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_TABLES['dim_forma_pagamento']} AS
SELECT
    SK_FORMAPAGTO,
    ID_FORMAPAGTO_ORIGEM,
    DESCRICAO_FORMAPAGTO,
    TIPO_FORMAPAGTO,
    MODALIDADE,
    QTD_PARCELAS,
    FL_CREDITO,
    FL_ATIVO,
    current_timestamp() AS gold_data_processamento
FROM {SILVER_DIMS['forma_pagto']}
""")

# DIM_PROMOCAO
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_TABLES['dim_promocao']} AS
SELECT
    SK_PROMOCAO,
    ID_PROMOCAO_ORIGEM,
    NOME_PROMOCAO,
    TIPO_PROMOCAO,
    MECANICA_PROMOCAO,
    DATA_INICIO_PROMOCAO,
    DATA_FIM_PROMOCAO,
    PERCENTUAL_DESCONTO,
    VALOR_DESCONTO,
    FL_PROMOCAO_ATIVA,
    current_timestamp() AS gold_data_processamento
FROM {SILVER_DIMS['promocao']}
""")

# DIM_MOTIVO_RUPTURA: renome semantico para BI, mantendo origem DIM_PRODUTORUPTURA
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_TABLES['dim_motivo_ruptura']} AS
SELECT
    SK_PRODUTORUPTURA AS SK_MOTIVO_RUPTURA,
    ID_RUPTURA_ORIGEM,
    DESCRICAO_RUPTURA,
    TIPO_RUPTURA,
    RESPONSAVEL_RUPTURA,
    FL_ATIVO,
    current_timestamp() AS gold_data_processamento
FROM {SILVER_DIMS['motivo_ruptura']}
""")

print("Dimensões Gold conformadas criadas com sucesso.")
