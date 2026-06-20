import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="Dashboard Intelligent", layout="wide")
st.title("📊 Dashboard Intelligent (auto-adaptatif)")

uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

# ----------------------------
# NORMALISATION
# ----------------------------
def normalize(col):
    return re.sub(r'[^a-zA-Z0-9]', '', col.lower())

mapping = {
    "chiffredaffaires": "CA",
    "ca": "CA",
    "sales": "CA",
    "revenue": "CA",

    "profit": "Profit",
    "benefice": "Profit",
    "margin": "Profit",

    "cost": "Cost",
    "costs": "Cost",
    "expenses": "Cost",
    "achat": "Cost",
    "achats": "Cost",

    "date": "Date",
    "jour": "Date",

    "pays": "Pays",
    "country": "Pays",

    "produit": "Produit",
    "product": "Produit"
}

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # ----------------------------
    # RENOMMAGE INTELLIGENT
    # ----------------------------
    new_cols = {}

    for col in df.columns:
        key = normalize(col)
        if key in mapping:
            new_cols[col] = mapping[key]

    df = df.rename(columns=new_cols)

    st.write("📌 Colonnes détectées :", df.columns)

    # ----------------------------
    # CONVERSION DATE
    # ----------------------------
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # ----------------------------
    # KPI (ROBUSTES)
    # ----------------------------
    st.subheader("📌 Résumé global")

    col1, col2, col3, col4 = st.columns(4)

    if "CA" in df.columns:
        col1.metric("💰 Chiffre d'affaires", f"{df['CA'].sum():,.0f}")
    else:
        col1.metric("💰 CA", "N/A")

    if "Cost" in df.columns:
        col2.metric("📉 Achats / Coûts", f"{df['Cost'].sum():,.0f}")
    else:
        col2.metric("📉 Coûts", "N/A")

    if "Profit" in df.columns:
        col3.metric("📈 Profit", f"{df['Profit'].sum():,.0f}")
    else:
        if "CA" in df.columns and "Cost" in df.columns:
            df["Profit"] = df["CA"] - df["Cost"]
            col3.metric("📈 Profit", f"{df['Profit'].sum():,.0f}")
        else:
            col3.metric("📈 Profit", "N/A")

    col4.metric("📊 Lignes", len(df))

    # ----------------------------
    # FILTRES
    # ----------------------------
    st.sidebar.header("🔎 Filtres")

    if "Pays" in df.columns:
        pays = st.sidebar.multiselect(
            "Pays",
            df["Pays"].dropna().unique(),
            default=df["Pays"].dropna().unique()
        )
        df = df[df["Pays"].isin(pays)]

    if "Produit" in df.columns:
        produits = st.sidebar.multiselect(
            "Produits",
            df["Produit"].dropna().unique(),
            default=df["Produit"].dropna().unique()
        )
        df = df[df["Produit"].isin(produits)]

    # ----------------------------
    # EVOLUTION CA
    # ----------------------------
    st.subheader("📈 Évolution")

    if "Date" in df.columns and "CA" in df.columns:
        evo = df.groupby("Date")["CA"].sum().reset_index()
        fig = px.line(evo, x="Date", y="CA", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # PAYS
    # ----------------------------
    if "Pays" in df.columns and "CA" in df.columns:
        st.subheader("🌍 CA par pays")
        pays_df = df.groupby("Pays")["CA"].sum().reset_index()
        fig = px.pie(pays_df, values="CA", names="Pays")
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # PRODUITS
    # ----------------------------
    if "Produit" in df.columns and "CA" in df.columns:
        st.subheader("📦 CA par produit")
        prod_df = df.groupby("Produit")["CA"].sum().reset_index()
        fig = px.pie(prod_df, values="CA", names="Produit")
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # TABLE
    # ----------------------------
    st.subheader("📋 Données")
    st.dataframe(df, use_container_width=True)
