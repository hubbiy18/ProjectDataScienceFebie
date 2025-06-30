import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Prediksi Dropout Mahasiswa", layout="wide")

# Cek apakah file model ada
if not os.path.exists("model_dropout_rf.pkl"):
    st.error("❌ Model tidak ditemukan. Pastikan file 'model_dropout_rf.pkl' tersedia.")
    st.stop()

# Load model
model = joblib.load("model_dropout_rf.pkl")

st.title("🎓 Aplikasi Prediksi Dropout Mahasiswa")
st.markdown("### Silakan lengkapi data mahasiswa berikut:")

def input_pengguna():
    status_perkawinan = st.selectbox("Status Perkawinan", [1, 2, 3, 4, 5, 6], format_func=lambda x: {
        1: "Lajang", 2: "Menikah", 3: "Duda/Janda", 4: "Cerai", 5: "Pasangan Tinggal Bersama", 6: "Pisah Secara Hukum"
    }[x])

    mode_aplikasi = st.selectbox("Cara Masuk Perguruan Tinggi", [1, 2, 5, 7, 10, 15, 16, 17, 18, 26, 27, 39, 42, 43, 44, 51, 53, 57])
    urutan_aplikasi = st.slider("Urutan Pilihan Program Studi", 0, 9, 0)
    jurusan = st.selectbox("Program Studi", [33, 171, 8014, 9003, 9070, 9085, 9119, 9130, 9147, 9238, 9254, 9500, 9556, 9670, 9773, 9853, 9991])
    waktu_kuliah = st.selectbox("Waktu Perkuliahan", [1, 0], format_func=lambda x: "Pagi / Reguler" if x == 1 else "Malam / Non-Reguler")

    kualifikasi_sebelumnya = st.selectbox("Jenjang Pendidikan Sebelumnya", [1,2,3,4,5,6,9,10,12,14,15,19,38,39,40,42,43])
    nilai_kualifikasi = st.slider("Nilai Akhir Pendidikan Sebelumnya", 0, 200, 150)
    kewarganegaraan = st.selectbox("Kewarganegaraan", [1,2,6,11,13,14,17,21,22,24,25,26,32,41,62,100,101,103,105,108,109])

    pendidikan_ibu = st.selectbox("Pendidikan Terakhir Ibu", list(range(1, 45)))
    pendidikan_ayah = st.selectbox("Pendidikan Terakhir Ayah", list(range(1, 45)))
    pekerjaan_ibu = st.selectbox("Pekerjaan Ibu", [0,1,2,3,4,5,6,7,8,9,10,90,99,122,123,125,131,132,134,141,143,144,151,152,153,171,173,175,191,192,193,194])
    pekerjaan_ayah = st.selectbox("Pekerjaan Ayah", [0,1,2,3,4,5,6,7,8,9,10,90,99,101,102,103,112,114,121,122,123,124,131,132,134,135,141,143,144,151,152,153,154,161,163,171,172,174,175,181,182,183,192,193,194,195])

    nilai_masuk = st.slider("Nilai Tes Masuk Universitas", 0, 200, 160)
    pindahan = st.selectbox("Apakah Mahasiswa Pindahan?", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")
    kebutuhan_khusus = st.selectbox("Memiliki Kebutuhan Khusus?", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")
    penunggak = st.selectbox("Menunggak Biaya Kuliah?", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")
    pembayaran_lunas = st.selectbox("Pembayaran Sudah Lunas?", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")
    jenis_kelamin = st.selectbox("Jenis Kelamin", [0, 1], format_func=lambda x: "Perempuan" if x == 0 else "Laki-laki")
    beasiswa = st.selectbox("Menerima Beasiswa?", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")
    usia = st.slider("Usia Saat Masuk Kuliah", 16, 70, 20)
    internasional = st.selectbox("Mahasiswa Internasional?", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")

    # Semester 1
    kredit_1 = st.slider("Semester 1 - Kredit Diakui", 0, 10, 0)
    ambil_1 = st.slider("Semester 1 - Mata Kuliah Diambil", 0, 10, 6)
    nilai_1 = st.slider("Semester 1 - Evaluasi Diikuti", 0, 10, 5)
    lulus_1 = st.slider("Semester 1 - Mata Kuliah Lulus", 0, 10, 4)
    rata_1 = st.slider("Semester 1 - Rata-rata Nilai", 0.0, 20.0, 10.0)
    tidak_ikut_1 = st.slider("Semester 1 - Tidak Ikut Evaluasi", 0, 10, 0)

    # Semester 2
    kredit_2 = st.slider("Semester 2 - Kredit Diakui", 0, 10, 0)
    ambil_2 = st.slider("Semester 2 - Mata Kuliah Diambil", 0, 10, 6)
    nilai_2 = st.slider("Semester 2 - Evaluasi Diikuti", 0, 10, 5)
    lulus_2 = st.slider("Semester 2 - Mata Kuliah Lulus", 0, 10, 4)
    rata_2 = st.slider("Semester 2 - Rata-rata Nilai", 0.0, 20.0, 10.0)
    tidak_ikut_2 = st.slider("Semester 2 - Tidak Ikut Evaluasi", 0, 10, 0)

    # Data Makro
    pengangguran = st.slider("Tingkat Pengangguran Nasional (%)", 0.0, 25.0, 7.0)
    inflasi = st.slider("Tingkat Inflasi Nasional (%)", 0.0, 10.0, 1.5)
    gdp = st.slider("Produk Domestik Bruto (GDP)", 0.0, 300.0, 200.0)

    return np.array([[status_perkawinan, mode_aplikasi, urutan_aplikasi, jurusan, waktu_kuliah,
                      kualifikasi_sebelumnya, nilai_kualifikasi, kewarganegaraan, pendidikan_ibu, pendidikan_ayah,
                      pekerjaan_ibu, pekerjaan_ayah, nilai_masuk, pindahan, kebutuhan_khusus,
                      penunggak, pembayaran_lunas, jenis_kelamin, beasiswa, usia, internasional,
                      kredit_1, ambil_1, nilai_1, lulus_1, rata_1, tidak_ikut_1,
                      kredit_2, ambil_2, nilai_2, lulus_2, rata_2, tidak_ikut_2,
                      pengangguran, inflasi, gdp]])

# Ambil data
data_input = input_pengguna()

# Tampilkan data input
st.markdown("###Data yang Anda Masukkan:")
kolom = ["Status Perkawinan", "Mode Aplikasi", "Urutan Aplikasi", "Program Studi", "Waktu Kuliah",
         "Kualifikasi Sebelumnya", "Nilai Kualifikasi", "Kewarganegaraan", "Pendidikan Ibu", "Pendidikan Ayah",
         "Pekerjaan Ibu", "Pekerjaan Ayah", "Nilai Masuk", "Pindahan", "Kebutuhan Khusus",
         "Penunggak", "Pembayaran Lunas", "Jenis Kelamin", "Beasiswa", "Usia", "Internasional",
         "Kredit S1", "Ambil S1", "Nilai S1", "Lulus S1", "Rata2 S1", "Tidak Ikut S1",
         "Kredit S2", "Ambil S2", "Nilai S2", "Lulus S2", "Rata2 S2", "Tidak Ikut S2",
         "Pengangguran", "Inflasi", "GDP"]

df = pd.DataFrame(data_input, columns=kolom)
st.dataframe(df)

# Prediksi
if st.button("Prediksi Dropout"):
    hasil = model.predict(data_input)
    label = {0: "Masih Kuliah", 1: "Dropout", 2: "Lulus"}[hasil[0]]
    st.success(f"Hasil Prediksi: **{label}**")

    # Probabilitas
    proba = model.predict_proba(data_input)[0]
    st.markdown("###Probabilitas:")
    proba_df = pd.DataFrame({
        "Kategori": ["Masih Kuliah", "Dropout", "Lulus"],
        "Probabilitas (%)": [proba[0]*100, proba[1]*100, proba[2]*100]
    })
    st.bar_chart(proba_df.set_index("Kategori"))
