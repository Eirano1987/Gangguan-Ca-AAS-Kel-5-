# Analisis Ca dengan AAS (GBC Avanta)

Kalkulator deret larutan kalsium (Ca) untuk Atomic Absorption Spectroscopy, lengkap dengan model 3D interaktif GBC Avanta AAS.

## Fitur

- Tabel pipet (mL) untuk deret standar Ca dalam matriks HNO3
- 13 skenario otomatis:
  - Ca saja
  - Ca + PO4 atau SO4 (pengganggu)
  - PO4 atau SO4 + Sr, La, atau EDTA (pelindung)
  - PO4 + SO4, dengan atau tanpa Sr, La, atau EDTA
- Hitung konsentrasi Ca dari mL stok yang dipipet
- Kurva kalibrasi (A = mC + b, R²) dan konsentrasi sampel dengan faktor pengenceran
- Unduh tabel sebagai CSV
- Model 3D GBC Avanta: putar 360°, mode tembus pandang, animasi nyala dan berkas cahaya, serta efek pengganggu dan pelindung terhadap sinyal

## Isi repo

| File | Fungsi |
|------|--------|
| `app.py` | Aplikasi web (Streamlit) |
| `deret_ca.py` | Logika perhitungan, bisa dijalankan sendiri lewat terminal |
| `avanta_aas.html` | Model 3D AAS (three.js, dimuat dari CDN) |
| `requirements.txt` | Daftar library Python |

## Cara menjalankan

```bash
pip install -r requirements.txt
streamlit run app.py
```

Hanya perhitungan, tanpa web:

```bash
python deret_ca.py
```

Hasilnya dicetak di terminal dan disimpan ke `deret_ca.csv`.

## Konfigurasi

Nilai bawaan (volume labu 50 mL, stok, konsentrasi PO4/SO4/Sr/La/EDTA, % HNO3) hanya contoh. Ubah lewat sidebar aplikasi, atau di bagian KONFIGURASI pada `deret_ca.py`.

## Catatan

- Model 3D bersifat skematik, bukan replika presisi alat. Nilai absorbansi di model hanya ilustrasi.
- Model 3D butuh koneksi internet untuk memuat three.js.
- Pastikan `avanta_aas.html` berada satu folder dengan `app.py`.
