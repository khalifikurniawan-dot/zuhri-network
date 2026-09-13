#!/data/data/com.termux/files/usr/bin/python
"""
P2P-MESH — DISCOVERY SERVICE
Mencari node lain di jaringan lokal
Protokol: ZUHRI K-8.0
"""

import socket
import time
import sys
import os

BROADCAST_PORT = 8001
NODE_NAME = input("🔑 Nama node Anda: ") or "Anonymous"

# ===== WARNA =====
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
GOLD = "\033[93m"
DIM = "\033[2m"

def send_broadcast():
    """Kirim sinyal pencarian ke jaringan"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(2)
    message = f"P2P-MESH|{NODE_NAME}|{time.time()}"
    for _ in range(3):
        try:
            sock.sendto(message.encode(), ('255.255.255.255', BROADCAST_PORT))
        except:
            pass
        time.sleep(1)
    sock.close()

def listen_broadcast():
    """Dengarkan balasan dari node lain"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(('', BROADCAST_PORT))
    except:
        print(f"{RED}❌ Gagal bind ke port {BROADCAST_PORT}{RESET}")
        return []
    
    sock.settimeout(5)
    nodes = []
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            try:
                parts = data.decode().split('|')
                if len(parts) >= 2:
                    name = parts[1]
                    if addr[0] not in nodes:
                        nodes.append(addr[0])
                        print(f"{GREEN}🔍 Node ditemukan: {name} ({addr[0]}){RESET}")
            except:
                pass
    except socket.timeout:
        pass
    finally:
        sock.close()
    return nodes

def main():
    os.system('clear')
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📡 P2P-MESH — DISCOVERY SERVICE                              ║
║  ──────────────────────────────────────────────────────────────  ║
║  NODE  : {NODE_NAME}
║  PORT  : {BROADCAST_PORT}
║  STATUS: 🟢 SCANNING
║  PROTOKOL: ZUHRI K-8.0
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    print(f"{YELLOW}📡 Mencari node di jaringan...{RESET}")
    print(f"{DIM}{'─' * 50}{RESET}\n")
    
    # Kirim broadcast
    send_broadcast()
    
    # Dengarkan balasan
    nodes = listen_broadcast()
    
    print(f"\n{DIM}{'─' * 50}{RESET}")
    
    if nodes:
        print(f"\n{GREEN}✅ {len(nodes)} node ditemukan:{RESET}")
        print(f"{BOLD}Koneksi yang tersedia:{RESET}")
        for ip in nodes:
            print(f"  {GOLD}→ /connect {ip}{RESET}")
        print(f"\n{DIM}Gunakan perintah di atas di dalam mesh_node.py{RESET}")
    else:
        print(f"\n{YELLOW}⚠️ Tidak ada node ditemukan.{RESET}")
        print(f"{DIM}Pastikan node lain sedang aktif.{RESET}")
    
    print(f"{DIM}{'─' * 50}{RESET}\n")

if __name__ == "__main__":
    main()
