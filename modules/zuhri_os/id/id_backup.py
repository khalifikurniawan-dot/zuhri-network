#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI ID — BACKUP & RESTORE MODULE
Backup lengkap dengan enkripsi & verifikasi
"""

import os
import sys
import json
import shutil
import subprocess
import tarfile
import hashlib
from datetime import datetime
from pathlib import Path

HOME = os.path.expanduser("~")
ID_DIR = os.path.join(HOME, "zuhri_os", "id")
ID_FILE = os.path.join(ID_DIR, "identity.json")
KEY_FILE = os.path.join(ID_DIR, "identity.key")
BACKUP_DIR = os.path.join(ID_DIR, "backups")
SDCARD_DIR = "/sdcard/backup_zuhri"

os.makedirs(BACKUP_DIR, exist_ok=True)

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
def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"

def get_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest()

# ============================================================
# BACKUP LENGKAP
# ============================================================
def do_backup():
    """Backup lengkap Zuhri ID"""
    if not os.path.exists(ID_FILE) or not os.path.exists(KEY_FILE):
        print(f"{RED}❌ Zuhri ID belum dibuat.{RESET}")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"zuhri_id_{timestamp}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    os.makedirs(backup_path, exist_ok=True)
    
    # Copy file
    shutil.copy2(ID_FILE, os.path.join(backup_path, "identity.json"))
    shutil.copy2(KEY_FILE, os.path.join(backup_path, "identity.key"))
    
    # Set permission
    os.chmod(os.path.join(backup_path, "identity.key"), 0o600)
    os.chmod(os.path.join(backup_path, "identity.json"), 0o644)
    
    # Metadata
    identity = json.load(open(ID_FILE))
    meta = {
        "zuhri_id": identity['zuhri_id'],
        "name": identity['name'],
        "role": identity['role'],
        "backup_time": datetime.now().isoformat(),
        "version": "1.0"
    }
    with open(os.path.join(backup_path, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    
    # Buat arsip tar.gz
    archive = os.path.join(BACKUP_DIR, f"{backup_name}.tar.gz")
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(backup_path, arcname=backup_name)
    
    # Hash SHA-256 arsip
    archive_hash = get_sha256(archive)
    
    # Simpan hash
    with open(archive + ".sha256", "w") as f:
        f.write(archive_hash)
    
    # Copy ke sdcard
    sdcard_ok = False
    try:
        os.makedirs(SDCARD_DIR, exist_ok=True)
        shutil.copy2(archive, os.path.join(SDCARD_DIR, f"{backup_name}.tar.gz"))
        shutil.copy2(archive + ".sha256", os.path.join(SDCARD_DIR, f"{backup_name}.tar.gz.sha256"))
        sdcard_ok = True
    except Exception as e:
        pass
    
    # Hitung ukuran
    archive_size = os.path.getsize(archive)
    
    print(f"""
{BOLD}{GREEN}╔══════════════════════════════════════════════════════════════════╗
║  ✅ BACKUP ZUHRI ID BERHASIL!                                  ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{GOLD}🆔 Zuhri ID:{RESET}   {identity['zuhri_id']}
{GOLD}👤 Nama:{RESET}       {identity['name']}
{GOLD}📅 Waktu:{RESET}      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{GOLD}📂 Lokasi Backup:{RESET}
   {backup_path}/

{GOLD}📦 Arsip:{RESET}
   {archive}
   Ukuran: {format_size(archive_size)}

{GOLD}🔐 Hash SHA-256:{RESET}
   {archive_hash[:64]}...
""")
    
    if sdcard_ok:
        print(f"{GOLD}💾 Di HP:{RESET}")
        print(f"   {SDCARD_DIR}/{backup_name}.tar.gz\n")
    
    return True

# ============================================================
# BACKUP TERENKRIPSI
# ============================================================
def do_backup_encrypted():
    """Backup dengan enkripsi AES-256-GCM"""
    if not os.path.exists(ID_FILE) or not os.path.exists(KEY_FILE):
        print(f"{RED}❌ Zuhri ID belum ada.{RESET}")
        return False
    
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
    except ImportError:
        print(f"{RED}❌ Install cryptography: pip install cryptography{RESET}")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"zuhri_id_{timestamp}_enc"
    
    # Baca data
    identity_data = open(ID_FILE, 'rb').read()
    key_data = open(KEY_FILE, 'rb').read()
    
    # Gabung data
    combined = json.dumps({
        "identity": identity_data.decode(),
        "key": key_data.decode()
    }).encode()
    
    # Password
    password = input("🔐 Password enkripsi: ").strip()
    if len(password) < 8:
        print(f"{RED}❌ Password minimal 8 karakter{RESET}")
        return False
    
    # Derive key
    import secrets
    salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    
    # Encrypt
    nonce = secrets.token_bytes(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, combined, None)
    
    # Format: SALT + NONCE + CIPHERTEXT
    output = salt + nonce + ciphertext
    
    # Simpan
    enc_file = os.path.join(BACKUP_DIR, f"{backup_name}.zuhri")
    with open(enc_file, 'wb') as f:
        f.write(output)
    
    # Hash
    enc_hash = get_sha256(enc_file)
    with open(enc_file + ".sha256", "w") as f:
        f.write(enc_hash)
    
    # Copy ke sdcard
    sdcard_ok = False
    try:
        os.makedirs(SDCARD_DIR, exist_ok=True)
        shutil.copy2(enc_file, os.path.join(SDCARD_DIR, f"{backup_name}.zuhri"))
        shutil.copy2(enc_file + ".sha256", os.path.join(SDCARD_DIR, f"{backup_name}.zuhri.sha256"))
        sdcard_ok = True
    except:
        pass
    
    size = os.path.getsize(enc_file)
    
    print(f"""
{BOLD}{GREEN}╔══════════════════════════════════════════════════════════════════╗
║  ✅ BACKUP TERENKRIPSI BERHASIL!                               ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{GOLD}📦 File:{RESET}   {enc_file}
{GOLD}📊 Ukuran:{RESET} {format_size(size)}
{GOLD}🔐 Algoritma:{RESET} AES-256-GCM + PBKDF2
{GOLD}🔑 Hash:{RESET}   {enc_hash[:64]}...
""")
    
    if sdcard_ok:
        print(f"{GOLD}💾 Di HP:{RESET}  {SDCARD_DIR}/{backup_name}.zuhri\n")
    
    return True

# ============================================================
# RESTORE
# ============================================================
def do_restore(archive_path):
    """Restore dari arsip backup"""
    if not os.path.exists(archive_path):
        print(f"{RED}❌ File tidak ditemukan: {archive_path}{RESET}")
        return False
    
    # Verifikasi hash (jika ada)
    hash_file = archive_path + ".sha256"
    if os.path.exists(hash_file):
        expected_hash = open(hash_file).read().strip()
        actual_hash = get_sha256(archive_path)
        if expected_hash != actual_hash:
            print(f"{RED}❌ Hash tidak cocok! File mungkin korup.{RESET}")
            return False
        print(f"{GREEN}✅ Hash verified{RESET}")
    
    # Backup ID lama dulu
    if os.path.exists(ID_FILE):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        old_backup = os.path.join(BACKUP_DIR, f"before_restore_{timestamp}")
        os.makedirs(old_backup, exist_ok=True)
        shutil.copy2(ID_FILE, old_backup)
        shutil.copy2(KEY_FILE, old_backup)
        print(f"{YELLOW}⚠️  ID lama di-backup ke: {old_backup}{RESET}")
    
    # Extract ke temp
    temp_dir = os.path.join(BACKUP_DIR, "_temp_restore")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(temp_dir)
        
        # Cari file
        found_key = None
        found_json = None
        for root, dirs, files in os.walk(temp_dir):
            for f in files:
                if f == "identity.key":
                    found_key = os.path.join(root, f)
                elif f == "identity.json":
                    found_json = os.path.join(root, f)
        
        if not found_key or not found_json:
            print(f"{RED}❌ File identity.key/json tidak ditemukan.{RESET}")
            return False
        
        # Copy ke lokasi asli
        shutil.copy2(found_key, KEY_FILE)
        shutil.copy2(found_json, ID_FILE)
        os.chmod(KEY_FILE, 0o600)
        os.chmod(ID_FILE, 0o644)
        
        shutil.rmtree(temp_dir)
        
        identity = json.load(open(ID_FILE))
        
        print(f"""
{BOLD}{GREEN}╔══════════════════════════════════════════════════════════════════╗
║  ✅ RESTORE ZUHRI ID BERHASIL!                                 ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{GOLD}🆔 Zuhri ID:{RESET}   {identity['zuhri_id']}
{GOLD}👤 Nama:{RESET}       {identity['name']}
{GOLD}🎭 Role:{RESET}       {identity['role']}
{GOLD}📅 Dibuat:{RESET}     {identity['created'][:19]}
""")
        return True
    except Exception as e:
        print(f"{RED}❌ Restore gagal: {e}{RESET}")
        return False

# ============================================================
# RESTORE TERENKRIPSI
# ============================================================
def do_restore_encrypted(enc_path):
    """Restore dari backup terenkripsi"""
    if not os.path.exists(enc_path):
        print(f"{RED}❌ File tidak ditemukan: {enc_path}{RESET}")
        return False
    
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
    except ImportError:
        print(f"{RED}❌ Install cryptography{RESET}")
        return False
    
    # Baca file
    data = open(enc_path, 'rb').read()
    salt = data[:16]
    nonce = data[16:28]
    ciphertext = data[28:]
    
    # Password
    password = input("🔐 Password enkripsi: ").strip()
    
    try:
        # Derive key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=600000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        
        # Decrypt
        aesgcm = AESGCM(key)
        combined = aesgcm.decrypt(nonce, ciphertext, None)
        
        # Parse
        parsed = json.loads(combined.decode())
        identity_data = parsed['identity']
        key_data = parsed['key']
        
        # Backup ID lama
        if os.path.exists(ID_FILE):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            old_backup = os.path.join(BACKUP_DIR, f"before_restore_{timestamp}")
            os.makedirs(old_backup, exist_ok=True)
            shutil.copy2(ID_FILE, old_backup)
            shutil.copy2(KEY_FILE, old_backup)
            print(f"{YELLOW}⚠️  ID lama di-backup{RESET}")
        
        # Tulis file
        with open(ID_FILE, 'w') as f:
            f.write(identity_data)
        with open(KEY_FILE, 'w') as f:
            f.write(key_data)
        os.chmod(KEY_FILE, 0o600)
        os.chmod(ID_FILE, 0o644)
        
        identity = json.loads(identity_data)
        
        print(f"""
{BOLD}{GREEN}✅ RESTORE TERENKRIPSI BERHASIL!{RESET}

{GOLD}🆔 ID:{RESET}   {identity['zuhri_id']}
{GOLD}👤 Nama:{RESET} {identity['name']}
""")
        return True
    except Exception as e:
        print(f"{RED}❌ Password salah atau file rusak: {e}{RESET}")
        return False

# ============================================================
# LIST BACKUP
# ============================================================
def do_list():
    """Tampilkan daftar backup"""
    archives = sorted([f for f in os.listdir(BACKUP_DIR) 
                      if f.endswith(('.tar.gz', '.zuhri'))], reverse=True)
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📂 DAFTAR BACKUP ZUHRI ID                                     ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    if not archives:
        print(f"{YELLOW}Belum ada backup.{RESET}\n")
        return
    
    print(f"{BOLD}Total: {len(archives)} backup{RESET}\n")
    
    for i, a in enumerate(archives, 1):
        path = os.path.join(BACKUP_DIR, a)
        size = format_size(os.path.getsize(path))
        
        # Baca metadata
        meta_file = None
        if a.endswith('.tar.gz'):
            base = a.replace('.tar.gz', '')
            meta_path = os.path.join(BACKUP_DIR, base, "meta.json")
            if os.path.exists(meta_path):
                meta = json.load(open(meta_path))
                zuhri_id = meta.get('zuhri_id', 'N/A')[:20] + "..."
                date = meta.get('backup_time', 'N/A')[:19]
            else:
                zuhri_id = "N/A"
                date = "N/A"
        else:
            zuhri_id = "(terenkripsi)"
            date = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M")
        
        type_icon = "🔐" if a.endswith('.zuhri') else "📦"
        
        print(f"  {GOLD}{i}.{RESET} {type_icon} {a}")
        print(f"     {DIM}📅 {date} | 💾 {size} | 🆔 {zuhri_id}{RESET}")
    print()

# ============================================================
# EXPORT PUBLIC ONLY
# ============================================================
def do_export_public():
    """Export hanya public ID (untuk sharing)"""
    identity = json.load(open(ID_FILE))
    
    export = {
        "zuhri_id": identity['zuhri_id'],
        "name": identity['name'],
        "role": identity['role'],
        "public_key": identity['public_key'],
        "protocol": identity['protocol'],
        "gen": identity['gen'],
        "resonance": identity['resonance'],
        "exported": datetime.now().isoformat()
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_file = os.path.join(BACKUP_DIR, f"public_{timestamp}.json")
    with open(export_file, 'w') as f:
        json.dump(export, f, indent=2)
    
    print(f"""
{BOLD}{GREEN}✅ EXPORT PUBLIC ID BERHASIL!{RESET}

{GOLD}📄 File:{RESET} {export_file}

{GOLD}Isi:{RESET}
{json.dumps(export, indent=2)}

{DIM}⚠️  File ini AMAN dibagikan. Tidak ada private key.{RESET}
""")

# ============================================================
# CLEANUP OLD BACKUPS
# ============================================================
def do_cleanup(keep=10):
    """Hapus backup lama, simpan 10 terbaru"""
    archives = sorted([f for f in os.listdir(BACKUP_DIR) 
                      if f.endswith(('.tar.gz', '.zuhri'))])
    
    if len(archives) <= keep:
        print(f"{GREEN}✅ Tidak perlu cleanup. Total: {len(archives)} backup{RESET}")
        return
    
    to_delete = archives[:-keep]
    
    print(f"\n{YELLOW}🗑️  Menghapus {len(to_delete)} backup lama...{RESET}\n")
    for a in to_delete:
        os.remove(os.path.join(BACKUP_DIR, a))
        print(f"  {DIM}✓ Dihapus: {a}{RESET}")
    
    print(f"\n{GREEN}✅ Cleanup selesai. Sisa: {keep} backup{RESET}\n")

# ============================================================
# VERIFY BACKUP
# ============================================================
def do_verify(archive_path):
    """Verifikasi backup"""
    if not os.path.exists(archive_path):
        print(f"{RED}❌ File tidak ditemukan{RESET}")
        return
    
    hash_file = archive_path + ".sha256"
    if not os.path.exists(hash_file):
        print(f"{YELLOW}⚠️  File hash tidak ada, skip verifikasi{RESET}")
        return
    
    expected = open(hash_file).read().strip()
    actual = get_sha256(archive_path)
    
    print(f"\n{BOLD}{CYAN}🔐 VERIFIKASI BACKUP{RESET}\n")
    print(f"  File    : {os.path.basename(archive_path)}")
    print(f"  Expected: {DIM}{expected}{RESET}")
    print(f"  Actual  : {DIM}{actual}{RESET}\n")
    
    if expected == actual:
        print(f"{GREEN}✅ HASH COCOK — File ASLI{RESET}\n")
    else:
        print(f"{RED}❌ HASH TIDAK COCOK — File RUSAK/DIUBAH!{RESET}\n")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🆔 ZUHRI ID — BACKUP & RESTORE                                ║
║  ──────────────────────────────────────────────────────────────  ║
║  STATUS: ✅ AKTIF                                              ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {CYAN}1.{RESET}  📦 Backup Biasa (tar.gz)
  {CYAN}2.{RESET}  🔐 Backup Terenkripsi (AES-256-GCM)
  {CYAN}3.{RESET}  📂 Restore dari Arsip
  {CYAN}4.{RESET}  🔓 Restore dari File Terenkripsi
  {CYAN}5.{RESET}  📋 Lihat Daftar Backup
  {CYAN}6.{RESET}  📤 Export Public ID
  {CYAN}7.{RESET}  🔐 Verifikasi Hash Backup
  {CYAN}8.{RESET}  🗑️  Cleanup Backup Lama
  {CYAN}0.{RESET}  Keluar
""")
        
        choice = input(f"{GOLD}  📡 Pilih (0-8): {RESET}").strip()
        
        if choice == "1":
            do_backup()
            input(f"\n{DIM}Tekan Enter...{RESET}")
        elif choice == "2":
            do_backup_encrypted()
            input(f"\n{DIM}Tekan Enter...{RESET}")
        elif choice == "3":
            path = input("📂 Path arsip: ").strip()
            do_restore(path)
            input(f"\n{DIM}Tekan Enter...{RESET}")
        elif choice == "4":
            path = input("📂 Path file terenkripsi: ").strip()
            do_restore_encrypted(path)
            input(f"\n{DIM}Tekan Enter...{RESET}")
        elif choice == "5":
            do_list()
            input(f"\n{DIM}Tekan Enter...{RESET}")
        elif choice == "6":
            do_export_public()
            input(f"\n{DIM}Tekan Enter...{RESET}")
        elif choice == "7":
            path = input("📂 Path file: ").strip()
            do_verify(path)
            input(f"\n{DIM}Tekan Enter...{RESET}")
        elif choice == "8":
            do_cleanup()
            input(f"\n{DIM}Tekan Enter...{RESET}")
        elif choice == "0":
            break

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "backup":
            do_backup()
        elif cmd == "encrypted":
            do_backup_encrypted()
        elif cmd == "restore" and len(sys.argv) > 2:
            do_restore(sys.argv[2])
        elif cmd == "restore-enc" and len(sys.argv) > 2:
            do_restore_encrypted(sys.argv[2])
        elif cmd == "list":
            do_list()
        elif cmd == "export":
            do_export_public()
        elif cmd == "verify" and len(sys.argv) > 2:
            do_verify(sys.argv[2])
        elif cmd == "cleanup":
            do_cleanup()
        else:
            menu()
    else:
        menu()
