# Notebook: 00_config_silver
# Objetivo: centralizar configuracoes, schemas, chaves e regras simples para a camada Silver.

from pyspark.sql import types as T

RAW_BASE_PATH = "/Files/raw/oracle_dw"
SILVER_SCHEMA = "silver"
SOURCE_FORMAT = "parquet"

# Tabelas do projeto
DIM_TABLES = [
    "dim_categoria", "dim_marca", "dim_fornecedor", "dim_produto", "dim_cliente",
    "dim_formapagto", "dim_promocao", "dim_sazonalidade", "dim_tempo",
    "dim_produtoruptura", "dim_loja", "dim_canalvenda"
]

FACT_TABLES = [
    "fato_vendas", "fato_estoque", "fato_ruptura_estoque", "fato_metas"
]

TECH_TABLES = ["controle_carga", "log_execucao"]
ALL_TABLES = DIM_TABLES + FACT_TABLES + TECH_TABLES

# Tipos Spark por tabela. A Silver aplica tipagem explícita, mas mantém baixa transformação.
SCHEMAS = {
    "dim_categoria": {
        "SK_CATEGORIA": "long", "ID_CATEGORIA_ORIGEM": "string", "NOME_CATEGORIA": "string",
        "NOME_DEPARTAMENTO": "string", "FL_ATIVO": "string", "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "dim_marca": {
        "SK_MARCA": "long", "ID_MARCA_ORIGEM": "string", "NOME_MARCA": "string", "PAIS_ORIGEM": "string",
        "FL_MARCA_PROPRIA": "string", "FL_ATIVO": "string", "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "dim_fornecedor": {
        "SK_FORNECEDOR": "long", "ID_FORNECEDOR_ORIGEM": "string", "NOME_FORNECEDOR": "string", "CNPJ_FORNECEDOR": "string",
        "CIDADE": "string", "ESTADO": "string", "PAIS": "string", "TIPO_FORNECEDOR": "string", "FL_ATIVO": "string",
        "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "dim_produto": {
        "SK_PRODUTO": "long", "ID_PRODUTO_ORIGEM": "string", "SK_CATEGORIA": "long", "SK_MARCA": "long", "SK_FORNECEDOR": "long",
        "NOME_PRODUTO": "string", "DESCRICAO_PRODUTO": "string", "CODIGO_BARRAS": "string", "SKU": "string", "UNIDADE_MEDIDA": "string",
        "PESO_KG": "decimal(18,4)", "ALTURA_CM": "decimal(18,4)", "LARGURA_CM": "decimal(18,4)", "PROFUNDIDADE_CM": "decimal(18,4)",
        "CUSTO_UNITARIO": "decimal(18,2)", "PRECO_LISTA": "decimal(18,2)", "FL_PERECIVEL": "string", "FL_ATIVO": "string",
        "DATA_INICIO_VIGENCIA": "date", "DATA_FIM_VIGENCIA": "date", "FL_REGISTRO_ATUAL": "string",
        "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "dim_cliente": {
        "SK_CLIENTE": "long", "ID_CLIENTE_ORIGEM": "string", "NOME_CLIENTE": "string", "TIPO_CLIENTE": "string", "CPF_CNPJ": "string",
        "SEXO": "string", "FAIXA_ETARIA": "string", "DATA_NASCIMENTO": "date", "CIDADE": "string", "ESTADO": "string", "PAIS": "string",
        "SEGMENTO_CLIENTE": "string", "DATA_CADASTRO": "date", "DATA_INICIO_VIGENCIA": "date", "DATA_FIM_VIGENCIA": "date",
        "FL_REGISTRO_ATUAL": "string", "FL_ATIVO": "string", "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "dim_formapagto": {
        "SK_FORMAPAGTO": "long", "ID_FORMAPAGTO_ORIGEM": "string", "DESCRICAO_FORMAPAGTO": "string", "TIPO_FORMAPAGTO": "string",
        "MODALIDADE": "string", "QTD_PARCELAS": "int", "FL_CREDITO": "string", "FL_ATIVO": "string", "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "dim_promocao": {
        "SK_PROMOCAO": "long", "ID_PROMOCAO_ORIGEM": "string", "NOME_PROMOCAO": "string", "TIPO_PROMOCAO": "string", "MECANICA_PROMOCAO": "string",
        "DATA_INICIO_PROMOCAO": "date", "DATA_FIM_PROMOCAO": "date", "PERCENTUAL_DESCONTO": "decimal(9,4)", "VALOR_DESCONTO": "decimal(18,2)",
        "FL_PROMOCAO_ATIVA": "string", "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "dim_sazonalidade": {
        "SK_SAZONALIDADE": "long", "ID_SAZONALIDADE_ORIGEM": "string", "NOME_SAZONALIDADE": "string", "TIPO_SAZONALIDADE": "string",
        "DESCRICAO": "string", "DATA_INICIO": "date", "DATA_FIM": "date", "FL_RECORRENTE": "string", "FL_ATIVO": "string",
        "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "dim_tempo": {
        "SK_TEMPO": "long", "DATA_COMPLETA": "date", "DIA": "int", "MES": "int", "ANO": "int", "NOME_DIA_SEMANA": "string",
        "NUM_DIA_SEMANA": "int", "NOME_MES": "string", "ANO_MES": "string", "TRIMESTRE": "int", "SEMESTRE": "int",
        "FL_FIM_SEMANA": "string", "FL_FERIADO": "string", "NOME_FERIADO": "string", "DATA_CARGA": "timestamp"
    },
    "dim_produtoruptura": {
        "SK_PRODUTORUPTURA": "long", "ID_RUPTURA_ORIGEM": "string", "DESCRICAO_RUPTURA": "string", "TIPO_RUPTURA": "string",
        "RESPONSAVEL_RUPTURA": "string", "FL_ATIVO": "string", "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "dim_loja": {
        "SK_LOJA": "long", "ID_LOJA_ORIGEM": "string", "NOME_LOJA": "string", "CNPJ_LOJA": "string", "TIPO_LOJA": "string",
        "CIDADE": "string", "ESTADO": "string", "REGIONAL": "string", "PAIS": "string", "DATA_ABERTURA": "date", "FL_ATIVO": "string",
        "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "dim_canalvenda": {
        "SK_CANALVENDA": "long", "ID_CANALVENDA_ORIGEM": "string", "NOME_CANALVENDA": "string", "TIPO_CANAL": "string",
        "DESCRICAO_CANAL": "string", "FL_ATIVO": "string", "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "fato_vendas": {
        "SK_FATO_VENDA": "long", "ID_VENDA_ORIGEM": "string", "ID_ITEM_VENDA_ORIGEM": "string", "SK_TEMPO": "long", "SK_CLIENTE": "long",
        "SK_PRODUTO": "long", "SK_CATEGORIA": "long", "SK_MARCA": "long", "SK_FORNECEDOR": "long", "SK_FORMAPAGTO": "long", "SK_PROMOCAO": "long",
        "SK_LOJA": "long", "SK_CANALVENDA": "long", "QUANTIDADE": "decimal(18,4)", "VALOR_UNITARIO": "decimal(18,2)", "VALOR_BRUTO": "decimal(18,2)",
        "VALOR_DESCONTO": "decimal(18,2)", "VALOR_LIQUIDO": "decimal(18,2)", "CUSTO_TOTAL": "decimal(18,2)", "MARGEM_BRUTA": "decimal(18,2)",
        "DATA_HORA_VENDA": "timestamp", "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "fato_estoque": {
        "SK_FATO_ESTOQUE": "long", "ID_ESTOQUE_ORIGEM": "string", "SK_TEMPO": "long", "SK_PRODUTO": "long", "SK_LOJA": "long", "SK_CATEGORIA": "long",
        "SK_MARCA": "long", "SK_FORNECEDOR": "long", "QTD_ESTOQUE_DISPONIVEL": "decimal(18,4)", "QTD_ESTOQUE_RESERVADO": "decimal(18,4)",
        "QTD_ESTOQUE_BLOQUEADO": "decimal(18,4)", "QTD_ESTOQUE_TRANSITO": "decimal(18,4)", "QTD_ESTOQUE_TOTAL": "decimal(18,4)",
        "QTD_ESTOQUE_MINIMO": "decimal(18,4)", "QTD_ESTOQUE_MAXIMO": "decimal(18,4)", "QTD_PONTO_REPOSICAO": "decimal(18,4)",
        "CUSTO_UNITARIO": "decimal(18,2)", "VALOR_ESTOQUE_CUSTO": "decimal(18,2)", "VALOR_ESTOQUE_VENDA": "decimal(18,2)",
        "DIAS_COBERTURA_ESTOQUE": "decimal(10,2)", "GIRO_ESTOQUE": "decimal(10,4)", "FL_RUPTURA": "string", "FL_ESTOQUE_BAIXO": "string",
        "FL_EXCESSO_ESTOQUE": "string", "DATA_REFERENCIA_ESTOQUE": "date", "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "fato_ruptura_estoque": {
        "SK_FATO_RUPTURA": "long", "ID_RUPTURA_ORIGEM": "string", "SK_TEMPO": "long", "SK_PRODUTO": "long", "SK_LOJA": "long",
        "SK_MOTIVO_RUPTURA": "long", "QTD_ESTOQUE_ESPERADO": "decimal(18,4)", "QTD_ESTOQUE_DISPONIVEL": "decimal(18,4)",
        "QTD_RUPTURA": "decimal(18,4)", "DIAS_RUPTURA": "decimal(10,2)", "VALOR_VENDA_PERDIDA": "decimal(18,2)",
        "FL_RUPTURA": "string", "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    },
    "fato_metas": {
        "SK_FATO_META": "long", "ID_META_ORIGEM": "string", "SK_TEMPO": "long", "SK_LOJA": "long", "SK_CANALVENDA": "long", "SK_PRODUTO": "long",
        "SK_CATEGORIA": "long", "SK_MARCA": "long", "ANO": "int", "MES": "int", "ANO_MES": "string", "TIPO_META": "string",
        "META_FATURAMENTO_BRUTO": "decimal(18,2)", "META_FATURAMENTO_LIQUIDO": "decimal(18,2)", "META_QTD_VENDAS": "decimal(18,4)",
        "META_QTD_ITENS": "decimal(18,4)", "META_TICKET_MEDIO": "decimal(18,2)", "META_MARGEM_BRUTA": "decimal(18,2)",
        "META_PERCENTUAL_MARGEM": "decimal(9,4)", "DATA_INICIO_META": "date", "DATA_FIM_META": "date", "FL_META_ATIVA": "string",
        "DATA_CARGA": "timestamp", "DATA_ATUALIZACAO_DW": "timestamp"
    }
}

# Colunas obrigatorias para descarte de nulos na Silver.
REQUIRED_COLUMNS = {
    "dim_categoria": ["SK_CATEGORIA", "ID_CATEGORIA_ORIGEM", "NOME_CATEGORIA"],
    "dim_marca": ["SK_MARCA", "ID_MARCA_ORIGEM", "NOME_MARCA"],
    "dim_fornecedor": ["SK_FORNECEDOR", "ID_FORNECEDOR_ORIGEM", "NOME_FORNECEDOR"],
    "dim_produto": ["SK_PRODUTO", "ID_PRODUTO_ORIGEM", "SK_CATEGORIA", "NOME_PRODUTO"],
    "dim_cliente": ["SK_CLIENTE", "ID_CLIENTE_ORIGEM"],
    "dim_formapagto": ["SK_FORMAPAGTO", "ID_FORMAPAGTO_ORIGEM", "DESCRICAO_FORMAPAGTO"],
    "dim_promocao": ["SK_PROMOCAO", "ID_PROMOCAO_ORIGEM", "NOME_PROMOCAO"],
    "dim_sazonalidade": ["SK_SAZONALIDADE", "ID_SAZONALIDADE_ORIGEM", "NOME_SAZONALIDADE"],
    "dim_tempo": ["SK_TEMPO", "DATA_COMPLETA"],
    "dim_produtoruptura": ["SK_PRODUTORUPTURA", "ID_RUPTURA_ORIGEM", "DESCRICAO_RUPTURA"],
    "dim_loja": ["SK_LOJA", "ID_LOJA_ORIGEM", "NOME_LOJA"],
    "dim_canalvenda": ["SK_CANALVENDA", "ID_CANALVENDA_ORIGEM", "NOME_CANALVENDA"],
    "fato_vendas": ["SK_FATO_VENDA", "ID_VENDA_ORIGEM", "SK_TEMPO", "SK_PRODUTO"],
    "fato_estoque": ["SK_FATO_ESTOQUE", "SK_TEMPO", "SK_PRODUTO", "SK_LOJA"],
    "fato_ruptura_estoque": ["SK_FATO_RUPTURA", "SK_TEMPO", "SK_PRODUTO", "SK_LOJA"],
    "fato_metas": ["SK_FATO_META", "SK_TEMPO", "ANO", "MES", "ANO_MES", "TIPO_META"]
}

# Chaves de deduplicacao. A primeira tentativa usa o grao/chave natural; fallback usa todas as colunas.
DEDUP_KEYS = {
    "dim_categoria": ["SK_CATEGORIA"],
    "dim_marca": ["SK_MARCA"],
    "dim_fornecedor": ["SK_FORNECEDOR"],
    "dim_produto": ["SK_PRODUTO"],
    "dim_cliente": ["SK_CLIENTE"],
    "dim_formapagto": ["SK_FORMAPAGTO"],
    "dim_promocao": ["SK_PROMOCAO"],
    "dim_sazonalidade": ["SK_SAZONALIDADE"],
    "dim_tempo": ["SK_TEMPO"],
    "dim_produtoruptura": ["SK_PRODUTORUPTURA"],
    "dim_loja": ["SK_LOJA"],
    "dim_canalvenda": ["SK_CANALVENDA"],
    "fato_vendas": ["ID_VENDA_ORIGEM", "ID_ITEM_VENDA_ORIGEM"],
    "fato_estoque": ["SK_PRODUTO", "SK_LOJA", "SK_TEMPO"],
    "fato_ruptura_estoque": ["ID_RUPTURA_ORIGEM"],
    "fato_metas": ["ANO_MES", "SK_LOJA", "SK_CANALVENDA", "SK_PRODUTO", "SK_CATEGORIA", "SK_MARCA", "TIPO_META"]
}

print(f"SILVER_SCHEMA: {SILVER_SCHEMA}")
print(f"RAW_BASE_PATH: {RAW_BASE_PATH}")
print(f"Total de tabelas Silver configuradas: {len(ALL_TABLES)}")
