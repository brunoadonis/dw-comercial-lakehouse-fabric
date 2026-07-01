# Estratégia Incremental

## Projeto: Data Warehouse Comercial

## 1. Objetivo

Este documento descreve a estratégia de carga incremental adotada para o Data Warehouse Comercial.

O objetivo é definir como os dados devem ser extraídos, tratados, carregados, atualizados, auditados e reprocessados nas tabelas dimensionais, tabelas fato e tabelas técnicas do modelo.

A estratégia incremental foi desenhada para reduzir recargas completas, melhorar performance, permitir rastreabilidade e aproximar o projeto de um cenário real de Engenharia de Dados.

---

## 2. Escopo

A estratégia incremental se aplica aos seguintes grupos de tabelas:

```text
Dimensões
Fatos
Tabelas técnicas de controle
Tabelas técnicas de log
```

Tabelas contempladas:

```text
dw.DIM_CATEGORIA
dw.DIM_MARCA
dw.DIM_FORNECEDOR
dw.DIM_PRODUTO
dw.DIM_CLIENTE
dw.DIM_FORMAPAGTO
dw.DIM_PROMOCAO
dw.DIM_SAZONALIDADE
dw.DIM_TEMPO
dw.DIM_PRODUTORUPTURA
dw.DIM_LOJA
dw.DIM_CANALVENDA

dw.FATO_VENDAS
dw.FATO_ESTOQUE
dw.FATO_RUPTURA_ESTOQUE
dw.FATO_METAS

dw.CONTROLE_CARGA
dw.LOG_EXECUCAO
```

---

## 3. Conceitos Utilizados

## 3.1. Carga Full

Carga full é o processo em que todos os dados de uma tabela são processados novamente.

Esse tipo de carga pode ser utilizado em cenários como:

- Primeira carga do ambiente.
- Reprocessamento completo.
- Correção estrutural de dados.
- Baixo volume de dados.
- Tabelas pequenas de domínio.

## 3.2. Carga Incremental

Carga incremental é o processo em que apenas registros novos ou alterados desde a última execução bem-sucedida são processados.

Esse tipo de carga reduz o volume processado e melhora a eficiência do pipeline.

## 3.3. Watermark

Watermark é o valor de controle utilizado para identificar o intervalo de dados que deve ser processado em uma carga incremental.

Exemplos de colunas utilizadas como watermark:

```text
DATA_ATUALIZACAO_DW
DATA_CARGA
DATA_HORA_VENDA
DATA_REFERENCIA_ESTOQUE
DATA_INICIO_META
DATA_FIM_META
```

## 3.4. Controle de Carga

A tabela `dw.CONTROLE_CARGA` deve armazenar o status de cada carga e os valores de watermark utilizados.

## 3.5. Log de Execução

A tabela `dw.LOG_EXECUCAO` deve armazenar eventos detalhados de cada etapa do processo.

---

## 4. Princípios da Estratégia Incremental

A estratégia incremental do projeto segue os seguintes princípios:

- Processar apenas dados novos ou alterados.
- Registrar início e fim de cada carga.
- Armazenar watermarks utilizados em cada execução.
- Registrar quantidade de linhas lidas, gravadas, atualizadas e rejeitadas.
- Permitir reprocessamento controlado.
- Evitar duplicidade no grão das tabelas fato.
- Preservar histórico em dimensões com SCD Tipo 2.
- Garantir rastreabilidade entre origem, DW e processos de carga.

---

## 5. Tabela de Controle de Carga

A tabela `dw.CONTROLE_CARGA` deve ser utilizada para armazenar o estado geral das cargas.

Campos principais:

```text
ID_CONTROLE_CARGA
NOME_PROCESSO
NOME_PIPELINE
NOME_TABELA
CAMADA_DADOS
TIPO_CARGA
STATUS_CARGA
DATA_INICIO_CARGA
DATA_FIM_CARGA
WATERMARK_INICIO
WATERMARK_FIM
ULTIMA_DATA_PROCESSADA
QTD_LINHAS_LIDAS
QTD_LINHAS_GRAVADAS
QTD_LINHAS_ATUALIZADAS
QTD_LINHAS_REJEITADAS
ID_EXECUCAO
MENSAGEM_ERRO
```

## 5.1. Status previstos

```text
INICIADO
EM_EXECUCAO
SUCESSO
ERRO
CANCELADO
REPROCESSADO
```

## 5.2. Tipos de carga previstos

```text
FULL
INCREMENTAL
REPROCESSAMENTO
MANUAL
```

---

## 6. Tabela de Log de Execução

A tabela `dw.LOG_EXECUCAO` deve ser utilizada para registrar eventos detalhados das etapas do pipeline.

Exemplos de eventos:

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

Exemplos de etapas:

```text
EXTRACAO
VALIDACAO_DADOS
RESOLUCAO_CHAVES
CARGA_DIMENSAO
CARGA_FATO
MERGE
FINALIZACAO
TRATAMENTO_ERRO
```

---

## 7. Estratégia Incremental para Dimensões

## 7.1. Dimensões de domínio simples

Dimensões de domínio simples possuem menor volume e baixa frequência de alteração.

Tabelas:

```text
dw.DIM_CATEGORIA
dw.DIM_MARCA
dw.DIM_FORNECEDOR
dw.DIM_FORMAPAGTO
dw.DIM_PROMOCAO
dw.DIM_SAZONALIDADE
dw.DIM_PRODUTORUPTURA
dw.DIM_LOJA
dw.DIM_CANALVENDA
```

### Estratégia recomendada

Utilizar `MERGE` baseado na chave de origem.

Chaves de origem:

```text
ID_CATEGORIA_ORIGEM
ID_MARCA_ORIGEM
ID_FORNECEDOR_ORIGEM
ID_FORMAPAGTO_ORIGEM
ID_PROMOCAO_ORIGEM
ID_SAZONALIDADE_ORIGEM
ID_RUPTURA_ORIGEM
ID_LOJA_ORIGEM
ID_CANALVENDA_ORIGEM
```

### Regra

- Se o registro não existir na dimensão, inserir.
- Se o registro existir e houver alteração em atributos relevantes, atualizar.
- Se não houver alteração, não executar ação.

### Tipo de histórico

Essas dimensões podem ser tratadas inicialmente como SCD Tipo 1, sobrescrevendo atributos alterados.

---

## 7.2. Dimensões com histórico SCD Tipo 2

Dimensões com histórico devem preservar versões anteriores dos registros.

Tabelas:

```text
dw.DIM_PRODUTO
dw.DIM_CLIENTE
```

### Estratégia recomendada

Utilizar SCD Tipo 2 com fechamento da versão anterior e inserção de nova versão.

Campos de controle histórico:

```text
DATA_INICIO_VIGENCIA
DATA_FIM_VIGENCIA
FL_REGISTRO_ATUAL
```

### Regra

Quando houver alteração em atributo rastreado:

1. Localizar o registro atual pela chave de origem.
2. Atualizar o registro atual, preenchendo `DATA_FIM_VIGENCIA`.
3. Alterar `FL_REGISTRO_ATUAL` para `N`.
4. Inserir uma nova versão com `FL_REGISTRO_ATUAL = 'S'`.
5. Preencher `DATA_INICIO_VIGENCIA` com a data da alteração ou data da carga.

### Atributos candidatos a histórico em `dw.DIM_PRODUTO`

```text
SK_CATEGORIA
SK_MARCA
SK_FORNECEDOR
NOME_PRODUTO
DESCRICAO_PRODUTO
UNIDADE_MEDIDA
CUSTO_UNITARIO
PRECO_LISTA
FL_PERECIVEL
FL_ATIVO
```

### Atributos candidatos a histórico em `dw.DIM_CLIENTE`

```text
TIPO_CLIENTE
CIDADE
ESTADO
PAIS
SEGMENTO_CLIENTE
FL_ATIVO
```

---

## 7.3. Dimensão Tempo

Tabela:

```text
dw.DIM_TEMPO
```

### Estratégia recomendada

A `DIM_TEMPO` deve ser carregada previamente por período fechado, preferencialmente por carga full controlada.

Exemplo de período recomendado para o projeto:

```text
2024-01-01 até 2026-12-31
```

### Regra

- A chave `SK_TEMPO` deve seguir o formato `YYYYMMDD`.
- A coluna `DATA_COMPLETA` deve ser única.
- A tabela deve ser carregada antes das tabelas fato.

---

## 8. Estratégia Incremental para Fatos

## 8.1. dw.FATO_VENDAS

### Grão

Uma linha por item de venda.

### Chave de negócio sugerida

```text
ID_VENDA_ORIGEM + ID_ITEM_VENDA_ORIGEM
```

### Watermark sugerido

```text
DATA_HORA_VENDA
DATA_ATUALIZACAO_DW
```

### Estratégia recomendada

Utilizar carga incremental com `MERGE` pela chave de negócio.

### Regras

- Inserir novos itens de venda.
- Atualizar itens já existentes quando houver alteração nos valores ou dimensões associadas.
- Evitar duplicidade por `ID_VENDA_ORIGEM` e `ID_ITEM_VENDA_ORIGEM`.
- Resolver todas as surrogate keys antes de carregar a fato.
- Registros sem dimensão obrigatória devem ser rejeitados ou associados a membro técnico.

### Dimensões obrigatórias

```text
SK_TEMPO
SK_PRODUTO
```

### Dimensões opcionais

```text
SK_CLIENTE
SK_CATEGORIA
SK_MARCA
SK_FORNECEDOR
SK_FORMAPAGTO
SK_PROMOCAO
SK_LOJA
SK_CANALVENDA
```

---

## 8.2. dw.FATO_ESTOQUE

### Grão

Uma linha por produto, loja e data.

### Chave de negócio sugerida

```text
SK_PRODUTO + SK_LOJA + SK_TEMPO
```

### Watermark sugerido

```text
DATA_REFERENCIA_ESTOQUE
DATA_ATUALIZACAO_DW
```

### Estratégia recomendada

Utilizar carga incremental por data de referência.

### Regras

- Carregar apenas posições de estoque novas ou alteradas.
- Garantir unicidade por produto, loja e tempo.
- Quando uma posição já existir para o mesmo produto, loja e data, atualizar os valores.
- Quando não existir, inserir nova posição.
- Calcular ou validar flags operacionais durante a carga.

### Flags calculáveis

```text
FL_RUPTURA
FL_ESTOQUE_BAIXO
FL_EXCESSO_ESTOQUE
```

### Regras de cálculo sugeridas

```text
FL_RUPTURA = 'S' quando QTD_ESTOQUE_DISPONIVEL = 0
FL_ESTOQUE_BAIXO = 'S' quando QTD_ESTOQUE_DISPONIVEL <= QTD_PONTO_REPOSICAO
FL_EXCESSO_ESTOQUE = 'S' quando QTD_ESTOQUE_TOTAL > QTD_ESTOQUE_MAXIMO
```

---

## 8.3. dw.FATO_RUPTURA_ESTOQUE

### Grão

Uma linha por evento de ruptura de produto, loja e data.

### Chave de negócio sugerida

```text
ID_RUPTURA_ORIGEM
```

Quando `ID_RUPTURA_ORIGEM` não estiver disponível, pode-se utilizar uma chave composta:

```text
SK_PRODUTO + SK_LOJA + SK_TEMPO + SK_MOTIVO_RUPTURA
```

### Watermark sugerido

```text
DATA_CARGA
DATA_ATUALIZACAO_DW
```

### Estratégia recomendada

Utilizar carga incremental baseada em eventos novos ou alterados.

### Regras

- Inserir novos eventos de ruptura.
- Atualizar eventos existentes quando houver alteração de quantidade, dias em ruptura ou valor perdido.
- Associar o evento a produto, loja, tempo e motivo de ruptura quando disponível.
- Não permitir valores negativos nas métricas de ruptura.

---

## 8.4. dw.FATO_METAS

### Grão

Uma linha por período, loja, canal, produto, categoria, marca e tipo de meta.

### Chave de negócio sugerida

```text
ANO_MES + SK_LOJA + SK_CANALVENDA + SK_PRODUTO + SK_CATEGORIA + SK_MARCA + TIPO_META
```

### Watermark sugerido

```text
DATA_INICIO_META
DATA_FIM_META
DATA_ATUALIZACAO_DW
```

### Estratégia recomendada

Utilizar `MERGE` por contexto da meta.

### Regras

- Inserir novas metas.
- Atualizar metas existentes quando houver alteração de valores planejados.
- Evitar duplicidade por contexto de meta.
- Manter `FL_META_ATIVA` atualizado.
- Não permitir metas com valores negativos.

---

## 9. Fluxo Incremental Padrão

O fluxo incremental recomendado é:

```text
1. Iniciar controle de carga
2. Registrar log de início
3. Ler último watermark bem-sucedido
4. Extrair dados novos ou alterados da origem
5. Validar estrutura e regras de qualidade
6. Resolver surrogate keys das dimensões
7. Executar MERGE ou INSERT na tabela destino
8. Registrar volumetria processada
9. Atualizar watermark final
10. Atualizar status da carga para SUCESSO
11. Registrar log de finalização
```

Em caso de erro:

```text
1. Registrar erro em LOG_EXECUCAO
2. Atualizar CONTROLE_CARGA com STATUS_CARGA = 'ERRO'
3. Armazenar MENSAGEM_ERRO
4. Não atualizar ULTIMA_DATA_PROCESSADA
5. Permitir reprocessamento posterior
```

---

## 10. Consulta do Último Watermark

Antes de iniciar uma carga incremental, o processo deve consultar a última execução bem-sucedida da tabela alvo.

Exemplo conceitual:

```sql
SELECT
    MAX(ULTIMA_DATA_PROCESSADA) AS ULTIMA_DATA_PROCESSADA
FROM dw.CONTROLE_CARGA
WHERE NOME_TABELA = 'dw.FATO_VENDAS'
  AND STATUS_CARGA = 'SUCESSO';
```

Caso não exista carga anterior bem-sucedida, o processo deve assumir uma carga inicial full ou utilizar uma data inicial padrão.

---

## 11. Registro de Início de Carga

Toda carga deve iniciar com um registro em `dw.CONTROLE_CARGA`.

Exemplo conceitual:

```sql
INSERT INTO dw.CONTROLE_CARGA (
    NOME_PROCESSO,
    NOME_PIPELINE,
    NOME_TABELA,
    CAMADA_DADOS,
    TIPO_CARGA,
    STATUS_CARGA,
    DATA_INICIO_CARGA,
    WATERMARK_INICIO,
    ID_EXECUCAO
)
VALUES (
    'CARGA_FATO_VENDAS',
    'PIPELINE_ORACLE_DW',
    'dw.FATO_VENDAS',
    'DW',
    'INCREMENTAL',
    'INICIADO',
    SYSTIMESTAMP,
    :WATERMARK_INICIO,
    :ID_EXECUCAO
);
```

---

## 12. Registro de Finalização com Sucesso

Ao final de uma carga bem-sucedida, o processo deve atualizar o controle de carga.

Exemplo conceitual:

```sql
UPDATE dw.CONTROLE_CARGA
SET
    STATUS_CARGA = 'SUCESSO',
    DATA_FIM_CARGA = SYSTIMESTAMP,
    WATERMARK_FIM = :WATERMARK_FIM,
    ULTIMA_DATA_PROCESSADA = :WATERMARK_FIM,
    QTD_LINHAS_LIDAS = :QTD_LINHAS_LIDAS,
    QTD_LINHAS_GRAVADAS = :QTD_LINHAS_GRAVADAS,
    QTD_LINHAS_ATUALIZADAS = :QTD_LINHAS_ATUALIZADAS,
    QTD_LINHAS_REJEITADAS = :QTD_LINHAS_REJEITADAS,
    DATA_ATUALIZACAO = SYSTIMESTAMP
WHERE ID_EXECUCAO = :ID_EXECUCAO
  AND NOME_TABELA = :NOME_TABELA;
```

---

## 13. Registro de Erro

Em caso de falha, a carga deve ser marcada como erro.

Exemplo conceitual:

```sql
UPDATE dw.CONTROLE_CARGA
SET
    STATUS_CARGA = 'ERRO',
    DATA_FIM_CARGA = SYSTIMESTAMP,
    MENSAGEM_ERRO = :MENSAGEM_ERRO,
    DATA_ATUALIZACAO = SYSTIMESTAMP
WHERE ID_EXECUCAO = :ID_EXECUCAO
  AND NOME_TABELA = :NOME_TABELA;
```

A coluna `ULTIMA_DATA_PROCESSADA` não deve ser atualizada em cargas com erro.

---

## 14. Estratégia de MERGE

## 14.1. MERGE em dimensões SCD Tipo 1

Para dimensões sem histórico, o `MERGE` deve:

- Atualizar atributos quando houver alteração.
- Inserir registros novos.
- Manter a chave de origem como referência principal para comparação.

Exemplo conceitual:

```sql
MERGE INTO dw.DIM_CATEGORIA d
USING stg_categoria s
ON (d.ID_CATEGORIA_ORIGEM = s.ID_CATEGORIA_ORIGEM)
WHEN MATCHED THEN
    UPDATE SET
        d.NOME_CATEGORIA = s.NOME_CATEGORIA,
        d.NOME_DEPARTAMENTO = s.NOME_DEPARTAMENTO,
        d.FL_ATIVO = s.FL_ATIVO,
        d.DATA_ATUALIZACAO_DW = SYSTIMESTAMP
WHEN NOT MATCHED THEN
    INSERT (
        ID_CATEGORIA_ORIGEM,
        NOME_CATEGORIA,
        NOME_DEPARTAMENTO,
        FL_ATIVO,
        DATA_CARGA
    )
    VALUES (
        s.ID_CATEGORIA_ORIGEM,
        s.NOME_CATEGORIA,
        s.NOME_DEPARTAMENTO,
        s.FL_ATIVO,
        SYSTIMESTAMP
    );
```

## 14.2. MERGE em fatos

Para fatos, o `MERGE` deve usar a chave de negócio ou o grão da tabela.

Exemplo para `dw.FATO_ESTOQUE`:

```sql
MERGE INTO dw.FATO_ESTOQUE d
USING stg_fato_estoque s
ON (
    d.SK_PRODUTO = s.SK_PRODUTO
    AND d.SK_LOJA = s.SK_LOJA
    AND d.SK_TEMPO = s.SK_TEMPO
)
WHEN MATCHED THEN
    UPDATE SET
        d.QTD_ESTOQUE_DISPONIVEL = s.QTD_ESTOQUE_DISPONIVEL,
        d.QTD_ESTOQUE_RESERVADO = s.QTD_ESTOQUE_RESERVADO,
        d.QTD_ESTOQUE_BLOQUEADO = s.QTD_ESTOQUE_BLOQUEADO,
        d.QTD_ESTOQUE_TRANSITO = s.QTD_ESTOQUE_TRANSITO,
        d.QTD_ESTOQUE_TOTAL = s.QTD_ESTOQUE_TOTAL,
        d.FL_RUPTURA = s.FL_RUPTURA,
        d.FL_ESTOQUE_BAIXO = s.FL_ESTOQUE_BAIXO,
        d.FL_EXCESSO_ESTOQUE = s.FL_EXCESSO_ESTOQUE,
        d.DATA_ATUALIZACAO_DW = SYSTIMESTAMP
WHEN NOT MATCHED THEN
    INSERT (
        ID_ESTOQUE_ORIGEM,
        SK_TEMPO,
        SK_PRODUTO,
        SK_LOJA,
        SK_CATEGORIA,
        SK_MARCA,
        SK_FORNECEDOR,
        QTD_ESTOQUE_DISPONIVEL,
        QTD_ESTOQUE_RESERVADO,
        QTD_ESTOQUE_BLOQUEADO,
        QTD_ESTOQUE_TRANSITO,
        QTD_ESTOQUE_TOTAL,
        FL_RUPTURA,
        FL_ESTOQUE_BAIXO,
        FL_EXCESSO_ESTOQUE,
        DATA_REFERENCIA_ESTOQUE,
        DATA_CARGA
    )
    VALUES (
        s.ID_ESTOQUE_ORIGEM,
        s.SK_TEMPO,
        s.SK_PRODUTO,
        s.SK_LOJA,
        s.SK_CATEGORIA,
        s.SK_MARCA,
        s.SK_FORNECEDOR,
        s.QTD_ESTOQUE_DISPONIVEL,
        s.QTD_ESTOQUE_RESERVADO,
        s.QTD_ESTOQUE_BLOQUEADO,
        s.QTD_ESTOQUE_TRANSITO,
        s.QTD_ESTOQUE_TOTAL,
        s.FL_RUPTURA,
        s.FL_ESTOQUE_BAIXO,
        s.FL_EXCESSO_ESTOQUE,
        s.DATA_REFERENCIA_ESTOQUE,
        SYSTIMESTAMP
    );
```

---

## 15. Estratégia SCD Tipo 2

Para dimensões com histórico, o processo deve comparar os atributos rastreados da origem com o registro atual no DW.

### Fluxo lógico

```text
1. Buscar registro atual pela chave de origem.
2. Comparar atributos rastreados.
3. Se não houver alteração, não executar ação.
4. Se houver alteração, fechar versão atual.
5. Inserir nova versão.
```

### Fechamento da versão atual

```sql
UPDATE dw.DIM_PRODUTO
SET
    DATA_FIM_VIGENCIA = :DATA_ALTERACAO,
    FL_REGISTRO_ATUAL = 'N',
    DATA_ATUALIZACAO_DW = SYSTIMESTAMP
WHERE ID_PRODUTO_ORIGEM = :ID_PRODUTO_ORIGEM
  AND FL_REGISTRO_ATUAL = 'S';
```

### Inserção da nova versão

```sql
INSERT INTO dw.DIM_PRODUTO (
    ID_PRODUTO_ORIGEM,
    SK_CATEGORIA,
    SK_MARCA,
    SK_FORNECEDOR,
    NOME_PRODUTO,
    DESCRICAO_PRODUTO,
    CODIGO_BARRAS,
    SKU,
    UNIDADE_MEDIDA,
    CUSTO_UNITARIO,
    PRECO_LISTA,
    FL_PERECIVEL,
    FL_ATIVO,
    DATA_INICIO_VIGENCIA,
    DATA_FIM_VIGENCIA,
    FL_REGISTRO_ATUAL,
    DATA_CARGA
)
VALUES (
    :ID_PRODUTO_ORIGEM,
    :SK_CATEGORIA,
    :SK_MARCA,
    :SK_FORNECEDOR,
    :NOME_PRODUTO,
    :DESCRICAO_PRODUTO,
    :CODIGO_BARRAS,
    :SKU,
    :UNIDADE_MEDIDA,
    :CUSTO_UNITARIO,
    :PRECO_LISTA,
    :FL_PERECIVEL,
    :FL_ATIVO,
    :DATA_ALTERACAO,
    NULL,
    'S',
    SYSTIMESTAMP
);
```

---

## 16. Resolução de Surrogate Keys

Antes da carga das tabelas fato, as chaves naturais da origem devem ser convertidas para surrogate keys das dimensões.

Exemplo conceitual para vendas:

```text
ID_PRODUTO_ORIGEM  -> SK_PRODUTO
ID_CLIENTE_ORIGEM  -> SK_CLIENTE
ID_LOJA_ORIGEM     -> SK_LOJA
ID_CANAL_ORIGEM    -> SK_CANALVENDA
DATA_VENDA         -> SK_TEMPO
```

Regras:

- Se a dimensão for obrigatória e a chave não for encontrada, o registro deve ser rejeitado ou direcionado para membro técnico.
- Se a dimensão for opcional, a chave pode permanecer nula ou ser substituída por membro técnico.
- Para dimensões SCD Tipo 2, deve-se localizar a versão vigente na data do evento.

Exemplo de regra para localizar produto vigente:

```sql
SELECT SK_PRODUTO
FROM dw.DIM_PRODUTO
WHERE ID_PRODUTO_ORIGEM = :ID_PRODUTO_ORIGEM
  AND :DATA_EVENTO >= DATA_INICIO_VIGENCIA
  AND (
        DATA_FIM_VIGENCIA IS NULL
        OR :DATA_EVENTO < DATA_FIM_VIGENCIA
      );
```

---

## 17. Tratamento de Registros Não Encontrados

Quando uma chave de dimensão não for encontrada, existem três opções:

```text
1. Rejeitar o registro.
2. Criar o membro técnico "Não identificado".
3. Enviar o registro para uma tabela de rejeição.
```

Para este projeto, recomenda-se criar membros técnicos nas dimensões.

Padrão sugerido:

```text
-1 = Não informado
-2 = Não aplicável
-3 = Não identificado
```

Essa abordagem reduz perda de registros nas fatos e facilita análises posteriores.

---

## 18. Reprocessamento

O reprocessamento deve ser utilizado quando houver necessidade de corrigir falhas, recarregar períodos ou ajustar dados históricos.

### Tipos de reprocessamento

```text
Reprocessamento por tabela
Reprocessamento por período
Reprocessamento por execução
Reprocessamento completo
```

### Regras

- Todo reprocessamento deve ser registrado em `dw.CONTROLE_CARGA`.
- O tipo de carga deve ser `REPROCESSAMENTO`.
- O processo deve registrar os períodos reprocessados.
- O processo deve gerar logs detalhados em `dw.LOG_EXECUCAO`.
- O reprocessamento não deve gerar duplicidade no grão da tabela destino.

---

## 19. Estratégia de Idempotência

Uma carga é considerada idempotente quando pode ser executada mais de uma vez sem gerar duplicidade ou inconsistência.

### Regras de idempotência

- Utilizar `MERGE` em tabelas com possibilidade de atualização.
- Utilizar chaves de negócio ou constraints de unicidade.
- Evitar `INSERT` puro em fatos incrementais sem validação de duplicidade.
- Registrar `ID_EXECUCAO` para rastrear cada execução.
- Não avançar watermark em caso de erro.

---

## 20. Estratégia de Qualidade de Dados

Antes de gravar os dados nas tabelas finais, o processo deve aplicar validações.

### Validações recomendadas

```text
Campos obrigatórios preenchidos
Valores numéricos não negativos
Datas de fim maiores ou iguais às datas de início
Flags com valores válidos
Chaves de dimensão existentes
Ausência de duplicidade no grão da tabela
```

### Registros inválidos

Registros inválidos devem ser tratados de uma das formas abaixo:

```text
Rejeição com log
Correção antes da carga
Associação a membro técnico
Envio para tabela de rejeição
```

---

## 21. Estratégia de Auditoria

Toda carga deve registrar informações mínimas de auditoria.

### Na tabela destino

Campos recomendados:

```text
DATA_CARGA
DATA_ATUALIZACAO_DW
```

### Na tabela de controle

Campos recomendados:

```text
DATA_INICIO_CARGA
DATA_FIM_CARGA
STATUS_CARGA
QTD_LINHAS_LIDAS
QTD_LINHAS_GRAVADAS
QTD_LINHAS_ATUALIZADAS
QTD_LINHAS_REJEITADAS
ULTIMA_DATA_PROCESSADA
```

### Na tabela de log

Campos recomendados:

```text
NOME_PROCESSO
NOME_ETAPA
TIPO_EVENTO
STATUS_EVENTO
DATA_INICIO_EVENTO
DATA_FIM_EVENTO
MENSAGEM_LOG
MENSAGEM_ERRO
```

---

## 22. Periodicidade Recomendada

A periodicidade das cargas pode variar conforme o tipo de dado.

| Tabela | Estratégia | Periodicidade sugerida |
|---|---|---|
| DIM_TEMPO | Full controlada | Sob demanda ou anual |
| DIM_CATEGORIA | Incremental ou merge | Diária ou sob demanda |
| DIM_MARCA | Incremental ou merge | Diária ou sob demanda |
| DIM_FORNECEDOR | Incremental ou merge | Diária ou sob demanda |
| DIM_PRODUTO | Incremental com SCD Tipo 2 | Diária |
| DIM_CLIENTE | Incremental com SCD Tipo 2 | Diária |
| DIM_FORMAPAGTO | Incremental ou merge | Sob demanda |
| DIM_PROMOCAO | Incremental ou merge | Diária |
| DIM_SAZONALIDADE | Incremental ou merge | Sob demanda |
| DIM_PRODUTORUPTURA | Incremental ou merge | Sob demanda |
| DIM_LOJA | Incremental ou merge | Sob demanda |
| DIM_CANALVENDA | Incremental ou merge | Sob demanda |
| FATO_VENDAS | Incremental | Diária ou intradiária |
| FATO_ESTOQUE | Snapshot incremental | Diária |
| FATO_RUPTURA_ESTOQUE | Incremental por evento | Diária ou intradiária |
| FATO_METAS | Incremental ou merge | Mensal ou sob demanda |

---

## 23. Ordem de Execução das Cargas

A ordem de carga deve respeitar as dependências entre dimensões e fatos.

Ordem recomendada:

```text
1. DIM_TEMPO
2. DIM_CATEGORIA
3. DIM_MARCA
4. DIM_FORNECEDOR
5. DIM_PRODUTO
6. DIM_CLIENTE
7. DIM_FORMAPAGTO
8. DIM_PROMOCAO
9. DIM_SAZONALIDADE
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

Observação: `CONTROLE_CARGA` e `LOG_EXECUCAO` são atualizadas durante toda a execução, mas aparecem ao final da lista por representarem tabelas técnicas de apoio.

---

## 24. Estratégia para Primeira Carga

Na primeira execução do projeto, recomenda-se utilizar carga full controlada para popular a base inicial.

### Fluxo recomendado

```text
1. Popular DIM_TEMPO
2. Popular dimensões de domínio
3. Popular dimensões com histórico
4. Popular fatos
5. Registrar cargas em CONTROLE_CARGA
6. Registrar etapas em LOG_EXECUCAO
7. Executar consultas de validação
```

Após a primeira carga, as execuções seguintes devem utilizar estratégia incremental.

---

## 25. Consultas de Validação Pós-Carga

## 25.1. Verificar cargas com erro

```sql
SELECT
    NOME_PROCESSO,
    NOME_TABELA,
    STATUS_CARGA,
    DATA_INICIO_CARGA,
    DATA_FIM_CARGA,
    MENSAGEM_ERRO
FROM dw.CONTROLE_CARGA
WHERE STATUS_CARGA = 'ERRO'
ORDER BY DATA_INICIO_CARGA DESC;
```

## 25.2. Verificar últimos watermarks

```sql
SELECT
    NOME_TABELA,
    MAX(ULTIMA_DATA_PROCESSADA) AS ULTIMA_DATA_PROCESSADA
FROM dw.CONTROLE_CARGA
WHERE STATUS_CARGA = 'SUCESSO'
GROUP BY NOME_TABELA
ORDER BY NOME_TABELA;
```

## 25.3. Verificar eventos de erro no log

```sql
SELECT
    ID_EXECUCAO,
    NOME_PROCESSO,
    NOME_ETAPA,
    NOME_TABELA,
    STATUS_EVENTO,
    CODIGO_ERRO,
    MENSAGEM_ERRO,
    DATA_LOG
FROM dw.LOG_EXECUCAO
WHERE STATUS_EVENTO = 'ERRO'
ORDER BY DATA_LOG DESC;
```

## 25.4. Verificar duplicidade em FATO_ESTOQUE

```sql
SELECT
    SK_PRODUTO,
    SK_LOJA,
    SK_TEMPO,
    COUNT(*) AS QTD_REGISTROS
FROM dw.FATO_ESTOQUE
GROUP BY
    SK_PRODUTO,
    SK_LOJA,
    SK_TEMPO
HAVING COUNT(*) > 1;
```

## 25.5. Verificar produto sem versão atual

```sql
SELECT
    ID_PRODUTO_ORIGEM,
    COUNT(*) AS QTD_ATUAIS
FROM dw.DIM_PRODUTO
WHERE FL_REGISTRO_ATUAL = 'S'
GROUP BY ID_PRODUTO_ORIGEM
HAVING COUNT(*) <> 1;
```

---

## 26. Critérios de Sucesso da Carga

Uma carga será considerada bem-sucedida quando:

- O processo terminar sem erro técnico.
- Todas as regras obrigatórias forem validadas.
- As chaves obrigatórias forem resolvidas.
- Não houver duplicidade no grão da tabela alvo.
- A volumetria estiver registrada em `dw.CONTROLE_CARGA`.
- Os eventos relevantes estiverem registrados em `dw.LOG_EXECUCAO`.
- O watermark for atualizado apenas após sucesso.

---

## 27. Critérios de Falha da Carga

Uma carga será considerada com falha quando ocorrer qualquer uma das situações abaixo:

- Erro técnico no processo.
- Violação de constraint obrigatória.
- Falha na resolução de surrogate key obrigatória.
- Detecção de duplicidade não tratada.
- Erro de conversão de tipo de dado.
- Registros obrigatórios ausentes.
- Falha no `MERGE` ou `INSERT`.

Nesses casos, a carga deve ser marcada como `ERRO` e o watermark não deve ser avançado.

---

## 28. Evoluções Futuras

Evoluções recomendadas para a estratégia incremental:

- Criar tabelas staging por entidade.
- Criar tabela de rejeições para dados inválidos.
- Implementar procedures PL/SQL de carga.
- Implementar jobs agendados.
- Criar tratamento transacional com commit e rollback controlados.
- Implementar hash de comparação para dimensões SCD.
- Implementar particionamento das fatos por `SK_TEMPO`.
- Criar monitoramento de SLA das cargas.
- Criar indicadores de qualidade de dados.
- Integrar o controle incremental com pipelines em Microsoft Fabric.

---

## 29. Conclusão

A estratégia incremental definida neste documento estabelece um padrão de carga confiável, rastreável e escalável para o Data Warehouse Comercial.

Ela permite reduzir volume de processamento, controlar execuções, apoiar reprocessamentos, preservar histórico em dimensões relevantes e garantir maior qualidade nas tabelas fato.

Essa abordagem aproxima o projeto de um cenário real de Engenharia de Dados, conectando modelagem dimensional, controle operacional, governança e boas práticas de pipelines analíticos.
