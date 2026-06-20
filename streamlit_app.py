
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Business", layout="wide")

st.title("📊 Dashboard Chiffre d'affaires & Profits")

uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    # ----------------------------
    # PREPARATION
    # ----------------------------
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    if "Profit" not in df.columns:
        if "Chiffre_Affaires" in df.columns and "Cout" in df.columns:
            df["Profit"] = df["Chiffre_Affaires"] - df["Cout"]

    # ----------------------------
    # FILTRES (arborescence)
    # ----------------------------
    st.sidebar.header("🔎 Filtres")

    if "Pays" in df.columns:
        pays = st.sidebar.multiselect("Pays", df["Pays"].dropna().unique(), default=df["Pays"].dropna().unique())
        df = df[df["Pays"].isin(pays)]

    if "Produit" in df.columns:
        produits = st.sidebar.multiselect("Produits", df["Produit"].dropna().unique(), default=df["Produit"].dropna().unique())
        df = df[df["Produit"].isin(produits)]

    # ----------------------------
    # KPI
    # ----------------------------
    st.subheader("📌 Résumé global")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 CA Total", f"{df['Chiffre_Affaires'].sum():,.0f} €")
    col2.metric("📉 Coûts", f"{df['Cout'].sum():,.0f} €")
    col3.metric("📈 Profit", f"{df['Profit'].sum():,.0f} €")

    # ----------------------------
    # EVOLUTION CA
    # ----------------------------
    st.subheader("📈 Évolution du chiffre d'affaires")

    ca_par_date = df.groupby("Date")["Chiffre_Affaires"].sum().reset_index()

    fig1 = px.line(ca_par_date, x="Date", y="Chiffre_Affaires", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    # ----------------------------
    # CAMEMBERT PAYS
    # ----------------------------
    st.subheader("🌍 CA & Profit par pays")

    if "Pays" in df.columns:
        pays_df = df.groupby("Pays")[["Chiffre_Affaires", "Profit"]].sum().reset_index()

        fig2 = px.pie(pays_df, values="Chiffre_Affaires", names="Pays", title="CA par pays")
        st.plotly_chart(fig2, use_container_width=True)

    # ----------------------------
    # CAMEMBERT PRODUIT
    # ----------------------------
    st.subheader("📦 CA & Profit par produit")

    if "Produit" in df.columns:
        prod_df = df.groupby("Produit")[["Chiffre_Affaires", "Profit"]].sum().reset_index()

        fig3 = px.pie(prod_df, values="Chiffre_Affaires", names="Produit", title="CA par produit")
        st.plotly_chart(fig3, use_container_width=True)

    # ----------------------------
    # TABLE
    # ----------------------------
    st.subheader("📋 Données")
    st.dataframe(df, use_container_width=True)

import re

def normalize(col):
    return re.sub(r'[^a-zA-Z0-9]', '', col.lower())

# dictionnaire "intelligent"
mapping = {
    "chiffredaffaires": "Chiffre_Affaires",
    "ca": "Chiffre_Affaires",
    "Sales": "Chiffre_Affaires",
    "revenue": "Chiffre_Affaires",


    "profit": "Profit",
    "benefice": "Profit",
    "margin": "Profit",

    "cost": "Cout",
    "costs": "Cout",
    "expenses": "Cout",

    "date": "Date",
    "jour": "Date",

    "pays": "Pays",
    "country": "Pays",

    "produit": "Produit",
    "Segment": "Produit",
    "product": "Produit"
}

new_cols = {}

for col in df.columns:
    key = normalize(col)
    if key in mapping:
        new_cols[col] = mapping[key]

df = df.rename(columns=new_cols)


