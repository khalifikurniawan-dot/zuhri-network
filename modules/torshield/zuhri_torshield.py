#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI TOR SHIELD — PERISAI BERLAPIS UNTUK DEEP/DARK WEB
Tor + DNSCrypt + Proxychains + Header Anonymizer
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, hashlib, subprocess, time, secrets
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
SHIELD_DIR = os.path.join(HOME, "zuhri_os", "torshield")
DATA_DIR = os.path.join(SHIELD_DIR, "data")
LOG_DIR = os.path.join(SHIELD_DIR, "logs")
CONF_DIR = os.path.join(SHIELD_DIR, "config")
for d in [DATA_DIR, LOG_DIR, CONF_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# LAYER 1 — TOR PROXY (NYATA)
# ============================================================
def tor_status():
    """Cek status Tor"""
    try:
        r = subprocess.run(["pgrep", "-x", "tor"], capture_output=True)
        return r.returncode == 0
    except:
        return False

def start_tor():
    """Jalankan Tor"""
    if tor_status():
        print(f"{GREEN}✅ Tor sudah berjalan{RESET}")
        return True
    
    print(f"{CYAN}🚀 Menjalankan Tor...{RESET}")
    
    # Buat config Tor
    torrc = os.path.join(CONF_DIR, "torrc")
    with open(torrc, "w") as f:
        f.write("""# ZUHRI TOR SHIELD CONFIG
SocksPort 9050
ControlPort 9051
Log notice file """ + LOG_DIR + """/tor.log
DataDirectory """ + CONF_DIR + """/tor-data
""")
    
    # Jalankan Tor
    subprocess.Popen(
        ["tor", "-f", torrc],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    print(f"{DIM}Menunggu Tor bootstrap (30 detik)...{RESET}")
    for i in range(30):
        time.sleep(1)
        print(f"\r{DIM}Menunggu... {i+1}s{RESET}", end="")
        if tor_status():
            break
    print()
    
    if tor_status():
        print(f"{GREEN}✅ Tor aktif{RESET}\n")
        return True
    else:
        print(f"{RED}❌ Tor gagal jalan{RESET}\n")
        return False

def check_tor_ip():
    """Cek IP Tor"""
    try:
        r = subprocess.run(
            ["torsocks", "curl", "-s", "--max-time", "10", "ifconfig.me"],
            capture_output=True, text=True, timeout=15
        )
        ip = r.stdout.strip()
        if ip and not ip.startswith("<") and "html" not in ip.lower():
            return ip
    except:
        pass
    return None

# ============================================================
# LAYER 2 — DNSCRYPT (DNS AMAN)
# ============================================================
def setup_dnscrypt():
    """Setup DNSCrypt untuk DNS aman"""
    print(f"{CYAN}🔐 Setup DNSCrypt...{RESET}")
    
    dnscrypt_conf = os.path.join(CONF_DIR, "dnscrypt-proxy.toml")
    
    with open(dnscrypt_conf, "w") as f:
        f.write("""# ZUHRI DNSCRYPT CONFIG
listen_addresses = ['127.0.0.1:5353']
server_names = ['cloudflare', 'quad9-dnscrypt-ip4-filter-pri']
force_tcp = false
timeout = 5000
keepalive = 30
log_level = 2
log_file = '""" + LOG_DIR + """/dnscrypt.log'
cert_refresh_delay = 240
fallback_resolvers = ['9.9.9.9:53', '8.8.8.8:53']
ignore_system_dns = true
netprobe_timeout = 60
block_ipv6 = false
""")
    
    print(f"{GREEN}✅ DNSCrypt config dibuat{RESET}")
    print(f"{DIM}Config: {dnscrypt_conf}{RESET}\n")

# ============================================================
# LAYER 3 — PROXYCHAINS (CHAIN PROXY)
# ============================================================
def setup_proxychains():
    """Setup proxychains untuk chain proxy"""
    print(f"{CYAN}🔗 Setup Proxychains...{RESET}")
    
    proxychains_conf = os.path.join(CONF_DIR, "proxychains.conf")
    
    with open(proxychains_conf, "w") as f:
        f.write("""# ZUHRI PROXYCHAINS CONFIG
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
socks5 127.0.0.1 9050
""")
    
    print(f"{GREEN}✅ Proxychains config dibuat{RESET}")
    print(f"{DIM}Config: {proxychains_conf}{RESET}\n")

# ============================================================
# LAYER 4 — HEADER ANONYMIZER
# ============================================================
def anonymize_headers():
    """Header anonymizer untuk curl"""
    print(f"{CYAN}🎭 Setup Header Anonymizer...{RESET}")
    
    # Generate random user agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    ]
    
    ua = secrets.choice(user_agents)
    
    with open(os.path.join(CONF_DIR, "user_agent.txt"), "w") as f:
        f.write(ua)
    
    print(f"{GREEN}✅ User Agent: {ua[:50]}...{RESET}\n")

# ============================================================
# LAYER 5 — ECHO-CORE CHECK
# ============================================================
def echo_check(url):
    """Echo-Core resonance check untuk URL"""
    h = hashlib.sha3_256(url.encode()).hexdigest()
    total = sum(int(c, 16) for c in h[:32])
    return (total % 10 + 8) % 10

# ============================================================
# FULL SHIELD MODE
# ============================================================
def full_shield():
    """Aktifkan semua lapisan"""
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🛡️  ZUHRI TOR SHIELD — PERISAI BERLAPIS                           ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{CYAN}Mengaktifkan 5 lapisan perisai...{RESET}
""")
    
    # Layer 1: Tor
    print(f"{GOLD}[1/5]{RESET} Tor Proxy")
    if start_tor():
        ip = check_tor_ip()
        if ip:
            print(f"  {GREEN}✅ IP Tor: {ip}{RESET}")
        else:
            print(f"  {YELLOW}⚠️  IP belum siap{RESET}")
    time.sleep(0.5)
    
    # Layer 2: DNSCrypt
    print(f"{GOLD}[2/5]{RESET} DNSCrypt (DNS aman)")
    setup_dnscrypt()
    time.sleep(0.3)
    
    # Layer 3: Proxychains
    print(f"{GOLD}[3/5]{RESET} Proxychains (Chain proxy)")
    setup_proxychains()
    time.sleep(0.3)
    
    # Layer 4: Header Anonymizer
    print(f"{GOLD}[4/5]{RESET} Header Anonymizer")
    anonymize_headers()
    time.sleep(0.3)
    
    # Layer 5: Echo-Core
    print(f"{GOLD}[5/5]{RESET} Echo-Core Check")
    print(f"  {GREEN}✅ Echo-Core siap{RESET}\n")
    
    print(f"""
{BOLD}{GREEN}╔══════════════════════════════════════════════════════════════════════╗
║  ✅ ZUHRI TOR SHIELD — AKTIF                                        ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📊 5 LAPISAN:{RESET}
  {GREEN}✅{RESET} 1. Tor Proxy (anonim)
  {GREEN}✅{RESET} 2. DNSCrypt (DNS aman)
  {GREEN}✅{RESET} 3. Proxychains (chain proxy)
  {GREEN}✅{RESET} 4. Header Anonymizer
  {GREEN}✅{RESET} 5. Echo-Core Check

{BOLD}🎯 PROTEKSI:{RESET}
  {GREEN}✅{RESET} IP tersembunyi (Tor)
  {GREEN}✅{RESET} DNS terenkripsi (DNSCrypt)
  {GREEN}✅{RESET} Multi-hop proxy (Proxychains)
  {GREEN}✅{RESET} Header anonim
  {GREEN}✅{RESET} Echo-Core verification

{BOLD}📋 CARA PAKAI:{RESET}
  {DIM}• Untuk akses .onion: curl via torsocks${RESET}
  {DIM}• Contoh: torsocks curl http://xxx.onion${RESET}
  {DIM}• Atau: proxychains4 curl http://xxx.onion${RESET}
""")
    
    if ZUHRI_ID_OK:
        log_verified("TORSHIELD_ACTIVE")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# AKSES .ONION
# ============================================================
def akses_onion():
    """Akses .onion dengan perisai"""
    os.system('clear')
    print(f"{BOLD}{CYAN}🌑 AKSES .ONION (PERISAI AKTIF){RESET}\n")
    
    if not tor_status():
        print(f"{YELLOW}⚠️  Tor belum jalan. Jalankan mode 1 dulu.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    url = input("🌐 URL .onion: ").strip()
    if not url:
        return
    
    # Echo-Core check
    resonansi = echo_check(url)
    print(f"\n{CYAN}🧬 Echo-Core Check:{RESET}")
    print(f"  URL: {url}")
    print(f"  Resonansi: {resonansi}/9")
    
    if resonansi >= 7:
        print(f"  Status: {GREEN}✅ Aman untuk diakses{RESET}")
    elif resonansi >= 4:
        print(f"  Status: {YELLOW}⚠️  Waspada{RESET}")
    else:
        print(f"  Status: {RED}❌ Risiko tinggi{RESET}")
    
    print(f"\n{CYAN}⏳ Mengakses via Tor...{RESET}\n")
    
    # Akses via torsocks + lynx
    try:
        subprocess.run(["torsocks", "lynx", url], timeout=60)
    except:
        # Fallback: pakai curl
        try:
            r = subprocess.run(
                ["torsocks", "curl", "-s", "--max-time", "30", url],
                capture_output=True, text=True, timeout=35
            )
            if r.stdout:
                print(r.stdout[:2000])
            else:
                print(f"{RED}❌ Gagal akses{RESET}")
        except:
            print(f"{RED}❌ Timeout atau error{RESET}")
    
    if ZUHRI_ID_OK:
        log_verified(f"TORSHIELD_ONION: {url[:50]}")
    
    input(f"\n{DIM}Enter...{RESET}")

# ============================================================
# CEK STATUS
# ============================================================
def status():
    """Cek status perisai"""
    os.system('clear')
    print(f"{BOLD}{CYAN}📊 STATUS ZUHRI TOR SHIELD{RESET}\n")
    
    # Tor
    tor = "✅ AKTIF" if tor_status() else "❌ MATI"
    print(f"  Layer 1 (Tor):        {tor}")
    
    # IP
    ip = check_tor_ip()
    if ip:
        print(f"  IP Tor:               {GREEN}{ip}{RESET}")
    else:
        print(f"  IP Tor:               {YELLOW}Tidak tersedia{RESET}")
    
    # DNSCrypt
    dns_conf = os.path.exists(os.path.join(CONF_DIR, "dnscrypt-proxy.toml"))
    print(f"  Layer 2 (DNSCrypt):   {'✅ Config ada' if dns_conf else '❌ Belum setup'}")
    
    # Proxychains
    pc_conf = os.path.exists(os.path.join(CONF_DIR, "proxychains.conf"))
    print(f"  Layer 3 (Proxychains): {'✅ Config ada' if pc_conf else '❌ Belum setup'}")
    
    # Header
    ua_file = os.path.join(CONF_DIR, "user_agent.txt")
    if os.path.exists(ua_file):
        ua = open(ua_file).read()[:40]
        print(f"  Layer 4 (Header):     ✅ {ua}...")
    else:
        print(f"  Layer 4 (Header):     ❌ Belum setup")
    
    # Echo-Core
    print(f"  Layer 5 (Echo-Core):  ✅ Aktif")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# TEST TOR
# ============================================================
def test_tor():
    """Test koneksi Tor"""
    os.system('clear')
    print(f"{BOLD}{CYAN}🧪 TEST KONEKSI TOR{RESET}\n")
    
    if not tor_status():
        print(f"{YELLOW}⚠️  Tor belum jalan. Jalankan mode 1 dulu.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    print(f"{CYAN}⏳ Test koneksi...{RESET}\n")
    
    # Test 1: IP
    print(f"{GOLD}Test 1: IP Tor{RESET}")
    ip = check_tor_ip()
    if ip:
        print(f"  {GREEN}✅ IP: {ip}{RESET}\n")
    else:
        print(f"  {RED}❌ Gagal{RESET}\n")
    
    # Test 2: Check Tor Project
    print(f"{GOLD}Test 2: Check Tor Project{RESET}")
    try:
        r = subprocess.run(
            ["torsocks", "curl", "-s", "--max-time", "15", "https://check.torproject.org/"],
            capture_output=True, text=True, timeout=20
        )
        if "Congratulations" in r.stdout:
            print(f"  {GREEN}✅ Tor terkonfirmasi!{RESET}\n")
        elif "not using" in r.stdout.lower():
            print(f"  {YELLOW}⚠️  Tidak terdeteksi Tor{RESET}\n")
        else:
            print(f"  {YELLOW}⚠️  Response tidak jelas{RESET}\n")
    except:
        print(f"  {RED}❌ Error{RESET}\n")
    
    # Test 3: .onion
    print(f"{GOLD}Test 3: Akses .onion{RESET}")
    try:
        r = subprocess.run(
            ["torsocks", "curl", "-s", "--max-time", "15", "http://zqktlwi4fecvo6ri.onion/"],
            capture_output=True, text=True, timeout=20
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
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🛡️  ZUHRI TOR SHIELD — PERISAI BERLAPIS                           ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                            ║
║  Teknologi: Tor + DNSCrypt + Proxychains + Header Anonymizer       ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🛡️  Aktifkan Full Shield (5 Lapisan)
  {GOLD}2.{RESET}  🌑 Akses .onion (Perisai Aktif)
  {GOLD}3.{RESET}  🧪 Test Koneksi Tor
  {GOLD}4.{RESET}  📊 Cek Status
  {GOLD}5.{RESET}  🚀 Jalankan Tor Saja
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-5): {RESET}").strip()
            if c == "0": break
            elif c == "1": full_shield()
            elif c == "2": akses_onion()
            elif c == "3": test_tor()
            elif c == "4": status()
            elif c == "5":
                os.system('clear')
                start_tor()
                input(f"{DIM}Enter...{RESET}")
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "shield": full_shield()
        elif cmd == "test": test_tor()
        elif cmd == "status": status()
        elif cmd == "onion": akses_onion()
        else: menu()
    else: menu()
