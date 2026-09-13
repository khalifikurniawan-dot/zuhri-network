#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI CRYPTO — PROTOKOL K-8.0 GEN ZUHRI v9.0
AES-256-GCM | RSA-4096 | Ed25519 | PBKDF2
Terintegrasi ZUHRI ID
"""

import os
import sys
import json
import base64
import hashlib
import secrets
from datetime import datetime
from pathlib import Path

# ===== ZUHRI AUTH =====
sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified, get_status
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

# ===== KRIPTOGRAFI =====
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding, ed25519
    from cryptography.hazmat.backends import default_backend
    CRYPTO_OK = True
except ImportError:
    CRYPTO_OK = False
    print("❌ Install: pip install cryptography")
    sys.exit(1)

# ===== KONFIGURASI =====
HOME = os.path.expanduser("~")
CRYPTO_DIR = os.path.join(HOME, "zuhri_os", "crypto")
VAULT_DIR = os.path.join(CRYPTO_DIR, "vault")
KEYS_DIR = os.path.join(CRYPTO_DIR, "keys")
LOG_DIR = os.path.join(HOME, "zuhri_os", "logs")

for d in [CRYPTO_DIR, VAULT_DIR, KEYS_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

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
# ZUHRI ID HELPER
# ============================================================
def get_id_badge():
    """Badge identitas untuk output"""
    if not ZUHRI_ID_OK:
        return f"{YELLOW}⚠️  TANPA ZUHRI ID{RESET}"
    s = get_status()
    if s['active']:
        return f"{GREEN}✅ {s['name']} ({s['zuhri_id'][:20]}...){RESET}"
    return f"{YELLOW}⚠️  TANPA ZUHRI ID{RESET}"

def sign_and_log(action, detail=""):
    """Tanda tangani aksi & catat ke log"""
    if not ZUHRI_ID_OK:
        return None
    
    identity = load_identity()
    if not identity:
        return None
    
    # Buat signature untuk aksi
    payload = f"{action}|{detail}|{datetime.now().isoformat()}"
    sig = sign(payload)
    
    # Log
    log_verified(f"CRYPTO_{action}: {detail}", "OK")
    
    return sig

# ============================================================
# AES-256-GCM — ENKRIPSI FILE
# ============================================================
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(filepath, password):
    """Enkripsi file dengan AES-256-GCM"""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        
        salt = secrets.token_bytes(16)
        nonce = secrets.token_bytes(12)
        key = derive_key(password, salt)
        
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, data, None)
        
        output = salt + nonce + ciphertext
        enc_path = filepath + ".zuhri"
        
        with open(enc_path, 'wb') as f:
            f.write(output)
        
        # Tanda tangani & log
        sig = sign_and_log("ENCRYPT", filepath)
        
        return enc_path, sig
    except Exception as e:
        print(f"{RED}❌ Enkripsi gagal: {e}{RESET}")
        return None, None

def decrypt_file(filepath, password):
    """Dekripsi file dengan AES-256-GCM"""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        
        salt = data[:16]
        nonce = data[16:28]
        ciphertext = data[28:]
        key = derive_key(password, salt)
        
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        out_path = filepath.replace(".zuhri", "")
        with open(out_path, 'wb') as f:
            f.write(plaintext)
        
        sig = sign_and_log("DECRYPT", filepath)
        
        return out_path, sig
    except Exception as e:
        print(f"{RED}❌ Dekripsi gagal (password salah?): {e}{RESET}")
        return None, None

# ============================================================
# RSA-4096
# ============================================================
def generate_rsa_keypair(name="zuhri"):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    
    password = input("🔐 Password untuk private key: ").strip()
    enc = serialization.BestAvailableEncryption(password.encode())
    
    priv_path = os.path.join(KEYS_DIR, f"{name}_private.pem")
    pub_path = os.path.join(KEYS_DIR, f"{name}_public.pem")
    
    with open(priv_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=enc
        ))
    
    public_key = private_key.public_key()
    with open(pub_path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    sign_and_log("RSA_KEYPAIR", name)
    
    print(f"{GREEN}✅ RSA-4096 keypair dibuat!{RESET}")
    print(f"  🔑 Private: {priv_path}")
    print(f"  🔓 Public : {pub_path}")
    return priv_path, pub_path

def rsa_encrypt(message, public_key_path):
    with open(public_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())
    
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    sign_and_log("RSA_ENCRYPT", f"{len(message)} char")
    return base64.b64encode(ciphertext).decode()

def rsa_decrypt(ciphertext_b64, private_key_path, password):
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(), password=password.encode(), backend=default_backend()
        )
    
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    sign_and_log("RSA_DECRYPT", f"{len(plaintext)} char")
    return plaintext.decode()

# ============================================================
# Ed25519
# ============================================================
def generate_ed25519_keypair(name="zuhri_sign"):
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    priv_path = os.path.join(KEYS_DIR, f"{name}_private.key")
    pub_path = os.path.join(KEYS_DIR, f"{name}_public.key")
    
    with open(priv_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    with open(pub_path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ))
    
    sign_and_log("ED25519_KEYPAIR", name)
    print(f"{GREEN}✅ Ed25519 keypair dibuat!{RESET}")
    return priv_path, pub_path

def sign_message(message, private_key_path):
    with open(private_key_path, 'rb') as f:
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(f.read())
    signature = private_key.sign(message.encode())
    sign_and_log("ED25519_SIGN", f"{len(message)} char")
    return base64.b64encode(signature).decode()

def verify_signature(message, signature_b64, public_key_path):
    with open(public_key_path, 'rb') as f:
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(f.read())
    try:
        signature = base64.b64decode(signature_b64)
        public_key.verify(signature, message.encode())
        return True
    except:
        return False

# ============================================================
# VAULT
# ============================================================
def vault_store(secret_name, secret_value, password):
    vault_file = os.path.join(VAULT_DIR, "kosmik_vault.json")
    
    vault = {}
    if os.path.exists(vault_file):
        try:
            with open(vault_file) as f:
                encrypted = json.load(f)
            salt = base64.b64decode(encrypted['salt'])
            nonce = base64.b64decode(encrypted['nonce'])
            ciphertext = base64.b64decode(encrypted['data'])
            key = derive_key(password, salt)
            aesgcm = AESGCM(key)
            vault = json.loads(aesgcm.decrypt(nonce, ciphertext, None).decode())
        except:
            vault = {}
    
    vault[secret_name] = {
        "value": secret_value,
        "created": datetime.now().isoformat()
    }
    
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, json.dumps(vault).encode(), None)
    
    with open(vault_file, 'w') as f:
        json.dump({
            'salt': base64.b64encode(salt).decode(),
            'nonce': base64.b64encode(nonce).decode(),
            'data': base64.b64encode(ciphertext).decode()
        }, f)
    
    sign_and_log("VAULT_STORE", secret_name)
    print(f"{GREEN}✅ Rahasia '{secret_name}' tersimpan di vault{RESET}")

def vault_retrieve(secret_name, password):
    vault_file = os.path.join(VAULT_DIR, "kosmik_vault.json")
    if not os.path.exists(vault_file):
        print(f"{RED}❌ Vault kosong{RESET}")
        return None
    
    try:
        with open(vault_file) as f:
            encrypted = json.load(f)
        salt = base64.b64decode(encrypted['salt'])
        nonce = base64.b64decode(encrypted['nonce'])
        ciphertext = base64.b64decode(encrypted['data'])
        key = derive_key(password, salt)
        aesgcm = AESGCM(key)
        vault = json.loads(aesgcm.decrypt(nonce, ciphertext, None).decode())
        
        if secret_name in vault:
            sign_and_log("VAULT_RETRIEVE", secret_name)
            return vault[secret_name]['value']
        else:
            print(f"{YELLOW}⚠️  '{secret_name}' tidak ditemukan{RESET}")
            return None
    except Exception as e:
        print(f"{RED}❌ Gagal buka vault (password salah?): {e}{RESET}")
        return None

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        
        # Header dengan Zuhri ID
        id_badge = get_id_badge()
        
        print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🔐 ZUHRI CRYPTO — PROTOKOL K-8.0 GEN ZUHRI v9.0               ║
║  ──────────────────────────────────────────────────────────────  ║
║  AES-256-GCM  |  RSA-4096  |  Ed25519  |  PBKDF2              ║
║  ZUHRI ID : {id_badge}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU KRIPTOGRAFI:{RESET}
  {CYAN}1.{RESET}  🔒 Enkripsi File (AES-256-GCM)
  {CYAN}2.{RESET}  🔓 Dekripsi File
  {CYAN}3.{RESET}  🔑 Generate RSA-4096 Keypair
  {CYAN}4.{RESET}  📨 RSA Encrypt/Decrypt Pesan
  {CYAN}5.{RESET}  ✍️  Ed25519 Sign/Verify
  {CYAN}6.{RESET}  🗝️  Vault — Simpan Rahasia
  {CYAN}7.{RESET}  🔍 Vault — Ambil Rahasia
  {CYAN}8.{RESET}  📊 Info Kriptografi
  {CYAN}0.{RESET}  Keluar
""")
        
        choice = input(f"{GOLD}  📡 Pilih (0-8): {RESET}").strip()
        
        if choice == "1":
            path = input("📂 Path file: ").strip()
            pwd = input("🔐 Password: ").strip()
            if os.path.exists(path):
                result, sig = encrypt_file(path, pwd)
                if result:
                    print(f"{GREEN}✅ File terenkripsi: {result}{RESET}")
                    if sig:
                        print(f"{DIM}🔐 Tanda tangan: {sig[:50]}...{RESET}")
            else:
                print(f"{RED}❌ File tidak ditemukan{RESET}")
            input(f"{DIM}Tekan Enter...{RESET}")
        
        elif choice == "2":
            path = input("📂 Path file .zuhri: ").strip()
            pwd = input("🔐 Password: ").strip()
            if os.path.exists(path):
                result, sig = decrypt_file(path, pwd)
                if result:
                    print(f"{GREEN}✅ File didekripsi: {result}{RESET}")
                    if sig:
                        print(f"{DIM}🔐 Tanda tangan: {sig[:50]}...{RESET}")
            else:
                print(f"{RED}❌ File tidak ditemukan{RESET}")
            input(f"{DIM}Tekan Enter...{RESET}")
        
        elif choice == "3":
            name = input("🏷️  Nama keypair (default: zuhri): ").strip() or "zuhri"
            generate_rsa_keypair(name)
            input(f"{DIM}Tekan Enter...{RESET}")
        
        elif choice == "4":
            print(f"  {CYAN}1.{RESET} Encrypt pesan")
            print(f"  {CYAN}2.{RESET} Decrypt pesan")
            sub = input("Pilih (1/2): ").strip()
            if sub == "1":
                msg = input("📝 Pesan: ").strip()
                pub = os.path.join(KEYS_DIR, "zuhri_public.pem")
                if os.path.exists(pub):
                    result = rsa_encrypt(msg, pub)
                    print(f"{GREEN}🔐 Ciphertext:{RESET}\n{result}")
                else:
                    print(f"{RED}❌ Generate RSA keypair dulu (menu 3){RESET}")
            elif sub == "2":
                ct = input("🔐 Ciphertext: ").strip()
                pwd = input("🔐 Password private key: ").strip()
                priv = os.path.join(KEYS_DIR, "zuhri_private.pem")
                if os.path.exists(priv):
                    try:
                        result = rsa_decrypt(ct, priv, pwd)
                        print(f"{GREEN}📨 Pesan:{RESET} {result}")
                    except:
                        print(f"{RED}❌ Dekripsi gagal{RESET}")
            input(f"{DIM}Tekan Enter...{RESET}")
        
        elif choice == "5":
            print(f"  {CYAN}1.{RESET} Generate keypair")
            print(f"  {CYAN}2.{RESET} Sign pesan")
            print(f"  {CYAN}3.{RESET} Verify")
            sub = input("Pilih (1/2/3): ").strip()
            if sub == "1":
                generate_ed25519_keypair()
            elif sub == "2":
                msg = input("📝 Pesan: ").strip()
                priv = os.path.join(KEYS_DIR, "zuhri_sign_private.key")
                if os.path.exists(priv):
                    sig = sign_message(msg, priv)
                    print(f"{GREEN}✍️  Signature:{RESET}\n{sig}")
            elif sub == "3":
                msg = input("📝 Pesan: ").strip()
                sig = input("✍️  Signature: ").strip()
                pub = os.path.join(KEYS_DIR, "zuhri_sign_public.key")
                if os.path.exists(pub):
                    valid = verify_signature(msg, sig, pub)
                    if valid:
                        print(f"{GREEN}✅ Tanda tangan VALID{RESET}")
                    else:
                        print(f"{RED}❌ Tanda tangan TIDAK VALID{RESET}")
            input(f"{DIM}Tekan Enter...{RESET}")
        
        elif choice == "6":
            name = input("🏷️  Nama rahasia: ").strip()
            value = input("🔐 Nilai rahasia: ").strip()
            pwd = input("🔐 Password vault: ").strip()
            vault_store(name, value, pwd)
            input(f"{DIM}Tekan Enter...{RESET}")
        
        elif choice == "7":
            name = input("🏷️  Nama rahasia: ").strip()
            pwd = input("🔐 Password vault: ").strip()
            result = vault_retrieve(name, pwd)
            if result:
                print(f"{GREEN}🗝️  Nilai:{RESET} {result}")
            input(f"{DIM}Tekan Enter...{RESET}")
        
        elif choice == "8":
            identity = load_identity() if ZUHRI_ID_OK else None
            print(f"""
{BOLD}{CYAN}📊 INFORMASI KRIPTOGRAFI{RESET}
{'─' * 55}
  {GOLD}AES-256-GCM{RESET}      → Enkripsi simetris (file)
  {GOLD}RSA-4096{RESET}         → Enkripsi asimetris (pesan)
  {GOLD}Ed25519{RESET}          → Tanda tangan digital
  {GOLD}PBKDF2-SHA256{RESET}   → 600.000 iterasi
  {GOLD}Vault{RESET}            → JSON terenkripsi

{BOLD}📂 LOKASI:{RESET}
  Crypto dir : {CRYPTO_DIR}
  Vault      : {VAULT_DIR}
  Keys       : {KEYS_DIR}
  Log        : {LOG_DIR}/verified.log

{BOLD}🆔 ZUHRI ID:{RESET}
  Status : {id_badge}
""")
            if identity:
                print(f"  ID     : {GOLD}{identity['zuhri_id']}{RESET}")
                print(f"  Nama   : {GOLD}{identity['name']}{RESET}")
            print(f"{'─' * 55}\n")
            input(f"{DIM}Tekan Enter...{RESET}")
        
        elif choice == "0":
            break

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    if not CRYPTO_OK:
        print(f"{RED}❌ Install: pip install cryptography{RESET}")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "info":
            print(f"ZUHRI CRYPTO — AES-256-GCM | RSA-4096 | Ed25519 | PBKDF2")
            print(f"ZUHRI ID : {get_id_badge()}")
        else:
            menu()
    else:
        menu()
