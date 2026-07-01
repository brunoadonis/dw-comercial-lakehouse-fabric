CREATE TABLE dw.LOG_EXECUCAO (
    ID_LOG_EXECUCAO         NUMBER GENERATED ALWAYS AS IDENTITY,

    ID_CONTROLE_CARGA       NUMBER,
    ID_EXECUCAO             VARCHAR2(100),

    NOME_PROCESSO           VARCHAR2(200) NOT NULL,
    NOME_PIPELINE           VARCHAR2(200),
    NOME_ETAPA              VARCHAR2(200) NOT NULL,
    NOME_TABELA             VARCHAR2(200),

    CAMADA_DADOS            VARCHAR2(50),
    TIPO_EVENTO             VARCHAR2(50) NOT NULL,
    STATUS_EVENTO           VARCHAR2(50) NOT NULL,

    DATA_INICIO_EVENTO      TIMESTAMP,
    DATA_FIM_EVENTO         TIMESTAMP,
    DURACAO_SEGUNDOS        NUMBER(18,2),

    QTD_LINHAS_PROCESSADAS  NUMBER DEFAULT 0 NOT NULL,
    QTD_LINHAS_INSERIDAS    NUMBER DEFAULT 0 NOT NULL,
    QTD_LINHAS_ATUALIZADAS  NUMBER DEFAULT 0 NOT NULL,
    QTD_LINHAS_EXCLUIDAS    NUMBER DEFAULT 0 NOT NULL,
    QTD_LINHAS_REJEITADAS   NUMBER DEFAULT 0 NOT NULL,

    CODIGO_ERRO             VARCHAR2(100),
    MENSAGEM_ERRO           VARCHAR2(4000),
    MENSAGEM_LOG            VARCHAR2(4000),

    HOST_EXECUCAO           VARCHAR2(200),
    USUARIO_EXECUCAO        VARCHAR2(100) DEFAULT USER,

    DATA_LOG                TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,

    CONSTRAINT PK_LOG_EXECUCAO 
        PRIMARY KEY (ID_LOG_EXECUCAO),

    CONSTRAINT FK_LOG_CONTROLE_CARGA 
        FOREIGN KEY (ID_CONTROLE_CARGA)
        REFERENCES dw.CONTROLE_CARGA (ID_CONTROLE_CARGA),

    CONSTRAINT CK_LOG_CAMADA_DADOS 
        CHECK (
            CAMADA_DADOS IN (
                'ORIGEM',
                'STAGING',
                'BRONZE',
                'SILVER',
                'GOLD',
                'DW'
            ) 
            OR CAMADA_DADOS IS NULL
        ),

    CONSTRAINT CK_LOG_TIPO_EVENTO 
        CHECK (TIPO_EVENTO IN (
            'INICIO',
            'FIM',
            'INFO',
            'ALERTA',
            'ERRO',
            'VALIDACAO',
            'MERGE',
            'INSERT',
            'UPDATE',
            'DELETE'
        )),

    CONSTRAINT CK_LOG_STATUS_EVENTO 
        CHECK (STATUS_EVENTO IN (
            'INICIADO',
            'EM_EXECUCAO',
            'SUCESSO',
            'ERRO',
            'ALERTA',
            'CANCELADO'
        )),

    CONSTRAINT CK_LOG_DATAS_EVENTO 
        CHECK (
            DATA_FIM_EVENTO IS NULL 
            OR DATA_INICIO_EVENTO IS NULL 
            OR DATA_FIM_EVENTO >= DATA_INICIO_EVENTO
        ),

    CONSTRAINT CK_LOG_DURACAO 
        CHECK (
            DURACAO_SEGUNDOS IS NULL 
            OR DURACAO_SEGUNDOS >= 0
        ),

    CONSTRAINT CK_LOG_QTD_PROC 
        CHECK (QTD_LINHAS_PROCESSADAS >= 0),

    CONSTRAINT CK_LOG_QTD_INS 
        CHECK (QTD_LINHAS_INSERIDAS >= 0),

    CONSTRAINT CK_LOG_QTD_UPD 
        CHECK (QTD_LINHAS_ATUALIZADAS >= 0),

    CONSTRAINT CK_LOG_QTD_DEL 
        CHECK (QTD_LINHAS_EXCLUIDAS >= 0),

    CONSTRAINT CK_LOG_QTD_REJ 
        CHECK (QTD_LINHAS_REJEITADAS >= 0)

COMMENT ON TABLE dw.LOG_EXECUCAO IS
'Tabela técnica responsável pelo registro detalhado dos eventos e etapas executadas durante os processos de carga de dados.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.ID_LOG_EXECUCAO IS 
'Chave primária surrogate da tabela de log de execução.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.ID_CONTROLE_CARGA IS 
'Chave estrangeira para a tabela dw.CONTROLE_CARGA.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.ID_EXECUCAO IS 
'Identificador único da execução do pipeline, notebook ou job.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.NOME_PROCESSO IS 
'Nome lógico do processo executado.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.NOME_PIPELINE IS 
'Nome do pipeline, notebook ou job responsável pelo evento.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.NOME_ETAPA IS 
'Nome da etapa específica do processamento. Exemplo: INGESTAO_BRONZE, MERGE_SILVER, CARGA_GOLD.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.NOME_TABELA IS 
'Nome da tabela relacionada ao evento registrado.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.CAMADA_DADOS IS 
'Camada de dados relacionada ao evento: ORIGEM, STAGING, BRONZE, SILVER, GOLD ou DW.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.TIPO_EVENTO IS 
'Tipo do evento registrado: INICIO, FIM, INFO, ALERTA, ERRO, VALIDACAO, MERGE, INSERT, UPDATE ou DELETE.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.STATUS_EVENTO IS 
'Status do evento registrado: INICIADO, EM_EXECUCAO, SUCESSO, ERRO, ALERTA ou CANCELADO.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.DATA_INICIO_EVENTO IS 
'Data e hora de início da etapa ou evento.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.DATA_FIM_EVENTO IS 
'Data e hora de finalização da etapa ou evento.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.DURACAO_SEGUNDOS IS 
'Duração da etapa ou evento em segundos.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.QTD_LINHAS_PROCESSADAS IS 
'Quantidade total de registros processados no evento.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.QTD_LINHAS_INSERIDAS IS 
'Quantidade de registros inseridos durante o evento.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.QTD_LINHAS_ATUALIZADAS IS 
'Quantidade de registros atualizados durante o evento.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.QTD_LINHAS_EXCLUIDAS IS 
'Quantidade de registros excluídos durante o evento.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.QTD_LINHAS_REJEITADAS IS 
'Quantidade de registros rejeitados durante o evento.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.CODIGO_ERRO IS 
'Código técnico do erro, quando aplicável.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.MENSAGEM_ERRO IS 
'Mensagem detalhada do erro, quando aplicável.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.MENSAGEM_LOG IS 
'Mensagem descritiva do evento registrado.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.HOST_EXECUCAO IS 
'Host, servidor, cluster ou ambiente em que o processo foi executado.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.USUARIO_EXECUCAO IS 
'Usuário responsável pela execução do evento.';

COMMENT ON COLUMN dw.LOG_EXECUCAO.DATA_LOG IS 
'Data e hora de criação do registro de log.';
);
