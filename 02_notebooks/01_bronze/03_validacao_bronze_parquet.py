# Notebook: 03_validacao_bronze_parquet
# Objetivo: validar tabelas Bronze geradas a partir da ingestao Parquet.

BRONZE_SCHEMA = "bronze"

EXPECTED_TABLES = [
    "dim_categoria",
    "dim_marca",
    "dim_fornecedor",
    "dim_produto",
    "dim_cliente",
    "dim_formapagto",
    "dim_promocao",
    "dim_sazonalidade",
    "dim_tempo",
    "dim_produtoruptura",
    "dim_loja",
    "dim_canalvenda",
    "fato_vendas",
    "fato_estoque",
    "fato_ruptura_estoque",
    "fato_metas",
    "controle_carga",
    "log_execucao"
]

results = []

for table_name in EXPECTED_TABLES:
    full_name = f"{BRONZE_SCHEMA}.{table_name}"
    try:
        df = spark.table(full_name)
        columns = df.columns
        qtd_linhas = df.count()
        possui_metadados = all(
            col in columns
            for col in [
                "bronze_data_ingestao",
                "bronze_id_execucao",
                "bronze_origem",
                "bronze_formato_origem",
                "bronze_caminho_origem"
            ]
        )
        status = "OK" if possui_metadados else "ALERTA_SEM_METADADOS"
        mensagem = None if possui_metadados else "Tabela sem todas as colunas tecnicas esperadas da Bronze Parquet"
    except Exception as e:
        qtd_linhas = 0
        possui_metadados = False
        status = "ERRO"
        mensagem = str(e)

    results.append((full_name, status, qtd_linhas, possui_metadados, mensagem))

validation_df = spark.createDataFrame(
    results,
    ["tabela", "status", "qtd_linhas", "possui_metadados_bronze", "mensagem"]
)

display(validation_df.orderBy("status", "tabela"))

(
    validation_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{BRONZE_SCHEMA}.validacao_bronze")
)
