#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI P2P-MESH V2.0 — JARINGAN DARURAT + VIDEO CALL + CHAT
Fitur: Chat, Voice Call, Video Call, File Transfer, SOS
"""

import json, time, socket, threading, random, os, sys, base64, subprocess
from datetime import datetime

try:
    from p2pnetwork.node import Node
except ImportError:
    print("Install: pip install p2pnetwork")
    sys.exit(1)

# ===== ZUHRI AUTH =====
sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
MEDIA_DIR = os.path.join(HOME, "kosmik", "p2p", "media")
os.makedirs(MEDIA_DIR, exist_ok=True)

HOST = '0.0.0.0'
PORT = 8000 + random.randint(1, 200)
NODE_NAME = input("🔑 Nama node Anda: ") or "Anonymous"

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ===== TAMPILAN AWAL =====
os.system('clear')
print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════════╗
║  📡 ZUHRI P2P-MESH V2.0 — JARINGAN DARURAT OFFLINE                      ║
║  ──────────────────────────────────────────────────────────────────────  ║
║  NODE  : {GOLD}{NODE_NAME}{RESET}
║  PORT  : {GOLD}{PORT}{RESET}
║  STATUS: {GREEN}🟢 ONLINE{RESET}
║  FITUR : Chat | Voice | Video | File | SOS                             ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
""")

if ZUHRI_ID_OK:
    identity = load_identity()
    if identity:
        print(f"{GREEN}🆔 ZUHRI ID: {GOLD}{identity['zuhri_id'][:32]}...{RESET}")
        print(f"{GREEN}✅ Mode: TERVERIFIKASI{RESET}\n")

# ===== MESH NODE CLASS =====
class MeshNode(Node):
    def __init__(self, name, host, port):
        super().__init__(host, port)
        self.name = name
        self.peers = []
        self.running = True
        self.video_active = False
        self.voice_active = False
        self.media_port = port + 1000  # Port media
    
    # ===== TERIMA PESAN =====
    def on_node_message(self, node, data):
        try:
            msg = json.loads(data)
            sender = msg.get('from', 'unknown')
            text = msg.get('text', '')
            msg_type = msg.get('type', 'chat')
            timestamp = msg.get('time', 'unknown')
            signature = msg.get('signature')
            public_key = msg.get('public_key')
            zuhri_id = msg.get('zuhri_id', 'N/A')
            
            # Verifikasi
            verified = False
            if signature and public_key:
                try:
                    verified = verify(text, signature, public_key)
                except:
                    pass
            
            # ===== SOS =====
            if msg_type == 'sos':
                badge = f"{GREEN}✅{RESET}" if verified else f"{RED}⚠️{RESET}"
                print(f"\n{RED}╔══════════════════════════════════════════════════════════╗")
                print(f"║  🆘 SOS DARURAT DITERIMA!                              ║")
                print(f"║  ────────────────────────────────────────────────────  ║")
                print(f"║  Pengirim: {sender} {badge}")
                print(f"║  ID     : {zuhri_id}")
                print(f"║  Pesan  : {text}")
                print(f"║  Waktu  : {timestamp}")
                print(f"╚══════════════════════════════════════════════════════════╝{RESET}\n")
                self.auto_sos_response(sender)
                return
            
            # ===== VIDEO CALL REQUEST =====
            if msg_type == 'video_call':
                print(f"\n{CYAN}📹 {sender} memanggil VIDEO...{RESET}")
                print(f"{GOLD}Terima? (y/n): {RESET}", end="")
                # Auto-accept (bisa diubah)
                time.sleep(1)
                self.send_message(f"VIDEO CALL DITERIMA dari {self.name}", "video_accept")
                print(f"{GREEN}✅ Video call diterima{RESET}\n")
                return
            
            # ===== VIDEO FRAME =====
            if msg_type == 'video_frame':
                frame_data = msg.get('frame', '')
                self.display_video_frame(frame_data, sender)
                return
            
            # ===== VOICE CALL REQUEST =====
            if msg_type == 'voice_call':
                print(f"\n{CYAN}🎤 {sender} memanggil VOICE...{RESET}")
                print(f"{GOLD}Terima? (y/n): {RESET}", end="")
                time.sleep(1)
                self.send_message(f"VOICE CALL DITERIMA dari {self.name}", "voice_accept")
                print(f"{GREEN}✅ Voice call diterima{RESET}\n")
                return
            
            # ===== FILE TRANSFER =====
            if msg_type == 'file':
                filename = msg.get('filename', 'unknown')
                file_data = msg.get('data', '')
                file_path = os.path.join(MEDIA_DIR, filename)
                try:
                    with open(file_path, 'wb') as f:
                        f.write(base64.b64decode(file_data))
                    print(f"\n{GREEN}📁 File diterima: {filename}{RESET}")
                    print(f"{DIM}   Lokasi: {file_path}{RESET}\n")
                except:
                    print(f"\n{RED}❌ Gagal terima file{RESET}\n")
                return
            
            # ===== CHAT =====
            if verified:
                print(f"\n{GREEN}📨 [{timestamp}] ✅ {sender}:{RESET} {text}")
                print(f"{DIM}   ID: {zuhri_id}{RESET}")
            elif signature:
                print(f"\n{RED}📨 [{timestamp}] ❌ {sender}:{RESET} {text}")
                print(f"{YELLOW}   ⚠️  Tanda tangan tidak valid!{RESET}")
            else:
                print(f"\n{DIM}📨 [{timestamp}] ⚠️  {sender}: {text}{RESET}")
        
        except Exception as e:
            print(f"{RED}⚠️ Error: {e}{RESET}")
    
    # ===== DISPLAY VIDEO FRAME =====
    def display_video_frame(self, frame_data, sender):
        try:
            import cv2
            import numpy as np
            
            img_bytes = base64.b64decode(frame_data)
            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is not None:
                cv2.imshow(f'Video Call - {sender}', frame)
                cv2.waitKey(1)
        except:
            # Fallback: tampilkan info
            print(f"{DIM}📹 Frame dari {sender} ({len(frame_data)} bytes){RESET}")
    
    # ===== AUTO SOS RESPONSE =====
    def auto_sos_response(self, sender):
        msg = {
            'from': self.name,
            'text': f"[RESPON SOS] {self.name} menerima sinyal.",
            'time': datetime.now().strftime('%H:%M:%S'),
            'type': 'sos_response'
        }
        if ZUHRI_ID_OK:
            identity = load_identity()
            if identity:
                sig = sign(msg['text'])
                if sig:
                    msg['signature'] = sig
                    msg['public_key'] = identity['public_key']
                    msg['zuhri_id'] = identity['zuhri_id']
        self.send_to_nodes(json.dumps(msg))
        print(f"{GREEN}✅ Auto-response SOS dikirim ke {sender}{RESET}")
    
    # ===== KIRIM PESAN =====
    def send_message(self, text, msg_type='chat'):
        msg = {
            'from': self.name,
            'text': text,
            'time': datetime.now().strftime('%H:%M:%S'),
            'type': msg_type
        }
        
        if ZUHRI_ID_OK and msg_type == 'chat':
            identity = load_identity()
            if identity:
                sig = sign(text)
                if sig:
                    msg['signature'] = sig
                    msg['public_key'] = identity['public_key']
                    msg['zuhri_id'] = identity['zuhri_id']
        
        self.send_to_nodes(json.dumps(msg))
        badge = "✅" if 'signature' in msg else "⚠️"
        print(f"{GOLD}📤 {badge} Pesan terkirim ke {len(self.peers)} node{RESET}")
    
    # ===== VIDEO CALL =====
    def start_video_call(self):
        """Mulai video call"""
        if not self.peers:
            print(f"{RED}❌ Tidak ada peer{RESET}")
            return
        
        print(f"{CYAN}📹 Memulai video call...{RESET}")
        self.video_active = True
        
        # Kirim request
        self.send_message(f"VIDEO CALL dari {self.name}", "video_call")
        
        # Thread kirim frame
        threading.Thread(target=self.send_video_frames, daemon=True).start()
        
        print(f"{GREEN}✅ Video call aktif{RESET}")
        print(f"{DIM}Tekan CTRL+C untuk berhenti{RESET}")
    
    def send_video_frames(self):
        """Kirim frame video via kamera"""
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print(f"{YELLOW}⚠️  Kamera tidak tersedia{RESET}")
                return
            
            while self.video_active:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Resize & compress
                frame = cv2.resize(frame, (320, 240))
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                frame_b64 = base64.b64encode(buffer).decode()
                
                # Kirim
                msg = {
                    'from': self.name,
                    'type': 'video_frame',
                    'frame': frame_b64,
                    'time': datetime.now().strftime('%H:%M:%S')
                }
                self.send_to_nodes(json.dumps(msg))
                
                time.sleep(0.2)  # 5 FPS
            
            cap.release()
        except ImportError:
            print(f"{YELLOW}⚠️  Install: pip install opencv-python{RESET}")
        except Exception as e:
            print(f"{RED}❌ Video error: {e}{RESET}")
    
    def stop_video_call(self):
        """Hentikan video call"""
        self.video_active = False
        print(f"{YELLOW}📹 Video call dihentikan{RESET}")
    
    # ===== VOICE CALL =====
    def start_voice_call(self):
        """Mulai voice call"""
        if not self.peers:
            print(f"{RED}❌ Tidak ada peer{RESET}")
            return
        
        print(f"{CYAN}🎤 Memulai voice call...{RESET}")
        self.voice_active = True
        
        self.send_message(f"VOICE CALL dari {self.name}", "voice_call")
        
        print(f"{GREEN}✅ Voice call aktif{RESET}")
        print(f"{DIM}Tekan CTRL+C untuk berhenti{RESET}")
    
    def stop_voice_call(self):
        """Hentikan voice call"""
        self.voice_active = False
        print(f"{YELLOW}🎤 Voice call dihentikan{RESET}")
    
    # ===== FILE TRANSFER =====
    def send_file(self, filepath):
        """Kirim file"""
        if not os.path.exists(filepath):
            print(f"{RED}❌ File tidak ada{RESET}")
            return
        
        filename = os.path.basename(filepath)
        size = os.path.getsize(filepath)
        
        print(f"{CYAN}📁 Mengirim file: {filename} ({size} bytes){RESET}")
        
        try:
            with open(filepath, 'rb') as f:
                file_data = base64.b64encode(f.read()).decode()
            
            msg = {
                'from': self.name,
                'type': 'file',
                'filename': filename,
                'data': file_data,
                'time': datetime.now().strftime('%H:%M:%S')
            }
            
            self.send_to_nodes(json.dumps(msg))
            print(f"{GREEN}✅ File terkirim ke {len(self.peers)} node{RESET}")
        except Exception as e:
            print(f"{RED}❌ Gagal kirim file: {e}{RESET}")
    
    # ===== KIRIM SOS =====
    def send_sos(self, text="SOS! Saya membutuhkan bantuan!"):
        msg = {
            'from': self.name,
            'text': text,
            'time': datetime.now().strftime('%H:%M:%S'),
            'type': 'sos'
        }
        if ZUHRI_ID_OK:
            identity = load_identity()
            if identity:
                sig = sign(text)
                if sig:
                    msg['signature'] = sig
                    msg['public_key'] = identity['public_key']
                    msg['zuhri_id'] = identity['zuhri_id']
        self.send_to_nodes(json.dumps(msg))
        print(f"\n{RED}🆘 SINYAL SOS DIKIRIM!{RESET}")
    
    # ===== NODE CONNECTED =====
    def on_node_connected(self, node):
        self.peers.append(node)
        print(f"\n{GREEN}🔗 Node terhubung: {node.id} (total: {len(self.peers)}){RESET}")
        self.send_message(f"👋 {self.name} bergabung di P2P-Mesh V2.0!")
    
    # ===== NODE DISCONNECTED =====
    def on_node_disconnected(self, node):
        if node in self.peers:
            self.peers.remove(node)
        print(f"\n{YELLOW}🔌 Node terputus: {node.id} (total: {len(self.peers)}){RESET}")
    
    # ===== SHOW PEERS =====
    def show_peers(self):
        print(f"\n{BOLD}📋 NODE TERHUBUNG:{RESET}")
        if self.peers:
            for i, p in enumerate(self.peers, 1):
                print(f"  {GOLD}{i}.{RESET} {p.id}")
        else:
            print(f"  {DIM}(Belum ada){RESET}")
        print()

# ===== START NODE =====
node = MeshNode(NODE_NAME, HOST, PORT)

def start_node():
    try:
        node.start()
        print(f"{GREEN}✅ Node berjalan di port {PORT}{RESET}\n")
    except Exception as e:
        print(f"{RED}❌ Gagal: {e}{RESET}")

threading.Thread(target=start_node, daemon=True).start()
time.sleep(2)

# ===== INTERFACE =====
print(f"""{BOLD}{CYAN}═══════════════════════════════════════════════════════════════════════════
  📡 P2P-MESH V2.0 — COMMANDS
═══════════════════════════════════════════════════════════════════════════{RESET}

  {GOLD}/connect <ip>{RESET}     → Hubungkan ke node lain
  {GOLD}/msg <pesan>{RESET}      → Kirim pesan (terverifikasi)
  {GOLD}/video{RESET}            → Video call
  {GOLD}/voice{RESET}            → Voice call
  {GOLD}/file <path>{RESET}      → Kirim file
  {GOLD}/sos{RESET}              → Sinyal darurat
  {GOLD}/peers{RESET}            → Lihat node terhubung
  {GOLD}/id{RESET}               → Lihat Zuhri ID
  {GOLD}/help{RESET}             → Bantuan
  {GOLD}/exit{RESET}             → Keluar

{BOLD}{CYAN}═══════════════════════════════════════════════════════════════════════════{RESET}
""")

# ===== MAIN LOOP =====
while True:
    try:
        c = input(f"{GOLD}📡 > {RESET}").strip()
        if not c: continue
        
        if c == "/exit":
            node.video_active = False
            node.voice_active = False
            node.stop()
            print(f"{CYAN}👋 Sampai jumpa!{RESET}")
            break
        
        elif c == "/peers":
            node.show_peers()
        
        elif c == "/id":
            if ZUHRI_ID_OK:
                identity = load_identity()
                if identity:
                    print(f"\n{BOLD}🆔 ZUHRI ID:{RESET}")
                    print(f"  ID: {identity['zuhri_id']}")
                    print(f"  Nama: {identity['name']}\n")
            else:
                print(f"{YELLOW}⚠️  Belum ada Zuhri ID{RESET}\n")
        
        elif c.startswith("/connect "):
            ip = c.split(" ")[1]
            try:
                node.connect_with_node(ip, PORT)
                print(f"🔗 Koneksi ke {ip}:{PORT}...")
            except Exception as e:
                print(f"{RED}❌ {e}{RESET}")
        
        elif c.startswith("/msg "):
            node.send_message(c[5:])
        
        elif c == "/video":
            node.start_video_call()
        
        elif c == "/voice":
            node.start_voice_call()
        
        elif c.startswith("/file "):
            node.send_file(c[6:])
        
        elif c == "/sos":
            text = input("📢 Pesan SOS: ") or "SOS! Butuh bantuan!"
            node.send_sos(text)
        
        elif c == "/help":
            print(f"""
{BOLD}{CYAN}BANTUAN P2P-MESH V2.0:{RESET}
  /connect <ip>   → Hubungkan node
  /msg <pesan>    → Kirim pesan
  /video          → Video call
  /voice          → Voice call
  /file <path>    → Kirim file
  /sos            → Sinyal darurat
  /peers          → Lihat node
  /id             → Lihat Zuhri ID
  /help           → Bantuan
  /exit           → Keluar
""")
        else:
            print(f"{RED}❌ Ketik /help{RESET}")
    
    except KeyboardInterrupt:
        node.video_active = False
        node.voice_active = False
        node.stop()
        break
    except Exception as e:
        print(f"{RED}⚠️ {e}{RESET}")
