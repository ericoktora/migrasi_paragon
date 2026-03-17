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
    


    
    cursor.execute("INSERT INTO `users`(`name`, `email`, `sip`, `password`, `foto`, `level`, `created_at`, `updated_at`) VALUES ('SLIMS','slims','-','$2y$10$3akfQWlf7Pho.BDq0EJx3ua45iOsCSOEn3TUnI2CTqudmU1c0aPrq','/img/user.jpg','3','2025-09-09 09:23:54','2025-09-09 09:23:54')")

    



    conn.commit()
    print("✅ Semua update berhasil dijalankan.")
except Exception as e:
    print(f"❌ Error saat update: {e}")
    conn.rollback()

cursor.close()
conn.close()
