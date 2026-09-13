#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI LOGIN — AUTENTIKASI TANPA PASSWORD
Challenge-Response dengan Zuhri ID (Ed25519)
"""

import os
import sys
import json
import base64
import secrets
import time
import subprocess
from datetime import datetime, timedelta

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.backends import default_backend
    CRYPTO_OK = True
except ImportError:
    CRYPTO_OK = False

HOME = os.path.expanduser("~")
ID_DIR = os.path.join(HOME, "zuhri_os", "id")
ID_FILE = os.path.join(ID_DIR, "identity.json")
KEY_FILE = os.path.join(ID_DIR, "identity.key")
SESSION_DIR = os.path.join(HOME, "zuhri_os", "sessions")
os.makedirs(SESSION_DIR, exist_ok=True)

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

# ============================================================
# UTIL
# ============================================================
def load_identity():
    if not os.path.exists(ID_FILE):
        return None
    with open(ID_FILE) as f:
        return json.load(f)

def load_private_key():
    if not os.path.exists(KEY_FILE):
        return None
    with open(KEY_FILE) as f:
        priv_b64 = json.load(f)['private_key']
    return ed25519.Ed25519PrivateKey.from_private_bytes(base64.b64decode(priv_b64))

def sign(text):
    priv = load_private_key()
    if not priv:
        return None
    return base64.b64encode(priv.sign(text.encode())).decode()

def verify_signature(text, sig_b64, pub_b64):
    try:
        pub = ed25519.Ed25519PublicKey.from_public_bytes(base64.b64decode(pub_b64))
        pub.verify(base64.b64decode(sig_b64), text.encode())
        return True
    except:
        return False

# ============================================================
# SERVER SIDE — CHALLENGE
# ============================================================
def create_challenge(zuhri_id):
    """Server buat challenge random"""
    challenge = secrets.token_hex(32)  # 64 char random
    expire = (datetime.now() + timedelta(minutes=5)).isoformat()
    
    challenge_data = {
        "challenge": challenge,
        "zuhri_id": zuhri_id,
        "created": datetime.now().isoformat(),
        "expire": expire,
        "used": False
    }
    
    challenge_file = os.path.join(SESSION_DIR, f"challenge_{zuhri_id}.json")
    with open(challenge_file, "w") as f:
        json.dump(challenge_data, f, indent=2)
    
    return challenge

def verify_login(zuhri_id, signature_b64, public_key_b64):
    """Server verifikasi login"""
    challenge_file = os.path.join(SESSION_DIR, f"challenge_{zuhri_id}.json")
    
    if not os.path.exists(challenge_file):
        return False, "Challenge tidak ditemukan"
    
    with open(challenge_file) as f:
        data = json.load(f)
    
    # Cek expire
    expire = datetime.fromisoformat(data['expire'])
    if datetime.now() > expire:
        return False, "Challenge kadaluarsa"
    
    # Cek sudah dipakai
    if data.get('used'):
        return False, "Challenge sudah dipakai"
    
    # Verifikasi signature
    if not verify_signature(data['challenge'], signature_b64, public_key_b64):
        return False, "Tanda tangan tidak valid"
    
    # Tandai sudah dipakai
    data['used'] = True
    with open(challenge_file, "w") as f:
        json.dump(data, f, indent=2)
    
    # Buat session token
    session_token = secrets.token_hex(32)
    session_data = {
        "zuhri_id": zuhri_id,
        "token": session_token,
        "login_time": datetime.now().isoformat(),
        "expire": (datetime.now() + timedelta(hours=24)).isoformat()
    }
    
    session_file = os.path.join(SESSION_DIR, f"session_{session_token}.json")
    with open(session_file, "w") as f:
        json.dump(session_data, f, indent=2)
    
    return True, session_token

# ============================================================
# CLIENT SIDE — LOGIN
# ============================================================
def do_login():
    """Login tanpa password"""
    identity = load_identity()
    if not identity:
        print(f"{RED}❌ Belum ada Zuhri ID. Jalankan: id create{RESET}")
        return
    
    print(f"""
{BOLD}{CYAN}🔐 ZUHRI LOGIN — TANPA PASSWORD{RESET}
{'─' * 50}
  Zuhri ID : {GOLD}{identity['zuhri_id']}{RESET}
  Nama     : {GOLD}{identity['name']}{RESET}
{'─' * 50}
""")
    
    # 1. Server buat challenge
    print(f"{CYAN}[1/3] Server membuat challenge...{RESET}")
    challenge = create_challenge(identity['zuhri_id'])
    print(f"      Challenge: {DIM}{challenge[:32]}...{RESET}")
    
    # 2. Client sign challenge
    print(f"{CYAN}[2/3] Menandatangani challenge...{RESET}")
    signature = sign(challenge)
    if not signature:
        print(f"{RED}❌ Gagal tanda tangan{RESET}")
        return
    print(f"      Signature: {DIM}{signature[:32]}...{RESET}")
    
    # 3. Server verifikasi
    print(f"{CYAN}[3/3] Server verifikasi...{RESET}")
    success, result = verify_login(identity['zuhri_id'], signature, identity['public_key'])
    
    if success:
        print(f"""
{BOLD}{GREEN}✅ LOGIN BERHASIL!{RESET}

{GOLD}🔑 Session Token:{RESET}
   {result}

{GOLD}⏰ Berlaku:{RESET} 24 jam
{GOLD}🆔 Zuhri ID:{RESET} {identity['zuhri_id']}
""")
        # Simpan token untuk sesi
        with open(os.path.join(SESSION_DIR, "current_token.txt"), "w") as f:
            f.write(result)
    else:
        print(f"{RED}❌ LOGIN GAGAL: {result}{RESET}")

def check_session():
    """Cek apakah masih login"""
    token_file = os.path.join(SESSION_DIR, "current_token.txt")
    if not os.path.exists(token_file):
        print(f"{YELLOW}⚠️  Belum login{RESET}")
        return False
    
    with open(token_file) as f:
        token = f.read().strip()
    
    session_file = os.path.join(SESSION_DIR, f"session_{token}.json")
    if not os.path.exists(session_file):
        print(f"{RED}❌ Session tidak valid{RESET}")
        return False
    
    with open(session_file) as f:
        session = json.load(f)
    
    expire = datetime.fromisoformat(session['expire'])
    if datetime.now() > expire:
        print(f"{RED}❌ Session kadaluarsa{RESET}")
        return False
    
    identity = load_identity()
    print(f"""
{BOLD}{GREEN}✅ SESSION AKTIF{RESET}
{'─' * 50}
  Zuhri ID : {GOLD}{session['zuhri_id']}{RESET}
  Nama     : {GOLD}{identity['name'] if identity else 'N/A'}{RESET}
  Login    : {GOLD}{session['login_time'][:19]}{RESET}
  Expire   : {GOLD}{session['expire'][:19]}{RESET}
{'─' * 50}
""")
    return True

def do_logout():
    """Logout — hapus session"""
    token_file = os.path.join(SESSION_DIR, "current_token.txt")
    if os.path.exists(token_file):
        with open(token_file) as f:
            token = f.read().strip()
        
        session_file = os.path.join(SESSION_DIR, f"session_{token}.json")
        if os.path.exists(session_file):
            os.remove(session_file)
        
        os.remove(token_file)
        print(f"{GREEN}✅ Logout berhasil{RESET}")
    else:
        print(f"{YELLOW}⚠️  Belum login{RESET}")

def protected_action():
    """Contoh aksi yang butuh login"""
    if not check_session():
        print(f"{RED}❌ Akses ditolak — login dulu: id login{RESET}")
        return
    
    print(f"{GREEN}✅ Akses diberikan!{RESET}")
    print(f"{DIM}Ini adalah aksi yang dilindungi Zuhri Login.{RESET}\n")

def show_help():
    print(f"""
{BOLD}{CYAN}🔐 ZUHRI LOGIN — BANTUAN{RESET}
{'─' * 50}
  {BOLD}id login{RESET}        → Login tanpa password
  {BOLD}id session{RESET}      → Cek session aktif
  {BOLD}id logout{RESET}       → Logout
  {BOLD}id protected{RESET}    → Test aksi terproteksi
  {BOLD}id help{RESET}         → Bantuan
{'─' * 50}
""")

if __name__ == "__main__":
    if not CRYPTO_OK:
        print(f"{RED}❌ Install: pip install cryptography{RESET}")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "login":
        do_login()
    elif cmd == "session":
        check_session()
    elif cmd == "logout":
        do_logout()
    elif cmd == "protected":
        protected_action()
    elif cmd == "help":
        show_help()
    else:
        show_help()
