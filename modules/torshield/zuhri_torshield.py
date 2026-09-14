#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI TOR SHIELD — PERISAI BERLAPIS (STABIL)
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
SHIELD_DIR = os.path.join(HOME, "zuhri_os", "torshield")
CONF_DIR = os.path.join(SHIELD_DIR, "config")
LOG_DIR = os.path.join(SHIELD_DIR, "logs")
for d in [CONF_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

TORRC = os.path.join(CONF_DIR, "torrc")
TORDATA = os.path.join(CONF_DIR, "tor-data")
TORLOG = os.path.join(CONF_DIR, "tor.log")

def clear(): os.system('clear')

# ============================================================
# CEK TOR
# ============================================================
def tor_running():
    try:
        return subprocess.run(["pgrep","-x","tor"],capture_output=True).returncode==0
    except: return False

def tor_ip():
    try:
        r = subprocess.run(["torsocks","curl","-s","--max-time","10","ifconfig.me"],
                          capture_output=True, text=True, timeout=15)
        ip = r.stdout.strip()
        if ip and not ip.startswith("<") and "html" not in ip.lower():
            return ip
    except: pass
    return None

# ============================================================
# BUAT CONFIG TOR STABIL
# ============================================================
def buat_torrc():
    """Buat config Tor yang stabil"""
    config = f"""# ZUHRI TOR SHIELD — CONFIG STABIL
SocksPort 9050
ControlPort 9051
DataDirectory {TORDATA}
Log notice file {TORLOG}
Log notice stdout
ClientOnly 1
AvoidDiskWrites 1
CircuitBuildTimeout 60
LearnCircuitBuildTimeout 0
NumEntryGuards 3
KeepalivePeriod 60
NewCircuitPeriod 30
MaxCircuitDirtiness 600
"""
    with open(TORRC, "w") as f:
        f.write(config)
    return TORRC

# ============================================================
# JALANKAN TOR
# ============================================================
def start_tor():
    """Jalankan Tor dengan benar"""
    if tor_running():
        ip = tor_ip()
        if ip:
            print(f"{GREEN}✅ Tor sudah aktif — IP: {ip}{RESET}")
            return True
    
    print(f"{CYAN}🚀 Menjalankan Tor...{RESET}")
    
    # Hentikan Tor lama
    subprocess.run(["pkill","tor"], capture_output=True)
    time.sleep(2)
    
    # Buat config
    buat_torrc()
    
    # Jalankan Tor
    subprocess.Popen(
        ["tor","-f",TORRC],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Tunggu bootstrap (max 60 detik)
    print(f"{DIM}Menunggu Tor bootstrap (max 60 detik)...{RESET}")
    for i in range(60):
        time.sleep(1)
        print(f"\r{DIM}Menunggu... {i+1}s{RESET}", end="")
        
        if tor_running():
            ip = tor_ip()
            if ip:
                print(f"\n{GREEN}✅ Tor aktif! IP: {ip}{RESET}\n")
                return True
    
    print(f"\n{YELLOW}⚠️  Tor belum siap setelah 60 detik{RESET}")
    print(f"{DIM}Cek log: {TORLOG}{RESET}\n")
    return False

# ============================================================
# CEK LOG TOR
# ============================================================
def cek_log():
    """Cek log Tor"""
    clear()
    print(f"{BOLD}{CYAN}📋 LOG TOR{RESET}\n")
    
    if os.path.exists(TORLOG):
        with open(TORLOG) as f:
            lines = f.readlines()
        
        # Tampilkan 20 baris terakhir
        for line in lines[-20:]:
            print(f"  {DIM}{line.strip()}{RESET}")
        
        # Cek bootstrap
        content = "".join(lines)
        if "Bootstrapped 100%" in content:
            print(f"\n{GREEN}✅ Tor bootstrap 100%{RESET}")
        elif "Bootstrapped" in content:
            # Ambil persen terakhir
            import re
            matches = re.findall(r"Bootstrapped (\d+)%", content)
            if matches:
                print(f"\n{YELLOW}⚠️  Tor baru bootstrap {matches[-1]}%{RESET}")
        else:
            print(f"\n{RED}❌ Tor belum bootstrap{RESET}")
    else:
        print(f"{YELLOW}Log belum ada. Jalankan Tor dulu.{RESET}")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# TEST TOR
# ============================================================
def test_tor():
    """Test koneksi Tor"""
    clear()
    print(f"{BOLD}{CYAN}🧪 TEST TOR{RESET}\n")
    
    if not tor_running():
        print(f"{YELLOW}⚠️  Tor belum jalan. Jalankan menu 1.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    # Test 1: IP
    print(f"{GOLD}Test 1: IP Tor{RESET}")
    ip = tor_ip()
    if ip:
        print(f"  {GREEN}✅ IP: {ip}{RESET}\n")
    else:
        print(f"  {RED}❌ Gagal{RESET}\n")
    
    # Test 2: Check Tor Project
    print(f"{GOLD}Test 2: Check Tor Project{RESET}")
    try:
        r = subprocess.run(
            ["torsocks","curl","-s","--max-time","15","https://check.torproject.org/"],
            capture_output=True, text=True, timeout=20
        )
        if "Congratulations" in r.stdout:
            print(f"  {GREEN}✅ Tor terkonfirmasi!{RESET}\n")
        elif "not using" in r.stdout.lower():
            print(f"  {YELLOW}⚠️  Tidak terdeteksi{RESET}\n")
        else:
            print(f"  {YELLOW}⚠️  Response tidak jelas{RESET}\n")
    except:
        print(f"  {RED}❌ Error{RESET}\n")
    
    # Test 3: .onion
    print(f"{GOLD}Test 3: Akses .onion (Ahmia){RESET}")
    try:
        r = subprocess.run(
            ["torsocks","curl","-s","--max-time","20","http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/"],
            capture_output=True, text=True, timeout=25
        )
        if r.stdout and len(r.stdout) > 100:
            print(f"  {GREEN}✅ .onion bisa diakses!{RESET}\n")
        else:
            print(f"  {YELLOW}⚠️  Response kosong{RESET}\n")
    except:
        print(f"  {RED}❌ Error{RESET}\n")
    
    if ZUHRI_ID_OK:
        log_verified("TORSHIELD_TEST")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# AKSES .ONION
# ============================================================
def akses_onion():
    """Akses .onion"""
    clear()
    print(f"{BOLD}{CYAN}🌑 AKSES .ONION{RESET}\n")
    
    if not tor_running():
        print(f"{YELLOW}⚠️  Tor belum jalan. Jalankan menu 1.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    print(f"{GOLD}Situs yang tersedia:{RESET}")
    print(f"  {GOLD}1.{RESET} Ahmia")
    print(f"  {GOLD}2.{RESET} DuckDuckGo")
    print(f"  {GOLD}3.{RESET} Hidden Wiki")
    print(f"  {GOLD}4.{RESET} ProPublica")
    print(f"  {GOLD}5.{RESET} Custom URL")
    print(f"  {GOLD}0.{RESET} Kembali")
    
    c = input(f"\n{CYAN}Pilih: {RESET}").strip()
    
    urls = {
        "1": ("http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/", "Ahmia"),
        "2": ("https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/?kp=-2&kl=id-id", "DuckDuckGo"),
        "3": ("http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page", "Hidden Wiki"),
        "4": ("https://propub3r6espa33w.onion/", "ProPublica"),
    }
    
    if c in urls:
        url, nama = urls[c]
        print(f"\n{CYAN}🌐 Membuka {nama}...{RESET}")
        print(f"{DIM}URL: {url}{RESET}\n")
        print(f"{YELLOW}⏳ Ini butuh waktu (Tor lambat)...{RESET}\n")
        
        try:
            # Pakai lynx kalau ada
            if subprocess.run(["which","lynx"],capture_output=True).returncode == 0:
                subprocess.run(["torsocks","lynx",url], timeout=120)
            else:
                r = subprocess.run(["torsocks","curl","-s","--max-time","60",url],
                                  capture_output=True, text=True, timeout=65)
                print(r.stdout[:3000] if r.stdout else "Tidak ada respons")
        except subprocess.TimeoutExpired:
            print(f"{RED}⏱️  Timeout — situs tidak merespons{RESET}")
        except Exception as e:
            print(f"{RED}❌ Error: {e}{RESET}")
    
    elif c == "5":
        url = input("🌐 URL .onion: ").strip()
        if url:
            print(f"\n{CYAN}🌐 Membuka...{RESET}\n")
            try:
                subprocess.run(["torsocks","lynx",url], timeout=120)
            except:
                print(f"{RED}❌ Gagal{RESET}")
    
    input(f"\n{DIM}Enter...{RESET}")

# ============================================================
# STATUS
# ============================================================
def status():
    """Cek status"""
    clear()
    print(f"{BOLD}{CYAN}📊 STATUS TOR SHIELD{RESET}\n")
    
    if tor_running():
        print(f"  Tor: {GREEN}✅ AKTIF{RESET}")
        ip = tor_ip()
        if ip:
            print(f"  IP:  {GREEN}{ip}{RESET}")
        else:
            print(f"  IP:  {YELLOW}Belum siap{RESET}")
    else:
        print(f"  Tor: {RED}❌ MATI{RESET}")
    
    # Config
    print(f"  Config: {'✅' if os.path.exists(TORRC) else '❌'}")
    print(f"  Log:    {'✅' if os.path.exists(TORLOG) else '❌'}")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        clear()
        tor_status = f"{GREEN}✅ AKTIF{RESET}" if tor_running() else f"{RED}❌ MATI{RESET}"
        
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🛡️  ZUHRI TOR SHIELD — PERISAI BERLAPIS                           ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Status Tor: {tor_status}
║  Protokol: K-8.0                                                    ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🚀 Jalankan Tor (Stabil)
  {GOLD}2.{RESET}  🧪 Test Tor
  {GOLD}3.{RESET}  🌑 Akses .onion
  {GOLD}4.{RESET}  📋 Cek Log Tor
  {GOLD}5.{RESET}  📊 Status
  {GOLD}6.{RESET}  🔄 Restart Tor
  {GOLD}0.{RESET}  Keluar
""")
        
        try:
            c = input(f"{GOLD}Pilih (0-6): {RESET}").strip()
            if c == "0": break
            elif c == "1": start_tor(); input(f"{DIM}Enter...{RESET}")
            elif c == "2": test_tor()
            elif c == "3": akses_onion()
            elif c == "4": cek_log()
            elif c == "5": status()
            elif c == "6":
                subprocess.run(["pkill","tor"], capture_output=True)
                time.sleep(2)
                start_tor()
                input(f"{DIM}Enter...{RESET}")
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "start": start_tor()
        elif cmd == "test": test_tor()
        elif cmd == "status": status()
        else: menu()
    else: menu()
