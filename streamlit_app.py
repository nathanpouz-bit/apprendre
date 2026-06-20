
import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="Dashboard Business", layout="wide")

st.title("📊 Dashboard Chiffre d'affaires & Profits")

uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

# ----------------------------
# FONCTION SMART (DOIT ÊTRE EN HAUT)
# ----------------------------
def normalize(col):
    return re.sub(r'[^a-zA-Z0-9]', '', col.lower())

mapping = {
    "chiffredaffaires": "Chiffre_Affaires",
    "ca": "Chiffre_Affaires",
    "sales": "Chiffre_Affaires",
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
    "segment": "Produit",
    "product": "Produit"
}

if uploaded_file is not None:

    # ----------------------------
    # LECTURE EXCEL
    # ----------------------------
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

    # ----------------------------
    # CHECKS DE SÉCURITÉ (IMPORTANT)
    # ----------------------------
    if "Chiffre_Affaires" not in df.columns:
        st.error("❌ Colonne Chiffre_Affaires introuvable dans ton Excel")
        st.write("Colonnes détectées :", df.columns)
        st.stop()

    # ----------------------------
    # PREPARATION
    # ----------------------------
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    if "Profit" not in df.columns:
        if "Chiffre_Affaires" in df.columns and "Cout" in df.columns:
            df["Profit"] = df["Chiffre_Affaires"] - df["Cout"]

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
    # KPI
    # ----------------------------
    st.subheader("📌 Résumé global")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 CA Total", f"{df['Chiffre_Affaires'].sum():,.0f} €")

    if "Cout" in df.columns:
        col2.metric("📉 Coûts", f"{df['Cout'].sum():,.0f} €")
    else:
        col2.metric("📉 Coûts", "N/A")

    if "Profit" in df.columns:
        col3.metric("📈 Profit", f"{df['Profit'].sum():,.0f} €")
    else:
        col3.metric("📈 Profit", "N/A")

    # ----------------------------
    # EVOLUTION CA
    # ----------------------------
    st.subheader("📈 Évolution du chiffre d'affaires")

    if "Date" in df.columns:
        ca_par_date = df.groupby("Date")["Chiffre_Affaires"].sum().reset_index()
        fig1 = px.line(ca_par_date, x="Date", y="Chiffre_Affaires", markers=True)
        st.plotly_chart(fig1, use_container_width=True)

    # ----------------------------
    # CAMEMBERT PAYS
    # ----------------------------
    st.subheader("🌍 CA par pays")

    if "Pays" in df.columns:
        pays_df = df.groupby("Pays")["Chiffre_Affaires"].sum().reset_index()
        fig2 = px.pie(pays_df, values="Chiffre_Affaires", names="Pays")
        st.plotly_chart(fig2, use_container_width=True)

    # ----------------------------
    # CAMEMBERT PRODUIT
    # ----------------------------
    st.subheader("📦 CA par produit")

    if "Produit" in df.columns:
        prod_df = df.groupby("Produit")["Chiffre_Affaires"].sum().reset_index()
        fig3 = px.pie(prod_df, values="Chiffre_Affaires", names="Produit")
        st.plotly_chart(fig3, use_container_width=True)

    # ----------------------------
    # TABLE
    # ----------------------------
    st.subheader("📋 Données")
    st.dataframe(df, use_container_width=True)


