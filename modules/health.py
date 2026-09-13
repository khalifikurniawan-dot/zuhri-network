#!/data/data/com.termux/files/usr/bin/python
"""
SYSTEM HEALTH — ZUHRI NETWORK
Monitor RAM, Storage, CPU, dan Status Sistem
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os
import sys
import subprocess
from datetime import datetime

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

def get_ram():
    try:
        mem = subprocess.getoutput("free -m").split("\n")
        total = int(mem[1].split()[1])
        used = int(mem[1].split()[2])
        free = int(mem[1].split()[3])
        percent = int(used / total * 100)
        return {'total': total, 'used': used, 'free': free, 'percent': percent}
    except:
        return {'total': 0, 'used': 0, 'free': 0, 'percent': 0}

def get_storage():
    try:
        storage = subprocess.getoutput("df -h /data").split("\n")
        total = storage[1].split()[1]
        used = storage[1].split()[2]
        avail = storage[1].split()[3]
        percent = storage[1].split()[4]
        return {'total': total, 'used': used, 'avail': avail, 'percent': percent}
    except:
        return {'total': 'N/A', 'used': 'N/A', 'avail': 'N/A', 'percent': '0%'}

def get_cpu():
    try:
        cpu = subprocess.getoutput("top -bn1 | head -5 | grep '%Cpu'")
        if cpu:
            parts = cpu.split()
            return parts[1] if len(parts) > 1 else "N/A"
        return "N/A"
    except:
        return "N/A"

def get_ollama():
    try:
        result = subprocess.run(["curl", "-s", "http://localhost:11434/api/tags"], 
                               capture_output=True, timeout=2)
        return "✅ RUNNING" if result.returncode == 0 else "❌ STOPPED"
    except:
        return "❌ STOPPED"

def get_tor():
    # Cek apakah Tor berjalan
    try:
        subprocess.run(["pgrep", "-x", "tor"], check=True, capture_output=True)
    except:
        # Jika tidak, jalankan Tor
        subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import time
        time.sleep(8)
    
    # Ambil IP Tor
    try:
        result = subprocess.run(["torsocks", "curl", "-s", "ifconfig.me"], 
                               capture_output=True, timeout=10)
        ip = result.stdout.decode().strip()
        if ip and "html" not in ip.lower():
            return ip
        return "❌ OFFLINE"
    except:
        return "❌ OFFLINE"

def get_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        if len(lines) > 1:
            return ", ".join([line.split()[0] for line in lines[1:] if line.strip()])
        return "none"
    except:
        return "unknown"

def bar(percent, width=20):
    """Buat bar visual"""
    filled = int(width * percent / 100)
    empty = width - filled
    if percent < 50:
        color = GREEN
    elif percent < 80:
        color = YELLOW
    else:
        color = RED
    return f"{color}{'█' * filled}{'░' * empty}{RESET}"

def main():
    os.system('clear')
    
    ram = get_ram()
    storage = get_storage()
    cpu = get_cpu()
    ollama = get_ollama()
    tor = get_tor()
    models = get_models()
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  💻 SYSTEM HEALTH — ZUHRI NETWORK                              ║
║  ──────────────────────────────────────────────────────────────  ║
║  PROTOKOL : {GOLD}K-8.0 — FLUID-CORE{RESET}
║  GEN      : {GOLD}ZUH-8-9-0-K-8.0{RESET}
║  WAKTU    : {GOLD}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}{CYAN}┌─────────────────────────────────────────────────────────────┐
│  📊 RAM                                                    │
├─────────────────────────────────────────────────────────────┤{RESET}
│  Total : {ram['total']} MB
│  Used  : {ram['used']} MB ({ram['percent']}%)
│  Free  : {ram['free']} MB
│  {bar(ram['percent'])}
{BOLD}{CYAN}└─────────────────────────────────────────────────────────────┘{RESET}

{BOLD}{CYAN}┌─────────────────────────────────────────────────────────────┐
│  💾 STORAGE                                                │
├─────────────────────────────────────────────────────────────┤{RESET}
│  Total : {storage['total']}
│  Used  : {storage['used']}
│  Avail : {storage['avail']}
│  Usage : {storage['percent']}
{BOLD}{CYAN}└─────────────────────────────────────────────────────────────┘{RESET}

{BOLD}{CYAN}┌─────────────────────────────────────────────────────────────┐
│  ⚙️  STATUS SISTEM                                         │
├─────────────────────────────────────────────────────────────┤{RESET}
│  CPU     : {cpu}
│  OLLAMA  : {ollama}
│  TOR     : {tor}
│  MODEL   : {models}
{BOLD}{CYAN}└─────────────────────────────────────────────────────────────┘{RESET}
""")

if __name__ == "__main__":
    main()
