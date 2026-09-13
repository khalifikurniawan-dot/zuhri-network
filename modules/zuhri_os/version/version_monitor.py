#!/data/data/com.termux/files/usr/bin/python
"""
VERSION MONITOR — ZUHRI OS
Cek Versi Sistem dan Update Tersedia
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os
import sys
import json
import subprocess
from datetime import datetime

HOME = os.path.expanduser("~")
CONFIG_FILE = os.path.join(HOME, ".zuhri_os_version.json")

# ===== KONFIGURASI =====
CURRENT_VERSION = "ZUHRI OS v1.0"
LATEST_VERSION = "ZUHRI OS v1.0"  # Update manual saat ada versi baru

# ===== KOMPONEN ZUHRI OS =====
COMPONENTS = {
    "Zuhri OS": {"file": "~/zuhri_os/zuhri_os.py", "version": "1.0"},
    "Zuhri Network": {"file": "~/zuhri.py", "version": "1.0"},
    "Key Kosmik": {"file": "~/kosmik/key.sh", "version": "2.0"},
    "Dark-Web Gateway": {"file": "/data/data/com.termux/files/usr/bin/dark-web", "version": "2.0"},
    "P2P-Mesh": {"file": "~/kosmik/p2p/mesh_node.py", "version": "1.0"},
    "Mesh-Scan": {"file": "~/kosmik/p2p/mesh_discovery.py", "version": "1.0"},
    "Edge-Vision": {"file": "~/kosmik/vision/edge_vision.py", "version": "1.0"},
    "Predictive-Shell": {"file": "~/kosmik/predictive_shell.py", "version": "1.0"},
    "Voice-Commander": {"file": "~/kosmik/voice/voice_commander.py", "version": "1.0"},
    "SOS-Beacon": {"file": "~/kosmik/sos_beacon.py", "version": "1.0"},
    "System Health": {"file": "~/health.py", "version": "1.0"},
    "FluidUpdater": {"file": "~/updater.py", "version": "1.0"},
    "Backup Manager": {"file": "~/zuhri_os/backup/backup_manager.py", "version": "1.0"}
}

# ===== WARNA =====
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
GOLD = "\033[93m"
MAGENTA = "\033[95m"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"installed": CURRENT_VERSION, "last_check": None}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def check_components():
    """Cek semua komponen ZUHRI OS"""
    installed = 0
    missing = 0
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📦 KOMPONEN ZUHRI OS                                          ║
║  ──────────────────────────────────────────────────────────────  ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    for name, data in COMPONENTS.items():
        path = os.path.expanduser(data['file'])
        version = data['version']
        
        if os.path.exists(path):
            print(f"  {GREEN}✅{RESET} {name:22} {DIM}v{version}{RESET}")
            installed += 1
        else:
            print(f"  {RED}❌{RESET} {name:22} {DIM}missing{RESET}")
            missing += 1
    
    print(f"""
{DIM}─────────────────────────────────────────────────────────────{RESET}
  {GREEN}Installed:{RESET} {installed}  |  {RED}Missing:{RESET} {missing}
{DIM}─────────────────────────────────────────────────────────────{RESET}
""")
    return installed, missing

def check_update():
    """Cek update tersedia"""
    config = load_config()
    current = config.get('installed', CURRENT_VERSION)
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🔍 CEK UPDATE — ZUHRI OS                                      ║
║  ──────────────────────────────────────────────────────────────  ║
║  Current version : {GOLD}{current}{RESET}
║  Latest version  : {GOLD}{LATEST_VERSION}{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    if LATEST_VERSION > current:
        print(f"{GREEN}✅ Update available!{RESET}")
        print(f"{CYAN}💡 Jalankan: update update{RESET}\n")
        return True
    else:
        print(f"{GREEN}✅ Sistem sudah versi terbaru!{RESET}\n")
        return False

def show_version():
    """Tampilkan versi lengkap"""
    config = load_config()
    installed, missing = check_components()
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📦 VERSION MONITOR — ZUHRI OS                                 ║
║  ──────────────────────────────────────────────────────────────  ║
║  OS Version   : {GOLD}{config.get('installed', CURRENT_VERSION)}{RESET}
║  Latest       : {GOLD}{LATEST_VERSION}{RESET}
║  Last Check   : {GOLD}{config.get('last_check', 'never')}{RESET}
║  Waktu        : {GOLD}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}
║  Komponen     : {GREEN}{installed}{RESET} installed / {RED}{missing}{RESET} missing
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    # Update config
    config['last_check'] = datetime.now().isoformat()
    save_config(config)

def show_help():
    print(f"""
{BOLD}{CYAN}📦 VERSION MONITOR — BANTUAN{RESET}
{'─' * 50}
  {BOLD}version{RESET}       → Lihat versi sistem & komponen
  {BOLD}version check{RESET} → Cek update tersedia
  {BOLD}version help{RESET}  → Tampilkan bantuan
{'─' * 50}
""")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "check":
            check_update()
        elif cmd == "help":
            show_help()
        else:
            show_version()
    else:
        show_version()
