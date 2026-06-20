import streamlit as st
import pandas as pd

st.title("Mon dashboard Excel")

# 1. Upload du fichier Excel
uploaded_file = st.file_uploader("Charge ton fichier Excel", type=["xlsx"])

if uploaded_file is not None:
    
    # 2. Lecture de l'Excel
    df = pd.read_excel(uploaded_file)

    # 3. Affichage des données
    st.subheader("Aperçu des données")
    st.write(df)

    # 4. Graphique automatique (simple)
    st.subheader("Graphique")
    
    # On prend les colonnes numériques automatiquement
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:
        st.bar_chart(df[numeric_cols])
    else:
        st.warning("Aucune colonne numérique pour faire un graphique")
