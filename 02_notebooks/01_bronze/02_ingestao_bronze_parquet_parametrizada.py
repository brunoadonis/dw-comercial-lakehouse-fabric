# Notebook: 02_ingestao_bronze_parquet_parametrizada
# Objetivo: ingerir uma unica tabela Parquet para Bronze Delta, recebendo parametros do Pipeline Fabric.
# Uso recomendado: chamar este notebook dentro de um ForEach no pipeline.

from pyspark.sql import functions as F
from datetime import datetime
import uuid

# Parametros default para execucao manual
try:
    table_name = dbutils.widgets.get("table_name")
except Exception:
    table_name = "DIM_PRODUTO"

try:
    raw_base_path = dbutils.widgets.get("raw_base_path")
except Exception:
    raw_base_path = "/Files/raw/oracle_dw"

try:
    bronze_schema = dbutils.widgets.get("bronze_schema")
except Exception:
    bronze_schema = "bronze"

try:
    tipo_carga = dbutils.widgets.get("tipo_carga")
except Exception:
    tipo_carga = "FULL_INICIAL"

try:
    id_execucao = dbutils.widgets.get("id_execucao")
except Exception:
    id_execucao = str(uuid.uuid4())

ORIGEM = "ORACLE_DW_PARQUET"
FILE_FORMAT = "parquet"

spark.sql(f"CREATE DATABASE IF NOT EXISTS {bronze_schema}")

source_path = f"{raw_base_path}/{table_name.lower()}"
target_table = f"{bronze_schema}.{table_name.lower()}"

data_inicio = datetime.utcnow()

try:
    df_raw = spark.read.parquet(source_path)
    qtd_linhas_lidas = df_raw.count()

    df_bronze = (
        df_raw
        .withColumn("bronze_data_ingestao", F.current_timestamp())
        .withColumn("bronze_id_execucao", F.lit(id_execucao))
        .withColumn("bronze_tabela_origem", F.lit(table_name))
        .withColumn("bronze_origem", F.lit(ORIGEM))
        .withColumn("bronze_tipo_carga", F.lit(tipo_carga))
        .withColumn("bronze_formato_origem", F.lit(FILE_FORMAT))
        .withColumn("bronze_caminho_origem", F.lit(source_path))
    )

    (
        df_bronze.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(target_table)
    )

    qtd_linhas_gravadas = spark.table(target_table).count()
    status = "SUCESSO"
    mensagem_erro = None

except Exception as e:
    qtd_linhas_lidas = 0
    qtd_linhas_gravadas = 0
    status = "ERRO"
    mensagem_erro = str(e)

data_fim = datetime.utcnow()

summary_df = spark.createDataFrame(
    [(
        id_execucao,
        table_name,
        status,
        qtd_linhas_lidas,
        qtd_linhas_gravadas,
        data_inicio,
        data_fim,
        mensagem_erro,
        source_path,
        target_table
    )],
    [
        "id_execucao",
        "nome_tabela",
        "status",
        "qtd_linhas_lidas",
        "qtd_linhas_gravadas",
        "data_inicio",
        "data_fim",
        "mensagem_erro",
        "source_path",
        "target_table"
    ]
)

(
    summary_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(f"{bronze_schema}.log_ingestao_bronze")
)

if status == "ERRO":
    raise Exception(f"Erro na ingestao Parquet da tabela {table_name}: {mensagem_erro}")

print(f"Tabela {target_table} carregada com sucesso. Linhas gravadas: {qtd_linhas_gravadas}")
