import mysql.connector

# =============================
# Fungsi helper
# =============================
def fix_datetime(val):
    if val in [0, '0', '', None, '0000-00-00 00:00:00']:
        return None
    return val

def fix_int(val, default=0):
    return int(val) if str(val).isdigit() else default


# =============================
# Koneksi database
# =============================
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


# =============================
# 1. Ambil ID valid
# =============================
cursor_tujuan.execute("SELECT id_transaksi_lab FROM transaksi_lab")
valid_transaksi_lab = {row[0] for row in cursor_tujuan.fetchall()}

cursor_tujuan.execute("SELECT id_transaksi_lab_detail FROM transaksi_lab_detail")
existing_details = {row[0] for row in cursor_tujuan.fetchall()}

print(f"ID transaksi_lab valid: {len(valid_transaksi_lab)}")
print(f"ID transaksi_lab_detail existing: {len(existing_details)}")


# =============================
# 2. Ambil data sumber
# =============================
cursor_awal.execute("""
SELECT DISTINCT
    tld.*,
    kl.kode_his AS kode_his,
    tl.kode_transaksi_lab AS id_lab,
    kl.satuan AS satuan
FROM transaksi_lab_detail tld
LEFT JOIN transaksi_lab tl 
    ON tld.id_transaksi_lab = tl.id_transaksi_lab
LEFT JOIN kode_lab kl 
    ON tld.id_kode_lab = kl.id_kode_lab
""")

data_joined = cursor_awal.fetchall()
print(f"Total data sumber: {len(data_joined)}")


# =============================
# 3. Filter & normalisasi data
# =============================
rows_to_insert = []

for row in data_joined:

    # Skip kalau tidak valid
    if row['id_transaksi_lab'] not in valid_transaksi_lab:
        continue

    if row['id_transaksi_lab_detail'] in existing_details:
        continue

    # =============================
    # FIX DATA
    # =============================
    row['acc'] = fix_int(row.get('acc'))

    # Fix datetime (INI YANG PENTING 🔥)
    row['waktu_sampel'] = fix_datetime(row.get('waktu_sampel'))
    row['created_at'] = fix_datetime(row.get('created_at'))
    row['updated_at'] = fix_datetime(row.get('updated_at'))

    # Optional: kalau ada field lain datetime
    # row['validasi'] = fix_datetime(row.get('validasi'))

    # =============================
    # DEFAULT VALUE
    # =============================
    row.update({
        'id_duplo_detail': None,
        'kode_hasil': '0',
        'id_asal': '1',
        'satuan': row.get('satuan') or None,
        'kode_his': row.get('kode_his') or None,
        'manual': 0,
        'status_note': 0,
        'note_hasil': None,
        'id_lab': None,
    })

    rows_to_insert.append(row)

print(f"Data siap insert: {len(rows_to_insert)}")


# =============================
# 4. Query insert
# =============================
query = """
INSERT INTO transaksi_lab_detail (
    id_transaksi_lab_detail, id_transaksi_lab, id_kode_lab,
    kode_his, kode_tes, id_lab, kode_hasil,
    hasil, satuan, cek_print, id_asal, flag, rujukan, ket,
    acc, user_acc, validasi, user_validasi, 
    harga, waktu_sampel, kritis, manual, status_note, note_hasil,
    created_at, updated_at
) VALUES (
    %(id_transaksi_lab_detail)s, %(id_transaksi_lab)s, %(id_kode_lab)s,
    %(kode_his)s, %(kode_tes)s, %(id_lab)s, %(kode_hasil)s,
    %(hasil)s, %(satuan)s, %(cek_print)s, %(id_asal)s, %(flag)s, %(rujukan)s, %(ket)s,
    %(acc)s, 1, %(acc)s, 1, 
    %(harga)s, %(waktu_sampel)s, 0, %(manual)s, %(status_note)s, %(note_hasil)s,
    %(created_at)s, %(updated_at)s
)
"""


# =============================
# 5. Insert batch
# =============================
batch_size = 10000
inserted = 0

for i in range(0, len(rows_to_insert), batch_size):
    batch = rows_to_insert[i:i+batch_size]

    try:
        cursor_tujuan.executemany(query, batch)
        db_tujuan.commit()

        inserted += len(batch)
        print(f"Batch {i//batch_size+1} OK ({len(batch)} row). Total: {inserted}/{len(rows_to_insert)}")

    except Exception as e:
        db_tujuan.rollback()
        print(f"❌ Gagal batch {i//batch_size+1}: {e}")

        # DEBUG (ambil 1 row penyebab)
        print("Contoh data error:")
        print(batch[0])
        break


print(f"✅ Selesai. Total berhasil: {inserted}, dilewati: {len(data_joined) - inserted}")