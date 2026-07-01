# Decisões Arquiteturais

## Projeto: Data Warehouse Comercial

## 1. Objetivo

Este documento registra as principais decisões arquiteturais adotadas na construção do Data Warehouse Comercial.

O objetivo é documentar os motivos técnicos e de negócio que justificam a modelagem, a organização das tabelas, o uso de chaves, a definição de fatos e dimensões, a criação de índices, o uso de tabelas de controle e log, além das escolhas relacionadas à manutenção, rastreabilidade, performance e escalabilidade do projeto.

---

## 2. Adoção de Modelagem Dimensional

### Decisão

Foi adotada uma modelagem dimensional baseada em tabelas fato e tabelas dimensão.

### Justificativa

A modelagem dimensional facilita consultas analíticas, melhora a compreensão do modelo por usuários técnicos e de negócio e é adequada para cenários de análise comercial, estoque, metas e ruptura.

### Impacto

Essa abordagem permite análises como:

- Faturamento por período.
- Vendas por loja.
- Desempenho por categoria.
- Estoque por produto.
- Ruptura por loja.
- Meta versus realizado.
- Margem por marca, categoria e fornecedor.

---

## 3. Uso do Schema `dw`

### Decisão

Todas as tabelas do modelo foram criadas no schema `dw`.

### Justificativa

O schema `dw` separa os objetos analíticos das tabelas operacionais ou transacionais, facilitando organização, governança, manutenção e entendimento do ambiente.

### Impacto

A separação por schema permite identificar claramente quais objetos pertencem ao Data Warehouse e reduz a ambiguidade entre estruturas analíticas e estruturas de origem.

---

## 4. Uso de Surrogate Keys

### Decisão

As dimensões utilizam chaves técnicas com prefixo `SK_`.

Exemplos:

```text
SK_PRODUTO
SK_CLIENTE
SK_LOJA
SK_TEMPO
SK_CATEGORIA
SK_MARCA
```

### Justificativa

Surrogate keys desacoplam o Data Warehouse das chaves naturais dos sistemas de origem e permitem maior controle sobre histórico, versionamento e integridade referencial.

### Impacto

Essa decisão facilita:

- Controle histórico em dimensões.
- Alteração de chaves naturais na origem.
- Padronização dos relacionamentos entre fatos e dimensões.
- Melhor performance em joins com tabelas fato.
- Independência entre o modelo analítico e os sistemas transacionais.

---

## 5. Manutenção das Chaves de Origem

### Decisão

As dimensões mantêm campos com padrão `ID_..._ORIGEM`.

Exemplos:

```text
ID_PRODUTO_ORIGEM
ID_CLIENTE_ORIGEM
ID_LOJA_ORIGEM
ID_FORNECEDOR_ORIGEM
ID_CANALVENDA_ORIGEM
```

### Justificativa

Essas colunas permitem rastrear os dados até o sistema fonte e apoiam processos de carga incremental, auditoria, conciliação e troubleshooting.

### Impacto

Essa decisão melhora a rastreabilidade e permite identificar a origem de cada registro carregado no DW.

---

## 6. Uso de SCD Tipo 2 em Produto e Cliente

### Decisão

As dimensões `DIM_PRODUTO` e `DIM_CLIENTE` foram preparadas para histórico com campos de vigência.

Campos utilizados:

```text
DATA_INICIO_VIGENCIA
DATA_FIM_VIGENCIA
FL_REGISTRO_ATUAL
```

### Justificativa

Produto e cliente são entidades que podem sofrer alterações relevantes ao longo do tempo.

Exemplos de mudanças em produto:

- Alteração de preço.
- Alteração de custo.
- Alteração de categoria.
- Alteração de fornecedor.
- Alteração de status comercial.

Exemplos de mudanças em cliente:

- Alteração de cidade.
- Alteração de estado.
- Alteração de segmento.
- Alteração de tipo de cliente.

### Impacto

Essa decisão permite análises históricas mais corretas, preservando o contexto do dado no momento em que o evento ocorreu.

---

## 7. Criação da Dimensão Tempo

### Decisão

Foi criada a tabela `DIM_TEMPO` com chave no formato `YYYYMMDD`.

Exemplo:

```text
20260630
```

### Justificativa

A dimensão tempo é essencial para análises por dia, mês, trimestre, semestre, ano, fim de semana e feriado.

### Impacto

Essa decisão facilita consultas temporais e padroniza os filtros de período nas tabelas fato.

---

## 8. Separação das Tabelas Fato

### Decisão

Foram criadas fatos separadas para vendas, estoque, ruptura e metas.

```text
FATO_VENDAS
FATO_ESTOQUE
FATO_RUPTURA_ESTOQUE
FATO_METAS
```

### Justificativa

Cada fato representa um processo de negócio diferente e possui um grão próprio.

### Impacto

A separação evita mistura de granularidades e melhora a clareza analítica.

Grãos definidos:

```text
FATO_VENDAS              -> uma linha por item de venda
FATO_ESTOQUE             -> uma linha por produto, loja e data
FATO_RUPTURA_ESTOQUE     -> uma linha por evento de ruptura
FATO_METAS               -> uma linha por contexto de meta
```

---

## 9. Desnormalização Parcial nas Fatos

### Decisão

Algumas chaves como categoria, marca e fornecedor também foram incluídas nas tabelas fato, mesmo podendo ser obtidas por meio da `DIM_PRODUTO`.

Exemplos:

```text
SK_CATEGORIA
SK_MARCA
SK_FORNECEDOR
```

### Justificativa

Essa decisão melhora a performance e simplifica consultas analíticas recorrentes, especialmente em análises de vendas, estoque e metas por categoria, marca e fornecedor.

### Impacto

Consultas por categoria, marca e fornecedor podem ser feitas diretamente na fato, com menor necessidade de joins adicionais.

### Trade-off

Há maior redundância no modelo. Por isso, a carga deve garantir consistência entre `DIM_PRODUTO` e as chaves derivadas nas fatos.

---

## 10. Criação da FATO_VENDAS como Fato Transacional

### Decisão

A tabela `FATO_VENDAS` foi modelada como uma tabela fato transacional.

### Justificativa

Vendas representam eventos de negócio ocorridos em determinado momento. Cada item vendido deve ser registrado individualmente para permitir análises em diferentes níveis de detalhe.

### Impacto

Essa decisão permite análises como:

- Faturamento bruto.
- Faturamento líquido.
- Quantidade vendida.
- Ticket médio.
- Margem bruta.
- Desconto aplicado.
- Vendas por produto, loja, cliente, canal e período.

---

## 11. Criação da FATO_ESTOQUE como Snapshot

### Decisão

A tabela `FATO_ESTOQUE` foi modelada como uma tabela fato snapshot periódico.

### Justificativa

Estoque representa uma posição em determinado momento, e não apenas um evento transacional. Por isso, a fato deve armazenar a fotografia do estoque por produto, loja e data.

### Impacto

Essa modelagem permite análises como:

- Estoque disponível por dia.
- Estoque baixo.
- Excesso de estoque.
- Valor parado em estoque.
- Cobertura de estoque.
- Ruptura por produto e loja.
- Evolução da posição de estoque ao longo do tempo.

---

## 12. Criação da FATO_RUPTURA_ESTOQUE

### Decisão

Foi criada uma fato específica para eventos de ruptura de estoque.

### Justificativa

Ruptura é um evento relevante para varejo, pois impacta diretamente a venda perdida, a disponibilidade de produto e a experiência do cliente.

### Impacto

Essa decisão permite medir:

- Produtos com maior ruptura.
- Lojas mais afetadas.
- Motivos de ruptura.
- Dias em ruptura.
- Valor estimado de venda perdida.
- Relação entre ruptura, estoque e desempenho comercial.

---

## 13. Criação da FATO_METAS

### Decisão

Foi criada uma fato para armazenar metas comerciais.

### Justificativa

Metas são dados planejados e devem ser comparados com dados realizados, principalmente vendas.

### Impacto

Essa decisão permite análises de:

- Meta versus realizado.
- Percentual de atingimento.
- Desempenho por loja.
- Desempenho por canal.
- Desempenho por categoria.
- Desvio em relação à meta.
- Acompanhamento comercial mensal.

---

## 14. Criação de Tabelas de Controle e Log

### Decisão

Foram criadas tabelas técnicas para controle de carga e log de execução.

```text
CONTROLE_CARGA
LOG_EXECUCAO
```

### Justificativa

Pipelines de dados precisam de rastreabilidade, controle de status, volumetria, registro de erros e suporte a reprocessamento.

### Impacto

Essa decisão permite acompanhar:

- Status das cargas.
- Última data processada.
- Quantidade de linhas lidas.
- Quantidade de linhas gravadas.
- Quantidade de linhas atualizadas.
- Quantidade de linhas rejeitadas.
- Erros ocorridos.
- Etapas executadas.
- Tempo de execução.

---

## 15. Uso de Índices nas Tabelas Fato

### Decisão

Foram criados índices nas principais chaves estrangeiras e em combinações analíticas das tabelas fato.

### Justificativa

As tabelas fato tendem a possuir maior volume de dados. Índices ajudam a melhorar a performance de consultas por tempo, produto, loja, canal, categoria, marca, fornecedor, promoção e forma de pagamento.

### Impacto

Essa decisão melhora consultas como:

- Vendas por período.
- Vendas por loja.
- Vendas por produto.
- Estoque por produto e loja.
- Ruptura por motivo.
- Metas por ano e mês.
- Meta versus realizado.

### Trade-off

Índices aumentam o custo de escrita em cargas massivas. Em ambiente produtivo, os índices devem ser avaliados conforme volume, frequência de carga e padrão real de consulta.

---

## 16. Uso de Constraints

### Decisão

Foram utilizadas constraints de chave primária, chave estrangeira, unicidade e validação.

### Justificativa

Constraints aumentam a qualidade e a integridade dos dados.

### Impacto

Essa decisão evita:

- Fatos apontando para dimensões inexistentes.
- Flags inválidas.
- Valores negativos indevidos.
- Datas finais menores que datas iniciais.
- Duplicidades em determinados grãos.
- Quebra de relacionamento entre entidades do modelo.

---

## 17. Uso de Valores Nulos em Algumas Foreign Keys

### Decisão

Algumas foreign keys nas fatos foram definidas como opcionais.

Exemplos:

```text
SK_CLIENTE
SK_PROMOCAO
SK_CANALVENDA
SK_FORMAPAGTO
SK_MARCA
SK_FORNECEDOR
```

### Justificativa

Nem todos os eventos de negócio possuem todas as informações disponíveis.

Exemplos:

- Venda sem cliente identificado.
- Venda sem promoção.
- Meta sem definição por produto.
- Venda sem canal informado na origem.
- Produto sem fornecedor informado.

### Impacto

Essa decisão dá flexibilidade ao modelo, mas exige cuidado nas consultas e dashboards.

### Recomendação futura

Criar registros técnicos nas dimensões para reduzir o uso de nulos em tabelas fato.

Padrão sugerido:

```text
-1 = Não informado
-2 = Não aplicável
-3 = Não identificado
```

---

## 18. Nome da Dimensão de Ruptura

### Decisão

Foi utilizada a dimensão `DIM_PRODUTORUPTURA`.

### Justificativa

A tabela representa classificações, tipos ou motivos associados a eventos de ruptura.

### Observação

Conceitualmente, o nome `DIM_MOTIVO_RUPTURA` poderia representar melhor o papel da dimensão.

### Impacto

O nome atual é funcional, mas uma nomenclatura mais semântica pode melhorar a clareza do modelo e a comunicação com outros profissionais.

---

## 19. Preparação para Cargas Incrementais

### Decisão

O modelo inclui campos e tabelas de apoio para controle incremental.

Exemplos:

```text
DATA_CARGA
DATA_ATUALIZACAO_DW
DATA_HORA_VENDA
WATERMARK_INICIO
WATERMARK_FIM
ULTIMA_DATA_PROCESSADA
```

### Justificativa

Cargas incrementais são essenciais para reduzir tempo de processamento, evitar recarga completa e aproximar o projeto de cenários reais de mercado.

### Impacto

Essa decisão permite implementar pipelines mais eficientes, rastreáveis e compatíveis com operação recorrente.

---

## 20. Separação entre Estrutura, Documentação e Carga

### Decisão

O projeto foi organizado em etapas separadas.

```text
Criação de tabelas
Criação de constraints
Criação de índices
Comentários
Dicionário de dados
Regras de negócio
Decisões arquiteturais
Carga de dados
Consultas analíticas
```

### Justificativa

Separar estrutura, carga e documentação facilita manutenção, versionamento, entendimento do projeto e apresentação técnica no GitHub.

### Impacto

Essa abordagem melhora a organização do repositório e permite evolução incremental do projeto.

---

## 21. Uso de Documentação Técnica

### Decisão

Foram previstos documentos específicos para diferentes objetivos.

```text
dicionario_de_dados.md
regras_de_negocio.md
decisoes_arquiteturais.md
```

### Justificativa

A documentação técnica facilita entendimento, manutenção e reutilização do projeto por outros profissionais.

### Impacto

Essa decisão torna o projeto mais apresentável para portfólio, entrevistas técnicas, LinkedIn e GitHub.

---

## 22. Preparação para Camadas Analíticas Futuras

### Decisão

O modelo foi preparado para permitir criação futura de views, consultas analíticas, dashboards e camadas de consumo.

### Justificativa

Um Data Warehouse deve ser consumido por ferramentas analíticas e processos de geração de indicadores.

### Impacto

Essa decisão permite evoluir o projeto para:

- Views de KPIs.
- Queries de negócio.
- Dashboards Power BI.
- Camada Gold em Lakehouse.
- Consumo via SQL Analytics Endpoint.
- Integração com Microsoft Fabric.

---

## 23. Possível Integração com Lakehouse

### Decisão

O modelo relacional em Oracle foi desenhado de forma compatível com futura ingestão para uma arquitetura Lakehouse.

### Justificativa

A separação entre dimensões, fatos, controle de carga e logs facilita a movimentação dos dados para camadas Bronze, Silver e Gold em plataformas modernas de dados.

### Impacto

Essa decisão permite conectar o projeto Oracle a pipelines em PySpark, Delta Lake e Microsoft Fabric.

---

## 24. Decisões Futuras

Algumas decisões podem ser revisitadas conforme o projeto evoluir:

- Renomear `DIM_PRODUTORUPTURA` para `DIM_MOTIVO_RUPTURA`.
- Criar registros técnicos para valores não informados.
- Criar uma camada staging antes do DW.
- Implementar procedures PL/SQL para carga.
- Implementar cargas incrementais com `MERGE`.
- Criar views analíticas para consumo.
- Criar dashboard em Power BI.
- Avaliar particionamento das fatos por tempo.
- Avaliar compressão ou paralelismo em tabelas grandes.
- Avaliar remoção ou criação de novos índices conforme padrões reais de consulta.
- Implementar testes automatizados de qualidade de dados.
- Criar tabela de rejeições para dados inválidos.

---

## 25. Resumo das Principais Decisões

| Decisão | Justificativa | Impacto |
|---|---|---|
| Modelagem dimensional | Facilitar consultas analíticas e entendimento de negócio | Modelo mais simples para análise |
| Uso de surrogate keys | Desacoplar o DW das chaves naturais da origem | Mais flexibilidade e suporte a histórico |
| Manutenção das chaves de origem | Garantir rastreabilidade | Facilita auditoria e conciliação |
| Uso de SCD em produto e cliente | Preservar histórico de alterações relevantes | Maior qualidade em análises históricas |
| Criação da DIM_TEMPO | Padronizar análises temporais | Consultas por período mais simples |
| Separação das fatos | Evitar mistura de granularidades | Modelo mais claro e consistente |
| Criação da FATO_ESTOQUE | Analisar posição de estoque ao longo do tempo | Suporte a estoque baixo, ruptura e cobertura |
| Criação da FATO_RUPTURA_ESTOQUE | Medir impactos de falta de estoque | Análise de venda perdida e disponibilidade |
| Criação da FATO_METAS | Permitir análise de meta versus realizado | Suporte ao acompanhamento comercial |
| Criação de controle e log | Garantir rastreabilidade e observabilidade | Melhor monitoramento das cargas |
| Criação de índices | Melhorar performance de consultas analíticas | Consultas mais eficientes |
| Uso de constraints | Aumentar qualidade e integridade dos dados | Menor risco de inconsistência |
| Documentação técnica | Facilitar manutenção e apresentação do projeto | Projeto mais profissional e reutilizável |

---

## 26. Conclusão

As decisões arquiteturais adotadas neste projeto foram orientadas por princípios de modelagem dimensional, rastreabilidade, qualidade de dados, performance analítica e facilidade de manutenção.

O modelo foi estruturado para representar processos comerciais relevantes, como vendas, estoque, ruptura e metas, mantendo flexibilidade para evolução futura em pipelines de dados, camada Lakehouse, dashboards e análises executivas.
