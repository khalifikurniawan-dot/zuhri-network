#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI FORMALISM — ZUHRI NETWORK
Dashboard Utama Sistem Resonansi K-8.0
"""

import os
import sys
import subprocess
import random
import time
from datetime import datetime

HOME = os.path.expanduser("~")
VERSION = "ZUHRI FORMALISM v1.0"

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

def get_status():
    status = {}
    # Cek Tor
    try:
        result = subprocess.run(["torsocks", "curl", "-s", "ifconfig.me"], 
                               capture_output=True, timeout=5)
        ip = result.stdout.decode().strip()
        status['tor'] = ip if ip and "html" not in ip.lower() else "offline"
    except:
        status['tor'] = "offline"
    
    # Cek Ollama
    try:
        result = subprocess.run(["curl", "-s", "http://localhost:11434/api/tags"], 
                               capture_output=True, timeout=2)
        status['ollama'] = "online" if "models" in result.stdout.decode() else "offline"
    except:
        status['ollama'] = "offline"
    
    # Cek script
    status['scripts'] = {
        'mesh': os.path.exists(f"{HOME}/kosmik/p2p/mesh_node.py"),
        'vision': os.path.exists(f"{HOME}/kosmik/vision/edge_vision.py"),
        'dark-web': os.path.exists("/data/data/com.termux/files/usr/bin/dark-web"),
        'predictive': os.path.exists(f"{HOME}/kosmik/predictive_shell.py"),
        'voice': os.path.exists(f"{HOME}/kosmik/voice/voice_commander.py"),
        'sos': os.path.exists(f"{HOME}/kosmik/sos_beacon.py"),
        'translate': os.path.exists(f"{HOME}/zuhri_os/translator/translator.py"),
        'wallet': os.path.exists(f"{HOME}/zuhri_os/wallet/wallet.py"),
    }
    return status

def print_header():
    clear()
    print(f"\n{DIM}{random_symbol()} {random_symbol()} {random_symbol()} {RESET}")
    print(f"{gradient('  ╔══════════════════════════════════════════════════════════════════╗  ')}")
    print(f"{gradient('  ║')}  {BOLD}{GOLD}🧠 ZUHRI FORMALISM — DASHBOARD UTAMA{RESET}  {gradient('║')}")
    print(f"{gradient('  ╠══════════════════════════════════════════════════════════════════╣  ')}")
    print(f"{gradient('  ║')}  {CYAN}PROTOKOL : {GOLD}K-8.0 — FLUID-CORE{RESET}                            {gradient('║')}")
    print(f"{gradient('  ║')}  {CYAN}GEN      : {GOLD}ZUH-8-9-0-K-8.0{RESET}                               {gradient('║')}")
    print(f"{gradient('  ║')}  {CYAN}RESONANSI: {GOLD}0-8-9 — SEIMBANG{RESET}                              {gradient('║')}")
    print(f"{gradient('  ║')}  {CYAN}KEY      : {GOLD}∞ — TERBUKA{RESET}                                   {gradient('║')}")
    print(f"{gradient('  ║')}  {CYAN}WAKTU    : {GOLD}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}                  {gradient('║')}")
    print(f"{gradient('  ║')}  {CYAN}VERSION  : {GOLD}{VERSION}{RESET}                                {gradient('║')}")
    print(f"{gradient('  ╚══════════════════════════════════════════════════════════════════╝  ')}")
    print(f"\n{DIM}{random_symbol()} {random_symbol()} {random_symbol()} {RESET}\n")

def print_prinsip():
    print(f"""
{BOLD}{CYAN}  ┌─────────────────────────────────────────────────────────────┐
  │  🧬 PRINSIP ZUHRI FORMALISM                                 │
  ├─────────────────────────────────────────────────────────────┤{RESET}
  │  {GOLD}1.{RESET} Keseimbangan Dinamis — {DIM}0-8-9 harmonis{RESET}
  │  {GOLD}2.{RESET} Fluid-Core — {DIM}Inti yang mengalir, bukan kaku{RESET}
  │  {GOLD}3.{RESET} Echo-Synapse — {DIM}Resonansi antar sistem{RESET}
  │  {GOLD}4.{RESET} Parallel Predictive — {DIM}Antisipasi, bukan reaksi{RESET}
  │  {GOLD}5.{RESET} Kemandirian Digital — {DIM}Tanpa cloud, tanpa kompromi{RESET}
{BOLD}{CYAN}  └─────────────────────────────────────────────────────────────┘{RESET}
""")

def print_status():
    status = get_status()
    
    if status['tor'] != "offline":
        tor_status = f"{GREEN}✅ {status['tor']}{RESET}"
    else:
        tor_status = f"{RED}❌ OFFLINE{RESET}"
    
    ollama_status = f"{GREEN}✅ ONLINE{RESET}" if status['ollama'] == "online" else f"{RED}❌ OFFLINE{RESET}"
    
    def sc(key):
        return f"{GREEN}✅{RESET}" if status['scripts'].get(key, False) else f"{RED}❌{RESET}"
    
    print(f"""{BOLD}{CYAN}  ┌─────────────────────────────────────────────────────────────┐
  │  📊 STATUS SISTEM RESONANSI                                │
  ├─────────────────────────────────────────────────────────────┤{RESET}
  │  {CYAN}TOR      {RESET}: {tor_status}                                     
  │  {CYAN}OLLAMA   {RESET}: {ollama_status}                                     
  │  {DIM}───────────────────────────────────────────────────────────{RESET}
  │  {CYAN}MESH{RESET}:{sc('mesh')}  {CYAN}VISION{RESET}:{sc('vision')}  {CYAN}DARK-WEB{RESET}:{sc('dark-web')}  
  │  {CYAN}PREDICT{RESET}:{sc('predictive')}  {CYAN}VOICE{RESET}:{sc('voice')}  {CYAN}SOS{RESET}:{sc('sos')}  
  │  {CYAN}TRANSLATE{RESET}:{sc('translate')}  {CYAN}WALLET{RESET}:{sc('wallet')}  
{BOLD}{CYAN}  └─────────────────────────────────────────────────────────────┘{RESET}
""")

def print_formula():
    print(f"""
{BOLD}{MAGENTA}  ╔══════════════════════════════════════════════════════════════════╗
  ║  🧬 FORMULA RESONANSI ZUHRI                                     ║
  ╠══════════════════════════════════════════════════════════════════╣{RESET}
{MAGENTA}  ║{RESET}                                                                  {MAGENTA}║{RESET}
{MAGENTA}  ║{RESET}  {GOLD}0{RESET} = {CYAN}KOSONG — Potensi Murni{RESET}                                 {MAGENTA}║{RESET}
{MAGENTA}  ║{RESET}  {GOLD}8{RESET} = {CYAN}INFINITI — Siklus Tak Terbatas{RESET}                          {MAGENTA}║{RESET}
{MAGENTA}  ║{RESET}  {GOLD}9{RESET} = {CYAN}KESEMPURNAAN — Keseimbangan{RESET}                             {MAGENTA}║{RESET}
{MAGENTA}  ║{RESET}                                                                  {MAGENTA}║{RESET}
{MAGENTA}  ║{RESET}  {BOLD}0 + 8 + 9 = 17 → 1 + 7 = 8{RESET}                                {MAGENTA}║{RESET}
{MAGENTA}  ║{RESET}  {DIM}Harmoni dalam ketidakterbatasan{RESET}                              {MAGENTA}║{RESET}
{MAGENTA}  ║{RESET}                                                                  {MAGENTA}║{RESET}
{BOLD}{MAGENTA}  ╚══════════════════════════════════════════════════════════════════╝{RESET}
""")

def main():
    while True:
        print_header()
        print_prinsip()
        print_status()
        print_formula()
        
        print(f"""{BOLD}{CYAN}  ┌─────────────────────────────────────────────────────────────┐
  │  📡 AKSI CEPAT                                              │
  ├─────────────────────────────────────────────────────────────┤{RESET}
  │  {CYAN}1.{RESET} Key Kosmik        → {GOLD}key{RESET}
  │  {CYAN}2.{RESET} Zuhri OS          → {GOLD}zos{RESET}
  │  {CYAN}3.{RESET} System Health     → {GOLD}health{RESET}
  │  {CYAN}4.{RESET} Version Monitor   → {GOLD}version{RESET}
  │  {CYAN}0.{RESET} Keluar            → {DIM}Tutup{RESET}
{BOLD}{CYAN}  └─────────────────────────────────────────────────────────────┘{RESET}
""")
        
        try:
            choice = input(f"{GOLD}  📡 Pilih aksi (0-4){RESET}: ").strip()
            if choice == "1":
                os.system("key")
            elif choice == "2":
                os.system("zos")
            elif choice == "3":
                os.system("health")
            elif choice == "4":
                os.system("version")
            elif choice == "0":
                print(f"\n{GOLD}👋 Resonansi dihentikan. Sampai jumpa, KURNIAWAN!{RESET}\n")
                break
        except KeyboardInterrupt:
            print(f"\n{GOLD}👋 Sampai jumpa!{RESET}")
            break

if __name__ == "__main__":
    main()
