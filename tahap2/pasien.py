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

cursor_awal.execute("SELECT * FROM pasien")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:
        # Tambahkan kolom baru di tujuan yang tidak ada di awal
        row.update({
            'alamat2': None,
            'alamat3': None,
            'alamat4': None,
            'email': None,
        })

        query = """
            INSERT INTO pasien (
                id_pasien, kode_rm, nik, nama, tempat_lahir, tgl_lahir,
                jenis_kelamin, alamat, alamat2, alamat3, alamat4,
                no_hp, email, kode_his, created_at, updated_at
            ) VALUES (
                %(id_pasien)s, %(kode_rm)s, %(nik)s, %(nama)s, %(tempat_lahir)s, %(tgl_lahir)s,
                %(jenis_kelamin)s, %(alamat)s, %(alamat2)s, %(alamat3)s, %(alamat4)s,
                %(no_hp)s, %(email)s, %(kode_his)s, %(created_at)s, %(updated_at)s
            )
        """
        cursor_tujuan.execute(query, row)
    except Exception as e:
        print(f"Gagal insert ID {row.get('id_pasien', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("Selesai memindahkan data pasien.")
