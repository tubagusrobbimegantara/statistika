"""
Streamlit app interaktif: Simulasi Pelemparan Koin (Gaya Seeing Theory)

Fitur:
- Tombol "Flip the Coin" (sekali lempar) dan "Flip 100 times"
- Animasi sederhana koin (H atau T)
- Dua grafik terpisah: Frekuensi hasil percobaan dan Peluang teoretis (probabilitas tetap 0.5)

Cara jalankan:
streamlit run streamlit_coin_visual.py
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulasi Pelemparan Koin", layout="centered")

# --- Inisialisasi state ---
if "heads_count" not in st.session_state:
    st.session_state.heads_count = 0
if "tails_count" not in st.session_state:
    st.session_state.tails_count = 0
if "total_flips" not in st.session_state:
    st.session_state.total_flips = 0
if "last_flip" not in st.session_state:
    st.session_state.last_flip = "T"

# --- Pengantar Teori Peluang ---
st.title("Simulasi Pelemparan Koin — Peristiwa Acak 🇮🇩")
st.markdown(
    """
    ### Pengantar
    Keacakan atau ketidakpastian dapat kita jumpai di berbagai aspek kehidupan. **Teori peluang** adalah cabang matematika
    yang membantu kita memahami dan menganalisis peristiwa acak secara logis dan terukur. Nilai peluang menunjukkan
    seberapa besar kemungkinan suatu peristiwa terjadi, dengan nilai antara 0 dan 1 — di mana 0 berarti mustahil terjadi,
    sedangkan 1 berarti pasti terjadi.

    Salah satu contoh sederhana dari peristiwa acak adalah **pelemparan koin yang adil**, di mana terdapat dua hasil
    yang mungkin: kepala (*heads*) atau ekor (*tails*). Karena koin dianggap seimbang, peluang munculnya kepala atau ekor
    adalah sama, yaitu **1/2** atau 0,5.

    Dalam praktiknya, jika kita melempar koin beberapa kali, hasilnya bisa jadi tidak tepat 50% kepala dan 50% ekor.
    Namun, semakin banyak kita melempar koin, rata-rata hasilnya akan semakin mendekati 50%.
    Fenomena ini dikenal sebagai **Hukum Bilangan Besar (Law of Large Numbers)**.
    """
)

p_heads = 0.5  # Probabilitas tetap (koin adil)

col1, col2 = st.columns([1, 1])

# --- Kolom kiri: tombol dan tampilan koin ---
with col1:
    st.markdown("### 🎯 Lempar Koin")
    flip_one = st.button("Flip the Coin")
    flip_100 = st.button("Flip 100 times")

    # Gambar koin sederhana dengan teks biru donker dan outline
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center;'>
        <div style='display:inline-block; border-radius:50%; border:3px solid black; width:120px; height:120px; 
                    line-height:120px; font-size:56px; font-weight:bold; background-color:white; 
                    color:#001F54; -webkit-text-stroke: 2px #001F54;'>
            {st.session_state.last_flip}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Jalankan simulasi jika tombol ditekan
    rng = np.random.default_rng()
    if flip_one:
        flip = rng.random() < p_heads
        if flip:
            st.session_state.heads_count += 1
            st.session_state.last_flip = "H"
        else:
            st.session_state.tails_count += 1
            st.session_state.last_flip = "T"
        st.session_state.total_flips += 1

    if flip_100:
        flips = rng.random(100) < p_heads
        st.session_state.heads_count += flips.sum()
        st.session_state.tails_count += 100 - flips.sum()
        st.session_state.total_flips += 100
        st.session_state.last_flip = "H" if flips[-1] else "T"

# --- Kolom kanan: grafik ---
with col2:
    st.markdown("### 📊 Visualisasi Hasil")
    heads = st.session_state.heads_count
    tails = st.session_state.tails_count
    total = st.session_state.total_flips if st.session_state.total_flips > 0 else 1

    frekuensi_teramati = np.array([heads / total, tails / total])
    peluang_teoretis = np.array([0.5, 0.5])
    labels = ["H", "T"]

    # Dua kolom untuk grafik berdampingan
    gcol1, gcol2 = st.columns(2)

    # --- Grafik Frekuensi hasil percobaan ---
    with gcol1:
        fig_obs, ax_obs = plt.subplots(figsize=(3, 3.5))
        bars = ax_obs.bar(labels, frekuensi_teramati, color="#00C2A0")
        ax_obs.set_ylim(0, 1)
        ax_obs.set_ylabel("Proporsi hasil percobaan")
        ax_obs.set_title("Frekuensi Hasil Percobaan")
        for bar in bars:
            yval = bar.get_height()
            ax_obs.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f"{yval:.2f}", ha='center')
        st.pyplot(fig_obs)

    # --- Grafik Peluang teoretis ---
    with gcol2:
        fig_true, ax_true = plt.subplots(figsize=(3, 3.5))
        bars = ax_true.bar(labels, peluang_teoretis, color="#6EC5FF")
        ax_true.set_ylim(0, 1)
        ax_true.set_ylabel("Nilai peluang teoretis")
        ax_true.set_title("Peluang Secara Teori")
        for bar in bars:
            yval = bar.get_height()
            ax_true.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f"{yval:.2f}", ha='center')
        st.pyplot(fig_true)

# --- Statistik singkat ---
st.markdown("---")
st.subheader("📈 Statistik Ringkas")
st.write(f"Total lemparan: **{st.session_state.total_flips}**")
st.write(f"Kepala (H): {st.session_state.heads_count} ({st.session_state.heads_count / max(1, st.session_state.total_flips):.2%})")
st.write(f"Ekor (T): {st.session_state.tails_count} ({st.session_state.tails_count / max(1, st.session_state.total_flips):.2%})")

# --- Tombol reset ---
if st.button("🔄 Reset Simulasi"):
    st.session_state.heads_count = 0
    st.session_state.tails_count = 0
    st.session_state.total_flips = 0
    st.session_state.last_flip = "T"
    st.rerun()

# --- Penjelasan bawah ---
st.markdown(
    """
    ---
    **Catatan:** Karena koin dianggap adil, peluang munculnya kepala dan ekor adalah sama, yaitu 0,5.
    Semakin banyak lemparan dilakukan, hasil dari percobaan (frekuensi) akan semakin mendekati nilai peluang
    secara teori. Fenomena ini merupakan contoh nyata dari **Hukum Bilangan Besar (Law of Large Numbers)**.

    🔗 *Sumber inspirasi: Seeing Theory — Chance Events (Brown University)*
    """
)
