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

cursor_awal.execute("SELECT * FROM dokter")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:
        

        query = """
            INSERT INTO dokter (
                id_dokter, nama_dokter, asal_dokter, kode_his, created_at, updated_at
            ) VALUES (
                %(id_dokter)s, %(nama_dokter)s, %(asal_dokter)s, %(kode_his)s, %(created_at)s, %(updated_at)s
            )
        """
        cursor_tujuan.execute(query, row)
    except Exception as e:
        print(f"Gagal insert ID {row.get('id_dokter', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("Selesai memindahkan data dokter.")
