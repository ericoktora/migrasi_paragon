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

cursor_awal.execute("SELECT * FROM kategori_catatan")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:
        

        query = """
            INSERT INTO kategori_catatan (
                id, nama, created_at, updated_at
            ) VALUES (
                %(id)s, %(nama)s, %(created_at)s, %(updated_at)s
            )
        """
        cursor_tujuan.execute(query, row)
    except Exception as e:
        print(f"Gagal insert ID {row.get('id', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("Selesai memindahkan data kategori_catatan.")
