#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI ENKRIPSI — EKOSISTEM ENKRIPSI LENGKAP
AES-256 • RSA-4096 • Ed25519 • ChaCha20 • Steganografi
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, base64, hashlib, secrets, shutil, subprocess
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding, ed25519
    from cryptography.hazmat.backends import default_backend
    CRYPTO_OK = True
except ImportError:
    CRYPTO_OK = False
    print("❌ Install: pip install cryptography")
    sys.exit(1)

HOME = os.path.expanduser("~")
ENC_DIR = os.path.join(HOME, "zuhri_os", "enkripsi")
DATA_DIR = os.path.join(ENC_DIR, "data")
KEY_DIR = os.path.join(ENC_DIR, "keys")
VAULT_DIR = os.path.join(ENC_DIR, "vault")
for d in [DATA_DIR, KEY_DIR, VAULT_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

# ============================================================
# UTIL
# ============================================================
def derive_key(password, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                     iterations=600000, backend=default_backend())
    return kdf.derive(password.encode())

def get_id_badge():
    if not ZUHRI_ID_OK: return f"{YELLOW}⚠️  TANPA ID{RESET}"
    i = load_identity()
    return f"{GREEN}✅ {i['name']}{RESET}" if i else f"{YELLOW}⚠️{RESET}"

# ============================================================
# 1. ENKRIPSI TEKS
# ============================================================
def enkripsi_teks():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🔐 ZUHRI ENKRIPSI — ENKRIPSI TEKS                             ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    text = input("📝 Teks: ").strip()
    if not text: return
    pwd = input("🔐 Password: ").strip()
    if not pwd: return
    
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    key = derive_key(pwd, salt)
    aes = AESGCM(key)
    ct = aes.encrypt(nonce, text.encode(), None)
    
    output = base64.b64encode(salt + nonce + ct).decode()
    
    print(f"""
{BOLD}{GREEN}✅ TERENKRIPSI!{RESET}

{GOLD}Ciphertext:{RESET}
{output}

{DIM}Simpan ciphertext ini. Untuk dekripsi, pakai menu 2.{RESET}
""")
    input(f"{DIM}Enter...{RESET}")

def dekripsi_teks():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🔓 ZUHRI ENKRIPSI — DEKRIPSI TEKS                             ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    ct_b64 = input("🔐 Ciphertext: ").strip()
    pwd = input("🔐 Password: ").strip()
    
    try:
        data = base64.b64decode(ct_b64)
        salt, nonce, ct = data[:16], data[16:28], data[28:]
        key = derive_key(pwd, salt)
        aes = AESGCM(key)
        pt = aes.decrypt(nonce, ct, None).decode()
        print(f"\n{GREEN}✅ Plaintext:{RESET}\n{pt}\n")
    except Exception as e:
        print(f"\n{RED}❌ Password salah atau data rusak{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# 2. ENKRIPSI FILE
# ============================================================
def enkripsi_file():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  📁 ZUHRI ENKRIPSI — ENKRIPSI FILE                             ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    path = input("📂 Path file: ").strip()
    if not os.path.exists(path):
        print(f"{RED}❌ File tidak ditemukan{RESET}\n")
        input(f"{DIM}Enter...{RESET}"); return
    
    pwd = input("🔐 Password: ").strip()
    if not pwd: return
    
    try:
        data = open(path, 'rb').read()
        salt = secrets.token_bytes(16)
        nonce = secrets.token_bytes(12)
        key = derive_key(pwd, salt)
        aes = AESGCM(key)
        ct = aes.encrypt(nonce, data, None)
        
        out = path + ".zuhri"
        open(out, 'wb').write(salt + nonce + ct)
        
        size_in = os.path.getsize(path)
        size_out = os.path.getsize(out)
        
        print(f"""
{GREEN}✅ FILE TERENKRIPSI!{RESET}
  Input  : {size_in} bytes
  Output : {size_out} bytes
  File   : {out}
""")
        if ZUHRI_ID_OK: log_verified(f"ENCRYPT_FILE: {os.path.basename(path)}")
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

def dekripsi_file():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🔓 ZUHRI ENKRIPSI — DEKRIPSI FILE                             ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    path = input("📂 Path file .zuhri: ").strip()
    if not os.path.exists(path):
        print(f"{RED}❌ File tidak ditemukan{RESET}\n")
        input(f"{DIM}Enter...{RESET}"); return
    
    pwd = input("🔐 Password: ").strip()
    
    try:
        data = open(path, 'rb').read()
        salt, nonce, ct = data[:16], data[16:28], data[28:]
        key = derive_key(pwd, salt)
        aes = AESGCM(key)
        pt = aes.decrypt(nonce, ct, None)
        
        out = path.replace(".zuhri", "")
        open(out, 'wb').write(pt)
        print(f"\n{GREEN}✅ File didekripsi: {out}{RESET}\n")
        if ZUHRI_ID_OK: log_verified(f"DECRYPT_FILE: {os.path.basename(path)}")
    except Exception as e:
        print(f"\n{RED}❌ Password salah atau file rusak{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# 3. ENKRIPSI FOLDER (BATCH)
# ============================================================
def enkripsi_folder():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  📦 ZUHRI ENKRIPSI — ENKRIPSI FOLDER (BATCH)                   ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    folder = input("📂 Path folder: ").strip()
    if not os.path.isdir(folder):
        print(f"{RED}❌ Folder tidak ditemukan{RESET}\n")
        input(f"{DIM}Enter...{RESET}"); return
    
    pwd = input("🔐 Password: ").strip()
    if not pwd: return
    
    count = 0
    failed = 0
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith('.zuhri'): continue
            path = os.path.join(root, f)
            try:
                data = open(path, 'rb').read()
                salt = secrets.token_bytes(16)
                nonce = secrets.token_bytes(12)
                key = derive_key(pwd, salt)
                aes = AESGCM(key)
                ct = aes.encrypt(nonce, data, None)
                open(path + ".zuhri", 'wb').write(salt + nonce + ct)
                count += 1
                print(f"  {GREEN}✅{RESET} {path}")
            except:
                failed += 1
                print(f"  {RED}❌{RESET} {path}")
    
    print(f"\n{GREEN}✅ Selesai: {count} file, {failed} gagal{RESET}\n")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# 4. HASH CHECKER
# ============================================================
def hash_checker():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🔍 ZUHRI ENKRIPSI — HASH CHECKER                              ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    path = input("📂 Path file: ").strip()
    if not os.path.exists(path):
        print(f"{RED}❌ File tidak ditemukan{RESET}\n")
        input(f"{DIM}Enter...{RESET}"); return
    
    algos = {
        "MD5": hashlib.md5(),
        "SHA-1": hashlib.sha1(),
        "SHA-256": hashlib.sha256(),
        "SHA-512": hashlib.sha512(),
    }
    
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            for h in algos.values():
                h.update(chunk)
    
    print(f"\n{BOLD}📊 HASH FILE:{RESET}\n")
    for name, h in algos.items():
        print(f"  {GOLD}{name:10}{RESET}: {h.hexdigest()}")
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# 5. DIGITAL SIGNATURE
# ============================================================
def digital_signature():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🖋️  ZUHRI ENKRIPSI — DIGITAL SIGNATURE                        ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}1.{RESET} Tanda tangan file
  {GOLD}2.{RESET} Verifikasi tanda tangan
""")
    c = input(f"\n{CYAN}Pilih: {RESET}").strip()
    
    if c == "1":
        path = input("📂 Path file: ").strip()
        if not os.path.exists(path) or not ZUHRI_ID_OK:
            print(f"{RED}❌ File tidak ada atau Zuhri ID tidak ada{RESET}")
            input(f"{DIM}Enter...{RESET}"); return
        
        identity = load_identity()
        h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        sig = sign(h)
        
        sig_file = path + ".sig"
        json.dump({
            "file": os.path.basename(path),
            "hash": h,
            "signature": sig,
            "public_key": identity['public_key'],
            "zuhri_id": identity['zuhri_id'],
            "signed_at": datetime.now().isoformat()
        }, open(sig_file, "w"), indent=2)
        
        print(f"\n{GREEN}✅ File ditandatangani: {sig_file}{RESET}\n")
        if ZUHRI_ID_OK: log_verified(f"SIGN_FILE: {os.path.basename(path)}")
    
    elif c == "2":
        path = input("📂 Path file: ").strip()
        sig_file = input("📂 Path signature (.sig): ").strip()
        
        if not os.path.exists(path) or not os.path.exists(sig_file):
            print(f"{RED}❌ File tidak ditemukan{RESET}")
            input(f"{DIM}Enter...{RESET}"); return
        
        data = json.load(open(sig_file))
        h_now = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        
        print(f"\n{BOLD}📊 VERIFIKASI:{RESET}\n")
        print(f"  Hash tersimpan : {data['hash'][:32]}...")
        print(f"  Hash sekarang  : {h_now[:32]}...")
        
        if data['hash'] == h_now:
            print(f"\n  {GREEN}✅ File ASLI — Tidak diubah{RESET}")
            if verify(data['hash'], data['signature'], data['public_key']):
                print(f"  {GREEN}✅ Signature VALID{RESET}\n")
            else:
                print(f"  {RED}❌ Signature TIDAK VALID{RESET}\n")
        else:
            print(f"\n  {RED}❌ File sudah DIUBAH!{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# 6. PASSWORD MANAGER
# ============================================================
def password_manager():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🔑 ZUHRI ENKRIPSI — PASSWORD MANAGER                          ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}1.{RESET} Tambah password
  {GOLD}2.{RESET} Lihat password
  {GOLD}3.{RESET} Generate password kuat
""")
    c = input(f"\n{CYAN}Pilih: {RESET}").strip()
    
    vault_file = os.path.join(VAULT_DIR, "passwords.zuhri")
    
    if c == "1":
        master = input("🔐 Master password: ").strip()
        if not master: return
        
        name = input("🏷️  Nama akun: ").strip()
        user = input("👤 Username: ").strip()
        pwd = input("🔑 Password: ").strip()
        
        # Load vault lama
        vault = {}
        if os.path.exists(vault_file):
            try:
                data = open(vault_file, 'rb').read()
                salt, nonce, ct = data[:16], data[16:28], data[28:]
                key = derive_key(master, salt)
                aes = AESGCM(key)
                vault = json.loads(aes.decrypt(nonce, ct, None).decode())
            except:
                print(f"{RED}❌ Master password salah{RESET}")
                input(f"{DIM}Enter...{RESET}"); return
        
        vault[name] = {"username": user, "password": pwd, "added": datetime.now().isoformat()}
        
        # Encrypt ulang
        salt = secrets.token_bytes(16)
        nonce = secrets.token_bytes(12)
        key = derive_key(master, salt)
        aes = AESGCM(key)
        ct = aes.encrypt(nonce, json.dumps(vault).encode(), None)
        open(vault_file, 'wb').write(salt + nonce + ct)
        
        print(f"\n{GREEN}✅ Password '{name}' tersimpan{RESET}\n")
    
    elif c == "2":
        if not os.path.exists(vault_file):
            print(f"{YELLOW}⚠️  Belum ada password tersimpan{RESET}\n")
            input(f"{DIM}Enter...{RESET}"); return
        
        master = input("🔐 Master password: ").strip()
        try:
            data = open(vault_file, 'rb').read()
            salt, nonce, ct = data[:16], data[16:28], data[28:]
            key = derive_key(master, salt)
            aes = AESGCM(key)
            vault = json.loads(aes.decrypt(nonce, ct, None).decode())
            
            print(f"\n{BOLD}🔑 DAFTAR PASSWORD:{RESET}\n")
            for name, info in vault.items():
                print(f"  {GOLD}{name}{RESET}")
                print(f"    👤 {info['username']}")
                print(f"    🔑 {info['password']}")
                print()
        except:
            print(f"{RED}❌ Master password salah{RESET}\n")
    
    elif c == "3":
        import string
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        length = int(input("Panjang (default 16): ").strip() or "16")
        pwd = ''.join(secrets.choice(chars) for _ in range(length))
        print(f"\n{GREEN}🔑 Password: {pwd}{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# 7. STEGANOGRAFI
# ============================================================
def steganografi():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🖼️  ZUHRI ENKRIPSI — STEGANOGRAFI                            ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{YELLOW}⚠️  Butuh Pillow: pip install Pillow{RESET}
{DIM}Menyembunyikan pesan di dalam gambar.{RESET}
""")
    
    try:
        from PIL import Image
    except ImportError:
        print(f"{RED}❌ Install dulu: pip install Pillow{RESET}\n")
        input(f"{DIM}Enter...{RESET}"); return
    
    print(f"  {GOLD}1.{RESET} Sembunyikan pesan di gambar")
    print(f"  {GOLD}2.{RESET} Baca pesan dari gambar")
    
    c = input(f"\n{CYAN}Pilih: {RESET}").strip()
    
    if c == "1":
        img_path = input("🖼️  Path gambar: ").strip()
        msg = input("📝 Pesan: ").strip()
        
        if not os.path.exists(img_path): 
            print(f"{RED}❌ Gambar tidak ada{RESET}")
            input(f"{DIM}Enter...{RESET}"); return
        
        img = Image.open(img_path).convert('RGB')
        pixels = list(img.getdata())
        
        msg_bin = ''.join(format(ord(c), '08b') for c in msg) + '1111111111111110'
        
        new_pixels = []
        idx = 0
        for px in pixels:
            new_px = []
            for ch in px:
                if idx < len(msg_bin):
                    new_px.append((ch & 0xFE) | int(msg_bin[idx]))
                    idx += 1
                else:
                    new_px.append(ch)
            new_pixels.append(tuple(new_px))
        
        new_img = Image.new(img.mode, img.size)
        new_img.putdata(new_pixels)
        out = img_path.replace('.', '_stego.')
        new_img.save(out)
        
        print(f"\n{GREEN}✅ Pesan tersembunyi di: {out}{RESET}\n")
    
    elif c == "2":
        img_path = input("🖼️  Path gambar: ").strip()
        if not os.path.exists(img_path):
            print(f"{RED}❌ Gambar tidak ada{RESET}")
            input(f"{DIM}Enter...{RESET}"); return
        
        img = Image.open(img_path).convert('RGB')
        pixels = list(img.getdata())
        
        bits = ""
        for px in pixels:
            for ch in px:
                bits += str(ch & 1)
        
        msg = ""
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8: break
            if byte == '11111110': break
            msg += chr(int(byte, 2))
        
        print(f"\n{GREEN}📝 Pesan:{RESET}\n{msg}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# 8. KEY MANAGER
# ============================================================
def key_manager():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🗝️  ZUHRI ENKRIPSI — KEY MANAGER                              ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    keys = [f for f in os.listdir(KEY_DIR) if f.endswith(('.key', '.pem'))]
    
    print(f"{BOLD}📂 DAFTAR KUNCI:{RESET}\n")
    if keys:
        for i, k in enumerate(keys, 1):
            size = os.path.getsize(os.path.join(KEY_DIR, k))
            print(f"  {GOLD}{i}.{RESET} {k} {DIM}({size} bytes){RESET}")
    else:
        print(f"  {DIM}Belum ada kunci.{RESET}")
    
    print(f"\n{BOLD}📋 MENU:{RESET}")
    print(f"  {GOLD}1.{RESET} Generate RSA-4096 keypair")
    print(f"  {GOLD}2.{RESET} Generate Ed25519 keypair")
    print(f"  {GOLD}3.{RESET} Lihat kunci")
    print(f"  {GOLD}0.{RESET} Kembali")
    
    c = input(f"\n{CYAN}Pilih: {RESET}").strip()
    
    if c == "1":
        name = input("🏷️  Nama keypair: ").strip() or "key"
        pwd = input("🔐 Password: ").strip()
        
        priv = rsa.generate_private_key(public_exponent=65537, key_size=4096, backend=default_backend())
        enc = serialization.BestAvailableEncryption(pwd.encode())
        
        priv_path = os.path.join(KEY_DIR, f"{name}_private.pem")
        pub_path = os.path.join(KEY_DIR, f"{name}_public.pem")
        
        open(priv_path, 'wb').write(priv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=enc
        ))
        open(pub_path, 'wb').write(priv.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
        
        print(f"\n{GREEN}✅ RSA-4096 dibuat!{RESET}\n")
    
    elif c == "2":
        name = input("🏷️  Nama keypair: ").strip() or "sign"
        priv = ed25519.Ed25519PrivateKey.generate()
        
        priv_path = os.path.join(KEY_DIR, f"{name}_private.key")
        pub_path = os.path.join(KEY_DIR, f"{name}_public.key")
        
        open(priv_path, 'wb').write(priv.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ))
        open(pub_path, 'wb').write(priv.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ))
        
        print(f"\n{GREEN}✅ Ed25519 dibuat!{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🔐 ZUHRI ENKRIPSI — EKOSISTEM ENKRIPSI LENGKAP                ║
║  ──────────────────────────────────────────────────────────────  ║
║  AES-256 | RSA-4096 | Ed25519 | ChaCha20 | Steganografi        ║
║  Operator: {get_id_badge()}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🔐 Enkripsi Teks
  {GOLD}2.{RESET}  🔓 Dekripsi Teks
  {GOLD}3.{RESET}  📁 Enkripsi File
  {GOLD}4.{RESET}  📂 Dekripsi File
  {GOLD}5.{RESET}  📦 Enkripsi Folder (Batch)
  {GOLD}6.{RESET}  🔍 Hash Checker (MD5, SHA-256, dll)
  {GOLD}7.{RESET}  🖋️  Digital Signature
  {GOLD}8.{RESET}  🔑 Password Manager
  {GOLD}9.{RESET}  🖼️  Steganografi (Sembunyikan di Gambar)
  {GOLD}10.{RESET} 🗝️  Key Manager
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-10): {RESET}").strip()
            if c == "0": break
            elif c == "1": enkripsi_teks()
            elif c == "2": dekripsi_teks()
            elif c == "3": enkripsi_file()
            elif c == "4": dekripsi_file()
            elif c == "5": enkripsi_folder()
            elif c == "6": hash_checker()
            elif c == "7": digital_signature()
            elif c == "8": password_manager()
            elif c == "9": steganografi()
            elif c == "10": key_manager()
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "help":
            print("""
🔐 ZUHRI ENKRIPSI
  enkripsi          → Menu interaktif
  enkripsi teks     → Enkripsi teks
  enkripsi file     → Enkripsi file
  enkripsi hash     → Hash checker
  enkripsi passwd   → Password manager
""")
        else: menu()
    else: menu()
