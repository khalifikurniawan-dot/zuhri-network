#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI DID — DECENTRALIZED IDENTIFIER
Identitas terdesentralisasi berbasis Zuhri ID
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, base64, hashlib, secrets
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
DID_DIR = os.path.join(HOME, "zuhri_os", "did")
DATA_DIR = os.path.join(DID_DIR, "data")
DOCS_DIR = os.path.join(DID_DIR, "docs")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# UTIL
# ============================================================
def did_file():
    if not ZUHRI_ID_OK: return None
    i = load_identity()
    if not i: return None
    return os.path.join(DATA_DIR, f"did_{i['zuhri_id']}.json")

def compute_hash(data):
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()

def get_id_badge():
    if not ZUHRI_ID_OK: return f"{YELLOW}⚠️  TANPA ID{RESET}"
    i = load_identity()
    return f"{GREEN}✅ {i['name']}{RESET}" if i else f"{YELLOW}⚠️{RESET}"

# ============================================================
# BUAT DID
# ============================================================
def create_did():
    if not ZUHRI_ID_OK:
        print(f"{RED}❌ Butuh Zuhri ID{RESET}")
        input(f"{DIM}Enter...{RESET}"); return
    
    identity = load_identity()
    f = did_file()
    
    if os.path.exists(f):
        confirm = input(f"{YELLOW}⚠️  DID sudah ada. Buat baru? (y/n): {RESET}").strip().lower()
        if confirm != 'y': return
    
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🆔 ZUHRI DID — BUAT DECENTRALIZED ID                          ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{DIM}DID Anda akan dibuat dari Zuhri ID yang sudah ada.{RESET}
""")
    
    # DID = did:zuhri:<hash dari zuhri_id>
    did_hash = hashlib.sha256(identity['zuhri_id'].encode()).hexdigest()[:40]
    did = f"did:zuhri:{did_hash}"
    
    # DID Document
    did_doc = {
        "@context": ["https://www.w3.org/ns/did/v1"],
        "id": did,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "zuhri_id": identity['zuhri_id'],
        "verificationMethod": [{
            "id": f"{did}#key-1",
            "type": "Ed25519VerificationKey2020",
            "controller": did,
            "publicKeyBase64": identity['public_key']
        }],
        "authentication": [f"{did}#key-1"],
        "assertionMethod": [f"{did}#key-1"],
        "service": [{
            "id": f"{did}#zuhri-network",
            "type": "ZuhriNetwork",
            "serviceEndpoint": "zuhri://local"
        }],
        "claims": {
            "name": identity['name'],
            "role": identity.get('role', 'Operator'),
            "protocol": "K-8.0",
            "gen": "ZUH-8-9-0-K-8.0"
        },
        "hash": None,
        "signature": None,
        "public_key": identity['public_key']
    }
    
    # Hash DID document (tanpa hash & signature)
    doc_copy = {k: v for k, v in did_doc.items() if k not in ['hash', 'signature']}
    did_doc['hash'] = compute_hash(doc_copy)
    
    # Tanda tangan
    sig = sign(did_doc['hash'])
    if sig:
        did_doc['signature'] = sig
    
    # Simpan
    json.dump(did_doc, open(f, "w"), indent=2)
    
    log_verified(f"DID_CREATE: {did}")
    
    print(f"""
{BOLD}{GREEN}╔══════════════════════════════════════════════════════════════════╗
║  ✅ DID BERHASIL DIBUAT!                                       ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}DID{RESET}       : {did}
  {GOLD}Zuhri ID{RESET}  : {identity['zuhri_id']}
  {GOLD}Hash{RESET}      : {did_doc['hash'][:32]}...
  {GOLD}Signature{RESET} : {'✅' if sig else '❌'}

{DIM}DID Anda bisa diverifikasi tanpa server pusat.{RESET}
""")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# LIHAT DID
# ============================================================
def show_did():
    f = did_file()
    if not f or not os.path.exists(f):
        print(f"{YELLOW}⚠️  Belum ada DID. Buat dulu: menu 1{RESET}\n")
        input(f"{DIM}Enter...{RESET}"); return
    
    doc = json.load(open(f))
    
    # Verifikasi
    doc_copy = {k: v for k, v in doc.items() if k not in ['hash', 'signature']}
    h = compute_hash(doc_copy)
    hash_ok = h == doc['hash']
    sig_ok = verify(doc['hash'], doc.get('signature', ''), doc.get('public_key', ''))
    
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🆔 ZUHRI DID — DECENTRALIZED IDENTIFIER                       ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}DID{RESET}         : {doc['id']}
  {GOLD}Zuhri ID{RESET}    : {doc['zuhri_id']}
  {GOLD}Dibuat{RESET}      : {doc['created'][:19]}
  {GOLD}Diupdate{RESET}    : {doc['updated'][:19]}

{BOLD}👤 CLAIMS:{RESET}
  {GOLD}Nama{RESET}        : {doc['claims']['name']}
  {GOLD}Role{RESET}        : {doc['claims']['role']}
  {GOLD}Protokol{RESET}    : {doc['claims']['protocol']}

{BOLD}🔑 VERIFICATION:{RESET}
  {GOLD}Method{RESET}      : {doc['verificationMethod'][0]['type']}
  {GOLD}Public Key{RESET}  : {doc['verificationMethod'][0]['publicKeyBase64'][:40]}...

{BOLD}📊 STATUS:{RESET}
  {GOLD}Hash{RESET}        : {'✅ VALID' if hash_ok else '❌ INVALID'}
  {GOLD}Signature{RESET}   : {'✅ VALID' if sig_ok else '❌ INVALID'}
  {GOLD}DID{RESET}         : {'✅ SELF-SOVEREIGN' if (hash_ok and sig_ok) else '❌ TAMPERED'}
""")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# EXPORT DID
# ============================================================
def export_did():
    f = did_file()
    if not f or not os.path.exists(f):
        print(f"{YELLOW}⚠️  Belum ada DID.{RESET}\n")
        input(f"{DIM}Enter...{RESET}"); return
    
    doc = json.load(open(f))
    did_clean = doc['id'].replace(':', '_')
    export_file = os.path.join(DOCS_DIR, f"{did_clean}.json")
    json.dump(doc, open(export_file, "w"), indent=2)
    
    # Copy ke sdcard
    try:
        sdcard = "/sdcard/Download"
        if os.path.exists(sdcard):
            import shutil
            shutil.copy2(export_file, sdcard)
            print(f"{GREEN}✅ Export: {sdcard}/{os.path.basename(export_file)}{RESET}")
    except: pass
    
    print(f"\n{GREEN}✅ DID Document diexport: {export_file}{RESET}\n")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# VERIFIKASI DID LAIN
# ============================================================
def verify_did():
    os.system('clear')
    print(f"\n{BOLD}{CYAN}🔍 VERIFIKASI DID — Pihak Lain{RESET}\n")
    path = input("📂 Path file DID: ").strip()
    
    if not os.path.exists(path):
        print(f"{RED}❌ File tidak ditemukan{RESET}\n")
        input(f"{DIM}Enter...{RESET}"); return
    
    try:
        doc = json.load(open(path))
    except:
        print(f"{RED}❌ File bukan JSON valid{RESET}\n")
        input(f"{DIM}Enter...{RESET}"); return
    
    # Verifikasi hash
    doc_copy = {k: v for k, v in doc.items() if k not in ['hash', 'signature']}
    h = compute_hash(doc_copy)
    hash_ok = h == doc.get('hash', '')
    
    # Verifikasi signature
    sig_ok = verify(doc.get('hash', ''), doc.get('signature', ''), doc.get('public_key', ''))
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🔍 HASIL VERIFIKASI DID                                       ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}DID{RESET}       : {doc.get('id', 'N/A')}
  {GOLD}Nama{RESET}      : {doc.get('claims', {}).get('name', 'N/A')}
  {GOLD}Role{RESET}      : {doc.get('claims', {}).get('role', 'N/A')}

{BOLD}📊 VERIFIKASI:{RESET}
  Hash      : {'✅ VALID' if hash_ok else '❌ INVALID'}
  Signature : {'✅ VALID' if sig_ok else '❌ INVALID'}

{BOLD}Status:{RESET} {'✅ DID ASLI — Tidak ada tampering' if (hash_ok and sig_ok) else '❌ DID PALSU / DIUBAH'}
""")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# TAMBAH CLAIM
# ============================================================
def add_claim():
    f = did_file()
    if not f or not os.path.exists(f):
        print(f"{YELLOW}⚠️  Belum ada DID.{RESET}\n")
        input(f"{DIM}Enter...{RESET}"); return
    
    doc = json.load(open(f))
    
    os.system('clear')
    print(f"\n{BOLD}{CYAN}➕ TAMBAH CLAIM KE DID{RESET}\n")
    
    claim_type = input("📋 Tipe claim (mis: skill, sertifikat, alamat): ").strip()
    claim_value = input("📝 Nilai claim: ").strip()
    
    if not claim_type or not claim_value:
        return
    
    doc['claims'][claim_type] = claim_value
    doc['updated'] = datetime.now().isoformat()
    
    # Re-hash & re-sign
    doc_copy = {k: v for k, v in doc.items() if k not in ['hash', 'signature']}
    doc['hash'] = compute_hash(doc_copy)
    sig = sign(doc['hash'])
    if sig: doc['signature'] = sig
    
    json.dump(doc, open(f, "w"), indent=2)
    
    log_verified(f"DID_CLAIM_ADD: {claim_type}")
    
    print(f"\n{GREEN}✅ Claim '{claim_type}' ditambahkan{RESET}\n")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        f = did_file()
        has_did = f and os.path.exists(f)
        
        # Ambil info DID
        did_id = "Belum dibuat"
        if has_did:
            try:
                doc = json.load(open(f))
                did_id = doc['id'][:40] + "..."
            except: pass
        
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🆔 ZUHRI DID — DECENTRALIZED IDENTIFIER                       ║
║  ──────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                       ║
║  Operator: {get_id_badge()}
║  DID: {GOLD}{did_id}{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  ➕ Buat DID Baru
  {GOLD}2.{RESET}  👁️  Lihat DID Saya
  {GOLD}3.{RESET}  📤 Export DID Document
  {GOLD}4.{RESET}  🔍 Verifikasi DID Lain
  {GOLD}5.{RESET}  📝 Tambah Claim
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-5): {RESET}").strip()
            if c == "0": break
            elif c == "1": create_did()
            elif c == "2": show_did()
            elif c == "3": export_did()
            elif c == "4": verify_did()
            elif c == "5": add_claim()
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "create": create_did()
        elif cmd == "show": show_did()
        elif cmd == "verify": verify_did()
        elif cmd == "export": export_did()
        else: menu()
    else: menu()
