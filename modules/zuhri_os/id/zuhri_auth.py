#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI AUTH — MODUL AUTENTIKASI TERPUSAT
Dipakai semua modul Zuhri Network untuk verifikasi Zuhri ID
"""

import os
import sys
import json
import base64
from datetime import datetime

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

# ===== WARNA =====
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
GOLD = "\033[93m"

# ============================================================
# CORE FUNCTIONS
# ============================================================
def load_identity():
    """Load identitas Zuhri ID"""
    if not os.path.exists(ID_FILE):
        return None
    try:
        with open(ID_FILE) as f:
            return json.load(f)
    except:
        return None

def load_private_key():
    """Load private key Ed25519"""
    if not os.path.exists(KEY_FILE):
        return None
    try:
        with open(KEY_FILE) as f:
            priv_b64 = json.load(f)['private_key']
        return ed25519.Ed25519PrivateKey.from_private_bytes(base64.b64decode(priv_b64))
    except:
        return None

def sign(text):
    """Tanda tangani teks dengan private key"""
    if not CRYPTO_OK:
        return None
    priv = load_private_key()
    if not priv:
        return None
    try:
        return base64.b64encode(priv.sign(text.encode())).decode()
    except:
        return None

def verify(text, sig_b64, pub_b64):
    """Verifikasi tanda tangan"""
    if not CRYPTO_OK:
        return False
    try:
        pub = ed25519.Ed25519PublicKey.from_public_bytes(base64.b64decode(pub_b64))
        pub.verify(base64.b64decode(sig_b64), text.encode())
        return True
    except:
        return False

# ============================================================
# SECURE MESSAGE
# ============================================================
def secure_package(text, msg_type="chat"):
    """Buat paket pesan terverifikasi"""
    identity = load_identity()
    if not identity:
        return None
    
    signature = sign(text)
    if not signature:
        return None
    
    return {
        "type": msg_type,
        "text": text,
        "from": identity['name'],
        "zuhri_id": identity['zuhri_id'],
        "public_key": identity['public_key'],
        "signature": signature,
        "time": datetime.now().strftime('%H:%M:%S'),
        "verified": True
    }

def process_package(data):
    """Proses paket masuk, verifikasi tanda tangan"""
    try:
        if isinstance(data, str):
            msg = json.loads(data)
        else:
            msg = data
    except:
        return None
    
    if "signature" in msg and "public_key" in msg and "text" in msg:
        valid = verify(msg['text'], msg['signature'], msg['public_key'])
        msg['verified'] = valid
        if not valid:
            msg['warning'] = "⚠️  TANDA TANGAN TIDAK VALID — KEMUNGKINAN IMPERSONASI!"
        return msg
    
    msg['verified'] = False
    msg['warning'] = "⚠️  Pesan tanpa Zuhri ID"
    return msg

# ============================================================
# VERIFIED LOGGER
# ============================================================
def log_verified(action, status="OK"):
    """Catat aksi terverifikasi ke log"""
    identity = load_identity()
    log_dir = os.path.join(HOME, "zuhri_os", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "verified.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    zuhri_id = identity['zuhri_id'] if identity else "ANONYMOUS"
    
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] [{status}] [{zuhri_id}] {action}\n")

# ============================================================
# STATUS CHECKER
# ============================================================
def get_status():
    """Cek status Zuhri ID"""
    identity = load_identity()
    if not identity:
        return {
            "active": False,
            "zuhri_id": None,
            "name": None,
            "message": "❌ Zuhri ID belum dibuat"
        }
    
    return {
        "active": True,
        "zuhri_id": identity['zuhri_id'],
        "name": identity['name'],
        "role": identity.get('role', 'Operator'),
        "message": "✅ Zuhri ID aktif"
    }

# ============================================================
# TEST
# ============================================================
if __name__ == "__main__":
    status = get_status()
    
    print(f"""
{BOLD}{CYAN}🆔 ZUHRI AUTH — MODUL TERPUSAT{RESET}
{'─' * 55}
  Status   : {status['message']}
""")
    
    if status['active']:
        print(f"  Zuhri ID : {GOLD}{status['zuhri_id']}{RESET}")
        print(f"  Nama     : {GOLD}{status['name']}{RESET}")
        print(f"  Role     : {GOLD}{status['role']}{RESET}\n")
        
        # Test sign
        test_text = "Test Zuhri Auth"
        sig = sign(test_text)
        if sig:
            print(f"{GREEN}✅ Tanda tangan: {sig[:40]}...{RESET}")
            
            # Test verify
            if verify(test_text, sig, status.get('public_key', load_identity()['public_key'])):
                print(f"{GREEN}✅ Verifikasi BERHASIL{RESET}")
            else:
                print(f"{RED}❌ Verifikasi GAGAL{RESET}")
        else:
            print(f"{RED}❌ Gagal tanda tangan{RESET}")
    print()
