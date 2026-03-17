import mysql.connector # type: ignore

conn = mysql.connector.connect(
    host="localhost",
    user="eric",
    password="eric123",
    database="db_slims_paragon_aio"
)

cursor = conn.cursor()

# Jalankan semua query
try:
    


    cursor.execute("UPDATE kode_lab_detail set rangen = rangen + 100")
    
    cursor.execute("""
        UPDATE kode_lab_detail
        SET rangen = CASE
            WHEN rangen = 100 THEN 0
            WHEN rangen = 104 THEN 3
            WHEN rangen = 105 THEN 4
            WHEN rangen = 106 THEN 1
            WHEN rangen = 107 THEN 2
        END;
    """)

    cursor.execute("""
        UPDATE kode_lab 
        SET `case` = 4
            WHERE nilai_rujukan != '-' 
            AND nilai_rujukan != '0' 
            AND nilai_rujukan NOT LIKE '%~%' 
            AND nilai_rujukan NOT LIKE '%-%' 
            AND nilai_rujukan NOT LIKE '%≤%' 
            AND nilai_rujukan NOT LIKE '%≥%' 
            AND nilai_rujukan NOT LIKE '%.%';
    """)

    cursor.execute("""
        INSERT INTO kode_lab_detail (id_kode_lab, `case`, sex, rangeu, waktu, nr1,rangen,nr2, single, nrujukan,created_at,updated_at)
        SELECT id_kode_lab, 4,0,0,0,0,0,0, nilai_rujukan,nilai_rujukan, NOW() as created_at, NOW() as updated_at
        FROM kode_lab
        WHERE `case` = 4
    """)

    cursor.execute("UPDATE kode_lab SET `status` = 1")

    cursor.execute("""
        UPDATE kode_lab kl
        JOIN paket_lab_detail pld ON kl.id_kode_lab = pld.id_kode_lab
        SET `status` = 2
        WHERE kl.id_kode_lab = pld.id_kode_lab
    """)

    cursor.execute("UPDATE kode_lab SET tipe_hasil = 'Nar' WHERE kode_his='GDT'")

    cursor.execute("UPDATE asal_rujukan SET nama = 'RS PARAGON' WHERE id = 1")

    
    



    conn.commit()
    print("✅ Semua update berhasil dijalankan.")
except Exception as e:
    print(f"❌ Error saat update: {e}")
    conn.rollback()

cursor.close()
conn.close()
