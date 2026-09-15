#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI WEATHER — CUACA OFFLINE & PREDIKSI
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, subprocess, time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
WEA_DIR = os.path.join(HOME, "zuhri_os", "weather")
DATA_DIR = os.path.join(WEA_DIR, "data")
LOG_DIR = os.path.join(WEA_DIR, "logs")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

# ============================================================
# KOTA DI INDONESIA (Database offline)
# ============================================================
KOTA = {
    "jakarta": {"nama": "Jakarta", "lat": -6.21, "lon": 106.85, "zona": "WIB"},
    "surabaya": {"nama": "Surabaya", "lat": -7.25, "lon": 112.75, "zona": "WIB"},
    "bandung": {"nama": "Bandung", "lat": -6.91, "lon": 107.61, "zona": "WIB"},
    "medan": {"nama": "Medan", "lat": 3.59, "lon": 98.67, "zona": "WIB"},
    "semarang": {"nama": "Semarang", "lat": -6.97, "lon": 110.42, "zona": "WIB"},
    "makassar": {"nama": "Makassar", "lat": -5.15, "lon": 119.43, "zona": "WITA"},
    "palembang": {"nama": "Palembang", "lat": -2.99, "lon": 104.75, "zona": "WIB"},
    "denpasar": {"nama": "Denpasar", "lat": -8.65, "lon": 115.21, "zona": "WITA"},
    "yogyakarta": {"nama": "Yogyakarta", "lat": -7.79, "lon": 110.36, "zona": "WIB"},
    "balikpapan": {"nama": "Balikpapan", "lat": -1.27, "lon": 116.83, "zona": "WITA"},
    "manado": {"nama": "Manado", "lat": 1.47, "lon": 124.84, "zona": "WITA"},
    "jayapura": {"nama": "Jayapura", "lat": -2.53, "lon": 140.71, "zona": "WIT"},
    "padang": {"nama": "Padang", "lat": -0.95, "lon": 100.35, "zona": "WIB"},
    "pekanbaru": {"nama": "Pekanbaru", "lat": 0.51, "lon": 101.45, "zona": "WIB"},
    "banjarmasin": {"nama": "Banjarmasin", "lat": -3.32, "lon": 114.59, "zona": "WITA"},
}

# ============================================================
# AMBIL CUACA ONLINE (via wttr.in — gratis)
# ============================================================
def cuaca_online(kota):
    """Ambil cuaca dari wttr.in (gratis, no API key)"""
    try:
        # wttr.in format JSON
        url = f"https://wttr.in/{kota}?format=j1"
        r = subprocess.run(
            ["curl", "-s", "--max-time", "10", url],
            capture_output=True, text=True, timeout=15
        )
        
        if r.stdout:
            data = json.loads(r.stdout)
            
            current = data.get("current_condition", [{}])[0]
            area = data.get("nearest_area", [{}])[0]
            
            return {
                "kota": area.get("areaName", [{}])[0].get("value", kota),
                "negara": area.get("country", [{}])[0].get("value", "Indonesia"),
                "suhu": current.get("temp_C", "?"),
                "terasa": current.get("FeelsLikeC", "?"),
                "kelembapan": current.get("humidity", "?"),
                "angin": current.get("windspeedKmph", "?"),
                "arah_angin": current.get("winddir16Point", "?"),
                "tekanan": current.get("pressure", "?"),
                "cuaca": current.get("weatherDesc", [{}])[0].get("value", "?"),
                "visibilitas": current.get("visibility", "?"),
                "uv": current.get("uvIndex", "?"),
                "waktu": current.get("localObsDateTime", "?"),
                "prakiraan": data.get("weather", [])
            }
    except Exception as e:
        pass
    return None

# ============================================================
# CUACA OFFLINE (Database lokal)
# ============================================================
def cuaca_offline(kota):
    """Prediksi cuaca offline berdasarkan data historis"""
    if kota not in KOTA:
        return None
    
    info = KOTA[kota]
    bulan = datetime.now().month
    
    # Database musim Indonesia (offline)
    # Musim hujan: Nov-Mar, Musim kemarau: Apr-Okt
    if bulan in [11, 12, 1, 2, 3]:
        musim = "Hujan"
        kondisi = ["Hujan ringan", "Hujan sedang", "Berawan", "Mendung"]
    else:
        musim = "Kemarau"
        kondisi = ["Cerah", "Berawan", "Panas", "Cerah berawan"]
    
    # Suhu estimasi berdasarkan kota & musim
    suhu_base = {
        "jakarta": 30, "surabaya": 32, "bandung": 22,
        "medan": 30, "semarang": 30, "makassar": 30,
        "palembang": 30, "denpasar": 28, "yogyakarta": 28,
        "balikpapan": 29, "manado": 29, "jayapura": 29,
        "padang": 29, "pekanbaru": 30, "banjarmasin": 30
    }
    
    suhu = suhu_base.get(kota, 30)
    if musim == "Hujan":
        suhu -= 2
    
    return {
        "kota": info['nama'],
        "zona": info['zona'],
        "musim": musim,
        "suhu_estimasi": f"{suhu}°C",
        "kondisi": kondisi,
        "sumber": "Database offline (estimasi)"
    }

# ============================================================
# PRAKIRAAN 3 HARI
# ============================================================
def prakiraan_3hari(kota):
    """Prakiraan 3 hari"""
    data = cuaca_online(kota)
    if not data:
        return None
    
    prakiraan = []
    for day in data.get('prakiraan', [])[:3]:
        prakiraan.append({
            "tanggal": day.get("date", "?"),
            "max": day.get("maxtempC", "?"),
            "min": day.get("mintempC", "?"),
            "cuaca": day.get("hourly", [{}])[0].get("weatherDesc", [{}])[0].get("value", "?"),
            "hujan": day.get("hourly", [{}])[0].get("chanceofrain", "?"),
        })
    
    return prakiraan

# ============================================================
# INFO BENCANA CUACA
# ============================================================
def info_bencana():
    """Info bencana cuaca dari BMKG (online)"""
    os.system('clear')
    print(f"""
{BOLD}{RED}╔══════════════════════════════════════════════════════════════════════╗
║  ⚠️  INFO BENCANA CUACA — BMKG                                     ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{CYAN}📡 Sumber: BMKG (bmkg.go.id)${RESET}

{BOLD}🌊 JENIS BENCANA CUACA:${RESET}
  {GOLD}•${RESET} Banjir
  {GOLD}•${RESET} Tanah longsor
  {GOLD}•${RESET} Angin puting beliung
  {GOLD}•${RESET} Gelombang tinggi
  {GOLD}•${RESET} Kekeringan
  {GOLD}•${RESET} Kebakaran hutan

{BOLD}📞 KONTAK DARURAT:${RESET}
  {GOLD}•${RESET} BMKG: 196
  {GOLD}•${RESET} BNPB: 117
  {GOLD}•${RESET} Basarnas: 115

{BOLD}🌐 WEBSITE:${RESET}
  {DIM}• https://www.bmkg.go.id${RESET}
  {DIM}• https://magma.esdm.go.id${RESET}

{BOLD}📱 APLIKASI:${RESET}
  {DIM}• Info BMKG (Play Store)${RESET}
  {DIM}• MAGMA Indonesia${RESET}
""")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU CUACA
# ============================================================
def cek_cuaca():
    os.system('clear')
    print(f"{BOLD}{CYAN}🌤️  CEK CUACA{RESET}\n")
    print(f"{DIM}Kota tersedia:{RESET}")
    
    kota_list = list(KOTA.keys())
    for i, k in enumerate(kota_list, 1):
        print(f"  {GOLD}{i:2}.{RESET} {KOTA[k]['nama']}")
    
    print(f"\n  {GOLD}0.{RESET}  Ketik manual")
    
    try:
        c = input(f"\n{CYAN}Pilih kota: {RESET}").strip()
        
        if c == "0":
            kota = input("Nama kota: ").strip().lower()
        else:
            idx = int(c) - 1
            if 0 <= idx < len(kota_list):
                kota = kota_list[idx]
            else:
                return
        
        print(f"\n{CYAN}⏳ Mengambil data cuaca...{RESET}\n")
        
        # Coba online dulu
        data = cuaca_online(kota)
        
        if data:
            print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  🌤️  CUACA — {data['kota']}, {data['negara']}
╚══════════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}🌡️  Suhu:{RESET}         {GREEN}{data['suhu']}°C{RESET} (terasa {data['terasa']}°C)
  {GOLD}☁️  Cuaca:{RESET}        {data['cuaca']}
  {GOLD}💧 Kelembapan:{RESET}   {data['kelembapan']}%
  {GOLD}💨 Angin:{RESET}        {data['angin']} km/jam ({data['arah_angin']})
  {GOLD}📊 Tekanan:{RESET}      {data['tekanan']} hPa
  {GOLD}👁️  Visibilitas:{RESET} {data['visibilitas']} km
  {GOLD}☀️  UV Index:{RESET}    {data['uv']}
  {GOLD}🕐 Waktu:{RESET}        {data['waktu']}
""")
            
            # Prakiraan 3 hari
            prakiraan = prakiraan_3hari(kota)
            if prakiraan:
                print(f"{BOLD}{CYAN}📅 PRAKIRAAN 3 HARI:{RESET}\n")
                for p in prakiraan:
                    print(f"  {GOLD}{p['tanggal']}{RESET}")
                    print(f"    Suhu: {p['min']}°C - {p['max']}°C")
                    print(f"    Cuaca: {p['cuaca']}")
                    print(f"    Hujan: {p['hujan']}%")
                    print()
            
            if ZUHRI_ID_OK:
                log_verified(f"WEATHER: {data['kota']}")
        else:
            # Fallback offline
            print(f"{YELLOW}⚠️  Tidak bisa akses internet, pakai database offline{RESET}\n")
            offline = cuaca_offline(kota)
            if offline:
                print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  🌤️  CUACA OFFLINE — {offline['kota']} ({offline['zona']})
╚══════════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}🗓️  Musim:{RESET}      {offline['musim']}
  {GOLD}🌡️  Suhu:{RESET}       {offline['suhu_estimasi']}
  {GOLD}☁️  Kondisi:{RESET}    {', '.join(offline['kondisi'])}
  {GOLD}📊 Sumber:{RESET}      {offline['sumber']}

{DIM}Untuk data akurat, sambungkan ke internet.${RESET}
""")
    except ValueError:
        print(f"{RED}❌ Input tidak valid{RESET}")
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}")
    
    input(f"\n{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  🌤️  ZUHRI WEATHER — CUACA OFFLINE & PREDIKSI                      ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                            ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🌤️  Cek Cuaca (Online)
  {GOLD}2.{RESET}  📊 Cuaca Offline (Database)
  {GOLD}3.{RESET}  📅 Prakiraan 3 Hari
  {GOLD}4.{RESET}  ⚠️  Info Bencana Cuaca
  {GOLD}5.{RESET}  📋 Daftar Kota
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-5): {RESET}").strip()
            if c == "0": break
            elif c == "1": cek_cuaca()
            elif c == "2":
                os.system('clear')
                print(f"{BOLD}{CYAN}📊 CUACA OFFLINE{RESET}\n")
                print(f"{DIM}Database offline:{RESET}")
                for i, (k, v) in enumerate(KOTA.items(), 1):
                    print(f"  {GOLD}{i:2}.{RESET} {v['nama']} ({v['zona']})")
                
                try:
                    c2 = input(f"\n{CYAN}Pilih kota: {RESET}").strip()
                    idx = int(c2) - 1
                    kota = list(KOTA.keys())[idx]
                    offline = cuaca_offline(kota)
                    
                    if offline:
                        print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  🌤️  CUACA OFFLINE — {offline['kota']}
╚══════════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}🗓️  Musim:{RESET}      {offline['musim']}
  {GOLD}🌡️  Suhu:{RESET}       {offline['suhu_estimasi']}
  {GOLD}☁️  Kondisi:{RESET}    {', '.join(offline['kondisi'])}
  {GOLD}📊 Sumber:{RESET}      {offline['sumber']}
""")
                except:
                    pass
                input(f"{DIM}Enter...{RESET}")
            elif c == "3":
                os.system('clear')
                kota = input(f"{CYAN}Kota: {RESET}").strip().lower()
                print(f"\n{CYAN}⏳ Mengambil prakiraan...{RESET}\n")
                prakiraan = prakiraan_3hari(kota)
                if prakiraan:
                    print(f"{BOLD}{CYAN}📅 PRAKIRAAN 3 HARI — {kota.upper()}{RESET}\n")
                    for p in prakiraan:
                        print(f"  {GOLD}{p['tanggal']}{RESET}")
                        print(f"    🌡️  {p['min']}°C - {p['max']}°C")
                        print(f"    ☁️  {p['cuaca']}")
                        print(f"    💧 Hujan: {p['hujan']}%")
                        print()
                else:
                    print(f"{YELLOW}⚠️  Tidak bisa ambil data (butuh internet){RESET}")
                input(f"{DIM}Enter...{RESET}")
            elif c == "4": info_bencana()
            elif c == "5":
                os.system('clear')
                print(f"{BOLD}{CYAN}📋 DAFTAR KOTA ({len(KOTA)}){RESET}\n")
                for k, v in KOTA.items():
                    print(f"  {GOLD}•{RESET} {v['nama']:15} ({v['zona']}) - {v['lat']}, {v['lon']}")
                print()
                input(f"{DIM}Enter...{RESET}")
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "cek":
            kota = sys.argv[2] if len(sys.argv) > 2 else "jakarta"
            data = cuaca_online(kota)
            if data:
                print(f"Cuaca {data['kota']}: {data['cuaca']}, {data['suhu']}°C")
            else:
                print("Tidak bisa ambil data")
        elif cmd == "offline":
            kota = sys.argv[2] if len(sys.argv) > 2 else "jakarta"
            data = cuaca_offline(kota)
            print(json.dumps(data, indent=2) if data else "Kota tidak ada")
        else: menu()
    else: menu()
