#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI KURIKULUM — AI GENERATOR MODUL
Generate materi modul otomatis dengan AI
"""

import os
import sys
import json
import subprocess

HOME = os.path.expanduser("~")
KUR_DIR = os.path.join(HOME, "zuhri_os", "kurikulum")
CONTENT_DIR = os.path.join(KUR_DIR, "content")
os.makedirs(CONTENT_DIR, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"

KURIKULUM = {
    "1.1": {"nama":"Logika","total":8},
    "1.2": {"nama":"Matematika","total":12},
    "1.3": {"nama":"Problem Solving","total":6},
    "1.4": {"nama":"Matriks","total":5},
    "1.5": {"nama":"Simulasi","total":5},
    "1.6": {"nama":"Multi-Dimensi","total":6},
    "2.1": {"nama":"Fisika","total":10},
    "2.2": {"nama":"Kimia","total":8},
    "2.3": {"nama":"Biologi","total":8},
    "2.4": {"nama":"Ekologi","total":6},
    "2.5": {"nama":"Astronomi","total":8},
    "3.1": {"nama":"Psikologi","total":8},
    "3.2": {"nama":"Neurosains","total":8},
    "3.3": {"nama":"Kesadaran","total":6},
    "3.4": {"nama":"Kognisi","total":6},
    "4.1": {"nama":"Intuisi","total":4},
    "4.2": {"nama":"Irfani","total":5},
    "4.3": {"nama":"Observasi","total":5},
    "4.4": {"nama":"Metakognisi","total":5},
    "4.5": {"nama":"Epistemologi","total":7},
    "5.1": {"nama":"Ilmu Komputer","total":10},
    "5.2": {"nama":"Algoritma","total":10},
    "5.3": {"nama":"Data","total":8},
    "5.4": {"nama":"AI","total":12},
    "5.5": {"nama":"Sistem & Jaringan","total":8},
    "6.1": {"nama":"Analisis Multidimensi","total":7},
    "6.2": {"nama":"Sintesis Pengetahuan","total":6},
    "6.3": {"nama":"Pemodelan","total":7},
    "6.4": {"nama":"Eksplorasi Ilmiah","total":6},
    "6.5": {"nama":"Arsitektur Kognitif","total":8},
}

def generate_modul(mk, modul_num, mapel_nama):
    """Generate materi modul dengan AI"""
    
    content_file = os.path.join(CONTENT_DIR, f"{mk}_modul_{modul_num}.txt")
    
    if os.path.exists(content_file):
        return content_file
    
    prompt = f"""Buat materi pembelajaran lengkap dalam Bahasa Indonesia untuk:

Mata Pelajaran: {mapel_nama}
Modul: {modul_num}
Level: Kurikulum K-8.0

Format materi (WAJIB ikuti):
1. JUDUL MODUL
2. TUJUAN PEMBELAJARAN (3-5 poin)
3. PENDAHULUAN (2-3 paragraf)
4. MATERI INTI (5-7 konsep utama, masing-masing dijelaskan)
5. CONTOH & APLIKASI
6. LATIHAN SOAL (5 soal)
7. RINGKASAN
8. REFERENSI LANJUTAN

Buat maksimal 1500 kata. Gunakan bahasa yang mudah dipahami. Langsung mulai tanpa pembuka."""

    print(f"  {CYAN}⏳ Generate {mk} modul {modul_num}...{RESET}")
    
    try:
        result = subprocess.run(
            ["ollama", "run", "phi", prompt],
            capture_output=True, text=True, timeout=120
        )
        
        if result.stdout:
            with open(content_file, "w") as f:
                f.write(result.stdout)
            print(f"  {GREEN}✅ Tersimpan: {os.path.basename(content_file)}{RESET}")
            return content_file
        else:
            print(f"  {RED}❌ Gagal generate{RESET}")
            return None
    except subprocess.TimeoutExpired:
        print(f"  {YELLOW}⚠️  Timeout{RESET}")
        return None
    except Exception as e:
        print(f"  {RED}❌ {e}{RESET}")
        return None

def generate_all(mapel_kode=None, limit=3):
    """Generate semua modul atau mapel tertentu"""
    
    if mapel_kode:
        items = [(mapel_kode, KURIKULUM[mapel_kode])]
    else:
        items = list(KURIKULUM.items())
    
    total_done = 0
    
    for mk, data in items:
        print(f"\n{BOLD}{CYAN}📚 {mk} — {data['nama']}{RESET}")
        
        for i in range(1, data['total'] + 1):
            content_file = os.path.join(CONTENT_DIR, f"{mk}_modul_{i}.txt")
            
            if os.path.exists(content_file):
                print(f"  {DIM}✓ Modul {i} sudah ada{RESET}")
                continue
            
            generate_modul(mk, i, data['nama'])
            total_done += 1
            
            if total_done >= limit and mapel_kode is None:
                print(f"\n{YELLOW}⚠️  Limit {limit} modul tercapai. Jalankan lagi untuk lanjut.{RESET}")
                return
    
    print(f"\n{GREEN}✅ Selesai! {total_done} modul baru digenerate.{RESET}")

def show_menu():
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🧬 ZUHRI KURIKULUM — AI GENERATOR MODUL                       ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 MENU:{RESET}
  {GOLD}1.{RESET} Generate 3 modul (test)
  {GOLD}2.{RESET} Generate 10 modul
  {GOLD}3.{RESET} Generate semua (lama, ~6 jam)
  {GOLD}4.{RESET} Generate mapel tertentu
  {GOLD}5.{RESET} Cek status modul
  {GOLD}0.{RESET} Keluar
""")

def cek_status():
    files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.txt')]
    total_modul = sum(d['total'] for d in KURIKULUM.values())
    
    print(f"\n{BOLD}{CYAN}📊 STATUS MODUL{RESET}\n")
    print(f"  Total modul    : {total_modul}")
    print(f"  Sudah dibuat   : {GREEN}{len(files)}{RESET}")
    print(f"  Belum dibuat   : {YELLOW}{total_modul - len(files)}{RESET}")
    
    pct = len(files) / total_modul * 100 if total_modul else 0
    bar = "█" * int(pct/5) + "░" * (20 - int(pct/5))
    print(f"  Progress       : {bar} {pct:.1f}%\n")

if __name__ == "__main__":
    # Cek Ollama
    try:
        result = subprocess.run(["pgrep", "ollama"], capture_output=True)
        if result.returncode != 0:
            print(f"{YELLOW}⚠️  Ollama belum jalan. Menjalankan...{RESET}")
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            import time
            time.sleep(3)
    except:
        pass
    
    while True:
        os.system('clear')
        show_menu()
        
        try:
            c = input(f"{GOLD}Pilih (0-5): {RESET}").strip()
            
            if c == "0": break
            elif c == "1":
                print(f"\n{CYAN}⏳ Generate 3 modul test...{RESET}\n")
                generate_all(limit=3)
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif c == "2":
                print(f"\n{CYAN}⏳ Generate 10 modul...{RESET}\n")
                generate_all(limit=10)
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif c == "3":
                print(f"\n{YELLOW}⚠️  Ini akan makan waktu ~6 jam.{RESET}")
                confirm = input(f"{CYAN}Lanjut? (y/n): {RESET}").strip().lower()
                if confirm == "y":
                    generate_all(limit=9999)
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif c == "4":
                print(f"\n{BOLD}Mapel tersedia:{RESET}")
                for k in KURIKULUM.keys():
                    print(f"  {k} — {KURIKULUM[k]['nama']}")
                mk = input(f"\n{CYAN}Kode mapel (misal 1.1): {RESET}").strip()
                if mk in KURIKULUM:
                    print(f"\n{CYAN}⏳ Generate {KURIKULUM[mk]['total']} modul {KURIKULUM[mk]['nama']}...{RESET}\n")
                    generate_all(mapel_kode=mk, limit=9999)
                else:
                    print(f"{RED}❌ Mapel tidak ditemukan{RESET}")
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif c == "5":
                cek_status()
                input(f"\n{DIM}Tekan Enter...{RESET}")
        except KeyboardInterrupt:
            break

