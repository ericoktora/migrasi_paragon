import subprocess

# Daftar file python yang ingin dijalankan
scripts = [
    "pasien.py",
    "ruangan.py",
    "tr_lab.py",
    "tr_lab_dt.py",
    "tr_pkt_lab.py",
    "duplo.py",
    "duplo_detail.py",
    "duplo_ori.py",
    "duplo_ori_dt.py",
    "history.py",
    "tat.py",
    "query_tahap_2.py"

]

for script in scripts:
    print(f"\n🚀 Menjalankan: {script}")
    result = subprocess.run(["python3", script])
    
    if result.returncode != 0:
        print(f"❌ Gagal menjalankan {script}, hentikan proses.")
        break
    else:
        print(f"✅ Selesai: {script}")
