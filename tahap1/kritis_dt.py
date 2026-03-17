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

cursor_awal.execute("SELECT * FROM kritis_detail")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:

        row.update({
            'single': None

        })        
        

        query = """
            INSERT INTO kritis_detail (
                id, id_kritis, `case`, gender, umur1, rangeu, umur2,
                waktu, nr1, rangen, nr2, nrujukan, single, created_at, updated_at
            ) VALUES (
                %(id)s, %(id_kritis)s, %(case)s, %(gender)s, %(umur1)s, %(rangeu)s, 
                %(umur2)s, %(waktu)s, %(nr1)s, %(rangen)s, 
                %(nr2)s, %(nrujukan)s, %(single)s, %(created_at)s, %(updated_at)s
            )
        """
        cursor_tujuan.execute(query, row)
    except Exception as e:
        print(f"Gagal insert ID {row.get('id', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("Selesai memindahkan data kritis_detail.")
