#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI P2P-MESH V2.0 — HYBRID NETWORK
LAN + WAN + Relay + Enkripsi
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, time, random, socket, threading, hashlib, base64, secrets, subprocess
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    CRYPTO_OK = True
except ImportError:
    CRYPTO_OK = False

HOME = os.path.expanduser("~")
MESH_DIR = os.path.join(HOME, "kosmik", "p2p")
os.makedirs(MESH_DIR, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

# ============================================================
# KONFIGURASI V2.0
# ============================================================
HOST = '0.0.0.0'
LAN_PORT = 8000 + random.randint(1, 200)
WAN_PORT = 9000 + random.randint(1, 200)
DISCOVERY_PORT = 8001
RELAY_PORT = 9100

# Identitas
if ZUHRI_ID_OK:
    identity = load_identity()
    if identity:
        NODE_NAME = identity['name']
        ZUHRI_ID = identity['zuhri_id']
    else:
        NODE_NAME = input("🔑 Nama node: ") or "Anonymous"
        ZUHRI_ID = None
else:
    NODE_NAME = input("🔑 Nama node: ") or "Anonymous"
    ZUHRI_ID = None

# ============================================================
# STATE
# ============================================================
peers = []           # LAN peers
wan_peers = []       # WAN peers
relay_peers = []     # Relay peers
messages = []        # Message history
running = True

# ============================================================
# ENKRIPSI V2.0
# ============================================================
def encrypt_msg(text, password="zuhri-mesh"):
    """Enkripsi pesan dengan AES-256-GCM"""
    if not CRYPTO_OK:
        return base64.b64encode(text.encode()).decode()
    
    try:
        salt = secrets.token_bytes(16)
        nonce = secrets.token_bytes(12)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt,
            iterations=100000, backend=default_backend()
        )
        key = kdf.derive(password.encode())
        aes = AESGCM(key)
        ct = aes.encrypt(nonce, text.encode(), None)
        return base64.b64encode(salt + nonce + ct).decode()
    except:
        return base64.b64encode(text.encode()).decode()

def decrypt_msg(ciphertext, password="zuhri-mesh"):
    """Dekripsi pesan"""
    if not CRYPTO_OK:
        try:
            return base64.b64decode(ciphertext).decode()
        except:
            return ciphertext
    
    try:
        data = base64.b64decode(ciphertext)
        salt, nonce, ct = data[:16], data[16:28], data[28:]
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt,
            iterations=100000, backend=default_backend()
        )
        key = kdf.derive(password.encode())
        aes = AESGCM(key)
        return aes.decrypt(nonce, ct, None).decode()
    except:
        return None

# ============================================================
# LAN MODE (Seperti V1)
# ============================================================
def lan_listener():
    """Listener LAN"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", LAN_PORT))
        s.settimeout(2)
        
        while running:
            try:
                data, addr = s.recvfrom(4096)
                msg = json.loads(data.decode())
                
                # Dekripsi
                if 'encrypted' in msg:
                    dec = decrypt_msg(msg['encrypted'])
                    if dec:
                        msg['text'] = dec
                
                msg['from_ip'] = addr[0]
                msg['received'] = datetime.now().isoformat()
                msg['network'] = 'LAN'
                messages.append(msg)
                
                # Tampilkan
                print(f"\n{BLUE}📡 [LAN] [{msg.get('from','?')}]{RESET} {msg.get('text','')}")
                print(f"{DIM}   {msg.get('time','')} | {addr[0]}{RESET}")
            except socket.timeout:
                continue
            except Exception as e:
                pass
    except Exception as e:
        print(f"{RED}❌ LAN listener error: {e}{RESET}")

def lan_send(text):
    """Kirim via LAN broadcast"""
    msg = {
        "type": "chat",
        "from": NODE_NAME,
        "text": text,
        "network": "LAN",
        "time": datetime.now().strftime("%H:%M:%S"),
        "zuhri_id": ZUHRI_ID
    }
    
    # Enkripsi
    msg['encrypted'] = encrypt_msg(text)
    del msg['text']
    
    # Tanda tangan
    if ZUHRI_ID_OK:
        sig = sign(text)
        if sig:
            msg['signature'] = sig
            msg['public_key'] = load_identity()['public_key']
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(json.dumps(msg).encode(), ("255.255.255.255", LAN_PORT))
        s.close()
        return True
    except:
        return False

# ============================================================
# WAN MODE (Via Internet — Tracker)
# ============================================================
def wan_listener():
    """Listener WAN"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", WAN_PORT))
        s.settimeout(2)
        
        while running:
            try:
                data, addr = s.recvfrom(4096)
                msg = json.loads(data.decode())
                
                if 'encrypted' in msg:
                    dec = decrypt_msg(msg['encrypted'])
                    if dec:
                        msg['text'] = dec
                
                msg['from_ip'] = addr[0]
                msg['network'] = 'WAN'
                messages.append(msg)
                
                print(f"\n{MAGENTA}🌐 [WAN] [{msg.get('from','?')}]{RESET} {msg.get('text','')}")
                print(f"{DIM}   {msg.get('time','')} | {addr[0]}{RESET}")
            except socket.timeout:
                continue
            except:
                pass
    except:
        pass

def wan_send(host, port, text):
    """Kirim ke host tertentu (WAN)"""
    msg = {
        "type": "chat",
        "from": NODE_NAME,
        "network": "WAN",
        "time": datetime.now().strftime("%H:%M:%S"),
        "zuhri_id": ZUHRI_ID
    }
    msg['encrypted'] = encrypt_msg(text)
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(json.dumps(msg).encode(), (host, port))
        s.close()
        return True
    except Exception as e:
        print(f"{RED}❌ Gagal kirim WAN: {e}{RESET}")
        return False

# ============================================================
# DISCOVERY — Cari node otomatis
# ============================================================
def discovery_listener():
    """Dengar broadcast discovery"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", DISCOVERY_PORT))
        s.settimeout(2)
        
        while running:
            try:
                data, addr = s.recvfrom(1024)
                msg = json.loads(data.decode())
                
                if msg.get('type') == 'discovery':
                    if addr[0] not in peers:
                        peers.append(addr[0])
                        print(f"\n{GREEN}🔍 Node ditemukan: {msg.get('name','?')} ({addr[0]}){RESET}")
            except socket.timeout:
                continue
            except:
                pass
    except:
        pass

def discovery_broadcast():
    """Broadcast kehadiran"""
    msg = {
        "type": "discovery",
        "name": NODE_NAME,
        "zuhri_id": ZUHRI_ID,
        "port": LAN_PORT,
        "time": datetime.now().isoformat()
    }
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(json.dumps(msg).encode(), ("255.255.255.255", DISCOVERY_PORT))
        s.close()
    except:
        pass

# ============================================================
# RELAY MODE
# ============================================================
def relay_listener():
    """Terima pesan relay"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", RELAY_PORT))
        s.settimeout(2)
        
        while running:
            try:
                data, addr = s.recvfrom(4096)
                msg = json.loads(data.decode())
                
                # Forward ke LAN
                lan_send(f"[RELAY dari {msg.get('from','?')}] {msg.get('text','')}")
                relay_peers.append(addr[0])
            except socket.timeout:
                continue
            except:
                pass
    except:
        pass

# ============================================================
# GET IP
# ============================================================
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_public_ip():
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "5", "ifconfig.me"],
            capture_output=True, text=True, timeout=10
        )
        return r.stdout.strip() or "Tidak terdeteksi"
    except:
        return "Tidak terdeteksi"

# ============================================================
# TAMPILAN
# ============================================================
def clear():
    os.system('clear')

def print_header():
    clear()
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  📡 ZUHRI P2P-MESH V2.0 — HYBRID NETWORK                            ║
║  ──────────────────────────────────────────────────────────────────  ║
║  NODE     : {GOLD}{NODE_NAME}{RESET}
║  ZUHRI ID : {GOLD}{ZUHRI_ID[:32] if ZUHRI_ID else 'Tidak ada'}{RESET}
║  LAN PORT : {LAN_PORT} | WAN PORT: {WAN_PORT}{RESET}
║  LOCAL IP : {CYAN}{local_ip}{RESET}
║  PUBLIC IP: {CYAN}{public_ip}{RESET}
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")

def print_status():
    print(f"""{BOLD}{CYAN}  📊 STATUS:{RESET}
  {GREEN}✅{RESET} LAN Peers    : {len(peers)}
  {GREEN}✅{RESET} WAN Peers    : {len(wan_peers)}
  {GREEN}✅{RESET} Relay Peers  : {len(relay_peers)}
  {GREEN}✅{RESET} Messages     : {len(messages)}
  {GREEN}✅{RESET} Enkripsi      : {'AES-256-GCM' if CRYPTO_OK else 'Base64'}
""")

def print_help():
    print(f"""{BOLD}{CYAN}📡 PERINTAH:{RESET}
  {GOLD}/lan <pesan>{RESET}        → Chat LAN (broadcast)
  {GOLD}/wan <ip> <port> <pesan>{RESET} → Chat WAN (direct)
  {GOLD}/discover{RESET}            → Cari node
  {GOLD}/relay <pesan>{RESET}        → Relay pesan
  {GOLD}/peers{RESET}               → Lihat peers
  {GOLD}/status{RESET}              → Status
  {GOLD}/history{RESET}             → Riwayat
  {GOLD}/ip{RESET}                  → Lihat IP
  {GOLD}/help{RESET}                → Bantuan
  {GOLD}/exit{RESET}                → Keluar
""")

# ============================================================
# MAIN
# ============================================================
def main():
    global running
    
    print_header()
    print(f"{CYAN}🚀 Memulai P2P-Mesh V2.0...{RESET}\n")
    
    # Start threads
    threads = [
        threading.Thread(target=lan_listener, daemon=True),
        threading.Thread(target=wan_listener, daemon=True),
        threading.Thread(target=discovery_listener, daemon=True),
        threading.Thread(target=relay_listener, daemon=True),
    ]
    
    for t in threads:
        t.start()
        time.sleep(0.3)
    
    # Broadcast discovery
    discovery_broadcast()
    
    print(f"{GREEN}✅ Semua service aktif:{RESET}")
    print(f"  {GOLD}•{RESET} LAN Listener : port {LAN_PORT}")
    print(f"  {GOLD}•{RESET} WAN Listener : port {WAN_PORT}")
    print(f"  {GOLD}•{RESET} Discovery    : port {DISCOVERY_PORT}")
    print(f"  {GOLD}•{RESET} Relay        : port {RELAY_PORT}")
    print()
    
    print_status()
    print()
    print_help()
    
    # Loop perintah
    while running:
        try:
            cmd = input(f"{GOLD}📡 > {RESET}").strip()
            
            if not cmd:
                continue
            
            if cmd.lower() in ["/exit", "/quit", "exit", "quit"]:
                running = False
                print(f"\n{CYAN}👋 Sampai jumpa!{RESET}\n")
                break
            
            elif cmd == "/help":
                print_help()
            
            elif cmd == "/status":
                print_status()
            
            elif cmd == "/peers":
                print(f"\n{BOLD}📋 LAN PEERS:{RESET}")
                for p in peers:
                    print(f"  • {p}")
                print(f"\n{BOLD}📋 WAN PEERS:{RESET}")
                for p in wan_peers:
                    print(f"  • {p}")
                print(f"\n{BOLD}📋 RELAY PEERS:{RESET}")
                for p in relay_peers:
                    print(f"  • {p}")
                print()
            
            elif cmd == "/history":
                print(f"\n{BOLD}📜 RIWAYAT ({len(messages)}):{RESET}")
                for m in messages[-20:]:
                    net = m.get('network', '?')
                    print(f"  [{net}] {m.get('from','?')}: {m.get('text','')}")
                print()
            
            elif cmd == "/ip":
                print(f"\n{BOLD}🌐 IP:{RESET}")
                print(f"  Local  : {get_local_ip()}")
                print(f"  Public : {get_public_ip()}\n")
            
            elif cmd == "/discover":
                print(f"\n{CYAN}🔍 Broadcast discovery...{RESET}")
                discovery_broadcast()
                print(f"{GREEN}✅ Selesai{RESET}\n")
            
            elif cmd.startswith("/lan "):
                text = cmd[5:]
                if lan_send(text):
                    print(f"{GREEN}✅ LAN terkirim{RESET}")
                else:
                    print(f"{RED}❌ Gagal kirim LAN{RESET}")
            
            elif cmd.startswith("/wan "):
                parts = cmd[5:].split(" ", 2)
                if len(parts) >= 3:
                    host, port, text = parts[0], parts[1], parts[2]
                    if wan_send(host, int(port), text):
                        print(f"{GREEN}✅ WAN terkirim ke {host}:{port}{RESET}")
                    else:
                        print(f"{RED}❌ Gagal kirim WAN{RESET}")
                else:
                    print(f"{YELLOW}⚠️  Format: /wan <ip> <port> <pesan>{RESET}")
            
            elif cmd.startswith("/relay "):
                text = cmd[7:]
                # Broadcast ke LAN + relay
                lan_send(f"[RELAY] {text}")
                print(f"{GREEN}✅ Relay terkirim{RESET}")
            
            else:
                print(f"{YELLOW}⚠️  Perintah tidak dikenal. Ketik /help{RESET}")
        
        except KeyboardInterrupt:
            running = False
            print(f"\n{CYAN}👋 Sampai jumpa!{RESET}\n")
            break
        except Exception as e:
            print(f"{RED}❌ Error: {e}{RESET}")

if __name__ == "__main__":
    main()
