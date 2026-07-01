# Notebook: 00_config_gold
# Objetivo: centralizar parametros da camada Gold para modelos semanticos de BI.

SILVER_SCHEMA = "silver"
GOLD_SCHEMA = "gold"

# Tabelas Silver de origem
SILVER_DIMS = {
    "tempo": f"{SILVER_SCHEMA}.dim_tempo",
    "cliente": f"{SILVER_SCHEMA}.dim_cliente",
    "produto": f"{SILVER_SCHEMA}.dim_produto",
    "categoria": f"{SILVER_SCHEMA}.dim_categoria",
    "marca": f"{SILVER_SCHEMA}.dim_marca",
    "fornecedor": f"{SILVER_SCHEMA}.dim_fornecedor",
    "forma_pagto": f"{SILVER_SCHEMA}.dim_formapagto",
    "promocao": f"{SILVER_SCHEMA}.dim_promocao",
    "loja": f"{SILVER_SCHEMA}.dim_loja",
    "canal_venda": f"{SILVER_SCHEMA}.dim_canalvenda",
    "motivo_ruptura": f"{SILVER_SCHEMA}.dim_produtoruptura"
}

SILVER_FACTS = {
    "vendas": f"{SILVER_SCHEMA}.fato_vendas",
    "estoque": f"{SILVER_SCHEMA}.fato_estoque",
    "ruptura": f"{SILVER_SCHEMA}.fato_ruptura_estoque",
    "metas": f"{SILVER_SCHEMA}.fato_metas"
}

# Tabelas Gold finais
GOLD_TABLES = {
    "dim_tempo": f"{GOLD_SCHEMA}.dim_tempo",
    "dim_cliente": f"{GOLD_SCHEMA}.dim_cliente",
    "dim_produto": f"{GOLD_SCHEMA}.dim_produto",
    "dim_loja": f"{GOLD_SCHEMA}.dim_loja",
    "dim_canal_venda": f"{GOLD_SCHEMA}.dim_canal_venda",
    "dim_forma_pagamento": f"{GOLD_SCHEMA}.dim_forma_pagamento",
    "dim_promocao": f"{GOLD_SCHEMA}.dim_promocao",
    "dim_motivo_ruptura": f"{GOLD_SCHEMA}.dim_motivo_ruptura",
    "fato_vendas": f"{GOLD_SCHEMA}.fato_vendas",
    "fato_estoque": f"{GOLD_SCHEMA}.fato_estoque",
    "fato_ruptura_estoque": f"{GOLD_SCHEMA}.fato_ruptura_estoque",
    "fato_metas": f"{GOLD_SCHEMA}.fato_metas",
    "kpi_vendas_mensal": f"{GOLD_SCHEMA}.kpi_vendas_mensal",
    "kpi_meta_vs_realizado": f"{GOLD_SCHEMA}.kpi_meta_vs_realizado",
    "kpi_estoque_atual": f"{GOLD_SCHEMA}.kpi_estoque_atual",
    "kpi_ruptura_mensal": f"{GOLD_SCHEMA}.kpi_ruptura_mensal",
    "mart_resumo_executivo": f"{GOLD_SCHEMA}.mart_resumo_executivo"
}

spark.sql(f"CREATE DATABASE IF NOT EXISTS {GOLD_SCHEMA}") # type: ignore

print(f"SILVER_SCHEMA: {SILVER_SCHEMA}")
print(f"GOLD_SCHEMA: {GOLD_SCHEMA}")
print(f"Total de tabelas Gold planejadas: {len(GOLD_TABLES)}")
