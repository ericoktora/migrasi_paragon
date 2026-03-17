import mysql.connector # type: ignore
from datetime import datetime

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
cursor_awal.execute("SELECT * FROM kode_lab")
data_awal = cursor_awal.fetchall()

for row in data_awal:
    try:

        metoda_value = row.get('metoda')
        if metoda_value in (None, '', 'NULL', 'null'):
            metoda_value = '-'
        row['metoda'] = metoda_value
        # Isi kolom tambahan & default agar tidak KeyError
        defaults = {
            'id_spesimen_snomed': None,
            'kode_loinc': None,
            'loinc_satuan': None,
            'type_loinc': None,
            'code_system': None,
            'flaging': 1,
            'nilai_default': None,
            'status': '0',
        }
        for k, v in defaults.items():
            row.setdefault(k, v)

        # Konversi datetime ke format timestamp string (jika ada)
        for time_field in ['created_at', 'updated_at']:
            if row.get(time_field) and not isinstance(row[time_field], datetime):
                try:
                    row[time_field] = datetime.strptime(row[time_field], "%Y-%m-%d %H:%M:%S")
                except Exception:
                    row[time_field] = None

        query = """
            INSERT INTO kode_lab (
                id_kode_lab, id_spesimen_snomed, id_sub_kategori, grub1, grub2, grub3, nama, en, kode_loinc, loinc_satuan, type_loinc, code_system, 
                kode_tes, kd_lis, satuan, status, nilai_rujukan, metoda, `case`, kode_his, harga, keterangan, info,
                koma, min,max, flaging, created_at, updated_at, nilai_default
            ) VALUES (
                %(id_kode_lab)s, %(id_spesimen_snomed)s, %(id_sub_kategori)s, %(grub1)s, %(grub2)s, %(grub3)s, %(nama)s, 
                %(nama_ing)s, %(kode_loinc)s, %(loinc_satuan)s, %(type_loinc)s, %(code_system)s, %(kode_tes)s, %(kd_lis)s, %(satuan)s, %(status)s, 
                %(nilai_rujukan)s, %(metoda)s, %(case)s, %(kode_his)s, %(harga)s, %(keterangan)s,
                %(keterangan)s, %(koma)s, %(kode_kel)s, %(satuan_ing)s, %(flaging)s, 
                %(created_at)s, %(updated_at)s, %(nilai_default)s
            )
        """
        cursor_tujuan.execute(query, row)

    except Exception as e:
        print(f"Gagal insert ID {row.get('id_kode_lab', 'UNKNOWN')}: {e}")

db_tujuan.commit()
print("✅ Selesai memindahkan data.")
