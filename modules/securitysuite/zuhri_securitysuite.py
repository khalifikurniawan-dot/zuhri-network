#!/usr/bin/env python3
"""
ZUHRI SECURITY SUITE — PUSAT KEAMANAN TERPADU
Botnet Hunter • Tor Shield • Echo-Core • Enkripsi
"""

import os, sys, json, subprocess, time
from datetime import datetime

HOME = os.path.expanduser("~")
SS_DIR = os.path.join(HOME, "zuhri_os", "securitysuite")
DATA_DIR = os.path.join(SS_DIR, "data")
LOG_DIR = os.path.join(SS_DIR, "logs")
for d in [DATA_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

def clear(): os.system('clear')
def pause():
    input(f"\n{DIM}━━━ Tekan Enter untuk lanjut ━━━{RESET}\n")

# ============================================================
# 1. BOTNET HUNTER
# ============================================================
def botnet_hunter():
    clear()
    print(f"""
{BOLD}{RED}╔══════════════════════════════════════════════════════════════════════════╗
║  🛡️  ZUHRI BOTNET HUNTER — DETEKSI ANCAMAN JARINGAN                     ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 MENU:{RESET}
  {GOLD}1.{RESET} 🔍 Full Scan (Deteksi Lengkap)
  {GOLD}2.{RESET} ⚙️  Cek Proses Mencurigakan
  {GOLD}3.{RESET} 🌐 Cek Port Terbuka
  {GOLD}4.{RESET} 📡 Cek Koneksi Aktif
  {GOLD}5.{RESET} 📂 Cek File Mencurigakan
  {GOLD}6.{RESET} 🔍 Cek DNS
  {GOLD}7.{RESET} 📊 Log Scan Sebelumnya
  {GOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "0": return
        elif c == "1":
            print(f"\n{CYAN}🔍 Scanning...{RESET}\n")
            subprocess.run(["python", os.path.expanduser("~/zuhri_os/botnet/zuhri_botnet.py"), "scan"])
            pause()
        else:
            subprocess.run(["python", os.path.expanduser("~/zuhri_os/botnet/zuhri_botnet.py")])
    except: pause()

# ============================================================
# 2. TOR SHIELD
# ============================================================
def tor_shield():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  🛡️  ZUHRI TOR SHIELD — PERISAI BERLAPIS                                ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 MENU:{RESET}
  {GOLD}1.{RESET} 🛡️  Aktifkan Full Shield (5 Lapisan)
  {GOLD}2.{RESET} 🌑 Akses .onion (Perisai Aktif)
  {GOLD}3.{RESET} 🧪 Test Koneksi Tor
  {GOLD}4.{RESET} 📊 Cek Status
  {GOLD}5.{RESET} 🚀 Jalankan Tor Saja
  {GOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "0": return
        subprocess.run(["python", os.path.expanduser("~/zuhri_os/torshield/zuhri_torshield.py"), c] if c in ["1","2","3","4","5"] else ["python", os.path.expanduser("~/zuhri_os/torshield/zuhri_torshield.py")])
        pause()
    except: pause()

# ============================================================
# 3. ECHO-CORE
# ============================================================
def echo_core():
    clear()
    print(f"""
{BOLD}{BLUE}╔══════════════════════════════════════════════════════════════════════════╗
║  🛡️  ZUHRI ECHO-CORE — POST-QUANTUM SHIELD                              ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 MENU:{RESET}
  {GOLD}1.{RESET} 🛡️  Echo Encryption (Multi-layer)
  {GOLD}2.{RESET} 🔐 Post-Quantum Crypto (ML-KEM & ML-DSA)
  {GOLD}3.{RESET} 📊 Quantum Threat Scanner
  {GOLD}4.{RESET} ℹ️  Info Echo-Core
  {GOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "0": return
        subprocess.run(["python", os.path.expanduser("~/zuhri_os/echocore/zuhri_echocore.py")])
        pause()
    except: pause()

# ============================================================
# 4. ENKRIPSI
# ============================================================
def enkripsi():
    clear()
    print(f"""
{BOLD}{GREEN}╔══════════════════════════════════════════════════════════════════════════╗
║  🔐 ZUHRI ENKRIPSI — KEAMANAN DATA                                     ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 MENU:{RESET}
  {GOLD}1.{RESET} 🔐 Enkripsi Teks
  {GOLD}2.{RESET} 🔓 Dekripsi Teks
  {GOLD}3.{RESET} 📁 Enkripsi File
  {GOLD}4.{RESET} 📂 Dekripsi File
  {GOLD}5.{RESET} 📦 Enkripsi Folder (Batch)
  {GOLD}6.{RESET} 🔍 Hash Checker
  {GOLD}7.{RESET} 🖋️  Digital Signature
  {GOLD}8.{RESET} 🔑 Password Manager
  {GOLD}9.{RESET} 🖼️  Steganografi
  {GOLD}10.{RESET} 🗝️  Key Manager
  {GOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "0": return
        subprocess.run(["python", os.path.expanduser("~/zuhri_os/enkripsi/zuhri_enkripsi.py")])
        pause()
    except: pause()

# ============================================================
# MENU UTAMA
# ============================================================
def menu():
    while True:
        clear()
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  🛡️  ZUHRI SECURITY SUITE — PUSAT KEAMANAN TERPADU                     ║
║  ──────────────────────────────────────────────────────────────────────  ║
║  Botnet Hunter • Tor Shield • Echo-Core • Enkripsi                     ║
║  Waktu: {GOLD}{datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}{RESET}
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 KELOMPOK KEAMANAN:{RESET}

  {GOLD}1.{RESET}  🛡️  {BOLD}ZUHRI BOTNET HUNTER{RESET}      → Deteksi ancaman jaringan
  {GOLD}2.{RESET}  🛡️  {BOLD}ZUHRI TOR SHIELD{RESET}         → Perisai Tor berlapis
  {GOLD}3.{RESET}  🛡️  {BOLD}ZUHRI ECHO-CORE{RESET}          → Perisai Kuantum (PQC)
  {GOLD}4.{RESET}  🔐 {BOLD}ZUHRI ENKRIPSI{RESET}           → Keamanan data lengkap

  {GOLD}5.{RESET}  📊 {BOLD}STATUS SEMUA LAYER{RESET}       → Cek semua keamanan
  {GOLD}6.{RESET}  ℹ️  {BOLD}INFO SECURITY SUITE{RESET}      → Penjelasan

  {GOLD}0.{RESET}  🚪 Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-6): {RESET}").strip()
            if c == "0": break
            elif c == "1": botnet_hunter()
            elif c == "2": tor_shield()
            elif c == "3": echo_core()
            elif c == "4": enkripsi()
            elif c == "5": status_semua()
            elif c == "6": info()
        except KeyboardInterrupt:
            break

def status_semua():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  📊 STATUS SEMUA LAYER KEAMANAN                                         ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    # Cek Tor
    tor_ok = subprocess.run(["pgrep", "-x", "tor"], capture_output=True).returncode == 0
    print(f"  🛡️  Botnet Hunter  : {GREEN}✅ TERSEDIA{RESET}")
    print(f"  🛡️  Tor Shield     : {GREEN + '✅ AKTIF' + RESET if tor_ok else RED + '❌ TOR MATI' + RESET}")
    print(f"  🛡️  Echo-Core      : {GREEN}✅ TERSEDIA{RESET}")
    print(f"  🔐 Enkripsi        : {GREEN}✅ TERSEDIA{RESET}")
    print()
    pause()

def info():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  ℹ️  INFO ZUHRI SECURITY SUITE                                           ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}🎯 4 KELOMPOK KEAMANAN:{RESET}

  {GOLD}1.{RESET} 🛡️  {BOLD}Botnet Hunter{RESET}
     Deteksi proses, port, koneksi mencurigakan.

  {GOLD}2.{RESET} 🛡️  {BOLD}Tor Shield{RESET}
     Perisai berlapis untuk deep/dark web.

  {GOLD}3.{RESET} 🛡️  {BOLD}Echo-Core{RESET}
     Post-Quantum Cryptography (PQC).

  {GOLD}4.{RESET} 🔐 {BOLD}Enkripsi{RESET}
     Enkripsi file, teks, steganografi, password manager.

{BOLD}🎯 FILOSOFI:{RESET}
  {CYAN}"Keamanan berlapis — melindungi data Anda${RESET}
  {CYAN}dari ancaman jaringan hingga kuantum."{RESET}
""")
    pause()

if __name__ == "__main__":
    menu()
