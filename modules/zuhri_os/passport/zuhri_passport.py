#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI PASSPORT — IDENTITAS LINTAS NEGARA
Global Digital Identity dengan Zuhri ID
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os
import sys
import json
import base64
import hashlib
import secrets
from datetime import datetime

# ===== ZUHRI AUTH =====
sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified, get_status
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

# ===== KONFIGURASI =====
HOME = os.path.expanduser("~")
PASSPORT_DIR = os.path.join(HOME, "zuhri_os", "passport")
DATA_DIR = os.path.join(PASSPORT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

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
def get_id_badge():
    if not ZUHRI_ID_OK:
        return f"{YELLOW}⚠️  TANPA ZUHRI ID{RESET}"
    s = get_status()
    if s['active']:
        return f"{GREEN}✅ {s['name']} ({s['zuhri_id'][:20]}...){RESET}"
    return f"{YELLOW}⚠️  TANPA ZUHRI ID{RESET}"

def get_passport_file():
    identity = load_identity()
    if not identity:
        return None
    return os.path.join(DATA_DIR, f"passport_{identity['zuhri_id']}.json")

def compute_hash(data):
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()

# ============================================================
# BUAT PASSPORT
# ============================================================
def create_passport():
    """Buat passport digital lintas negara"""
    if not ZUHRI_ID_OK:
        print(f"{RED}❌ Butuh Zuhri ID{RESET}")
        return
    
    identity = load_identity()
    if not identity:
        print(f"{RED}❌ Zuhri ID tidak ditemukan{RESET}")
        return
    
    passport_file = get_passport_file()
    if os.path.exists(passport_file):
        confirm = input(f"{YELLOW}⚠️  Passport sudah ada. Buat baru? (y/n): {RESET}").strip().lower()
        if confirm != 'y':
            return
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🌍 ZUHRI PASSPORT — BUAT IDENTITAS LINTAS NEGARA              ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Isi data passport digital Anda: (semua opsional kecuali nama){RESET}
""")
    
    # Data dasar
    display_name = input(f"👤 Nama tampilan [{identity['name']}]: ").strip() or identity['name']
    country = input("🌍 Negara asal (opsional): ").strip() or "Global Citizen"
    city = input("🏙️  Kota (opsional): ").strip()
    languages = input("🗣️  Bahasa (pisah koma, misal: id,en): ").strip() or "id"
    skills = input("💼 Skill (pisah koma): ").strip()
    bio = input("📝 Bio singkat: ").strip()
    
    # Parsing
    lang_list = [l.strip() for l in languages.split(",") if l.strip()]
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    
    passport = {
        "passport_id": "ZP-" + secrets.token_hex(8).upper(),
        "zuhri_id": identity['zuhri_id'],
        "display_name": display_name,
        "country": country,
        "city": city,
        "languages": lang_list,
        "skills": skill_list,
        "bio": bio,
        "issued": datetime.now().isoformat(),
        "expires": None,
        "status": "active",
        "endorsements": [],
        "reputation": 0,
        "public_key": identity['public_key'],
        "protocol": "K-8.0",
        "gen": "ZUH-8-9-0-K-8.0",
        "signature": None,
        "hash": None
    }
    
    # Hash passport
    passport_hash = compute_hash({k: v for k, v in passport.items() if k not in ['signature', 'hash']})
    passport['hash'] = passport_hash
    
    # Tanda tangan
    sign_payload = f"{passport['passport_id']}|{passport_hash}|{identity['zuhri_id']}"
    sig = sign(sign_payload)
    if sig:
        passport['signature'] = sig
    
    # Simpan
    with open(passport_file, 'w') as f:
        json.dump(passport, f, indent=2)
    
    log_verified(f"PASSPORT_CREATE: {passport['passport_id']}")
    
    print(f"""
{BOLD}{GREEN}✅ PASSPORT DIBUAT!{RESET}

{GOLD}🛂 Passport ID:{RESET} {passport['passport_id']}
{GOLD}🆔 Zuhri ID:{RESET}    {identity['zuhri_id']}
{GOLD}👤 Nama:{RESET}        {display_name}
{GOLD}🌍 Negara:{RESET}      {country}
{GOLD}🏙️  Kota:{RESET}        {city or 'N/A'}
{GOLD}🗣️  Bahasa:{RESET}      {', '.join(lang_list)}
{GOLD}💼 Skill:{RESET}        {', '.join(skill_list) if skill_list else 'N/A'}
{GOLD}📝 Bio:{RESET}          {bio or 'N/A'}

{GOLD}🔐 Hash:{RESET} {passport_hash[:32]}...
{GOLD}✍️  Signature:{RESET} {sig[:40] if sig else 'N/A'}...

{GREEN}✅ Passport ini berlaku GLOBAL — lintas negara!{RESET}
""")

# ============================================================
# TAMPILKAN PASSPORT
# ============================================================
def show_passport():
    """Tampilkan passport"""
    identity = load_identity()
    if not identity:
        print(f"{RED}❌ Zuhri ID tidak ditemukan{RESET}")
        return
    
    passport_file = get_passport_file()
    if not os.path.exists(passport_file):
        print(f"{YELLOW}⚠️  Belum ada passport. Buat dulu: passport create{RESET}")
        return
    
    passport = json.load(open(passport_file))
    
    # Cek signature valid?
    passport_copy = {k: v for k, v in passport.items() if k not in ['signature']}
    sig = passport['signature']
    sign_payload = f"{passport['passport_id']}|{passport['hash']}|{passport['zuhri_id']}"
    sig_valid = verify(sign_payload, sig, passport['public_key']) if sig else False
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🌍 ZUHRI PASSPORT — IDENTITAS LINTAS NEGARA                   ║
║  ═══════════════════════════════════════════════════════════════  ║
║                                                                  ║
║    🛂 Passport ID : {GOLD}{passport['passport_id']}{RESET}
║    🆔 Zuhri ID    : {GOLD}{passport['zuhri_id']}{RESET}
║    👤 Nama        : {GOLD}{passport['display_name']}{RESET}
║    🌍 Negara      : {GOLD}{passport['country']}{RESET}
║    🏙️  Kota        : {GOLD}{passport['city'] or 'N/A'}{RESET}
║    🗣️  Bahasa      : {GOLD}{', '.join(passport['languages'])}{RESET}
║    💼 Skill       : {GOLD}{', '.join(passport['skills']) if passport['skills'] else 'N/A'}{RESET}
║    📝 Bio         : {GOLD}{passport['bio'] or 'N/A'}{RESET}
║                                                                  ║
║  ═══════════════════════════════════════════════════════════════  ║
║    📅 Diterbitkan  : {GOLD}{passport['issued'][:19]}{RESET}
║    🔐 Status       : {GREEN}✅ ACTIVE{RESET}
║    ⭐ Reputasi     : {GOLD}{passport['reputation']}{RESET}
║    🤝 Endorsements : {GOLD}{len(passport['endorsements'])}{RESET}
║    ✍️  Signature    : {GREEN + '✅ VALID' + RESET if sig_valid else RED + '❌ INVALID' + RESET}
║                                                                  ║
{BOLD}{CYAN}╚══════════════════════════════════════════════════════════════════╝{RESET}

{GOLD}🔑 Hash:{RESET} {passport['hash']}
""")

# ============================================================
# EXPORT PASSPORT (UNTUK SHARING)
# ============================================================
def export_passport():
    """Export passport (public only)"""
    identity = load_identity()
    passport_file = get_passport_file()
    
    if not os.path.exists(passport_file):
        print(f"{YELLOW}⚠️  Belum ada passport{RESET}")
        return
    
    passport = json.load(open(passport_file))
    
    # Hapus data sensitif
    export = passport.copy()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_file = os.path.join(DATA_DIR, f"export_{timestamp}.json")
    
    with open(export_file, 'w') as f:
        json.dump(export, f, indent=2)
    
    print(f"""
{BOLD}{GREEN}✅ PASSPORT DI-EXPORT!{RESET}

{GOLD}📄 File:{RESET} {export_file}

{GOLD}Isi:{RESET}
{json.dumps(export, indent=2)}

{DIM}⚠️  File ini AMAN dibagikan — berisi public key, bukan private key.{RESET}
""")

# ============================================================
# VERIFIKASI PASSPORT ORANG LAIN
# ============================================================
def verify_passport():
    """Verifikasi passport dari file"""
    path = input("📂 Path file passport: ").strip()
    if not os.path.exists(path):
        print(f"{RED}❌ File tidak ditemukan{RESET}")
        return
    
    try:
        passport = json.load(open(path))
    except:
        print(f"{RED}❌ File bukan JSON valid{RESET}")
        return
    
    print(f"""
{BOLD}{CYAN}🔐 VERIFIKASI PASSPORT{RESET}
{'─' * 65}
  Passport ID : {passport.get('passport_id', 'N/A')}
  Nama        : {passport.get('display_name', 'N/A')}
  Zuhri ID    : {passport.get('zuhri_id', 'N/A')}
  Negara      : {passport.get('country', 'N/A')}
{'─' * 65}
""")
    
    # Verifikasi hash
    passport_copy = {k: v for k, v in passport.items() if k not in ['signature']}
    expected_hash = compute_hash({k: v for k, v in passport_copy.items() if k not in ['hash']})
    
    print(f"  {GOLD}Hash Tersimpan:{RESET} {passport.get('hash', 'N/A')[:32]}...")
    print(f"  {GOLD}Hash Dihitung:{RESET} {expected_hash[:32]}...")
    
    hash_ok = passport.get('hash') == expected_hash
    if hash_ok:
        print(f"  {GREEN}✅ Hash COCOK — Passport ASLI{RESET}")
    else:
        print(f"  {RED}❌ Hash TIDAK COCOK — Passport DIUBAH!{RESET}")
    
    # Verifikasi signature
    sig = passport.get('signature')
    pub = passport.get('public_key')
    
    if sig and pub:
        sign_payload = f"{passport['passport_id']}|{passport['hash']}|{passport['zuhri_id']}"
        if verify(sign_payload, sig, pub):
            print(f"  {GREEN}✅ Signature VALID — Diterbitkan oleh pemilik ID{RESET}")
        else:
            print(f"  {RED}❌ Signature TIDAK VALID{RESET}")
    else:
        print(f"  {YELLOW}⚠️  Tidak ada signature{RESET}")
    
    print(f"{'─' * 65}\n")

# ============================================================
# ENDORSEMENT (REPUTASI)
# ============================================================
def endorse():
    """Endorse passport orang lain"""
    identity = load_identity()
    if not identity:
        print(f"{RED}❌ Butuh Zuhri ID{RESET}")
        return
    
    path = input("📂 Path passport target: ").strip()
    if not os.path.exists(path):
        print(f"{RED}❌ File tidak ditemukan{RESET}")
        return
    
    try:
        target = json.load(open(path))
    except:
        print(f"{RED}❌ File tidak valid{RESET}")
        return
    
    if target['zuhri_id'] == identity['zuhri_id']:
        print(f"{RED}❌ Tidak bisa endorse diri sendiri{RESET}")
        return
    
    message = input("💬 Pesan endorsement: ").strip() or "Trusted!"
    
    # Buat endorsement
    endorsement = {
        "from": identity['zuhri_id'],
        "from_name": identity['name'],
        "message": message,
        "time": datetime.now().isoformat()
    }
    
    # Tanda tangani
    end_str = json.dumps(endorsement, sort_keys=True)
    sig = sign(end_str)
    if sig:
        endorsement['signature'] = sig
        endorsement['public_key'] = identity['public_key']
    
    # Simpan ke file endorsements
    end_file = os.path.join(DATA_DIR, f"endorsements_{target['zuhri_id']}.json")
    
    endorsements = []
    if os.path.exists(end_file):
        endorsements = json.load(open(end_file))
    
    endorsements.append(endorsement)
    
    with open(end_file, 'w') as f:
        json.dump(endorsements, f, indent=2)
    
    log_verified(f"ENDORSE: {target['passport_id']} — {message[:50]}")
    
    print(f"""
{BOLD}{GREEN}✅ ENDORSEMENT BERHASIL!{RESET}

{GOLD}Target:{RESET}  {target['display_name']} ({target['passport_id']})
{GOLD}Dari:{RESET}    {identity['name']}
{GOLD}Pesan:{RESET}   {message}
{GOLD}Signature:{RESET} {sig[:40]}...
""")

# ============================================================
# LIST PASSPORTS
# ============================================================
def list_passports():
    """Lihat semua passport"""
    files = [f for f in os.listdir(DATA_DIR) if f.startswith('passport_') and f.endswith('.json')]
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🌍 DAFTAR PASSPORT                                            ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    if not files:
        print(f"{YELLOW}Belum ada passport.{RESET}\n")
        return
    
    for i, f in enumerate(files, 1):
        p = json.load(open(os.path.join(DATA_DIR, f)))
        print(f"  {GOLD}{i}.{RESET} {BOLD}{p['display_name']}{RESET} ({p['country']})")
        print(f"     {DIM}ID: {p['passport_id']} | Zuhri: {p['zuhri_id'][:24]}... | Reputasi: {p['reputation']}{RESET}")
    print()

# ============================================================
# HELP
# ============================================================
def show_help():
    print(f"""
{BOLD}{CYAN}🌍 ZUHRI PASSPORT — BANTUAN{RESET}
{'─' * 55}
  {BOLD}passport create{RESET}    → Buat passport lintas negara
  {BOLD}passport show{RESET}      → Tampilkan passport Anda
  {BOLD}passport export{RESET}    → Export passport (public)
  {BOLD}passport verify{RESET}    → Verifikasi passport
  {BOLD}passport endorse{RESET}   → Beri endorsement
  {BOLD}passport list{RESET}      → Daftar passport
  {BOLD}passport help{RESET}      → Bantuan
{'─' * 55}
  Operator: {get_id_badge()}
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
    
    if cmd == "create":
        create_passport()
    elif cmd == "show":
        show_passport()
    elif cmd == "export":
        export_passport()
    elif cmd == "verify":
        verify_passport()
    elif cmd == "endorse":
        endorse()
    elif cmd == "list":
        list_passports()
    elif cmd == "help":
        show_help()
    else:
        show_help()
