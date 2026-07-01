# Data Warehouse Comercial: Oracle DW + Lakehouse Bronze

## 1. Visão Geral

Este projeto tem como objetivo construir uma base analítica de dados comerciais com foco em Engenharia de Dados, modelagem dimensional, controle de cargas, rastreabilidade e preparação para arquitetura Lakehouse.

A proposta é simular um ambiente corporativo de varejo, contemplando processos de negócio como vendas, estoque, ruptura de estoque, metas comerciais, clientes, produtos, fornecedores, lojas, canais de venda, promoções e sazonalidades.

O projeto está sendo desenvolvido de forma incremental, com commits por etapa, para manter rastreabilidade cronológica da evolução técnica.

---

## 2. Objetivo do Projeto

Construir uma solução de dados com alta aplicabilidade em Engenharia de Dados, demonstrando:

- Modelagem dimensional em Oracle.
- Criação de dimensões e fatos.
- Definição de constraints, primary keys e foreign keys.
- Criação de índices para consultas analíticas.
- Documentação técnica do modelo.
- Definição de regras de negócio.
- Definição de decisões arquiteturais.
- Estratégia incremental de carga.
- Criação de notebooks PySpark para ingestão Bronze.
- Preparação para evolução em camadas Bronze, Silver e Gold.

---

## 3. Stack Técnica

- Oracle Database
- SQL
- PL/SQL, em etapa futura
- PySpark
- Microsoft Fabric Lakehouse
- Delta Lake
- Parquet
- GitHub
- Markdown para documentação técnica

---

## 4. Arquitetura Atual

A arquitetura atual contempla a criação de um Data Warehouse relacional no Oracle e preparação da ingestão para a camada Bronze em Lakehouse.

```text
Oracle DW
    |
    |-- Tabelas dimensão
    |-- Tabelas fato
    |-- Tabelas técnicas de controle e log
    |
Arquivos Parquet no OneLake
    |
    |-- /Files/raw/oracle_dw/<nome_tabela>
    |
Microsoft Fabric Lakehouse
    |
    |-- bronze.<tabela>
    |
Próximas etapas
    |
    |-- Silver: limpeza, tipagem, qualidade, deduplicação
    |-- Gold: modelo analítico e KPIs
```

---

## 5. Status Atual do Projeto

Até o momento, foram concluídas as seguintes etapas:

- Definição do tema do projeto.
- Desenho do modelo dimensional.
- Criação das tabelas dimensão no schema `dw`.
- Criação das tabelas fato no schema `dw`.
- Criação das tabelas técnicas de controle e log.
- Criação de índices para as tabelas fato.
- Validação conceitual das dimensões, fatos e índices.
- Criação da documentação técnica inicial.
- Criação dos notebooks de ingestão Bronze via Parquet.

O projeto ainda não possui carga populada nas tabelas dimensionais e fatos. A próxima etapa será gerar ou carregar massa de dados fictícia para simular um cenário real de processamento.

---

## 6. Modelo Dimensional

## 6.1. Dimensões

As dimensões criadas no schema `dw` são:

```text
dw.DIM_CATEGORIA
dw.DIM_CLIENTE
dw.DIM_PRODUTO
dw.DIM_FORNECEDOR
dw.DIM_FORMAPAGTO
dw.DIM_MARCA
dw.DIM_PROMOCAO
dw.DIM_PRODUTORUPTURA
dw.DIM_SAZONALIDADE
dw.DIM_TEMPO
dw.DIM_LOJA
dw.DIM_CANALVENDA
```

## 6.2. Fatos

As tabelas fato criadas são:

```text
dw.FATO_VENDAS
dw.FATO_ESTOQUE
dw.FATO_RUPTURA_ESTOQUE
dw.FATO_METAS
```

## 6.3. Tabelas Técnicas

As tabelas técnicas criadas são:

```text
dw.CONTROLE_CARGA
dw.LOG_EXECUCAO
```

Essas tabelas foram criadas para armazenar informações de auditoria, status de carga, volumetria, watermarks, erros e logs das execuções.

---

## 7. Grão das Tabelas Fato

## 7.1. dw.FATO_VENDAS

Grão: uma linha por item de venda.

Essa fato armazenará eventos comerciais de venda, contendo métricas como quantidade, valor bruto, desconto, valor líquido, custo total e margem bruta.

## 7.2. dw.FATO_ESTOQUE

Grão: uma linha por produto, loja e data de referência.

Essa fato representará a posição de estoque, contendo estoque disponível, reservado, bloqueado, em trânsito, estoque mínimo, estoque máximo, ponto de reposição, valor de estoque e flags operacionais.

## 7.3. dw.FATO_RUPTURA_ESTOQUE

Grão: uma linha por evento de ruptura de produto, loja e data.

Essa fato armazenará eventos de ruptura de estoque, permitindo análise de venda perdida, motivo da ruptura, dias em ruptura e quantidade em ruptura.

## 7.4. dw.FATO_METAS

Grão: uma linha por período, loja, canal, produto, categoria, marca e tipo de meta.

Essa fato armazenará metas comerciais de faturamento, volume, margem e ticket médio, viabilizando análise de meta versus realizado.

---

## 8. Principais Relacionamentos

## 8.1. Relacionamentos da Dimensão Produto

```text
dw.DIM_PRODUTO.SK_CATEGORIA  -> dw.DIM_CATEGORIA.SK_CATEGORIA
dw.DIM_PRODUTO.SK_MARCA      -> dw.DIM_MARCA.SK_MARCA
dw.DIM_PRODUTO.SK_FORNECEDOR -> dw.DIM_FORNECEDOR.SK_FORNECEDOR
```

## 8.2. Relacionamentos da FATO_VENDAS

```text
dw.FATO_VENDAS.SK_TEMPO       -> dw.DIM_TEMPO.SK_TEMPO
dw.FATO_VENDAS.SK_CLIENTE     -> dw.DIM_CLIENTE.SK_CLIENTE
dw.FATO_VENDAS.SK_PRODUTO     -> dw.DIM_PRODUTO.SK_PRODUTO
dw.FATO_VENDAS.SK_CATEGORIA   -> dw.DIM_CATEGORIA.SK_CATEGORIA
dw.FATO_VENDAS.SK_MARCA       -> dw.DIM_MARCA.SK_MARCA
dw.FATO_VENDAS.SK_FORNECEDOR  -> dw.DIM_FORNECEDOR.SK_FORNECEDOR
dw.FATO_VENDAS.SK_FORMAPAGTO  -> dw.DIM_FORMAPAGTO.SK_FORMAPAGTO
dw.FATO_VENDAS.SK_PROMOCAO    -> dw.DIM_PROMOCAO.SK_PROMOCAO
dw.FATO_VENDAS.SK_LOJA        -> dw.DIM_LOJA.SK_LOJA
dw.FATO_VENDAS.SK_CANALVENDA  -> dw.DIM_CANALVENDA.SK_CANALVENDA
```

## 8.3. Relacionamentos da FATO_ESTOQUE

```text
dw.FATO_ESTOQUE.SK_TEMPO      -> dw.DIM_TEMPO.SK_TEMPO
dw.FATO_ESTOQUE.SK_PRODUTO    -> dw.DIM_PRODUTO.SK_PRODUTO
dw.FATO_ESTOQUE.SK_LOJA       -> dw.DIM_LOJA.SK_LOJA
dw.FATO_ESTOQUE.SK_CATEGORIA  -> dw.DIM_CATEGORIA.SK_CATEGORIA
dw.FATO_ESTOQUE.SK_MARCA      -> dw.DIM_MARCA.SK_MARCA
dw.FATO_ESTOQUE.SK_FORNECEDOR -> dw.DIM_FORNECEDOR.SK_FORNECEDOR
```

## 8.4. Relacionamentos da FATO_RUPTURA_ESTOQUE

```text
dw.FATO_RUPTURA_ESTOQUE.SK_TEMPO          -> dw.DIM_TEMPO.SK_TEMPO
dw.FATO_RUPTURA_ESTOQUE.SK_PRODUTO        -> dw.DIM_PRODUTO.SK_PRODUTO
dw.FATO_RUPTURA_ESTOQUE.SK_LOJA           -> dw.DIM_LOJA.SK_LOJA
dw.FATO_RUPTURA_ESTOQUE.SK_MOTIVO_RUPTURA -> dw.DIM_PRODUTORUPTURA.SK_PRODUTORUPTURA
```

## 8.5. Relacionamentos da FATO_METAS

```text
dw.FATO_METAS.SK_TEMPO      -> dw.DIM_TEMPO.SK_TEMPO
dw.FATO_METAS.SK_LOJA       -> dw.DIM_LOJA.SK_LOJA
dw.FATO_METAS.SK_CANALVENDA -> dw.DIM_CANALVENDA.SK_CANALVENDA
dw.FATO_METAS.SK_PRODUTO    -> dw.DIM_PRODUTO.SK_PRODUTO
dw.FATO_METAS.SK_CATEGORIA  -> dw.DIM_CATEGORIA.SK_CATEGORIA
dw.FATO_METAS.SK_MARCA      -> dw.DIM_MARCA.SK_MARCA
```

---

## 9. Estratégia de Ingestão Bronze

A ingestão Bronze foi planejada para utilizar arquivos Parquet como origem.

Premissa de origem:

```text
/Files/raw/oracle_dw/<nome_tabela>
```

Exemplos:

```text
/Files/raw/oracle_dw/dim_produto
/Files/raw/oracle_dw/fato_vendas
/Files/raw/oracle_dw/fato_estoque
```

Destino esperado no Lakehouse:

```text
bronze.dim_produto
bronze.fato_vendas
bronze.fato_estoque
```

A camada Bronze deve preservar os dados com baixa transformação. As etapas de padronização, deduplicação, validação de regras de negócio e resolução de chaves serão tratadas posteriormente na camada Silver.

---

## 10. Metadados Técnicos da Bronze

Os notebooks de ingestão adicionam os seguintes metadados técnicos:

```text
bronze_data_ingestao
bronze_id_execucao
bronze_tabela_origem
bronze_origem
bronze_tipo_carga
bronze_formato_origem
bronze_caminho_origem
```

Esses campos permitem rastrear a origem, o momento da ingestão, o tipo de carga e o identificador da execução.

---

## 11. Notebooks Criados

Os notebooks criados para a ingestão Bronze via Parquet são:

```text
notebooks/
├── 00_config_bronze_parquet.py
├── 01_ingestao_bronze_parquet_para_delta.py
├── 02_ingestao_bronze_parquet_parametrizada.py
└── 03_validacao_bronze_parquet.py
```

## 11.1. 00_config_bronze_parquet.py

Centraliza parâmetros, caminho raw, schema Bronze, formato de arquivo, listas de dimensões, fatos e tabelas técnicas.

## 11.2. 01_ingestao_bronze_parquet_para_delta.py

Executa a ingestão em lote de todas as tabelas Parquet para Delta na camada Bronze.

## 11.3. 02_ingestao_bronze_parquet_parametrizada.py

Executa a ingestão de uma única tabela por vez, recebendo parâmetros do pipeline.

Esse notebook é recomendado para uso em orquestração com loop `ForEach` no Microsoft Fabric.

## 11.4. 03_validacao_bronze_parquet.py

Valida se as tabelas Bronze foram criadas, se possuem linhas e se contêm os metadados técnicos esperados.

---

## 12. Pipeline Bronze Planejado

O pipeline Bronze pode ser executado de duas formas.

## 12.1. Execução em lote

```text
1. Executar 00_config_bronze_parquet.py
2. Executar 01_ingestao_bronze_parquet_para_delta.py
3. Executar 03_validacao_bronze_parquet.py
```

## 12.2. Execução parametrizada

```text
1. Definir lista de tabelas
2. Executar ForEach sobre a lista
3. Para cada item, executar 02_ingestao_bronze_parquet_parametrizada.py
4. Ao final, executar 03_validacao_bronze_parquet.py
```

A execução parametrizada é a abordagem recomendada para um pipeline mais próximo de ambiente produtivo.

---

## 13. Documentação Criada

A documentação técnica criada até o momento está planejada para a pasta `docs/`.

```text
docs/
├── dicionario_de_dados.md
├── regras_de_negocio.md
├── decisoes_arquiteturais.md
└── estrategia_incremental.md
```

## 13.1. dicionario_de_dados.md

Documenta as tabelas, colunas, tipos de dados, chaves, obrigatoriedade, descrições e regras associadas.

## 13.2. regras_de_negocio.md

Documenta as regras funcionais e técnicas para dimensões, fatos, tabelas técnicas, qualidade de dados e indicadores analíticos.

## 13.3. decisoes_arquiteturais.md

Documenta o racional das principais decisões técnicas adotadas no projeto.

## 13.4. estrategia_incremental.md

Documenta a estratégia de carga full, incremental, watermark, merge, SCD Tipo 2, reprocessamento, auditoria e validação pós-carga.

---

## 14. Estrutura Recomendada do Repositório

```text
fabric-retail-dw-lakehouse/
│
├── README.md
│
├── sql/
│   ├── 01_create_dimensions.sql
│   ├── 02_create_facts.sql
│   ├── 03_create_control_log_tables.sql
│   ├── 04_create_indexes.sql
│   └── 05_comments.sql
│
├── notebooks/
│   ├── bronze/
│   │   ├── 00_config_bronze_parquet.py
│   │   ├── 01_ingestao_bronze_parquet_para_delta.py
│   │   ├── 02_ingestao_bronze_parquet_parametrizada.py
│   │   └── 03_validacao_bronze_parquet.py
│   │
│   ├── silver/
│   └── gold/
│
├── pipelines/
│   └── pipeline_bronze_parquet_orquestracao.md
│
├── docs/
│   ├── dicionario_de_dados.md
│   ├── regras_de_negocio.md
│   ├── decisoes_arquiteturais.md
│   └── estrategia_incremental.md
│
├── data/
│   └── sample/
│
└── assets/
    └── architecture/
```

---

## 15. Decisões Técnicas Já Tomadas

- Uso de modelagem dimensional.
- Uso do schema `dw` para o Data Warehouse relacional.
- Uso de surrogate keys com prefixo `SK_`.
- Preservação das chaves de origem com padrão `ID_..._ORIGEM`.
- Uso de SCD Tipo 2 em produto e cliente.
- Criação de fatos separadas para vendas, estoque, ruptura e metas.
- Criação de tabelas técnicas para controle e log.
- Uso de índices nas principais chaves analíticas das fatos.
- Adoção de Parquet como formato intermediário para ingestão Bronze.
- Gravação da Bronze em Delta Lake.
- Separação entre documentação, SQL, notebooks e pipelines.

---

## 16. Próximas Etapas

As próximas etapas planejadas são:

```text
1. Organizar os arquivos gerados na estrutura do repositório.
2. Criar massa de dados fictícia em Parquet.
3. Executar ingestão Bronze no Lakehouse.
4. Criar notebooks Silver para limpeza, tipagem e deduplicação.
5. Implementar tratamento SCD Tipo 2 em DIM_PRODUTO e DIM_CLIENTE.
6. Criar camada Gold com KPIs comerciais.
7. Criar consultas analíticas SQL.
8. Criar dashboard ou evidências visuais para apresentação.
9. Publicar resumo técnico no LinkedIn.
```

---

## 17. Indicadores Planejados

O modelo permitirá construir indicadores como:

- Faturamento bruto.
- Faturamento líquido.
- Desconto total.
- Quantidade de vendas.
- Quantidade de itens vendidos.
- Ticket médio.
- Margem bruta.
- Percentual de margem.
- Estoque disponível.
- Valor de estoque a custo.
- Produtos em ruptura.
- Venda perdida estimada por ruptura.
- Meta versus realizado.
- Percentual de atingimento de meta.

---

## 18. Histórico Cronológico do Projeto

## Etapa 1: Ideação

Definição do tema do projeto: Data Warehouse Comercial com Oracle, PySpark, Microsoft Fabric e arquitetura Lakehouse.

## Etapa 2: Modelagem Dimensional

Definição das dimensões, fatos, relacionamentos, chaves primárias, chaves estrangeiras e constraints.

## Etapa 3: Índices

Criação dos índices para melhorar consultas analíticas em vendas, estoque, ruptura e metas.

## Etapa 4: Tabelas Técnicas

Criação das tabelas `CONTROLE_CARGA` e `LOG_EXECUCAO` para rastreabilidade, observabilidade e controle de execução.

## Etapa 5: Documentação

Criação dos documentos técnicos:

```text
dicionario_de_dados.md
regras_de_negocio.md
decisoes_arquiteturais.md
estrategia_incremental.md
```

## Etapa 6: Ingestão Bronze

Criação dos notebooks de ingestão Bronze usando arquivos Parquet como origem e Delta Lake como destino.

---

## 19. Como Executar Futuramente

## 19.1. Preparar os dados raw

Disponibilizar os arquivos Parquet no caminho:

```text
/Files/raw/oracle_dw/<nome_tabela>
```

## 19.2. Executar ingestão Bronze

Executar o notebook em lote:

```text
01_ingestao_bronze_parquet_para_delta.py
```

Ou executar a versão parametrizada por tabela:

```text
02_ingestao_bronze_parquet_parametrizada.py
```

## 19.3. Validar Bronze

Executar:

```text
03_validacao_bronze_parquet.py
```

## 19.4. Conferir logs

Consultar:

```text
bronze.log_ingestao_bronze
bronze.validacao_bronze
```

---

## 20. Observações

Este projeto ainda está em desenvolvimento.

A etapa atual tem foco em estruturação, documentação, modelagem e preparação da ingestão Bronze. As cargas com dados e as camadas Silver e Gold serão desenvolvidas nas próximas fases.

---

## 21. Autor

Bruno Adonis Rocha Santos

Perfil: Engenheiro de Dados | PySpark + SQL | Microsoft Fabric + PL/SQL | Metodologias Ágeis
