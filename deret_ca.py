"""
Deret larutan analisis Ca (AAS) dengan pengganggu (PO4, SO4)
dan agen pelindung (Sr, La, EDTA), semua dalam matriks HNO3.

Skenario dibuat otomatis dari kombinasi:
  pengganggu : -, PO4, SO4, PO4+SO4
  pelindung  : -, Sr, La, EDTA
(pelindung tanpa pengganggu tidak dibuat)

Jalankan:  python deret_ca.py
"""
import numpy as np
import pandas as pd

# ================= KONFIGURASI =================
V_AKHIR = 50.0                 # mL, volume labu takar
HNO3_PERSEN = 1.0              # % v/v HNO3 pekat di larutan akhir
KONS_CA = [0, 1, 2, 4, 6, 8, 10]   # mg/L, deret standar Ca

STOK = {"Ca": 1000.0, "PO4": 1000.0, "SO4": 1000.0,
        "Sr": 10000.0, "La": 10000.0, "EDTA": 10000.0}      # mg/L
KONS_AKHIR = {"PO4": 100.0, "SO4": 100.0,
              "Sr": 1000.0, "La": 1000.0, "EDTA": 1000.0}   # mg/L di larutan akhir
# ===============================================

PENGGANGGU = {"tanpa pengganggu": [], "PO4": ["PO4"], "SO4": ["SO4"], "PO4 + SO4": ["PO4", "SO4"]}
PELINDUNG = {"tanpa pelindung": [], "Sr": ["Sr"], "La": ["La"], "EDTA": ["EDTA"]}


def daftar_skenario():
    """Return dict nama -> daftar zat tambahan."""
    out = {}
    for pn, pz in PENGGANGGU.items():
        for ln, lz in PELINDUNG.items():
            if not pz and lz:
                continue
            nama = "Ca saja" if not pz and not lz else "Ca + " + " + ".join(pz + lz)
            out[nama] = pz + lz
    return out


def ml_pipet(c_akhir, c_stok, v_akhir=V_AKHIR):
    """C1*V1 = C2*V2 -> mL stok yang dipipet."""
    return c_akhir * v_akhir / c_stok


def konsentrasi_dari_ml(ml_ca, c_stok=None, v_akhir=V_AKHIR):
    """Kebalikannya: mL stok Ca yang dipipet -> mg/L di larutan akhir."""
    c_stok = STOK["Ca"] if c_stok is None else c_stok
    return ml_ca * c_stok / v_akhir


def tabel(zat_tambahan, kons_ca=None, v_akhir=V_AKHIR):
    kons_ca = KONS_CA if kons_ca is None else kons_ca
    baris = []
    for ca in kons_ca:
        r = {"Ca (mg/L)": ca, "mL Ca": ml_pipet(ca, STOK["Ca"], v_akhir)}
        total = r["mL Ca"]
        for z in zat_tambahan:
            r[f"mL {z}"] = ml_pipet(KONS_AKHIR[z], STOK[z], v_akhir)
            total += r[f"mL {z}"]
        r["mL HNO3 pekat"] = HNO3_PERSEN / 100 * v_akhir
        total += r["mL HNO3 pekat"]
        r["mL aquades (ad)"] = v_akhir - total
        baris.append(r)
    df = pd.DataFrame(baris).round(3)
    if (df["mL aquades (ad)"] < 0).any():
        print("PERINGATAN: volume pipet melebihi labu takar; naikkan konsentrasi stok.")
    return df


def kalibrasi(konsentrasi, absorbansi):
    """Regresi linear A = m*C + b -> m, b, R2."""
    x, y = np.asarray(konsentrasi, float), np.asarray(absorbansi, float)
    m, b = np.polyfit(x, y, 1)
    return m, b, np.corrcoef(x, y)[0, 1] ** 2


def hitung_konsentrasi(abs_sampel, m, b, faktor_pengenceran=1.0):
    return (abs_sampel - b) / m * faktor_pengenceran


if __name__ == "__main__":
    pd.set_option("display.width", 200, "display.max_columns", None)
    semua = []
    for nama, zat in daftar_skenario().items():
        df = tabel(zat)
        print(f"\n=== {nama} ===")
        print(df.to_string(index=False))
        semua.append(df.assign(Skenario=nama))
    pd.concat(semua).to_csv("deret_ca.csv", index=False)
    print("\nSemua tabel disimpan ke deret_ca.csv")
