# Notebook: 05_validacao_gold
# Objetivo: validar existencia e volumetria das tabelas Gold.
# Premissa: executar previamente 00_config_gold.py.

from datetime import datetime

validation_rows = []

for logical_name, full_name in GOLD_TABLES.items():
    try:
        df = spark.table(full_name)
        qtd = df.count()
        status = "OK"
        msg = None
    except Exception as e:
        qtd = 0
        status = "ERRO"
        msg = str(e)

    validation_rows.append((logical_name, full_name, qtd, status, msg, datetime.utcnow()))

validation_df = spark.createDataFrame(
    validation_rows,
    ["tabela_logica", "tabela_fisica", "qtd_linhas", "status", "mensagem", "data_validacao"]
)

(
    validation_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{GOLD_SCHEMA}.validacao_gold")
)

display(validation_df.orderBy("status", "tabela_logica"))
