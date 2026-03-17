import mysql.connector

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

cursor_awal.execute("SELECT * FROM transaksi_paket_lab")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:

        query = """
            INSERT INTO transaksi_paket_lab (
                id_transaksi_paket_lab, id_transaksi_lab, id_paket_lab, id_harga_kultur,
                harga, created_at, updated_at
            ) VALUES (
                %(id_transaksi_paket_lab)s, %(id_transaksi_lab)s, %(id_paket_lab)s, %(id_harga_kultur)s,
                %(harga)s, %(created_at)s, %(updated_at)s
            )
        """
        cursor_tujuan.execute(query, row)
    except Exception as e:
        print(f"Gagal insert ID {row.get('id_transaksi_paket_lab', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("Selesai memindahkan data transaksi paket lab.")
