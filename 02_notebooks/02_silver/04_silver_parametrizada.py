# Notebook: 04_silver_parametrizada
# Objetivo: processar uma unica tabela para Silver, recebendo parametros do Pipeline Fabric.
# Recomendado para uso em ForEach.
# Premissa: executar/importar previamente 00_config_silver e 01_utils_silver.

from datetime import datetime

try:
    table_name = dbutils.widgets.get("table_name").lower()
except Exception:
    table_name = "dim_produto"

try:
    raw_base_path = dbutils.widgets.get("raw_base_path")
except Exception:
    raw_base_path = RAW_BASE_PATH

try:
    silver_schema = dbutils.widgets.get("silver_schema")
except Exception:
    silver_schema = SILVER_SCHEMA

spark.sql(f"CREATE DATABASE IF NOT EXISTS {silver_schema}")

if table_name not in SCHEMAS:
    raise ValueError(f"Tabela nao configurada na Silver: {table_name}")

try:
    quality_row = process_table(
        table_name=table_name,
        raw_base_path=raw_base_path,
        silver_schema=silver_schema,
        schema_map=SCHEMAS[table_name],
        required_cols=REQUIRED_COLUMNS.get(table_name, []),
        dedup_keys=DEDUP_KEYS.get(table_name, [])
    )
except Exception as e:
    quality_row = (table_name, 0, 0, 0, 0, "ERRO", str(e), datetime.utcnow())

quality_df = spark.createDataFrame(
    [quality_row],
    ["tabela", "qtd_raw", "qtd_pos_nulos_obrigatorios", "qtd_silver", "qtd_duplicados_removidos", "status", "mensagem", "data_processamento"]
)

(
    quality_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(f"{silver_schema}.log_qualidade_silver")
)

display(quality_df)

if quality_row[5] == "ERRO":
    raise Exception(quality_row[6])
