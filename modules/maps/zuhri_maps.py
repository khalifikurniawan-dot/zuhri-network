#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI MAPS — PETA OFFLINE & NAVIGASI
Peta, GPS, Kompas, Info Geografis
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, subprocess, math, secrets
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
MAPS_DIR = os.path.join(HOME, "zuhri_os", "maps")
DATA_DIR = os.path.join(MAPS_DIR, "data")
CACHE_DIR = os.path.join(MAPS_DIR, "cache")
SAVED_DIR = os.path.join(MAPS_DIR, "saved")
for d in [DATA_DIR, CACHE_DIR, SAVED_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# DATABASE LOKASI PENTING (INDONESIA)
# ============================================================
LOKASI_PENTING = {
    "jakarta": {"nama":"Jakarta","lat":-6.2088,"lon":106.8456,"tipe":"ibukota"},
    "surabaya": {"nama":"Surabaya","lat":-7.2575,"lon":112.7521,"tipe":"kota"},
    "bandung": {"nama":"Bandung","lat":-6.9175,"lon":107.6191,"tipe":"kota"},
    "medan": {"nama":"Medan","lat":3.5952,"lon":98.6722,"tipe":"kota"},
    "semarang": {"nama":"Semarang","lat":-6.9667,"lon":110.4167,"tipe":"kota"},
    "makassar": {"nama":"Makassar","lat":-5.1477,"lon":119.4327,"tipe":"kota"},
    "palembang": {"nama":"Palembang","lat":-2.9761,"lon":104.7754,"tipe":"kota"},
    "denpasar": {"nama":"Denpasar","lat":-8.6705,"lon":115.2126,"tipe":"kota"},
    "yogyakarta": {"nama":"Yogyakarta","lat":-7.7956,"lon":110.3695,"tipe":"kota"},
    "balikpapan": {"nama":"Balikpapan","lat":-1.2379,"lon":116.8529,"tipe":"kota"},
}

# ============================================================
# GET GPS LOCATION
# ============================================================
def get_gps():
    """Dapatkan lokasi GPS via termux-api"""
    try:
        r = subprocess.run(
            ["termux-location"],
            capture_output=True, text=True, timeout=15
        )
        if r.stdout:
            data = json.loads(r.stdout)
            return {
                "lat": data.get("latitude", 0),
                "lon": data.get("longitude", 0),
                "alt": data.get("altitude", 0),
                "acc": data.get("accuracy", 0),
                "provider": data.get("provider", "unknown"),
                "time": data.get("time", "")
            }
    except Exception as e:
        pass
    return None

# ============================================================
# HAVERSINE DISTANCE
# ============================================================
def hitung_jarak(lat1, lon1, lat2, lon2):
    """Hitung jarak antara 2 koordinat (km)"""
    R = 6371  # Radius bumi (km)
    
    lat1_r = math.radians(lat1)
    lat2_r = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

# ============================================================
# MENU GPS
# ============================================================
def show_gps():
    os.system('clear')
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  📍 ZUHRI MAPS — LOKASI GPS                                         ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{CYAN}⏳ Mengambil lokasi GPS...{RESET}
{DIM}Pastikan GPS aktif & izin diberikan.${RESET}
""")
    
    gps = get_gps()
    
    if not gps:
        print(f"{RED}❌ Gagal ambil GPS{RESET}")
        print(f"{YELLOW}Pastikan:${RESET}")
        print(f"{DIM}  1. Termux:API terinstall dari F-Droid{RESET}")
        print(f"{DIM}  2. GPS aktif di HP{RESET}")
        print(f"{DIM}  3. Izin lokasi diberikan{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    print(f"""
{BOLD}📍 LOKASI ANDA:{RESET}
  {GOLD}Latitude{RESET}  : {gps['lat']}
  {GOLD}Longitude{RESET} : {gps['lon']}
  {GOLD}Altitude{RESET}  : {gps['alt']} m
  {GOLD}Akurasi{RESET}   : {gps['acc']} m
  {GOLD}Provider{RESET}  : {gps['provider']}
  {GOLD}Waktu{RESET}     : {gps['time']}
""")
    
    # Cek jarak ke kota terdekat
    print(f"{BOLD}🏙️  JARAK KE KOTA TERDEKAT:{RESET}\n")
    
    jarak_list = []
    for key, kota in LOKASI_PENTING.items():
        jarak = hitung_jarak(gps['lat'], gps['lon'], kota['lat'], kota['lon'])
        jarak_list.append((kota['nama'], jarak, kota['tipe']))
    
    jarak_list.sort(key=lambda x: x[1])
    
    for nama, jarak, tipe in jarak_list[:5]:
        print(f"  {GOLD}•{RESET} {nama:15} {jarak:8.1f} km {DIM}({tipe}){RESET}")
    
    print()
    print(f"{BOLD}🗺️  LINK PETA:{RESET}")
    print(f"  {CYAN}https://www.openstreetmap.org/?mlat={gps['lat']}&mlon={gps['lon']}#map=15/{gps['lat']}/{gps['lon']}{RESET}\n")
    
    # Simpan lokasi
    if ZUHRI_ID_OK:
        loc_file = os.path.join(DATA_DIR, f"location_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        json.dump(gps, open(loc_file, "w"), indent=2)
        log_verified(f"MAPS_GPS: {gps['lat']},{gps['lon']}")
    
    print(f"{BOLD}📋 AKSI:{RESET}")
    print(f"  {GOLD}1.{RESET} Buka di browser")
    print(f"  {GOLD}2.{RESET} Copy koordinat")
    print(f"  {GOLD}0.{RESET} Kembali")
    
    c = input(f"\n{GOLD}Pilih: {RESET}").strip()
    
    if c == "1":
        url = f"https://www.openstreetmap.org/?mlat={gps['lat']}&mlon={gps['lon']}#map=15/{gps['lat']}/{gps['lon']}"
        os.system(f"termux-open-url '{url}' 2>/dev/null")
        print(f"{GREEN}✅ Dibuka di browser{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
    elif c == "2":
        print(f"\n{GREEN}📍 Koordinat:{RESET}")
        print(f"{gps['lat']}, {gps['lon']}\n")
        input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU JARAK
# ============================================================
def hitung_jarak_menu():
    os.system('clear')
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  📏 ZUHRI MAPS — HITUNG JARAK                                       ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    print(f"{BOLD}🏙️  DAFTAR KOTA:{RESET}\n")
    keys = list(LOKASI_PENTING.keys())
    for i, key in enumerate(keys, 1):
        k = LOKASI_PENTING[key]
        print(f"  {GOLD}{i}.{RESET} {k['nama']:15} {DIM}({k['lat']}, {k['lon']}){RESET}")
    
    print()
    
    try:
        c1 = int(input(f"{CYAN}Kota asal (nomor): {RESET}")) - 1
        c2 = int(input(f"{CYAN}Kota tujuan (nomor): {RESET}")) - 1
        
        if 0 <= c1 < len(keys) and 0 <= c2 < len(keys):
            k1 = LOKASI_PENTING[keys[c1]]
            k2 = LOKASI_PENTING[keys[c2]]
            
            jarak = hitung_jarak(k1['lat'], k1['lon'], k2['lat'], k2['lon'])
            
            print(f"""
{BOLD}📏 HASIL:{RESET}
  {GOLD}Dari{RESET}   : {k1['nama']}
  {GOLD}Ke{RESET}     : {k2['nama']}
  {GOLD}Jarak{RESET}  : {GREEN}{jarak:.2f} km{RESET}

  {DIM}Estimasi waktu tempuh:${RESET}
  {GOLD}🚗 Mobil{RESET}  : {jarak/60:.1f} jam ({jarak/60*60:.0f} km/h)
  {GOLD}🏍️  Motor{RESET}  : {jarak/50:.1f} jam ({jarak/50*60:.0f} km/h)
  {GOLD}🚶 Jalan{RESET}  : {jarak/5:.1f} jam ({jarak/5*60:.0f} km/h)
""")
    except:
        print(f"{RED}❌ Input tidak valid{RESET}")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU KOMPAS
# ============================================================
def show_compass():
    os.system('clear')
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  🧭 ZUHRI MAPS — KOMPAS                                             ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    # Ambil orientasi via sensor
    try:
        r = subprocess.run(
            ["termux-sensor", "-s", "magnetic_field", "-n", "1"],
            capture_output=True, text=True, timeout=5
        )
        if r.stdout:
            data = json.loads(r.stdout)
            for key, val in data.items():
                if isinstance(val, dict) and "values" in val:
                    x, y, z = val["values"][:3]
                    heading = math.degrees(math.atan2(y, x))
                    if heading < 0:
                        heading += 360
                    
                    # Arah mata angin
                    arah = ["U", "TL", "T", "TG", "S", "BD", "B", "BL"]
                    idx = int((heading + 22.5) / 45) % 8
                    
                    print(f"""
{BOLD}🧭 ORIENTASI:{RESET}
  {GOLD}Arah{RESET}     : {GREEN}{arah[idx]}{RESET} ({heading:.0f}°)
  {GOLD}X{RESET}        : {x:.2f}
  {GOLD}Y{RESET}        : {y:.2f}
  {GOLD}Z{RESET}        : {z:.2f}
  
  {DIM}U=Utara, T=Timur, S=Selatan, B=Barat${RESET}
  {DIM}TL=Timur Laut, TG=Tenggara, BD=Barat Daya, BL=Barat Laut${RESET}
""")
                    input(f"{DIM}Enter...{RESET}")
                    return
    except:
        pass
    
    print(f"{YELLOW}⚠️  Sensor magnetik tidak tersedia{RESET}")
    print(f"{DIM}Pastikan Termux:API terinstall${RESET}\n")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU SIMPAN LOKASI
# ============================================================
def simpan_lokasi():
    os.system('clear')
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  📌 ZUHRI MAPS — SIMPAN LOKASI PENTING                              ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    nama = input("🏷️  Nama lokasi: ").strip()
    if not nama:
        return
    
    print(f"\n{GOLD}1.{RESET} Gunakan GPS saat ini")
    print(f"{GOLD}2.{RESET} Input koordinat manual")
    
    c = input(f"\n{CYAN}Pilih: {RESET}").strip()
    
    if c == "1":
        gps = get_gps()
        if not gps:
            print(f"{RED}❌ Gagal ambil GPS{RESET}\n")
            input(f"{DIM}Enter...{RESET}")
            return
        lat, lon = gps['lat'], gps['lon']
    elif c == "2":
        try:
            lat = float(input("Latitude: ").strip())
            lon = float(input("Longitude: ").strip())
        except:
            print(f"{RED}❌ Input tidak valid{RESET}\n")
            input(f"{DIM}Enter...{RESET}")
            return
    else:
        return
    
    lokasi = {
        "nama": nama,
        "lat": lat,
        "lon": lon,
        "disimpan": datetime.now().isoformat()
    }
    
    f = os.path.join(SAVED_DIR, f"lokasi_{secrets.token_hex(4)}.json")
    json.dump(lokasi, open(f, "w"), indent=2)
    
    print(f"\n{GREEN}✅ Lokasi '{nama}' disimpan!{RESET}")
    print(f"{GOLD}Koordinat:{RESET} {lat}, {lon}\n")
    
    if ZUHRI_ID_OK:
        log_verified(f"MAPS_SAVE: {nama}")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU LIHAT LOKASI TERSIMPAN
# ============================================================
def lihat_lokasi():
    os.system('clear')
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  📌 ZUHRI MAPS — LOKASI TERSIMPAN                                   ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    files = [f for f in os.listdir(SAVED_DIR) if f.endswith('.json')]
    
    if not files:
        print(f"{YELLOW}Belum ada lokasi tersimpan.${RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    for i, f in enumerate(files, 1):
        lokasi = json.load(open(os.path.join(SAVED_DIR, f)))
        print(f"{GOLD}{i}.{RESET} {BOLD}{lokasi['nama']}{RESET}")
        print(f"   {DIM}📍 {lokasi['lat']}, {lokasi['lon']}{RESET}")
        print(f"   {DIM}📅 {lokasi['disimpan'][:19]}{RESET}\n")
    
    print(f"{DIM}Total: {len(files)} lokasi{RESET}\n")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU INFO CUACA (OFFLINE)
# ============================================================
def info_cuaca():
    os.system('clear')
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  🌤️  ZUHRI MAPS — INFO CUACA (OFFLINE)                              ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{YELLOW}⚠️  Fitur cuaca real-time butuh internet.${RESET}
{DIM}Berikut info cuaca offline (perkiraan).${RESET}

{BOLD}🌤️  INFO MUSIM DI INDONESIA:{RESET}

  {GOLD}🇮🇩 INDONESIA:{RESET}
    • Musim Kemarau : April - September
    • Musim Hujan   : Oktober - Maret
    • Suhu rata-rata: 25-33°C
    • Kelembapan    : 60-90%

  {GOLD}🌴 MUSIM KHAS:{RESET}
    • Kemarau → Panas, kering, debu
    • Hujan   → Basah, banjir, lembab
    • Pancaroba → Cuaca tidak stabil

{BOLD}📊 CARA CEK CUACA REAL-TIME:{RESET}
  {GOLD}1.{RESET} Buka browser: {CYAN}bmkg.go.id{RESET}
  {GOLD}2.{RESET} Install app: BMKG, Weather Indonesia
  {GOLD}3.{RESET} Cek via web: {CYAN}weather.com{RESET}
""")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🗺️  ZUHRI MAPS — PETA OFFLINE & NAVIGASI                           ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                            ║
║  100% Offline — Tanpa Internet                                      ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  📍 Lihat Lokasi GPS
  {GOLD}2.{RESET}  📏 Hitung Jarak Antar Kota
  {GOLD}3.{RESET}  🧭 Kompas
  {GOLD}4.{RESET}  📌 Simpan Lokasi Penting
  {GOLD}5.{RESET}  📂 Lihat Lokasi Tersimpan
  {GOLD}6.{RESET}  🌤️  Info Cuaca (Offline)
  {GOLD}7.{RESET}  🌐 Buka Peta Online (OSM)
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-7): {RESET}").strip()
            if c == "0": break
            elif c == "1": show_gps()
            elif c == "2": hitung_jarak_menu()
            elif c == "3": show_compass()
            elif c == "4": simpan_lokasi()
            elif c == "5": lihat_lokasi()
            elif c == "6": info_cuaca()
            elif c == "7":
                os.system("termux-open-url 'https://www.openstreetmap.org' 2>/dev/null")
                print(f"{GREEN}✅ Buka OpenStreetMap di browser{RESET}\n")
                input(f"{DIM}Enter...{RESET}")
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "gps": show_gps()
        elif cmd == "jarak": hitung_jarak_menu()
        elif cmd == "kompas": show_compass()
        else: menu()
    else: menu()
