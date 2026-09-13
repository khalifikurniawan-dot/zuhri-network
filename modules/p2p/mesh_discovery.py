#!/usr/bin/env python3
"""ZUHRI MESH-SCAN V2.0 — Cari node + Media discovery"""

import socket, time, sys, os, json

BROADCAST_PORT = 8001
NODE_NAME = input("🔑 Nama node: ") or "Anonymous"

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
GREEN="\033[92m"; YELLOW="\033[93m"; CYAN="\033[96m"; RED="\033[91m"

def clear(): os.system('clear')

def send_broadcast():
    """Kirim sinyal pencarian"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(2)
        
        message = f"P2P-MESH-V2|{NODE_NAME}|{time.time()}"
        
        for _ in range(3):
            try:
                sock.sendto(message.encode(), ('255.255.255.255', BROADCAST_PORT))
            except:
                pass
            time.sleep(1)
        
        sock.close()
        return True
    except:
        return False

def listen_broadcast():
    """Dengarkan balasan"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', BROADCAST_PORT))
        sock.settimeout(5)
        
        nodes = []
        
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                try:
                    parts = data.decode().split('|')
                    if len(parts) >= 2:
                        name = parts[1]
                        if addr[0] not in nodes:
                            nodes.append(addr[0])
                            print(f"  {GREEN}🔍 Node ditemukan:{RESET} {name} ({addr[0]})")
                except:
                    pass
            except socket.timeout:
                break
            except:
                break
        
        sock.close()
        return nodes
    except:
        return []

def main():
    clear()
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════════╗
║  📡 ZUHRI MESH-SCAN V2.0 — DISCOVERY SERVICE                            ║
║  ──────────────────────────────────────────────────────────────────────  ║
║  NODE  : {NODE_NAME}{RESET}
║  PORT  : {BROADCAST_PORT}{RESET}
║  STATUS: {GREEN}🟢 SCANNING{RESET}
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{YELLOW}📡 Mencari node di jaringan...{RESET}
{DIM}{'─' * 55}{RESET}
""")
    
    send_broadcast()
    nodes = listen_broadcast()
    
    print(f"{DIM}{'─' * 55}{RESET}")
    
    if nodes:
        print(f"\n{GREEN}✅ {len(nodes)} node ditemukan:{RESET}\n")
        print(f"{BOLD}Koneksi yang tersedia:{RESET}\n")
        for ip in nodes:
            print(f"  {GOLD}→ /connect {ip}{RESET}")
        print(f"\n{DIM}Gunakan perintah di atas di dalam mesh_node.py{RESET}")
    else:
        print(f"\n{YELLOW}⚠️  Tidak ada node ditemukan.{RESET}")
        print(f"{DIM}Pastikan node lain sedang aktif.{RESET}")
    
    print(f"{DIM}{'─' * 55}{RESET}\n")

if __name__ == "__main__":
    main()
