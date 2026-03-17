import mysql.connector

# --- Koneksi ke database ---
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
cursor_tujuan = db_tujuan.cursor(dictionary=True)

print("🔍 Mengambil data dari database sumber...")

# Ambil data dari database awal
cursor_awal.execute("SELECT * FROM transaksi_lab_detail WHERE id_kode_lab = 163")
data_awal = cursor_awal.fetchall()

# Ambil data hasil (tabel referensi)
cursor_awal.execute("SELECT * FROM transaksi_lab_gdt")
data_gdt = cursor_awal.fetchall()

# Buat peta hasil berdasarkan id_transaksi_lab
hasil_map = {}
for row in data_gdt:
    hasil_map[row["id_transaksi_lab"]] = row

# Mapping id_kode_lab baru ke kolom hasil
kl_map = {
    252: "eritrosit",
    253: "lekosit",
    254: "trombosit",
    255: "kesan",
    256: "kesimpulan",
    257: "saran",
    258: "hbaealat",
}

total_rows = len(data_awal)
print(f"Total data yang akan dipindahkan: {total_rows}")

inserted_tld = 0
inserted_tl_desk = 0
batch_size = 100

# --- Proses migrasi ---
for i, row in enumerate(data_awal, start=1):
    id_tl = row["id_transaksi_lab"]
    id_tl_data = hasil_map.get(id_tl)

    if not id_tl_data:
        print(f"⚠️ id_transaksi_lab {id_tl} tidak ditemukan di transaksi_lab_gdt, dilewati.")
        continue

    for id_kl_new, kolom_kl in kl_map.items():
        try:
            # a. Insert ke db_tujuan.transaksi_lab_detail
            cursor_tujuan.execute(
                "INSERT INTO transaksi_lab_detail (id_transaksi_lab, id_kode_lab) VALUES (%s, %s)",
                (id_tl, id_kl_new)
            )
            db_tujuan.commit()
            id_tld_new = cursor_tujuan.lastrowid
            inserted_tld += 1

            # b. Ambil hasil dari kolom di gdt
            hasil_value = id_tl_data.get(kolom_kl)

            # c. Insert ke transaksi_lab_deskripsi
            cursor_tujuan.execute(
                "INSERT INTO transaksi_lab_deskripsi (id_transaksi_lab, id_transaksi_lab_detail, hasil) VALUES (%s, %s, %s)",
                (id_tl, id_tld_new, hasil_value)
            )
            db_tujuan.commit()
            id_tl_desk_new = cursor_tujuan.lastrowid
            inserted_tl_desk += 1

            # d. Update transaksi_lab_detail.hasil = "id:<id_tl_desk>"
            cursor_tujuan.execute(
                "UPDATE transaksi_lab_detail SET hasil = CONCAT('id:', %s) WHERE id_transaksi_lab = %s AND id_transaksi_lab_detail = %s",
                (id_tl_desk_new, id_tl, id_tld_new)
            )
            db_tujuan.commit()

        except Exception as e:
            db_tujuan.rollback()
            print(f"❌ Error pada id_transaksi_lab={id_tl}, id_kode_lab={id_kl_new}: {e}")

    # tampilkan progress tiap batch
    if i % batch_size == 0:
        print(f"Progress: {i}/{total_rows} data selesai.")

print("✅ Migrasi selesai.")
print(f"Total transaksi_lab_detail baru: {inserted_tld}")
print(f"Total transaksi_lab_deskripsi baru: {inserted_tl_desk}")

cursor_awal.close()
cursor_tujuan.close()
db_awal.close()
db_tujuan.close()


# # Query insert
# query = """
#     INSERT INTO transaksi_lab (
#         id_transaksi_lab, kode_transaksi_lab, no_order, no_registrasi,
#         id_pasien, umur_tahun, umur_bulan, umur_hari,
#         id_ruangan, id_asal, id_ruangan_awal, perusahaan, id_status,
#         id_petugas_lab, id_instalasi, id_kelas, id_cara_masuk, jenis_rawat,
#         klinik, nama_dokter_pengirim, alamat_dokter_pengirim, dokter_acc,
#         id_dokter, sampel, jenis_sampel, catatan, status, jenis_permeriksaan,
#         id_user, waktu_sampel, user_cekin, tgl_validasi, tgl_order,
#         tgl_print, proses, prioritas, status_prioritas, diagnose,
#         is_mcu, selesai, created_at, updated_at
#     ) VALUES (
#         %(id_transaksi_lab)s, %(kode_transaksi_lab)s, %(no_order)s, %(no_registrasi)s,
#         %(id_pasien)s, %(umur_tahun)s, %(umur_bulan)s, %(umur_hari)s,
#         %(id_ruangan)s, 1, %(id_ruangan_awal)s, %(perusahaan)s, %(id_status)s,
#         %(id_petugas_lab)s, %(id_instalasi)s, %(id_kelas)s, 1, 'Rawat Jalan',
#         %(klinik)s, %(nama_dokter_pengirim)s, %(alamat_dokter_pengirim)s, %(dokter_acc)s,
#         %(id_dokter)s, %(sampel)s, %(jenis_sampel)s, %(catatan)s, %(status)s, %(jenis_permeriksaan)s,
#         %(id_user)s, %(waktu_sampel)s, %(user_cekin)s, %(tgl_validasi)s, %(tgl_order)s,
#         %(tgl_print)s, %(proses)s, %(prioritas)s, %(status_prioritas)s, %(diagnose)s,
#         %(is_mcu)s, %(selesai)s, %(created_at)s, %(updated_at)s
#     )
# """

# # Batch insert
# batch_size = 10000   # bisa disesuaikan
# inserted = 0

# for i in range(0, total_rows, batch_size):
#     batch = data_awal[i:i+batch_size]
#     try:
#         cursor_tujuan.executemany(query, batch)
#         db_tujuan.commit()
#         inserted += len(batch)
#         print(f"Batch {i//batch_size + 1} berhasil dimasukkan ({len(batch)} row). "
#               f"Total inserted: {inserted}/{total_rows}")
#     except Exception as e:
#         db_tujuan.rollback()
#         print(f"Gagal insert batch {i//batch_size + 1}: {e}")

print("✅ Selesai memindahkan data transaksi_lab.")
