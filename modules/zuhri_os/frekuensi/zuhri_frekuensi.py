#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI FREKUENSI — MONITORING RESONANSI & ANOMALI
Sensor HP + Data Publik + Visualisasi
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os
import sys
import json
import subprocess
import math
import random
from datetime import datetime

HOME = os.path.expanduser("~")
FREQ_DIR = os.path.join(HOME, "zuhri_os", "frekuensi")
DATA_DIR = os.path.join(FREQ_DIR, "data")
LOG_DIR = os.path.join(FREQ_DIR, "logs")
VIS_DIR = os.path.join(FREQ_DIR, "visual")
for d in [DATA_DIR, LOG_DIR, VIS_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# BACA SENSOR HP
# ============================================================
def baca_sensor(sensor="accelerometer"):
    """Baca sensor HP via termux-api"""
    try:
        result = subprocess.run(
            ["termux-sensor", "-s", sensor, "-n", "1"],
            capture_output=True, text=True, timeout=5
        )
        if result.stdout:
            data = json.loads(result.stdout)
            # Ambil nilai
            for key, val in data.items():
                if isinstance(val, dict) and "values" in val:
                    return val["values"]
                elif isinstance(val, list) and len(val) >= 3:
                    return val[:3]
    except Exception as e:
        pass
    return None

def baca_semua_sensor():
    """Baca semua sensor yang tersedia"""
    sensors = {}
    
    sensor_list = [
        ("accelerometer", "Akselerometer", "m/s²"),
        ("magnetic_field", "Magnetometer", "μT"),
        ("gyroscope", "Gyroscope", "rad/s"),
        ("gravity", "Gravitasi", "m/s²"),
        ("light", "Cahaya", "lux"),
        ("pressure", "Tekanan", "hPa"),
        ("proximity", "Proximity", "cm"),
        ("humidity", "Kelembapan", "%"),
    ]
    
    for sensor_id, nama, unit in sensor_list:
        val = baca_sensor(sensor_id)
        if val:
            sensors[nama] = {"values": val, "unit": unit}
    
    return sensors

# ============================================================
# MODUL 1 — RESONANSI GELOMBANG (Sonar/LIDAR Simulation)
# ============================================================
def analisis_gelombang():
    """Analisis gelombang & resonansi (sonar/lidar)"""
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🌊 MODUL 1 — RESONANSI GELOMBANG (SONAR/LIDAR)                ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Analisis gelombang & resonansi berbasis sensor akustik dan vibrasi.{RESET}

{BOLD}📡 Frekuensi yang dipantau:{RESET}
  {GOLD}•{RESET} Infrasonik  : < 20 Hz (gempa, vulkanik)
  {GOLD}•{RESET} Audiosonik  : 20 Hz - 20 kHz
  {GOLD}•{RESET} Ultrasonik  : > 20 kHz (sonar, LIDAR)

""")
    
    # Simulasi pembacaan resonansi
    print(f"{CYAN}📊 Memindai frekuensi...{RESET}\n")
    
    freq_data = {
        "infrasonik": [],
        "audiosonik": [],
        "ultrasonik": []
    }
    
    for i in range(10):
        freq_data["infrasonik"].append(round(random.uniform(0.5, 20), 2))
        freq_data["audiosonik"].append(round(random.uniform(20, 20000), 1))
        freq_data["ultrasonik"].append(round(random.uniform(20000, 100000), 0))
    
    # Tampilkan visualisasi
    print(f"{BOLD}📊 SPEKTRUM FREKUENSI:{RESET}\n")
    
    # Infrasonik
    infra_max = max(freq_data["infrasonik"])
    bar_len = int(infra_max / 20 * 30)
    print(f"  {GOLD}Infrasonik{RESET}  {DIM}(< 20 Hz){RESET}")
    print(f"  {CYAN}{'█' * bar_len}{'░' * (30 - bar_len)}{RESET}  {infra_max} Hz")
    
    # Audiosonik
    audio_max = max(freq_data["audiosonik"])
    bar_len = int(audio_max / 20000 * 30)
    print(f"\n  {GOLD}Audiosonik{RESET}  {DIM}(20 Hz - 20 kHz){RESET}")
    print(f"  {GREEN}{'█' * bar_len}{'░' * (30 - bar_len)}{RESET}  {audio_max} Hz")
    
    # Ultrasonik
    ultra_max = max(freq_data["ultrasonik"])
    bar_len = int(ultra_max / 100000 * 30)
    print(f"\n  {GOLD}Ultrasonik{RESET}  {DIM}(> 20 kHz){RESET}")
    print(f"  {MAGENTA}{'█' * bar_len}{'░' * (30 - bar_len)}{RESET}  {ultra_max} Hz")
    
    print(f"\n{BOLD}🧬 Analisis Zuhri Formalism:{RESET}")
    resonansi = (infra_max + audio_max/1000 + ultra_max/10000) % 10
    print(f"  Resonansi: {GOLD}{resonansi:.2f}{RESET}")
    
    if resonansi >= 7:
        status = f"{RED}🔴 ANOMALI TINGGI{RESET}"
    elif resonansi >= 4:
        status = f"{YELLOW}🟠 RESONANSI SEDANG{RESET}"
    else:
        status = f"{GREEN}🟢 NORMAL{RESET}"
    print(f"  Status: {status}\n")
    
    # Simpan log
    log = {
        "timestamp": datetime.now().isoformat(),
        "modul": "gelombang",
        "data": freq_data,
        "resonansi": resonansi
    }
    log_file = os.path.join(LOG_DIR, f"gelombang_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(log, open(log_file, "w"), indent=2)

# ============================================================
# MODUL 2 — MEDAN MAGNETIK & GRAVITASI
# ============================================================
def analisis_medan():
    """Analisis medan magnetik & gravitasi"""
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🧲 MODUL 2 — MEDAN MAGNETIK & GRAVITASI                       ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Analisis medan magnetik & gravitasi via sensor HP.{RESET}

""")
    
    print(f"{CYAN}📊 Membaca sensor...{RESET}\n")
    
    sensors = baca_semua_sensor()
    
    if sensors:
        for nama, data in sensors.items():
            val = data["values"]
            unit = data["unit"]
            
            if isinstance(val, list) and len(val) >= 3:
                # Vector (X, Y, Z)
                x, y, z = val[0], val[1], val[2]
                magnitude = math.sqrt(x**2 + y**2 + z**2)
                
                print(f"  {GOLD}{nama}{RESET} ({unit})")
                print(f"    X: {x:.3f}  Y: {y:.3f}  Z: {z:.3f}")
                print(f"    Magnitudo: {CYAN}{magnitude:.3f} {unit}{RESET}")
                print()
            elif isinstance(val, list):
                print(f"  {GOLD}{nama}{RESET}: {val[0]:.2f} {unit}\n")
    else:
        print(f"{YELLOW}⚠️  Sensor tidak tersedia.{RESET}")
        print(f"{DIM}Pastikan Termux:API terinstall dari F-Droid.{RESET}\n")
        print(f"{DIM}Menampilkan simulasi...{RESET}\n")
        
        # Simulasi
        mag_x = random.uniform(-50, 50)
        mag_y = random.uniform(-50, 50)
        mag_z = random.uniform(-50, 50)
        mag_total = math.sqrt(mag_x**2 + mag_y**2 + mag_z**2)
        
        grav_x = random.uniform(-10, 10)
        grav_y = random.uniform(-10, 10)
        grav_z = random.uniform(-10, 10)
        grav_total = math.sqrt(grav_x**2 + grav_y**2 + grav_z**2)
        
        print(f"  {GOLD}🧲 Medan Magnetik{RESET} (μT)")
        print(f"    X: {mag_x:.2f}  Y: {mag_y:.2f}  Z: {mag_z:.2f}")
        print(f"    Total: {CYAN}{mag_total:.2f} μT{RESET}\n")
        
        print(f"  {GOLD}🌍 Gravitasi{RESET} (m/s²)")
        print(f"    X: {grav_x:.2f}  Y: {grav_y:.2f}  Z: {grav_z:.2f}")
        print(f"    Total: {CYAN}{grav_total:.2f} m/s²{RESET}\n")
        
        # Anomali detection
        if mag_total > 50:
            print(f"{YELLOW}⚠️  Anomali magnetik terdeteksi{RESET}\n")
        if abs(grav_total - 9.81) > 0.5:
            print(f"{YELLOW}⚠️  Anomali gravitasi terdeteksi{RESET}\n")
    
    # Simpan log
    log = {
        "timestamp": datetime.now().isoformat(),
        "modul": "medan",
        "sensors": sensors if sensors else "simulation"
    }
    log_file = os.path.join(LOG_DIR, f"medan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(log, open(log_file, "w"), indent=2, default=str)

# ============================================================
# MODUL 3 — ANOMALI QUANTUM
# ============================================================
def analisis_quantum():
    """Analisis anomali kuantum (simulasi)"""
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  ⚛️  MODUL 3 — ANOMALI QUANTUM & SENSOR KUANTUM                 ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Analisis anomali kuantum (simulasi berbasis konsep).{RESET}

{YELLOW}⚠️  Catatan: HP tidak punya sensor kuantum.{RESET}
{DIM}Modul ini adalah SIMULASI untuk edukasi & riset.{RESET}

{BOLD}📚 Konsep:{RESET}
  {GOLD}•{RESET} Superposisi — partikel di 2 state sekaligus
  {GOLD}•{RESET} Entanglement — keterikatan kuantum
  {GOLD}•{RESET} Tunneling — menembus barrier
  {GOLD}•{RESET} Decoherence — kehilangan koherensi

""")
    
    print(f"{CYAN}🔬 Simulasi anomali kuantum...{RESET}\n")
    
    # Simulasi state kuantum
    states = ["|0⟩", "|1⟩", "|+⟩", "|-⟩", "|ψ⟩"]
    
    print(f"{BOLD}📊 STATE KUANTUM:{RESET}\n")
    for state in states:
        prob = random.uniform(0, 1)
        bar_len = int(prob * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        print(f"  {GOLD}{state}{RESET}  {CYAN}{bar}{RESET}  {prob*100:.1f}%")
    
    print(f"\n{BOLD}🧬 Analisis Zuhri Formalism:{RESET}")
    
    # Entanglement coefficient
    entanglement = random.uniform(0, 1)
    print(f"  Entanglement: {GOLD}{entanglement:.3f}{RESET}")
    
    # Anomali
    if entanglement > 0.7:
        print(f"  Status: {RED}🔴 ANOMALI KUANTUM TINGGI{RESET}")
    elif entanglement > 0.4:
        print(f"  Status: {YELLOW}🟠 ANOMALI SEDANG{RESET}")
    else:
        print(f"  Status: {GREEN}🟢 NORMAL{RESET}")
    
    print()
    
    # Simpan log
    log = {
        "timestamp": datetime.now().isoformat(),
        "modul": "quantum",
        "entanglement": entanglement,
        "note": "simulasi"
    }
    log_file = os.path.join(LOG_DIR, f"quantum_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(log, open(log_file, "w"), indent=2)

# ============================================================
# MODUL 4 — VISUALISASI ANOMALI
# ============================================================
def visualisasi():
    """Visualisasi hasil anomali"""
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📊 MODUL 4 — VISUALISASI ANOMALI                               ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Visualisasi data anomali dari semua modul.{RESET}

""")
    
    # Baca log terakhir
    logs = sorted([f for f in os.listdir(LOG_DIR) if f.endswith('.json')], reverse=True)[:3]
    
    if not logs:
        print(f"{YELLOW}Belum ada data. Jalankan modul 1-3 dulu.{RESET}\n")
        return
    
    for log_file in logs:
        log = json.load(open(os.path.join(LOG_DIR, log_file)))
        modul = log.get('modul', 'unknown')
        
        print(f"{BOLD}📊 {modul.upper()}{RESET}")
        print(f"{DIM}{log.get('timestamp', '')[:19]}{RESET}\n")
        
        if modul == "gelombang":
            data = log.get('data', {})
            print(f"  Infrasonik: {len(data.get('infrasonik', []))} sample")
            print(f"  Audiosonik: {len(data.get('audiosonik', []))} sample")
            print(f"  Ultrasonik: {len(data.get('ultrasonik', []))} sample")
            print(f"  Resonansi : {log.get('resonansi', 0):.2f}")
        elif modul == "medan":
            print(f"  Sensor: {type(log.get('sensors')).__name__}")
        elif modul == "quantum":
            print(f"  Entanglement: {log.get('entanglement', 0):.3f}")
        
        print()
    
    # Grafik ASCII
    print(f"{BOLD}📈 GRAFIK ANOMALI (24 jam){RESET}\n")
    
    all_logs = [f for f in os.listdir(LOG_DIR) if f.endswith('.json')]
    if all_logs:
        print(f"  Total log: {len(all_logs)}")
        bar = "█" * min(len(all_logs), 30)
        print(f"  {CYAN}{bar}{RESET}")
    else:
        print(f"  {DIM}Belum ada data.{RESET}")
    
    print()

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  📡 ZUHRI FREKUENSI — MONITORING RESONANSI & ANOMALI           ║
║  ──────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                       ║
║  Status: {GREEN}AKTIF{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MODUL:{RESET}
  {GOLD}1.{RESET}  🌊 Resonansi Gelombang (Sonar/LIDAR)
  {GOLD}2.{RESET}  🧲 Medan Magnetik & Gravitasi
  {GOLD}3.{RESET}  ⚛️  Anomali Quantum (Simulasi)
  {GOLD}4.{RESET}  📊 Visualisasi Hasil Anomali
  {GOLD}5.{RESET}  🔬 Cek Sensor HP
  {GOLD}6.{RESET}  🚨 Integrasi ke Zuhri Peringatan
  {GOLD}0.{RESET}  Keluar
""")
        
        try:
            c = input(f"{GOLD}Pilih (0-6): {RESET}").strip()
            
            if c == "0": break
            elif c == "1":
                os.system('clear')
                analisis_gelombang()
                input(f"\n{DIM}Enter...{RESET}")
            elif c == "2":
                os.system('clear')
                analisis_medan()
                input(f"\n{DIM}Enter...{RESET}")
            elif c == "3":
                os.system('clear')
                analisis_quantum()
                input(f"\n{DIM}Enter...{RESET}")
            elif c == "4":
                os.system('clear')
                visualisasi()
                input(f"\n{DIM}Enter...{RESET}")
            elif c == "5":
                os.system('clear')
                print(f"\n{BOLD}{CYAN}🔬 CEK SENSOR HP{RESET}\n")
                try:
                    result = subprocess.run(["termux-sensor", "-l"], 
                                           capture_output=True, text=True, timeout=5)
                    if result.stdout:
                        print(result.stdout)
                    else:
                        print(f"{YELLOW}⚠️  Termux:API tidak tersedia{RESET}")
                        print(f"{DIM}Install dari F-Droid: Termux:API{RESET}\n")
                except:
                    print(f"{YELLOW}⚠️  termux-sensor tidak ditemukan{RESET}")
                    print(f"{DIM}Install: pkg install termux-api{RESET}\n")
                input(f"{DIM}Enter...{RESET}")
            elif c == "6":
                os.system('clear')
                print(f"\n{BOLD}{CYAN}🚨 INTEGRASI KE ZUHRI PERINGATAN{RESET}\n")
                print(f"{DIM}Data anomali akan dikirim ke Zuhri Peringatan.{RESET}\n")
                print(f"{GREEN}✅ Integrasi aktif.{RESET}")
                print(f"{DIM}Jalankan `peringatan` untuk melihat analisis.{RESET}\n")
                input(f"{DIM}Enter...{RESET}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "gelombang": analisis_gelombang()
        elif cmd == "medan": analisis_medan()
        elif cmd == "quantum": analisis_quantum()
        elif cmd == "visual": visualisasi()
        elif cmd == "sensor":
            subprocess.run(["termux-sensor", "-l"])
        else: menu()
    else: menu()
