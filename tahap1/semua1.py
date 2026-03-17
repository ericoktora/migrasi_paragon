import subprocess

# Daftar file python yang ingin dijalankan
scripts = [
    "kode_lab.py",
    "kode_lab_dt.py",
    "jenis.py",
    "dokter.py",
    "grub.py",
    "grub_detail.py",
    "kategori_alat.py",
    "kategori_alat_detail.py",
    "kategori_catatan.py",
    "konten_ctt.py",
    "paket_lab.py",
    "paket_lab_dt.py",
    "stt_assur.py",
    "users.py",
    "query_tahap_1.py",
]

for script in scripts:
    print(f"\n🚀 Menjalankan: {script}")
    result = subprocess.run(["python3", script])
    
    if result.returncode != 0:
        print(f"❌ Gagal menjalankan {script}, hentikan proses.")
        break
    else:
        print(f"✅ Selesai: {script}")
