# Regras de Negócio

## Projeto: Data Warehouse Comercial

## 1. Objetivo do Documento

Este documento descreve as principais regras de negócio aplicadas ao modelo dimensional do projeto de Data Warehouse Comercial.

As regras cobrem os domínios de vendas, estoque, ruptura, metas comerciais, dimensões de apoio, controle de carga, log de execução e qualidade dos dados.

O objetivo é garantir que as cargas, transformações e consultas analíticas sigam critérios consistentes, auditáveis e reutilizáveis.

---

## 2. Escopo do Modelo

O modelo contempla os seguintes macroprocessos:

- Cadastro de produtos, categorias, marcas e fornecedores.
- Cadastro de clientes.
- Cadastro de lojas e canais de venda.
- Cadastro de formas de pagamento.
- Cadastro de promoções e sazonalidades.
- Registro de vendas.
- Registro de posição de estoque.
- Registro de eventos de ruptura de estoque.
- Registro de metas comerciais.
- Controle e auditoria de cargas.
- Log de execução de processos.

---

## 3. Convenções Gerais

### 3.1. Chaves técnicas

Todas as tabelas dimensionais utilizam surrogate keys com prefixo `SK_`.

Exemplos:

```text
SK_PRODUTO
SK_CLIENTE
SK_LOJA
SK_TEMPO
```

As tabelas fato devem armazenar as surrogate keys das dimensões relacionadas.

### 3.2. Chaves de origem

As colunas com padrão `ID_..._ORIGEM` representam identificadores do sistema fonte.

Essas colunas devem ser utilizadas para rastreabilidade, conciliação e processos de carga incremental.

### 3.3. Flags

Campos iniciados por `FL_` devem aceitar preferencialmente os valores:

```text
S = Sim
N = Não
```

### 3.4. Campos de auditoria

As tabelas devem possuir campos de controle como:

```text
DATA_CARGA
DATA_ATUALIZACAO_DW
```

Esses campos devem ser preenchidos durante os processos de carga ou atualização.

---

## 4. Regras de Negócio das Dimensões

## 4.1. dw.DIM_CATEGORIA

### RN-CAT-001: Identificação única da categoria

Cada categoria deve possuir um identificador de origem único em `ID_CATEGORIA_ORIGEM`.

### RN-CAT-002: Categoria obrigatória

Toda categoria deve possuir `NOME_CATEGORIA` preenchido.

### RN-CAT-003: Status da categoria

A coluna `FL_ATIVO` deve indicar se a categoria está ativa ou inativa.

Valores permitidos:

```text
S
N
```

---

## 4.2. dw.DIM_MARCA

### RN-MAR-001: Identificação única da marca

Cada marca deve possuir um identificador de origem único em `ID_MARCA_ORIGEM`.

### RN-MAR-002: Nome da marca obrigatório

A coluna `NOME_MARCA` deve estar preenchida.

### RN-MAR-003: Marca própria

A coluna `FL_MARCA_PROPRIA` deve indicar se a marca pertence à própria empresa.

Valores permitidos:

```text
S
N
```

### RN-MAR-004: Status da marca

A coluna `FL_ATIVO` deve indicar se a marca está ativa ou inativa.

---

## 4.3. dw.DIM_FORNECEDOR

### RN-FOR-001: Identificação única do fornecedor

Cada fornecedor deve possuir um identificador de origem único em `ID_FORNECEDOR_ORIGEM`.

### RN-FOR-002: Nome do fornecedor obrigatório

A coluna `NOME_FORNECEDOR` deve estar preenchida.

### RN-FOR-003: País padrão

Quando não houver país informado, o valor padrão deve ser:

```text
Brasil
```

### RN-FOR-004: Unidade federativa

Quando informado, o campo `ESTADO` deve conter a sigla da unidade federativa com dois caracteres.

### RN-FOR-005: Status do fornecedor

A coluna `FL_ATIVO` deve aceitar apenas:

```text
S
N
```

---

## 4.4. dw.DIM_PRODUTO

### RN-PROD-001: Identificação do produto

Todo produto deve possuir `ID_PRODUTO_ORIGEM` preenchido.

### RN-PROD-002: Produto vinculado à categoria

Todo produto deve estar vinculado a uma categoria válida por meio de `SK_CATEGORIA`.

### RN-PROD-003: Marca e fornecedor opcionais

As colunas `SK_MARCA` e `SK_FORNECEDOR` podem ser nulas quando a informação não estiver disponível.

### RN-PROD-004: Nome do produto obrigatório

A coluna `NOME_PRODUTO` deve estar preenchida.

### RN-PROD-005: Valores monetários não negativos

Os campos abaixo devem ser maiores ou iguais a zero quando informados:

```text
CUSTO_UNITARIO
PRECO_LISTA
```

### RN-PROD-006: Medidas físicas não negativas

Os campos abaixo devem ser maiores ou iguais a zero quando informados:

```text
PESO_KG
ALTURA_CM
LARGURA_CM
PROFUNDIDADE_CM
```

### RN-PROD-007: Produto perecível

A coluna `FL_PERECIVEL` deve aceitar apenas:

```text
S
N
```

### RN-PROD-008: Controle de vigência

Quando `DATA_FIM_VIGENCIA` estiver preenchida, ela deve ser maior ou igual a `DATA_INICIO_VIGENCIA`.

### RN-PROD-009: Registro atual

A coluna `FL_REGISTRO_ATUAL` deve indicar se o registro representa a versão atual do produto.

Valores permitidos:

```text
S
N
```

### RN-PROD-010: Histórico de produto

Caso um produto sofra alteração relevante em atributos controlados historicamente, uma nova versão deve ser criada na dimensão, mantendo o mesmo `ID_PRODUTO_ORIGEM` e uma nova `SK_PRODUTO`.

---

## 4.5. dw.DIM_CLIENTE

### RN-CLI-001: Identificação do cliente

Todo cliente deve possuir `ID_CLIENTE_ORIGEM` preenchido.

### RN-CLI-002: Tipo de cliente

A coluna `TIPO_CLIENTE` deve aceitar somente:

```text
PF
PJ
```

ou valor nulo quando não informado.

### RN-CLI-003: País padrão

Quando não houver país informado, o valor padrão deve ser:

```text
Brasil
```

### RN-CLI-004: Unidade federativa

Quando informado, o campo `ESTADO` deve conter a sigla da unidade federativa com dois caracteres.

### RN-CLI-005: Controle de vigência

Quando `DATA_FIM_VIGENCIA` estiver preenchida, ela deve ser maior ou igual a `DATA_INICIO_VIGENCIA`.

### RN-CLI-006: Registro atual

A coluna `FL_REGISTRO_ATUAL` deve indicar se o registro representa a versão atual do cliente.

Valores permitidos:

```text
S
N
```

### RN-CLI-007: Histórico de cliente

Alterações relevantes em atributos cadastrais ou de segmentação podem gerar nova versão histórica do cliente.

Exemplos de atributos candidatos a histórico:

```text
CIDADE
ESTADO
SEGMENTO_CLIENTE
TIPO_CLIENTE
```

---

## 4.6. dw.DIM_FORMAPAGTO

### RN-FPG-001: Identificação única da forma de pagamento

Cada forma de pagamento deve possuir `ID_FORMAPAGTO_ORIGEM` único.

### RN-FPG-002: Descrição obrigatória

A coluna `DESCRICAO_FORMAPAGTO` deve estar preenchida.

### RN-FPG-003: Quantidade de parcelas

Quando informada, `QTD_PARCELAS` deve ser maior ou igual a zero.

### RN-FPG-004: Identificação de crédito

A coluna `FL_CREDITO` deve indicar se a forma de pagamento representa crédito.

Valores permitidos:

```text
S
N
```

---

## 4.7. dw.DIM_PROMOCAO

### RN-PROM-001: Identificação única da promoção

Cada promoção deve possuir `ID_PROMOCAO_ORIGEM` único.

### RN-PROM-002: Nome da promoção obrigatório

A coluna `NOME_PROMOCAO` deve estar preenchida.

### RN-PROM-003: Vigência da promoção

A data final da promoção deve ser maior ou igual à data inicial.

Regra:

```text
DATA_FIM_PROMOCAO >= DATA_INICIO_PROMOCAO
```

### RN-PROM-004: Percentual de desconto

Quando informado, `PERCENTUAL_DESCONTO` deve estar entre 0 e 100.

### RN-PROM-005: Valor de desconto

Quando informado, `VALOR_DESCONTO` deve ser maior ou igual a zero.

### RN-PROM-006: Promoção ativa

A coluna `FL_PROMOCAO_ATIVA` deve aceitar apenas:

```text
S
N
```

---

## 4.8. dw.DIM_SAZONALIDADE

### RN-SAZ-001: Identificação única da sazonalidade

Cada sazonalidade deve possuir `ID_SAZONALIDADE_ORIGEM` único.

### RN-SAZ-002: Nome da sazonalidade obrigatório

A coluna `NOME_SAZONALIDADE` deve estar preenchida.

### RN-SAZ-003: Período da sazonalidade

A data final deve ser maior ou igual à data inicial.

Regra:

```text
DATA_FIM >= DATA_INICIO
```

### RN-SAZ-004: Recorrência

A coluna `FL_RECORRENTE` deve indicar se a sazonalidade é recorrente.

Valores permitidos:

```text
S
N
```

### RN-SAZ-005: Status da sazonalidade

A coluna `FL_ATIVO` deve aceitar apenas:

```text
S
N
```

---

## 4.9. dw.DIM_TEMPO

### RN-TMP-001: Chave da data

A coluna `SK_TEMPO` deve seguir o formato numérico `YYYYMMDD`.

Exemplo:

```text
20260630
```

### RN-TMP-002: Data única

A coluna `DATA_COMPLETA` deve ser única.

### RN-TMP-003: Dia válido

A coluna `DIA` deve conter valor entre 1 e 31.

### RN-TMP-004: Mês válido

A coluna `MES` deve conter valor entre 1 e 12.

### RN-TMP-005: Trimestre válido

A coluna `TRIMESTRE` deve conter valor entre 1 e 4.

### RN-TMP-006: Semestre válido

A coluna `SEMESTRE` deve conter valor entre 1 e 2.

### RN-TMP-007: Fim de semana

A coluna `FL_FIM_SEMANA` deve aceitar apenas:

```text
S
N
```

### RN-TMP-008: Feriado

A coluna `FL_FERIADO` deve aceitar apenas:

```text
S
N
```

Quando `FL_FERIADO = 'S'`, recomenda-se preencher `NOME_FERIADO`.

---

## 4.10. dw.DIM_PRODUTORUPTURA

### RN-RUPDIM-001: Identificação única da classificação de ruptura

Cada motivo, tipo ou classificação de ruptura deve possuir `ID_RUPTURA_ORIGEM` único.

### RN-RUPDIM-002: Descrição obrigatória

A coluna `DESCRICAO_RUPTURA` deve estar preenchida.

### RN-RUPDIM-003: Tipo de ruptura

A coluna `TIPO_RUPTURA` deve classificar a ruptura.

Exemplos:

```text
Logística
Fornecedor
Demanda
Cadastro
Estoque
```

### RN-RUPDIM-004: Responsável pela ruptura

A coluna `RESPONSAVEL_RUPTURA` deve indicar, quando aplicável, a área ou entidade associada ao evento de ruptura.

Exemplos:

```text
Fornecedor
Loja
Centro de Distribuição
Comercial
Cadastro
```

### RN-RUPDIM-005: Status da classificação

A coluna `FL_ATIVO` deve aceitar apenas:

```text
S
N
```

---

## 4.11. dw.DIM_LOJA

### RN-LOJ-001: Identificação única da loja

Cada loja deve possuir `ID_LOJA_ORIGEM` único.

### RN-LOJ-002: Nome da loja obrigatório

A coluna `NOME_LOJA` deve estar preenchida.

### RN-LOJ-003: Unidade federativa

Quando informado, o campo `ESTADO` deve conter a sigla da unidade federativa com dois caracteres.

### RN-LOJ-004: País padrão

Quando não houver país informado, o valor padrão deve ser:

```text
Brasil
```

### RN-LOJ-005: Status da loja

A coluna `FL_ATIVO` deve aceitar apenas:

```text
S
N
```

---

## 4.12. dw.DIM_CANALVENDA

### RN-CAN-001: Identificação única do canal de venda

Cada canal de venda deve possuir `ID_CANALVENDA_ORIGEM` único.

### RN-CAN-002: Nome do canal obrigatório

A coluna `NOME_CANALVENDA` deve estar preenchida.

### RN-CAN-003: Tipo do canal

A coluna `TIPO_CANAL` deve classificar o canal de venda.

Exemplos:

```text
Físico
Digital
Marketplace
Parceiro
Atacado
```

### RN-CAN-004: Status do canal

A coluna `FL_ATIVO` deve aceitar apenas:

```text
S
N
```

---

## 5. Regras de Negócio das Tabelas Fato

## 5.1. dw.FATO_VENDAS

### RN-VND-001: Grão da tabela

A tabela `dw.FATO_VENDAS` deve armazenar uma linha por item de venda.

Quando uma venda possuir múltiplos itens, cada item deve gerar uma linha na fato.

### RN-VND-002: Venda obrigatória

A coluna `ID_VENDA_ORIGEM` deve estar preenchida.

### RN-VND-003: Produto obrigatório

Toda linha da fato de vendas deve possuir `SK_PRODUTO` válido.

### RN-VND-004: Tempo obrigatório

Toda linha da fato de vendas deve possuir `SK_TEMPO` válido.

### RN-VND-005: Quantidade não negativa

A coluna `QUANTIDADE` deve ser maior ou igual a zero.

### RN-VND-006: Valor unitário não negativo

A coluna `VALOR_UNITARIO` deve ser maior ou igual a zero.

### RN-VND-007: Valor bruto não negativo

A coluna `VALOR_BRUTO` deve ser maior ou igual a zero.

### RN-VND-008: Valor de desconto não negativo

A coluna `VALOR_DESCONTO` deve ser maior ou igual a zero.

### RN-VND-009: Valor líquido não negativo

A coluna `VALOR_LIQUIDO` deve ser maior ou igual a zero.

### RN-VND-010: Custo total

Quando informado, `CUSTO_TOTAL` deve ser maior ou igual a zero.

### RN-VND-011: Margem bruta

A margem bruta pode ser calculada como:

```text
MARGEM_BRUTA = VALOR_LIQUIDO - CUSTO_TOTAL
```

Essa regra deve ser aplicada quando houver custo disponível.

### RN-VND-012: Valor líquido esperado

Quando não houver acréscimos, frete, juros ou impostos adicionais, recomenda-se validar:

```text
VALOR_LIQUIDO = VALOR_BRUTO - VALOR_DESCONTO
```

### RN-VND-013: Dimensões derivadas do produto

As colunas abaixo podem ser derivadas da dimensão produto durante a carga:

```text
SK_CATEGORIA
SK_MARCA
SK_FORNECEDOR
```

Essa desnormalização é permitida para facilitar consultas analíticas.

### RN-VND-014: Promoção opcional

`SK_PROMOCAO` pode ser nula quando a venda não possuir promoção associada.

### RN-VND-015: Cliente opcional

`SK_CLIENTE` pode ser nula quando a venda não estiver associada a um cliente identificado.

---

## 5.2. dw.FATO_ESTOQUE

### RN-EST-001: Grão da tabela

A tabela `dw.FATO_ESTOQUE` deve armazenar uma linha por produto, loja e data de referência.

### RN-EST-002: Produto obrigatório

Toda posição de estoque deve possuir `SK_PRODUTO` válido.

### RN-EST-003: Loja obrigatória

Toda posição de estoque deve possuir `SK_LOJA` válido.

### RN-EST-004: Tempo obrigatório

Toda posição de estoque deve possuir `SK_TEMPO` válido.

### RN-EST-005: Data de referência obrigatória

A coluna `DATA_REFERENCIA_ESTOQUE` deve estar preenchida.

### RN-EST-006: Quantidades não negativas

As colunas abaixo devem ser maiores ou iguais a zero:

```text
QTD_ESTOQUE_DISPONIVEL
QTD_ESTOQUE_RESERVADO
QTD_ESTOQUE_BLOQUEADO
QTD_ESTOQUE_TRANSITO
QTD_ESTOQUE_TOTAL
```

### RN-EST-007: Quantidades parametrizadas

As colunas abaixo devem ser maiores ou iguais a zero quando informadas:

```text
QTD_ESTOQUE_MINIMO
QTD_ESTOQUE_MAXIMO
QTD_PONTO_REPOSICAO
```

### RN-EST-008: Cálculo do estoque total

Recomenda-se calcular ou validar o estoque total como:

```text
QTD_ESTOQUE_TOTAL = QTD_ESTOQUE_DISPONIVEL + QTD_ESTOQUE_RESERVADO + QTD_ESTOQUE_BLOQUEADO + QTD_ESTOQUE_TRANSITO
```

### RN-EST-009: Valor de estoque a custo

Quando houver custo unitário disponível, recomenda-se calcular:

```text
VALOR_ESTOQUE_CUSTO = QTD_ESTOQUE_TOTAL * CUSTO_UNITARIO
```

### RN-EST-010: Valor potencial de estoque a venda

Quando houver preço de venda disponível, recomenda-se calcular:

```text
VALOR_ESTOQUE_VENDA = QTD_ESTOQUE_TOTAL * PRECO_LISTA
```

### RN-EST-011: Flag de ruptura

A coluna `FL_RUPTURA` deve indicar se o produto está em ruptura na loja e data analisadas.

Regra sugerida:

```text
FL_RUPTURA = 'S' quando QTD_ESTOQUE_DISPONIVEL = 0
FL_RUPTURA = 'N' quando QTD_ESTOQUE_DISPONIVEL > 0
```

### RN-EST-012: Flag de estoque baixo

A coluna `FL_ESTOQUE_BAIXO` deve indicar se o estoque disponível está abaixo do ponto mínimo ou ponto de reposição.

Regra sugerida:

```text
FL_ESTOQUE_BAIXO = 'S' quando QTD_ESTOQUE_DISPONIVEL <= QTD_PONTO_REPOSICAO
```

### RN-EST-013: Flag de excesso de estoque

A coluna `FL_EXCESSO_ESTOQUE` deve indicar se o estoque total excede o estoque máximo definido.

Regra sugerida:

```text
FL_EXCESSO_ESTOQUE = 'S' quando QTD_ESTOQUE_TOTAL > QTD_ESTOQUE_MAXIMO
```

### RN-EST-014: Integridade do grão

Não deve existir mais de uma linha para a mesma combinação:

```text
SK_PRODUTO
SK_LOJA
SK_TEMPO
```

---

## 5.3. dw.FATO_RUPTURA_ESTOQUE

### RN-RUP-001: Grão da tabela

A tabela `dw.FATO_RUPTURA_ESTOQUE` deve armazenar uma linha por evento de ruptura de produto, loja e data.

### RN-RUP-002: Produto obrigatório

Todo evento de ruptura deve possuir `SK_PRODUTO` válido.

### RN-RUP-003: Loja obrigatória

Todo evento de ruptura deve possuir `SK_LOJA` válido.

### RN-RUP-004: Tempo obrigatório

Todo evento de ruptura deve possuir `SK_TEMPO` válido.

### RN-RUP-005: Motivo de ruptura

Quando disponível, o evento deve estar associado a um motivo ou classificação de ruptura por meio de `SK_MOTIVO_RUPTURA`.

### RN-RUP-006: Quantidades não negativas

As colunas abaixo devem ser maiores ou iguais a zero quando informadas:

```text
QTD_ESTOQUE_ESPERADO
QTD_ESTOQUE_DISPONIVEL
QTD_RUPTURA
```

### RN-RUP-007: Dias de ruptura

Quando informado, `DIAS_RUPTURA` deve ser maior ou igual a zero.

### RN-RUP-008: Venda perdida

Quando informado, `VALOR_VENDA_PERDIDA` deve ser maior ou igual a zero.

### RN-RUP-009: Flag de ruptura

A coluna `FL_RUPTURA` deve aceitar apenas:

```text
S
N
```

### RN-RUP-010: Cálculo da quantidade em ruptura

Quando houver estoque esperado e disponível, pode-se calcular:

```text
QTD_RUPTURA = QTD_ESTOQUE_ESPERADO - QTD_ESTOQUE_DISPONIVEL
```

A quantidade em ruptura não deve ser negativa.

### RN-RUP-011: Estimativa de venda perdida

Quando houver preço médio ou venda média disponível, a venda perdida pode ser estimada por:

```text
VALOR_VENDA_PERDIDA = QTD_RUPTURA * VALOR_MEDIO_VENDA
```

---

## 5.4. dw.FATO_METAS

### RN-MET-001: Grão da tabela

A tabela `dw.FATO_METAS` deve armazenar uma linha por período, loja, canal, produto, categoria, marca e tipo de meta.

### RN-MET-002: Tempo obrigatório

Toda meta deve possuir `SK_TEMPO` válido.

### RN-MET-003: Ano obrigatório

A coluna `ANO` deve estar preenchida.

### RN-MET-004: Mês válido

A coluna `MES` deve conter valor entre 1 e 12.

### RN-MET-005: Ano/mês obrigatório

A coluna `ANO_MES` deve estar preenchida no formato recomendado:

```text
YYYY-MM
```

### RN-MET-006: Tipo de meta

A coluna `TIPO_META` deve aceitar apenas os valores:

```text
FATURAMENTO
VOLUME
MARGEM
TICKET_MEDIO
MISTA
```

### RN-MET-007: Metas de faturamento

As colunas abaixo devem ser maiores ou iguais a zero:

```text
META_FATURAMENTO_BRUTO
META_FATURAMENTO_LIQUIDO
```

### RN-MET-008: Metas quantitativas

As colunas abaixo devem ser maiores ou iguais a zero quando informadas:

```text
META_QTD_VENDAS
META_QTD_ITENS
```

### RN-MET-009: Ticket médio

Quando informado, `META_TICKET_MEDIO` deve ser maior ou igual a zero.

### RN-MET-010: Margem bruta

Quando informada, `META_MARGEM_BRUTA` deve ser maior ou igual a zero.

### RN-MET-011: Percentual de margem

Quando informado, `META_PERCENTUAL_MARGEM` deve estar entre 0 e 100.

### RN-MET-012: Vigência da meta

A data final da meta deve ser maior ou igual à data inicial.

Regra:

```text
DATA_FIM_META >= DATA_INICIO_META
```

### RN-MET-013: Meta ativa

A coluna `FL_META_ATIVA` deve aceitar apenas:

```text
S
N
```

### RN-MET-014: Duplicidade de contexto

Não deve existir mais de uma meta para o mesmo contexto analítico:

```text
ANO_MES
SK_LOJA
SK_CANALVENDA
SK_PRODUTO
SK_CATEGORIA
SK_MARCA
TIPO_META
```

### RN-MET-015: Meta versus realizado

O percentual de atingimento da meta pode ser calculado por:

```text
PERCENTUAL_ATINGIMENTO = FATURAMENTO_REALIZADO / META_FATURAMENTO_LIQUIDO * 100
```

Quando a meta for zero, a divisão deve ser evitada.

---

## 6. Regras das Tabelas Técnicas

## 6.1. dw.CONTROLE_CARGA

### RN-CTRL-001: Registro por carga

Cada execução de carga deve gerar pelo menos um registro em `dw.CONTROLE_CARGA`.

### RN-CTRL-002: Processo obrigatório

A coluna `NOME_PROCESSO` deve estar preenchida.

### RN-CTRL-003: Tabela obrigatória

A coluna `NOME_TABELA` deve estar preenchida.

### RN-CTRL-004: Camada válida

A coluna `CAMADA_DADOS` deve aceitar apenas:

```text
ORIGEM
STAGING
BRONZE
SILVER
GOLD
DW
```

### RN-CTRL-005: Tipo de carga válido

A coluna `TIPO_CARGA` deve aceitar apenas:

```text
FULL
INCREMENTAL
REPROCESSAMENTO
MANUAL
```

### RN-CTRL-006: Status de carga válido

A coluna `STATUS_CARGA` deve aceitar apenas:

```text
INICIADO
EM_EXECUCAO
SUCESSO
ERRO
CANCELADO
REPROCESSADO
```

### RN-CTRL-007: Datas da carga

Quando preenchida, `DATA_FIM_CARGA` deve ser maior ou igual a `DATA_INICIO_CARGA`.

### RN-CTRL-008: Watermark

Quando utilizados, `WATERMARK_FIM` deve ser maior ou igual a `WATERMARK_INICIO`.

### RN-CTRL-009: Volumetria não negativa

As colunas abaixo devem ser maiores ou iguais a zero:

```text
QTD_LINHAS_LIDAS
QTD_LINHAS_GRAVADAS
QTD_LINHAS_ATUALIZADAS
QTD_LINHAS_REJEITADAS
```

### RN-CTRL-010: Atualização do último processamento

A coluna `ULTIMA_DATA_PROCESSADA` deve ser atualizada somente quando a carga terminar com sucesso.

---

## 6.2. dw.LOG_EXECUCAO

### RN-LOG-001: Registro por evento

Cada etapa relevante do pipeline deve gerar um registro em `dw.LOG_EXECUCAO`.

### RN-LOG-002: Processo obrigatório

A coluna `NOME_PROCESSO` deve estar preenchida.

### RN-LOG-003: Etapa obrigatória

A coluna `NOME_ETAPA` deve estar preenchida.

### RN-LOG-004: Tipo de evento válido

A coluna `TIPO_EVENTO` deve aceitar apenas:

```text
INICIO
FIM
INFO
ALERTA
ERRO
VALIDACAO
MERGE
INSERT
UPDATE
DELETE
```

### RN-LOG-005: Status de evento válido

A coluna `STATUS_EVENTO` deve aceitar apenas:

```text
INICIADO
EM_EXECUCAO
SUCESSO
ERRO
ALERTA
CANCELADO
```

### RN-LOG-006: Datas do evento

Quando preenchida, `DATA_FIM_EVENTO` deve ser maior ou igual a `DATA_INICIO_EVENTO`.

### RN-LOG-007: Duração não negativa

Quando informada, `DURACAO_SEGUNDOS` deve ser maior ou igual a zero.

### RN-LOG-008: Volumetria não negativa

As colunas abaixo devem ser maiores ou iguais a zero:

```text
QTD_LINHAS_PROCESSADAS
QTD_LINHAS_INSERIDAS
QTD_LINHAS_ATUALIZADAS
QTD_LINHAS_EXCLUIDAS
QTD_LINHAS_REJEITADAS
```

### RN-LOG-009: Registro de erro

Quando `STATUS_EVENTO = 'ERRO'`, recomenda-se preencher:

```text
CODIGO_ERRO
MENSAGEM_ERRO
```

---

## 7. Regras de Qualidade de Dados

## 7.1. Integridade referencial

Todas as chaves estrangeiras das tabelas fato devem apontar para registros válidos nas dimensões correspondentes.

## 7.2. Registros não identificados

Recomenda-se criar registros técnicos nas dimensões para representar situações como:

```text
Não informado
Não aplicável
Não identificado
```

Padrão sugerido:

```text
-1 = Não informado
-2 = Não aplicável
-3 = Não identificado
```

## 7.3. Campos monetários

Campos monetários não devem receber valores negativos, exceto em cenários específicos de devolução, estorno ou ajuste financeiro, caso sejam modelados futuramente.

## 7.4. Campos quantitativos

Campos quantitativos devem ser maiores ou iguais a zero, exceto quando houver regra específica de ajuste, devolução ou inventário negativo.

## 7.5. Datas de fim

Datas de fim de vigência, promoção, sazonalidade, meta, carga ou evento não devem ser menores que as respectivas datas de início.

## 7.6. Duplicidade em fatos

Deve ser evitada duplicidade no grão das tabelas fato.

Exemplos:

```text
FATO_ESTOQUE: SK_PRODUTO + SK_LOJA + SK_TEMPO
FATO_METAS: ANO_MES + SK_LOJA + SK_CANALVENDA + SK_PRODUTO + SK_CATEGORIA + SK_MARCA + TIPO_META
FATO_VENDAS: ID_VENDA_ORIGEM + ID_ITEM_VENDA_ORIGEM
```

## 7.7. Campos obrigatórios

Campos definidos como obrigatórios no modelo devem ser validados durante os processos de carga.

Registros inválidos devem ser:

- Rejeitados.
- Corrigidos antes da carga.
- Direcionados para tabela de erro ou log.

---

## 8. Regras de Carga

## 8.1. Ordem de carga recomendada

A ordem de carga deve respeitar as dependências entre dimensões e fatos.

Ordem sugerida:

```text
1. DIM_CATEGORIA
2. DIM_MARCA
3. DIM_FORNECEDOR
4. DIM_PRODUTO
5. DIM_CLIENTE
6. DIM_FORMAPAGTO
7. DIM_PROMOCAO
8. DIM_SAZONALIDADE
9. DIM_TEMPO
10. DIM_PRODUTORUPTURA
11. DIM_LOJA
12. DIM_CANALVENDA
13. FATO_VENDAS
14. FATO_ESTOQUE
15. FATO_RUPTURA_ESTOQUE
16. FATO_METAS
17. CONTROLE_CARGA
18. LOG_EXECUCAO
```

## 8.2. Cargas dimensionais

Dimensões sem controle histórico podem ser carregadas com estratégia de sobrescrita controlada ou merge.

Dimensões com controle histórico devem aplicar lógica SCD Tipo 2 quando houver mudança em atributos relevantes.

## 8.3. Cargas fato

Tabelas fato devem ser carregadas após as dimensões correspondentes estarem disponíveis.

Antes da carga da fato, devem ser resolvidas as surrogate keys das dimensões.

## 8.4. Carga incremental

Cargas incrementais devem utilizar campos de controle, como:

```text
DATA_ATUALIZACAO_DW
DATA_CARGA
DATA_HORA_VENDA
WATERMARK_INICIO
WATERMARK_FIM
ULTIMA_DATA_PROCESSADA
```

## 8.5. Reprocessamento

Todo reprocessamento deve ser registrado na tabela `dw.CONTROLE_CARGA` com `TIPO_CARGA = 'REPROCESSAMENTO'` ou `STATUS_CARGA = 'REPROCESSADO'`, conforme o caso.

## 8.6. Logs de execução

Cada etapa relevante do processo deve gerar registros em `dw.LOG_EXECUCAO`.

Exemplos de etapas:

```text
EXTRACAO
VALIDACAO
TRANSFORMACAO
MERGE
INSERT
FINALIZACAO
ERRO
```

---

## 9. Regras Analíticas

## 9.1. Faturamento bruto

O faturamento bruto deve ser calculado pela soma de `VALOR_BRUTO`.

```text
FATURAMENTO_BRUTO = SUM(VALOR_BRUTO)
```

## 9.2. Faturamento líquido

O faturamento líquido deve ser calculado pela soma de `VALOR_LIQUIDO`.

```text
FATURAMENTO_LIQUIDO = SUM(VALOR_LIQUIDO)
```

## 9.3. Desconto total

O desconto total deve ser calculado pela soma de `VALOR_DESCONTO`.

```text
DESCONTO_TOTAL = SUM(VALOR_DESCONTO)
```

## 9.4. Ticket médio

O ticket médio pode ser calculado por:

```text
TICKET_MEDIO = SUM(VALOR_LIQUIDO) / COUNT(DISTINCT ID_VENDA_ORIGEM)
```

## 9.5. Quantidade de vendas

A quantidade de vendas deve considerar vendas distintas.

```text
QTD_VENDAS = COUNT(DISTINCT ID_VENDA_ORIGEM)
```

## 9.6. Quantidade de itens vendidos

A quantidade de itens vendidos deve ser calculada por:

```text
QTD_ITENS = SUM(QUANTIDADE)
```

## 9.7. Margem bruta

A margem bruta pode ser calculada por:

```text
MARGEM_BRUTA = SUM(VALOR_LIQUIDO) - SUM(CUSTO_TOTAL)
```

## 9.8. Percentual de margem

O percentual de margem pode ser calculado por:

```text
PERCENTUAL_MARGEM = SUM(MARGEM_BRUTA) / SUM(VALOR_LIQUIDO) * 100
```

## 9.9. Valor de estoque a custo

O valor do estoque a custo pode ser calculado por:

```text
VALOR_ESTOQUE_CUSTO = SUM(VALOR_ESTOQUE_CUSTO)
```

## 9.10. Percentual de atingimento de meta

O percentual de atingimento de meta pode ser calculado por:

```text
PERCENTUAL_ATINGIMENTO = FATURAMENTO_REALIZADO / META_FATURAMENTO_LIQUIDO * 100
```

Quando `META_FATURAMENTO_LIQUIDO = 0`, a divisão deve ser evitada.

---

## 10. Observações Finais

Este documento deve ser revisado sempre que houver alteração no modelo dimensional, inclusão de novas tabelas, mudança de regras de carga ou alteração em indicadores de negócio.

As regras aqui descritas devem ser utilizadas como referência para:

- Desenvolvimento de pipelines de carga.
- Implementação de validações de qualidade de dados.
- Criação de consultas analíticas.
- Construção de dashboards.
- Documentação do repositório do projeto.
