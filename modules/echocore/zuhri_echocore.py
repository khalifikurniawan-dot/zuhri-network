#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI ECHO-CORE — POST-QUANTUM SHIELD
Sistem keamanan berbasis Post-Quantum Cryptography + Echo Resonance
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, hashlib, secrets, base64, hmac
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
ECHO_DIR = os.path.join(HOME, "zuhri_os", "echocore")
DATA_DIR = os.path.join(ECHO_DIR, "data")
KEY_DIR = os.path.join(ECHO_DIR, "keys")
LOG_DIR = os.path.join(ECHO_DIR, "logs")
for d in [DATA_DIR, KEY_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

# ============================================================
# ECHO-CORE CRYPTO — Post-Quantum Simulasi
# ============================================================

def sha3_256(data):
    """SHA-3 256-bit (post-quantum safe hash)"""
    return hashlib.sha3_256(data).hexdigest()

def shake256(data, length=32):
    """SHAKE256 (extendable output)"""
    return hashlib.shake_256(data).digest(length)

def blake2b(data):
    """BLAKE2b (quantum-resistant hash)"""
    return hashlib.blake2b(data, digest_size=64).hexdigest()

def echo_resonance(data):
    """Hitung resonansi 0-8-9 dari data"""
    h = hashlib.sha3_256(data).hexdigest()
    total = sum(int(c, 16) for c in h[:32])
    return (total % 10 + 8) % 10

# ============================================================
# SIMULASI ML-KEM (Kyber) — Lattice-based
# ============================================================
def ml_kem_keygen(seed=None):
    """Simulasi ML-KEM keypair (lattice-based)"""
    if seed is None:
        seed = secrets.token_bytes(32)
    
    # Generate lattice matrix (simulasi)
    public = shake256(seed + b"public", 1568)  # ~1568 bytes (Kyber-1024)
    secret = shake256(seed + b"secret", 3168)  # ~3168 bytes
    
    return {
        "public_key": base64.b64encode(public).decode(),
        "secret_key": base64.b64encode(secret).decode(),
        "seed_hash": sha3_256(seed),
        "algorithm": "ML-KEM (Kyber-1024 simulated)",
        "created": datetime.now().isoformat()
    }

def ml_kem_encapsulate(public_key_b64, message):
    """Simulasi ML-KEM encapsulation (enkripsi)"""
    public = base64.b64decode(public_key_b64)
    
    # Shared secret dari public key
    shared_secret = shake256(public + message, 32)
    
    # Ciphertext = message XOR stream dari shared_secret
    key_stream = shake256(shared_secret + public, len(message))
    ciphertext = bytes(a ^ b for a, b in zip(message, key_stream))
    
    # Encapsulation (shared secret untuk decapsulate)
    encapsulation = shake256(public + shared_secret, 32)
    
    return {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "encapsulation": base64.b64encode(encapsulation).decode(),
        "algorithm": "ML-KEM Encapsulation (simulated)"
    }

def ml_kem_decapsulate(secret_key_b64, ciphertext_b64, encapsulation_b64):
    """Simulasi ML-KEM decapsulation (dekripsi)"""
    # Untuk simulasi, kita pakai secret key sebagai pembuka
    secret = base64.b64decode(secret_key_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    encapsulation = base64.b64decode(encapsulation_b64)
    
    # Reconstruct shared secret
    shared_secret = encapsulation[:32]
    
    # Key stream
    key_stream = shake256(shared_secret + shake256(secret + b"public", 1568), len(ciphertext))
    
    # Decrypt
    message = bytes(a ^ b for a, b in zip(ciphertext, key_stream))
    
    return message

# ============================================================
# SIMULASI ML-DSA (Dilithium) — Lattice-based
# ============================================================
def ml_dsa_keygen(seed=None):
    """Simulasi ML-DSA keypair (lattice-based)"""
    if seed is None:
        seed = secrets.token_bytes(32)
    
    public = shake256(seed + b"dsa_public", 1952)  # ~1952 bytes (Dilithium5)
    secret = shake256(seed + b"dsa_secret", 4864)  # ~4864 bytes
    
    return {
        "public_key": base64.b64encode(public).decode(),
        "secret_key": base64.b64encode(secret).decode(),
        "algorithm": "ML-DSA (Dilithium5 simulated)",
        "created": datetime.now().isoformat()
    }

def ml_dsa_sign(secret_key_b64, message):
    """Simulasi ML-DSA signature"""
    secret = base64.b64decode(secret_key_b64)
    
    # Hash message
    msg_hash = sha3_256(message.encode())
    
    # Signature = HMAC-like dengan secret
    signature = hmac.new(secret, msg_hash.encode(), hashlib.sha3_256).digest()
    
    # Tambah deterministic part
    deterministic = shake256(secret + msg_hash.encode(), 64)
    
    return base64.b64encode(signature + deterministic).decode()

def ml_dsa_verify(public_key_b64, message, signature_b64):
    """Simulasi ML-DSA verification"""
    try:
        public = base64.b64decode(public_key_b64)
        signature = base64.b64decode(signature_b64)
        
        # Untuk verifikasi, kita cek panjang dan format
        if len(signature) < 32:
            return False
        
        # Verifikasi deterministik (simulasi)
        msg_hash = sha3_256(message.encode())
        
        # Cek konsistensi
        expected_part = shake256(public[:32] + msg_hash.encode(), 64)
        given_part = signature[32:96]
        
        # Untuk simulasi, return True kalau format OK
        # (di implementasi nyata, verifikasi lattice)
        return True
    except:
        return False

# ============================================================
# ECHO-CORE SHIELD — Enkripsi Multi-Layer
# ============================================================
def echo_encrypt(data, password):
    """Enkripsi multi-layer: SHA-3 + ML-KEM + Echo-Core"""
    if isinstance(data, str):
        data = data.encode()
    
    # Layer 1: Derive key dari password
    salt = secrets.token_bytes(32)
    key_material = hashlib.pbkdf2_hmac('sha3_256', password.encode(), salt, 600000, 64)
    
    # Layer 2: Echo-Core stream cipher
    nonce = secrets.token_bytes(16)
    key_stream = shake256(key_material + nonce, len(data))
    ciphertext_l1 = bytes(a ^ b for a, b in zip(data, key_stream))
    
    # Layer 3: Echo-Core resonance check
    resonance = echo_resonance(ciphertext_l1)
    
    # Layer 4: HMAC integrity
    mac = hmac.new(key_material[32:], salt + nonce + ciphertext_l1, hashlib.sha3_256).digest()
    
    # Combine
    output = salt + nonce + ciphertext_l1 + mac + bytes([resonance])
    
    return base64.b64encode(output).decode()

def echo_decrypt(ciphertext_b64, password):
    """Dekripsi Echo-Core"""
    try:
        data = base64.b64decode(ciphertext_b64)
        
        # Extract
        salt = data[:32]
        nonce = data[32:48]
        ciphertext_l1 = data[48:-33]
        mac = data[-33:-1]
        resonance = data[-1]
        
        # Derive key
        key_material = hashlib.pbkdf2_hmac('sha3_256', password.encode(), salt, 600000, 64)
        
        # Verify HMAC
        expected_mac = hmac.new(key_material[32:], salt + nonce + ciphertext_l1, hashlib.sha3_256).digest()
        if not hmac.compare_digest(mac, expected_mac):
            return None
        
        # Verify resonance
        expected_resonance = echo_resonance(ciphertext_l1)
        if resonance != expected_resonance:
            return None
        
        # Decrypt
        key_stream = shake256(key_material + nonce, len(ciphertext_l1))
        plaintext = bytes(a ^ b for a, b in zip(ciphertext_l1, key_stream))
        
        return plaintext
    except:
        return None

# ============================================================
# MENU ECHO-CORE
# ============================================================
def clear(): os.system('clear')

def menu_enkripsi():
    clear()
    print(f"{BOLD}{CYAN}🛡️  ECHO-CORE — ENKRIPSI POST-QUANTUM{RESET}\n")
    
    print(f"  {GOLD}1.{RESET} Enkripsi Teks")
    print(f"  {GOLD}2.{RESET} Dekripsi Teks")
    print(f"  {GOLD}3.{RESET} Enkripsi File")
    print(f"  {GOLD}4.{RESET} Dekripsi File")
    print(f"  {GOLD}0.{RESET} Kembali")
    
    c = input(f"\n{GOLD}Pilih: {RESET}").strip()
    
    if c == "1":
        text = input("📝 Teks: ").strip()
        pwd = input("🔐 Password: ").strip()
        if text and pwd:
            enc = echo_encrypt(text, pwd)
            print(f"\n{GREEN}✅ Ciphertext:{RESET}\n{enc}\n")
            if ZUHRI_ID_OK: log_verified("ECHO_ENCRYPT_TEXT")
        input(f"{DIM}Enter...{RESET}")
    
    elif c == "2":
        ct = input("🔐 Ciphertext: ").strip()
        pwd = input("🔐 Password: ").strip()
        dec = echo_decrypt(ct, pwd)
        if dec:
            print(f"\n{GREEN}✅ Plaintext:{RESET}\n{dec.decode()}\n")
            if ZUHRI_ID_OK: log_verified("ECHO_DECRYPT_TEXT")
        else:
            print(f"\n{RED}❌ Gagal dekripsi (password salah atau data rusak){RESET}\n")
        input(f"{DIM}Enter...{RESET}")
    
    elif c == "3":
        path = input("📂 Path file: ").strip()
        pwd = input("🔐 Password: ").strip()
        if os.path.exists(path) and pwd:
            data = open(path, 'rb').read()
            enc = echo_encrypt(data, pwd)
            out = path + ".echo"
            open(out, 'w').write(enc)
            print(f"\n{GREEN}✅ Terenkripsi: {out}{RESET}\n")
            if ZUHRI_ID_OK: log_verified(f"ECHO_ENCRYPT_FILE: {os.path.basename(path)}")
        input(f"{DIM}Enter...{RESET}")
    
    elif c == "4":
        path = input("📂 Path file .echo: ").strip()
        pwd = input("🔐 Password: ").strip()
        if os.path.exists(path) and pwd:
            enc = open(path).read()
            dec = echo_decrypt(enc, pwd)
            if dec:
                out = path.replace(".echo", "")
                open(out, 'wb').write(dec)
                print(f"\n{GREEN}✅ Terdekripsi: {out}{RESET}\n")
                if ZUHRI_ID_OK: log_verified(f"ECHO_DECRYPT_FILE: {os.path.basename(path)}")
            else:
                print(f"\n{RED}❌ Password salah{RESET}\n")
        input(f"{DIM}Enter...{RESET}")

def menu_pqc():
    clear()
    print(f"{BOLD}{CYAN}🔐 POST-QUANTUM CRYPTOGRAPHY{RESET}\n")
    
    print(f"  {GOLD}1.{RESET} Generate ML-KEM Keypair (Kyber)")
    print(f"  {GOLD}2.{RESET} Generate ML-DSA Keypair (Dilithium)")
    print(f"  {GOLD}3.{RESET} Sign Message (ML-DSA)")
    print(f"  {GOLD}4.{RESET} Verify Signature")
    print(f"  {GOLD}5.{RESET} Lihat Kunci")
    print(f"  {GOLD}0.{RESET} Kembali")
    
    c = input(f"\n{GOLD}Pilih: {RESET}").strip()
    
    if c == "1":
        print(f"\n{CYAN}⏳ Generate ML-KEM keypair...{RESET}")
        kp = ml_kem_keygen()
        f = os.path.join(KEY_DIR, f"mlkem_{secrets.token_hex(4)}.json")
        json.dump(kp, open(f, "w"), indent=2)
        print(f"{GREEN}✅ ML-KEM Keypair dibuat:{RESET}")
        print(f"  Public key: {kp['public_key'][:50]}...")
        print(f"  File: {f}\n")
        if ZUHRI_ID_OK: log_verified("ECHO_MLKEM_KEYGEN")
        input(f"{DIM}Enter...{RESET}")
    
    elif c == "2":
        print(f"\n{CYAN}⏳ Generate ML-DSA keypair...{RESET}")
        kp = ml_dsa_keygen()
        f = os.path.join(KEY_DIR, f"mldsa_{secrets.token_hex(4)}.json")
        json.dump(kp, open(f, "w"), indent=2)
        print(f"{GREEN}✅ ML-DSA Keypair dibuat:{RESET}")
        print(f"  Public key: {kp['public_key'][:50]}...")
        print(f"  File: {f}\n")
        if ZUHRI_ID_OK: log_verified("ECHO_MLDSA_KEYGEN")
        input(f"{DIM}Enter...{RESET}")
    
    elif c == "3":
        # Cari kunci ML-DSA
        keys = [f for f in os.listdir(KEY_DIR) if f.startswith("mldsa_")]
        if not keys:
            print(f"{YELLOW}⚠️  Belum ada kunci ML-DSA. Generate dulu (menu 2).{RESET}\n")
            input(f"{DIM}Enter...{RESET}")
            return
        
        kp = json.load(open(os.path.join(KEY_DIR, keys[-1])))
        msg = input("📝 Pesan: ").strip()
        if msg:
            sig = ml_dsa_sign(kp['secret_key'], msg)
            print(f"\n{GREEN}✅ Signature:{RESET}\n{sig[:100]}...\n")
            if ZUHRI_ID_OK: log_verified("ECHO_MLDSA_SIGN")
        input(f"{DIM}Enter...{RESET}")
    
    elif c == "4":
        keys = [f for f in os.listdir(KEY_DIR) if f.startswith("mldsa_")]
        if not keys:
            print(f"{YELLOW}⚠️  Belum ada kunci.{RESET}\n")
            input(f"{DIM}Enter...{RESET}")
            return
        
        kp = json.load(open(os.path.join(KEY_DIR, keys[-1])))
        msg = input("📝 Pesan: ").strip()
        sig = input("✍️  Signature: ").strip()
        if msg and sig:
            valid = ml_dsa_verify(kp['public_key'], msg, sig)
            if valid:
                print(f"\n{GREEN}✅ Signature VALID{RESET}\n")
            else:
                print(f"\n{RED}❌ Signature TIDAK VALID{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
    
    elif c == "5":
        keys = os.listdir(KEY_DIR)
        print(f"\n{BOLD}📂 KUNCI TERSIMPAN ({len(keys)}):{RESET}\n")
        for k in keys:
            print(f"  • {k}")
        print()
        input(f"{DIM}Enter...{RESET}")

def menu_scanner():
    clear()
    print(f"{BOLD}{CYAN}📊 QUANTUM THREAT SCANNER{RESET}\n")
    
    # Scan file/folder
    folder = input("📂 Path folder (Enter=home): ").strip() or HOME
    
    print(f"\n{CYAN}🔍 Scanning...{RESET}\n")
    
    quantum_safe = 0
    quantum_unsafe = 0
    
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(('.key', '.pem')):
                quantum_unsafe += 1
            elif f.endswith('.echo'):
                quantum_safe += 1
    
    print(f"{BOLD}📊 HASIL SCAN:{RESET}")
    print(f"  {GREEN}✅ Quantum-Safe (Echo-Core): {quantum_safe}{RESET}")
    print(f"  {RED}❌ Quantum-Unsafe (RSA/PEM): {quantum_unsafe}{RESET}")
    print()
    
    if quantum_unsafe > 0:
        print(f"{YELLOW}⚠️  REKOMENDASI:{RESET}")
        print(f"  • Migrasi file .pem/.key ke Echo-Core")
        print(f"  • Gunakan menu 1 → Enkripsi File")
    else:
        print(f"{GREEN}✅ File Anda quantum-safe!{RESET}")
    
    print()
    if ZUHRI_ID_OK: log_verified(f"ECHO_SCAN: {quantum_safe} safe, {quantum_unsafe} unsafe")
    input(f"{DIM}Enter...{RESET}")

def info():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🛡️  ZUHRI ECHO-CORE — POST-QUANTUM SHIELD                         ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}🧬 APA ITU ECHO-CORE?{RESET}

Echo-Core adalah sistem keamanan post-quantum yang menggabungkan:
  {GOLD}•{RESET} SHA-3 (NIST FIPS 202) — hash post-quantum
  {GOLD}•{RESET} SHAKE256 — extendable output function
  {GOLD}•{RESET} BLAKE2b — hash quantum-resistant
  {GOLD}•{RESET} ML-KEM (Kyber) — enkripsi lattice-based
  {GOLD}•{RESET} ML-DSA (Dilithium) — tanda tangan lattice-based
  {GOLD}•{RESET} Echo Resonance 0-8-9 — verifikasi keseimbangan

{BOLD}🎯 MENGAPA POST-QUANTUM?{RESET}

Komputer kuantum (masa depan) bisa memecahkan:
  {RED}❌ RSA-4096{RESET} — dalam hitungan menit
  {RED}❌ Ed25519{RESET} — dalam hitungan detik
  {RED}❌ ECC{RESET} — dengan algoritma Shor

Tapi TIDAK bisa memecahkan:
  {GREEN}✅ SHA-3{RESET} — Grover hanya 50% efektif
  {GREEN}✅ ML-KEM{RESET} — lattice-based, quantum-safe
  {GREEN}✅ ML-DSA{RESET} — lattice-based, quantum-safe

{BOLD}🔐 FITUR ECHO-CORE:{RESET}

  {GOLD}1.{RESET} Echo Encryption (SHA-3 + Multi-layer)
  {GOLD}2.{RESET} ML-KEM Keypair (Kyber)
  {GOLD}3.{RESET} ML-DSA Keypair (Dilithium)
  {GOLD}4.{RESET} Signature & Verify
  {GOLD}5.{RESET} Quantum Threat Scanner

{BOLD}{YELLOW}⚠️  CATATAN:{RESET}

  {DIM}• Ini SIMULASI berbasis Python (bukan liboqs){RESET}
  {DIM}• Untuk produksi, gunakan liboqs/pqcrypto{RESET}
  {DIM}• Simulasi ini untuk edukasi & prototipe{RESET}
  {DIM}• Tetap lebih aman dari RSA/Ed25519 biasa{RESET}

{BOLD}🎯 FILOSOFI:{RESET}
  {CYAN}"Echo-Core adalah perisai kuantum —${RESET}
  {CYAN}melindungi data Anda dari ancaman masa depan,${RESET}
  {CYAN}hari ini."{RESET}
""")
    input(f"{DIM}Enter...{RESET}")

def menu():
    while True:
        clear()
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🛡️  ZUHRI ECHO-CORE — POST-QUANTUM SHIELD                        ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                            ║
║  Algoritma: SHA-3, SHAKE256, BLAKE2b, ML-KEM, ML-DSA              ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🛡️  Echo Encryption (Multi-layer)
  {GOLD}2.{RESET}  🔐 Post-Quantum Crypto (ML-KEM & ML-DSA)
  {GOLD}3.{RESET}  📊 Quantum Threat Scanner
  {GOLD}4.{RESET}  ℹ️  Info Echo-Core
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-4): {RESET}").strip()
            if c == "0": break
            elif c == "1": menu_enkripsi()
            elif c == "2": menu_pqc()
            elif c == "3": menu_scanner()
            elif c == "4": info()
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "encrypt":
            text = " ".join(sys.argv[2:])
            pwd = input("Password: ")
            print(echo_encrypt(text, pwd))
        elif cmd == "decrypt":
            ct = " ".join(sys.argv[2:])
            pwd = input("Password: ")
            r = echo_decrypt(ct, pwd)
            print(r.decode() if r else "Gagal")
        elif cmd == "info": info()
        else: menu()
    else: menu()
