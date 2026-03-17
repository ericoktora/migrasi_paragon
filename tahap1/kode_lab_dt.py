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
cursor_awal.execute("SELECT * FROM kode_lab_detail")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:
       
        row.update({
            'urut': None,
            'single': None

        })

        query = """
            INSERT INTO kode_lab_detail (
                id_kode_lab_detail, id_kode_lab, urut, ket, `case`, sex, umur1, rangeu, umur2, waktu, nr1, rangen, nr2, single,
                nrujukan, created_at, updated_at
            ) VALUES (
                %(id_kode_lab_detail)s, %(id_kode_lab)s, %(urut)s, %(ket)s, %(case)s, %(sex)s, %(umur1)s, %(rangeu)s, %(umur2)s, 
                %(waktu)s, %(nr1)s, %(rangen)s, %(nr2)s, %(single)s, %(nrujukan)s, %(created_at)s, %(updated_at)s
            )
        """
        cursor_tujuan.execute(query, row)

    except Exception as e:
        print(f"Gagal insert ID {row.get('id_kode_lab_detail', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("Selesai memindahkan data.")
