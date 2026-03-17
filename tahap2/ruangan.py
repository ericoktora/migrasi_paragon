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

cursor_awal.execute("SELECT * FROM ruangan")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:
        row.update({
            'kode_ruangan': None
        })

        

        query = """
            INSERT INTO ruangan (
                id_ruangan,  nama_ruangan, kode_his, created_at, updated_at
            ) VALUES (
                %(id_ruangan)s, %(nama_ruangan)s, %(kode_his)s, %(created_at)s, %(updated_at)s
            )
        """
        cursor_tujuan.execute(query, row)
    except Exception as e:
        print(f"Gagal insert ID {row.get('id_ruangan', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("Selesai memindahkan data ruangan.")
