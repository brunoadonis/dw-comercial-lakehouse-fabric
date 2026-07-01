# Pipeline Silver - Orquestração

## Objetivo

Processar os arquivos Parquet da área raw e gravar tabelas Delta na camada Silver.

A Silver deste projeto aplica tratamentos simples e controlados:

- padronização de nomes de colunas;
- trim em campos texto;
- transformação de string vazia para null;
- normalização de valores numéricos com `.` e `,`;
- tipagem explícita por tabela;
- descarte de registros com nulos em colunas obrigatórias;
- remoção de duplicados por chave definida;
- gravação em Delta Table no schema `silver`;
- geração de log de qualidade simples.

## Notebooks

```text
00_config_silver.py
01_utils_silver.py
02_silver_dimensoes.py
03_silver_fatos.py
04_silver_parametrizada.py
05_validacao_silver.py
```

## Fluxo simples

```text
1. Executar 00_config_silver.py
2. Executar 01_utils_silver.py
3. Executar 02_silver_dimensoes.py
4. Executar 03_silver_fatos.py
5. Executar 05_validacao_silver.py
```

## Fluxo recomendado em Pipeline Fabric

```text
1. Criar array com a lista de tabelas
2. Executar ForEach sobre a lista
3. Para cada tabela, chamar 04_silver_parametrizada.py
4. Ao final, executar 05_validacao_silver.py
```

## Origem esperada

```text
/Files/raw/oracle_dw/<nome_tabela>
```

Exemplo:

```text
/Files/raw/oracle_dw/dim_produto
/Files/raw/oracle_dw/fato_vendas
```

## Destino esperado

```text
silver.<nome_tabela>
```

Exemplo:

```text
silver.dim_produto
silver.fato_vendas
```

## Observação

A Silver não deve conter modelagem final de BI. A criação de fatos/dimensões analíticas finais, agregados, KPIs e regras de negócio mais elaboradas deve ficar para a camada Gold.
