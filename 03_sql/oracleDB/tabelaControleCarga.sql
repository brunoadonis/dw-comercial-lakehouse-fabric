CREATE TABLE dw.CONTROLE_CARGA (
    ID_CONTROLE_CARGA       NUMBER GENERATED ALWAYS AS IDENTITY,

    NOME_PROCESSO           VARCHAR2(200) NOT NULL,
    NOME_PIPELINE           VARCHAR2(200),
    NOME_TABELA             VARCHAR2(200) NOT NULL,
    CAMADA_DADOS            VARCHAR2(50)  NOT NULL,

    TIPO_CARGA              VARCHAR2(50)  NOT NULL,
    STATUS_CARGA            VARCHAR2(50)  NOT NULL,

    DATA_INICIO_CARGA       TIMESTAMP,
    DATA_FIM_CARGA          TIMESTAMP,

    WATERMARK_INICIO        TIMESTAMP,
    WATERMARK_FIM           TIMESTAMP,
    ULTIMA_DATA_PROCESSADA  TIMESTAMP,

    QTD_LINHAS_LIDAS        NUMBER DEFAULT 0 NOT NULL,
    QTD_LINHAS_GRAVADAS     NUMBER DEFAULT 0 NOT NULL,
    QTD_LINHAS_ATUALIZADAS  NUMBER DEFAULT 0 NOT NULL,
    QTD_LINHAS_REJEITADAS   NUMBER DEFAULT 0 NOT NULL,

    ID_EXECUCAO             VARCHAR2(100),
    USUARIO_EXECUCAO        VARCHAR2(100) DEFAULT USER,
    MENSAGEM_ERRO           VARCHAR2(4000),

    DATA_CRIACAO            TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    DATA_ATUALIZACAO        TIMESTAMP,

    CONSTRAINT PK_CONTROLE_CARGA 
        PRIMARY KEY (ID_CONTROLE_CARGA),

    CONSTRAINT CK_CC_CAMADA_DADOS 
        CHECK (CAMADA_DADOS IN (
            'ORIGEM',
            'STAGING',
            'BRONZE',
            'SILVER',
            'GOLD',
            'DW'
        )),

    CONSTRAINT CK_CC_TIPO_CARGA 
        CHECK (TIPO_CARGA IN (
            'FULL',
            'INCREMENTAL',
            'REPROCESSAMENTO',
            'MANUAL'
        )),

    CONSTRAINT CK_CC_STATUS_CARGA 
        CHECK (STATUS_CARGA IN (
            'INICIADO',
            'EM_EXECUCAO',
            'SUCESSO',
            'ERRO',
            'CANCELADO',
            'REPROCESSADO'
        )),

    CONSTRAINT CK_CC_QTD_LIDAS 
        CHECK (QTD_LINHAS_LIDAS >= 0),

    CONSTRAINT CK_CC_QTD_GRAVADAS 
        CHECK (QTD_LINHAS_GRAVADAS >= 0),

    CONSTRAINT CK_CC_QTD_ATUALIZADAS 
        CHECK (QTD_LINHAS_ATUALIZADAS >= 0),

    CONSTRAINT CK_CC_QTD_REJEITADAS 
        CHECK (QTD_LINHAS_REJEITADAS >= 0),

    CONSTRAINT CK_CC_DATAS_CARGA 
        CHECK (
            DATA_FIM_CARGA IS NULL 
            OR DATA_INICIO_CARGA IS NULL 
            OR DATA_FIM_CARGA >= DATA_INICIO_CARGA
        ),

    CONSTRAINT CK_CC_WATERMARK 
        CHECK (
            WATERMARK_FIM IS NULL 
            OR WATERMARK_INICIO IS NULL 
            OR WATERMARK_FIM >= WATERMARK_INICIO
        )

COMMENT ON TABLE dw.CONTROLE_CARGA IS
'Tabela técnica responsável pelo controle das cargas de dados, armazenando status, watermark, métricas de linhas processadas e informações de auditoria.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.ID_CONTROLE_CARGA IS 
'Chave primária surrogate da tabela de controle de carga.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.NOME_PROCESSO IS 
'Nome lógico do processo de carga. Exemplo: CARGA_FATO_VENDAS.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.NOME_PIPELINE IS 
'Nome do pipeline ou notebook responsável pela execução da carga.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.NOME_TABELA IS 
'Nome da tabela alvo processada pela carga.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.CAMADA_DADOS IS 
'Camada de dados relacionada ao processo: ORIGEM, STAGING, BRONZE, SILVER, GOLD ou DW.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.TIPO_CARGA IS 
'Tipo de carga executada: FULL, INCREMENTAL, REPROCESSAMENTO ou MANUAL.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.STATUS_CARGA IS 
'Status atual ou final da carga: INICIADO, EM_EXECUCAO, SUCESSO, ERRO, CANCELADO ou REPROCESSADO.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.DATA_INICIO_CARGA IS 
'Data e hora de início da carga.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.DATA_FIM_CARGA IS 
'Data e hora de finalização da carga.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.WATERMARK_INICIO IS 
'Valor inicial do watermark utilizado na carga incremental.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.WATERMARK_FIM IS 
'Valor final do watermark utilizado na carga incremental.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.ULTIMA_DATA_PROCESSADA IS 
'Última data efetivamente processada com sucesso.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.QTD_LINHAS_LIDAS IS 
'Quantidade de registros lidos na carga.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.QTD_LINHAS_GRAVADAS IS 
'Quantidade de registros gravados na tabela destino.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.QTD_LINHAS_ATUALIZADAS IS 
'Quantidade de registros atualizados no processo de carga.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.QTD_LINHAS_REJEITADAS IS 
'Quantidade de registros rejeitados por erro, validação ou regra de qualidade.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.ID_EXECUCAO IS 
'Identificador único da execução do pipeline, notebook ou job.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.USUARIO_EXECUCAO IS 
'Usuário responsável pela execução da carga.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.MENSAGEM_ERRO IS 
'Mensagem de erro capturada em caso de falha no processamento.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.DATA_CRIACAO IS 
'Data e hora de criação do registro de controle.';

COMMENT ON COLUMN dw.CONTROLE_CARGA.DATA_ATUALIZACAO IS 
'Data e hora da última atualização do registro de controle.';
);