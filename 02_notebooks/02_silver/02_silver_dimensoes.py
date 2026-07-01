# Notebook: 02_silver_dimensoes
# Objetivo: transformar os Parquets raw das dimensoes em Delta Tables na Silver.
# Premissa: executar/importar previamente 00_config_silver e 01_utils_silver.

from datetime import datetime

spark.sql(f"CREATE DATABASE IF NOT EXISTS {SILVER_SCHEMA}")

quality_rows = []

for table_name in DIM_TABLES:
    try:
        print(f"Processando Silver dimensão: {table_name}")
        row = process_table(
            table_name=table_name,
            raw_base_path=RAW_BASE_PATH,
            silver_schema=SILVER_SCHEMA,
            schema_map=SCHEMAS[table_name],
            required_cols=REQUIRED_COLUMNS.get(table_name, []),
            dedup_keys=DEDUP_KEYS.get(table_name, [])
        )
        quality_rows.append(row)
        print(f"OK: {table_name}")
    except Exception as e:
        print(f"ERRO: {table_name} -> {str(e)}")
        quality_rows.append((table_name, 0, 0, 0, 0, "ERRO", str(e), datetime.utcnow()))

quality_df = spark.createDataFrame(
    quality_rows,
    ["tabela", "qtd_raw", "qtd_pos_nulos_obrigatorios", "qtd_silver", "qtd_duplicados_removidos", "status", "mensagem", "data_processamento"]
)

(
    quality_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(f"{SILVER_SCHEMA}.log_qualidade_silver")
)

display(quality_df.orderBy("status", "tabela"))
