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
    


    cursor.execute("UPDATE transaksi_lab set id_asal = 1;")

    cursor.execute("UPDATE transaksi_lab set id_cara_masuk = 1;")

    
    

    conn.commit()
    print("✅ Semua update berhasil dijalankan.")
except Exception as e:
    print(f"❌ Error saat update: {e}")
    conn.rollback()

cursor.close()
conn.close()
