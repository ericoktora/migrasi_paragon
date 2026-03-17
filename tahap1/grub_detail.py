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

cursor_awal.execute("SELECT * FROM grub_detail")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:
        

        query = """
            INSERT INTO grub_detail (
                id_grub_detail, id_grub, id_kode_lab, created_at, updated_at
            ) VALUES (
                %(id_grub_detail)s, %(id_grub)s, %(id_kode_lab)s, %(created_at)s, %(updated_at)s
            )
        """
        cursor_tujuan.execute(query, row)
    except Exception as e:
        print(f"Gagal insert ID {row.get('id_grub_detail', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("Selesai memindahkan data grub_detail.")
