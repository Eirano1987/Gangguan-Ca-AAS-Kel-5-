"""
Aplikasi web (Streamlit): kalkulator deret Ca + model 3D GBC Avanta AAS.
Jalankan:  streamlit run app.py
Taruh avanta_aas.html dan deret_ca.py di folder yang sama.
"""
from pathlib import Path
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import deret_ca as dc

st.set_page_config(page_title="Analisis Ca - AAS", layout="wide")
st.title("Analisis Ca dengan AAS (GBC Avanta)")

with st.sidebar:
    st.header("Pengaturan")
    dc.V_AKHIR = st.number_input("Volume labu (mL)", 1.0, 1000.0, 50.0)
    dc.HNO3_PERSEN = st.number_input("HNO3 pekat akhir (% v/v)", 0.0, 20.0, 1.0)
    st.subheader("Stok (mg/L)")
    for k in dc.STOK:
        dc.STOK[k] = st.number_input(f"Stok {k}", 1.0, 1e6, dc.STOK[k], key="s" + k)
    st.subheader("Konsentrasi akhir (mg/L)")
    for k in dc.KONS_AKHIR:
        dc.KONS_AKHIR[k] = st.number_input(f"{k} akhir", 0.0, 1e5, dc.KONS_AKHIR[k], key="c" + k)

skenario = dc.daftar_skenario()
nama = st.selectbox("Skenario", list(skenario))
deret = [float(x) for x in st.text_input("Deret Ca (mg/L)", "0,1,2,4,6,8,10").split(",") if x.strip()]

tab1, tab2, tab3 = st.tabs(["Tabel pipet", "Kalibrasi", "Hitung dari mL Ca"])
with tab1:
    df = dc.tabel(skenario[nama], deret)
    st.dataframe(df, use_container_width=True)
    st.download_button("Unduh CSV", df.to_csv(index=False), "deret_ca.csv")
with tab2:
    a = st.text_input("Absorbansi standar (urut sesuai deret, pisah koma)")
    A = [float(x) for x in a.split(",") if x.strip()]
    if len(A) >= 2 and len(A) == len(deret):
        m, b, r2 = dc.kalibrasi(deret, A)
        st.write(f"A = {m:.4f}·C + {b:.4f}  |  R² = {r2:.4f}")
        sam = st.number_input("Absorbansi sampel", value=0.0, format="%.4f")
        fp = st.number_input("Faktor pengenceran", value=1.0)
        st.success(f"Ca sampel = {dc.hitung_konsentrasi(sam, m, b, fp):.3f} mg/L")
        st.line_chart(pd.DataFrame({"A": A}, index=deret))
    elif A:
        st.warning(f"Jumlah absorbansi ({len(A)}) harus sama dengan deret Ca ({len(deret)}).")
with tab3:
    ml = st.number_input("mL stok Ca yang dipipet", 0.0, 100.0, 1.0)
    st.info(f"Konsentrasi Ca di labu {dc.V_AKHIR:g} mL = {dc.konsentrasi_dari_ml(ml, dc.STOK['Ca'], dc.V_AKHIR):.3f} mg/L")

st.header("Model 3D GBC Avanta")
html = Path(__file__).with_name("avanta_aas.html")
if html.exists():
    components.html(html.read_text(encoding="utf8"), height=720, scrolling=True)
else:
    st.warning("avanta_aas.html tidak ditemukan di folder yang sama.")
