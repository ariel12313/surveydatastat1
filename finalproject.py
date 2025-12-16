import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, shapiro

# =====================
# Page Config
# =====================
st.set_page_config(page_title="Survey Data Analysis", layout="wide")

# =====================
# Language Dictionary
# =====================
LANG = {
    "id": {
        "title": "📊 Aplikasi Analisis Data Survei",
        "desc": "Analisis deskriptif dan asosiasi (korelasi) otomatis berdasarkan uji normalitas.",
        "upload": "Upload file Excel (.xlsx)",
        "preview": "Pratinjau Data",
        "desc_stat": "Analisis Deskriptif",
        "select_x": "Pilih Variabel X",
        "select_y": "Pilih Variabel Y",
        "analyze": "Analisis Asosiasi",
        "result": "📌 Hasil Analisis",
        "analysis_desc": "📝 Deskripsi Analisis",
        "method": "Metode Korelasi",
        "corr": "Koefisien Korelasi",
        "pval": "p-value",
        "info": "Silakan upload file Excel untuk memulai.",
        "positive": "positif",
        "negative": "negatif"
    },
    "en": {
        "title": "📊 Survey Data Analysis App",
        "desc": "Descriptive and association analysis (correlation) based on normality testing.",
        "upload": "Upload Excel file (.xlsx)",
        "preview": "Data Preview",
        "desc_stat": "Descriptive Analysis",
        "select_x": "Select Variable X",
        "select_y": "Select Variable Y",
        "analyze": "Association Analysis",
        "result": "📌 Analysis Result",
        "analysis_desc": "📝 Analysis Description",
        "method": "Correlation Method",
        "corr": "Correlation Coefficient",
        "pval": "p-value",
        "info": "Please upload an Excel file to start.",
        "positive": "positive",
        "negative": "negative"
    }
}

# =====================
# Language Selector
# =====================
st.sidebar.title("🌐 Language / Bahasa")
lang = st.sidebar.radio(
    "Select Language",
    ["id", "en"],
    format_func=lambda x: "🇮🇩 Bahasa Indonesia" if x == "id" else "🇬🇧 English"
)
T = LANG[lang]

# =====================
# Title
# =====================
st.title(T["title"])
st.write(T["desc"])

# =====================
# Upload File
# =====================
uploaded_file = st.file_uploader(T["upload"], type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader(T["preview"])
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    # =====================
    # Descriptive Analysis
    # =====================
    st.subheader(T["desc_stat"])
    st.dataframe(df[numeric_cols].describe())

    # =====================
    # Association Analysis
    # =====================
    col_x = st.selectbox(T["select_x"], numeric_cols)
    col_y = st.selectbox(T["select_y"], numeric_cols, index=1 if len(numeric_cols) > 1 else 0)

    if st.button(T["analyze"]):
        data = df[[col_x, col_y]].dropna()

        # Normality Test
        _, p_x = shapiro(data[col_x])
        _, p_y = shapiro(data[col_y])

        if p_x > 0.05 and p_y > 0.05:
            method = "Pearson"
            corr, pval = pearsonr(data[col_x], data[col_y])
        else:
            method = "Spearman"
            corr, pval = spearmanr(data[col_x], data[col_y])

        direction = T["positive"] if corr > 0 else T["negative"]

        # =====================
        # Output
        # =====================
        st.subheader(T["result"])
        st.write(f"**{T['method']}**: {method}")
        st.write(f"**{T['corr']}**: {corr:.4f}")
        st.write(f"**{T['pval']}**: {pval:.4f}")

        # =====================
        # Visualization (Streamlit Built-in Scatter Chart)
        # =====================
        st.subheader(f"📈 Scatter Plot: {col_x} vs {col_y}")
        
        # Prepare data for scatter chart
        chart_data = data[[col_x, col_y]].copy()
        
        # Use Streamlit's native scatter_chart
        st.scatter_chart(
            chart_data,
            x=col_x,
            y=col_y,
            size=20,
            color='#FF4B4B'
        )
        
        # =====================
        # Description
        # =====================
        st.subheader(T["analysis_desc"])
        st.markdown(f"""
Hubungan antara **{col_x}** dan **{col_y}** dianalisis menggunakan metode **{method}**.
Nilai koefisien korelasi sebesar **{corr:.3f}** dengan arah hubungan **{direction}**.
""")

else:
    st.info(T["info"])
