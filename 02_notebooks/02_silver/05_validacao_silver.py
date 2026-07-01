# Notebook: 05_validacao_silver
# Objetivo: validar volumetria e existencia das Delta Tables da camada Silver.
# Premissa: executar/importar previamente 00_config_silver.

from datetime import datetime

validation_rows = []

for table_name in ALL_TABLES:
    full_name = f"{SILVER_SCHEMA}.{table_name}"
    try:
        df = spark.table(full_name)
        qtd = df.count()
        cols = df.columns
        has_metadata = all(c in cols for c in ["silver_data_processamento", "silver_tabela_origem", "silver_camada_origem"])
        status = "OK" if has_metadata else "ALERTA_SEM_METADADOS"
        msg = None if has_metadata else "Tabela sem metadados Silver esperados"
    except Exception as e:
        qtd = 0
        has_metadata = False
        status = "ERRO"
        msg = str(e)

    validation_rows.append((table_name, full_name, qtd, has_metadata, status, msg, datetime.utcnow()))

validation_df = spark.createDataFrame(
    validation_rows,
    ["tabela", "nome_completo", "qtd_linhas", "possui_metadados_silver", "status", "mensagem", "data_validacao"]
)

(
    validation_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{SILVER_SCHEMA}.validacao_silver")
)

display(validation_df.orderBy("status", "tabela"))
