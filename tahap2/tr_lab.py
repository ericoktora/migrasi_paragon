import mysql.connector
import json

# === KONFIGURASI DATABASE ===
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

print("=== MULAI MIGRASI DATA transaksi_lab ===")

# === AMBIL DATA DARI DATABASE SUMBER ===
cursor_awal.execute("SELECT * FROM transaksi_lab")
data_awal = cursor_awal.fetchall()
total_rows = len(data_awal)
print(f"Total data ditemukan: {total_rows}")

# === PRE-PROCESSING DATA ===
for row in data_awal:
    # Konversi umur ke integer aman
    row["umur_tahun"] = int(row.get("umur_tahun", 0) or 0)
    row["umur_bulan"] = int(row.get("umur_bulan", 0) or 0)
    row["umur_hari"] = int(row.get("umur_hari", 0) or 0)

    # Pastikan kolom opsional selalu ada
    for key in ["kesan", "saran"]:
        value = row.get(key)
        if value in (None, "", "NULL"):
            row[key] = "[]"  # JSON kosong valid
        else:
            try:
                json.loads(value)  # sudah JSON valid
                row[key] = value
            except Exception:
                # bungkus teks biasa menjadi JSON array
                row[key] = json.dumps([str(value)])

# === QUERY INSERT (SAMA DENGAN STRUKTUR TUJUAN) ===
query = """
    INSERT INTO transaksi_lab (
        id_transaksi_lab, kode_transaksi_lab, no_order, no_registrasi,
        id_pasien, umur_tahun, umur_bulan, umur_hari,
        id_ruangan, id_asal, perusahaan, id_status,
        id_petugas_lab, id_cara_masuk, jenis_rawat,
        klinik, nama_dokter_pengirim, alamat_dokter_pengirim, dokter_acc,
        id_dokter, sampel, jenis_sampel, catatan, status, jenis_permeriksaan,
        id_user, waktu_sampel, user_cekin, tgl_validasi, tgl_order,
        tgl_print, proses, prioritas, status_prioritas, 
        selesai, created_at, updated_at, kesan, saran
    ) VALUES (
        %(id_transaksi_lab)s, %(kode_transaksi_lab)s, %(kode_transaksi_lab)s, %(no_registrasi)s,
        %(id_pasien)s, %(umur_tahun)s, %(umur_bulan)s, %(umur_hari)s,
        %(id_ruangan)s, 1, %(perusahaan)s, %(id_status)s,
        %(id_petugas_lab)s, 1, 'Rawat Jalan',
        %(klinik)s, %(nama_dokter_pengirim)s, %(alamat_dokter_pengirim)s, %(dokter_acc)s,
        1, %(sampel)s, %(jenis_sampel)s, %(catatan)s, %(status)s, %(jenis_permeriksaan)s,
        %(id_user)s, %(created_at)s, %(id_user)s, %(updated_at)s, %(tgl_order)s,
        %(updated_at)s, %(proses)s, %(prioritas)s, 0, 
        0, %(created_at)s, %(updated_at)s, %(kesan)s, %(saran)s
    )
"""

# === EKSEKUSI BATCH INSERT ===
batch_size = 5000
inserted = 0
batch_num = 0

for i in range(0, total_rows, batch_size):
    batch_num += 1
    batch = data_awal[i:i + batch_size]
    try:
        cursor_tujuan.executemany(query, batch)
        db_tujuan.commit()
        inserted += len(batch)
        print(f"✅ Batch {batch_num} berhasil ({inserted}/{total_rows})")
    except Exception as e:
        db_tujuan.rollback()
        print(f"❌ Gagal insert batch {batch_num}: {e}")

print("=== MIGRASI SELESAI ===")
print(f"Total berhasil dimasukkan: {inserted} dari {total_rows}")

# === TUTUP KONEKSI ===
cursor_awal.close()
cursor_tujuan.close()
db_awal.close()
db_tujuan.close()
