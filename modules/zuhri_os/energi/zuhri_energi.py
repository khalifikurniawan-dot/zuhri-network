#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI ENERGI — KEMANDIRIAN ENERGI DIGITAL
Monitor Baterai • Optimasi Daya • Statistik
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, subprocess, time
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
ENERGI_DIR = os.path.join(HOME, "zuhri_os", "energi")
DATA_DIR = os.path.join(ENERGI_DIR, "data")
LOG_DIR = os.path.join(ENERGI_DIR, "logs")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# BACA BATERAI
# ============================================================
def baca_baterai():
    """Baca status baterai via termux-api"""
    try:
        r = subprocess.run(["termux-battery-status"], capture_output=True, text=True, timeout=5)
        if r.stdout:
            return json.loads(r.stdout)
    except: pass
    return None

def get_baterai_info():
    """Dapatkan info baterai lengkap"""
    data = baca_baterai()
    
    if not data:
        # Fallback: baca dari /sys/class/power_supply
        info = {}
        try:
            with open("/sys/class/power_supply/battery/capacity") as f:
                info["percentage"] = int(f.read().strip())
        except: pass
        try:
            with open("/sys/class/power_supply/battery/status") as f:
                info["status"] = f.read().strip()
        except: pass
        try:
            with open("/sys/class/power_supply/battery/temp") as f:
                info["temperature"] = int(f.read().strip()) / 10
        except: pass
        try:
            with open("/sys/class/power_supply/battery/voltage_now") as f:
                info["voltage"] = int(f.read().strip()) / 1000000
        except: pass
        
        return info if info else None
    
    return data

# ============================================================
# TAMPILKAN STATUS
# ============================================================
def show_status():
    data = get_baterai_info()
    
    if not data:
        print(f"{RED}❌ Tidak bisa baca baterai.{RESET}")
        print(f"{DIM}Pastikan Termux:API terinstall dari F-Droid.{RESET}\n")
        return
    
    pct = data.get('percentage', 0)
    status = data.get('status', 'UNKNOWN')
    temp = data.get('temperature', 0)
    voltage = data.get('voltage', 0)
    health = data.get('health', 'UNKNOWN')
    plugged = data.get('plugged', 'UNPLUGGED')
    
    # Warna berdasarkan level
    if pct >= 60:
        color = GREEN
        emoji = "🔋"
    elif pct >= 30:
        color = YELLOW
        emoji = "🪫"
    else:
        color = RED
        emoji = "🪫"
    
    # Bar visual
    bar_len = int(pct / 5)
    bar = "█" * bar_len + "░" * (20 - bar_len)
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  ⚡ ZUHRI ENERGI — STATUS BATERAI                              ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  {emoji} {BOLD}Level:{RESET} {color}{pct}%{RESET}
  {color}{bar}{RESET}

  {GOLD}📊 Status:{RESET}      {status}
  {GOLD}🌡️  Suhu:{RESET}        {temp}°C
  {GOLD}⚡ Voltase:{RESET}     {voltage} V
  {GOLD}💚 Kesehatan:{RESET}   {health}
  {GOLD}🔌 Pengisian:{RESET}   {plugged}
  {GOLD}📅 Waktu:{RESET}       {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")
    
    # Simpan log
    if ZUHRI_ID_OK:
        log_file = os.path.join(LOG_DIR, f"baterai_{datetime.now().strftime('%Y%m%d')}.json")
        logs = []
        if os.path.exists(log_file):
            try: logs = json.load(open(log_file))
            except: logs = []
        logs.append({
            "time": datetime.now().isoformat(),
            "percentage": pct,
            "status": status,
            "temp": temp,
            "voltage": voltage
        })
        json.dump(logs, open(log_file, "w"), indent=2)
        log_verified(f"ENERGI: {pct}% - {status}")
    
    # Saran
    print(f"{BOLD}💡 Saran:{RESET}")
    if pct < 20:
        print(f"  {RED}⚠️  Baterai rendah! Segera charge.{RESET}")
    elif pct < 50:
        print(f"  {YELLOW}⚠️  Baterai sedang. Bisa charge nanti.{RESET}")
    elif pct > 90 and status == "CHARGING":
        print(f"  {GREEN}✅ Baterai hampir penuh. Cabut charger.{RESET}")
    else:
        print(f"  {GREEN}✅ Baterai aman.{RESET}")
    
    if temp > 40:
        print(f"  {RED}🌡️  Suhu tinggi! Hindari penggunaan berat.{RESET}")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# STATISTIK
# ============================================================
def show_stats():
    log_files = sorted([f for f in os.listdir(LOG_DIR) if f.startswith('baterai_')])
    
    if not log_files:
        print(f"{YELLOW}Belum ada data.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    all_logs = []
    for f in log_files[-7:]:  # 7 hari terakhir
        try:
            logs = json.load(open(os.path.join(LOG_DIR, f)))
            all_logs.extend(logs)
        except: pass
    
    if not all_logs:
        print(f"{YELLOW}Belum ada data.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    # Statistik
    total = len(all_logs)
    avg_pct = sum(l.get('percentage', 0) for l in all_logs) / total
    avg_temp = sum(l.get('temp', 0) for l in all_logs) / total
    max_pct = max(l.get('percentage', 0) for l in all_logs)
    min_pct = min(l.get('percentage', 0) for l in all_logs)
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  📊 STATISTIK BATERAI — 7 HARI TERAKHIR                        ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}Total sampel:{RESET}    {total}
  {GOLD}Rata-rata level:{RESET} {avg_pct:.1f}%
  {GOLD}Level tertinggi:{RESET} {max_pct}%
  {GOLD}Level terendah:{RESET}  {min_pct}%
  {GOLD}Rata-rata suhu:{RESET}  {avg_temp:.1f}°C
""")
    
    # Grafik per hari
    print(f"{BOLD}📈 GRAFIK HARIAN:{RESET}\n")
    for f in log_files[-7:]:
        try:
            logs = json.load(open(os.path.join(LOG_DIR, f)))
            if logs:
                avg = sum(l.get('percentage', 0) for l in logs) / len(logs)
                bar_len = int(avg / 5)
                bar = "█" * bar_len + "░" * (20 - bar_len)
                date = f.replace('baterai_', '').replace('.json', '')
                date_fmt = f"{date[6:8]}/{date[4:6]}/{date[0:4]}"
                color = GREEN if avg > 60 else (YELLOW if avg > 30 else RED)
                print(f"  {date_fmt}  {color}{bar}{RESET} {avg:.0f}%")
        except: pass
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# OPTIMASI DAYA
# ============================================================
def optimasi_daya():
    data = get_baterai_info()
    if not data:
        print(f"{RED}❌ Tidak bisa baca baterai.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    pct = data.get('percentage', 0)
    temp = data.get('temperature', 0)
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  ⚡ OPTIMASI DAYA — ZUHRI ENERGI                               ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  Level saat ini: {GOLD}{pct}%{RESET}
  Suhu saat ini:  {GOLD}{temp}°C{RESET}

{BOLD}💡 Rekomendasi Hemat Daya:{RESET}
""")
    
    tips = []
    
    if pct < 30:
        tips.append(f"{RED}🔴 KRITIS:{RESET}")
        tips.append("  • Aktifkan mode hemat daya di HP")
        tips.append("  • Matikan WiFi/Bluetooth jika tidak dipakai")
        tips.append("  • Turunkan kecerahan layar")
        tips.append("  • Tutup aplikasi background")
        tips.append("  • Jangan pakai AI atau Tor")
    elif pct < 60:
        tips.append(f"{YELLOW}🟡 SEDANG:{RESET}")
        tips.append("  • Batasi penggunaan AI")
        tips.append("  • Matikan GPS jika tidak dipakai")
        tips.append("  • Gunakan dark mode")
    else:
        tips.append(f"{GREEN}🟢 AMAN:{RESET}")
        tips.append("  • Bisa pakai fitur berat")
        tips.append("  • Bisa jalan Tor/AI")
    
    if temp > 40:
        tips.append(f"\n{RED}🌡️  SUHU TINGGI:{RESET}")
        tips.append("  • Istirahatkan HP sejenak")
        tips.append("  • Jangan charge sambil pakai")
    
    for tip in tips:
        print(f"  {tip}")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# PREDIKSI
# ============================================================
def prediksi():
    data = get_baterai_info()
    if not data:
        print(f"{RED}❌ Tidak bisa baca baterai.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    pct = data.get('percentage', 0)
    status = data.get('status', 'UNKNOWN')
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🔮 PREDIKSI BATERAI — ZUHRI ENERGI                            ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  Level: {GOLD}{pct}%{RESET}  |  Status: {GOLD}{status}{RESET}

""")
    
    if status == "CHARGING":
        # Estimasi waktu charge
        sisa_pct = 100 - pct
        estimasi = sisa_pct * 2  # Asumsi 2 menit per %
        print(f"{GREEN}🔌 Sedang charging{RESET}")
        print(f"  Estimasi penuh: {GOLD}{estimasi} menit{RESET}\n")
    else:
        # Estimasi waktu pakai
        if pct > 80: estimasi = "8-12 jam"
        elif pct > 60: estimasi = "5-8 jam"
        elif pct > 40: estimasi = "3-5 jam"
        elif pct > 20: estimasi = "1-3 jam"
        elif pct > 10: estimasi = "30-60 menit"
        else: estimasi = "< 30 menit"
        
        print(f"{YELLOW}🔋 Sedang dipakai{RESET}")
        print(f"  Estimasi bertahan: {GOLD}{estimasi}{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        
        # Cek baterai untuk header
        data = get_baterai_info()
        pct = data.get('percentage', '?') if data else '?'
        
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  ⚡ ZUHRI ENERGI — KEMANDIRIAN ENERGI DIGITAL                  ║
║  ──────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                       ║
║  Baterai: {GOLD}{pct}%{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🔋 Status Baterai
  {GOLD}2.{RESET}  📊 Statistik (7 hari)
  {GOLD}3.{RESET}  ⚡ Optimasi Daya
  {GOLD}4.{RESET}  🔮 Prediksi Baterai
  {GOLD}5.{RESET}  📈 Monitor Real-time
  {GOLD}0.{RESET}  Keluar
""")
        
        try:
            c = input(f"{GOLD}Pilih (0-5): {RESET}").strip()
            if c == "0": break
            elif c == "1":
                os.system('clear'); show_status()
            elif c == "2":
                os.system('clear'); show_stats()
            elif c == "3":
                os.system('clear'); optimasi_daya()
            elif c == "4":
                os.system('clear'); prediksi()
            elif c == "5":
                monitor_realtime()
        except KeyboardInterrupt: break

def monitor_realtime():
    """Monitor baterai real-time"""
    print(f"\n{BOLD}{CYAN}📈 MONITOR REAL-TIME (CTRL+C untuk stop){RESET}\n")
    try:
        while True:
            data = get_baterai_info()
            if data:
                pct = data.get('percentage', 0)
                temp = data.get('temperature', 0)
                status = data.get('status', '?')
                bar_len = int(pct / 5)
                bar = "█" * bar_len + "░" * (20 - bar_len)
                color = GREEN if pct > 60 else (YELLOW if pct > 30 else RED)
                print(f"\r  {color}{bar}{RESET} {pct:3}%  {temp}°C  {status}     ", end="")
            time.sleep(5)
    except KeyboardInterrupt:
        print(f"\n\n{DIM}Monitor dihentikan.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "status": show_status()
        elif cmd == "stats": show_stats()
        elif cmd == "monitor": monitor_realtime()
        else: menu()
    else: menu()
