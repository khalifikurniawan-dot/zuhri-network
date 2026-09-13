#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI BOTNET HUNTER — DETEKSI ANCAMAN JARINGAN
Monitor koneksi, proses, DNS, dan port
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, subprocess, re
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
BOTNET_DIR = os.path.join(HOME, "zuhri_os", "botnet")
DATA_DIR = os.path.join(BOTNET_DIR, "data")
LOG_DIR = os.path.join(BOTNET_DIR, "logs")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# DATABASE PROSES MENCURIGAKAN
# ============================================================
SUSPICIOUS_PROCESSES = [
    "nc", "ncat", "netcat", "telnet", "socat",  # Reverse shell
    "miner", "xmrig", "cgminer", "bfgminer",    # Crypto miner
    "wget", "curl",                              # Download mencurigakan (hati-hati)
    "ssh", "scp", "sftp",                        # Remote access
    "python -m http.server",                     # Server local
    "mimikatz", "meterpreter", "metasploit",     # Tools hacking
]

SUSPICIOUS_PORTS = [
    22, 23, 445, 3389, 4444, 5555, 6666, 31337,  # Backdoor umum
    1080, 3128, 8080, 8888,                      # Proxy
]

SUSPICIOUS_DNS_KEYWORDS = [
    "dyndns", "no-ip", "duckdns", "hopto", "zapto", "serveftp",
    "ngrok", "serveo", "localhost.run", "telebit",
    "onion", "tor", "i2p",
]

# ============================================================
# CEK PROSES
# ============================================================
def cek_proses():
    """Cek proses mencurigakan"""
    print(f"{CYAN}🔍 Memindai proses...{RESET}\n")
    
    threats = []
    
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=10)
        lines = result.stdout.split('\n')
        
        for line in lines:
            for sus in SUSPICIOUS_PROCESSES:
                if sus in line and "grep" not in line and "botnet" not in line:
                    threats.append({
                        "type": "process",
                        "severity": "WARNING",
                        "detail": line.strip()[:100]
                    })
                    break
    except: pass
    
    if threats:
        print(f"{YELLOW}⚠️  {len(threats)} proses mencurigakan:{RESET}")
        for t in threats[:10]:
            print(f"  {RED}•{RESET} {t['detail']}")
    else:
        print(f"{GREEN}✅ Tidak ada proses mencurigakan{RESET}")
    
    print()
    return threats

# ============================================================
# CEK KONEKSI JARINGAN
# ============================================================
def cek_koneksi():
    """Cek koneksi jaringan aktif"""
    print(f"{CYAN}🌐 Memindai koneksi jaringan...{RESET}\n")
    
    threats = []
    
    try:
        result = subprocess.run(["ss", "-tuln"], capture_output=True, text=True, timeout=10)
        lines = result.stdout.split('\n')
        
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 5:
                local = parts[4] if len(parts) > 4 else ""
                
                # Cek port
                match = re.search(r':(\d+)$', local)
                if match:
                    port = int(match.group(1))
                    if port in SUSPICIOUS_PORTS:
                        threats.append({
                            "type": "port",
                            "severity": "WARNING",
                            "detail": f"Port {port} terbuka: {line.strip()[:80]}"
                        })
    except: pass
    
    if threats:
        print(f"{YELLOW}⚠️  {len(threats)} port mencurigakan:{RESET}")
        for t in threats[:10]:
            print(f"  {RED}•{RESET} {t['detail']}")
    else:
        print(f"{GREEN}✅ Tidak ada port mencurigakan{RESET}")
    
    print()
    return threats

# ============================================================
# CEK KONEKSI ESTABLISHED
# ============================================================
def cek_koneksi_aktif():
    """Cek koneksi aktif keluar"""
    print(f"{CYAN}📡 Memindai koneksi aktif...{RESET}\n")
    
    try:
        result = subprocess.run(["ss", "-tun"], capture_output=True, text=True, timeout=10)
        lines = result.stdout.split('\n')
        
        established = []
        for line in lines[1:]:
            if "ESTAB" in line:
                parts = line.split()
                if len(parts) >= 5:
                    remote = parts[5] if len(parts) > 5 else ""
                    established.append(remote)
        
        if established:
            print(f"{GOLD}🔗 {len(established)} koneksi aktif:{RESET}")
            for c in established[:10]:
                print(f"  {CYAN}→{RESET} {c}")
        else:
            print(f"{GREEN}✅ Tidak ada koneksi aktif keluar{RESET}")
        
        print()
        return established
    except:
        print(f"{YELLOW}⚠️  Tidak bisa cek koneksi{RESET}\n")
        return []

# ============================================================
# CEK FILE MENCURIGAKAN
# ============================================================
def cek_file():
    """Cek file mencurigakan di home"""
    print(f"{CYAN}📂 Memindai file...{RESET}\n")
    
    threats = []
    
    # File dengan nama aneh
    suspicious_names = [".miner", ".bot", ".rat", ".keylog", ".crypt", "xmrig"]
    
    try:
        for f in os.listdir(HOME):
            for sus in suspicious_names:
                if sus in f.lower():
                    threats.append({
                        "type": "file",
                        "detail": f"File mencurigakan: {f}"
                    })
                    break
    except: pass
    
    if threats:
        print(f"{YELLOW}⚠️  {len(threats)} file mencurigakan:{RESET}")
        for t in threats:
            print(f"  {RED}•{RESET} {t['detail']}")
    else:
        print(f"{GREEN}✅ Tidak ada file mencurigakan{RESET}")
    
    print()
    return threats

# ============================================================
# CEK DNS
# ============================================================
def cek_dns():
    """Cek DNS request mencurigakan"""
    print(f"{CYAN}🔍 Memeriksa DNS...{RESET}\n")
    
    # Cek /etc/hosts
    try:
        if os.path.exists("/etc/hosts"):
            with open("/etc/hosts") as f:
                content = f.read()
                for kw in SUSPICIOUS_DNS_KEYWORDS:
                    if kw in content.lower():
                        print(f"{YELLOW}⚠️  DNS mencurigakan: {kw}{RESET}")
                        return [{"type": "dns", "detail": kw}]
    except: pass
    
    print(f"{GREEN}✅ Tidak ada DNS mencurigakan{RESET}\n")
    return []

# ============================================================
# FULL SCAN
# ============================================================
def full_scan():
    """Scan lengkap"""
    os.system('clear')
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🛡️  ZUHRI BOTNET HUNTER — FULL SCAN                           ║
║  ──────────────────────────────────────────────────────────────  ║
║  Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                  ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Memindai sistem... (5-10 detik){RESET}
""")
    
    all_threats = []
    all_threats.extend(cek_proses())
    all_threats.extend(cek_koneksi())
    all_threats.extend(cek_file())
    all_threats.extend(cek_dns())
    connections = cek_koneksi_aktif()
    
    # Ringkasan
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📊 RINGKASAN SCAN                                             ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  Total ancaman  : {RED if all_threats else GREEN}{len(all_threats)}{RESET}
  Koneksi aktif  : {len(connections)}
  Waktu scan     : {datetime.now().strftime('%H:%M:%S')}
""")
    
    if all_threats:
        print(f"{YELLOW}⚠️  Perlu perhatian:{RESET}")
        for t in all_threats[:5]:
            print(f"  {RED}•{RESET} [{t['type']}] {t['detail'][:60]}")
    else:
        print(f"{GREEN}✅ Sistem AMAN — tidak ada ancaman{RESET}")
    
    # Simpan log
    log = {
        "timestamp": datetime.now().isoformat(),
        "threats": all_threats,
        "connections": connections,
        "status": "CLEAN" if not all_threats else "WARNING"
    }
    log_file = os.path.join(LOG_DIR, f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(log, open(log_file, "w"), indent=2)
    
    if ZUHRI_ID_OK:
        log_verified(f"BOTNET_SCAN: {len(all_threats)} ancaman")
    
    print()
    input(f"{DIM}Tekan Enter...{RESET}")

# ============================================================
# LIHAT LOG
# ============================================================
def lihat_log():
    """Lihat log scan sebelumnya"""
    os.system('clear')
    logs = sorted([f for f in os.listdir(LOG_DIR) if f.startswith('scan_')], reverse=True)
    
    print(f"\n{BOLD}{CYAN}📊 LOG SCAN BOTNET HUNTER{RESET}\n")
    
    if not logs:
        print(f"{YELLOW}Belum ada log.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    for log_file in logs[:10]:
        try:
            log = json.load(open(os.path.join(LOG_DIR, log_file)))
            ts = log['timestamp'][:19]
            threat_count = len(log.get('threats', []))
            status = log.get('status', 'UNKNOWN')
            
            color = GREEN if status == "CLEAN" else YELLOW
            icon = "✅" if status == "CLEAN" else "⚠️"
            
            print(f"  {icon} {ts}  {color}{status:8}{RESET}  {threat_count} ancaman")
        except: pass
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🛡️  ZUHRI BOTNET HUNTER — DETEKSI ANCAMAN JARINGAN            ║
║  ──────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                       ║
║  Status: {GREEN}AKTIF{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🔍 Full Scan (Deteksi Lengkap)
  {GOLD}2.{RESET}  ⚙️  Cek Proses Mencurigakan
  {GOLD}3.{RESET}  🌐 Cek Port Terbuka
  {GOLD}4.{RESET}  📡 Cek Koneksi Aktif
  {GOLD}5.{RESET}  📂 Cek File Mencurigakan
  {GOLD}6.{RESET}  🔍 Cek DNS
  {GOLD}7.{RESET}  📊 Log Scan Sebelumnya
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-7): {RESET}").strip()
            if c == "0": break
            elif c == "1": full_scan()
            elif c == "2":
                os.system('clear'); cek_proses(); input(f"{DIM}Enter...{RESET}")
            elif c == "3":
                os.system('clear'); cek_koneksi(); input(f"{DIM}Enter...{RESET}")
            elif c == "4":
                os.system('clear'); cek_koneksi_aktif(); input(f"{DIM}Enter...{RESET}")
            elif c == "5":
                os.system('clear'); cek_file(); input(f"{DIM}Enter...{RESET}")
            elif c == "6":
                os.system('clear'); cek_dns(); input(f"{DIM}Enter...{RESET}")
            elif c == "7": lihat_log()
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "scan": full_scan()
        elif cmd == "log": lihat_log()
        else: menu()
    else: menu()
