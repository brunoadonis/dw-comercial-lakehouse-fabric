# Notebook: 01_ingestao_bronze_parquet_para_delta
# Objetivo: ingerir arquivos Parquet da area raw para a camada Bronze em formato Delta.
# Contexto: os dados do Oracle DW devem estar previamente exportados para o OneLake em formato Parquet.

from pyspark.sql import functions as F
from datetime import datetime
import uuid

ID_EXECUCAO = str(uuid.uuid4())
BRONZE_SCHEMA = "bronze"
RAW_BASE_PATH = "/Files/raw/oracle_dw"
FILE_FORMAT = "parquet"
TIPO_CARGA = "FULL_INICIAL"
ORIGEM = "ORACLE_DW_PARQUET"

TABLES = [
    "DIM_CATEGORIA",
    "DIM_MARCA",
    "DIM_FORNECEDOR",
    "DIM_PRODUTO",
    "DIM_CLIENTE",
    "DIM_FORMAPAGTO",
    "DIM_PROMOCAO",
    "DIM_SAZONALIDADE",
    "DIM_TEMPO",
    "DIM_PRODUTORUPTURA",
    "DIM_LOJA",
    "DIM_CANALVENDA",
    "FATO_VENDAS",
    "FATO_ESTOQUE",
    "FATO_RUPTURA_ESTOQUE",
    "FATO_METAS",
    "CONTROLE_CARGA",
    "LOG_EXECUCAO"
]

spark.sql(f"CREATE DATABASE IF NOT EXISTS {BRONZE_SCHEMA}")


def get_source_path(table_name: str) -> str:
    return f"{RAW_BASE_PATH}/{table_name.lower()}"


def read_parquet_table(table_name: str):
    source_path = get_source_path(table_name)
    return spark.read.parquet(source_path)


def add_bronze_metadata(df, table_name: str):
    source_path = get_source_path(table_name)
    return (
        df
        .withColumn("bronze_data_ingestao", F.current_timestamp())
        .withColumn("bronze_id_execucao", F.lit(ID_EXECUCAO))
        .withColumn("bronze_tabela_origem", F.lit(table_name))
        .withColumn("bronze_origem", F.lit(ORIGEM))
        .withColumn("bronze_tipo_carga", F.lit(TIPO_CARGA))
        .withColumn("bronze_formato_origem", F.lit(FILE_FORMAT))
        .withColumn("bronze_caminho_origem", F.lit(source_path))
    )


def write_delta_table(df, table_name: str):
    target_table = f"{BRONZE_SCHEMA}.{table_name.lower()}"
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(target_table)
    )
    return target_table


summary = []

for table_name in TABLES:
    data_inicio = datetime.utcnow()
    try:
        print(f"Iniciando ingestao Parquet para Bronze: {table_name}")

        df_raw = read_parquet_table(table_name)
        qtd_linhas_lidas = df_raw.count()

        df_bronze = add_bronze_metadata(df_raw, table_name)
        target_table = write_delta_table(df_bronze, table_name)
        qtd_linhas_gravadas = spark.table(target_table).count()

        status = "SUCESSO"
        mensagem_erro = None

        print(f"Tabela gravada: {target_table} | Linhas: {qtd_linhas_gravadas}")

    except Exception as e:
        qtd_linhas_lidas = 0
        qtd_linhas_gravadas = 0
        status = "ERRO"
        mensagem_erro = str(e)
        print(f"Erro na ingestao da tabela {table_name}: {mensagem_erro}")

    data_fim = datetime.utcnow()
    summary.append((
        ID_EXECUCAO,
        table_name,
        status,
        qtd_linhas_lidas,
        qtd_linhas_gravadas,
        data_inicio,
        data_fim,
        mensagem_erro
    ))

summary_df = spark.createDataFrame(
    summary,
    [
        "id_execucao",
        "nome_tabela",
        "status",
        "qtd_linhas_lidas",
        "qtd_linhas_gravadas",
        "data_inicio",
        "data_fim",
        "mensagem_erro"
    ]
)

(
    summary_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(f"{BRONZE_SCHEMA}.log_ingestao_bronze")
)

print("Ingestao Bronze via Parquet finalizada")
