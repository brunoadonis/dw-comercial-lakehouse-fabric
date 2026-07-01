# Data Flow

## Projeto: DW Comercial Lakehouse com Microsoft Fabric

## 1. Objetivo

Este documento descreve o fluxo de dados do projeto **DW Comercial Lakehouse com Microsoft Fabric**, desde a geração/entrada dos dados fictícios até a preparação das camadas Bronze, Silver e Gold para consumo analítico em ferramentas de BI.

O objetivo é documentar, de forma cronológica e arquitetural, como os dados percorrem o pipeline de dados do projeto, quais transformações são aplicadas em cada camada e quais artefatos são gerados ao longo do processo.

---

## 2. Visão Geral do Fluxo

O projeto segue uma arquitetura em camadas, inspirada no padrão Medallion Architecture:

```text
Data Sample CSV
        ↓
Raw Files / Parquet
        ↓
Bronze Delta Tables
        ↓
Silver Delta Tables
        ↓
Gold Delta Tables
        ↓
Modelo Semântico / Power BI
```

Cada camada possui uma responsabilidade específica:

```text
Raw     -> Armazenamento inicial dos arquivos de entrada
Bronze  -> Ingestão dos dados com baixa transformação
Silver  -> Padronização, tipagem e qualidade básica
Gold    -> Modelagem analítica e regras de negócio para BI
BI      -> Consumo por dashboards, relatórios e modelo semântico
```

---

## 3. Origem dos Dados

A origem inicial do projeto são arquivos CSV fictícios gerados para simular um ambiente comercial de varejo.

Os arquivos estão planejados para armazenamento no repositório em:

```text
data/sample/csv/
```

Exemplos de arquivos:

```text
dim_categoria.csv
dim_marca.csv
dim_fornecedor.csv
dim_produto.csv
dim_cliente.csv
dim_formapagto.csv
dim_promocao.csv
dim_sazonalidade.csv
dim_tempo.csv
dim_produtoruptura.csv
dim_loja.csv
dim_canalvenda.csv
fato_vendas.csv
fato_estoque.csv
fato_ruptura_estoque.csv
fato_metas.csv
controle_carga.csv
log_execucao.csv
```

Os arquivos CSV utilizam:

```text
Separador: ;
Encoding: UTF-8 com BOM
Datas: YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS
Valores decimais: ponto decimal
```

---

## 4. Conversão para Raw Parquet

Antes da ingestão para a camada Bronze, os arquivos CSV podem ser convertidos para Parquet e disponibilizados na área raw do Lakehouse.

Caminho esperado no OneLake:

```text
/Files/raw/oracle_dw/<nome_tabela>
```

Exemplos:

```text
/Files/raw/oracle_dw/dim_produto
/Files/raw/oracle_dw/fato_vendas
/Files/raw/oracle_dw/fato_estoque
```

A camada raw tem como objetivo armazenar os dados recebidos em um formato otimizado para leitura, sem aplicação de regras de negócio.

---

## 5. Camada Bronze

## 5.1. Objetivo da Bronze

A camada Bronze representa a primeira camada estruturada do Lakehouse.

Ela recebe os dados originados dos arquivos Parquet e grava as tabelas em formato Delta, mantendo os dados próximos ao formato de origem.

A Bronze deve aplicar apenas transformações mínimas, como:

- leitura dos arquivos Parquet;
- inclusão de metadados técnicos;
- gravação em Delta Table;
- controle básico da ingestão.

## 5.2. Origem da Bronze

```text
/Files/raw/oracle_dw/<nome_tabela>
```

## 5.3. Destino da Bronze

```text
bronze.<nome_tabela>
```

Exemplos:

```text
bronze.dim_produto
bronze.dim_cliente
bronze.fato_vendas
bronze.fato_estoque
```

## 5.4. Metadados Técnicos da Bronze

Durante a ingestão Bronze, são adicionadas colunas técnicas para rastreabilidade:

```text
bronze_data_ingestao
bronze_id_execucao
bronze_tabela_origem
bronze_origem
bronze_tipo_carga
bronze_formato_origem
bronze_caminho_origem
```

Essas colunas permitem identificar:

- quando o dado foi ingerido;
- qual execução realizou a ingestão;
- qual tabela originou o dado;
- qual caminho físico foi utilizado;
- qual formato de arquivo foi utilizado;
- qual tipo de carga foi executado.

## 5.5. Notebooks da Bronze

Os notebooks responsáveis pela Bronze são:

```text
notebooks/bronze/00_config_bronze_parquet.py
notebooks/bronze/01_ingestao_bronze_parquet_para_delta.py
notebooks/bronze/02_ingestao_bronze_parquet_parametrizada.py
notebooks/bronze/03_validacao_bronze_parquet.py
```

## 5.6. Fluxo da Bronze

```text
1. Ler arquivos Parquet da área raw
2. Adicionar metadados técnicos
3. Gravar dados como Delta Table no schema bronze
4. Registrar log de ingestão
5. Validar existência e volumetria das tabelas
```

---

## 6. Camada Silver

## 6.1. Objetivo da Silver

A camada Silver representa a etapa de padronização e preparação técnica dos dados.

Ela consome os dados da camada raw/Parquet ou Bronze, aplica tratamentos simples e grava as tabelas em formato Delta no schema `silver`.

A Silver não deve aplicar regras analíticas complexas. Seu objetivo é entregar dados limpos, tipados e minimamente confiáveis para a camada Gold.

## 6.2. Tratamentos Aplicados na Silver

Os principais tratamentos da camada Silver são:

- padronização dos nomes das colunas;
- aplicação de trim em campos texto;
- conversão de strings vazias para nulo;
- normalização de valores numéricos com vírgula e ponto;
- aplicação de schema explícito por tabela;
- conversão de tipos de dados;
- remoção de registros com nulos em colunas obrigatórias;
- remoção de duplicados por chave definida;
- inclusão de metadados de processamento;
- gravação em Delta Table.

## 6.3. Exemplo de Padronização Numérica

A Silver deve tratar valores numéricos que possam chegar em formatos diferentes:

```text
1.234,56 -> 1234.56
1234,56  -> 1234.56
1234.56  -> 1234.56
```

Esse tratamento garante que campos monetários e quantitativos sejam armazenados corretamente como tipos numéricos.

## 6.4. Destino da Silver

```text
silver.<nome_tabela>
```

Exemplos:

```text
silver.dim_produto
silver.dim_cliente
silver.fato_vendas
silver.fato_estoque
silver.fato_metas
```

## 6.5. Metadados Técnicos da Silver

A camada Silver adiciona os seguintes metadados:

```text
silver_data_processamento
silver_tabela_origem
silver_camada_origem
```

## 6.6. Notebooks da Silver

Os notebooks responsáveis pela Silver são:

```text
notebooks/silver/00_config_silver.py
notebooks/silver/01_utils_silver.py
notebooks/silver/02_silver_dimensoes.py
notebooks/silver/03_silver_fatos.py
notebooks/silver/04_silver_parametrizada.py
notebooks/silver/05_validacao_silver.py
```

## 6.7. Fluxo da Silver

```text
1. Ler dados Parquet da área raw
2. Padronizar nomes de colunas
3. Limpar campos texto
4. Converter strings vazias para nulo
5. Normalizar campos numéricos
6. Aplicar schema explícito
7. Remover nulos obrigatórios
8. Remover duplicados
9. Adicionar metadados Silver
10. Gravar Delta Table no schema silver
11. Gerar log de qualidade
12. Validar tabelas Silver
```

---

## 7. Camada Gold

## 7.1. Objetivo da Gold

A camada Gold representa a camada de negócio do projeto.

Ela consome as tabelas Silver e aplica decisões de inteligência de negócios para construção de modelos semânticos e dashboards em BI.

É na Gold que são criadas:

- dimensões conformadas;
- fatos analíticas;
- tabelas de KPI;
- marts executivos;
- estruturas prontas para consumo pelo Power BI.

## 7.2. Transformações Aplicadas na Gold

A camada Gold aplica transformações como:

- enriquecimento da dimensão produto com categoria, marca e fornecedor;
- renome semântico da dimensão de ruptura para motivo de ruptura;
- cálculo de indicadores de vendas;
- cálculo de margem e percentual de margem;
- cálculo de percentual de desconto;
- classificação de status de estoque;
- consolidação mensal de vendas;
- cálculo de meta versus realizado;
- consolidação de ruptura e venda perdida;
- criação do mart executivo mensal.

## 7.3. Tabelas Gold de Dimensão

```text
gold.dim_tempo
gold.dim_cliente
gold.dim_produto
gold.dim_loja
gold.dim_canal_venda
gold.dim_forma_pagamento
gold.dim_promocao
gold.dim_motivo_ruptura
```

## 7.4. Tabelas Gold de Fato

```text
gold.fato_vendas
gold.fato_estoque
gold.fato_ruptura_estoque
gold.fato_metas
```

## 7.5. Tabelas Gold de KPI e Marts

```text
gold.kpi_vendas_mensal
gold.kpi_meta_vs_realizado
gold.kpi_estoque_atual
gold.kpi_ruptura_mensal
gold.mart_resumo_executivo
```

## 7.6. Notebooks da Gold

Os notebooks responsáveis pela Gold são:

```text
notebooks/gold/00_config_gold.py
notebooks/gold/01_gold_dimensoes_conformadas.py
notebooks/gold/02_gold_fatos_modeladas.py
notebooks/gold/03_gold_kpis_comerciais.py
notebooks/gold/04_gold_mart_resumo_executivo.py
notebooks/gold/05_validacao_gold.py
```

Também foi criado um arquivo SQL com consultas de exemplo:

```text
sql/06_gold_consultas_bi_exemplos.sql
```

## 7.7. Fluxo da Gold

```text
1. Ler tabelas Silver
2. Criar dimensões conformadas
3. Criar fatos analíticas
4. Calcular indicadores comerciais
5. Calcular meta versus realizado
6. Calcular indicadores de estoque atual
7. Calcular indicadores de ruptura
8. Criar mart resumo executivo
9. Validar tabelas Gold
```

---

## 8. Modelo Semântico para BI

A camada Gold foi desenhada para permitir a construção de um modelo semântico no Power BI ou ferramenta equivalente.

## 8.1. Dimensões Recomendadas

```text
dim_tempo
dim_cliente
dim_produto
dim_loja
dim_canal_venda
dim_forma_pagamento
dim_promocao
dim_motivo_ruptura
```

## 8.2. Fatos Recomendadas

```text
fato_vendas
fato_estoque
fato_ruptura_estoque
fato_metas
```

## 8.3. Tabelas Agregadas para Consumo Direto

```text
kpi_vendas_mensal
kpi_meta_vs_realizado
kpi_estoque_atual
kpi_ruptura_mensal
mart_resumo_executivo
```

Essas tabelas podem ser usadas diretamente em páginas executivas ou como base para medidas DAX.

---

## 9. Indicadores Disponíveis

A camada Gold disponibiliza indicadores como:

```text
Faturamento bruto
Faturamento líquido
Valor de desconto
Percentual de desconto
Custo total
Margem bruta
Percentual de margem
Quantidade de vendas
Quantidade de itens vendidos
Quantidade de clientes distintos
Ticket médio
Meta de faturamento
Realizado de faturamento
Desvio da meta
Percentual de atingimento da meta
Status da meta
Estoque disponível
Estoque total
Valor de estoque a custo
Valor de estoque a venda
Dias de cobertura de estoque
Giro de estoque
Indicador de ruptura
Indicador de estoque baixo
Indicador de excesso de estoque
Quantidade de eventos de ruptura
Quantidade em ruptura
Dias em ruptura
Valor de venda perdida
```

---

## 10. Páginas Sugeridas para Dashboard

## 10.1. Visão Executiva

Objetivo: acompanhar a saúde geral do negócio.

Indicadores sugeridos:

```text
Faturamento líquido
Margem bruta
Percentual de margem
Ticket médio
Quantidade de vendas
Percentual de atingimento da meta
Venda perdida por ruptura
```

Tabelas sugeridas:

```text
gold.mart_resumo_executivo
gold.kpi_vendas_mensal
gold.kpi_meta_vs_realizado
```

## 10.2. Vendas

Objetivo: analisar desempenho comercial.

Indicadores sugeridos:

```text
Faturamento por mês
Faturamento por loja
Faturamento por categoria
Faturamento por canal
Top produtos
Ticket médio
Margem por categoria
```

Tabelas sugeridas:

```text
gold.fato_vendas
gold.kpi_vendas_mensal
gold.dim_produto
gold.dim_loja
gold.dim_tempo
gold.dim_canal_venda
```

## 10.3. Estoque

Objetivo: acompanhar disponibilidade e risco operacional.

Indicadores sugeridos:

```text
Estoque disponível
Estoque baixo
Excesso de estoque
Produtos em ruptura
Valor parado em estoque
Dias de cobertura
```

Tabelas sugeridas:

```text
gold.fato_estoque
gold.kpi_estoque_atual
gold.dim_produto
gold.dim_loja
```

## 10.4. Ruptura

Objetivo: analisar impacto da falta de estoque.

Indicadores sugeridos:

```text
Eventos de ruptura
Venda perdida estimada
Dias em ruptura
Ruptura por categoria
Ruptura por loja
Motivo da ruptura
```

Tabelas sugeridas:

```text
gold.fato_ruptura_estoque
gold.kpi_ruptura_mensal
gold.dim_motivo_ruptura
gold.dim_produto
gold.dim_loja
```

## 10.5. Metas

Objetivo: comparar planejamento comercial com realizado.

Indicadores sugeridos:

```text
Meta de faturamento
Faturamento realizado
Desvio da meta
Percentual de atingimento
Status da meta
Atingimento por loja
Atingimento por canal
Atingimento por categoria
```

Tabelas sugeridas:

```text
gold.fato_metas
gold.kpi_meta_vs_realizado
gold.dim_loja
gold.dim_canal_venda
gold.dim_produto
gold.dim_tempo
```

---

## 11. Ordem Geral de Execução do Projeto

A ordem geral recomendada do fluxo de dados é:

```text
1. Disponibilizar CSVs fictícios em data/sample/csv
2. Converter CSVs para Parquet na área raw do Lakehouse
3. Executar notebooks Bronze
4. Executar validação Bronze
5. Executar notebooks Silver
6. Executar validação Silver
7. Executar notebooks Gold
8. Executar validação Gold
9. Conectar Power BI às tabelas Gold
10. Criar modelo semântico e dashboards
```

---

## 12. Fluxo Detalhado por Camada

```text
data/sample/csv
    ↓
/Files/raw/oracle_dw
    ↓
bronze.<tabela>
    ↓
silver.<tabela>
    ↓
gold.dim_*
gold.fato_*
gold.kpi_*
gold.mart_*
    ↓
Power BI / Modelo Semântico
```

---

## 13. Responsabilidades por Camada

| Camada | Responsabilidade |
|---|---|
| CSV Sample | Massa fictícia versionada no GitHub |
| Raw Parquet | Arquivos otimizados no OneLake |
| Bronze | Ingestão com baixa transformação e rastreabilidade |
| Silver | Padronização, tipagem, deduplicação e qualidade simples |
| Gold | Regras de negócio, KPIs e modelo analítico |
| BI | Visualização, modelo semântico e análise executiva |

---

## 14. Observações

A camada Gold foi propositalmente desenhada para aproximar o projeto de um ambiente real de BI.

A Silver não concentra regras analíticas complexas. Ela apenas prepara os dados para que a Gold aplique as decisões de negócio.

O modelo final pode evoluir com:

```text
views semânticas
medidas DAX
modelo estrela no Power BI
agregações adicionais
particionamento por período
testes de qualidade de dados
monitoramento de pipelines
```

---

## 15. Resumo

O fluxo de dados deste projeto demonstra uma jornada completa de Engenharia de Dados:

```text
Arquivo fictício versionado
    → armazenamento raw
    → ingestão Bronze
    → tratamento Silver
    → modelagem Gold
    → consumo em BI
```

Essa estrutura permite rastreabilidade, organização em camadas, evolução incremental e construção de indicadores comerciais relevantes para análise executiva.
