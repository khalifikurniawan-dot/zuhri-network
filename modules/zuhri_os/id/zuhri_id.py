#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI ID — IDENTITAS DIGITAL MANDIRI (FULL)
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
Fitur: Create, Show, Sign, Verify, Export, Backup, Restore, Login, Session, Logout
"""

import os
import sys
import json
import base64
import hashlib
import secrets
import shutil
import subprocess
import time
from datetime import datetime, timedelta

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    CRYPTO_OK = True
except ImportError:
    CRYPTO_OK = False
    print("❌ Install: pip install cryptography")
    sys.exit(1)

# ============================================================
# KONFIGURASI
# ============================================================
HOME = os.path.expanduser("~")
ID_DIR = os.path.join(HOME, "zuhri_os", "id")
ID_FILE = os.path.join(ID_DIR, "identity.json")
KEY_FILE = os.path.join(ID_DIR, "identity.key")
BACKUP_DIR = os.path.join(ID_DIR, "backups")
SESSION_DIR = os.path.join(HOME, "zuhri_os", "sessions")

for d in [ID_DIR, BACKUP_DIR, SESSION_DIR]:
    os.makedirs(d, exist_ok=True)

# ============================================================
# WARNA
# ============================================================
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

def verify_sig(text, sig_b64, pub_b64):
    try:
        pub = ed25519.Ed25519PublicKey.from_public_bytes(base64.b64decode(pub_b64))
        pub.verify(base64.b64decode(sig_b64), text.encode())
        return True
    except:
        return False

# ============================================================
# CREATE
# ============================================================
def generate_id(name, role="Operator"):
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    
    zuhri_id = "ZUH-" + hashlib.sha256(pub_bytes).hexdigest()[:32].upper()
    
    identity = {
        "zuhri_id": zuhri_id,
        "name": name,
        "role": role,
        "public_key": base64.b64encode(pub_bytes).decode(),
        "created": datetime.now().isoformat(),
        "protocol": "K-8.0",
        "gen": "ZUH-8-9-0-K-8.0",
        "resonance": "0-8-9"
    }
    
    with open(KEY_FILE, 'w') as f:
        json.dump({"private_key": base64.b64encode(priv_bytes).decode()}, f)
    os.chmod(KEY_FILE, 0o600)
    
    with open(ID_FILE, 'w') as f:
        json.dump(identity, f, indent=2)
    os.chmod(ID_FILE, 0o644)
    
    return identity

def cmd_create():
    existing = load_identity()
    if existing:
        confirm = input(f"{YELLOW}⚠️  Zuhri ID sudah ada ({existing['zuhri_id']}). Buat baru? (y/n): {RESET}").strip().lower()
        if confirm != 'y':
            return
    
    name = input("🏷️  Nama Anda: ").strip() or "Anonymous"
    role = input("🎭  Role (default: Operator): ").strip() or "Operator"
    
    identity = generate_id(name, role)
    
    print(f"""
{BOLD}{GREEN}✅ ZUHRI ID BERHASIL DIBUAT!{RESET}

{GOLD}🆔 ID ANDA:{RESET}
   {BOLD}{identity['zuhri_id']}{RESET}

{DIM}Simpan ID ini. Ini identitas digital Anda.{RESET}
""")

# ============================================================
# SHOW
# ============================================================
def cmd_show():
    identity = load_identity()
    if not identity:
        print(f"{RED}❌ Belum ada Zuhri ID. Buat dulu: id create{RESET}")
        return
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🆔 ZUHRI ID — IDENTITAS DIGITAL MANDIRI                       ║
║  ──────────────────────────────────────────────────────────────  ║
║  ID       : {GOLD}{identity['zuhri_id']}{RESET}
║  Nama     : {GOLD}{identity['name']}{RESET}
║  Role     : {GOLD}{identity['role']}{RESET}
║  Dibuat   : {GOLD}{identity['created'][:19]}{RESET}
║  Protokol : {GOLD}{identity['protocol']}{RESET}
║  Gen      : {GOLD}{identity['gen']}{RESET}
║  Resonansi: {GOLD}{identity['resonance']}{RESET}
║  ──────────────────────────────────────────────────────────────  ║
║  Public Key: {DIM}{identity['public_key'][:40]}...{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")

# ============================================================
# SIGN
# ============================================================
def cmd_sign(args):
    if not args:
        print(f"{RED}❌ Format: id sign \"pesan\"{RESET}")
        return
    message = " ".join(args)
    signature = sign(message)
    if signature:
        print(f"{GREEN}✍️  Signature:{RESET}\n{signature}\n")
    else:
        print(f"{RED}❌ Belum ada Zuhri ID. Buat dulu: id create{RESET}")

# ============================================================
# VERIFY
# ============================================================
def cmd_verify():
    identity = load_identity()
    if not identity:
        print(f"{RED}❌ Belum ada Zuhri ID.{RESET}")
        return
    
    message = input("📝 Pesan: ").strip()
    sig = input("✍️  Signature: ").strip()
    
    if verify_sig(message, sig, identity['public_key']):
        print(f"{GREEN}✅ Tanda tangan VALID!{RESET}\n")
    else:
        print(f"{RED}❌ Tanda tangan TIDAK VALID!{RESET}\n")

# ============================================================
# EXPORT
# ============================================================
def cmd_export():
    identity = load_identity()
    if not identity:
        print(f"{RED}❌ Belum ada Zuhri ID.{RESET}")
        return
    
    export = {
        "zuhri_id": identity['zuhri_id'],
        "name": identity['name'],
        "public_key": identity['public_key'],
        "protocol": identity['protocol'],
        "gen": identity['gen']
    }
    print(json.dumps(export, indent=2))

# ============================================================
# BACKUP
# ============================================================
def cmd_backup():
    if not os.path.exists(ID_FILE) or not os.path.exists(KEY_FILE):
        print(f"{RED}❌ Zuhri ID belum dibuat.{RESET}")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"zuhri_id_{timestamp}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    os.makedirs(backup_path, exist_ok=True)
    
    shutil.copy2(ID_FILE, os.path.join(backup_path, "identity.json"))
    shutil.copy2(KEY_FILE, os.path.join(backup_path, "identity.key"))
    
    archive = os.path.join(BACKUP_DIR, f"{backup_name}.tar.gz")
    subprocess.run(["tar", "-czf", archive, "-C", BACKUP_DIR, backup_name], check=False)
    
    sdcard_dir = "/sdcard/backup_zuhri"
    sdcard_ok = False
    try:
        os.makedirs(sdcard_dir, exist_ok=True)
        shutil.copy2(archive, os.path.join(sdcard_dir, f"{backup_name}.tar.gz"))
        sdcard_ok = True
    except:
        pass
    
    print(f"""
{BOLD}{GREEN}✅ BACKUP ZUHRI ID BERHASIL!{RESET}

{GOLD}📂 Lokasi Backup:{RESET}
   {backup_path}/

{GOLD}📦 Arsip:{RESET}
   {archive}
""")
    if sdcard_ok:
        print(f"{GOLD}💾 Di HP:{RESET}\n   /sdcard/backup_zuhri/{backup_name}.tar.gz\n")

# ============================================================
# RESTORE
# ============================================================
def cmd_restore(args):
    if not args:
        print(f"{RED}❌ Format: id restore <path_arsip>{RESET}")
        return
    
    archive_path = args[0]
    if not os.path.exists(archive_path):
        print(f"{RED}❌ File tidak ditemukan: {archive_path}{RESET}")
        return
    
    # Backup ID lama
    if os.path.exists(ID_FILE):
        old_backup = os.path.join(BACKUP_DIR, f"before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(old_backup, exist_ok=True)
        shutil.copy2(ID_FILE, old_backup)
        shutil.copy2(KEY_FILE, old_backup)
        print(f"{YELLOW}⚠️  ID lama di-backup ke: {old_backup}{RESET}")
    
    temp_dir = os.path.join(BACKUP_DIR, "_temp_restore")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        subprocess.run(["tar", "-xzf", archive_path, "-C", temp_dir], check=True)
        
        found_key = None
        found_json = None
        for root, dirs, files in os.walk(temp_dir):
            for f in files:
                if f == "identity.key":
                    found_key = os.path.join(root, f)
                elif f == "identity.json":
                    found_json = os.path.join(root, f)
        
        if found_key and found_json:
            shutil.copy2(found_key, KEY_FILE)
            shutil.copy2(found_json, ID_FILE)
            os.chmod(KEY_FILE, 0o600)
            os.chmod(ID_FILE, 0o644)
            shutil.rmtree(temp_dir)
            
            identity = load_identity()
            print(f"""
{BOLD}{GREEN}✅ RESTORE ZUHRI ID BERHASIL!{RESET}

{GOLD}🆔 ID:{RESET}   {identity['zuhri_id']}
{GOLD}👤 Nama:{RESET} {identity['name']}
""")
        else:
            print(f"{RED}❌ File identity.key/json tidak ditemukan dalam arsip.{RESET}")
    except Exception as e:
        print(f"{RED}❌ Restore gagal: {e}{RESET}")

# ============================================================
# LIST BACKUP
# ============================================================
def cmd_list():
    archives = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.tar.gz')], reverse=True)
    
    print(f"\n{BOLD}{CYAN}📂 DAFTAR BACKUP ZUHRI ID{RESET}\n")
    
    if not archives:
        print(f"{YELLOW}Belum ada backup.{RESET}\n")
        return
    
    for i, a in enumerate(archives, 1):
        path = os.path.join(BACKUP_DIR, a)
        size = os.path.getsize(path) / 1024
        print(f"  {GOLD}{i}.{RESET} {a} ({size:.1f} KB)")
    print()

# ============================================================
# LOGIN
# ============================================================
def cmd_login():
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
    
    # 1. Buat challenge
    print(f"{CYAN}[1/3] Server membuat challenge...{RESET}")
    challenge = secrets.token_hex(32)
    challenge_file = os.path.join(SESSION_DIR, f"challenge_{identity['zuhri_id']}.json")
    challenge_data = {
        "challenge": challenge,
        "zuhri_id": identity['zuhri_id'],
        "created": datetime.now().isoformat(),
        "expire": (datetime.now() + timedelta(minutes=5)).isoformat(),
        "used": False
    }
    with open(challenge_file, "w") as f:
        json.dump(challenge_data, f, indent=2)
    print(f"      {DIM}{challenge[:32]}...{RESET}")
    
    # 2. Sign challenge
    print(f"{CYAN}[2/3] Menandatangani...{RESET}")
    signature = sign(challenge)
    print(f"      {DIM}{signature[:32]}...{RESET}")
    
    # 3. Verify
    print(f"{CYAN}[3/3] Verifikasi...{RESET}")
    if not verify_sig(challenge, signature, identity['public_key']):
        print(f"{RED}❌ Login gagal: signature tidak valid{RESET}")
        return
    
    challenge_data['used'] = True
    with open(challenge_file, "w") as f:
        json.dump(challenge_data, f, indent=2)
    
    # Buat session
    session_token = secrets.token_hex(32)
    session_data = {
        "zuhri_id": identity['zuhri_id'],
        "token": session_token,
        "login_time": datetime.now().isoformat(),
        "expire": (datetime.now() + timedelta(hours=24)).isoformat()
    }
    session_file = os.path.join(SESSION_DIR, f"session_{session_token}.json")
    with open(session_file, "w") as f:
        json.dump(session_data, f, indent=2)
    
    with open(os.path.join(SESSION_DIR, "current_token.txt"), "w") as f:
        f.write(session_token)
    
    print(f"""
{BOLD}{GREEN}✅ LOGIN BERHASIL!{RESET}

{GOLD}🔑 Session Token:{RESET}
   {session_token}

{GOLD}⏰ Berlaku:{RESET} 24 jam
""")

def cmd_session():
    token_file = os.path.join(SESSION_DIR, "current_token.txt")
    if not os.path.exists(token_file):
        print(f"{YELLOW}⚠️  Belum login{RESET}")
        return
    
    with open(token_file) as f:
        token = f.read().strip()
    
    session_file = os.path.join(SESSION_DIR, f"session_{token}.json")
    if not os.path.exists(session_file):
        print(f"{RED}❌ Session tidak valid{RESET}")
        return
    
    with open(session_file) as f:
        session = json.load(f)
    
    if datetime.now() > datetime.fromisoformat(session['expire']):
        print(f"{RED}❌ Session kadaluarsa{RESET}")
        return
    
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

def cmd_logout():
    token_file = os.path.join(SESSION_DIR, "current_token.txt")
    if not os.path.exists(token_file):
        print(f"{YELLOW}⚠️  Belum login{RESET}")
        return
    
    with open(token_file) as f:
        token = f.read().strip()
    
    session_file = os.path.join(SESSION_DIR, f"session_{token}.json")
    if os.path.exists(session_file):
        os.remove(session_file)
    
    os.remove(token_file)
    print(f"{GREEN}✅ Logout berhasil{RESET}")

def cmd_protected():
    token_file = os.path.join(SESSION_DIR, "current_token.txt")
    if not os.path.exists(token_file):
        print(f"{RED}❌ Akses ditolak — login dulu: id login{RESET}")
        return
    
    print(f"{GREEN}✅ Akses diberikan!{RESET}")
    print(f"{DIM}Ini adalah aksi yang dilindungi Zuhri Login.{RESET}\n")

# ============================================================
# HELP
# ============================================================
def show_help():
    print(f"""
{BOLD}{CYAN}🆔 ZUHRI ID — BANTUAN{RESET}
{'─' * 55}
  {BOLD}id create{RESET}              → Buat Zuhri ID baru
  {BOLD}id show{RESET}                → Tampilkan Zuhri ID
  {BOLD}id sign "pesan"{RESET}        → Tanda tangani pesan
  {BOLD}id verify{RESET}              → Verifikasi tanda tangan
  {BOLD}id export{RESET}              → Export public ID
  {BOLD}id backup{RESET}              → Backup Zuhri ID
  {BOLD}id restore <arsip>{RESET}     → Restore dari backup
  {BOLD}id list{RESET}                → Lihat daftar backup
  {BOLD}id login{RESET}               → Login tanpa password
  {BOLD}id session{RESET}             → Cek session aktif
  {BOLD}id logout{RESET}              → Logout
  {BOLD}id protected{RESET}           → Test aksi terproteksi
  {BOLD}id help{RESET}                → Bantuan
{'─' * 55}
""")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    args = sys.argv[2:]
    
    if cmd == "create":
        cmd_create()
    elif cmd == "show":
        cmd_show()
    elif cmd == "sign":
        cmd_sign(args)
    elif cmd == "verify":
        cmd_verify()
    elif cmd == "export":
        cmd_export()
    elif cmd == "backup":
        cmd_backup()
    elif cmd == "restore":
        cmd_restore(args)
    elif cmd == "list":
        cmd_list()
    elif cmd == "login":
        cmd_login()
    elif cmd == "session":
        cmd_session()
    elif cmd == "logout":
        cmd_logout()
    elif cmd == "protected":
        cmd_protected()
    elif cmd == "help":
        show_help()
    else:
        show_help()
