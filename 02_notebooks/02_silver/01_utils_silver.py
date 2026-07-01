# Notebook: 01_utils_silver
# Objetivo: funcoes reutilizaveis para ingestao e tratamento simples na camada Silver.

from pyspark.sql import functions as F
from pyspark.sql import DataFrame
from datetime import datetime
import re


def normalize_column_names(df: DataFrame) -> DataFrame:
    """Padroniza nomes de colunas para upper case, removendo espacos laterais."""
    for c in df.columns:
        df = df.withColumnRenamed(c, c.strip().upper())
    return df


def trim_string_columns(df: DataFrame) -> DataFrame:
    """Aplica trim e transforma strings vazias em null."""
    for c, t in df.dtypes:
        if t == "string":
            df = df.withColumn(c, F.trim(F.col(c)))
            df = df.withColumn(c, F.when(F.col(c) == "", F.lit(None)).otherwise(F.col(c)))
    return df


def normalize_decimal_string(col_name: str):
    """
    Normaliza valores numericos em string para padrao com ponto decimal.
    Trata formatos comuns:
    - 1.234,56 -> 1234.56
    - 1234,56  -> 1234.56
    - 1234.56  -> 1234.56
    """
    c = F.trim(F.col(col_name).cast("string"))
    has_comma = c.contains(",")
    has_dot = c.contains(".")
    return (
        F.when(has_comma & has_dot, F.regexp_replace(F.regexp_replace(c, "\\.", ""), ",", "."))
         .when(has_comma & (~has_dot), F.regexp_replace(c, ",", "."))
         .otherwise(c)
    )


def cast_columns(df: DataFrame, schema_map: dict) -> DataFrame:
    """Cria colunas ausentes como null e aplica tipagem explicita conforme schema_map."""
    for col_name, spark_type in schema_map.items():
        if col_name not in df.columns:
            df = df.withColumn(col_name, F.lit(None))

        type_lower = spark_type.lower()
        if type_lower.startswith("decimal"):
            df = df.withColumn(col_name, normalize_decimal_string(col_name).cast(spark_type))
        elif type_lower == "date":
            df = df.withColumn(col_name, F.to_date(F.col(col_name)))
        elif type_lower == "timestamp":
            df = df.withColumn(col_name, F.to_timestamp(F.col(col_name)))
        else:
            df = df.withColumn(col_name, F.col(col_name).cast(spark_type))

    # Mantem somente colunas previstas no schema, na ordem definida.
    return df.select([F.col(c) for c in schema_map.keys()])


def drop_required_nulls(df: DataFrame, required_cols: list) -> DataFrame:
    valid_cols = [c for c in required_cols if c in df.columns]
    if not valid_cols:
        return df
    return df.dropna(subset=valid_cols)


def deduplicate(df: DataFrame, keys: list) -> DataFrame:
    valid_keys = [c for c in keys if c in df.columns]
    if valid_keys:
        return df.dropDuplicates(valid_keys)
    return df.dropDuplicates()


def add_silver_metadata(df: DataFrame, table_name: str) -> DataFrame:
    return (
        df
        .withColumn("silver_data_processamento", F.current_timestamp())
        .withColumn("silver_tabela_origem", F.lit(table_name))
        .withColumn("silver_camada_origem", F.lit("raw_parquet"))
    )


def build_quality_row(table_name: str, raw_count: int, after_required_count: int, final_count: int, duplicate_count: int, status: str, msg: str = None):
    return (table_name, raw_count, after_required_count, final_count, duplicate_count, status, msg, datetime.utcnow())


def process_table(table_name: str, raw_base_path: str, silver_schema: str, schema_map: dict, required_cols: list, dedup_keys: list):
    source_path = f"{raw_base_path}/{table_name}"
    target_table = f"{silver_schema}.{table_name}"

    df_raw = spark.read.parquet(source_path)
    raw_count = df_raw.count()

    df = normalize_column_names(df_raw)
    df = trim_string_columns(df)
    df = cast_columns(df, schema_map)

    df_required = drop_required_nulls(df, required_cols)
    after_required_count = df_required.count()

    before_dedup_count = after_required_count
    df_final = deduplicate(df_required, dedup_keys)
    final_count = df_final.count()
    duplicate_count = before_dedup_count - final_count

    df_final = add_silver_metadata(df_final, table_name)

    (
        df_final.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(target_table)
    )

    return build_quality_row(table_name, raw_count, after_required_count, final_count, duplicate_count, "SUCESSO")
