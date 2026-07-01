# Pipeline Bronze Parquet - Orquestração

## Objetivo

Orquestrar a ingestão de arquivos Parquet da área raw do OneLake para a camada Bronze do Lakehouse.

## Premissa

Os dados do Oracle DW devem estar previamente exportados em formato Parquet no caminho:

```text
/Files/raw/oracle_dw/<nome_tabela>
```

Exemplo:

```text
/Files/raw/oracle_dw/dim_produto
/Files/raw/oracle_dw/fato_vendas
```

## Notebooks

1. `00_config_bronze_parquet.py`
   - Centraliza parâmetros, tabelas e configurações da ingestão Parquet.

2. `01_ingestao_bronze_parquet_para_delta.py`
   - Executa ingestão em lote de todas as tabelas Parquet para Delta Bronze.

3. `02_ingestao_bronze_parquet_parametrizada.py`
   - Executa ingestão de uma tabela por vez, recomendado para uso em ForEach no pipeline.

4. `03_validacao_bronze_parquet.py`
   - Valida existência, volumetria e metadados das tabelas Bronze.

## Fluxo simples

```text
1. Executar 00_config_bronze_parquet.py
2. Executar 01_ingestao_bronze_parquet_para_delta.py
3. Executar 03_validacao_bronze_parquet.py
```

## Fluxo recomendado com pipeline parametrizado

```text
1. Definir array de tabelas
2. Executar ForEach sobre a lista de tabelas
3. Para cada tabela, chamar 02_ingestao_bronze_parquet_parametrizada.py
4. Ao fim do loop, executar 03_validacao_bronze_parquet.py
```

## Lista de tabelas

```text
DIM_CATEGORIA
DIM_MARCA
DIM_FORNECEDOR
DIM_PRODUTO
DIM_CLIENTE
DIM_FORMAPAGTO
DIM_PROMOCAO
DIM_SAZONALIDADE
DIM_TEMPO
DIM_PRODUTORUPTURA
DIM_LOJA
DIM_CANALVENDA
FATO_VENDAS
FATO_ESTOQUE
FATO_RUPTURA_ESTOQUE
FATO_METAS
CONTROLE_CARGA
LOG_EXECUCAO
```

## Metadados técnicos adicionados na Bronze

```text
bronze_data_ingestao
bronze_id_execucao
bronze_tabela_origem
bronze_origem
bronze_tipo_carga
bronze_formato_origem
bronze_caminho_origem
```

## Observação

A camada Bronze deve preservar os dados com baixa transformação. Padronização, deduplicação, regras de qualidade, resolução de chaves e regras de negócio devem ficar para a camada Silver.
