#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI KURIKULUM K-8.0 — KOMPREHENSIF
30 Kurikulum | 6 Kelompok | Baca Modul + AI Generate
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime

# ===== ZUHRI AUTH =====
sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
KUR_DIR = os.path.join(HOME, "zuhri_os", "kurikulum")
DATA_DIR = os.path.join(KUR_DIR, "data")
PROG_DIR = os.path.join(KUR_DIR, "progress")
CONTENT_DIR = os.path.join(KUR_DIR, "content")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PROG_DIR, exist_ok=True)
os.makedirs(CONTENT_DIR, exist_ok=True)

# ===== WARNA =====
RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
BLUE="\033[94m"; MAGENTA="\033[95m"; CYAN="\033[96m"
GOLD="\033[93m"; WHITE="\033[97m"

# ============================================================
# PETA KURIKULUM K-8.0
# ============================================================
KURIKULUM = {
    "1": {"kelompok":"FONDASI BERPIKIR","warna":CYAN,"mapel":{
        "1.1":{"nama":"Logika","deskripsi":"Dasar penalaran: silogisme, deduksi, induksi, logika formal & informal.","modul":8},
        "1.2":{"nama":"Matematika","deskripsi":"Aritmatika, aljabar, kalkulus, geometri, statistika.","modul":12},
        "1.3":{"nama":"Problem Solving","deskripsi":"Strategi pemecahan masalah, heuristik, berpikir kritis.","modul":6},
        "1.4":{"nama":"Matriks","deskripsi":"Aljabar linear, operasi matriks, transformasi.","modul":5},
        "1.5":{"nama":"Simulasi","deskripsi":"Pemodelan sistem, Monte Carlo, agent-based.","modul":5},
        "1.6":{"nama":"Multi-Dimensi","deskripsi":"Berpikir sistem, tensor, geometri non-Euclidean.","modul":6}
    }},
    "2": {"kelompok":"SAINS ALAM","warna":GREEN,"mapel":{
        "2.1":{"nama":"Fisika","deskripsi":"Mekanika, termodinamika, elektromagnetik, kuantum.","modul":10},
        "2.2":{"nama":"Kimia","deskripsi":"Atom, molekul, reaksi, organik, biokimia.","modul":8},
        "2.3":{"nama":"Biologi","deskripsi":"Sel, genetika, evolusi, ekosistem.","modul":8},
        "2.4":{"nama":"Ekologi","deskripsi":"Interaksi makhluk hidup, konservasi, iklim.","modul":6},
        "2.5":{"nama":"Astronomi","deskripsi":"Tata surya, bintang, galaksi, kosmologi.","modul":8}
    }},
    "3": {"kelompok":"ILMU MANUSIA","warna":MAGENTA,"mapel":{
        "3.1":{"nama":"Psikologi","deskripsi":"Kognitif, behavioral, humanistik, sosial.","modul":8},
        "3.2":{"nama":"Neurosains","deskripsi":"Neuron, sinaps, otak, neuroplastisitas.","modul":8},
        "3.3":{"nama":"Kesadaran","deskripsi":"Fenomenologi, kesadaran diri, meditasi.","modul":6},
        "3.4":{"nama":"Kognisi","deskripsi":"Perhatian, memori, bahasa, pengambilan keputusan.","modul":6}
    }},
    "4": {"kelompok":"PENGETAHUAN & EPISTEMOLOGI","warna":GOLD,"mapel":{
        "4.1":{"nama":"Intuisi","deskripsi":"Pengetahuan non-verbal, insting, firasat.","modul":4},
        "4.2":{"nama":"Irfani","deskripsi":"Pengetahuan spiritual, tasawuf, gnosis.","modul":5},
        "4.3":{"nama":"Observasi","deskripsi":"Metode ilmiah, pengamatan, eksperimen.","modul":5},
        "4.4":{"nama":"Metakognisi","deskripsi":"Berpikir tentang berpikir, self-awareness.","modul":5},
        "4.5":{"nama":"Epistemologi","deskripsi":"Teori pengetahuan, justifikasi, skeptisisme.","modul":7}
    }},
    "5": {"kelompok":"KOMPUTASI & TEKNOLOGI","warna":BLUE,"mapel":{
        "5.1":{"nama":"Ilmu Komputer","deskripsi":"Hardware, software, OS, arsitektur.","modul":10},
        "5.2":{"nama":"Algoritma","deskripsi":"Struktur data, sorting, graph, DP.","modul":10},
        "5.3":{"nama":"Data","deskripsi":"Database, big data, analitik, visualisasi.","modul":8},
        "5.4":{"nama":"AI","deskripsi":"Machine learning, deep learning, NLP, CV.","modul":12},
        "5.5":{"nama":"Sistem & Jaringan","deskripsi":"Network, protokol, keamanan siber.","modul":8}
    }},
    "6": {"kelompok":"INTEGRASI","warna":RED,"mapel":{
        "6.1":{"nama":"Analisis Multidimensi","deskripsi":"Analisis lintas domain, sistem kompleks.","modul":7},
        "6.2":{"nama":"Sintesis Pengetahuan","deskripsi":"Menggabungkan disiplin ilmu.","modul":6},
        "6.3":{"nama":"Pemodelan","deskripsi":"Model matematis, simulasi, prediktif.","modul":7},
        "6.4":{"nama":"Eksplorasi Ilmiah","deskripsi":"Riset, metodologi, publikasi.","modul":6},
        "6.5":{"nama":"Arsitektur Kognitif","deskripsi":"Desain sistem berpikir, integrasi AI.","modul":8}
    }}
}

# ============================================================
# UTIL
# ============================================================
def get_id_badge():
    if not ZUHRI_ID_OK:
        return f"{YELLOW}⚠️  TANPA ZUHRI ID{RESET}"
    i = load_identity()
    if i:
        return f"{GREEN}✅ {i['name']}{RESET}"
    return f"{YELLOW}⚠️  TANPA ZUHRI ID{RESET}"

def load_progress():
    if not ZUHRI_ID_OK: return {}
    i = load_identity()
    if not i: return {}
    f = os.path.join(PROG_DIR, f"{i['zuhri_id']}.json")
    if os.path.exists(f):
        return json.load(open(f))
    return {}

def save_progress(data):
    if not ZUHRI_ID_OK: return
    i = load_identity()
    if not i: return
    f = os.path.join(PROG_DIR, f"{i['zuhri_id']}.json")
    json.dump(data, open(f, "w"), indent=2)

def total_mapel():
    return sum(len(v['mapel']) for v in KURIKULUM.values())

def total_modul():
    return sum(mv['modul'] for v in KURIKULUM.values() for mv in v['mapel'].values())

def cek_ollama():
    """Cek apakah Ollama berjalan"""
    try:
        r = subprocess.run(["pgrep","ollama"], capture_output=True)
        return r.returncode == 0
    except:
        return False

# ============================================================
# AI GENERATE MODUL
# ============================================================
def generate_materi(mk, modul_num, mapel_nama):
    """Generate materi modul pakai AI"""
    content_file = os.path.join(CONTENT_DIR, f"{mk}_modul_{modul_num}.txt")
    
    print(f"\n{YELLOW}⏳ Materi belum ada. Generate pakai AI (phi)...{RESET}")
    print(f"{DIM}   Mohon tunggu 30-90 detik...{RESET}\n")
    
    if not cek_ollama():
        print(f"{YELLOW}⚠️  Ollama belum jalan. Menjalankan...{RESET}")
        try:
            subprocess.Popen(["ollama","serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(3)
        except: pass
    
    prompt = f"""Buat materi pembelajaran Bahasa Indonesia:

Mapel: {mapel_nama}
Modul: {modul_num}

Format WAJIB:
# {mapel_nama} — Modul {modul_num}

## Tujuan Pembelajaran
- [3-5 poin]

## Pendahuluan
[2-3 paragraf]

## Materi Inti
[5-7 konsep, jelaskan masing-masing]

## Contoh & Aplikasi
[2-3 contoh nyata]

## Latihan Soal
[5 soal]

## Ringkasan
[2-3 paragraf]

## Referensi
[3-5 referensi]

Maks 1200 kata. Langsung mulai."""

    try:
        result = subprocess.run(["ollama","run","phi",prompt], 
                               capture_output=True, text=True, timeout=180)
        if result.stdout:
            with open(content_file, "w") as f:
                f.write(result.stdout)
            print(f"{GREEN}✅ Materi tersimpan!{RESET}\n")
            return content_file
        else:
            print(f"{RED}❌ Gagal generate materi{RESET}\n")
            return None
    except subprocess.TimeoutExpired:
        print(f"{YELLOW}⚠️  Timeout. Coba lagi nanti.{RESET}\n")
        return None
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}\n")
        return None

# ============================================================
# TAMPILKAN PETA
# ============================================================
def tampilkan_peta():
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  🧬 ZUHRI KURIKULUM K-8.0 — PETA KOMPREHENSIF                          ║
║  ────────────────────────────────────────────────────────────────────    ║
║  Total: {total_mapel()} Kurikulum | {total_modul()} Modul | 6 Kelompok                            ║
║  Operator: {get_id_badge()}
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    for k, kel in KURIKULUM.items():
        w = kel['warna']
        print(f"{BOLD}{w}━━━ KELOMPOK {k} — {kel['kelompok']} ━━━{RESET}\n")
        for mk, mv in kel['mapel'].items():
            print(f"  {GOLD}{mk}{RESET}  {BOLD}{mv['nama']}{RESET}")
            print(f"        {DIM}{mv['deskripsi']}{RESET}")
            print(f"        {CYAN}📚 {mv['modul']} modul{RESET}")
            print()
        print()

def tampilkan_kelompok(k):
    if k not in KURIKULUM:
        return
    kel = KURIKULUM[k]
    w = kel['warna']
    print(f"""
{BOLD}{w}╔══════════════════════════════════════════════════════════════════════════╗
║  📚 KELOMPOK {k} — {kel['kelompok']}
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
""")
    for mk, mv in kel['mapel'].items():
        print(f"  {GOLD}{mk}{RESET}  {BOLD}{mv['nama']}{RESET}")
        print(f"        {DIM}{mv['deskripsi']}{RESET}")
        print(f"        {CYAN}📚 {mv['modul']} modul{RESET}")
        print()

# ============================================================
# BELAJAR MODUL
# ============================================================
def belajar(mk):
    mapel = None
    for k, kel in KURIKULUM.items():
        if mk in kel['mapel']:
            mapel = kel['mapel'][mk]
            warna = kel['warna']
            kelompok = kel['kelompok']
            break
    
    if not mapel:
        print(f"{RED}❌ Kurikulum tidak ditemukan{RESET}")
        return
    
    prog = load_progress()
    prog_key = f"kurikulum_{mk}"
    done = prog.get(prog_key, {}).get('done', [])
    
    while True:
        os.system('clear')
        print(f"""
{BOLD}{warna}╔══════════════════════════════════════════════════════════════════════════╗
║  📖 {mapel['nama']} — {kelompok}
║  ────────────────────────────────────────────────────────────────────    ║
║  {mapel['deskripsi']}
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
""")
        
        total_modul_num = mapel['modul']
        print(f"  {BOLD}Progress:{RESET} {len(done)}/{total_modul_num} modul\n")
        
        for i in range(1, total_modul_num + 1):
            st = f"{GREEN}✅{RESET}" if i in done else f"{DIM}◯{RESET}"
            content_file = os.path.join(CONTENT_DIR, f"{mk}_modul_{i}.txt")
            avail = f"{GOLD}📖{RESET}" if os.path.exists(content_file) else f"{DIM}📄{RESET}"
            print(f"  {st} {avail} Modul {i}")
        
        print(f"\n  {DIM}0. Kembali{RESET}")
        print(f"  {DIM}99. Reset progress{RESET}\n")
        
        try:
            c = input(f"{GOLD}Pilih modul: {RESET}").strip()
            if c == "0": break
            if c == "99":
                prog[prog_key] = {"done": []}
                save_progress(prog)
                done = []
                continue
            
            mi = int(c)
            if 1 <= mi <= total_modul_num:
                content_file = os.path.join(CONTENT_DIR, f"{mk}_modul_{mi}.txt")
                os.system('clear')
                
                if os.path.exists(content_file):
                    # Tampilkan materi
                    print(f"{BOLD}{warna}╔══════════════════════════════════════════════════════════════════════════╗")
                    print(f"║  📚 {mapel['nama']} — MODUL {mi}")
                    print(f"╚══════════════════════════════════════════════════════════════════════════╝{RESET}\n")
                    with open(content_file) as f:
                        print(f.read())
                    print(f"\n{DIM}{'─'*70}{RESET}")
                    aksi = input(f"{GOLD}[selesai/kembali]: {RESET}").strip().lower()
                    if aksi == "selesai":
                        if mi not in done:
                            done.append(mi)
                            prog[prog_key] = {"done": done}
                            save_progress(prog)
                            if ZUHRI_ID_OK:
                                log_verified(f"KURIKULUM: {mapel['nama']} Modul {mi}")
                            print(f"\n{GREEN}✅ Modul {mi} selesai!{RESET}\n")
                        input(f"{DIM}Tekan Enter...{RESET}")
                else:
                    # Belum ada materi → tanya generate
                    print(f"{BOLD}{warna}╔══════════════════════════════════════════════════════════════════════════╗")
                    print(f"║  📚 {mapel['nama']} — MODUL {mi}")
                    print(f"╚══════════════════════════════════════════════════════════════════════════╝{RESET}\n")
                    print(f"{YELLOW}⚠️  Materi modul ini belum dibuat.{RESET}\n")
                    print(f"Generate materi dengan AI (phi)?")
                    print(f"  {GOLD}y{RESET} — Ya, generate sekarang")
                    print(f"  {GOLD}n{RESET} — Kembali\n")
                    
                    pilihan = input(f"{GOLD}Pilih (y/n): {RESET}").strip().lower()
                    if pilihan == "y":
                        generate_materi(mk, mi, mapel['nama'])
                        # Setelah generate, tampilkan
                        if os.path.exists(content_file):
                            print(f"{GREEN}✅ Materi siap dibaca!{RESET}\n")
                            with open(content_file) as f:
                                print(f.read())
                            print(f"\n{DIM}{'─'*70}{RESET}")
                            aksi = input(f"{GOLD}[selesai/kembali]: {RESET}").strip().lower()
                            if aksi == "selesai":
                                done.append(mi)
                                prog[prog_key] = {"done": done}
                                save_progress(prog)
                        input(f"{DIM}Tekan Enter...{RESET}")
        except ValueError:
            pass
        except KeyboardInterrupt:
            break

# ============================================================
# STATISTIK
# ============================================================
def show_stats():
    prog = load_progress()
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  📊 STATISTIK KURIKULUM K-8.0                                          ║
║  Operator: {get_id_badge()}
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📚 TOTAL:{RESET}
  Kurikulum : {total_mapel()}
  Modul     : {total_modul()}
  Kelompok  : 6

{BOLD}📈 PROGRESS:{RESET}
""")
    
    total_done = 0
    for k, kel in KURIKULUM.items():
        w = kel['warna']
        print(f"  {BOLD}{w}Kelompok {k}: {kel['kelompok']}{RESET}")
        for mk, mv in kel['mapel'].items():
            key = f"kurikulum_{mk}"
            done = len(prog.get(key, {}).get('done', []))
            total = mv['modul']
            total_done += done
            pct = done / total * 100 if total else 0
            bar = "█" * int(pct/5) + "░" * (20 - int(pct/5))
            print(f"    {GOLD}{mk}{RESET} {mv['nama']:20} {done:2}/{total:2} {bar} {pct:.0f}%")
        print()
    
    pct = total_done / total_modul() * 100 if total_modul() else 0
    print(f"{BOLD}🎯 TOTAL: {total_done}/{total_modul()} ({pct:.1f}%){RESET}\n")

# ============================================================
# MENU
# ============================================================
def belajar_menu():
    os.system('clear')
    print(f"\n{BOLD}{CYAN}📖 PILIH KURIKULUM{RESET}\n")
    items = []
    for k, kel in KURIKULUM.items():
        for mk, mv in kel['mapel'].items():
            items.append((mk, mv))
    for i, (mk, mv) in enumerate(items, 1):
        print(f"  {GOLD}{i}.{RESET} {mk} — {mv['nama']}")
    try:
        c = int(input(f"\n{CYAN}Pilih: {RESET}")) - 1
        if 0 <= c < len(items):
            belajar(items[c][0])
    except: pass

def menu():
    while True:
        os.system('clear')
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  🧬 ZUHRI KURIKULUM K-8.0 — KOMPREHENSIF                               ║
║  ────────────────────────────────────────────────────────────────────    ║
║  {total_mapel()} Kurikulum | {total_modul()} Modul | 6 Kelompok                            ║
║  Operator: {get_id_badge()}
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🗺️  Peta Kurikulum Lengkap
  {GOLD}2.{RESET}  📚 Kelompok 1 — Fondasi Berpikir
  {GOLD}3.{RESET}  🌿 Kelompok 2 — Sains Alam
  {GOLD}4.{RESET}  🧠 Kelompok 3 — Ilmu Manusia
  {GOLD}5.{RESET}  🔮 Kelompok 4 — Pengetahuan & Epistemologi
  {GOLD}6.{RESET}  💻 Kelompok 5 — Komputasi & Teknologi
  {GOLD}7.{RESET}  🎯 Kelompok 6 — Integrasi
  {GOLD}8.{RESET}  📖 Belajar (Baca Modul)
  {GOLD}9.{RESET}  📊 Statistik Progress
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-9): {RESET}").strip()
            if c == "0": break
            elif c == "1":
                os.system('clear'); tampilkan_peta(); input(f"\n{DIM}Enter...{RESET}")
            elif c in ["2","3","4","5","6","7"]:
                os.system('clear'); tampilkan_kelompok(str(int(c)-1)); input(f"\n{DIM}Enter...{RESET}")
            elif c == "8":
                belajar_menu()
            elif c == "9":
                os.system('clear'); show_stats(); input(f"\n{DIM}Enter...{RESET}")
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "peta": tampilkan_peta()
        elif cmd == "stats": show_stats()
        else: menu()
    else: menu()
