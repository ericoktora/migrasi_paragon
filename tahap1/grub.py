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
cursor_awal.execute("SELECT * FROM grub")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:
       
        row.update({
            'autoloader': 0

        })

        query = """
            INSERT INTO grub (
                id_grub, grub1, grub2, grub3, autoloader, created_at, updated_at
            ) VALUES (
                %(id_grub)s, %(grub1)s, %(grub2)s, %(grub3)s, %(autoloader)s, %(created_at)s, %(updated_at)s
            )
        """
        cursor_tujuan.execute(query, row)

    except Exception as e:
        print(f"Gagal insert ID {row.get('id_grub', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("Selesai memindahkan data.")
