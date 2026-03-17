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

cursor_awal.execute("SELECT * FROM kategori_alat_detail")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:
        row.update({
            'alias': row.get('kode_lis', '-'),

        })
        

        query = """
            INSERT INTO kategori_alat_detail (
                id_kategori_alat_detail, id_kategori_alat, id_kode_lab, no_item, kode_lis, alias, kali, created_at, updated_at
            ) VALUES (
                %(id_kategori_alat_detail)s, %(id_kategori_alat)s, %(id_kode_lab)s, %(no_item)s, %(kode_lis)s, %(alias)s, %(kali)s, %(created_at)s, %(updated_at)s
            )
        """
        cursor_tujuan.execute(query, row)
    except Exception as e:
        print(f"Gagal insert ID {row.get('id_kategori_alat_detail', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("Selesai memindahkan data kategori_alat_detail.")
