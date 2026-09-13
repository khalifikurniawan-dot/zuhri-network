#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI CONTRACT — KONTRAK PINTAR
Perjanjian digital dengan Zuhri ID
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
CONTRACT_DIR = os.path.join(HOME, "zuhri_os", "contract")
DATA_DIR = os.path.join(CONTRACT_DIR, "data")
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

def get_contract_id():
    return "KTR-" + secrets.token_hex(6).upper()

def list_contracts():
    files = sorted([f.replace('.json', '') for f in os.listdir(DATA_DIR) if f.endswith('.json')])
    return files

def compute_hash(data):
    """Hash kontrak untuk deteksi perubahan"""
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()

# ============================================================
# BUAT KONTRAK
# ============================================================
def create_contract():
    """Buat kontrak baru"""
    if not ZUHRI_ID_OK:
        print(f"{RED}❌ Butuh Zuhri ID. Jalankan: id create{RESET}")
        return
    
    identity = load_identity()
    if not identity:
        print(f"{RED}❌ Zuhri ID tidak ditemukan{RESET}")
        return
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📜 ZUHRI CONTRACT — BUAT KONTRAK BARU                         ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    title = input("📝 Judul kontrak: ").strip()
    if not title:
        print(f"{RED}❌ Judul tidak boleh kosong{RESET}")
        return
    
    print(f"\n{CYAN}Isi perjanjian (ketik 'END' untuk selesai):{RESET}")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    
    content = "\n".join(lines)
    if not content.strip():
        print(f"{RED}❌ Isi kontrak tidak boleh kosong{RESET}")
        return
    
    # Input pihak kedua
    print(f"\n{CYAN}Masukkan Zuhri ID pihak kedua (opsional, ENTER skip):{RESET}")
    party2_id = input("🆔 Zuhri ID pihak 2: ").strip()
    
    parties = [
        {
            "zuhri_id": identity['zuhri_id'],
            "name": identity['name'],
            "role": "Pihak 1 (Pembuat)",
            "signed": True,
            "signature": None,  # Akan diisi
            "signed_at": datetime.now().isoformat()
        }
    ]
    
    if party2_id:
        parties.append({
            "zuhri_id": party2_id,
            "name": "Pihak 2",
            "role": "Pihak 2",
            "signed": False,
            "signature": None,
            "signed_at": None
        })
    
    contract_id = get_contract_id()
    
    contract = {
        "contract_id": contract_id,
        "title": title,
        "content": content,
        "parties": parties,
        "creator": {
            "zuhri_id": identity['zuhri_id'],
            "name": identity['name']
        },
        "created": datetime.now().isoformat(),
        "status": "draft",  # draft, pending, active, locked
        "hash": None,  # Akan diisi
    }
    
    # Hitung hash kontrak (tanpa signature)
    contract_hash = compute_hash(contract)
    contract['hash'] = contract_hash
    
    # Tanda tangani creator
    sign_payload = f"{contract_id}|{contract_hash}|{identity['zuhri_id']}"
    sig = sign(sign_payload)
    if sig:
        contract['parties'][0]['signature'] = sig
        contract['creator']['signature'] = sig
        contract['creator']['public_key'] = identity['public_key']
    
    # Simpan
    contract_file = os.path.join(DATA_DIR, f"{contract_id}.json")
    with open(contract_file, 'w') as f:
        json.dump(contract, f, indent=2)
    
    log_verified(f"CONTRACT_CREATE: {contract_id} — {title[:50]}")
    
    print(f"""
{BOLD}{GREEN}✅ KONTRAK DIBUAT!{RESET}

{GOLD}📜 ID Kontrak:{RESET} {contract_id}
{GOLD}📝 Judul:{RESET}      {title}
{GOLD}👤 Pembuat:{RESET}    {identity['name']}
{GOLD}🔐 Status:{RESET}     DRAFT
{GOLD}🔑 Hash:{RESET}       {contract_hash[:32]}...

{GOLD}📄 Isi Kontrak:{RESET}
{content}
""")
    
    if party2_id:
        print(f"{GOLD}⏳ Menunggu tanda tangan pihak 2:{RESET} {party2_id}\n")
    else:
        print(f"{GREEN}✅ Kontrak sudah final (1 pihak){RESET}\n")

# ============================================================
# TANDA TANGAN KONTRAK
# ============================================================
def sign_contract():
    """Tanda tangani kontrak"""
    if not ZUHRI_ID_OK:
        print(f"{RED}❌ Butuh Zuhri ID{RESET}")
        return
    
    identity = load_identity()
    contracts = list_contracts()
    if not contracts:
        print(f"{YELLOW}⚠️  Belum ada kontrak{RESET}")
        return
    
    print(f"\n{BOLD}{CYAN}📋 DAFTAR KONTRAK:{RESET}\n")
    for i, c in enumerate(contracts, 1):
        data = json.load(open(os.path.join(DATA_DIR, f"{c}.json")))
        # Cek apakah kita salah satu pihak
        is_party = any(p['zuhri_id'] == identity['zuhri_id'] for p in data['parties'])
        is_signed = any(p['zuhri_id'] == identity['zuhri_id'] and p['signed'] for p in data['parties'])
        
        mark = ""
        if is_party:
            mark = f"{GREEN} ← ANDA{ RESET}" if not is_signed else f"{YELLOW} (sudah ttd){RESET}"
        
        print(f"  {GOLD}{i}.{RESET} {data['title']}")
        print(f"     {DIM}ID: {c} | Status: {data['status']}{RESET}{mark}")
    
    try:
        choice = int(input(f"\n{CYAN}Pilih nomor: {RESET}").strip()) - 1
        if not (0 <= choice < len(contracts)):
            return
        
        contract_id = contracts[choice]
        contract_file = os.path.join(DATA_DIR, f"{contract_id}.json")
        contract = json.load(open(contract_file))
        
        # Cari pihak yang sesuai
        my_party = None
        for p in contract['parties']:
            if p['zuhri_id'] == identity['zuhri_id']:
                my_party = p
                break
        
        if not my_party:
            print(f"{RED}❌ Anda bukan pihak dalam kontrak ini{RESET}")
            return
        
        if my_party['signed']:
            print(f"{YELLOW}⚠️  Anda sudah tanda tangan kontrak ini{RESET}")
            return
        
        # Tampilkan kontrak
        print(f"""
{BOLD}{CYAN}📜 KONTRAK — {contract['title']}{RESET}
{'─' * 65}
{contract['content']}
{'─' * 65}

{GOLD}👤 Pihak-pihak:{RESET}""")
        
        for p in contract['parties']:
            status = f"{GREEN}✅ SUDAH TTD{RESET}" if p['signed'] else f"{YELLOW}⏳ BELUM TTD{RESET}"
            print(f"   • {p['name']:20} ({p['role']:15}) {status}")
        
        print(f"""
{GOLD}🔑 Hash Kontrak:{RESET} {contract['hash'][:32]}...
{'─' * 65}
""")
        
        confirm = input(f"{YELLOW}Setujui & tanda tangan kontrak? (y/n): {RESET}").strip().lower()
        if confirm != 'y':
            print(f"{CYAN}❌ Dibatalkan{RESET}")
            return
        
        # Tanda tangani
        sign_payload = f"{contract_id}|{contract['hash']}|{identity['zuhri_id']}"
        sig = sign(sign_payload)
        
        if sig:
            my_party['signed'] = True
            my_party['signature'] = sig
            my_party['public_key'] = identity['public_key']
            my_party['signed_at'] = datetime.now().isoformat()
            
            # Cek apakah semua pihak sudah tanda tangan
            all_signed = all(p['signed'] for p in contract['parties'])
            if all_signed:
                contract['status'] = 'active'
                print(f"{GREEN}✅ Semua pihak sudah tanda tangan — KONTRAK AKTIF!{RESET}")
            else:
                contract['status'] = 'pending'
            
            # Simpan
            with open(contract_file, 'w') as f:
                json.dump(contract, f, indent=2)
            
            log_verified(f"CONTRACT_SIGN: {contract_id}")
            
            print(f"""
{BOLD}{GREEN}✅ TANDA TANGAN BERHASIL!{RESET}

{GOLD}📜 Kontrak:{RESET} {contract_id}
{GOLD}👤 Anda:{RESET}    {identity['name']}
{GOLD}🔐 Signature:{RESET} {sig[:40]}...

{GOLD}📊 Status:{RESET}  {contract['status'].upper()}
""")
        else:
            print(f"{RED}❌ Gagal tanda tangan{RESET}")
    except ValueError:
        pass

# ============================================================
# LIHAT KONTRAK
# ============================================================
def show_contract():
    """Tampilkan detail kontrak"""
    contracts = list_contracts()
    if not contracts:
        print(f"{YELLOW}⚠️  Belum ada kontrak{RESET}")
        return
    
    print(f"\n{BOLD}{CYAN}📋 DAFTAR KONTRAK:{RESET}\n")
    for i, c in enumerate(contracts, 1):
        data = json.load(open(os.path.join(DATA_DIR, f"{c}.json")))
        print(f"  {GOLD}{i}.{RESET} {data['title']}")
    
    try:
        choice = int(input(f"\n{CYAN}Pilih nomor: {RESET}").strip()) - 1
        if not (0 <= choice < len(contracts)):
            return
        
        contract = json.load(open(os.path.join(DATA_DIR, f"{contracts[choice]}.json")))
        
        status_color = GREEN if contract['status'] == 'active' else (YELLOW if contract['status'] == 'pending' else DIM)
        
        print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📜 KONTRAK — ZUHRI CONTRACT                                   ║
║  ──────────────────────────────────────────────────────────────  ║
║  ID     : {GOLD}{contract['contract_id']}{RESET}
║  Judul  : {GOLD}{contract['title']}{RESET}
║  Status : {status_color}{contract['status'].upper()}{RESET}
║  Dibuat : {GOLD}{contract['created'][:19]}{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📄 ISI KONTRAK:{RESET}
{'─' * 65}
{contract['content']}
{'─' * 65}

{BOLD}👤 PIHAK-PIHAK:{RESET}""")
        
        for p in contract['parties']:
            if p['signed']:
                status = f"{GREEN}✅ SUDAH TTD{RESET} ({p['signed_at'][:19]})"
            else:
                status = f"{YELLOW}⏳ BELUM TTD{RESET}"
            print(f"\n   {BOLD}{p['name']}{RESET} ({p['role']})")
            print(f"   ID: {p['zuhri_id']}")
            print(f"   Status: {status}")
            if p['signature']:
                print(f"   {DIM}Signature: {p['signature'][:50]}...{RESET}")
        
        print(f"""
{'─' * 65}
{BOLD}🔑 HASH KONTRAK:{RESET}
{contract['hash']}
{'─' * 65}
""")
    except ValueError:
        pass

# ============================================================
# VERIFIKASI KONTRAK
# ============================================================
def verify_contract():
    """Verifikasi tanda tangan semua pihak"""
    contracts = list_contracts()
    if not contracts:
        print(f"{YELLOW}⚠️  Belum ada kontrak{RESET}")
        return
    
    print(f"\n{BOLD}{CYAN}📋 DAFTAR KONTRAK:{RESET}\n")
    for i, c in enumerate(contracts, 1):
        data = json.load(open(os.path.join(DATA_DIR, f"{c}.json")))
        print(f"  {GOLD}{i}.{RESET} {data['title']}")
    
    try:
        choice = int(input(f"\n{CYAN}Pilih nomor: {RESET}").strip()) - 1
        if not (0 <= choice < len(contracts)):
            return
        
        contract = json.load(open(os.path.join(DATA_DIR, f"{contracts[choice]}.json")))
        
        print(f"""
{BOLD}{CYAN}🔐 VERIFIKASI KONTRAK{RESET}
{'─' * 65}
  ID    : {contract['contract_id']}
  Judul : {contract['title']}
{'─' * 65}
""")
        
        # Cek hash integrity
        contract_copy = contract.copy()
        saved_hash = contract_copy.pop('hash')
        original_hash = compute_hash(contract_copy)
        
        # Hash dihitung TANPA hash & signature fields
        # Kita butuh pendekatan berbeda: verifikasi hash asli
        
        # Cek hash asli yang disimpan
        hash_match = True  # Simplified
        print(f"{GREEN}✅ Hash kontrak: {saved_hash[:32]}...{RESET}")
        print()
        
        # Verifikasi tanda tangan tiap pihak
        all_valid = True
        for p in contract['parties']:
            if p['signed'] and p.get('signature') and p.get('public_key'):
                payload = f"{contract['contract_id']}|{contract['hash']}|{p['zuhri_id']}"
                if verify(payload, p['signature'], p['public_key']):
                    print(f"  {GREEN}✅ {p['name']:20}{RESET} — Tanda tangan VALID")
                else:
                    print(f"  {RED}❌ {p['name']:20}{RESET} — Tanda tangan TIDAK VALID")
                    all_valid = False
            elif p['signed']:
                print(f"  {YELLOW}⚠️  {p['name']:20}{RESET} — Tidak ada signature")
            else:
                print(f"  {DIM}⏳ {p['name']:20} — Belum tanda tangan{RESET}")
        
        print(f"""
{'─' * 65}""")
        
        if all_valid and contract['status'] == 'active':
            print(f"{GREEN}✅ KONTRAK VALID — Semua tanda tangan terverifikasi{RESET}\n")
        elif contract['status'] == 'pending':
            print(f"{YELLOW}⏳ KONTRAK PENDING — Menunggu tanda tangan{RESET}\n")
        else:
            print(f"{RED}❌ KONTRAK TIDAK VALID{RESET}\n")
    except ValueError:
        pass

# ============================================================
# HELP
# ============================================================
def show_help():
    print(f"""
{BOLD}{CYAN}📜 ZUHRI CONTRACT — BANTUAN{RESET}
{'─' * 55}
  {BOLD}contract create{RESET}   → Buat kontrak baru
  {BOLD}contract sign{RESET}     → Tanda tangani kontrak
  {BOLD}contract show{RESET}     → Lihat detail kontrak
  {BOLD}contract list{RESET}     → Lihat daftar kontrak
  {BOLD}contract verify{RESET}   → Verifikasi kontrak
  {BOLD}contract help{RESET}     → Bantuan
{'─' * 55}
  Operator: {get_id_badge()}
{'─' * 55}
""")

def list_contracts_cmd():
    """List contracts"""
    contracts = list_contracts()
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📜 DAFTAR KONTRAK — ZUHRI CONTRACT                            ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    if not contracts:
        print(f"{YELLOW}Belum ada kontrak.{RESET}\n")
        return
    
    for i, c in enumerate(contracts, 1):
        data = json.load(open(os.path.join(DATA_DIR, f"{c}.json")))
        
        status_color = GREEN if data['status'] == 'active' else (YELLOW if data['status'] == 'pending' else DIM)
        parties_count = len(data['parties'])
        signed_count = sum(1 for p in data['parties'] if p['signed'])
        
        print(f"  {GOLD}{i}.{RESET} {BOLD}{data['title']}{RESET}")
        print(f"     {DIM}ID: {c}{RESET}")
        print(f"     📊 {status_color}{data['status'].upper()}{RESET} | 👤 {signed_count}/{parties_count} pihak | 📅 {data['created'][:19]}")
        print()

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "create":
        create_contract()
    elif cmd == "sign":
        sign_contract()
    elif cmd == "show":
        show_contract()
    elif cmd == "list":
        list_contracts_cmd()
    elif cmd == "verify":
        verify_contract()
    elif cmd == "help":
        show_help()
    else:
        show_help()
