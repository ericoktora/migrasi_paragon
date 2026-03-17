import mysql.connector # type: ignore

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
cursor_tujuan = db_tujuan.cursor()

# Ambil data dari sumber
cursor_awal.execute("SELECT * FROM duplo")
data_awal = cursor_awal.fetchall()

# Query insert
query = """
    INSERT INTO duplo (
        id_duplo, kode_transaksi_lab, alat, date_tr, date_run, created_at, updated_at
    ) VALUES (
        %(id_duplo)s, %(kode_transaksi_lab)s, %(alat)s, %(date_tr)s, %(date_run)s, %(created_at)s, %(updated_at)s
    )
"""

# Bagi ke dalam batch
batch_size = 10000  # bisa disesuaikan
for i in range(0, len(data_awal), batch_size):
    batch = data_awal[i:i+batch_size]
    try:
        cursor_tujuan.executemany(query, batch)
        db_tujuan.commit()
        print(f"Batch {i//batch_size + 1} berhasil dimasukkan ({len(batch)} row).")
    except Exception as e:
        db_tujuan.rollback()
        print(f"Gagal insert batch {i//batch_size + 1}: {e}")

print("Selesai memindahkan data duplo.")