#!/data/data/com.termux/files/usr/bin/python
"""
SOS BEACON — ZUHRI NETWORK
Sinyal Darurat Offline via Broadcast
"""

import os
import sys
import time
import json
import socket
import threading
import subprocess
from datetime import datetime

VERSION = "SOS-BEACON v1.0"
BROADCAST_PORT = 1998
NAME = input("🔑 Nama/ID Anda: ") or "Anonymous"
LOCATION = input("📍 Lokasi (opsional): ") or "Unknown"

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_gps():
    try:
        result = subprocess.run(["termux-location"], capture_output=True, text=True, timeout=5)
        if result.stdout:
            data = json.loads(result.stdout)
            return f"{data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}"
    except:
        pass
    return LOCATION

def send_sos_broadcast(message, location):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(1)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sos_data = {
            'type': 'SOS',
            'from': NAME,
            'location': location,
            'message': message,
            'time': timestamp,
            'ip': get_ip()
        }
        sock.sendto(json.dumps(sos_data).encode(), ('255.255.255.255', BROADCAST_PORT))
        sock.close()
        return True
    except:
        return False

def listen_sos():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', BROADCAST_PORT))
        sock.settimeout(2)
        while True:
            try:
                data, addr = sock.recvfrom(2048)
                sos = json.loads(data.decode())
                if sos.get('type') == 'SOS':
                    print(f"""
{RED}╔══════════════════════════════════════════════════════════════════╗
║  🆘 SOS DARURAT DITERIMA!                                      ║
║  ──────────────────────────────────────────────────────────────  ║
║  PENGIRIM : {sos.get('from', 'Unknown')}
║  LOKASI   : {sos.get('location', 'Unknown')}
║  PESAN    : {sos.get('message', 'Tidak ada pesan')}
║  WAKTU    : {sos.get('time', 'Unknown')}
║  IP       : {sos.get('ip', 'Unknown')}
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
                    try:
                        subprocess.run(["termux-vibrate", "-d", "2000"], timeout=2)
                    except:
                        pass
            except:
                pass
    except:
        pass

def sos_beacon():
    os.system('clear')
    print(f"""
{RED}╔══════════════════════════════════════════════════════════════════╗
║  🆘 SOS BEACON — MODE DARURAT AKTIF                              ║
║  ──────────────────────────────────────────────────────────────  ║
║  NAMA   : {NAME}
║  LOKASI : {LOCATION}
║  IP     : {get_ip()}
║  STATUS : {GREEN}✅ BEACON AKTIF{RED}
║  ──────────────────────────────────────────────────────────────  ║
║  {YELLOW}TEKAN CTRL+C UNTUK BERHENTI{RED}
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    listener = threading.Thread(target=listen_sos, daemon=True)
    listener.start()
    
    count = 0
    message = input(f"\n{CYAN}📢 Pesan SOS (enter default): {RESET}").strip()
    if not message:
        message = "SOS! Saya membutuhkan bantuan darurat!"
    
    location = get_gps()
    
    try:
        while True:
            count += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"{YELLOW}[{timestamp}] 🆘 SOS #{count} dikirim...{RESET}")
            if send_sos_broadcast(message, location):
                print(f"{GREEN}  ✅ SOS terkirim{RESET}")
            else:
                print(f"{RED}  ❌ Gagal mengirim SOS{RESET}")
            print(f"{CYAN}  📡 Listening for responses...{RESET}\n")
            time.sleep(30)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}🛑 SOS Beacon dihentikan.{RESET}")
        print(f"{GREEN}✅ Total SOS terkirim: {count}{RESET}")

def show_help():
    print(f"""
{BOLD}{CYAN}SOS BEACON — BANTUAN{RESET}
{'─' * 40}
  {BOLD}sos beacon{RESET}        → Mulai mode darurat
  {BOLD}sos listen{RESET}        → Hanya mendengar sinyal SOS
  {BOLD}sos send "pesan"{RESET}  → Kirim SOS satu kali
  {BOLD}sos help{RESET}          → Tampilkan bantuan
{'─' * 40}
""")

def send_once():
    message = input("📢 Pesan SOS: ").strip() or "SOS! Saya membutuhkan bantuan!"
    location = get_gps()
    if send_sos_broadcast(message, location):
        print(f"{GREEN}✅ SOS terkirim!{RESET}")
        print(f"  📍 Lokasi: {location}")
    else:
        print(f"{RED}❌ Gagal mengirim SOS{RESET}")

def listen_only():
    os.system('clear')
    print(f"{CYAN}📡 Mendengar sinyal SOS... (CTRL+C untuk berhenti){RESET}")
    try:
        listen_sos()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}🛑 Berhenti mendengar.{RESET}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "beacon":
            sos_beacon()
        elif cmd == "listen":
            listen_only()
        elif cmd == "send":
            send_once()
        elif cmd == "help":
            show_help()
        else:
            print(f"{RED}❌ Perintah tidak dikenal: {cmd}{RESET}")
            show_help()
    else:
        show_help()
