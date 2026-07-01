# Relatorio Interativo: Desempenho de Vendas - Matricial
# Projeto: DW Comercial Lakehouse com Microsoft Fabric
# Objetivo: criar uma experiencia analitica em Python, similar a um relatorio Power BI,
# usando os dados tratados/modelados na camada Gold como referencia conceitual.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Desempenho de Vendas - Matricial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Configuracoes
# -----------------------------
DEFAULT_DATA_DIR = Path("01_data/sample/csv")

REQUIRED_FILES = {
    "fato_vendas": "fato_vendas.csv",
    "fato_metas": "fato_metas.csv",
    "dim_tempo": "dim_tempo.csv",
    "dim_produto": "dim_produto.csv",
    "dim_loja": "dim_loja.csv",
    "dim_canalvenda": "dim_canalvenda.csv",
    "dim_categoria": "dim_categoria.csv",
    "dim_marca": "dim_marca.csv",
    "dim_fornecedor": "dim_fornecedor.csv"
}

# -----------------------------
# Funcoes utilitarias
# -----------------------------
@st.cache_data(show_spinner=False)
def read_csv_semicolon(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep=";", encoding="utf-8-sig")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().upper() for c in df.columns]
    return df


def to_numeric_safe(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    df = df.copy()
    for col in cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
                .replace({"": np.nan, "nan": np.nan, "None": np.nan})
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


@st.cache_data(show_spinner=True)
def load_model(data_dir: str) -> dict:
    data_path = Path(data_dir)
    dfs = {}

    missing = []
    for logical_name, file_name in REQUIRED_FILES.items():
        file_path = data_path / file_name
        if not file_path.exists():
            missing.append(str(file_path))
        else:
            dfs[logical_name] = normalize_columns(read_csv_semicolon(str(file_path)))

    if missing:
        raise FileNotFoundError("Arquivos nao encontrados:\n" + "\n".join(missing))

    # Conversoes principais
    numeric_vendas = [
        "QUANTIDADE", "VALOR_UNITARIO", "VALOR_BRUTO", "VALOR_DESCONTO",
        "VALOR_LIQUIDO", "CUSTO_TOTAL", "MARGEM_BRUTA"
    ]
    numeric_metas = [
        "META_FATURAMENTO_BRUTO", "META_FATURAMENTO_LIQUIDO", "META_QTD_VENDAS",
        "META_QTD_ITENS", "META_TICKET_MEDIO", "META_MARGEM_BRUTA", "META_PERCENTUAL_MARGEM"
    ]

    dfs["fato_vendas"] = to_numeric_safe(dfs["fato_vendas"], numeric_vendas)
    dfs["fato_metas"] = to_numeric_safe(dfs["fato_metas"], numeric_metas)

    # Datas
    if "DATA_HORA_VENDA" in dfs["fato_vendas"].columns:
        dfs["fato_vendas"]["DATA_HORA_VENDA"] = pd.to_datetime(dfs["fato_vendas"]["DATA_HORA_VENDA"], errors="coerce")
    if "DATA_COMPLETA" in dfs["dim_tempo"].columns:
        dfs["dim_tempo"]["DATA_COMPLETA"] = pd.to_datetime(dfs["dim_tempo"]["DATA_COMPLETA"], errors="coerce")

    # Gold logic: produto conformado
    dim_produto = dfs["dim_produto"].merge(
        dfs["dim_categoria"][["SK_CATEGORIA", "NOME_CATEGORIA", "NOME_DEPARTAMENTO"]],
        on="SK_CATEGORIA",
        how="left"
    ).merge(
        dfs["dim_marca"][["SK_MARCA", "NOME_MARCA", "FL_MARCA_PROPRIA"]],
        on="SK_MARCA",
        how="left"
    ).merge(
        dfs["dim_fornecedor"][["SK_FORNECEDOR", "NOME_FORNECEDOR", "TIPO_FORNECEDOR"]],
        on="SK_FORNECEDOR",
        how="left"
    )

    vendas = dfs["fato_vendas"].merge(
        dfs["dim_tempo"][["SK_TEMPO", "DATA_COMPLETA", "ANO", "MES", "ANO_MES", "NOME_MES"]],
        on="SK_TEMPO",
        how="left"
    ).merge(
        dim_produto[[
            "SK_PRODUTO", "NOME_PRODUTO", "SKU", "UNIDADE_MEDIDA", "NOME_CATEGORIA",
            "NOME_DEPARTAMENTO", "NOME_MARCA", "NOME_FORNECEDOR", "FL_PERECIVEL"
        ]],
        on="SK_PRODUTO",
        how="left"
    ).merge(
        dfs["dim_loja"][["SK_LOJA", "NOME_LOJA", "TIPO_LOJA", "CIDADE", "ESTADO", "REGIONAL"]],
        on="SK_LOJA",
        how="left"
    ).merge(
        dfs["dim_canalvenda"][["SK_CANALVENDA", "NOME_CANALVENDA", "TIPO_CANAL"]],
        on="SK_CANALVENDA",
        how="left"
    )

    vendas["PERCENTUAL_MARGEM"] = np.where(
        vendas["VALOR_LIQUIDO"] > 0,
        vendas["MARGEM_BRUTA"] / vendas["VALOR_LIQUIDO"] * 100,
        np.nan
    )

    vendas["PERCENTUAL_DESCONTO"] = np.where(
        vendas["VALOR_BRUTO"] > 0,
        vendas["VALOR_DESCONTO"] / vendas["VALOR_BRUTO"] * 100,
        np.nan
    )

    metas = dfs["fato_metas"].merge(
        dfs["dim_loja"][["SK_LOJA", "NOME_LOJA", "REGIONAL", "ESTADO"]],
        on="SK_LOJA",
        how="left"
    ).merge(
        dfs["dim_canalvenda"][["SK_CANALVENDA", "NOME_CANALVENDA"]],
        on="SK_CANALVENDA",
        how="left"
    ).merge(
        dfs["dim_categoria"][["SK_CATEGORIA", "NOME_CATEGORIA"]],
        on="SK_CATEGORIA",
        how="left"
    )

    return {
        "vendas": vendas,
        "metas": metas,
        "dim_produto": dim_produto,
        "dim_tempo": dfs["dim_tempo"],
        "dim_loja": dfs["dim_loja"],
        "dim_canalvenda": dfs["dim_canalvenda"],
        "dim_categoria": dfs["dim_categoria"]
    }


def currency_br(value):
    if pd.isna(value):
        return "R$ 0,00"
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def number_br(value, decimals=0):
    if pd.isna(value):
        return "0"
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def percent_br(value):
    if pd.isna(value):
        return "0,00%"
    return f"{value:.2f}%".replace(".", ",")


# -----------------------------
# Layout
# -----------------------------
st.title("Desempenho de Vendas - Matricial")
st.caption("Relatório interativo em Python inspirado em Power BI, baseado nas decisões analíticas da camada Gold.")

with st.sidebar:
    st.header("Configuração")
    data_dir = st.text_input("Pasta dos CSVs", value=str(DEFAULT_DATA_DIR))
    st.caption("Esperado: data/sample/csv com os CSVs separados por ponto e vírgula.")

try:
    model = load_model(data_dir)
except Exception as e:
    st.error("Não foi possível carregar os dados.")
    st.code(str(e))
    st.stop()

vendas = model["vendas"].copy()
metas = model["metas"].copy()

# -----------------------------
# Filtros dinamicos
# -----------------------------
with st.sidebar:
    st.header("Filtros")

    anos = sorted(vendas["ANO"].dropna().unique().tolist()) if "ANO" in vendas.columns else []
    ano_sel = st.multiselect("Ano", anos, default=anos)

    meses = sorted(vendas["MES"].dropna().unique().tolist()) if "MES" in vendas.columns else []
    mes_sel = st.multiselect("Mês", meses, default=meses)

    regionais = sorted(vendas["REGIONAL"].dropna().unique().tolist()) if "REGIONAL" in vendas.columns else []
    regional_sel = st.multiselect("Regional", regionais, default=regionais)

    lojas = sorted(vendas["NOME_LOJA"].dropna().unique().tolist()) if "NOME_LOJA" in vendas.columns else []
    loja_sel = st.multiselect("Loja", lojas, default=lojas)

    canais = sorted(vendas["NOME_CANALVENDA"].dropna().unique().tolist()) if "NOME_CANALVENDA" in vendas.columns else []
    canal_sel = st.multiselect("Canal", canais, default=canais)

    categorias = sorted(vendas["NOME_CATEGORIA"].dropna().unique().tolist()) if "NOME_CATEGORIA" in vendas.columns else []
    categoria_sel = st.multiselect("Categoria", categorias, default=categorias)

    marcas = sorted(vendas["NOME_MARCA"].dropna().unique().tolist()) if "NOME_MARCA" in vendas.columns else []
    marca_sel = st.multiselect("Marca", marcas, default=marcas)

mask = pd.Series(True, index=vendas.index)
if ano_sel:
    mask &= vendas["ANO"].isin(ano_sel)
if mes_sel:
    mask &= vendas["MES"].isin(mes_sel)
if regional_sel:
    mask &= vendas["REGIONAL"].isin(regional_sel)
if loja_sel:
    mask &= vendas["NOME_LOJA"].isin(loja_sel)
if canal_sel:
    mask &= vendas["NOME_CANALVENDA"].isin(canal_sel)
if categoria_sel:
    mask &= vendas["NOME_CATEGORIA"].isin(categoria_sel)
if marca_sel:
    mask &= vendas["NOME_MARCA"].isin(marca_sel)

vf = vendas[mask].copy()

# Filtrar metas no mesmo contexto basico
mf = metas.copy()
if ano_sel:
    mf = mf[mf["ANO"].isin(ano_sel)]
if mes_sel:
    mf = mf[mf["MES"].isin(mes_sel)]
if regional_sel and "REGIONAL" in mf.columns:
    mf = mf[mf["REGIONAL"].isin(regional_sel)]
if loja_sel and "NOME_LOJA" in mf.columns:
    mf = mf[mf["NOME_LOJA"].isin(loja_sel)]
if canal_sel and "NOME_CANALVENDA" in mf.columns:
    mf = mf[mf["NOME_CANALVENDA"].isin(canal_sel)]
if categoria_sel and "NOME_CATEGORIA" in mf.columns:
    mf = mf[mf["NOME_CATEGORIA"].isin(categoria_sel)]

# -----------------------------
# KPIs principais
# -----------------------------
fat_liq = vf["VALOR_LIQUIDO"].sum()
fat_bruto = vf["VALOR_BRUTO"].sum()
desconto = vf["VALOR_DESCONTO"].sum()
custo = vf["CUSTO_TOTAL"].sum()
margem = vf["MARGEM_BRUTA"].sum()
qtd_vendas = vf["ID_VENDA_ORIGEM"].nunique()
qtd_itens = vf["QUANTIDADE"].sum()
ticket = fat_liq / qtd_vendas if qtd_vendas else 0
perc_margem = margem / fat_liq * 100 if fat_liq else 0
meta_liq = mf["META_FATURAMENTO_LIQUIDO"].sum() if "META_FATURAMENTO_LIQUIDO" in mf.columns else 0
ating_meta = fat_liq / meta_liq * 100 if meta_liq else 0

st.subheader("Visão Executiva")

kpi_cols = st.columns(6)
kpi_cols[0].metric("Faturamento Líquido", currency_br(fat_liq))
kpi_cols[1].metric("Margem Bruta", currency_br(margem), delta=percent_br(perc_margem))
kpi_cols[2].metric("Ticket Médio", currency_br(ticket))
kpi_cols[3].metric("Qtd. Vendas", number_br(qtd_vendas, 0))
kpi_cols[4].metric("Qtd. Itens", number_br(qtd_itens, 0))
kpi_cols[5].metric("Atingimento Meta", percent_br(ating_meta))

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Matriz Comercial", "Tendência Mensal", "Produtos e Categorias", "Meta vs Realizado", "Base Analítica"
])

with tab1:
    st.markdown("### Matriz de desempenho por loja e categoria")
    metric_matrix = st.selectbox(
        "Métrica da matriz",
        ["VALOR_LIQUIDO", "MARGEM_BRUTA", "QUANTIDADE", "VALOR_DESCONTO"],
        index=0
    )

    matrix = vf.pivot_table(
        index="NOME_LOJA",
        columns="NOME_CATEGORIA",
        values=metric_matrix,
        aggfunc="sum",
        fill_value=0
    )

    if not matrix.empty:
        fig = px.imshow(
            matrix,
            text_auto=".2s",
            aspect="auto",
            color_continuous_scale="Blues",
            title=f"Matriz {metric_matrix} por Loja x Categoria"
        )
        fig.update_layout(height=650)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(matrix.style.format("{:,.2f}"), use_container_width=True)
    else:
        st.info("Sem dados para a matriz com os filtros selecionados.")

with tab2:
    st.markdown("### Tendência mensal de vendas")
    mensal = (
        vf.groupby("ANO_MES", dropna=False)
        .agg(
            FATURAMENTO_LIQUIDO=("VALOR_LIQUIDO", "sum"),
            FATURAMENTO_BRUTO=("VALOR_BRUTO", "sum"),
            MARGEM_BRUTA=("MARGEM_BRUTA", "sum"),
            QTD_VENDAS=("ID_VENDA_ORIGEM", "nunique"),
            QTD_ITENS=("QUANTIDADE", "sum")
        )
        .reset_index()
        .sort_values("ANO_MES")
    )
    mensal["TICKET_MEDIO"] = np.where(mensal["QTD_VENDAS"] > 0, mensal["FATURAMENTO_LIQUIDO"] / mensal["QTD_VENDAS"], np.nan)
    mensal["PERCENTUAL_MARGEM"] = np.where(mensal["FATURAMENTO_LIQUIDO"] > 0, mensal["MARGEM_BRUTA"] / mensal["FATURAMENTO_LIQUIDO"] * 100, np.nan)

    if not mensal.empty:
        fig_line = px.line(
            mensal,
            x="ANO_MES",
            y=["FATURAMENTO_LIQUIDO", "MARGEM_BRUTA"],
            markers=True,
            title="Faturamento Líquido e Margem Bruta por Mês"
        )
        st.plotly_chart(fig_line, use_container_width=True)

        fig_ticket = px.bar(
            mensal,
            x="ANO_MES",
            y="TICKET_MEDIO",
            title="Ticket Médio por Mês"
        )
        st.plotly_chart(fig_ticket, use_container_width=True)

        st.dataframe(mensal, use_container_width=True)
    else:
        st.info("Sem dados mensais com os filtros selecionados.")

with tab3:
    st.markdown("### Produtos, categorias e rentabilidade")
    col_a, col_b = st.columns(2)

    cat = (
        vf.groupby("NOME_CATEGORIA", dropna=False)
        .agg(
            FATURAMENTO_LIQUIDO=("VALOR_LIQUIDO", "sum"),
            MARGEM_BRUTA=("MARGEM_BRUTA", "sum"),
            QTD_ITENS=("QUANTIDADE", "sum")
        )
        .reset_index()
        .sort_values("FATURAMENTO_LIQUIDO", ascending=False)
    )
    cat["PERCENTUAL_MARGEM"] = np.where(cat["FATURAMENTO_LIQUIDO"] > 0, cat["MARGEM_BRUTA"] / cat["FATURAMENTO_LIQUIDO"] * 100, np.nan)

    top_produtos = (
        vf.groupby(["NOME_PRODUTO", "NOME_CATEGORIA"], dropna=False)
        .agg(
            FATURAMENTO_LIQUIDO=("VALOR_LIQUIDO", "sum"),
            MARGEM_BRUTA=("MARGEM_BRUTA", "sum"),
            QTD_ITENS=("QUANTIDADE", "sum")
        )
        .reset_index()
        .sort_values("FATURAMENTO_LIQUIDO", ascending=False)
        .head(20)
    )

    with col_a:
        fig_cat = px.bar(
            cat,
            x="FATURAMENTO_LIQUIDO",
            y="NOME_CATEGORIA",
            orientation="h",
            title="Faturamento por Categoria",
            color="PERCENTUAL_MARGEM",
            color_continuous_scale="Viridis"
        )
        fig_cat.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_b:
        fig_top = px.bar(
            top_produtos,
            x="FATURAMENTO_LIQUIDO",
            y="NOME_PRODUTO",
            orientation="h",
            color="NOME_CATEGORIA",
            title="Top 20 Produtos por Faturamento"
        )
        fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top, use_container_width=True)

    st.dataframe(top_produtos, use_container_width=True)

with tab4:
    st.markdown("### Meta versus realizado")

    realizado = (
        vf.groupby(["ANO_MES", "SK_LOJA", "SK_CANALVENDA", "SK_CATEGORIA"], dropna=False)
        .agg(
            FATURAMENTO_LIQUIDO_REALIZADO=("VALOR_LIQUIDO", "sum"),
            MARGEM_BRUTA_REALIZADA=("MARGEM_BRUTA", "sum"),
            QTD_VENDAS_REALIZADA=("ID_VENDA_ORIGEM", "nunique"),
            QTD_ITENS_REALIZADA=("QUANTIDADE", "sum")
        )
        .reset_index()
    )

    meta_ctx = mf.copy()
    join_cols = ["ANO_MES", "SK_LOJA", "SK_CANALVENDA", "SK_CATEGORIA"]
    meta_real = meta_ctx.merge(realizado, on=join_cols, how="left")
    for col in ["FATURAMENTO_LIQUIDO_REALIZADO", "MARGEM_BRUTA_REALIZADA", "QTD_VENDAS_REALIZADA", "QTD_ITENS_REALIZADA"]:
        if col in meta_real.columns:
            meta_real[col] = meta_real[col].fillna(0)

    meta_real["DESVIO_META_VALOR"] = meta_real["FATURAMENTO_LIQUIDO_REALIZADO"] - meta_real["META_FATURAMENTO_LIQUIDO"]
    meta_real["PERCENTUAL_ATINGIMENTO_META"] = np.where(
        meta_real["META_FATURAMENTO_LIQUIDO"] > 0,
        meta_real["FATURAMENTO_LIQUIDO_REALIZADO"] / meta_real["META_FATURAMENTO_LIQUIDO"] * 100,
        np.nan
    )
    meta_real["STATUS_META"] = np.select(
        [
            meta_real["META_FATURAMENTO_LIQUIDO"].fillna(0) == 0,
            meta_real["PERCENTUAL_ATINGIMENTO_META"] >= 100,
            meta_real["PERCENTUAL_ATINGIMENTO_META"] >= 90
        ],
        ["SEM_META", "ACIMA_DA_META", "PROXIMO_DA_META"],
        default="ABAIXO_DA_META"
    )

    resumo_meta = (
        meta_real.groupby("ANO_MES", dropna=False)
        .agg(
            META_FATURAMENTO_LIQUIDO=("META_FATURAMENTO_LIQUIDO", "sum"),
            FATURAMENTO_LIQUIDO_REALIZADO=("FATURAMENTO_LIQUIDO_REALIZADO", "sum")
        )
        .reset_index()
        .sort_values("ANO_MES")
    )
    resumo_meta["PERCENTUAL_ATINGIMENTO_META"] = np.where(
        resumo_meta["META_FATURAMENTO_LIQUIDO"] > 0,
        resumo_meta["FATURAMENTO_LIQUIDO_REALIZADO"] / resumo_meta["META_FATURAMENTO_LIQUIDO"] * 100,
        np.nan
    )

    fig_meta = go.Figure()
    fig_meta.add_trace(go.Bar(x=resumo_meta["ANO_MES"], y=resumo_meta["META_FATURAMENTO_LIQUIDO"], name="Meta"))
    fig_meta.add_trace(go.Bar(x=resumo_meta["ANO_MES"], y=resumo_meta["FATURAMENTO_LIQUIDO_REALIZADO"], name="Realizado"))
    fig_meta.update_layout(barmode="group", title="Meta x Realizado por Mês")
    st.plotly_chart(fig_meta, use_container_width=True)

    status_count = meta_real.groupby("STATUS_META").size().reset_index(name="QTD_CONTEXTOS")
    fig_status = px.pie(status_count, names="STATUS_META", values="QTD_CONTEXTOS", title="Distribuição de Status da Meta")
    st.plotly_chart(fig_status, use_container_width=True)

    st.dataframe(meta_real.sort_values("PERCENTUAL_ATINGIMENTO_META", ascending=False), use_container_width=True)

with tab5:
    st.markdown("### Base analítica filtrada")
    st.info("Esta tabela funciona como uma visão detalhada para auditoria e exploração dos dados filtrados.")
    cols = [
        "DATA_COMPLETA", "ANO_MES", "NOME_LOJA", "REGIONAL", "NOME_CANALVENDA", "NOME_CATEGORIA",
        "NOME_MARCA", "NOME_PRODUTO", "ID_VENDA_ORIGEM", "QUANTIDADE", "VALOR_BRUTO",
        "VALOR_DESCONTO", "VALOR_LIQUIDO", "CUSTO_TOTAL", "MARGEM_BRUTA", "PERCENTUAL_MARGEM"
    ]
    cols = [c for c in cols if c in vf.columns]
    st.dataframe(vf[cols].sort_values(cols[0] if cols else vf.columns[0], ascending=False), use_container_width=True)

    csv = vf[cols].to_csv(index=False, sep=";").encode("utf-8-sig")
    st.download_button(
        label="Baixar base filtrada em CSV",
        data=csv,
        file_name="desempenho_vendas_matricial_filtrado.csv",
        mime="text/csv"
    )

# -----------------------------
# Rodape
# -----------------------------
st.divider()
st.caption(
    "Relatório criado para a pasta 05_modelagem_de_dados. "
    "A lógica segue as decisões da camada Gold: dimensões conformadas, fato vendas enriquecida, "
    "meta versus realizado e matriz de desempenho comercial."
)
