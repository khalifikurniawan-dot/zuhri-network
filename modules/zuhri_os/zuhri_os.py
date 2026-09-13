#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI OS — SISTEM OPERASI MINI (FULL)
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
Terintegrasi ZUHRI ID
"""

import os
import sys
import subprocess
import time
import random
from datetime import datetime

HOME = os.path.expanduser("~")
VERSION = "ZUHRI OS v2.0"

# ===== ZUHRI AUTH =====
sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import get_status, log_verified, load_identity
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

# ===== WARNA =====
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
GOLD = "\033[93m"

SYMBOLS = ["◈", "◇", "◆", "◉", "◎", "●", "○", "✦", "✧", "★", "☆"]

# ============================================================
# UTIL
# ============================================================
def gradient(text):
    colors = [CYAN, MAGENTA, GOLD]
    result = ""
    for i, char in enumerate(text):
        result += f"{colors[i % 3]}{char}{RESET}"
    return result

def random_symbol():
    return random.choice(SYMBOLS)

def clear():
    os.system('clear')

# ============================================================
# BOOT SEQUENCE
# ============================================================
def boot_sequence():
    clear()
    boot_lines = [
        "  [BOOT] ZUHRI OS v2.0 — Memulai sistem...",
        "  [BOOT] Memuat protokol K-8.0...",
        "  [BOOT] Sinkronisasi Fluid-Core...",
        "  [BOOT] Mengaktifkan Echo-Synapse...",
        "  [BOOT] Resonansi 0-8-9 — SEIMBANG",
        "  [BOOT] Gen Zuhri: ZUH-8-9-0-K-8.0",
    ]
    
    # Cek Zuhri ID
    if ZUHRI_ID_OK:
        s = get_status()
        if s['active']:
            boot_lines.append(f"  [BOOT] Zuhri ID: {s['zuhri_id'][:24]}...")
            boot_lines.append(f"  [BOOT] Operator: {s['name']}")
        else:
            boot_lines.append("  [BOOT] ⚠️  Zuhri ID belum dibuat")
    else:
        boot_lines.append("  [BOOT] ⚠️  Modul Zuhri Auth tidak tersedia")
    
    boot_lines.append("  [BOOT] Status: ✅ ONLINE")
    
    for line in boot_lines:
        print(f"{CYAN}{line}{RESET}")
        time.sleep(0.15)
    print()
    time.sleep(0.2)

# ============================================================
# STATUS
# ============================================================
def get_status_all():
    status = {}
    
    # Cek Tor
    try:
        result = subprocess.run(
            ["torsocks", "curl", "-s", "--max-time", "10", "ifconfig.me"],
            capture_output=True, timeout=15
        )
        ip = result.stdout.decode().strip()
        if ip and not ip.startswith("<") and "html" not in ip.lower() and len(ip) < 50:
            status['tor'] = ip
        else:
            status['tor'] = "offline"
    except:
        status['tor'] = "offline"
    
    # Cek Ollama
    try:
        result = subprocess.run(["curl", "-s", "http://localhost:11434/api/tags"],
                               capture_output=True, timeout=2)
        status['ollama'] = "online" if "models" in result.stdout.decode() else "offline"
    except:
        status['ollama'] = "offline"
    
    # Cek scripts
    status['scripts'] = {
        'mesh': os.path.exists(f"{HOME}/kosmik/p2p/mesh_node.py"),
        'vision': os.path.exists(f"{HOME}/kosmik/vision/edge_vision.py"),
        'dark-web': os.path.exists("/data/data/com.termux/files/usr/bin/dark-web"),
        'predictive': os.path.exists(f"{HOME}/kosmik/predictive_shell.py"),
        'voice': os.path.exists(f"{HOME}/kosmik/voice/voice_commander.py"),
        'sos': os.path.exists(f"{HOME}/kosmik/sos_beacon.py"),
        'wallet': os.path.exists(f"{HOME}/zuhri_os/wallet/wallet.py"),
    }
    return status

# ============================================================
# PRINT HEADER
# ============================================================
def print_header():
    clear()
    
    # Zuhri ID
    id_display = "N/A"
    name_display = "ANONYMOUS"
    if ZUHRI_ID_OK:
        s = get_status()
        if s['active']:
            id_display = s['zuhri_id'][:32] + "..."
            name_display = s['name']
        else:
            id_display = "❌ Belum dibuat"
            name_display = "❌ Belum dibuat"
    
    print(f"\n{DIM}{random_symbol()} {random_symbol()} {random_symbol()} {RESET}")
    print(f"{gradient('  ╔══════════════════════════════════════════════════════════════════╗  ')}")
    print(f"{gradient('  ║')}  {BOLD}{GOLD}🌌 ZUHRI OS v2.0 — SISTEM OPERASI MINI{RESET}  {gradient('║')}")
    print(f"{gradient('  ╠══════════════════════════════════════════════════════════════════╣  ')}")
    print(f"{gradient('  ║')}  {CYAN}OPERATOR{RESET} : {GOLD}{name_display}{RESET}                                       {gradient('║')}")
    print(f"{gradient('  ║')}  {CYAN}ZUHRI ID{RESET} : {GOLD}{id_display}{RESET}                {gradient('║')}")
    print(f"{gradient('  ║')}  {CYAN}PROTOKOL{RESET} : {GOLD}K-8.0 — FLUID-CORE{RESET}                            {gradient('║')}")
    print(f"{gradient('  ║')}  {CYAN}RESONANSI{RESET}: {GOLD}0-8-9 — SEIMBANG{RESET}                              {gradient('║')}")
    print(f"{gradient('  ║')}  {CYAN}VERSION{RESET}  : {GOLD}{VERSION}{RESET}                                           {gradient('║')}")
    print(f"{gradient('  ╚══════════════════════════════════════════════════════════════════╝  ')}")
    print(f"\n{DIM}{random_symbol()} {random_symbol()} {random_symbol()} {RESET}\n")

# ============================================================
# PRINT STATUS
# ============================================================
def print_status():
    status = get_status_all()
    
    if status['tor'] != "offline":
        tor_status = f"{GREEN}✅ {status['tor']}{RESET}"
    else:
        tor_status = f"{RED}❌ OFFLINE{RESET}"
    
    ollama_status = f"{GREEN}✅ ONLINE{RESET}" if status['ollama'] == "online" else f"{RED}❌ OFFLINE{RESET}"
    
    def sc(key):
        return f"{GREEN}✅{RESET}" if status['scripts'].get(key, False) else f"{RED}❌{RESET}"
    
    print(f"""{BOLD}{CYAN}  ┌─────────────────────────────────────────────────────────────┐
  │  📊 STATUS SISTEM                                            │
  ├─────────────────────────────────────────────────────────────┤{RESET}
  │  {CYAN}TOR      {RESET}: {tor_status}
  │  {CYAN}OLLAMA   {RESET}: {ollama_status}
  │  {DIM}───────────────────────────────────────────────────────────{RESET}
  │  {CYAN}MESH     {RESET}: {sc('mesh')}     {CYAN}VISION   {RESET}: {sc('vision')}
  │  {CYAN}DARK-WEB {RESET}: {sc('dark-web')}     {CYAN}PREDICT  {RESET}: {sc('predictive')}
  │  {CYAN}VOICE    {RESET}: {sc('voice')}     {CYAN}SOS      {RESET}: {sc('sos')}
  │  {CYAN}WALLET   {RESET}: {sc('wallet')}
{BOLD}{CYAN}  └─────────────────────────────────────────────────────────────┘{RESET}
""")

# ============================================================
# PRINT MENU
# ============================================================
def print_menu():
    print(f"""
{gradient('  ┌─────────────────────────────────────────────────────────────┐  ')}
{gradient('  │')}  {BOLD}📡 APLIKASI ZUHRI OS{RESET}                                     {gradient('│')}
{gradient('  ├─────────────────────────────────────────────────────────────┤  ')}
{gradient('  │')}  {CYAN}1.{RESET}  Local LLM           → {MAGENTA}AI pribadi offline{RESET}                 {gradient('│')}
{gradient('  │')}  {CYAN}2.{RESET}  P2P-Mesh + Zuhri ID → {MAGENTA}Jaringan terverifikasi{RESET}             {gradient('│')}
{gradient('  │')}  {CYAN}3.{RESET}  Edge-Vision         → {MAGENTA}Deteksi objek offline{RESET}              {gradient('│')}
{gradient('  │')}  {CYAN}4.{RESET}  Dark-Web Gateway    → {MAGENTA}Akses .onion anonim{RESET}                {gradient('│')}
{gradient('  │')}  {CYAN}5.{RESET}  Predictive-Shell    → {GREEN}Terminal prediktif ✅{RESET}                 {gradient('│')}
{gradient('  │')}  {CYAN}6.{RESET}  Voice-Commander     → {GREEN}Kontrol suara ✅{RESET}                      {gradient('│')}
{gradient('  │')}  {CYAN}7.{RESET}  SOS-Beacon          → {GREEN}Sinyal darurat ✅{RESET}                     {gradient('│')}
{gradient('  │')}  {CYAN}8.{RESET}  Crypto-Wallet       → {GREEN}Dompet offline ✅{RESET}                    {gradient('│')}
{gradient('  │')}  {CYAN}9.{RESET}  Zuhri ID            → {GOLD}Identitas digital{RESET}                  {gradient('│')}
{gradient('  │')}  {CYAN}10.{RESET} Zuhri Crypto        → {GOLD}Enkripsi & Vault{RESET}                   {gradient('│')}
{gradient('  │')}  {CYAN}11.{RESET} Terminal Biasa      → {MAGENTA}Masuk ke shell Termux{RESET}                {gradient('│')}
{gradient('  │')}  {CYAN}12.{RESET} System Info         → {MAGENTA}Info sistem{RESET}                         {gradient('│')}
{gradient('  │')}  {CYAN}0.{RESET}  Matikan Zuhri OS    → {MAGENTA}Keluar{RESET}                              {gradient('│')}
{gradient('  └─────────────────────────────────────────────────────────────┘  ')}
""")

# ============================================================
# SYSTEM INFO
# ============================================================
def system_info():
    clear()
    import platform
    
    identity = load_identity() if ZUHRI_ID_OK else None
    
    print(f"""
{BOLD}{CYAN}  ╔══════════════════════════════════════════════════════════════════╗
  ║  💻 SYSTEM INFORMATION — ZUHRI OS v2.0                          ║
  ╠══════════════════════════════════════════════════════════════════╣{RESET}
{CYAN}  ║{RESET}  {BOLD}OS          {RESET}: ZUHRI OS v2.0
{CYAN}  ║{RESET}  {BOLD}Kernel      {RESET}: {platform.platform()}
{CYAN}  ║{RESET}  {BOLD}Python      {RESET}: {platform.python_version()}
{CYAN}  ║{RESET}  {BOLD}Arsitektur  {RESET}: {platform.machine()}
{CYAN}  ║{RESET}  {BOLD}Waktu       {RESET}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{BOLD}{CYAN}  ╠══════════════════════════════════════════════════════════════════╣{RESET}""")
    
    if identity:
        print(f"""{CYAN}  ║{RESET}  {BOLD}ZUHRI ID    {RESET}: {identity['zuhri_id']}
{CYAN}  ║{RESET}  {BOLD}Nama        {RESET}: {identity['name']}
{CYAN}  ║{RESET}  {BOLD}Role        {RESET}: {identity.get('role', 'Operator')}
{CYAN}  ║{RESET}  {BOLD}Protocol    {RESET}: {identity['protocol']}
{CYAN}  ║{RESET}  {BOLD}Gen         {RESET}: {identity['gen']}
{CYAN}  ║{RESET}  {BOLD}Dibuat      {RESET}: {identity['created'][:19]}""")
    else:
        print(f"{CYAN}  ║{RESET}  {RED}⚠️  Zuhri ID belum dibuat{RESET}")
    
    print(f"{BOLD}{CYAN}  ╚══════════════════════════════════════════════════════════════════╝{RESET}\n")
    input(f"{DIM}Tekan Enter untuk kembali...{RESET}")

# ============================================================
# RUN CHOICE
# ============================================================
def run_choice(choice):
    if choice == 0:
        print(f"\n{GOLD}🛑 Mematikan Zuhri OS...{RESET}")
        if ZUHRI_ID_OK:
            log_verified("ZUHRI_OS_SHUTDOWN", "OK")
        time.sleep(1)
        print(f"{GOLD}👋 Sampai jumpa, KURNIAWAN!{RESET}\n")
        return False
    
    if choice == 11:
        print(f"\n{CYAN}🚀 Masuk ke terminal Termux...{RESET}\n")
        os.system("bash")
        input(f"\n{DIM}Tekan Enter untuk kembali...{RESET}")
        return True
    
    if choice == 12:
        system_info()
        return True
    
    paths = {
        1: ("Local LLM", 'ollama run tinyllama "Jawab dalam Bahasa Indonesia. "'),
        2: ("P2P-Mesh + Zuhri ID", f"python {HOME}/kosmik/p2p/mesh_node.py"),
        3: ("Edge-Vision", f"python {HOME}/kosmik/vision/edge_vision.py"),
        4: ("Dark-Web Gateway", "dark-web"),
        5: ("Predictive-Shell", f"python {HOME}/kosmik/predictive_shell.py"),
        6: ("Voice-Commander", f"python {HOME}/kosmik/voice/voice_commander.py"),
        7: ("SOS-Beacon", f"python {HOME}/kosmik/sos_beacon.py"),
        8: ("Crypto-Wallet", f"python {HOME}/zuhri_os/wallet/wallet.py"),
        9: ("Zuhri ID", f"python {HOME}/zuhri_os/id/zuhri_id.py"),
        10: ("Zuhri Crypto", f"python {HOME}/zuhri_os/crypto/zuhri_crypto.py"),
    }
    
    if choice in paths:
        name, cmd = paths[choice]
        print(f"\n{CYAN}🚀 Menjalankan: {GOLD}{name}{RESET}\n")
        if ZUHRI_ID_OK:
            log_verified(f"ZUHRI_OS_RUN: {name}")
        os.system(cmd)
        input(f"\n{DIM}Tekan Enter untuk kembali...{RESET}")
        return True
    
    print(f"\n{RED}❌ Pilihan tidak valid!{RESET}")
    time.sleep(1)
    return True

# ============================================================
# MAIN
# ============================================================
def main():
    boot_sequence()
    
    if ZUHRI_ID_OK:
        log_verified("ZUHRI_OS_BOOT", "OK")
    
    while True:
        print_header()
        print_status()
        print_menu()
        
        try:
            choice = input(f"\n{GOLD}📡 Pilih aplikasi (0-12){RESET}: ").strip()
            if choice == "":
                continue
            try:
                choice_num = int(choice)
                if not run_choice(choice_num):
                    break
            except ValueError:
                print(f"{RED}❌ Masukkan angka 0-12!{RESET}")
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{GOLD}👋 Sampai jumpa!{RESET}")
            if ZUHRI_ID_OK:
                log_verified("ZUHRI_OS_INTERRUPT", "OK")
            break

if __name__ == "__main__":
    main()
