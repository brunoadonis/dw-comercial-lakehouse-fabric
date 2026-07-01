# Data Quality Rules

## Projeto: DW Comercial Lakehouse com Microsoft Fabric

## 1. Objetivo

Este documento define as regras de qualidade de dados aplicadas ao projeto **DW Comercial Lakehouse com Microsoft Fabric**.

As regras descritas aqui têm como objetivo garantir que os dados carregados nas camadas Bronze, Silver e Gold estejam minimamente consistentes, rastreáveis, íntegros e adequados para a construção de modelos semânticos e dashboards de BI.

A proposta deste projeto é aplicar controles de qualidade de forma proporcional à arquitetura:

```text
Bronze  -> validações técnicas e rastreabilidade da ingestão
Silver  -> padronização, tipagem, nulos obrigatórios e duplicidade
Gold    -> consistência analítica, regras de negócio e indicadores finais
```

---

## 2. Escopo

As regras de qualidade deste documento se aplicam às seguintes camadas:

```text
Raw
Bronze
Silver
Gold
BI
```

E às seguintes entidades do modelo:

```text
Dimensões
Fatos
Tabelas técnicas
KPIs
Marts analíticos
```

Tabelas principais avaliadas:

```text
dim_categoria
dim_marca
dim_fornecedor
dim_produto
dim_cliente
dim_formapagto
dim_promocao
dim_sazonalidade
dim_tempo
dim_produtoruptura
dim_loja
dim_canalvenda
fato_vendas
fato_estoque
fato_ruptura_estoque
fato_metas
controle_carga
log_execucao
```

---

## 3. Princípios de Qualidade de Dados

As regras de qualidade seguem os seguintes princípios:

- Completude: campos obrigatórios devem estar preenchidos.
- Unicidade: registros não devem violar o grão definido da tabela.
- Validade: campos devem respeitar domínios, formatos e tipos esperados.
- Consistência: relacionamentos entre fatos e dimensões devem ser preservados.
- Integridade: chaves estrangeiras devem possuir correspondência nas dimensões.
- Rastreabilidade: cada carga deve permitir identificação da origem e da execução.
- Conformidade analítica: indicadores da Gold devem seguir regras de negócio documentadas.

---

## 4. Severidade das Regras

As regras são classificadas por severidade:

| Severidade | Descrição | Ação recomendada |
|---|---|---|
| Crítica | Impede o uso seguro do dado | Rejeitar registro ou falhar carga |
| Alta | Pode distorcer análises importantes | Corrigir, rejeitar ou enviar para quarentena |
| Média | Afeta qualidade, mas não impede uso controlado | Registrar ocorrência e monitorar |
| Baixa | Problema informativo ou de padronização | Registrar e corrigir em ciclo futuro |

---

## 5. Regras Gerais para Todas as Camadas

## 5.1. DQ-GER-001: Arquivos devem estar disponíveis

**Camada:** Raw  
**Severidade:** Crítica  
**Descrição:** Todos os arquivos esperados devem estar disponíveis no caminho de entrada.

Caminho esperado:

```text
/Files/raw/oracle_dw/<nome_tabela>
```

**Critério de sucesso:** todos os diretórios/tabelas esperados devem existir.  
**Ação em caso de falha:** interromper a carga da tabela ausente e registrar erro no log.

---

## 5.2. DQ-GER-002: Arquivos devem possuir registros

**Camada:** Raw/Bronze  
**Severidade:** Alta  
**Descrição:** Arquivos de entrada não devem estar vazios, exceto quando houver justificativa de negócio.

**Critério de sucesso:** quantidade de linhas maior que zero.  
**Ação em caso de falha:** registrar alerta ou erro, conforme criticidade da tabela.

---

## 5.3. DQ-GER-003: Schema deve conter colunas esperadas

**Camada:** Silver  
**Severidade:** Crítica  
**Descrição:** Cada tabela deve conter as colunas previstas no schema configurado.

**Critério de sucesso:** todas as colunas obrigatórias do schema devem existir.  
**Ação em caso de falha:** falhar processamento da tabela.

---

## 5.4. DQ-GER-004: Tipos de dados devem ser aplicados

**Camada:** Silver  
**Severidade:** Alta  
**Descrição:** Os campos devem ser convertidos para os tipos definidos no schema da Silver.

Exemplos:

```text
SK_*                 -> long
Campos monetários   -> decimal
Campos quantitativos -> decimal
Datas                -> date ou timestamp
Flags                -> string
```

**Critério de sucesso:** colunas convertidas sem perda significativa de registros.  
**Ação em caso de falha:** registrar erro de conversão e rejeitar registros inválidos.

---

## 5.5. DQ-GER-005: Strings vazias devem ser tratadas como nulo

**Camada:** Silver  
**Severidade:** Média  
**Descrição:** Campos vazios em texto devem ser convertidos para `null`.

**Critério de sucesso:** strings vazias não devem permanecer como valor válido.  
**Ação em caso de falha:** aplicar correção automática na Silver.

---

## 5.6. DQ-GER-006: Valores numéricos com vírgula devem ser padronizados

**Camada:** Silver  
**Severidade:** Alta  
**Descrição:** Valores numéricos devem ser padronizados para ponto decimal.

Exemplos:

```text
1.234,56 -> 1234.56
1234,56  -> 1234.56
1234.56  -> 1234.56
```

**Critério de sucesso:** campos monetários e quantitativos devem ser armazenados como decimal.  
**Ação em caso de falha:** registrar erro de conversão.

---

## 6. Regras de Qualidade para Dimensões

## 6.1. DQ-DIM-001: Surrogate key obrigatória

**Camada:** Silver/Gold  
**Severidade:** Crítica  
**Tabelas aplicáveis:** todas as dimensões  
**Descrição:** Toda dimensão deve possuir sua chave técnica preenchida.

Exemplos:

```text
SK_PRODUTO
SK_CLIENTE
SK_LOJA
SK_TEMPO
```

**Critério de sucesso:** nenhum registro da dimensão deve possuir chave técnica nula.  
**Ação em caso de falha:** rejeitar registro.

---

## 6.2. DQ-DIM-002: Chave de origem obrigatória

**Camada:** Silver/Gold  
**Severidade:** Alta  
**Tabelas aplicáveis:** dimensões com campo `ID_..._ORIGEM`  
**Descrição:** A chave natural da origem deve estar preenchida para rastreabilidade.

Exemplos:

```text
ID_PRODUTO_ORIGEM
ID_CLIENTE_ORIGEM
ID_LOJA_ORIGEM
ID_CATEGORIA_ORIGEM
```

**Critério de sucesso:** registros não devem possuir chave de origem nula.  
**Ação em caso de falha:** rejeitar registro ou enviar para quarentena.

---

## 6.3. DQ-DIM-003: Flags devem possuir domínio válido

**Camada:** Silver/Gold  
**Severidade:** Alta  
**Descrição:** Campos de flag devem aceitar apenas valores esperados.

Valores válidos:

```text
S
N
```

Campos aplicáveis:

```text
FL_ATIVO
FL_REGISTRO_ATUAL
FL_PERECIVEL
FL_PROMOCAO_ATIVA
FL_RECORRENTE
FL_FIM_SEMANA
FL_FERIADO
```

**Critério de sucesso:** nenhum valor diferente de `S` ou `N`.  
**Ação em caso de falha:** rejeitar ou padronizar quando houver regra clara.

---

## 6.4. DQ-DIM-004: Datas de vigência devem ser consistentes

**Camada:** Silver/Gold  
**Severidade:** Alta  
**Tabelas aplicáveis:** `dim_produto`, `dim_cliente`  
**Descrição:** A data final de vigência não pode ser menor que a data inicial.

Regra:

```text
DATA_FIM_VIGENCIA >= DATA_INICIO_VIGENCIA
```

**Critério de sucesso:** todos os registros históricos devem respeitar a ordem temporal.  
**Ação em caso de falha:** rejeitar registro ou corrigir histórico.

---

## 6.5. DQ-DIM-005: Apenas um registro atual por chave de origem

**Camada:** Gold  
**Severidade:** Alta  
**Tabelas aplicáveis:** `dim_produto`, `dim_cliente`  
**Descrição:** Para dimensões SCD Tipo 2, deve existir apenas um registro atual por chave de origem.

Regra:

```text
Para cada ID_..._ORIGEM, deve existir no máximo um registro com FL_REGISTRO_ATUAL = 'S'
```

**Critério de sucesso:** contagem de registros atuais por chave de origem menor ou igual a 1.  
**Ação em caso de falha:** registrar inconsistência e corrigir histórico.

---

## 6.6. DQ-DIM-006: Produto deve possuir categoria válida

**Camada:** Silver/Gold  
**Severidade:** Crítica  
**Tabela:** `dim_produto`  
**Descrição:** Todo produto deve estar associado a uma categoria existente.

**Critério de sucesso:** `SK_CATEGORIA` do produto deve existir em `dim_categoria`.  
**Ação em caso de falha:** rejeitar produto ou associar a membro técnico.

---

## 6.7. DQ-DIM-007: Produto deve possuir unidade coerente

**Camada:** Silver/Gold  
**Severidade:** Média  
**Tabela:** `dim_produto`  
**Descrição:** A unidade de medida deve ser coerente com o tipo de produto.

Exemplos esperados:

```text
Bebidas                -> ML ou LT
Queijos e frios sólidos -> KG, UN ou PCT
Padaria                -> UN, PCT ou KG
Eletrônicos            -> UN
Bazar                  -> UN ou PCT
Hortifruti             -> KG ou UN
```

**Critério de sucesso:** produtos devem possuir descrição e unidade compatíveis.  
**Ação em caso de falha:** corrigir cadastro do produto.

---

## 7. Regras de Qualidade para Fatos

## 7.1. DQ-FAT-001: Fatos devem possuir chave de tempo válida

**Camada:** Silver/Gold  
**Severidade:** Crítica  
**Tabelas aplicáveis:** todas as fatos  
**Descrição:** Toda linha de fato deve possuir `SK_TEMPO` válido e existente na dimensão tempo.

**Critério de sucesso:** `SK_TEMPO` da fato deve existir em `dim_tempo`.  
**Ação em caso de falha:** rejeitar registro.

---

## 7.2. DQ-FAT-002: Fatos devem possuir produto válido quando aplicável

**Camada:** Silver/Gold  
**Severidade:** Crítica  
**Tabelas aplicáveis:** `fato_vendas`, `fato_estoque`, `fato_ruptura_estoque`  
**Descrição:** Toda linha dessas fatos deve possuir `SK_PRODUTO` existente em `dim_produto`.

**Critério de sucesso:** `SK_PRODUTO` válido.  
**Ação em caso de falha:** rejeitar registro ou associar a membro técnico.

---

## 7.3. DQ-FAT-003: Valores monetários não devem ser negativos

**Camada:** Silver/Gold  
**Severidade:** Alta  
**Descrição:** Campos monetários devem ser maiores ou iguais a zero, exceto em cenários futuros de estorno ou devolução.

Campos aplicáveis:

```text
VALOR_UNITARIO
VALOR_BRUTO
VALOR_DESCONTO
VALOR_LIQUIDO
CUSTO_TOTAL
VALOR_ESTOQUE_CUSTO
VALOR_ESTOQUE_VENDA
VALOR_VENDA_PERDIDA
META_FATURAMENTO_BRUTO
META_FATURAMENTO_LIQUIDO
```

**Critério de sucesso:** nenhum campo monetário negativo.  
**Ação em caso de falha:** rejeitar registro ou classificar como ajuste se houver regra futura.

---

## 7.4. DQ-FAT-004: Quantidades não devem ser negativas

**Camada:** Silver/Gold  
**Severidade:** Alta  
**Descrição:** Campos quantitativos devem ser maiores ou iguais a zero.

Campos aplicáveis:

```text
QUANTIDADE
QTD_ESTOQUE_DISPONIVEL
QTD_ESTOQUE_RESERVADO
QTD_ESTOQUE_BLOQUEADO
QTD_ESTOQUE_TRANSITO
QTD_ESTOQUE_TOTAL
QTD_RUPTURA
META_QTD_VENDAS
META_QTD_ITENS
```

**Critério de sucesso:** nenhum valor quantitativo negativo.  
**Ação em caso de falha:** rejeitar registro.

---

## 7.5. DQ-FAT-005: Valor líquido da venda deve ser coerente

**Camada:** Gold  
**Severidade:** Média  
**Tabela:** `fato_vendas`  
**Descrição:** Quando não houver juros, frete ou acréscimos, o valor líquido deve ser coerente com o valor bruto e desconto.

Regra sugerida:

```text
VALOR_LIQUIDO = VALOR_BRUTO - VALOR_DESCONTO
```

**Critério de sucesso:** divergência dentro de tolerância aceitável.  
**Ação em caso de falha:** registrar alerta para análise.

---

## 7.6. DQ-FAT-006: Margem bruta deve ser coerente

**Camada:** Gold  
**Severidade:** Média  
**Tabela:** `fato_vendas`  
**Descrição:** A margem bruta deve ser coerente com valor líquido e custo total.

Regra:

```text
MARGEM_BRUTA = VALOR_LIQUIDO - CUSTO_TOTAL
```

**Critério de sucesso:** divergência dentro de tolerância aceitável.  
**Ação em caso de falha:** registrar alerta.

---

## 7.7. DQ-FAT-007: Grão da FATO_ESTOQUE deve ser único

**Camada:** Silver/Gold  
**Severidade:** Crítica  
**Tabela:** `fato_estoque`  
**Descrição:** Não deve existir mais de uma linha para a mesma combinação de produto, loja e tempo.

Grão:

```text
SK_PRODUTO + SK_LOJA + SK_TEMPO
```

**Critério de sucesso:** contagem por grão igual a 1.  
**Ação em caso de falha:** remover duplicados na Silver ou consolidar registros.

---

## 7.8. DQ-FAT-008: Grão da FATO_VENDAS deve ser único

**Camada:** Silver/Gold  
**Severidade:** Alta  
**Tabela:** `fato_vendas`  
**Descrição:** Não deve existir duplicidade para a mesma venda e item de venda.

Grão:

```text
ID_VENDA_ORIGEM + ID_ITEM_VENDA_ORIGEM
```

**Critério de sucesso:** contagem por grão igual a 1.  
**Ação em caso de falha:** deduplicar pelo par de chaves.

---

## 7.9. DQ-FAT-009: Grão da FATO_METAS deve ser único

**Camada:** Silver/Gold  
**Severidade:** Alta  
**Tabela:** `fato_metas`  
**Descrição:** Não deve existir duplicidade no contexto da meta.

Grão:

```text
ANO_MES + SK_LOJA + SK_CANALVENDA + SK_PRODUTO + SK_CATEGORIA + SK_MARCA + TIPO_META
```

**Critério de sucesso:** contagem por grão igual a 1.  
**Ação em caso de falha:** consolidar ou manter o registro mais recente.

---

## 7.10. DQ-FAT-010: Datas das metas devem ser consistentes

**Camada:** Silver/Gold  
**Severidade:** Alta  
**Tabela:** `fato_metas`  
**Descrição:** A data final da meta não pode ser menor que a data inicial.

Regra:

```text
DATA_FIM_META >= DATA_INICIO_META
```

**Critério de sucesso:** todas as metas devem respeitar a vigência temporal.  
**Ação em caso de falha:** rejeitar meta.

---

## 8. Regras de Qualidade para Tabelas Técnicas

## 8.1. DQ-TEC-001: Controle de carga deve possuir status válido

**Camada:** Silver/Gold  
**Severidade:** Alta  
**Tabela:** `controle_carga`  
**Descrição:** O campo `STATUS_CARGA` deve possuir domínio válido.

Valores esperados:

```text
INICIADO
EM_EXECUCAO
SUCESSO
ERRO
CANCELADO
REPROCESSADO
```

**Critério de sucesso:** nenhum status fora do domínio.  
**Ação em caso de falha:** registrar erro de controle operacional.

---

## 8.2. DQ-TEC-002: Log de execução deve possuir status válido

**Camada:** Silver/Gold  
**Severidade:** Alta  
**Tabela:** `log_execucao`  
**Descrição:** O campo `STATUS_EVENTO` deve possuir domínio válido.

Valores esperados:

```text
INICIADO
EM_EXECUCAO
SUCESSO
ERRO
ALERTA
CANCELADO
```

**Critério de sucesso:** nenhum status fora do domínio.  
**Ação em caso de falha:** registrar inconsistência técnica.

---

## 8.3. DQ-TEC-003: Watermark não deve retroceder

**Camada:** Gold  
**Severidade:** Média  
**Tabela:** `controle_carga`  
**Descrição:** O watermark final deve ser maior ou igual ao inicial.

Regra:

```text
WATERMARK_FIM >= WATERMARK_INICIO
```

**Critério de sucesso:** nenhum watermark final menor que o inicial.  
**Ação em caso de falha:** investigar carga incremental.

---

## 9. Regras de Qualidade para Gold e BI

## 9.1. DQ-GOLD-001: KPI de vendas mensal deve possuir faturamento não negativo

**Camada:** Gold  
**Severidade:** Alta  
**Tabela:** `kpi_vendas_mensal`  
**Descrição:** O faturamento consolidado não deve ser negativo.

Campos aplicáveis:

```text
FATURAMENTO_BRUTO
FATURAMENTO_LIQUIDO
VALOR_DESCONTO
```

**Critério de sucesso:** valores maiores ou iguais a zero.  
**Ação em caso de falha:** revisar fato de vendas.

---

## 9.2. DQ-GOLD-002: Percentual de margem deve ser calculável

**Camada:** Gold  
**Severidade:** Média  
**Tabela:** `kpi_vendas_mensal`  
**Descrição:** O percentual de margem deve ser calculado somente quando o faturamento líquido for maior que zero.

Regra:

```text
PERCENTUAL_MARGEM = MARGEM_BRUTA / FATURAMENTO_LIQUIDO * 100
```

**Critério de sucesso:** não deve haver divisão por zero.  
**Ação em caso de falha:** retornar nulo quando denominador for zero.

---

## 9.3. DQ-GOLD-003: Percentual de atingimento da meta deve evitar divisão por zero

**Camada:** Gold  
**Severidade:** Alta  
**Tabela:** `kpi_meta_vs_realizado`  
**Descrição:** O percentual de atingimento deve ser calculado somente quando a meta for maior que zero.

Regra:

```text
PERCENTUAL_ATINGIMENTO_META = FATURAMENTO_LIQUIDO_REALIZADO / META_FATURAMENTO_LIQUIDO * 100
```

**Critério de sucesso:** não deve haver divisão por zero.  
**Ação em caso de falha:** retornar nulo ou classificar como `SEM_META`.

---

## 9.4. DQ-GOLD-004: Estoque atual deve considerar a última data disponível

**Camada:** Gold  
**Severidade:** Média  
**Tabela:** `kpi_estoque_atual`  
**Descrição:** A tabela de estoque atual deve utilizar somente a última data disponível na fato estoque.

**Critério de sucesso:** todos os registros devem possuir o mesmo `SK_TEMPO` máximo.  
**Ação em caso de falha:** revisar query da Gold.

---

## 9.5. DQ-GOLD-005: Status de estoque deve possuir domínio válido

**Camada:** Gold  
**Severidade:** Média  
**Tabela:** `kpi_estoque_atual`  
**Descrição:** O status de estoque deve possuir valores controlados.

Valores esperados:

```text
RUPTURA
ESTOQUE_BAIXO
EXCESSO
NORMAL
```

**Critério de sucesso:** nenhum valor fora do domínio.  
**Ação em caso de falha:** ajustar regra de classificação.

---

## 10. Consultas de Validação Sugeridas

## 10.1. Verificar duplicidade em estoque

```sql
SELECT
    SK_PRODUTO,
    SK_LOJA,
    SK_TEMPO,
    COUNT(*) AS QTD
FROM silver.fato_estoque
GROUP BY
    SK_PRODUTO,
    SK_LOJA,
    SK_TEMPO
HAVING COUNT(*) > 1;
```

## 10.2. Verificar vendas com produto inexistente

```sql
SELECT
    v.SK_PRODUTO,
    COUNT(*) AS QTD_REGISTROS
FROM silver.fato_vendas v
LEFT JOIN silver.dim_produto p
    ON v.SK_PRODUTO = p.SK_PRODUTO
WHERE p.SK_PRODUTO IS NULL
GROUP BY v.SK_PRODUTO;
```

## 10.3. Verificar valores monetários negativos em vendas

```sql
SELECT
    COUNT(*) AS QTD_REGISTROS_INVALIDOS
FROM silver.fato_vendas
WHERE VALOR_UNITARIO < 0
   OR VALOR_BRUTO < 0
   OR VALOR_DESCONTO < 0
   OR VALOR_LIQUIDO < 0
   OR CUSTO_TOTAL < 0;
```

## 10.4. Verificar metas com mês inválido

```sql
SELECT
    COUNT(*) AS QTD_REGISTROS_INVALIDOS
FROM silver.fato_metas
WHERE MES < 1
   OR MES > 12;
```

## 10.5. Verificar dimensões SCD com mais de um registro atual

```sql
SELECT
    ID_PRODUTO_ORIGEM,
    COUNT(*) AS QTD_REGISTROS_ATUAIS
FROM silver.dim_produto
WHERE FL_REGISTRO_ATUAL = 'S'
GROUP BY ID_PRODUTO_ORIGEM
HAVING COUNT(*) > 1;
```

## 10.6. Verificar status de estoque inválido na Gold

```sql
SELECT
    STATUS_ESTOQUE,
    COUNT(*) AS QTD
FROM gold.kpi_estoque_atual
GROUP BY STATUS_ESTOQUE
HAVING STATUS_ESTOQUE NOT IN ('RUPTURA', 'ESTOQUE_BAIXO', 'EXCESSO', 'NORMAL');
```

---

## 11. Evidências de Qualidade

As evidências de qualidade devem ser armazenadas em tabelas de validação e logs técnicos.

Tabelas recomendadas:

```text
bronze.log_ingestao_bronze
bronze.validacao_bronze
silver.log_qualidade_silver
silver.validacao_silver
gold.validacao_gold
```

Essas tabelas permitem acompanhar:

- quantidade de registros lidos;
- quantidade de registros gravados;
- duplicados removidos;
- registros descartados por nulos obrigatórios;
- status de execução;
- mensagens de erro;
- data de processamento.

---

## 12. Estratégia de Ação para Falhas

| Tipo de falha | Camada | Ação recomendada |
|---|---|---|
| Arquivo ausente | Raw/Bronze | Falhar carga da tabela |
| Arquivo vazio | Raw/Bronze | Registrar alerta ou falhar carga |
| Schema inválido | Silver | Falhar processamento |
| Conversão de tipo inválida | Silver | Rejeitar registros inválidos |
| Chave obrigatória nula | Silver | Remover ou rejeitar registro |
| Duplicidade de grão | Silver | Deduplicar ou consolidar |
| FK inexistente | Silver/Gold | Enviar para correção ou membro técnico |
| KPI incoerente | Gold | Revisar regra de negócio |
| Divisão por zero | Gold | Retornar nulo ou classificar como sem meta |

---

## 13. Regras Prioritárias para Finalização do Projeto

Para finalizar o projeto com um nível adequado de qualidade, as regras prioritárias são:

```text
1. Validar existência dos arquivos raw
2. Validar volumetria das tabelas Bronze
3. Aplicar schemas explícitos na Silver
4. Remover nulos de campos obrigatórios
5. Remover duplicados por grão
6. Validar chaves principais das dimensões
7. Validar integridade básica entre fatos e dimensões
8. Validar valores monetários e quantitativos não negativos
9. Validar KPIs principais da Gold
10. Registrar evidências em tabelas de validação
```

---

## 14. Evoluções Futuras

Em versões futuras do projeto, as regras de qualidade podem evoluir para:

```text
Data contracts
Expectations automatizadas
Great Expectations
Deequ
Testes unitários de dados
Pipeline com bloqueio por qualidade
Tabela de quarentena
Alertas por SLA
Monitoramento de freshness
Validação de anomalias
Reconciliação entre origem e destino
```

---

## 15. Conclusão

As regras de qualidade definidas neste documento garantem que o fluxo de dados do projeto tenha controles mínimos, porém relevantes, para uma solução analítica confiável.

A estratégia adotada mantém a Bronze simples e rastreável, transforma a Silver em uma camada tipada e padronizada, e assegura que a Gold aplique regras de negócio e indicadores consistentes para consumo em BI.
