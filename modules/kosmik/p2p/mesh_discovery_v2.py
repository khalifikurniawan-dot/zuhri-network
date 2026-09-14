#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI MESH DISCOVERY V2.0 — Cari Node
LAN + WAN Discovery
"""

import os, sys, json, socket, time, subprocess
from datetime import datetime

DISCOVERY_PORT = 8001
LAN_PORT = 8000

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

NODE_NAME = input("🔑 Nama node: ").strip() or "Anonymous"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def discover():
    """Cari node di jaringan"""
    print(f"\n{CYAN}🔍 Memulai discovery...{RESET}\n")
    
    # Broadcast
    msg = {
        "type": "discovery",
        "name": NODE_NAME,
        "ip": get_local_ip(),
        "time": datetime.now().isoformat()
    }
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    try:
        for i in range(3):
            sock.sendto(json.dumps(msg).encode(), ("255.255.255.255", DISCOVERY_PORT))
            print(f"{DIM}  Broadcast #{i+1}{RESET}")
            time.sleep(0.5)
    except:
        pass
    
    # Listen
    sock.settimeout(5)
    sock.bind(("", DISCOVERY_PORT + 100))
    
    nodes = []
    print(f"\n{CYAN}📡 Mendengar balasan (5 detik)...{RESET}\n")
    
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            try:
                reply = json.loads(data.decode())
                if addr[0] not in [n['ip'] for n in nodes]:
                    nodes.append({
                        "ip": addr[0],
                        "name": reply.get('name', '?'),
                        "time": reply.get('time', '?')
                    })
                    print(f"  {GREEN}🔍 {reply.get('name','?')} ({addr[0]}){RESET}")
            except:
                pass
    except socket.timeout:
        pass
    finally:
        sock.close()
    
    print(f"\n{BOLD}📊 HASIL:{RESET}")
    print(f"  Node ditemukan: {len(nodes)}")
    
    if nodes:
        print(f"\n{BOLD}🔗 NODE:{RESET}")
        for n in nodes:
            print(f"  {GOLD}•{RESET} {n['name']} → {n['ip']}")
        print(f"\n{DIM}Koneksi: /wan {nodes[0]['ip']} 9000 <pesan>{RESET}")
    else:
        print(f"  {YELLOW}Tidak ada node ditemukan.{RESET}")
        print(f"  {DIM}Pastikan node lain sedang aktif di WiFi yang sama.{RESET}")
    
    print()

if __name__ == "__main__":
    discover()
