# Dicionário de Dados

## Projeto: Data Warehouse Comercial

## 1. Visão Geral

Este dicionário de dados documenta as tabelas dimensionais, tabelas fato e tabelas técnicas utilizadas no modelo dimensional do projeto de Data Warehouse Comercial.

O modelo foi construído no schema `dw` e contempla análises de vendas, estoque, ruptura, metas comerciais, clientes, produtos, fornecedores, lojas, canais de venda, promoções e sazonalidades.

## 2. Convenções de Nomenclatura

| Prefixo/Sufixo | Significado |
|---|---|
| SK_ | Surrogate Key, chave técnica gerada no Data Warehouse |
| ID_..._ORIGEM | Chave natural oriunda do sistema fonte |
| DIM_ | Tabela dimensão |
| FATO_ | Tabela fato |
| FL_ | Flag ou indicador lógico |
| DATA_CARGA | Data/hora em que o registro foi carregado no DW |
| DATA_ATUALIZACAO_DW | Data/hora da última atualização do registro no DW |
| DATA_INICIO_VIGENCIA | Data de início da validade histórica do registro |
| DATA_FIM_VIGENCIA | Data de fim da validade histórica do registro |
| FL_REGISTRO_ATUAL | Indica se o registro representa a versão atual |
| UK_ | Unique Key |
| PK_ | Primary Key |
| FK_ | Foreign Key |
| CK_ | Check Constraint |

---

# 3. Dimensões

## 3.1. dw.DIM_CATEGORIA

Tabela responsável por armazenar as categorias e departamentos dos produtos.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_CATEGORIA | NUMBER | PK | Sim | Chave técnica da categoria no DW. | Gerada automaticamente por identity. |
| ID_CATEGORIA_ORIGEM | VARCHAR2(50) | UK | Sim | Identificador da categoria no sistema de origem. | Deve ser único. |
| NOME_CATEGORIA | VARCHAR2(150) | Não | Sim | Nome da categoria do produto. | Deve estar preenchido. |
| NOME_DEPARTAMENTO | VARCHAR2(150) | Não | Não | Nome do departamento ao qual a categoria pertence. | Preenchimento opcional. |
| FL_ATIVO | CHAR(1) | Não | Sim | Indica se a categoria está ativa. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

## 3.2. dw.DIM_MARCA

Tabela responsável por armazenar as marcas dos produtos.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_MARCA | NUMBER | PK | Sim | Chave técnica da marca no DW. | Gerada automaticamente por identity. |
| ID_MARCA_ORIGEM | VARCHAR2(50) | UK | Sim | Identificador da marca no sistema de origem. | Deve ser único. |
| NOME_MARCA | VARCHAR2(150) | Não | Sim | Nome da marca. | Deve estar preenchido. |
| PAIS_ORIGEM | VARCHAR2(100) | Não | Não | País de origem da marca. | Preenchimento opcional. |
| FL_MARCA_PROPRIA | CHAR(1) | Não | Sim | Indica se a marca é própria. | Valores permitidos: `S` ou `N`. |
| FL_ATIVO | CHAR(1) | Não | Sim | Indica se a marca está ativa. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

## 3.3. dw.DIM_FORNECEDOR

Tabela responsável por armazenar os fornecedores dos produtos.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_FORNECEDOR | NUMBER | PK | Sim | Chave técnica do fornecedor no DW. | Gerada automaticamente por identity. |
| ID_FORNECEDOR_ORIGEM | VARCHAR2(50) | UK | Sim | Identificador do fornecedor no sistema de origem. | Deve ser único. |
| NOME_FORNECEDOR | VARCHAR2(200) | Não | Sim | Nome do fornecedor. | Deve estar preenchido. |
| CNPJ_FORNECEDOR | VARCHAR2(20) | Não | Não | CNPJ do fornecedor. | Preenchimento opcional. |
| CIDADE | VARCHAR2(100) | Não | Não | Cidade do fornecedor. | Preenchimento opcional. |
| ESTADO | VARCHAR2(2) | Não | Não | Unidade federativa do fornecedor. | Recomenda-se usar sigla UF com 2 caracteres. |
| PAIS | VARCHAR2(100) | Não | Não | País do fornecedor. | Default `Brasil`. |
| TIPO_FORNECEDOR | VARCHAR2(100) | Não | Não | Classificação do fornecedor. | Exemplo: indústria, distribuidor, importador. |
| FL_ATIVO | CHAR(1) | Não | Sim | Indica se o fornecedor está ativo. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

## 3.4. dw.DIM_PRODUTO

Tabela responsável por armazenar os produtos e seus atributos comerciais, físicos e históricos.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_PRODUTO | NUMBER | PK | Sim | Chave técnica do produto no DW. | Gerada automaticamente por identity. |
| ID_PRODUTO_ORIGEM | VARCHAR2(50) | Não | Sim | Identificador do produto no sistema de origem. | Pode se repetir em cenários SCD Tipo 2. |
| SK_CATEGORIA | NUMBER | FK | Sim | Chave da categoria do produto. | Referencia `dw.DIM_CATEGORIA`. |
| SK_MARCA | NUMBER | FK | Não | Chave da marca do produto. | Referencia `dw.DIM_MARCA`. |
| SK_FORNECEDOR | NUMBER | FK | Não | Chave do fornecedor do produto. | Referencia `dw.DIM_FORNECEDOR`. |
| NOME_PRODUTO | VARCHAR2(250) | Não | Sim | Nome do produto. | Deve estar preenchido. |
| DESCRICAO_PRODUTO | VARCHAR2(500) | Não | Não | Descrição detalhada do produto. | Preenchimento opcional. |
| CODIGO_BARRAS | VARCHAR2(50) | Não | Não | Código de barras do produto. | Preenchimento opcional. |
| SKU | VARCHAR2(100) | Não | Não | Código SKU do produto. | Preenchimento opcional. |
| UNIDADE_MEDIDA | VARCHAR2(20) | Não | Não | Unidade de medida comercial. | Exemplo: UN, KG, CX, LT. |
| PESO_KG | NUMBER(18,4) | Não | Não | Peso do produto em quilogramas. | Deve ser maior ou igual a zero, quando informado. |
| ALTURA_CM | NUMBER(18,4) | Não | Não | Altura do produto em centímetros. | Deve ser maior ou igual a zero, quando informado. |
| LARGURA_CM | NUMBER(18,4) | Não | Não | Largura do produto em centímetros. | Deve ser maior ou igual a zero, quando informado. |
| PROFUNDIDADE_CM | NUMBER(18,4) | Não | Não | Profundidade do produto em centímetros. | Deve ser maior ou igual a zero, quando informado. |
| CUSTO_UNITARIO | NUMBER(18,2) | Não | Não | Custo unitário do produto. | Deve ser maior ou igual a zero, quando informado. |
| PRECO_LISTA | NUMBER(18,2) | Não | Não | Preço de lista do produto. | Deve ser maior ou igual a zero, quando informado. |
| FL_PERECIVEL | CHAR(1) | Não | Sim | Indica se o produto é perecível. | Valores permitidos: `S` ou `N`. |
| FL_ATIVO | CHAR(1) | Não | Sim | Indica se o produto está ativo. | Valores permitidos: `S` ou `N`. |
| DATA_INICIO_VIGENCIA | DATE | Não | Sim | Data de início da vigência do registro. | Usada para controle histórico. |
| DATA_FIM_VIGENCIA | DATE | Não | Não | Data de fim da vigência do registro. | Nula para registro atual. |
| FL_REGISTRO_ATUAL | CHAR(1) | Não | Sim | Indica se o registro é a versão atual do produto. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

## 3.5. dw.DIM_CLIENTE

Tabela responsável por armazenar dados cadastrais, demográficos e de segmentação dos clientes.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_CLIENTE | NUMBER | PK | Sim | Chave técnica do cliente no DW. | Gerada automaticamente por identity. |
| ID_CLIENTE_ORIGEM | VARCHAR2(50) | Não | Sim | Identificador do cliente no sistema de origem. | Pode se repetir em cenários SCD Tipo 2. |
| NOME_CLIENTE | VARCHAR2(200) | Não | Não | Nome do cliente. | Preenchimento opcional. |
| TIPO_CLIENTE | VARCHAR2(50) | Não | Não | Tipo de cliente. | Valores esperados: `PF` ou `PJ`. |
| CPF_CNPJ | VARCHAR2(20) | Não | Não | Documento do cliente. | Pode conter CPF ou CNPJ. |
| SEXO | VARCHAR2(20) | Não | Não | Sexo informado do cliente. | Preenchimento opcional. |
| FAIXA_ETARIA | VARCHAR2(50) | Não | Não | Faixa etária do cliente. | Pode ser derivada da data de nascimento. |
| DATA_NASCIMENTO | DATE | Não | Não | Data de nascimento do cliente. | Preenchimento opcional. |
| CIDADE | VARCHAR2(100) | Não | Não | Cidade do cliente. | Preenchimento opcional. |
| ESTADO | VARCHAR2(2) | Não | Não | Unidade federativa do cliente. | Recomenda-se usar sigla UF com 2 caracteres. |
| PAIS | VARCHAR2(100) | Não | Não | País do cliente. | Default `Brasil`. |
| SEGMENTO_CLIENTE | VARCHAR2(100) | Não | Não | Segmento comercial do cliente. | Exemplo: varejo, recorrente, premium. |
| DATA_CADASTRO | DATE | Não | Não | Data de cadastro do cliente. | Preenchimento opcional. |
| DATA_INICIO_VIGENCIA | DATE | Não | Sim | Data de início da vigência histórica. | Usada para controle SCD. |
| DATA_FIM_VIGENCIA | DATE | Não | Não | Data de fim da vigência histórica. | Nula para registro atual. |
| FL_REGISTRO_ATUAL | CHAR(1) | Não | Sim | Indica se o registro é a versão atual do cliente. | Valores permitidos: `S` ou `N`. |
| FL_ATIVO | CHAR(1) | Não | Sim | Indica se o cliente está ativo. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

## 3.6. dw.DIM_FORMAPAGTO

Tabela responsável por armazenar as formas de pagamento.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_FORMAPAGTO | NUMBER | PK | Sim | Chave técnica da forma de pagamento no DW. | Gerada automaticamente por identity. |
| ID_FORMAPAGTO_ORIGEM | VARCHAR2(50) | UK | Sim | Identificador da forma de pagamento no sistema de origem. | Deve ser único. |
| DESCRICAO_FORMAPAGTO | VARCHAR2(100) | Não | Sim | Descrição da forma de pagamento. | Exemplo: dinheiro, cartão crédito, PIX. |
| TIPO_FORMAPAGTO | VARCHAR2(50) | Não | Não | Tipo da forma de pagamento. | Exemplo: à vista, cartão, digital. |
| MODALIDADE | VARCHAR2(50) | Não | Não | Modalidade da forma de pagamento. | Exemplo: crédito, débito, boleto. |
| QTD_PARCELAS | NUMBER(3) | Não | Não | Quantidade de parcelas associada. | Deve ser maior ou igual a zero, quando informada. |
| FL_CREDITO | CHAR(1) | Não | Sim | Indica se a forma de pagamento é crédito. | Valores permitidos: `S` ou `N`. |
| FL_ATIVO | CHAR(1) | Não | Sim | Indica se a forma de pagamento está ativa. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

## 3.7. dw.DIM_PROMOCAO

Tabela responsável por armazenar promoções e condições comerciais.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_PROMOCAO | NUMBER | PK | Sim | Chave técnica da promoção no DW. | Gerada automaticamente por identity. |
| ID_PROMOCAO_ORIGEM | VARCHAR2(50) | UK | Sim | Identificador da promoção no sistema de origem. | Deve ser único. |
| NOME_PROMOCAO | VARCHAR2(200) | Não | Sim | Nome da promoção. | Deve estar preenchido. |
| TIPO_PROMOCAO | VARCHAR2(100) | Não | Não | Tipo da promoção. | Exemplo: desconto, leve mais pague menos, campanha sazonal. |
| MECANICA_PROMOCAO | VARCHAR2(200) | Não | Não | Descrição da mecânica promocional. | Preenchimento opcional. |
| DATA_INICIO_PROMOCAO | DATE | Não | Sim | Data de início da promoção. | Deve ser menor ou igual à data fim. |
| DATA_FIM_PROMOCAO | DATE | Não | Sim | Data de fim da promoção. | Deve ser maior ou igual à data início. |
| PERCENTUAL_DESCONTO | NUMBER(9,4) | Não | Não | Percentual de desconto aplicado. | Deve estar entre 0 e 100, quando informado. |
| VALOR_DESCONTO | NUMBER(18,2) | Não | Não | Valor fixo de desconto aplicado. | Deve ser maior ou igual a zero, quando informado. |
| FL_PROMOCAO_ATIVA | CHAR(1) | Não | Sim | Indica se a promoção está ativa. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

## 3.8. dw.DIM_SAZONALIDADE

Tabela responsável por armazenar períodos sazonais relevantes para análise comercial.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_SAZONALIDADE | NUMBER | PK | Sim | Chave técnica da sazonalidade no DW. | Gerada automaticamente por identity. |
| ID_SAZONALIDADE_ORIGEM | VARCHAR2(50) | UK | Sim | Identificador da sazonalidade no sistema de origem. | Deve ser único. |
| NOME_SAZONALIDADE | VARCHAR2(150) | Não | Sim | Nome da sazonalidade. | Exemplo: Black Friday, Natal, Dia das Mães. |
| TIPO_SAZONALIDADE | VARCHAR2(100) | Não | Não | Tipo de sazonalidade. | Exemplo: comercial, climática, comemorativa. |
| DESCRICAO | VARCHAR2(500) | Não | Não | Descrição detalhada da sazonalidade. | Preenchimento opcional. |
| DATA_INICIO | DATE | Não | Sim | Data de início do período sazonal. | Deve ser menor ou igual à data fim. |
| DATA_FIM | DATE | Não | Sim | Data de fim do período sazonal. | Deve ser maior ou igual à data início. |
| FL_RECORRENTE | CHAR(1) | Não | Sim | Indica se a sazonalidade ocorre de forma recorrente. | Valores permitidos: `S` ou `N`. |
| FL_ATIVO | CHAR(1) | Não | Sim | Indica se a sazonalidade está ativa. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

## 3.9. dw.DIM_TEMPO

Tabela calendário utilizada nas análises temporais.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_TEMPO | NUMBER(8) | PK | Sim | Chave técnica da data no formato `YYYYMMDD`. | Exemplo: `20260630`. |
| DATA_COMPLETA | DATE | UK | Sim | Data completa. | Deve ser única. |
| DIA | NUMBER(2) | Não | Sim | Dia do mês. | Valor entre 1 e 31. |
| MES | NUMBER(2) | Não | Sim | Número do mês. | Valor entre 1 e 12. |
| ANO | NUMBER(4) | Não | Sim | Ano da data. | Exemplo: 2026. |
| NOME_DIA_SEMANA | VARCHAR2(30) | Não | Não | Nome do dia da semana. | Exemplo: segunda-feira. |
| NUM_DIA_SEMANA | NUMBER(1) | Não | Não | Número do dia da semana. | Recomendado valor entre 1 e 7. |
| NOME_MES | VARCHAR2(30) | Não | Não | Nome do mês. | Exemplo: junho. |
| ANO_MES | VARCHAR2(7) | Não | Não | Ano e mês da data. | Formato recomendado: `YYYY-MM`. |
| TRIMESTRE | NUMBER(1) | Não | Não | Trimestre da data. | Valor entre 1 e 4. |
| SEMESTRE | NUMBER(1) | Não | Não | Semestre da data. | Valor entre 1 e 2. |
| FL_FIM_SEMANA | CHAR(1) | Não | Sim | Indica se a data é fim de semana. | Valores permitidos: `S` ou `N`. |
| FL_FERIADO | CHAR(1) | Não | Sim | Indica se a data é feriado. | Valores permitidos: `S` ou `N`. |
| NOME_FERIADO | VARCHAR2(150) | Não | Não | Nome do feriado. | Preenchido quando `FL_FERIADO = 'S'`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |

---

## 3.10. dw.DIM_PRODUTORUPTURA

Tabela responsável por armazenar os tipos, motivos ou classificações de ruptura.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_PRODUTORUPTURA | NUMBER | PK | Sim | Chave técnica da classificação de ruptura. | Gerada automaticamente por identity. |
| ID_RUPTURA_ORIGEM | VARCHAR2(50) | UK | Sim | Identificador da ruptura no sistema de origem. | Deve ser único. |
| DESCRICAO_RUPTURA | VARCHAR2(200) | Não | Sim | Descrição da ruptura. | Deve estar preenchida. |
| TIPO_RUPTURA | VARCHAR2(100) | Não | Não | Tipo da ruptura. | Exemplo: logística, fornecedor, demanda, cadastro. |
| RESPONSAVEL_RUPTURA | VARCHAR2(100) | Não | Não | Responsável associado à ruptura. | Exemplo: fornecedor, loja, centro de distribuição. |
| FL_ATIVO | CHAR(1) | Não | Sim | Indica se o motivo da ruptura está ativo. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

Observação: conceitualmente, esta tabela também poderia ser nomeada como `DIM_MOTIVO_RUPTURA`, pois representa a classificação ou motivo da ruptura.

---

## 3.11. dw.DIM_LOJA

Tabela responsável por armazenar as lojas ou unidades comerciais.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_LOJA | NUMBER | PK | Sim | Chave técnica da loja no DW. | Gerada automaticamente por identity. |
| ID_LOJA_ORIGEM | VARCHAR2(50) | UK | Sim | Identificador da loja no sistema de origem. | Deve ser único. |
| NOME_LOJA | VARCHAR2(200) | Não | Sim | Nome da loja. | Deve estar preenchido. |
| CNPJ_LOJA | VARCHAR2(20) | Não | Não | CNPJ da loja. | Preenchimento opcional. |
| TIPO_LOJA | VARCHAR2(100) | Não | Não | Tipo da loja. | Exemplo: física, e-commerce, CD, franquia. |
| CIDADE | VARCHAR2(100) | Não | Não | Cidade da loja. | Preenchimento opcional. |
| ESTADO | VARCHAR2(2) | Não | Não | Unidade federativa da loja. | Recomenda-se usar sigla UF com 2 caracteres. |
| REGIONAL | VARCHAR2(100) | Não | Não | Regional comercial da loja. | Exemplo: Sudeste, Nordeste, Sul. |
| PAIS | VARCHAR2(100) | Não | Não | País da loja. | Default `Brasil`. |
| DATA_ABERTURA | DATE | Não | Não | Data de abertura da loja. | Preenchimento opcional. |
| FL_ATIVO | CHAR(1) | Não | Sim | Indica se a loja está ativa. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

## 3.12. dw.DIM_CANALVENDA

Tabela responsável por armazenar os canais de venda.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_CANALVENDA | NUMBER | PK | Sim | Chave técnica do canal de venda no DW. | Gerada automaticamente por identity. |
| ID_CANALVENDA_ORIGEM | VARCHAR2(50) | UK | Sim | Identificador do canal de venda no sistema de origem. | Deve ser único. |
| NOME_CANALVENDA | VARCHAR2(100) | Não | Sim | Nome do canal de venda. | Exemplo: loja física, e-commerce, marketplace. |
| TIPO_CANAL | VARCHAR2(100) | Não | Não | Tipo do canal. | Exemplo: físico, digital, parceiro. |
| DESCRICAO_CANAL | VARCHAR2(300) | Não | Não | Descrição do canal de venda. | Preenchimento opcional. |
| FL_ATIVO | CHAR(1) | Não | Sim | Indica se o canal de venda está ativo. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

# 4. Tabelas Fato

## 4.1. dw.FATO_VENDAS

Tabela fato transacional responsável por armazenar os itens vendidos.

Grão da tabela: uma linha por item de venda.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_FATO_VENDA | NUMBER | PK | Sim | Chave técnica da linha da fato de vendas. | Gerada automaticamente por identity. |
| ID_VENDA_ORIGEM | VARCHAR2(50) | Não | Sim | Identificador da venda no sistema de origem. | Deve estar preenchido. |
| ID_ITEM_VENDA_ORIGEM | VARCHAR2(50) | Não | Não | Identificador do item da venda no sistema de origem. | Usado quando a venda possui múltiplos itens. |
| SK_TEMPO | NUMBER(8) | FK | Sim | Chave da data da venda. | Referencia `dw.DIM_TEMPO`. |
| SK_CLIENTE | NUMBER | FK | Não | Chave do cliente da venda. | Referencia `dw.DIM_CLIENTE`. |
| SK_PRODUTO | NUMBER | FK | Sim | Chave do produto vendido. | Referencia `dw.DIM_PRODUTO`. |
| SK_CATEGORIA | NUMBER | FK | Não | Chave da categoria do produto vendido. | Referencia `dw.DIM_CATEGORIA`. |
| SK_MARCA | NUMBER | FK | Não | Chave da marca do produto vendido. | Referencia `dw.DIM_MARCA`. |
| SK_FORNECEDOR | NUMBER | FK | Não | Chave do fornecedor do produto vendido. | Referencia `dw.DIM_FORNECEDOR`. |
| SK_FORMAPAGTO | NUMBER | FK | Não | Chave da forma de pagamento. | Referencia `dw.DIM_FORMAPAGTO`. |
| SK_PROMOCAO | NUMBER | FK | Não | Chave da promoção aplicada. | Referencia `dw.DIM_PROMOCAO`. |
| SK_LOJA | NUMBER | FK | Não | Chave da loja onde ocorreu a venda. | Referencia `dw.DIM_LOJA`. |
| SK_CANALVENDA | NUMBER | FK | Não | Chave do canal de venda. | Referencia `dw.DIM_CANALVENDA`. |
| QUANTIDADE | NUMBER(18,4) | Não | Sim | Quantidade vendida do item. | Deve ser maior ou igual a zero. |
| VALOR_UNITARIO | NUMBER(18,2) | Não | Sim | Valor unitário do item vendido. | Deve ser maior ou igual a zero. |
| VALOR_BRUTO | NUMBER(18,2) | Não | Sim | Valor bruto da venda. | Deve ser maior ou igual a zero. |
| VALOR_DESCONTO | NUMBER(18,2) | Não | Sim | Valor de desconto aplicado. | Deve ser maior ou igual a zero. |
| VALOR_LIQUIDO | NUMBER(18,2) | Não | Sim | Valor líquido da venda. | Deve ser maior ou igual a zero. |
| CUSTO_TOTAL | NUMBER(18,2) | Não | Não | Custo total do item vendido. | Deve ser maior ou igual a zero, quando informado. |
| MARGEM_BRUTA | NUMBER(18,2) | Não | Não | Margem bruta da venda. | Pode ser calculada por `VALOR_LIQUIDO - CUSTO_TOTAL`. |
| DATA_HORA_VENDA | TIMESTAMP | Não | Não | Data e hora real da venda. | Usada para análises intradiárias. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

## 4.2. dw.FATO_ESTOQUE

Tabela fato snapshot responsável por armazenar a posição de estoque.

Grão da tabela: uma linha por produto, loja e data.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_FATO_ESTOQUE | NUMBER | PK | Sim | Chave técnica da linha da fato de estoque. | Gerada automaticamente por identity. |
| ID_ESTOQUE_ORIGEM | VARCHAR2(50) | Não | Não | Identificador da posição de estoque na origem. | Preenchimento opcional. |
| SK_TEMPO | NUMBER(8) | FK | Sim | Chave da data de referência do estoque. | Referencia `dw.DIM_TEMPO`. |
| SK_PRODUTO | NUMBER | FK | Sim | Chave do produto. | Referencia `dw.DIM_PRODUTO`. |
| SK_LOJA | NUMBER | FK | Sim | Chave da loja. | Referencia `dw.DIM_LOJA`. |
| SK_CATEGORIA | NUMBER | FK | Não | Chave da categoria do produto. | Referencia `dw.DIM_CATEGORIA`. |
| SK_MARCA | NUMBER | FK | Não | Chave da marca do produto. | Referencia `dw.DIM_MARCA`. |
| SK_FORNECEDOR | NUMBER | FK | Não | Chave do fornecedor do produto. | Referencia `dw.DIM_FORNECEDOR`. |
| QTD_ESTOQUE_DISPONIVEL | NUMBER(18,4) | Não | Sim | Quantidade disponível para venda. | Deve ser maior ou igual a zero. |
| QTD_ESTOQUE_RESERVADO | NUMBER(18,4) | Não | Sim | Quantidade reservada. | Deve ser maior ou igual a zero. |
| QTD_ESTOQUE_BLOQUEADO | NUMBER(18,4) | Não | Sim | Quantidade bloqueada. | Deve ser maior ou igual a zero. |
| QTD_ESTOQUE_TRANSITO | NUMBER(18,4) | Não | Sim | Quantidade em trânsito. | Deve ser maior ou igual a zero. |
| QTD_ESTOQUE_TOTAL | NUMBER(18,4) | Não | Sim | Quantidade total de estoque. | Deve ser maior ou igual a zero. |
| QTD_ESTOQUE_MINIMO | NUMBER(18,4) | Não | Não | Quantidade mínima esperada em estoque. | Deve ser maior ou igual a zero, quando informada. |
| QTD_ESTOQUE_MAXIMO | NUMBER(18,4) | Não | Não | Quantidade máxima esperada em estoque. | Deve ser maior ou igual a zero, quando informada. |
| QTD_PONTO_REPOSICAO | NUMBER(18,4) | Não | Não | Quantidade que indica ponto de reposição. | Deve ser maior ou igual a zero, quando informada. |
| CUSTO_UNITARIO | NUMBER(18,2) | Não | Não | Custo unitário do produto em estoque. | Deve ser maior ou igual a zero, quando informado. |
| VALOR_ESTOQUE_CUSTO | NUMBER(18,2) | Não | Não | Valor total do estoque a custo. | Deve ser maior ou igual a zero, quando informado. |
| VALOR_ESTOQUE_VENDA | NUMBER(18,2) | Não | Não | Valor potencial de venda do estoque. | Deve ser maior ou igual a zero, quando informado. |
| DIAS_COBERTURA_ESTOQUE | NUMBER(10,2) | Não | Não | Estimativa de dias de cobertura do estoque. | Deve ser maior ou igual a zero, quando informado. |
| GIRO_ESTOQUE | NUMBER(10,4) | Não | Não | Indicador de giro de estoque. | Deve ser maior ou igual a zero, quando informado. |
| FL_RUPTURA | CHAR(1) | Não | Sim | Indica se existe ruptura de estoque. | Valores permitidos: `S` ou `N`. |
| FL_ESTOQUE_BAIXO | CHAR(1) | Não | Sim | Indica se o estoque está baixo. | Valores permitidos: `S` ou `N`. |
| FL_EXCESSO_ESTOQUE | CHAR(1) | Não | Sim | Indica se há excesso de estoque. | Valores permitidos: `S` ou `N`. |
| DATA_REFERENCIA_ESTOQUE | DATE | Não | Sim | Data de referência da posição de estoque. | Deve estar preenchida. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

## 4.3. dw.FATO_RUPTURA_ESTOQUE

Tabela fato responsável por armazenar eventos de ruptura de estoque.

Grão da tabela: uma linha por evento de ruptura de produto por loja e data.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_FATO_RUPTURA | NUMBER | PK | Sim | Chave técnica da linha da fato de ruptura. | Gerada automaticamente por identity. |
| ID_RUPTURA_ORIGEM | VARCHAR2(50) | Não | Não | Identificador da ruptura no sistema de origem. | Preenchimento opcional. |
| SK_TEMPO | NUMBER(8) | FK | Sim | Chave da data da ruptura. | Referencia `dw.DIM_TEMPO`. |
| SK_PRODUTO | NUMBER | FK | Sim | Chave do produto em ruptura. | Referencia `dw.DIM_PRODUTO`. |
| SK_LOJA | NUMBER | FK | Sim | Chave da loja afetada pela ruptura. | Referencia `dw.DIM_LOJA`. |
| SK_MOTIVO_RUPTURA | NUMBER | FK | Não | Chave do motivo ou classificação da ruptura. | Referencia `dw.DIM_PRODUTORUPTURA`. |
| QTD_ESTOQUE_ESPERADO | NUMBER(18,4) | Não | Não | Quantidade esperada de estoque. | Deve ser maior ou igual a zero, quando informada. |
| QTD_ESTOQUE_DISPONIVEL | NUMBER(18,4) | Não | Não | Quantidade disponível no momento da ruptura. | Deve ser maior ou igual a zero, quando informada. |
| QTD_RUPTURA | NUMBER(18,4) | Não | Não | Quantidade estimada em ruptura. | Deve ser maior ou igual a zero, quando informada. |
| DIAS_RUPTURA | NUMBER(10,2) | Não | Não | Quantidade de dias em ruptura. | Deve ser maior ou igual a zero, quando informada. |
| VALOR_VENDA_PERDIDA | NUMBER(18,2) | Não | Não | Valor estimado de venda perdida por ruptura. | Deve ser maior ou igual a zero, quando informado. |
| FL_RUPTURA | CHAR(1) | Não | Sim | Indica se houve ruptura. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

## 4.4. dw.FATO_METAS

Tabela fato responsável por armazenar metas comerciais.

Grão da tabela: uma linha por período, loja, canal, produto/categoria/marca e tipo de meta.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| SK_FATO_META | NUMBER | PK | Sim | Chave técnica da linha da fato de metas. | Gerada automaticamente por identity. |
| ID_META_ORIGEM | VARCHAR2(50) | Não | Não | Identificador da meta no sistema de origem. | Preenchimento opcional. |
| SK_TEMPO | NUMBER(8) | FK | Sim | Chave da data/período da meta. | Referencia `dw.DIM_TEMPO`. |
| SK_LOJA | NUMBER | FK | Não | Chave da loja da meta. | Referencia `dw.DIM_LOJA`. |
| SK_CANALVENDA | NUMBER | FK | Não | Chave do canal de venda da meta. | Referencia `dw.DIM_CANALVENDA`. |
| SK_PRODUTO | NUMBER | FK | Não | Chave do produto da meta. | Referencia `dw.DIM_PRODUTO`. |
| SK_CATEGORIA | NUMBER | FK | Não | Chave da categoria da meta. | Referencia `dw.DIM_CATEGORIA`. |
| SK_MARCA | NUMBER | FK | Não | Chave da marca da meta. | Referencia `dw.DIM_MARCA`. |
| ANO | NUMBER(4) | Não | Sim | Ano da meta. | Deve estar preenchido. |
| MES | NUMBER(2) | Não | Sim | Mês da meta. | Valor entre 1 e 12. |
| ANO_MES | VARCHAR2(7) | Não | Sim | Ano e mês da meta. | Formato recomendado: `YYYY-MM`. |
| TIPO_META | VARCHAR2(100) | Não | Sim | Tipo da meta comercial. | Valores permitidos: `FATURAMENTO`, `VOLUME`, `MARGEM`, `TICKET_MEDIO`, `MISTA`. |
| META_FATURAMENTO_BRUTO | NUMBER(18,2) | Não | Sim | Meta de faturamento bruto. | Deve ser maior ou igual a zero. |
| META_FATURAMENTO_LIQUIDO | NUMBER(18,2) | Não | Sim | Meta de faturamento líquido. | Deve ser maior ou igual a zero. |
| META_QTD_VENDAS | NUMBER(18,4) | Não | Não | Meta de quantidade de vendas. | Deve ser maior ou igual a zero, quando informada. |
| META_QTD_ITENS | NUMBER(18,4) | Não | Não | Meta de quantidade de itens vendidos. | Deve ser maior ou igual a zero, quando informada. |
| META_TICKET_MEDIO | NUMBER(18,2) | Não | Não | Meta de ticket médio. | Deve ser maior ou igual a zero, quando informada. |
| META_MARGEM_BRUTA | NUMBER(18,2) | Não | Não | Meta de margem bruta. | Deve ser maior ou igual a zero, quando informada. |
| META_PERCENTUAL_MARGEM | NUMBER(9,4) | Não | Não | Meta percentual de margem. | Deve estar entre 0 e 100, quando informada. |
| DATA_INICIO_META | DATE | Não | Sim | Data de início da vigência da meta. | Deve ser menor ou igual à data fim. |
| DATA_FIM_META | DATE | Não | Sim | Data de fim da vigência da meta. | Deve ser maior ou igual à data início. |
| FL_META_ATIVA | CHAR(1) | Não | Sim | Indica se a meta está ativa. | Valores permitidos: `S` ou `N`. |
| DATA_CARGA | TIMESTAMP | Não | Sim | Data e hora da carga do registro no DW. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO_DW | TIMESTAMP | Não | Não | Data e hora da última atualização do registro no DW. | Preenchida em atualizações. |

---

# 5. Tabelas Técnicas

## 5.1. dw.CONTROLE_CARGA

Tabela técnica responsável por controlar execuções de carga, status, watermark e volumetria.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| ID_CONTROLE_CARGA | NUMBER | PK | Sim | Chave técnica do controle de carga. | Gerada automaticamente por identity. |
| NOME_PROCESSO | VARCHAR2(200) | Não | Sim | Nome lógico do processo de carga. | Exemplo: `CARGA_FATO_VENDAS`. |
| NOME_PIPELINE | VARCHAR2(200) | Não | Não | Nome do pipeline, notebook ou job responsável. | Preenchimento opcional. |
| NOME_TABELA | VARCHAR2(200) | Não | Sim | Nome da tabela processada. | Exemplo: `dw.FATO_VENDAS`. |
| CAMADA_DADOS | VARCHAR2(50) | Não | Sim | Camada de dados processada. | Valores esperados: `ORIGEM`, `STAGING`, `BRONZE`, `SILVER`, `GOLD`, `DW`. |
| TIPO_CARGA | VARCHAR2(50) | Não | Sim | Tipo da carga executada. | Valores esperados: `FULL`, `INCREMENTAL`, `REPROCESSAMENTO`, `MANUAL`. |
| STATUS_CARGA | VARCHAR2(50) | Não | Sim | Status da carga. | Valores esperados: `INICIADO`, `EM_EXECUCAO`, `SUCESSO`, `ERRO`, `CANCELADO`, `REPROCESSADO`. |
| DATA_INICIO_CARGA | TIMESTAMP | Não | Não | Data e hora de início da carga. | Preenchida no início do processo. |
| DATA_FIM_CARGA | TIMESTAMP | Não | Não | Data e hora de fim da carga. | Deve ser maior ou igual à data de início. |
| WATERMARK_INICIO | TIMESTAMP | Não | Não | Watermark inicial utilizado na carga incremental. | Usado em cargas incrementais. |
| WATERMARK_FIM | TIMESTAMP | Não | Não | Watermark final utilizado na carga incremental. | Deve ser maior ou igual ao watermark inicial. |
| ULTIMA_DATA_PROCESSADA | TIMESTAMP | Não | Não | Última data processada com sucesso. | Atualizada ao fim de cargas bem-sucedidas. |
| QTD_LINHAS_LIDAS | NUMBER | Não | Sim | Quantidade de linhas lidas na origem. | Deve ser maior ou igual a zero. |
| QTD_LINHAS_GRAVADAS | NUMBER | Não | Sim | Quantidade de linhas gravadas no destino. | Deve ser maior ou igual a zero. |
| QTD_LINHAS_ATUALIZADAS | NUMBER | Não | Sim | Quantidade de linhas atualizadas. | Deve ser maior ou igual a zero. |
| QTD_LINHAS_REJEITADAS | NUMBER | Não | Sim | Quantidade de linhas rejeitadas. | Deve ser maior ou igual a zero. |
| ID_EXECUCAO | VARCHAR2(100) | Não | Não | Identificador único da execução. | Usado para rastreabilidade. |
| USUARIO_EXECUCAO | VARCHAR2(100) | Não | Não | Usuário responsável pela execução. | Default `USER`. |
| MENSAGEM_ERRO | VARCHAR2(4000) | Não | Não | Mensagem de erro em caso de falha. | Preenchida quando `STATUS_CARGA = 'ERRO'`. |
| DATA_CRIACAO | TIMESTAMP | Não | Sim | Data e hora de criação do registro. | Default `SYSTIMESTAMP`. |
| DATA_ATUALIZACAO | TIMESTAMP | Não | Não | Data e hora da última atualização do controle. | Preenchida em atualizações. |

---

## 5.2. dw.LOG_EXECUCAO

Tabela técnica responsável por registrar eventos e etapas dos processos de carga.

| Coluna | Tipo de dado | Chave | Obrigatório | Descrição | Regra de negócio |
|---|---:|---|---|---|---|
| ID_LOG_EXECUCAO | NUMBER | PK | Sim | Chave técnica do registro de log. | Gerada automaticamente por identity. |
| ID_CONTROLE_CARGA | NUMBER | FK | Não | Chave do controle de carga relacionado. | Referencia `dw.CONTROLE_CARGA`. |
| ID_EXECUCAO | VARCHAR2(100) | Não | Não | Identificador único da execução. | Deve ser o mesmo usado no controle da carga. |
| NOME_PROCESSO | VARCHAR2(200) | Não | Sim | Nome lógico do processo executado. | Exemplo: `CARGA_FATO_VENDAS`. |
| NOME_PIPELINE | VARCHAR2(200) | Não | Não | Nome do pipeline, notebook ou job. | Preenchimento opcional. |
| NOME_ETAPA | VARCHAR2(200) | Não | Sim | Nome da etapa executada. | Exemplo: `EXTRACAO`, `VALIDACAO`, `MERGE`, `FINALIZACAO`. |
| NOME_TABELA | VARCHAR2(200) | Não | Não | Nome da tabela relacionada ao evento. | Exemplo: `dw.FATO_VENDAS`. |
| CAMADA_DADOS | VARCHAR2(50) | Não | Não | Camada de dados relacionada ao evento. | Valores esperados: `ORIGEM`, `STAGING`, `BRONZE`, `SILVER`, `GOLD`, `DW`. |
| TIPO_EVENTO | VARCHAR2(50) | Não | Sim | Tipo do evento registrado. | Valores esperados: `INICIO`, `FIM`, `INFO`, `ALERTA`, `ERRO`, `VALIDACAO`, `MERGE`, `INSERT`, `UPDATE`, `DELETE`. |
| STATUS_EVENTO | VARCHAR2(50) | Não | Sim | Status do evento registrado. | Valores esperados: `INICIADO`, `EM_EXECUCAO`, `SUCESSO`, `ERRO`, `ALERTA`, `CANCELADO`. |
| DATA_INICIO_EVENTO | TIMESTAMP | Não | Não | Data e hora de início do evento. | Preenchida no início da etapa. |
| DATA_FIM_EVENTO | TIMESTAMP | Não | Não | Data e hora de fim do evento. | Deve ser maior ou igual à data de início. |
| DURACAO_SEGUNDOS | NUMBER(18,2) | Não | Não | Duração do evento em segundos. | Deve ser maior ou igual a zero, quando informada. |
| QTD_LINHAS_PROCESSADAS | NUMBER | Não | Sim | Quantidade total de linhas processadas. | Deve ser maior ou igual a zero. |
| QTD_LINHAS_INSERIDAS | NUMBER | Não | Sim | Quantidade de linhas inseridas. | Deve ser maior ou igual a zero. |
| QTD_LINHAS_ATUALIZADAS | NUMBER | Não | Sim | Quantidade de linhas atualizadas. | Deve ser maior ou igual a zero. |
| QTD_LINHAS_EXCLUIDAS | NUMBER | Não | Sim | Quantidade de linhas excluídas. | Deve ser maior ou igual a zero. |
| QTD_LINHAS_REJEITADAS | NUMBER | Não | Sim | Quantidade de linhas rejeitadas. | Deve ser maior ou igual a zero. |
| CODIGO_ERRO | VARCHAR2(100) | Não | Não | Código técnico do erro. | Preenchido em eventos de erro. |
| MENSAGEM_ERRO | VARCHAR2(4000) | Não | Não | Mensagem detalhada do erro. | Preenchida em eventos de erro. |
| MENSAGEM_LOG | VARCHAR2(4000) | Não | Não | Mensagem descritiva do evento. | Usada para observabilidade. |
| HOST_EXECUCAO | VARCHAR2(200) | Não | Não | Host, servidor, cluster ou ambiente de execução. | Preenchimento opcional. |
| USUARIO_EXECUCAO | VARCHAR2(100) | Não | Não | Usuário responsável pela execução. | Default `USER`. |
| DATA_LOG | TIMESTAMP | Não | Sim | Data e hora de criação do registro de log. | Default `SYSTIMESTAMP`. |

---

# 6. Relacionamentos Principais

## 6.1. Relacionamentos entre dimensões

| Tabela origem | Coluna origem | Tabela destino | Coluna destino | Tipo |
|---|---|---|---|---|
| dw.DIM_PRODUTO | SK_CATEGORIA | dw.DIM_CATEGORIA | SK_CATEGORIA | FK |
| dw.DIM_PRODUTO | SK_MARCA | dw.DIM_MARCA | SK_MARCA | FK |
| dw.DIM_PRODUTO | SK_FORNECEDOR | dw.DIM_FORNECEDOR | SK_FORNECEDOR | FK |

## 6.2. Relacionamentos da dw.FATO_VENDAS

| Coluna na fato | Dimensão relacionada | Coluna na dimensão |
|---|---|---|
| SK_TEMPO | dw.DIM_TEMPO | SK_TEMPO |
| SK_CLIENTE | dw.DIM_CLIENTE | SK_CLIENTE |
| SK_PRODUTO | dw.DIM_PRODUTO | SK_PRODUTO |
| SK_CATEGORIA | dw.DIM_CATEGORIA | SK_CATEGORIA |
| SK_MARCA | dw.DIM_MARCA | SK_MARCA |
| SK_FORNECEDOR | dw.DIM_FORNECEDOR | SK_FORNECEDOR |
| SK_FORMAPAGTO | dw.DIM_FORMAPAGTO | SK_FORMAPAGTO |
| SK_PROMOCAO | dw.DIM_PROMOCAO | SK_PROMOCAO |
| SK_LOJA | dw.DIM_LOJA | SK_LOJA |
| SK_CANALVENDA | dw.DIM_CANALVENDA | SK_CANALVENDA |

## 6.3. Relacionamentos da dw.FATO_ESTOQUE

| Coluna na fato | Dimensão relacionada | Coluna na dimensão |
|---|---|---|
| SK_TEMPO | dw.DIM_TEMPO | SK_TEMPO |
| SK_PRODUTO | dw.DIM_PRODUTO | SK_PRODUTO |
| SK_LOJA | dw.DIM_LOJA | SK_LOJA |
| SK_CATEGORIA | dw.DIM_CATEGORIA | SK_CATEGORIA |
| SK_MARCA | dw.DIM_MARCA | SK_MARCA |
| SK_FORNECEDOR | dw.DIM_FORNECEDOR | SK_FORNECEDOR |

## 6.4. Relacionamentos da dw.FATO_RUPTURA_ESTOQUE

| Coluna na fato | Dimensão relacionada | Coluna na dimensão |
|---|---|---|
| SK_TEMPO | dw.DIM_TEMPO | SK_TEMPO |
| SK_PRODUTO | dw.DIM_PRODUTO | SK_PRODUTO |
| SK_LOJA | dw.DIM_LOJA | SK_LOJA |
| SK_MOTIVO_RUPTURA | dw.DIM_PRODUTORUPTURA | SK_PRODUTORUPTURA |

## 6.5. Relacionamentos da dw.FATO_METAS

| Coluna na fato | Dimensão relacionada | Coluna na dimensão |
|---|---|---|
| SK_TEMPO | dw.DIM_TEMPO | SK_TEMPO |
| SK_LOJA | dw.DIM_LOJA | SK_LOJA |
| SK_CANALVENDA | dw.DIM_CANALVENDA | SK_CANALVENDA |
| SK_PRODUTO | dw.DIM_PRODUTO | SK_PRODUTO |
| SK_CATEGORIA | dw.DIM_CATEGORIA | SK_CATEGORIA |
| SK_MARCA | dw.DIM_MARCA | SK_MARCA |

## 6.6. Relacionamento técnico de log

| Tabela origem | Coluna origem | Tabela destino | Coluna destino | Tipo |
|---|---|---|---|---|
| dw.LOG_EXECUCAO | ID_CONTROLE_CARGA | dw.CONTROLE_CARGA | ID_CONTROLE_CARGA | FK |

---

# 7. Observações de Modelagem

## 7.1. Sobre chaves técnicas

Todas as dimensões utilizam surrogate keys como chave primária. As tabelas fato armazenam essas surrogate keys para garantir integridade referencial e melhorar a performance das consultas analíticas.

## 7.2. Sobre chaves de origem

As colunas `ID_..._ORIGEM` permitem rastrear os dados até o sistema fonte. Em dimensões com histórico, como produto e cliente, a chave de origem pode se repetir em múltiplas versões históricas.

## 7.3. Sobre SCD Tipo 2

As dimensões `dw.DIM_PRODUTO` e `dw.DIM_CLIENTE` possuem campos para controle histórico:

| Coluna | Finalidade |
|---|---|
| DATA_INICIO_VIGENCIA | Indica o início da validade do registro |
| DATA_FIM_VIGENCIA | Indica o fim da validade do registro |
| FL_REGISTRO_ATUAL | Indica se o registro é a versão atual |

## 7.4. Sobre fatos com chaves desnormalizadas

As tabelas fato possuem algumas chaves que também podem ser obtidas por meio da `dw.DIM_PRODUTO`, como `SK_CATEGORIA`, `SK_MARCA` e `SK_FORNECEDOR`.

Essa abordagem foi adotada para facilitar consultas analíticas e melhorar performance em cenários de alto volume.

## 7.5. Sobre dados não informados

Recomenda-se criar registros técnicos nas dimensões para representar valores não informados, não aplicáveis ou não identificados.

Exemplo de padrão sugerido:

| SK | Significado |
|---:|---|
| -1 | Não informado |
| -2 | Não aplicável |
| -3 | Não identificado |

Esse padrão reduz o uso de valores nulos em tabelas fato e facilita análises no Power BI, SQL e camadas Gold.

---