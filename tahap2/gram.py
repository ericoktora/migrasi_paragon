import mysql.connector
from datetime import datetime

# --- KONFIGURASI DATABASE ---
db_awal = mysql.connector.connect(
    host="localhost",
    user="eric",
    password="eric123",
    database="slims_paragon_db"
)

db_tujuan = mysql.connector.connect(
    host="localhost",
    user="eric",
    password="eric123",
    database="db_slims_paragon_aio"
)

cursor_awal = db_awal.cursor(dictionary=True)
cursor_tujuan = db_tujuan.cursor(dictionary=True)

# --- PEMETAAN ID_KODE_LAB KE KOLOM gram ---
kode_lab_mapping = {
    259: "bahan",
    260: "positif",
    261: "negatif",
    262: "lain",
    263: "kesan",
    264: "saran"
}

print("=== MULAI MIGRASI ===")

# --- LANGKAH 1: AMBIL DATA SUMBER ---
cursor_awal.execute("""
    SELECT * FROM transaksi_lab_detail
    WHERE id_kode_lab = 235
""")
data_sumber = cursor_awal.fetchall()

print(f"Total data ditemukan: {len(data_sumber)}")

for row in data_sumber:
    id_transaksi_lab = row["id_transaksi_lab"]

    # Ambil data gram berdasarkan id_transaksi_lab
    cursor_awal.execute("""
        SELECT * FROM transaksi_lab_gram
        WHERE id_transaksi_lab = %s
    """, (id_transaksi_lab,))
    gram = cursor_awal.fetchone()

    if not gram:
        print(f"❌ Tidak ada data GRAM untuk id_transaksi_lab: {id_transaksi_lab}")
        continue

    for id_kode_lab, kolom_nama in kode_lab_mapping.items():
        # Ambil isi kolom dari gram jika ada
        deskripsi_value = gram.get(kolom_nama) if gram.get(kolom_nama) else None

        # --- INSERT KE transaksi_lab_detail TUJUAN ---
        cursor_tujuan.execute("""
            INSERT INTO transaksi_lab_detail 
            (id_transaksi_lab, id_kode_lab, kode_tes, acc, validasi, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            id_transaksi_lab,
            id_kode_lab,
            kolom_nama,
            1,  # acc = 1
            1,  # validasi = 1
            datetime.now(),
            datetime.now()
        ))
        db_tujuan.commit()
        id_detail_baru = cursor_tujuan.lastrowid

        # --- INSERT KE transaksi_lab_deskripsi ---
        cursor_tujuan.execute("""
            INSERT INTO transaksi_lab_deskripsi 
            (id_transaksi_lab, id_transaksi_lab_detail, title, deskripsi, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            id_transaksi_lab,
            id_detail_baru,
            kolom_nama,
            deskripsi_value,
            datetime.now(),
            datetime.now()
        ))
        db_tujuan.commit()
        id_deskripsi_baru = cursor_tujuan.lastrowid

        # --- UPDATE HASIL DI transaksi_lab_detail ---
        hasil_value = f"id:{id_deskripsi_baru}"
        cursor_tujuan.execute("""
            UPDATE transaksi_lab_detail
            SET hasil = %s
            WHERE id_transaksi_lab_detail = %s
        """, (hasil_value, id_detail_baru))
        db_tujuan.commit()

        print(f"✔ id_transaksi_lab {id_transaksi_lab} → {kolom_nama} sukses (id_deskripsi={id_deskripsi_baru})")

print("=== MIGRASI SELESAI ===")

cursor_awal.close()
cursor_tujuan.close()
db_awal.close()
db_tujuan.close()
