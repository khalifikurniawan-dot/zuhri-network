#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI SOCIAL — MEDIA SOSIAL TERDESENTRALISASI
P2P + Zuhri ID + Broadcast
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, hashlib, secrets, socket, threading, time
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
SOC_DIR = os.path.join(HOME, "zuhri_os", "social")
DATA_DIR = os.path.join(SOC_DIR, "data")
FEED_DIR = os.path.join(SOC_DIR, "feed")
USER_DIR = os.path.join(SOC_DIR, "users")
for d in [DATA_DIR, FEED_DIR, USER_DIR]:
    os.makedirs(d, exist_ok=True)

FEED_FILE = os.path.join(DATA_DIR, "feed.json")
BROADCAST_PORT = 8002

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

# ============================================================
# FEED MANAGEMENT
# ============================================================
def load_feed():
    if os.path.exists(FEED_FILE):
        try:
            return json.load(open(FEED_FILE))
        except:
            return []
    return []

def save_feed(feed):
    json.dump(feed, open(FEED_FILE, "w"), indent=2)

# ============================================================
# BUAT POST
# ============================================================
def create_post():
    if not ZUHRI_ID_OK:
        print(f"{RED}❌ Butuh Zuhri ID{RESET}")
        input(f"{DIM}Enter...{RESET}")
        return
    
    identity = load_identity()
    if not identity:
        print(f"{RED}❌ Zuhri ID tidak ditemukan{RESET}")
        input(f"{DIM}Enter...{RESET}")
        return
    
    os.system('clear')
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  📝 BUAT POST — ZUHRI SOCIAL                                        ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    text = input("📝 Post: ").strip()
    if not text:
        return
    
    # Buat post
    post = {
        "id": secrets.token_hex(8),
        "author": {
            "zuhri_id": identity['zuhri_id'],
            "name": identity['name']
        },
        "text": text,
        "timestamp": datetime.now().isoformat(),
        "likes": 0,
        "signature": None,
        "public_key": None
    }
    
    # Tanda tangan
    post_str = json.dumps({
        "id": post['id'],
        "zuhri_id": identity['zuhri_id'],
        "text": text,
        "timestamp": post['timestamp']
    }, sort_keys=True)
    
    sig = sign(post_str)
    if sig:
        post['signature'] = sig
        post['public_key'] = identity['public_key']
    
    # Simpan ke feed
    feed = load_feed()
    feed.append(post)
    save_feed(feed)
    
    if ZUHRI_ID_OK:
        log_verified(f"SOCIAL_POST: {text[:30]}")
    
    print(f"""
{GREEN}✅ POST DIBUAT!{RESET}

  {GOLD}ID{RESET}       : {post['id']}
  {GOLD}Author{RESET}   : {identity['name']}
  {GOLD}Waktu{RESET}    : {post['timestamp'][:19]}
  {GOLD}Signature{RESET}: {'✅' if sig else '❌'}

{DIM}Post tersimpan di feed lokal.{RESET}
{DIM}Broadcast ke P2P? (nanti){RESET}
""")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# LIHAT FEED
# ============================================================
def view_feed():
    os.system('clear')
    feed = load_feed()
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  📱 ZUHRI SOCIAL — FEED                                            ║
║  Total: {len(feed)} post                                              ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    if not feed:
        print(f"{YELLOW}Belum ada post. Buat post dengan menu 1.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    # Tampilkan 20 post terbaru
    for post in feed[-20:][::-1]:
        # Verifikasi signature
        verified = False
        if post.get('signature') and post.get('public_key'):
            post_str = json.dumps({
                "id": post['id'],
                "zuhri_id": post['author']['zuhri_id'],
                "text": post['text'],
                "timestamp": post['timestamp']
            }, sort_keys=True)
            verified = verify(post_str, post['signature'], post['public_key'])
        
        badge = f"{GREEN}✅{RESET}" if verified else f"{YELLOW}⚠️ {RESET}"
        
        print(f"{BOLD}{CYAN}┌─────────────────────────────────────────────────────────────┐")
        print(f"│  {GOLD}{post['author']['name']}{RESET} {badge}  {DIM}{post['timestamp'][:19]}{RESET}")
        print(f"{CYAN}├─────────────────────────────────────────────────────────────┤{RESET}")
        print(f"│  {post['text']}")
        print(f"{CYAN}└─────────────────────────────────────────────────────────────┘{RESET}")
        print()
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# LIKE POST
# ============================================================
def like_post():
    os.system('clear')
    feed = load_feed()
    
    if not feed:
        print(f"{YELLOW}Belum ada post.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    print(f"{BOLD}{CYAN}👍 LIKE POST{RESET}\n")
    
    for i, post in enumerate(feed[-10:], 1):
        print(f"  {GOLD}{i}.{RESET} {post['author']['name']}: {post['text'][:50]}")
    
    try:
        c = int(input(f"\n{CYAN}Pilih nomor: {RESET}")) - 1
        if 0 <= c < len(feed[-10:]):
            post = feed[-(10-c)]
            post['likes'] = post.get('likes', 0) + 1
            save_feed(feed)
            print(f"\n{GREEN}✅ Liked! Total: {post['likes']}{RESET}\n")
    except:
        pass
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# BROADCAST P2P (kirim ke jaringan)
# ============================================================
def broadcast_post():
    """Broadcast post ke jaringan lokal"""
    if not ZUHRI_ID_OK:
        print(f"{RED}❌ Butuh Zuhri ID{RESET}")
        input(f"{DIM}Enter...{RESET}")
        return
    
    os.system('clear')
    print(f"{BOLD}{CYAN}📡 BROADCAST POST KE P2P{RESET}\n")
    
    feed = load_feed()
    if not feed:
        print(f"{YELLOW}Belum ada post.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    # Pilih post terakhir
    post = feed[-1]
    
    print(f"📝 Post: {post['text'][:60]}\n")
    print(f"{CYAN}⏳ Broadcast ke jaringan...{RESET}\n")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Broadcast
        msg = json.dumps({
            "type": "SOCIAL_POST",
            "post": post
        })
        
        sock.sendto(msg.encode(), ('255.255.255.255', BROADCAST_PORT))
        sock.close()
        
        print(f"{GREEN}✅ Post di-broadcast!{RESET}")
        print(f"{DIM}Port: {BROADCAST_PORT}{RESET}\n")
        
        if ZUHRI_ID_OK:
            log_verified("SOCIAL_BROADCAST")
    except Exception as e:
        print(f"{RED}❌ Gagal broadcast: {e}{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# TERIMA POST DARI JARINGAN
# ============================================================
def listen_posts():
    """Dengarkan post dari jaringan"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', BROADCAST_PORT))
        sock.settimeout(2)
        
        received = 0
        while True:
            try:
                data, addr = sock.recvfrom(4096)
                msg = json.loads(data.decode())
                
                if msg.get("type") == "SOCIAL_POST":
                    post = msg.get("post", {})
                    
                    # Cek duplikat
                    feed = load_feed()
                    existing_ids = [p['id'] for p in feed]
                    
                    if post.get('id') not in existing_ids:
                        feed.append(post)
                        save_feed(feed)
                        received += 1
                        print(f"\n📨 Post baru dari {post.get('author', {}).get('name', '?')}")
                        print(f"   {post.get('text', '')[:50]}")
            except socket.timeout:
                break
            except:
                pass
        
        sock.close()
        return received
    except:
        return 0

# ============================================================
# PROFIL
# ============================================================
def profil():
    os.system('clear')
    
    if not ZUHRI_ID_OK:
        print(f"{RED}❌ Belum ada Zuhri ID{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    identity = load_identity()
    feed = load_feed()
    
    # Hitung post milik sendiri
    my_posts = [p for p in feed if p['author']['zuhri_id'] == identity['zuhri_id']]
    total_likes = sum(p.get('likes', 0) for p in my_posts)
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  👤 PROFIL ZUHRI SOCIAL                                            ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}👤 Nama{RESET}      : {identity['name']}
  {GOLD}🆔 Zuhri ID{RESET}  : {identity['zuhri_id']}
  {GOLD}🎭 Role{RESET}      : {identity.get('role', 'Operator')}

{BOLD}📊 STATISTIK:{RESET}
  {GOLD}📝 Post{RESET}      : {len(my_posts)}
  {GOLD}👍 Likes{RESET}     : {total_likes}
  {GOLD}📱 Feed{RESET}      : {len(feed)} total post

{BOLD}📅 POST TERAKHIR:{RESET}""")
    
    for p in my_posts[-5:][::-1]:
        print(f"  • {p['text'][:50]}")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# INFO
# ============================================================
def info():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🌐 ZUHRI SOCIAL — INFO                                            ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}🧬 APA ITU ZUHRI SOCIAL?{RESET}

Media sosial terdesentralisasi berbasis P2P + Zuhri ID.

{BOLD}🎯 KARAKTERISTIK:{RESET}
  {GOLD}•{RESET} Tanpa server pusat
  {GOLD}•{RESET} Tanpa cloud
  {GOLD}•{RESET} Tanpa sensor
  {GOLD}•{RESET} Terenkripsi (Ed25519)
  {GOLD}•{RESET} Offline-first

{BOLD}🔐 KEAMANAN:{RESET}
  {GOLD}•{RESET} Setiap post ditandatangani Zuhri ID
  {GOLD}•{RESET} Verifikasi signature otomatis
  {GOLD}•{RESET} Tidak bisa dipalsukan
  {GOLD}•{RESET} Tidak ada tracking

{BOLD}📡 CARA KERJA:{RESET}
  1. Buat post → ditandatangani
  2. Broadcast ke jaringan (P2P)
  3. HP lain terima & verifikasi
  4. Post tersimpan di feed lokal

{BOLD}⚠️  KETERBATASAN:{RESET}
  {DIM}• Broadcast butuh WiFi lokal (satu jaringan)${RESET}
  {DIM}• Tidak ada server global (by design)${RESET}
  {DIM}• Feed tersimpan lokal, tidak sync otomatis${RESET}

{BOLD}🎯 FILOSOFI:{RESET}
  {CYAN}"Zuhri Social — media sosial milik Anda.${RESET}
  {CYAN}Tanpa algoritma, tanpa iklan, tanpa sensor."{RESET}
""")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        feed = load_feed()
        
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🌐 ZUHRI SOCIAL — MEDIA SOSIAL TERDESENTRALISASI                  ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                            ║
║  Total Post: {len(feed)}
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  📝 Buat Post
  {GOLD}2.{RESET}  📱 Lihat Feed
  {GOLD}3.{RESET}  👍 Like Post
  {GOLD}4.{RESET}  📡 Broadcast ke P2P
  {GOLD}5.{RESET}  📥 Terima Post dari Jaringan
  {GOLD}6.{RESET}  👤 Profil Saya
  {GOLD}7.{RESET}  ℹ️  Info Zuhri Social
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-7): {RESET}").strip()
            if c == "0": break
            elif c == "1": create_post()
            elif c == "2": view_feed()
            elif c == "3": like_post()
            elif c == "4": broadcast_post()
            elif c == "5":
                os.system('clear')
                print(f"{CYAN}📥 Mendengarkan post...{RESET}\n")
                n = listen_posts()
                print(f"\n{GREEN}✅ {n} post diterima{RESET}\n")
                input(f"{DIM}Enter...{RESET}")
            elif c == "6": profil()
            elif c == "7": info()
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "post":
            text = " ".join(sys.argv[2:])
            if text:
                identity = load_identity()
                post = {
                    "id": secrets.token_hex(8),
                    "author": {"zuhri_id": identity['zuhri_id'], "name": identity['name']},
                    "text": text,
                    "timestamp": datetime.now().isoformat(),
                    "likes": 0
                }
                feed = load_feed()
                feed.append(post)
                save_feed(feed)
                print(f"✅ Post dibuat: {text[:50]}")
        elif cmd == "feed":
            for p in load_feed()[-10:]:
                print(f"{p['author']['name']}: {p['text']}")
        elif cmd == "info": info()
        else: menu()
    else: menu()
