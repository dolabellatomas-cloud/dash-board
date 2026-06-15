import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# -----------------------------
# Dados de exemplo (troque por pd.read_csv("seu_arquivo.csv") )
# -----------------------------
@st.cache_data
def carregar_dados():
    np.random.seed(42)
    datas = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    regioes = ["Sudeste", "Sul", "Nordeste", "Norte", "Centro-Oeste"]
    produtos = ["Produto A", "Produto B", "Produto C"]

    df = pd.DataFrame({
        "data": np.random.choice(datas, 2000),
        "regiao": np.random.choice(regioes, 2000),
        "produto": np.random.choice(produtos, 2000),
        "vendas": np.random.randint(50, 500, 2000),
        "lucro": np.random.randint(5, 150, 2000),
    })
    return df

df = carregar_dados()

# -----------------------------
# Sidebar - filtros
# -----------------------------
st.sidebar.header("Filtros")

regioes_sel = st.sidebar.multiselect(
    "Região", options=df["regiao"].unique(), default=df["regiao"].unique()
)
produtos_sel = st.sidebar.multiselect(
    "Produto", options=df["produto"].unique(), default=df["produto"].unique()
)
data_min, data_max = st.sidebar.date_input(
    "Período",
    value=(df["data"].min(), df["data"].max()),
)

df_filtrado = df[
    (df["regiao"].isin(regioes_sel)) &
    (df["produto"].isin(produtos_sel)) &
    (df["data"] >= pd.to_datetime(data_min)) &
    (df["data"] <= pd.to_datetime(data_max))
]

# -----------------------------
# Cabeçalho e KPIs
# -----------------------------
st.title("📊 Dashboard de Vendas")

col1, col2, col3 = st.columns(3)
col1.metric("Total de Vendas", f"{df_filtrado['vendas'].sum():,.0f}")
col2.metric("Lucro Total", f"R$ {df_filtrado['lucro'].sum():,.2f}")
col3.metric("Nº de Registros", f"{len(df_filtrado):,}")

st.divider()

# -----------------------------
# Gráficos
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    vendas_por_regiao = df_filtrado.groupby("regiao")["vendas"].sum().reset_index()
    fig1 = px.bar(vendas_por_regiao, x="regiao", y="vendas", title="Vendas por Região")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    vendas_por_produto = df_filtrado.groupby("produto")["vendas"].sum().reset_index()
    fig2 = px.pie(vendas_por_produto, names="produto", values="vendas", title="Participação por Produto")
    st.plotly_chart(fig2, use_container_width=True)

vendas_por_dia = df_filtrado.groupby("data")["vendas"].sum().reset_index()
fig3 = px.line(vendas_por_dia, x="data", y="vendas", title="Vendas ao Longo do Tempo")
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Tabela
# -----------------------------
st.subheader("Dados detalhados")
st.dataframe(df_filtrado, use_container_width=True)
