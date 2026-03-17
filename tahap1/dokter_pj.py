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
cursor_awal.execute("SELECT * FROM dokter_pj")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:
       
        row.update({
            'alamat': None

        })

        query = """
            INSERT INTO dokter_pj (
                id, nama, sip, ttd, alamat, kode_his, created_at, updated_at
            ) VALUES (
                %(id)s, %(nama)s, %(sip)s, %(ttd)s, %(alamat)s, %(kode_his)s, %(created_at)s, %(updated_at)s
            )
        """
        cursor_tujuan.execute(query, row)

    except Exception as e:
        print(f"Gagal insert ID {row.get('id_dokter_pj', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("Selesai memindahkan data.")
