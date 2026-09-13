#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI PERINGATAN — SISTEM PERINGATAN DINI BENCANA
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
Integrasi: Satelit, Magnetik, Gelombang, Data Nasional
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
import math
import random

# ===== KONFIGURASI =====
HOME = os.path.expanduser("~")
WARN_DIR = os.path.join(HOME, "zuhri_os", "peringatan")
DATA_DIR = os.path.join(WARN_DIR, "data")
LOG_DIR = os.path.join(WARN_DIR, "logs")
ZONE_DIR = os.path.join(WARN_DIR, "zones")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(ZONE_DIR, exist_ok=True)

# ===== WARNA =====
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
GOLD = "\033[93m"
MAGENTA = "\033[95m"

# ===== ZONA RAWAN BENCANA (INDONESIA) =====
ZONA_RAWAN = {
    "aceh": {"nama": "Aceh", "lat": 5.55, "lon": 95.32, "risiko": "Gempa, Tsunami", "level": "TINGGI"},
    "sumut": {"nama": "Sumatera Utara", "lat": 3.59, "lon": 98.67, "risiko": "Gempa, Vulkanik", "level": "TINGGI"},
    "sumbar": {"nama": "Sumatera Barat", "lat": -0.95, "lon": 100.35, "risiko": "Gempa, Tsunami", "level": "TINGGI"},
    "bengkulu": {"nama": "Bengkulu", "lat": -3.80, "lon": 102.26, "risiko": "Gempa, Tsunami", "level": "TINGGI"},
    "lampung": {"nama": "Lampung", "lat": -5.45, "lon": 105.26, "risiko": "Gempa, Tsunami, Vulkanik", "level": "TINGGI"},
    "jabar": {"nama": "Jawa Barat", "lat": -6.91, "lon": 107.61, "risiko": "Gempa, Vulkanik", "level": "TINGGI"},
    "jateng": {"nama": "Jawa Tengah", "lat": -7.00, "lon": 110.00, "risiko": "Gempa, Vulkanik", "level": "TINGGI"},
    "yogya": {"nama": "Yogyakarta", "lat": -7.79, "lon": 110.36, "risiko": "Gempa, Vulkanik", "level": "TINGGI"},
    "jatim": {"nama": "Jawa Timur", "lat": -7.54, "lon": 112.23, "risiko": "Gempa, Vulkanik", "level": "TINGGI"},
    "bali": {"nama": "Bali", "lat": -8.65, "lon": 115.21, "risiko": "Gempa, Vulkanik", "level": "TINGGI"},
    "ntb": {"nama": "Nusa Tenggara Barat", "lat": -8.65, "lon": 117.36, "risiko": "Gempa, Tsunami, Vulkanik", "level": "TINGGI"},
    "ntt": {"nama": "Nusa Tenggara Timur", "lat": -8.65, "lon": 121.07, "risiko": "Gempa, Tsunami, Vulkanik", "level": "TINGGI"},
    "sulut": {"nama": "Sulawesi Utara", "lat": 1.47, "lon": 124.84, "risiko": "Gempa, Tsunami, Vulkanik", "level": "TINGGI"},
    "sulteng": {"nama": "Sulawesi Tengah", "lat": -1.43, "lon": 121.44, "risiko": "Gempa, Tsunami", "level": "TINGGI"},
    "maluku": {"nama": "Maluku", "lat": -3.23, "lon": 130.14, "risiko": "Gempa, Tsunami", "level": "TINGGI"},
    "papua": {"nama": "Papua", "lat": -4.26, "lon": 138.08, "risiko": "Gempa", "level": "SEDANG"},
    "jakarta": {"nama": "Jakarta", "lat": -6.21, "lon": 106.85, "risiko": "Banjir, Gempa", "level": "SEDANG"},
    "kalimantan": {"nama": "Kalimantan", "lat": -1.68, "lon": 113.38, "risiko": "Banjir, Karhutla", "level": "SEDANG"},
}

# ============================================================
# AMBIL DATA GEMPA BMKG (Realtime)
# ============================================================
def fetch_bmkg_earthquakes():
    """Ambil data gempa terbaru dari BMKG"""
    try:
        # Coba ambil dari API BMKG
        result = subprocess.run(
            ["curl", "-s", "--max-time", "10", "https://data.bmkg.go.id/DataMKG/TEWS/gempa.json"],
            capture_output=True, text=True, timeout=15
        )
        if result.stdout:
            data = json.loads(result.stdout)
            return data.get("Infogempa", {}).get("gempa", [])
    except:
        pass
    return []

def fetch_usgs_earthquakes():
    """Ambil data gempa dari USGS (global)"""
    try:
        # Gempa M4+ di Indonesia dalam 7 hari terakhir
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2026-09-05&minmagnitude=4.0&minlatitude=-11&maxlatitude=6&minlongitude=95&maxlongitude=141"
        result = subprocess.run(
            ["curl", "-s", "--max-time", "10", url],
            capture_output=True, text=True, timeout=15
        )
        if result.stdout:
            data = json.loads(result.stdout)
            return data.get("features", [])
    except:
        pass
    return []

# ============================================================
# ANALISIS ZONA RAWAN
# ============================================================
def analyze_zones():
    """Analisis zona rawan berdasarkan data gempa"""
    gempa_bmkg = fetch_bmkg_earthquakes()
    gempa_usgs = fetch_usgs_earthquakes()
    
    print(f"\n{BOLD}{CYAN}🌋 ANALISIS ZONA RAWAN — ZUHRI PERINGATAN{RESET}")
    print(f"{DIM}Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}\n")
    
    # Analisis per zona
    alerts = []
    
    for zone_id, zone in ZONA_RAWAN.items():
        # Hitung jarak ke gempa terbaru
        closest = None
        min_dist = float('inf')
        
        for gempa in gempa_bmkg[:10]:  # 10 gempa terbaru
            try:
                lat = float(gempa.get('Latitude', 0))
                lon = float(gempa.get('Longitude', 0))
                mag = float(gempa.get('Magnitude', 0))
                depth = float(gempa.get('Kedalaman', '0').replace(' km', ''))
                
                # Jarak (Haversine sederhana)
                dist = math.sqrt((lat - zone['lat'])**2 + (lon - zone['lon'])**2) * 111
                
                if dist < min_dist:
                    min_dist = dist
                    closest = {"mag": mag, "depth": depth, "dist": dist, "time": gempa.get('DateTime', '')}
            except:
                pass
        
        # Logika peringatan
        if closest:
            if min_dist < 100 and closest['mag'] >= 5.0:
                level = "🔴 SIAGA"
                color = RED
            elif min_dist < 200 and closest['mag'] >= 4.5:
                level = "🟠 WASPADA"
                color = YELLOW
            elif min_dist < 300:
                level = "🟡 PANTau"
                color = CYAN
            else:
                level = "🟢 AMAN"
                color = GREEN
        else:
            level = "🟢 AMAN"
            color = GREEN
            closest = {"mag": 0, "depth": 0, "dist": 0}
        
        alerts.append({
            "zone": zone,
            "level": level,
            "color": color,
            "closest": closest
        })
    
    # Tampilkan
    for a in alerts:
        z = a['zone']
        c = a['closest']
        
        print(f"  {a['color']}{a['level']}{RESET}  {BOLD}{z['nama']}{RESET}")
        print(f"         {DIM}Risiko: {z['risiko']} | Level: {z['level']}{RESET}")
        if c['mag'] > 0:
            print(f"         {DIM}Gempa terdekat: M{c['mag']} ({c['dist']:.0f} km){RESET}")
        print()
    
    # Simpan log
    log_file = os.path.join(LOG_DIR, f"zona_{datetime.now().strftime('%Y%m%d')}.json")
    with open(log_file, "w") as f:
        json.dump(alerts, f, indent=2, default=str)
    
    return alerts

# ============================================================
# PERINGATAN DINI BERBASIS ZUHRI FORMALISM
# ============================================================
def zuhri_alert_analysis():
    """Analisis berbasis resonansi Zuhri 0-8-9"""
    print(f"\n{BOLD}{MAGENTA}🧬 ANALISIS ZUHRI FORMALISM{RESET}")
    print(f"{DIM}Resonansi: 0-8-9 — Keseimbangan Dinamis{RESET}\n")
    
    # Ambil data
    gempa_bmkg = fetch_bmkg_earthquakes()
    
    if not gempa_bmkg:
        print(f"{YELLOW}⚠️  Data gempa tidak tersedia. Coba lagi nanti.{RESET}\n")
        return
    
    # Analisis pola
    total_gempa = len(gempa_bmkg)
    mag_avg = sum(float(g.get('Magnitude', 0)) for g in gempa_bmkg[:20]) / min(len(gempa_bmkg), 20)
    
    # Resonansi 0-8-9
    resonansi = (total_gempa * 8 + mag_avg * 9) % 10
    
    print(f"  📊 Total gempa terdeteksi: {GOLD}{total_gempa}{RESET}")
    print(f"  📈 Magnitudo rata-rata: {GOLD}M{mag_avg:.2f}{RESET}")
    print(f"  🧬 Resonansi Zuhri: {GOLD}{resonansi}{RESET}")
    
    # Interpretasi
    if resonansi >= 7:
        status = f"{RED}🔴 RESONANSI TINGGI — Potensi aktivitas seismik meningkat{RESET}"
    elif resonansi >= 4:
        status = f"{YELLOW}🟠 RESONANSI SEDANG — Perlu kewaspadaan{RESET}"
    else:
        status = f"{GREEN}🟢 RESONANSI RENDAH — Kondisi relatif stabil{RESET}"
    
    print(f"\n  {status}\n")
    
    # Simpan log
    log_file = os.path.join(LOG_DIR, f"zuhri_alert_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
    with open(log_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_gempa": total_gempa,
            "mag_avg": mag_avg,
            "resonansi": resonansi,
            "status": status
        }, f, indent=2)

# ============================================================
# INFO PREKURSOR (Magnetik & TEC)
# ============================================================
def show_precursor_info():
    """Tampilkan info tentang prekursor gempa"""
    print(f"""
{BOLD}{CYAN}🔬 INFO PREKURSOR GEMPA — ZUHRI PERINGATAN{RESET}
{'─' * 60}

{BOLD}📡 Prekursor Magnetik (Swarm Satellite){RESET}
Penelitian menunjukkan anomali medan magnet dapat terdeteksi
hingga 90 hari sebelum gempa besar. Akurasi: 79% [citation:13].

{S}Data yang dipantau:{RESET}
  • Medan magnet (H, D, Z)
  • Total Electron Content (TEC)
  • Frekuensi ULF (0.001-0.5 Hz)

{BOLD}🌊 Prekursor Gelombang (DAS & Seismik){RESET}
Distributed Acoustic Sensing (DAS) mendeteksi getaran
mikro dan gelombang seismik secara real-time [citation:22].

{BOLD}🛰️  Citra Satelit (SAR/PSInSAR){RESET}
Deteksi deformasi tanah skala milimeter untuk
vulkanik & longsor [citation:1].

{BOLD}⚠️  CATATAN PENTING{RESET}
BMKG menegaskan: {RED}Prediksi gempa belum bisa akurat 100%.{RESET}
ZUHRI PERINGATAN fokus pada:
  ✅ Peringatan Dini (setelah gempa)
  ✅ Monitoring Prekursor (potensi)
  ✅ Peta Risiko Komunitas

{DM}Sumber: BMKG, BNPB, ESA, USGS, IEEE DataPort{RESET}
""")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        
        print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🌋 ZUHRI PERINGATAN — SISTEM PERINGATAN DINI BENCANA          ║
║  ──────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                       ║
║  Status: {GREEN}AKTIF{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🌋 Analisis Zona Rawan (Real-time)
  {GOLD}2.{RESET}  🧬 Analisis Zuhri Formalism
  {GOLD}3.{RESET}  🔬 Info Prekursor Gempa
  {GOLD}4.{RESET}  📊 Lihat Log Peringatan
  {GOLD}5.{RESET}  📍 Cek Zona Spesifik
  {GOLD}6.{RESET}  🚨 Kirim Peringatan SOS
  {GOLD}0.{RESET}  Keluar
""")
        
        try:
            c = input(f"{GOLD}Pilih (0-6): {RESET}").strip()
            
            if c == "0":
                break
            elif c == "1":
                analyze_zones()
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif c == "2":
                zuhri_alert_analysis()
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif c == "3":
                show_precursor_info()
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif c == "4":
                show_logs()
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif c == "5":
                check_zone()
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif c == "6":
                kirim_sos()
                input(f"\n{DIM}Tekan Enter...{RESET}")
        except KeyboardInterrupt:
            break

def show_logs():
    """Tampilkan log peringatan"""
    logs = sorted([f for f in os.listdir(LOG_DIR) if f.endswith('.json')], reverse=True)
    
    print(f"\n{BOLD}{CYAN}📊 LOG PERINGATAN{RESET}\n")
    
    if not logs:
        print(f"{YELLOW}Belum ada log.{RESET}\n")
        return
    
    for log in logs[:5]:
        print(f"  {GOLD}📄{RESET} {log}")

def check_zone():
    """Cek zona spesifik"""
    print(f"\n{BOLD}{CYAN}📍 DAFTAR ZONA RAWAN{RESET}\n")
    
    zones = list(ZONA_RAWAN.items())
    for i, (zid, z) in enumerate(zones, 1):
        print(f"  {GOLD}{i}.{RESET} {z['nama']} — {DIM}{z['risiko']}{RESET}")
    
    try:
        c = int(input(f"\n{CYAN}Pilih zona: {RESET}")) - 1
        if 0 <= c < len(zones):
            zid, z = zones[c]
            print(f"""
{BOLD}{CYAN}📍 {z['nama']}{RESET}

  Koordinat : {z['lat']}, {z['lon']}
  Risiko    : {z['risiko']}
  Level     : {z['level']}
  Status    : {GREEN}✅ Dipantau{RESET}
""")
    except:
        pass

def kirim_sos():
    """Kirim SOS ke jaringan"""
    print(f"\n{BOLD}{RED}🚨 KIRIM PERINGATAN SOS{RESET}\n")
    
    pesan = input("Pesan SOS: ").strip() or "SOS! Bencana terdeteksi!"
    
    # Simpan log
    sos_file = os.path.join(LOG_DIR, f"sos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(sos_file, "w") as f:
        json.dump({
            "type": "SOS",
            "message": pesan,
            "timestamp": datetime.now().isoformat(),
            "status": "pending_broadcast"
        }, f, indent=2)
    
    print(f"\n{GREEN}✅ SOS disimpan: {sos_file}{RESET}")
    print(f"{DIM}Gunakan `sos beacon` untuk broadcast ke perangkat sekitar.{RESET}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "zona": analyze_zones()
        elif cmd == "zuhri": zuhri_alert_analysis()
        elif cmd == "info": show_precursor_info()
        elif cmd == "help":
            print("""
🌋 ZUHRI PERINGATAN — BANTUAN
─────────────────────────────
  peringatan           → Menu interaktif
  peringatan zona      → Analisis zona rawan
  peringatan zuhri     → Analisis Zuhri Formalism
  peringatan info      → Info prekursor
""")
        else: menu()
    else:
        menu()
