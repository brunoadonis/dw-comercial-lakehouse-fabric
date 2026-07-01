# Notebook: 00_config_bronze_parquet
# Objetivo: centralizar parametros da ingestao Bronze a partir de arquivos Parquet no Microsoft Fabric Lakehouse.

from pyspark.sql import functions as F
from datetime import datetime
import uuid

# Configuracoes gerais
LAKEHOUSE_NAME = "GC_Lakehouse"
BRONZE_SCHEMA = "bronze"
RAW_BASE_PATH = "/Files/raw/oracle_dw"
FILE_FORMAT = "parquet"

# Controle de execucao
ID_EXECUCAO = str(uuid.uuid4())
DATA_EXECUCAO_UTC = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# Dimensoes
DIM_TABLES = [
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
    "DIM_CANALVENDA"
]

# Fatos
FACT_TABLES = [
    "FATO_VENDAS",
    "FATO_ESTOQUE",
    "FATO_RUPTURA_ESTOQUE",
    "FATO_METAS"
]

# Tabelas tecnicas
TECH_TABLES = [
    "CONTROLE_CARGA",
    "LOG_EXECUCAO"
]

ALL_TABLES = DIM_TABLES + FACT_TABLES + TECH_TABLES

print(f"ID_EXECUCAO: {ID_EXECUCAO}")
print(f"DATA_EXECUCAO_UTC: {DATA_EXECUCAO_UTC}")
print(f"RAW_BASE_PATH: {RAW_BASE_PATH}")
print(f"FILE_FORMAT: {FILE_FORMAT}")
print(f"Total de tabelas configuradas: {len(ALL_TABLES)}")
