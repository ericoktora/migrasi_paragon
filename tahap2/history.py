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
cursor_awal.execute("SELECT * FROM history")
data_awal = cursor_awal.fetchall()

total_rows = len(data_awal)
print(f"Total data yang akan dipindahkan: {total_rows}")

# Query insert
query = """
    INSERT INTO history (
        id, id_transaksi_lab, id_user, aktivitas, keterangan, created_at, updated_at
    ) VALUES (
        %(id)s, %(id_transaksi_lab)s, %(id_user)s, %(aktivitas)s, %(keterangan)s, %(created_at)s, %(updated_at)s
    )
"""

# Bagi ke dalam batch
batch_size = 50000  # bisa kamu sesuaikan
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

print("✅ Selesai memindahkan data history.")
