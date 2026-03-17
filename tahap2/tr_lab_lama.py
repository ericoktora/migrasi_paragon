import mysql.connector # type: ignore

# Koneksi ke database sumber
db_awal = mysql.connector.connect(
    host="localhost",
    user="eric",
    password="eric123",
    database="slims_paragon_db"
)

# Koneksi ke database tujuan
db_tujuan = mysql.connector.connect(
    host="localhost",
    user="eric",
    password="eric123",
    database="db_slims_paragon_aio"
)

cursor_awal = db_awal.cursor(dictionary=True)
cursor_tujuan = db_tujuan.cursor()

# Ambil data dari database awal
cursor_awal.execute("SELECT * FROM transaksi_lab")
data_awal = cursor_awal.fetchall()

total_rows = len(data_awal)
print(f"Total data yang akan dipindahkan: {total_rows}")

# Pre-processing data (konversi umur + mapping default)
for row in data_awal:
    row['umur_tahun'] = int(row['umur_tahun']) if str(row['umur_tahun']).isdigit() else 0
    row['umur_bulan'] = int(row['umur_bulan']) if str(row['umur_bulan']).isdigit() else 0
    row['umur_hari'] = int(row['umur_hari']) if str(row['umur_hari']).isdigit() else 0

# Query insert
query = """
    INSERT INTO transaksi_lab (
        id_transaksi_lab, kode_transaksi_lab, no_order, no_registrasi,
        id_pasien, umur_tahun, umur_bulan, umur_hari,
        id_ruangan, id_asal, id_ruangan_awal, perusahaan, id_status,
        id_petugas_lab, id_instalasi, id_kelas, id_cara_masuk, jenis_rawat,
        klinik, nama_dokter_pengirim, alamat_dokter_pengirim, dokter_acc,
        id_dokter, sampel, jenis_sampel, catatan, status, jenis_permeriksaan,
        id_user, waktu_sampel, user_cekin, tgl_validasi, tgl_order,
        tgl_print, proses, prioritas, status_prioritas, diagnose,
        is_mcu, selesai, created_at, updated_at, kesan, saran
    ) VALUES (
        %(id_transaksi_lab)s, %(kode_transaksi_lab)s, %(no_order)s, %(no_registrasi)s,
        %(id_pasien)s, %(umur_tahun)s, %(umur_bulan)s, %(umur_hari)s,
        %(id_ruangan)s, 1, %(id_ruangan_awal)s, %(perusahaan)s, %(id_status)s,
        %(id_petugas_lab)s, %(id_instalasi)s, %(id_kelas)s, 1, 'Rawat Jalan',
        %(klinik)s, %(nama_dokter_pengirim)s, %(alamat_dokter_pengirim)s, %(dokter_acc)s,
        %(id_dokter)s, %(sampel)s, %(jenis_sampel)s, %(catatan)s, %(status)s, %(jenis_permeriksaan)s,
        %(id_user)s, %(waktu_sampel)s, %(user_cekin)s, %(tgl_validasi)s, %(tgl_order)s,
        %(tgl_print)s, %(proses)s, %(prioritas)s, %(status_prioritas)s, %(diagnose)s,
        %(is_mcu)s, %(selesai)s, %(created_at)s, %(updated_at)s, %(kesan)s, %(saran)s
    )
"""

# Batch insert
batch_size = 10000   # bisa disesuaikan
inserted = 0

for i in range(0, total_rows, batch_size):
    batch = data_awal[i:i+batch_size]
    try:
        cursor_tujuan.executemany(query, batch)
        db_tujuan.commit()
        inserted += len(batch)
        print(f"Batch {i//batch_size + 1} berhasil dimasukkan ({len(batch)} row). "
              f"Total inserted: {inserted}/{total_rows}")
    except Exception as e:
        db_tujuan.rollback()
        print(f"Gagal insert batch {i//batch_size + 1}: {e}")

print("✅ Selesai memindahkan data transaksi_lab.")
