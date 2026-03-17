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

cursor_awal.execute("SELECT * FROM kategori_alat")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:
        row.update({
            'status': 0,

        })
        

        query = """
            INSERT INTO kategori_alat (
                id_kategori_alat, nama, kode_lis, id_user, status, created_at, updated_at
            ) VALUES (
                %(id_kategori_alat)s, %(nama)s, %(kode_lis)s, %(id_user)s, %(status)s, %(created_at)s, %(updated_at)s
            )
        """
        cursor_tujuan.execute(query, row)
    except Exception as e:
        print(f"Gagal insert ID {row.get('id_kategori_alat', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("Selesai memindahkan data kategori_alat.")
