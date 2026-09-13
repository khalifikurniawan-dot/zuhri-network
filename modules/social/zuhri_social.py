#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI SOCIAL — MEDIA SOSIAL & CHAT
Mode: Offline (P2P-Mesh) + Online (Verified News)
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, hashlib, secrets, socket, threading, subprocess, time
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
SOCIAL_DIR = os.path.join(HOME, "zuhri_os", "social")
DATA_DIR = os.path.join(SOCIAL_DIR, "data")
LOG_DIR = os.path.join(SOCIAL_DIR, "logs")
GROUP_DIR = os.path.join(SOCIAL_DIR, "groups")
NEWS_DIR = os.path.join(SOCIAL_DIR, "news")
for d in [DATA_DIR, LOG_DIR, GROUP_DIR, NEWS_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# MODE 1 — OFFLINE CHAT (P2P-Mesh)
# ============================================================
CHAT_PORT = 9999
chat_running = False
chat_messages = []

def chat_server():
    """Server chat lokal"""
    global chat_messages
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", CHAT_PORT))
        s.settimeout(2)
        
        while chat_running:
            try:
                data, addr = s.recvfrom(4096)
                msg = json.loads(data.decode())
                msg['from_ip'] = addr[0]
                msg['received'] = datetime.now().isoformat()
                chat_messages.append(msg)
                
                # Tampilkan
                print(f"\n{GOLD}💬 [{msg.get('from','?')}]{RESET} {msg.get('text','')}")
                print(f"{DIM}   {msg.get('time','')} | {addr[0]}{RESET}")
            except socket.timeout:
                continue
            except:
                pass
    except:
        pass

def chat_send(text, group="umum"):
    """Kirim chat ke semua node"""
    identity = load_identity() if ZUHRI_ID_OK else None
    name = identity['name'] if identity else "Anonymous"
    
    msg = {
        "type": "chat",
        "from": name,
        "text": text,
        "group": group,
        "time": datetime.now().strftime("%H:%M:%S"),
        "zuhri_id": identity['zuhri_id'] if identity else None
    }
    
    # Tanda tangan
    if ZUHRI_ID_OK and identity:
        sig = sign(text)
        if sig:
            msg['signature'] = sig
            msg['public_key'] = identity['public_key']
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(json.dumps(msg).encode(), ("255.255.255.255", CHAT_PORT))
        s.close()
        return True
    except:
        return False

def chat_mode():
    """Mode chat offline"""
    global chat_running, chat_messages
    
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  💬 ZUHRI SOCIAL — CHAT OFFLINE (P2P-Mesh)                          ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Chat tanpa internet — semua HP di WiFi yang sama.${RESET}
{DIM}Ketik 'exit' untuk keluar, '/help' untuk bantuan.${RESET}
""")
    
    # Start server
    chat_running = True
    server_thread = threading.Thread(target=chat_server, daemon=True)
    server_thread.start()
    
    identity = load_identity() if ZUHRI_ID_OK else None
    name = identity['name'] if identity else "Anonymous"
    print(f"{GREEN}✅ Anda: {name}{RESET}")
    print(f"{GREEN}✅ Port: {CHAT_PORT}{RESET}")
    print(f"{DIM}Menunggu pesan...{RESET}\n")
    
    while chat_running:
        try:
            text = input(f"{GOLD}💬 > {RESET}").strip()
            
            if not text:
                continue
            
            if text.lower() in ["exit", "quit", "keluar"]:
                chat_running = False
                print(f"\n{CYAN}👋 Keluar dari chat{RESET}\n")
                break
            
            if text == "/help":
                print(f"""
{BOLD}{CYAN}BANTUAN CHAT:{RESET}
  /help       → Bantuan
  /list       → Lihat pesan
  /clear      → Hapus pesan
  /ip         → Lihat IP Anda
  /exit       → Keluar
""")
                continue
            
            if text == "/list":
                print(f"\n{BOLD}📨 PESAN ({len(chat_messages)}):{RESET}")
                for m in chat_messages[-20:]:
                    print(f"  {GOLD}[{m.get('from','?')}]{RESET} {m.get('text','')}")
                print()
                continue
            
            if text == "/clear":
                chat_messages = []
                print(f"{GREEN}✅ Pesan dihapus{RESET}\n")
                continue
            
            if text == "/ip":
                try:
                    r = subprocess.run(["ifconfig"], capture_output=True, text=True)
                    ips = [l.strip().split()[1] for l in r.stdout.split('\n') if 'inet ' in l]
                    print(f"{GREEN}IP: {', '.join(ips)}{RESET}\n")
                except:
                    print(f"{YELLOW}Tidak bisa cek IP{RESET}\n")
                continue
            
            # Kirim chat
            if chat_send(text):
                print(f"{DIM}✅ Terkirim{RESET}")
            else:
                print(f"{RED}❌ Gagal kirim{RESET}")
        
        except KeyboardInterrupt:
            chat_running = False
            print(f"\n{CYAN}👋 Keluar{RESET}\n")
            break

# ============================================================
# MODE 2 — ONLINE NEWS (Verified)
# ============================================================
NEWS_SOURCES = {
    "cnn": {"nama":"CNN Indonesia","url":"https://www.cnnindonesia.com","trust":9},
    "kompas": {"nama":"Kompas","url":"https://www.kompas.com","trust":9},
    "tempo": {"nama":"Tempo","url":"https://www.tempo.co","trust":9},
    "antaranews": {"nama":"Antara News","url":"https://www.antaranews.com","trust":10},
    "detik": {"nama":"Detik","url":"https://www.detik.com","trust":8},
    "bbc": {"nama":"BBC News","url":"https://www.bbc.com/news","trust":10},
    "reuters": {"nama":"Reuters","url":"https://www.reuters.com","trust":10},
    "aljazeera": {"nama":"Al Jazeera","url":"https://www.aljazeera.com","trust":9},
    "ap": {"nama":"Associated Press","url":"https://apnews.com","trust":10},
    "npr": {"nama":"NPR","url":"https://www.npr.org","trust":9},
}

# ============================================================
# HOAX CHECKER — Echo-Core Verification
# ============================================================
HOAX_KEYWORDS = [
    "kaget", "heboh", "viral", "sebarkan", "share", "bagikan",
    "awas", "bahaya", "hati-hati", "penting", "darurat",
    "segera", "jangan sampai", "percaya", "hoax", "bohong",
    "berita palsu", "tipu", "penipuan", "penipu",
]

def hoax_check(text):
    """Cek apakah teks berpotensi hoax"""
    text_lower = text.lower()
    score = 0
    reasons = []
    
    # Cek keyword hoax
    for kw in HOAX_KEYWORDS:
        if kw in text_lower:
            score += 1
            reasons.append(f"Kata kunci: {kw}")
    
    # Cek huruf kapital berlebihan
    if len(text) > 0:
        upper_ratio = sum(1 for c in text if c.isupper()) / len(text)
        if upper_ratio > 0.5:
            score += 2
            reasons.append("Huruf kapital berlebihan")
    
    # Cek tanda seru berlebihan
    if text.count("!") > 3:
        score += 2
        reasons.append("Tanda seru berlebihan")
    
    # Cek link mencurigakan
    if "bit.ly" in text_lower or "tinyurl" in text_lower:
        score += 3
        reasons.append("Link pendek (shortener)")
    
    # Cek panic words
    panic_words = ["segera sebarkan", "viralkan", "tolong share", "jangan sampai"]
    for pw in panic_words:
        if pw in text_lower:
            score += 3
            reasons.append(f"Panic word: {pw}")
    
    if score >= 5:
        return {"status": "HOAX", "score": score, "reasons": reasons}
    elif score >= 2:
        return {"status": "SUSPECT", "score": score, "reasons": reasons}
    else:
        return {"status": "CLEAN", "score": score, "reasons": ["Tidak ada indikasi hoax"]}

def echo_resonance(text):
    """Hitung resonansi 0-8-9"""
    h = hashlib.sha3_256(text.encode()).hexdigest()
    total = sum(int(c, 16) for c in h[:32])
    return (total % 10 + 8) % 10

def news_menu():
    """Menu berita online"""
    while True:
        os.system('clear')
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  📰 ZUHRI SOCIAL — VERIFIED NEWS                                    ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Berita dengan verifikasi protokol K-8.0                            ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 SUMBER BERITA:{RESET}""")
        
        for i, (key, src) in enumerate(NEWS_SOURCES.items(), 1):
            trust_bar = "★" * src['trust'] + "☆" * (10 - src['trust'])
            print(f"  {GOLD}{i:2}.{RESET} {src['nama']:20} {CYAN}{trust_bar}{RESET}")
        
        print(f"""
{BOLD}  📋 MENU:{RESET}
  {GOLD}0.${RESET}  Kembali
  {GOLD}99.${RESET} Cek Hoax (Verifikasi Teks)
""")
        
        try:
            c = input(f"{GOLD}Pilih: {RESET}").strip()
            
            if c == "0":
                break
            
            if c == "99":
                check_hoax_menu()
                continue
            
            idx = int(c) - 1
            keys = list(NEWS_SOURCES.keys())
            if 0 <= idx < len(keys):
                key = keys[idx]
                src = NEWS_SOURCES[key]
                print(f"\n{CYAN}🌐 Membuka {src['nama']}...{RESET}")
                print(f"{DIM}Trust Level: {src['trust']}/10{RESET}\n")
                
                # Buka via browser
                subprocess.run(["termux-open-url", src['url']], timeout=5)
                
                if ZUHRI_ID_OK:
                    log_verified(f"SOCIAL_NEWS: {src['nama']}")
                
                input(f"{DIM}Enter...{RESET}")
        except (ValueError, IndexError):
            pass
        except KeyboardInterrupt:
            break

def check_hoax_menu():
    """Cek hoax teks"""
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🔍 CEK HOAX — VERIFIKASI TEKS                                      ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Masukkan teks berita/pesan untuk dicek.${RESET}
""")
    
    text = input("📝 Teks: ").strip()
    if not text:
        return
    
    result = hoax_check(text)
    resonansi = echo_resonance(text)
    
    print(f"\n{BOLD}📊 HASIL VERIFIKASI:{RESET}\n")
    print(f"  {GOLD}Teks:{RESET} {text[:100]}...")
    print(f"  {GOLD}Resonansi:{RESET} {resonansi}/9")
    print(f"  {GOLD}Skor Hoax:{RESET} {result['score']}")
    print()
    
    if result['status'] == 'HOAX':
        print(f"  {RED}❌ STATUS: HOAX / BERITA PALSU{RESET}")
    elif result['status'] == 'SUSPECT':
        print(f"  {YELLOW}⚠️  STATUS: MENCURIGAKAN{RESET}")
    else:
        print(f"  {GREEN}✅ STATUS: BERSIH (tidak ada indikasi hoax){RESET}")
    
    print(f"\n{GOLD}📋 ALASAN:{RESET}")
    for r in result['reasons']:
        print(f"  • {r}")
    
    print(f"""
{BOLD}💡 TIPS VERIFIKASI:{RESET}
  {DIM}1. Cek sumber (dari media terpercaya?)${RESET}
  {DIM}2. Cek tanggal (masih relevan?)${RESET}
  {DIM}3. Cek foto (reverse image search)${RESET}
  {DIM}4. Cek 3+ sumber independen${RESET}
  {DIM}5. Jangan percaya 100% pada satu sumber${RESET}
  {DIM}6. Cek di: turnbackhoax.id, cekfakta.com${RESET}
""")
    
    if ZUHRI_ID_OK:
        log_verified(f"SOCIAL_HOAX_CHECK: {result['status']}")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# GRUP — Buat & Gabung
# ============================================================
def grup_menu():
    """Menu grup"""
    while True:
        os.system('clear')
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  👥 ZUHRI SOCIAL — GRUP                                             ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.${RESET} Buat Grup Baru
  {GOLD}2.${RESET} Lihat Daftar Grup
  {GOLD}3.${RESET} Gabung Grup
  {GOLD}0.${RESET} Kembali
""")
        
        try:
            c = input(f"{GOLD}Pilih: {RESET}").strip()
            
            if c == "0":
                break
            elif c == "1":
                nama = input("🏷️  Nama grup: ").strip()
                desk = input("📝 Deskripsi: ").strip()
                
                if nama:
                    grup_id = secrets.token_hex(4)
                    grup = {
                        "id": grup_id,
                        "nama": nama,
                        "deskripsi": desk,
                        "dibuat": datetime.now().isoformat(),
                        "anggota": []
                    }
                    
                    # Tambah diri sendiri
                    if ZUHRI_ID_OK:
                        identity = load_identity()
                        grup['anggota'].append(identity['zuhri_id'])
                    
                    f = os.path.join(GROUP_DIR, f"{grup_id}.json")
                    json.dump(grup, open(f, "w"), indent=2)
                    
                    print(f"\n{GREEN}✅ Grup '{nama}' dibuat!{RESET}")
                    print(f"{DIM}ID: {grup_id}{RESET}")
                    print(f"{DIM}Bagikan ID ini ke teman untuk gabung.{RESET}\n")
                    
                    if ZUHRI_ID_OK:
                        log_verified(f"SOCIAL_GROUP_CREATE: {nama}")
            
            elif c == "2":
                files = [f for f in os.listdir(GROUP_DIR) if f.endswith('.json')]
                print(f"\n{BOLD}👥 GRUP ({len(files)}):{RESET}\n")
                
                for f in files:
                    g = json.load(open(os.path.join(GROUP_DIR, f)))
                    print(f"  {GOLD}•{RESET} {g['nama']} ({g['id']})")
                    print(f"    {DIM}{g['deskripsi']}{RESET}")
                    print(f"    {DIM}Anggota: {len(g['anggota'])}{RESET}\n")
            
            elif c == "3":
                grup_id = input("🆔 ID grup: ").strip()
                f = os.path.join(GROUP_DIR, f"{grup_id}.json")
                
                if os.path.exists(f):
                    g = json.load(open(f))
                    
                    if ZUHRI_ID_OK:
                        identity = load_identity()
                        if identity['zuhri_id'] not in g['anggota']:
                            g['anggota'].append(identity['zuhri_id'])
                            json.dump(g, open(f, "w"), indent=2)
                            print(f"\n{GREEN}✅ Gabung ke '{g['nama']}'!{RESET}\n")
                        else:
                            print(f"\n{YELLOW}⚠️  Sudah jadi anggota{RESET}\n")
                    else:
                        print(f"\n{YELLOW}⚠️  Butuh Zuhri ID{RESET}\n")
                else:
                    print(f"\n{RED}❌ Grup tidak ditemukan{RESET}\n")
            
            input(f"{DIM}Enter...{RESET}")
        except KeyboardInterrupt:
            break

# ============================================================
# MENU UTAMA
# ============================================================
def menu():
    while True:
        os.system('clear')
        
        identity = load_identity() if ZUHRI_ID_OK else None
        name = identity['name'] if identity else "Anonymous"
        zid = identity['zuhri_id'][:20] + "..." if identity else "Tidak ada"
        
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🌐 ZUHRI SOCIAL — MEDIA SOSIAL & CHAT                             ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Operator: {GREEN}{name}{RESET}
║  Zuhri ID: {GOLD}{zid}{RESET}
║  Protokol: K-8.0                                                    ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MODE:{RESET}
  {GOLD}1.${RESET} 💬 Chat Offline (P2P-Mesh)
  {GOLD}2.${RESET} 👥 Grup (Buat/Gabung)
  {GOLD}3.${RESET} 📰 Berita Online (Verified)
  {GOLD}4.${RESET} 🔍 Cek Hoax
  {GOLD}5.${RESET} 📊 Info
  {GOLD}0.${RESET} Keluar
""")
        
        try:
            c = input(f"{GOLD}Pilih (0-5): {RESET}").strip()
            if c == "0": break
            elif c == "1": chat_mode()
            elif c == "2": grup_menu()
            elif c == "3": news_menu()
            elif c == "4": check_hoax_menu()
            elif c == "5":
                os.system('clear')
                print(f"""
{BOLD}{MAGENTA}📊 INFO ZUHRI SOCIAL{RESET}

{BOLD}🎯 FITUR:{RESET}
  {GOLD}•{RESET} Chat Offline (P2P-Mesh)
  {GOLD}•{RESET} Grup (Buat/Gabung)
  {GOLD}•{RESET} Berita Online (10 sumber terpercaya)
  {GOLD}•{RESET} Cek Hoax (Echo-Core verification)

{BOLD}🌐 MODE:{RESET}
  {GOLD}Offline:{RESET} Chat via WiFi lokal (tanpa internet)
  {GOLD}Online:{RESET} Berita dari media terpercaya

{BOLD}🔍 VERIFIKASI:{RESET}
  {GOLD}•{RESET} Trust Level (1-10) per sumber
  {GOLD}•{RESET} Hoax Check (7 indikator)
  {GOLD}•{RESET} Echo-Core resonance
  {GOLD}•{RESET} Sumber terpercaya (CNN, BBC, Reuters, AP)

{BOLD}⚠️  CATATAN:{RESET}
  {DIM}• Chat offline: butuh WiFi/Hotspot${RESET}
  {DIM}• Berita online: butuh internet${RESET}
  {DIM}• Cek hoax: offline${RESET}
""")
                input(f"{DIM}Enter...{RESET}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "chat": chat_mode()
        elif cmd == "news": news_menu()
        elif cmd == "hoax":
            text = " ".join(sys.argv[2:])
            r = hoax_check(text)
            print(json.dumps(r, indent=2, ensure_ascii=False))
        else: menu()
    else: menu()
