# Notebook: 02_gold_fatos_modeladas
# Objetivo: criar fatos Gold limpas e enriquecidas para modelo semantico.
# Premissa: executar previamente 00_config_gold.py e 01_gold_dimensoes_conformadas.py.

from pyspark.sql import functions as F

spark.sql(f"CREATE DATABASE IF NOT EXISTS {GOLD_SCHEMA}")

# FATO_VENDAS: fato analitica principal de vendas
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_TABLES['fato_vendas']} AS
SELECT
    v.SK_FATO_VENDA,
    v.ID_VENDA_ORIGEM,
    v.ID_ITEM_VENDA_ORIGEM,
    v.SK_TEMPO,
    v.SK_CLIENTE,
    v.SK_PRODUTO,
    v.SK_CATEGORIA,
    v.SK_MARCA,
    v.SK_FORNECEDOR,
    v.SK_FORMAPAGTO,
    v.SK_PROMOCAO,
    v.SK_LOJA,
    v.SK_CANALVENDA,
    v.QUANTIDADE,
    v.VALOR_UNITARIO,
    v.VALOR_BRUTO,
    v.VALOR_DESCONTO,
    v.VALOR_LIQUIDO,
    v.CUSTO_TOTAL,
    v.MARGEM_BRUTA,
    CASE
        WHEN v.VALOR_LIQUIDO > 0 THEN ROUND(v.MARGEM_BRUTA / v.VALOR_LIQUIDO * 100, 4)
        ELSE NULL
    END AS PERCENTUAL_MARGEM,
    CASE
        WHEN v.VALOR_BRUTO > 0 THEN ROUND(v.VALOR_DESCONTO / v.VALOR_BRUTO * 100, 4)
        ELSE NULL
    END AS PERCENTUAL_DESCONTO,
    v.DATA_HORA_VENDA,
    current_timestamp() AS gold_data_processamento
FROM {SILVER_FACTS['vendas']} v
""")

# FATO_ESTOQUE: snapshot de estoque para analises de disponibilidade
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_TABLES['fato_estoque']} AS
SELECT
    e.SK_FATO_ESTOQUE,
    e.ID_ESTOQUE_ORIGEM,
    e.SK_TEMPO,
    e.SK_PRODUTO,
    e.SK_LOJA,
    e.SK_CATEGORIA,
    e.SK_MARCA,
    e.SK_FORNECEDOR,
    e.QTD_ESTOQUE_DISPONIVEL,
    e.QTD_ESTOQUE_RESERVADO,
    e.QTD_ESTOQUE_BLOQUEADO,
    e.QTD_ESTOQUE_TRANSITO,
    e.QTD_ESTOQUE_TOTAL,
    e.QTD_ESTOQUE_MINIMO,
    e.QTD_ESTOQUE_MAXIMO,
    e.QTD_PONTO_REPOSICAO,
    e.CUSTO_UNITARIO,
    e.VALOR_ESTOQUE_CUSTO,
    e.VALOR_ESTOQUE_VENDA,
    e.DIAS_COBERTURA_ESTOQUE,
    e.GIRO_ESTOQUE,
    e.FL_RUPTURA,
    e.FL_ESTOQUE_BAIXO,
    e.FL_EXCESSO_ESTOQUE,
    CASE WHEN e.FL_RUPTURA = 'S' THEN 1 ELSE 0 END AS IND_RUPTURA,
    CASE WHEN e.FL_ESTOQUE_BAIXO = 'S' THEN 1 ELSE 0 END AS IND_ESTOQUE_BAIXO,
    CASE WHEN e.FL_EXCESSO_ESTOQUE = 'S' THEN 1 ELSE 0 END AS IND_EXCESSO_ESTOQUE,
    e.DATA_REFERENCIA_ESTOQUE,
    current_timestamp() AS gold_data_processamento
FROM {SILVER_FACTS['estoque']} e
""")

# FATO_RUPTURA_ESTOQUE: eventos de ruptura e venda perdida
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_TABLES['fato_ruptura_estoque']} AS
SELECT
    r.SK_FATO_RUPTURA,
    r.ID_RUPTURA_ORIGEM,
    r.SK_TEMPO,
    r.SK_PRODUTO,
    r.SK_LOJA,
    r.SK_MOTIVO_RUPTURA,
    r.QTD_ESTOQUE_ESPERADO,
    r.QTD_ESTOQUE_DISPONIVEL,
    r.QTD_RUPTURA,
    r.DIAS_RUPTURA,
    r.VALOR_VENDA_PERDIDA,
    r.FL_RUPTURA,
    CASE WHEN r.FL_RUPTURA = 'S' THEN 1 ELSE 0 END AS IND_RUPTURA,
    current_timestamp() AS gold_data_processamento
FROM {SILVER_FACTS['ruptura']} r
""")

# FATO_METAS: metas comerciais prontas para comparacao com vendas realizadas
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_TABLES['fato_metas']} AS
SELECT
    m.SK_FATO_META,
    m.ID_META_ORIGEM,
    m.SK_TEMPO,
    m.SK_LOJA,
    m.SK_CANALVENDA,
    m.SK_PRODUTO,
    m.SK_CATEGORIA,
    m.SK_MARCA,
    m.ANO,
    m.MES,
    m.ANO_MES,
    m.TIPO_META,
    m.META_FATURAMENTO_BRUTO,
    m.META_FATURAMENTO_LIQUIDO,
    m.META_QTD_VENDAS,
    m.META_QTD_ITENS,
    m.META_TICKET_MEDIO,
    m.META_MARGEM_BRUTA,
    m.META_PERCENTUAL_MARGEM,
    m.DATA_INICIO_META,
    m.DATA_FIM_META,
    m.FL_META_ATIVA,
    current_timestamp() AS gold_data_processamento
FROM {SILVER_FACTS['metas']} m
""")

print("Fatos Gold modeladas criadas com sucesso.")
