#!/data/data/com.termux/files/usr/bin/python
"""
P2P-MESH + ZUHRI ID (FULL)
Jaringan Darurat dengan Identitas Terverifikasi
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import json
import time
import socket
import threading
import random
import os
import sys
import base64
from datetime import datetime

from p2pnetwork.node import Node

# ===== IMPORT ZUHRI AUTH =====
sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import (
        load_identity, sign, verify,
        secure_package, process_package,
        get_status, log_verified
    )
    ZUHRI_AUTH_OK = True
except ImportError:
    ZUHRI_AUTH_OK = False

# ===== KONFIGURASI =====
HOME = os.path.expanduser("~")
HOST = '0.0.0.0'
PORT = 8000 + random.randint(1, 200)

# ===== IDENTITAS =====
if ZUHRI_AUTH_OK:
    STATUS = get_status()
    if STATUS['active']:
        NODE_NAME = STATUS['name']
        ZUHRI_ID = STATUS['zuhri_id']
    else:
        NODE_NAME = input("🔑 Nama node: ") or "Anonymous"
        ZUHRI_ID = None
else:
    NODE_NAME = input("🔑 Nama node: ") or "Anonymous"
    ZUHRI_ID = None

# ===== WARNA =====
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GOLD = "\033[93m"

# ===== TAMPILAN AWAL =====
os.system('clear')
print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📡 P2P-MESH + ZUHRI ID — ZUHRI NETWORK                        ║
║  ──────────────────────────────────────────────────────────────  ║
║  NODE  : {GOLD}{NODE_NAME}{RESET}
║  PORT  : {GOLD}{PORT}{RESET}
║  STATUS: {GREEN}🟢 ONLINE{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")

if ZUHRI_ID:
    print(f"{GREEN}🆔 ZUHRI ID: {GOLD}{ZUHRI_ID}{RESET}")
    print(f"{GREEN}✅ Mode    : TERVERIFIKASI{RESET}\n")
else:
    print(f"{YELLOW}⚠️  Zuhri ID belum ada — jalankan: id create{RESET}\n")

# ============================================================
# NODE CLASS
# ============================================================
class MeshNode(Node):
    def __init__(self, name, host, port):
        super().__init__(host, port)
        self.name = name
        self.peers = []
        self.running = True

    # ===== TERIMA PESAN =====
    def on_node_message(self, node, data):
        try:
            # Proses paket dengan Zuhri Auth
            if ZUHRI_AUTH_OK:
                msg = process_package(data)
                if not msg:
                    return
            else:
                msg = json.loads(data)
                msg['verified'] = False
            
            sender = msg.get('from', 'unknown')
            text = msg.get('text', '')
            msg_type = msg.get('type', 'chat')
            timestamp = msg.get('time', 'unknown')
            verified = msg.get('verified', False)
            warning = msg.get('warning', '')
            zuhri_id = msg.get('zuhri_id', 'N/A')

            # ===== SOS =====
            if msg_type == 'sos':
                badge = f"{GREEN}✅{RESET}" if verified else f"{RED}⚠️ {RESET}"
                print(f"""
{RED}╔══════════════════════════════════════════════════════════════════╗
║  🆘 SOS DARURAT DITERIMA!                                      ║
║  ──────────────────────────────────────────────────────────────  ║
║  PENGIRIM : {sender}
║  STATUS   : {badge}
║  ID       : {zuhri_id}
║  PESAN    : {text}
║  WAKTU    : {timestamp}
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
                self.auto_sos_response(sender)
                try:
                    os.system("termux-vibrate -d 2000 2>/dev/null &")
                except:
                    pass
                return

            # ===== SOS RESPONSE =====
            if msg_type == 'sos_response':
                print(f"\n{GREEN}✅ [RESPON SOS] {sender}: {text}{RESET}")
                return

            # ===== CHAT =====
            if verified:
                print(f"\n📨 [{timestamp}] {GREEN}✅{RESET} {BOLD}{sender}{RESET}: {text}")
                print(f"   {DIM}ID: {zuhri_id}{RESET}")
            elif warning:
                print(f"\n📨 [{timestamp}] {RED}⚠️ {RESET} {BOLD}{sender}{RESET}: {text}")
                print(f"   {YELLOW}{warning}{RESET}")
            else:
                print(f"\n📨 [{timestamp}] {DIM}{sender}{RESET}: {text}")

        except Exception as e:
            print(f"\n{RED}⚠️ Error: {e}{RESET}")

    # ===== AUTO SOS RESPONSE =====
    def auto_sos_response(self, sender):
        text = f"[RESPON SOS] {self.name} menerima sinyal. Bantuan segera."
        
        if ZUHRI_AUTH_OK:
            pkg = secure_package(text, "sos_response")
            if pkg:
                self.send_to_nodes(json.dumps(pkg))
                print(f"{GREEN}✅ Auto-response SOS terverifikasi dikirim ke {sender}{RESET}")
                return
        
        msg = {
            'from': self.name,
            'text': text,
            'time': datetime.now().strftime('%H:%M:%S'),
            'type': 'sos_response'
        }
        self.send_to_nodes(json.dumps(msg))
        print(f"✅ Auto-response SOS dikirim ke {sender}")

    # ===== KIRIM PESAN =====
    def send_message(self, text, msg_type='chat'):
        if ZUHRI_AUTH_OK:
            pkg = secure_package(text, msg_type)
            if pkg:
                self.send_to_nodes(json.dumps(pkg))
                log_verified(f"MESH_SEND: {text[:50]}")
                print(f"📤 {GREEN}✅{RESET} Pesan terverifikasi ke {len(self.peers)} node")
                return
        
        msg = {
            'from': self.name,
            'text': text,
            'time': datetime.now().strftime('%H:%M:%S'),
            'type': msg_type
        }
        self.send_to_nodes(json.dumps(msg))
        print(f"📤 {YELLOW}⚠️ {RESET} Pesan tanpa tanda tangan ke {len(self.peers)} node")

    # ===== KIRIM PESAN PANJANG =====
    def send_long_message(self, text):
        chunk = 500
        chunks = [text[i:i+chunk] for i in range(0, len(text), chunk)]
        if len(chunks) == 1:
            self.send_message(text)
        else:
            self.send_message(f"[PANJANG] {len(chunks)} bagian...")
            for i, c in enumerate(chunks, 1):
                self.send_message(f"[{i}/{len(chunks)}] {c}")
                time.sleep(0.5)

    # ===== KIRIM FILE =====
    def send_file(self, path):
        try:
            with open(path) as f:
                content = f.read()
            self.send_long_message(f"[FILE] {path}\n\n{content}")
            print(f"📄 File terkirim ({len(content)} karakter)")
        except Exception as e:
            print(f"{RED}❌ Gagal kirim file: {e}{RESET}")

    # ===== KIRIM SOS =====
    def send_sos(self, text="SOS! Saya membutuhkan bantuan!"):
        if ZUHRI_AUTH_OK:
            pkg = secure_package(text, "sos")
            if pkg:
                self.send_to_nodes(json.dumps(pkg))
                log_verified(f"SOS: {text[:50]}", "SOS")
                print(f"\n{RED}🆘 SINYAL SOS TERVERIFIKASI DIKIRIM!{RESET}")
                return
        
        msg = {
            'from': self.name,
            'text': text,
            'time': datetime.now().strftime('%H:%M:%S'),
            'type': 'sos'
        }
        self.send_to_nodes(json.dumps(msg))
        print(f"\n{RED}🆘 SINYAL SOS DIKIRIM (tanpa tanda tangan){RESET}")

    # ===== NODE CONNECTED =====
    def on_node_connected(self, node):
        self.peers.append(node)
        print(f"\n{GREEN}🔗 Node terhubung: {node.id} (total: {len(self.peers)}){RESET}")
        
        # Kirim welcome terverifikasi
        welcome = f"👋 {self.name} bergabung di P2P-Mesh!"
        self.send_message(welcome, "welcome")

    # ===== NODE DISCONNECTED =====
    def on_node_disconnected(self, node):
        if node in self.peers:
            self.peers.remove(node)
        print(f"\n{YELLOW}🔌 Node terputus: {node.id} (total: {len(self.peers)}){RESET}")

    # ===== LIHAT PEERS =====
    def show_peers(self):
        print(f"\n{BOLD}{CYAN}📋 NODE TERHUBUNG:{RESET}")
        if self.peers:
            for i, p in enumerate(self.peers, 1):
                print(f"  {GOLD}{i}.{RESET} {p.id}")
        else:
            print(f"  {DIM}(Belum ada node terhubung){RESET}")
        print()

# ============================================================
# START NODE
# ============================================================
node = MeshNode(NODE_NAME, HOST, PORT)

def start_node():
    try:
        node.start()
        print(f"{GREEN}✅ Node berjalan di port {PORT}{RESET}")
        print(f"{DIM}📡 Menunggu koneksi...{RESET}\n")
    except Exception as e:
        print(f"{RED}❌ Gagal start node: {e}{RESET}")

threading.Thread(target=start_node, daemon=True).start()
time.sleep(2)

# ============================================================
# INTERFACE
# ============================================================
print(f"""{BOLD}{CYAN}═══════════════════════════════════════════════════════════
  📡 P2P-MESH + ZUHRI ID — COMMANDS
═══════════════════════════════════════════════════════════{RESET}

  {GOLD}/connect <ip>{RESET}     → Hubungkan ke node lain
  {GOLD}/msg <pesan>{RESET}      → Kirim pesan terverifikasi
  {GOLD}/long <pesan>{RESET}     → Kirim pesan panjang
  {GOLD}/file <path>{RESET}      → Kirim file teks
  {GOLD}/sos{RESET}              → Sinyal darurat
  {GOLD}/peers{RESET}            → Lihat node terhubung
  {GOLD}/id{RESET}               → Lihat Zuhri ID
  {GOLD}/status{RESET}           → Status sistem
  {GOLD}/help{RESET}             → Bantuan
  {GOLD}/exit{RESET}             → Keluar

{BOLD}{CYAN}═══════════════════════════════════════════════════════════{RESET}
""")

# ============================================================
# MAIN LOOP
# ============================================================
while True:
    try:
        cmd = input(f"{GOLD}📡 > {RESET}").strip()
        if not cmd:
            continue

        # ===== EXIT =====
        if cmd == "/exit":
            print(f"{RED}🛑 Menutup node...{RESET}")
            node.stop()
            break

        # ===== PEERS =====
        elif cmd == "/peers":
            node.show_peers()

        # ===== ID =====
        elif cmd == "/id":
            if ZUHRI_ID:
                identity = load_identity()
                print(f"""
{BOLD}{CYAN}🆔 ZUHRI ID{RESET}
{'─' * 50}
  ID       : {GOLD}{identity['zuhri_id']}{RESET}
  Nama     : {GOLD}{identity['name']}{RESET}
  Role     : {GOLD}{identity.get('role', 'Operator')}{RESET}
  Dibuat   : {GOLD}{identity['created'][:19]}{RESET}
  Public   : {DIM}{identity['public_key'][:50]}...{RESET}
{'─' * 50}
""")
            else:
                print(f"{YELLOW}⚠️  Belum ada Zuhri ID — jalankan: id create{RESET}\n")

        # ===== STATUS =====
        elif cmd == "/status":
            print(f"""
{BOLD}{CYAN}📊 STATUS P2P-MESH{RESET}
{'─' * 50}
  Nama Node : {GOLD}{NODE_NAME}{RESET}
  Port      : {GOLD}{PORT}{RESET}
  Peers     : {GOLD}{len(node.peers)}{RESET}
  Zuhri ID  : {GOLD}{ZUHRI_ID if ZUHRI_ID else 'N/A'}{RESET}
  Mode      : {GREEN + '✅ TERVERIFIKASI' + RESET if ZUHRI_ID else YELLOW + '⚠️  TANPA ID' + RESET}
{'─' * 50}
""")

        # ===== CONNECT =====
        elif cmd.startswith("/connect "):
            ip = cmd.split(" ")[1]
            try:
                node.connect_with_node(ip, PORT)
                print(f"🔗 Mencoba koneksi ke {ip}:{PORT}...")
            except Exception as e:
                print(f"{RED}❌ Gagal koneksi: {e}{RESET}")

        # ===== MSG =====
        elif cmd.startswith("/msg "):
            node.send_message(cmd[5:])

        # ===== LONG =====
        elif cmd.startswith("/long "):
            node.send_long_message(cmd[6:])

        # ===== FILE =====
        elif cmd.startswith("/file "):
            node.send_file(cmd[6:])

        # ===== SOS =====
        elif cmd == "/sos":
            text = input("📢 Pesan SOS (Enter untuk default): ").strip()
            if not text:
                text = "SOS! Saya membutuhkan bantuan darurat!"
            node.send_sos(text)

        # ===== HELP =====
        elif cmd == "/help":
            print(f"""
{BOLD}{CYAN}📡 BANTUAN P2P-MESH{RESET}
{'─' * 50}
  {GOLD}/connect <ip>{RESET}     → Hubungkan node
  {GOLD}/msg <pesan>{RESET}      → Pesan terverifikasi
  {GOLD}/long <pesan>{RESET}     → Pesan panjang
  {GOLD}/file <path>{RESET}      → Kirim file
  {GOLD}/sos{RESET}              → Sinyal darurat
  {GOLD}/peers{RESET}            → Lihat node
  {GOLD}/id{RESET}               → Lihat Zuhri ID
  {GOLD}/status{RESET}           → Status sistem
  {GOLD}/help{RESET}             → Bantuan
  {GOLD}/exit{RESET}             → Keluar
{'─' * 50}
""")

        # ===== UNKNOWN =====
        else:
            print(f"{RED}❌ Perintah tidak dikenal. Ketik /help{RESET}")

    except KeyboardInterrupt:
        print(f"\n{RED}🛑 Keluar...{RESET}")
        node.stop()
        break
    except Exception as e:
        print(f"{RED}⚠️ {e}{RESET}")
