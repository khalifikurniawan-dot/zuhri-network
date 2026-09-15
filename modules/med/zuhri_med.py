#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI MED — KESEHATAN DIGITAL
Catatan kesehatan, pengingat obat, database penyakit
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, secrets, time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
MED_DIR = os.path.join(HOME, "zuhri_os", "med")
DATA_DIR = os.path.join(MED_DIR, "data")
LOG_DIR = os.path.join(MED_DIR, "logs")
REM_DIR = os.path.join(MED_DIR, "reminders")
for d in [DATA_DIR, LOG_DIR, REM_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# DATABASE PENYAKIT (OFFLINE)
# ============================================================
PENYAKIT = {
    "demam": {"nama":"Demam","gejala":["Suhu > 38°C","Menggigil","Badan lemas","Sakit kepala"],"penyebab":"Infeksi virus/bakteri","pencegahan":["Cuci tangan","Istirahat cukup","Minum air"],"kapan_ke_dokter":"Demam > 3 hari atau suhu > 39°C"},
    "batuk": {"nama":"Batuk","gejala":["Batuk kering","Batuk berdahak","Tenggorokan gatal"],"penyebab":"Infeksi saluran napas, alergi","pencegahan":["Hindari asap","Minum air hangat"],"kapan_ke_dokter":"Batuk > 2 minggu atau berdarah"},
    "flu": {"nama":"Flu","gejala":["Hidung tersumbat","Bersin","Sakit tenggorokan","Demam ringan"],"penyebab":"Virus influenza","pencegahan":["Vaksin flu","Cuci tangan","Istirahat"],"kapan_ke_dokter":"Gejala berat atau > 7 hari"},
    "diare": {"nama":"Diare","gejala":["BAB cair > 3x","Mual","Perut kembung"],"penyebab":"Infeksi, makanan tidak higienis","pencegahan":["Cuci tangan","Makanan bersih","Air matang"],"kapan_ke_dokter":"Diare > 2 hari atau dehidrasi"},
    "maag": {"nama":"Maag","gejala":["Nyeri perut atas","Mual","Perut kembung","Sensasi terbakar"],"penyebab":"Asam lambung, stres, makanan pedas","pencegahan":["Makan teratur","Hindari pedas","Kelola stres"],"kapan_ke_dokter":"Nyeri hebat atau muntah darah"},
    "hipertensi": {"nama":"Hipertensi","gejala":["Sakit kepala","Pusing","Mimisan","Sesak napas"],"penyebab":"Genetik, gaya hidup, stres","pencegahan":["Kurangi garam","Olahraga","Hindari stres"],"kapan_ke_dokter":"Tekanan darah > 140/90 mmHg"},
    "diabetes": {"nama":"Diabetes","gejala":["Sering haus","Sering kencing","Lemas","Luka sulit sembuh"],"penyebab":"Genetik, obesitas, gaya hidup","pencegahan":["Diet sehat","Olahraga","Cek gula darah"],"kapan_ke_dokter":"Gula darah > 200 mg/dL"},
    "asma": {"nama":"Asma","gejala":["Sesak napas","Mengi","Dada terasa berat","Batuk malam"],"penyebab":"Alergi, genetik, lingkungan","pencegahan":["Hindari alergen","Pakai inhaler","Olahraga teratur"],"kapan_ke_dokter":"Serangan berat atau inhaler tidak membantu"},
    "alergi": {"nama":"Alergi","gejala":["Bersin","Gatal","Ruam","Mata berair"],"penyebab":"Reaksi imun berlebihan","pencegahan":["Hindari alergen","Catat pemicu"],"kapan_ke_dokter":"Sesak napas atau bengkak"},
    "sakit_kepala": {"nama":"Sakit Kepala","gejala":["Nyeri kepala","Pusing","Mual"],"penyebab":"Stres, kurang tidur, dehidrasi","pencegahan":["Istirahat cukup","Minum air","Kelola stres"],"kapan_ke_dokter":"Sakit hebat mendadak atau > 3 hari"},
}

# ============================================================
# UTIL
# ============================================================
def clear(): os.system('clear')

def user_file():
    if not ZUHRI_ID_OK: return None
    i = load_identity()
    if not i: return None
    return os.path.join(DATA_DIR, f"med_{i['zuhri_id']}.json")

def load_data():
    f = user_file()
    if f and os.path.exists(f):
        return json.load(open(f))
    return {
        "profile": {"nama":"","goldar":"","alergi":"","tinggi":0,"berat":0},
        "riwayat": [],
        "obat": [],
        "vital": [],
        "kontak_darurat": []
    }

def save_data(d):
    f = user_file()
    if f: json.dump(d, open(f, "w"), indent=2)

# ============================================================
# 1. PROFIL KESEHATAN
# ============================================================
def profil():
    clear()
    print(f"{BOLD}{CYAN}👤 PROFIL KESEHATAN{RESET}\n")
    
    d = load_data()
    p = d.get("profile", {})
    
    print(f"  Nama     : {p.get('nama', '-')}")
    print(f"  Gol. Darah: {p.get('goldar', '-')}")
    print(f"  Alergi   : {p.get('alergi', '-')}")
    print(f"  Tinggi   : {p.get('tinggi', '-')} cm")
    print(f"  Berat    : {p.get('berat', '-')} kg")
    print()
    
    if input("Edit profil? (y/n): ").strip().lower() == "y":
        p['nama'] = input(f"Nama [{p.get('nama','')}]: ").strip() or p.get('nama','')
        p['goldar'] = input(f"Gol. Darah [{p.get('goldar','')}]: ").strip() or p.get('goldar','')
        p['alergi'] = input(f"Alergi [{p.get('alergi','')}]: ").strip() or p.get('alergi','')
        try:
            p['tinggi'] = int(input(f"Tinggi (cm) [{p.get('tinggi',0)}]: ").strip() or p.get('tinggi',0))
        except: pass
        try:
            p['berat'] = int(input(f"Berat (kg) [{p.get('berat',0)}]: ").strip() or p.get('berat',0))
        except: pass
        
        d['profile'] = p
        save_data(d)
        
        if ZUHRI_ID_OK: log_verified("MED_PROFILE_UPDATE")
        print(f"\n{GREEN}✅ Profil disimpan{RESET}")
    
    input(f"\n{DIM}Enter...{RESET}")

# ============================================================
# 2. RIWAYAT KESEHATAN
# ============================================================
def riwayat():
    while True:
        clear()
        print(f"{BOLD}{CYAN}📋 RIWAYAT KESEHATAN{RESET}\n")
        
        d = load_data()
        riw = d.get("riwayat", [])
        
        if riw:
            for i, r in enumerate(riw[-10:], 1):
                print(f"  {GOLD}{i}.{RESET} [{r['tanggal'][:10]}] {r['keluhan']}")
                if r.get('catatan'):
                    print(f"     {DIM}{r['catatan']}{RESET}")
        else:
            print(f"  {YELLOW}Belum ada riwayat{RESET}")
        
        print(f"\n  {GOLD}a.{RESET} Tambah")
        print(f"  {GOLD}0.{RESET} Kembali")
        
        c = input(f"\n{GOLD}Pilih: {RESET}").strip().lower()
        
        if c == "0": break
        elif c == "a":
            keluhan = input("📝 Keluhan: ").strip()
            catatan = input("📄 Catatan (obat/tindakan): ").strip()
            if keluhan:
                riw.append({
                    "id": secrets.token_hex(4),
                    "tanggal": datetime.now().isoformat(),
                    "keluhan": keluhan,
                    "catatan": catatan
                })
                d['riwayat'] = riw
                save_data(d)
                if ZUHRI_ID_OK: log_verified(f"MED_RIWAYAT: {keluhan[:30]}")
                print(f"{GREEN}✅ Ditambahkan{RESET}")
                time.sleep(1)

# ============================================================
# 3. PENGINGAT OBAT
# ============================================================
def obat():
    while True:
        clear()
        print(f"{BOLD}{CYAN}💊 PENGINGAT OBAT{RESET}\n")
        
        d = load_data()
        obs = d.get("obat", [])
        
        if obs:
            for i, o in enumerate(obs, 1):
                print(f"  {GOLD}{i}.{RESET} {o['nama']} — {o['dosis']} @ {', '.join(o['jadwal'])}")
        else:
            print(f"  {YELLOW}Belum ada obat{RESET}")
        
        print(f"\n  {GOLD}a.{RESET} Tambah obat")
        print(f"  {GOLD}0.{RESET} Kembali")
        
        c = input(f"\n{GOLD}Pilih: {RESET}").strip().lower()
        
        if c == "0": break
        elif c == "a":
            nama = input("💊 Nama obat: ").strip()
            dosis = input("📏 Dosis: ").strip()
            jadwal = input("⏰ Jadwal (jam, pisah koma): ").strip()
            if nama and jadwal:
                jadwal_list = [j.strip() for j in jadwal.split(",") if j.strip()]
                obs.append({
                    "id": secrets.token_hex(4),
                    "nama": nama,
                    "dosis": dosis,
                    "jadwal": jadwal_list,
                    "dibuat": datetime.now().isoformat()
                })
                d['obat'] = obs
                save_data(d)
                if ZUHRI_ID_OK: log_verified(f"MED_OBAT: {nama}")
                print(f"{GREEN}✅ Obat ditambahkan{RESET}")
                time.sleep(1)

# ============================================================
# 4. DATABASE PENYAKIT
# ============================================================
def cari_penyakit():
    clear()
    print(f"{BOLD}{CYAN}📚 DATABASE PENYAKIT{RESET}\n")
    print("Kata kunci (nama/gejala): ", end="")
    q = input().strip().lower()
    
    if not q:
        return
    
    clear()
    print(f"{BOLD}{CYAN}🔍 Hasil: '{q}'{RESET}\n")
    
    found = False
    for key, p in PENYAKIT.items():
        if q in key or q in p['nama'].lower() or any(q in g.lower() for g in p['gejala']):
            found = True
            print(f"{BOLD}{GOLD}📖 {p['nama']}{RESET}\n")
            print(f"  {CYAN}Gejala:{RESET}")
            for g in p['gejala']:
                print(f"    • {g}")
            print(f"  {CYAN}Penyebab:{RESET} {p['penyebab']}")
            print(f"  {CYAN}Pencegahan:{RESET}")
            for pr in p['pencegahan']:
                print(f"    • {pr}")
            print(f"  {CYAN}Kapan ke dokter:{RESET} {p['kapan_ke_dokter']}")
            print()
    
    if not found:
        print(f"{YELLOW}Tidak ditemukan.{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

def lihat_semua_penyakit():
    clear()
    print(f"{BOLD}{CYAN}📚 SEMUA PENYAKIT ({len(PENYAKIT)}){RESET}\n")
    
    for key, p in PENYAKIT.items():
        print(f"  {GOLD}•{RESET} {p['nama']} — {', '.join(p['gejala'][:2])}")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# 5. VITAL MONITOR
# ============================================================
def vital():
    while True:
        clear()
        print(f"{BOLD}{CYAN}📊 MONITOR VITAL{RESET}\n")
        
        d = load_data()
        v = d.get("vital", [])
        
        if v:
            print(f"{BOLD}10 Data Terakhir:{RESET}\n")
            for x in v[-10:]:
                print(f"  {DIM}{x['tanggal'][:16]}{RESET}")
                if x.get('tensi'): print(f"    🩺 Tensi: {x['tensi']} mmHg")
                if x.get('gula'): print(f"    🍬 Gula: {x['gula']} mg/dL")
                if x.get('suhu'): print(f"    🌡️  Suhu: {x['suhu']}°C")
                if x.get('berat'): print(f"    ⚖️  Berat: {x['berat']} kg")
                print()
        else:
            print(f"  {YELLOW}Belum ada data{RESET}")
        
        print(f"  {GOLD}a.{RESET} Tambah data")
        print(f"  {GOLD}0.{RESET} Kembali")
        
        c = input(f"\n{GOLD}Pilih: {RESET}").strip().lower()
        
        if c == "0": break
        elif c == "a":
            data = {"id": secrets.token_hex(4), "tanggal": datetime.now().isoformat()}
            tensi = input("🩺 Tensi (mis: 120/80, Enter skip): ").strip()
            if tensi: data['tensi'] = tensi
            gula = input("🍬 Gula darah (mg/dL, Enter skip): ").strip()
            if gula: data['gula'] = gula
            suhu = input("🌡️  Suhu (°C, Enter skip): ").strip()
            if suhu: data['suhu'] = suhu
            berat = input("⚖️  Berat (kg, Enter skip): ").strip()
            if berat: data['berat'] = berat
            
            v.append(data)
            d['vital'] = v
            save_data(d)
            if ZUHRI_ID_OK: log_verified("MED_VITAL")
            print(f"{GREEN}✅ Data disimpan{RESET}")
            time.sleep(1)

# ============================================================
# 6. KONTAK DARURAT
# ============================================================
def kontak():
    while True:
        clear()
        print(f"{BOLD}{CYAN}🆘 KONTAK DARURAT{RESET}\n")
        
        d = load_data()
        k = d.get("kontak_darurat", [])
        
        if k:
            for i, c in enumerate(k, 1):
                print(f"  {GOLD}{i}.{RESET} {c['nama']} — {c['telepon']}")
        else:
            print(f"  {YELLOW}Belum ada kontak{RESET}")
        
        print(f"\n  {GOLD}a.{RESET} Tambah kontak")
        print(f"  {GOLD}b.{RESET} Nomor darurat default")
        print(f"  {GOLD}0.{RESET} Kembali")
        
        c = input(f"\n{GOLD}Pilih: {RESET}").strip().lower()
        
        if c == "0": break
        elif c == "a":
            nama = input("👤 Nama: ").strip()
            telp = input("📞 Telepon: ").strip()
            if nama and telp:
                k.append({"id": secrets.token_hex(4), "nama": nama, "telepon": telp})
                d['kontak_darurat'] = k
                save_data(d)
                print(f"{GREEN}✅ Disimpan{RESET}")
                time.sleep(1)
        elif c == "b":
            clear()
            print(f"{BOLD}🚨 NOMOR DARURAT INDONESIA{RESET}\n")
            print(f"  {GOLD}112{RESET} — Darurat Nasional")
            print(f"  {GOLD}119{RESET} — Ambulans / Kesehatan")
            print(f"  {GOLD}110{RESET} — Polisi")
            print(f"  {GOLD}113{RESET} — Pemadam Kebakaran")
            print(f"  {GOLD}115{RESET} — SAR / Basarnas")
            print(f"  {GOLD}118{RESET} — PLN")
            print(f"  {GOLD}117{RESET} — Gangguan Telkom")
            print()
            input(f"{DIM}Enter...{RESET}")

# ============================================================
# 7. BMI CALCULATOR
# ============================================================
def bmi():
    clear()
    print(f"{BOLD}{CYAN}⚖️  BMI CALCULATOR{RESET}\n")
    
    try:
        bb = float(input("Berat (kg): ").strip())
        tb = float(input("Tinggi (cm): ").strip()) / 100
        
        bmi_val = bb / (tb ** 2)
        
        print(f"\n{BOLD}📊 BMI: {bmi_val:.2f}{RESET}\n")
        
        if bmi_val < 18.5:
            print(f"{YELLOW}⚠️  Kurus (Underweight){RESET}")
            print(f"  Saran: Tambah asupan gizi")
        elif bmi_val < 25:
            print(f"{GREEN}✅ Normal{RESET}")
            print(f"  Saran: Pertahankan gaya hidup sehat")
        elif bmi_val < 30:
            print(f"{YELLOW}⚠️  Gemuk (Overweight){RESET}")
            print(f"  Saran: Olahraga & diet seimbang")
        else:
            print(f"{RED}❌ Obesitas{RESET}")
            print(f"  Saran: Konsultasi dokter")
        
        print()
    except:
        print(f"{RED}❌ Input tidak valid{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        clear()
        i = load_identity() if ZUHRI_ID_OK else None
        nama = i['name'] if i else "Anonymous"
        
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🏥 ZUHRI MED — KESEHATAN DIGITAL                                   ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                            ║
║  Pasien: {GOLD}{nama}{RESET}
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  👤 Profil Kesehatan
  {GOLD}2.{RESET}  📋 Riwayat Kesehatan
  {GOLD}3.{RESET}  💊 Pengingat Obat
  {GOLD}4.{RESET}  📚 Database Penyakit
  {GOLD}5.{RESET}  📊 Monitor Vital (Tensi, Gula, Suhu)
  {GOLD}6.{RESET}  🆘 Kontak Darurat
  {GOLD}7.{RESET}  ⚖️  BMI Calculator
  {GOLD}0.{RESET}  Keluar

{DIM}  ⚠️  Zuhri Med BUKAN pengganti dokter.${RESET}
{DIM}  Konsultasi dokter untuk penyakit serius.${RESET}
""")
        try:
            c = input(f"{GOLD}Pilih (0-7): {RESET}").strip()
            if c == "0": break
            elif c == "1": profil()
            elif c == "2": riwayat()
            elif c == "3": obat()
            elif c == "4":
                clear()
                print(f"{BOLD}{CYAN}📚 DATABASE PENYAKIT{RESET}\n")
                print(f"  {GOLD}1.{RESET} Cari penyakit")
                print(f"  {GOLD}2.{RESET} Lihat semua")
                sub = input(f"\n{GOLD}Pilih: {RESET}").strip()
                if sub == "1": cari_penyakit()
                elif sub == "2": lihat_semua_penyakit()
            elif c == "5": vital()
            elif c == "6": kontak()
            elif c == "7": bmi()
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "penyakit": lihat_semua_penyakit()
        elif cmd == "bmi": bmi()
        else: menu()
    else: menu()
