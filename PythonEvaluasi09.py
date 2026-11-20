import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#============================================================
# KONFIGURASI DASHBOARD
#============================================================

st.set_page_config(
    page_title="Dashboard Analisis Diamonds",
    layout="wide"
)

st.markdown(
    """
    <style>
    [class*="st-key-bg_kpi"],
    [class*="st-key-bg_box"],
    [class*="st-key-bg_bar"],
    [class*="st-key-bg_pie"],
    [class*="st-key-bg_hist"],
    [class*="st-key-bg_heatmap"] {
        background-color: #FFB6D5;
        border: 2px solid #E84393;
        border-radius: 12px;
        padding: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
sns.set_theme(style="whitegrid")

#============================================================
# LOAD DATASET
#============================================================

path = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv"

df_dashboard = pd.read_csv(path)

#============================================================
# FITUR FILTER
#============================================================
st.sidebar.header("Filter Dashboard")

cut_value = sorted(df_dashboard["cut"].unique())
selected_cut = st.sidebar.multiselect(
    label="Kualitas Potongan Berlian",
    options=cut_value,
    default=cut_value
)

color_value = sorted(df_dashboard["color"].unique())
selected_color = st.sidebar.multiselect(
    label="Warna Berlian",
    options=color_value,
    default=color_value
)

clarity_value = sorted(df_dashboard["clarity"].unique())
selected_clarity = st.sidebar.multiselect(
    label="Kejernihan Berlian",
    options=clarity_value,
    default=clarity_value
)

df_filtered = df_dashboard[
    (df_dashboard["cut"].isin(selected_cut)) &
    (df_dashboard["color"].isin(selected_color)) &
    (df_dashboard["clarity"].isin(selected_clarity))
]

if df_filtered.empty:
    st.warning("Tidak ada data yang sesuai dengan filter.")
    st.stop()

#============================================================
# JUDUL DASHBOARD
#============================================================

st.title("DASHBOARD ANALISIS DIAMONDS")
st.caption("Dashboard Analisis Dataset Berlian - Praktikum Sains Data (Selfhi068)")

#============================================================
# KPI CARD
#============================================================

with st.container(border=True, key="bg_kpi"):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Data Berlian",
            f"{len(df_filtered):,}"
        )

    with col2:
        st.metric(
            "Rata-Rata Harga",
            f"${df_filtered['price'].mean():,.2f}"
        )

    with col3:
        st.metric(
            "Rata-Rata Carat",
            f"{df_filtered['carat'].mean():.2f}"
        )

    with col4:
        st.metric(
            "Harga Tertinggi",
            f"${df_filtered['price'].max():,.0f}"
        )

#============================================================
# PERSIAPAN DATA VISUALISASI
#============================================================

rata_harga_cut = (
    df_filtered.groupby("cut")["price"]
    .mean()
    .reindex(cut_value)
    .dropna()
    .reset_index()
)

jumlah_cut = (
    df_filtered["cut"]
    .value_counts()
    .reindex(cut_value)
    .dropna()
)

#============================================================
# FUNGSI PENGATUR GRAFIK
#============================================================

def atur_grafik(fig, ax, label_x, label_y):

    warna_kartu = "#FFF0F5"
    warna_teks = "#4A2040"
    warna_grid = "#F3A6C8"

    fig.patch.set_facecolor(warna_kartu)
    ax.set_facecolor(warna_kartu)

    ax.set_xlabel(
        label_x,
        color=warna_teks,
        fontweight="bold"
    )

    ax.set_ylabel(
        label_y,
        color=warna_teks,
        fontweight="bold"
    )

    ax.tick_params(colors=warna_teks)

    ax.grid(color=warna_grid, alpha=0.5)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_color(warna_grid)

#============================================================
# VISUALISASI BOXPLOT DAN BARPLOT
#============================================================

col1, col2 = st.columns(2)

#------------------------------------------------------------
# BOXPLOT
#------------------------------------------------------------

with col1:

    with st.container(border=True, key="bg_box"):

        st.markdown("**Distribusi Harga Berlian Berdasarkan Cut**")

        fig1, ax1 = plt.subplots()

        sns.boxplot(
            data=df_filtered,
            x="cut",
            y="price",
            color="#E84393",
            ax=ax1
        )

        atur_grafik(
            fig1,
            ax1,
            "Kualitas Potongan (Cut)",
            "Harga Berlian ($)"
        )

        plt.xticks(rotation=20)

        st.pyplot(fig1)
        plt.close(fig1)

#------------------------------------------------------------
# BARPLOT
#------------------------------------------------------------

with col2:

    with st.container(border=True, key="bg_bar"):

        st.markdown("**Rata-Rata Harga Berlian Berdasarkan Cut**")

        fig2, ax2 = plt.subplots()

        sns.barplot(
            data=rata_harga_cut,
            x="cut",
            y="price",
            color="#E84393",
            ax=ax2
        )

        atur_grafik(
            fig2,
            ax2,
            "Kualitas Potongan (Cut)",
            "Rata-Rata Harga ($)"
        )

        for container in ax2.containers:
            ax2.bar_label(
                container,
                fmt="$%.0f",
                fontsize=9,
                color="#4A2040"
            )

        plt.xticks(rotation=20)

        st.pyplot(fig2)
        plt.close(fig2)

#============================================================
# VISUALISASI PIE CHART DAN HISTOGRAM
#============================================================
col3, col4 = st.columns(2)

#------------------------------------------------------------
# PIE CHART
#------------------------------------------------------------

with col3:

    with st.container(border=True, key="bg_pie"):

        st.markdown("**Persentase Berlian Berdasarkan Cut**")

        fig3, ax3 = plt.subplots()

        ax3.pie(
            jumlah_cut,
            labels=jumlah_cut.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=[
                "#E84393",
                "#FF80AB",
                "#FFB6D5",
                "#F8C8DC",
                "#C2185B"
            ],
            textprops={"color": "#4A2040"}
        )

        ax3.axis("equal")

        fig3.patch.set_facecolor("#FFF0F5")

        st.pyplot(fig3)
        plt.close(fig3)

#------------------------------------------------------------
# HISTOGRAM
#------------------------------------------------------------

with col4:

    with st.container(border=True, key="bg_hist"):

        st.markdown("**Distribusi Harga Berlian**")

        fig4, ax4 = plt.subplots()

        sns.histplot(
            data=df_filtered,
            x="price",
            bins=30,
            color="#E84393",
            edgecolor="#FFFFFF",
            ax=ax4
        )

        atur_grafik(
            fig4,
            ax4,
            "Harga Berlian ($)",
            "Frekuensi"
        )

        st.pyplot(fig4)
        plt.close(fig4)

#============================================================
# VISUALISASI HEATMAP
#============================================================

with st.container(border=True, key="bg_heatmap"):

    st.markdown("**Heatmap Korelasi Antarvariabel Numerik**")

    korelasi = df_filtered.select_dtypes(
        include=np.number
    ).corr()

    fig5, ax5 = plt.subplots(figsize=(10, 6))

    fig5.patch.set_facecolor("#FFF0F5")
    ax5.set_facecolor("#FFF0F5")

    sns.heatmap(
        korelasi,
        annot=True,
        fmt=".2f",
        cmap="RdPu",
        linewidths=1,
        linecolor="#FFFFFF",
        ax=ax5
    )

    ax5.tick_params(colors="#4A2040")

    st.pyplot(fig5)
    plt.close(fig5)

#============================================================
# VIEW DATASET
#============================================================

with st.expander("Dataset Overview"):

    st.write("Jumlah Data:", len(df_filtered))

    st.dataframe(
        df_filtered,
        use_container_width=True
    )
