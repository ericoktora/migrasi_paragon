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
    


    
    cursor.execute("""
                
                INSERT INTO `kode_lab`(`nama`, `kode_tes`, `kd_lis`, `status`, `nilai_rujukan`, `metoda`, `case`, `kode_his`, `harga`, `koma`,`info`, `min`, `tipe_hasil`, `flaging`) VALUES 
                ('Eritrosit','1413','eri_gdt',1,'-','-','0','GDT',0,1,'GDT','GDT','Nar','1'),
                ('Leukosit','1414','leu_gdt',1,'-','-','0','GDT',0,1,'GDT','GDT','Nar','1'),
                ('Trombosit','1415','plt_gdt',1,'-','-','0','GDT',0,1,'GDT','GDT','Nar','1'),
                ('Kesan','1416','kes_gdt',1,'-','-','0','GDT',0,1,'GDT','GDT','Nar','1'),
                ('Kesimpulan','1417','kesi_gdt',1,'-','-','0','GDT',0,1,'GDT','GDT','Nar','1'),
                ('Saran','1418','sar_gdt',1,'-','-','0','GDT',0,1,'GDT','GDT','Nar','1'),
                ('hbaealat','1419','hbaealat',1,'-','-','0','GDT',0,1,'GDT','GDT','Nar','1'),
                ('Bahan','9611','bah_gram',1,'-','-','0','Pewarnaan Gram',0,1,'Pewarnaan Gram','Pewarnaan Gram','Nar','1'),
                ('Positif','9612','pos_gram',1,'-','-','0','Pewarnaan Gram',0,1,'Pewarnaan Gram','Pewarnaan Gram','Nar','1'),
                ('Negatif','9613','neg_gram',1,'-','-','0','Pewarnaan Gram',0,1,'Pewarnaan Gram','Pewarnaan Gram','Nar','1'),
                ('Lain','9614','lain_gram',1,'-','-','0','Pewarnaan Gram',0,1,'Pewarnaan Gram','Pewarnaan Gram','Nar','1'),
                ('Kesan','9615','kes_gram',1,'-','-','0','Pewarnaan Gram',0,1,'Pewarnaan Gram','Pewarnaan Gram','Nar','1'),
                ('Saran','9616','sar_gram',1,'-','-','0','Pewarnaan Gram',0,1,'Pewarnaan Gram','Pewarnaan Gram','Nar','1');
                
                """)
    
    cursor.execute("""
                
                INSERT INTO `grub` (`grub1`, `grub2`, `grub3`, `autoloader`) VALUES 
                ('HEMATOLOGI', 'Gambaran Darah Tepi', NULL, '0'),
                ('NO GROUP',NULL,NULL,'0'),
                ('MIKROBIOLOGI','Pewarnaan Gram',NULL,'0');

                
                """)

    cursor.execute("""
                
                INSERT INTO grub_detail (id_grub, id_kode_lab)
                SELECT 48, kode_lab.id_kode_lab
                FROM kode_lab
                WHERE kode_lab.id_kode_lab NOT IN (
                    SELECT grub_detail.id_kode_lab FROM grub_detail
                );
                
                """)

    



    conn.commit()
    print("✅ Semua update berhasil dijalankan.")
except Exception as e:
    print(f"❌ Error saat update: {e}")
    conn.rollback()

cursor.close()
conn.close()
