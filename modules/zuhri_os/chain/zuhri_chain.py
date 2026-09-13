#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI CHAIN — DATABASE TERDESENTRALISASI
Hash Chain + Zuhri ID + P2P Ready
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, hashlib, secrets
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
CHAIN_DIR = os.path.join(HOME, "zuhri_os", "chain")
DATA_DIR = os.path.join(CHAIN_DIR, "data")
LOG_DIR = os.path.join(CHAIN_DIR, "logs")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# CHAIN FILE
# ============================================================
def chain_file():
    if not ZUHRI_ID_OK: return None
    i = load_identity()
    if not i: return None
    return os.path.join(DATA_DIR, f"chain_{i['zuhri_id']}.json")

def load_chain():
    f = chain_file()
    if f and os.path.exists(f):
        return json.load(open(f))
    return {"blocks": [], "created": datetime.now().isoformat()}

def save_chain(chain):
    f = chain_file()
    if f: json.dump(chain, open(f, "w"), indent=2)

# ============================================================
# HASH UTIL
# ============================================================
def compute_hash(block):
    """Hitung hash block (tanpa field hash & signature)"""
    data = {k: v for k, v in block.items() if k not in ["hash", "signature", "public_key"]}
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def get_last_hash(chain):
    if not chain["blocks"]:
        return "0" * 64  # Genesis hash
    return chain["blocks"][-1]["hash"]

# ============================================================
# TAMBAH BLOCK
# ============================================================
def add_block():
    if not ZUHRI_ID_OK:
        print(f"{RED}❌ Butuh Zuhri ID{RESET}")
        input(f"{DIM}Enter...{RESET}"); return
    
    identity = load_identity()
    chain = load_chain()
    
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  ⛓️  ZUHRI CHAIN — TAMBAH BLOCK                                 ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Data Anda akan disimpan permanen di blockchain.{RESET}
{DIM}Tidak bisa diubah setelah ditambahkan.{RESET}
""")
    
    # Tipe data
    print(f"{BOLD}📋 Tipe Data:{RESET}")
    print(f"  {GOLD}1.{RESET} Catatan")
    print(f"  {GOLD}2.{RESET} Transaksi")
    print(f"  {GOLD}3.{RESET} Kontrak")
    print(f"  {GOLD}4.{RESET} Vote")
    print(f"  {GOLD}5.{RESET} Identitas")
    print(f"  {GOLD}6.{RESET} Custom")
    
    tipe = input(f"\n{CYAN}Pilih (1-6): {RESET}").strip()
    tipe_map = {"1":"catatan","2":"transaksi","3":"kontrak","4":"vote","5":"identitas","6":"custom"}
    tipe_str = tipe_map.get(tipe, "catatan")
    
    data = input(f"\n📝 Data: ").strip()
    if not data: return
    
    # Buat block
    block = {
        "index": len(chain["blocks"]),
        "timestamp": datetime.now().isoformat(),
        "type": tipe_str,
        "data": data,
        "author": {
            "zuhri_id": identity['zuhri_id'],
            "name": identity['name']
        },
        "prev_hash": get_last_hash(chain),
        "nonce": secrets.token_hex(8)
    }
    
    # Hitung hash
    block["hash"] = compute_hash(block)
    
    # Tanda tangan
    block["signature"] = sign(block["hash"])
    block["public_key"] = identity['public_key']
    
    # Tambah ke chain
    chain["blocks"].append(block)
    save_chain(chain)
    
    if ZUHRI_ID_OK:
        log_verified(f"CHAIN_ADD: Block #{block['index']} ({tipe_str})")
    
    print(f"""
{BOLD}{GREEN}╔══════════════════════════════════════════════════════════════════╗
║  ✅ BLOCK DITAMBAHKAN!                                         ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}Block #{RESET}     {block['index']}
  {GOLD}Tipe{RESET}        {tipe_str}
  {GOLD}Hash{RESET}        {block['hash'][:32]}...
  {GOLD}Prev Hash{RESET}   {block['prev_hash'][:32]}...
  {GOLD}Signature{RESET}   {'✅' if block['signature'] else '❌'}
  {GOLD}Total Block{RESET} {len(chain['blocks'])}
""")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# LIHAT CHAIN
# ============================================================
def show_chain():
    chain = load_chain()
    
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  ⛓️  ZUHRI CHAIN — LIHAT BLOCKCHAIN                             ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}Total Block:{RESET} {len(chain['blocks'])}
  {GOLD}Dibuat:{RESET}      {chain.get('created','N/A')[:19]}
""")
    
    if not chain['blocks']:
        print(f"\n{YELLOW}Belum ada block. Tambah dengan menu 1.{RESET}\n")
        input(f"{DIM}Enter...{RESET}"); return
    
    # Tampilkan 5 block terakhir
    blocks = chain['blocks'][-5:]
    
    for b in blocks:
        verified = "?"
        try:
            data = {k:v for k,v in b.items() if k not in ["hash","signature","public_key"]}
            h = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
            hash_ok = h == b['hash']
            sig_ok = verify(b['hash'], b.get('signature',''), b.get('public_key',''))
            verified = "✅ VALID" if (hash_ok and sig_ok) else "❌ INVALID"
        except: verified = "❌ ERROR"
        
        print(f"""
{BOLD}{CYAN}┌─────────────────────────────────────────────────────────────┐
│  Block #{b['index']}{RESET}
{CYAN}├─────────────────────────────────────────────────────────────┤{RESET}
│  {GOLD}Tipe{RESET}     : {b['type']}
│  {GOLD}Waktu{RESET}    : {b['timestamp'][:19]}
│  {GOLD}Author{RESET}   : {b['author']['name']}
│  {GOLD}Data{RESET}     : {b['data'][:50]}
│  {GOLD}Hash{RESET}     : {b['hash'][:32]}...
│  {GOLD}Prev{RESET}     : {b['prev_hash'][:32]}...
│  {GOLD}Verified{RESET} : {verified}
{CYAN}└─────────────────────────────────────────────────────────────┘{RESET}""")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# VERIFIKASI CHAIN
# ============================================================
def verify_chain():
    chain = load_chain()
    
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🔍 VERIFIKASI CHAIN — CEK INTEGRITAS                           ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    if not chain['blocks']:
        print(f"{YELLOW}Chain kosong.{RESET}\n")
        input(f"{DIM}Enter...{RESET}"); return
    
    valid = 0
    invalid = 0
    
    for i, b in enumerate(chain['blocks']):
        # 1. Cek hash
        data = {k:v for k,v in b.items() if k not in ["hash","signature","public_key"]}
        h = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        hash_ok = h == b['hash']
        
        # 2. Cek signature
        sig_ok = verify(b['hash'], b.get('signature',''), b.get('public_key',''))
        
        # 3. Cek prev_hash match
        if i == 0:
            prev_ok = b['prev_hash'] == "0" * 64
        else:
            prev_ok = b['prev_hash'] == chain['blocks'][i-1]['hash']
        
        status = "✅" if (hash_ok and sig_ok and prev_ok) else "❌"
        
        if status == "✅": valid += 1
        else: invalid += 1
        
        print(f"  {status} Block #{b['index']}  hash:{'✅' if hash_ok else '❌'}  sig:{'✅' if sig_ok else '❌'}  prev:{'✅' if prev_ok else '❌'}")
    
    print(f"""
{DIM}{'─'*60}{RESET}
{GOLD}Total{RESET}    : {len(chain['blocks'])}
{GREEN}Valid{RESET}    : {valid}
{RED}Invalid{RESET}  : {invalid}
{DIM}{'─'*60}{RESET}
""")
    
    if invalid == 0:
        print(f"{GREEN}✅ CHAIN VALID — Tidak ada tampering!{RESET}")
    else:
        print(f"{RED}⚠️  CHAIN TIDAK VALID — Ada block yang diubah!{RESET}")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# EXPORT CHAIN
# ============================================================
def export_chain():
    chain = load_chain()
    if not chain['blocks']:
        print(f"{YELLOW}Chain kosong.{RESET}")
        input(f"{DIM}Enter...{RESET}"); return
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_file = os.path.join(DATA_DIR, f"export_chain_{ts}.json")
    json.dump(chain, open(export_file, "w"), indent=2)
    
    # Copy ke sdcard
    try:
        sdcard = "/sdcard/Download"
        if os.path.exists(sdcard):
            import shutil
            shutil.copy2(export_file, sdcard)
            print(f"{GREEN}✅ Export: {sdcard}/{os.path.basename(export_file)}{RESET}")
    except: pass
    
    print(f"\n{GREEN}✅ Chain diexport: {export_file}{RESET}\n")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# STATISTIK
# ============================================================
def stats():
    chain = load_chain()
    
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  📊 STATISTIK ZUHRI CHAIN                                       ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}Total Block{RESET}  : {len(chain['blocks'])}
  {GOLD}Genesis{RESET}      : {chain.get('created','N/A')[:19]}
""")
    
    if chain['blocks']:
        # Per tipe
        types = {}
        for b in chain['blocks']:
            types[b['type']] = types.get(b['type'], 0) + 1
        
        print(f"\n{BOLD}📊 Per Tipe:{RESET}")
        for t, c in sorted(types.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * c + "░" * (10 - min(c, 10))
            print(f"  {t:12} {c:3}  {CYAN}{bar}{RESET}")
        
        print(f"\n{BOLD}📅 Block Terakhir:{RESET}")
        last = chain['blocks'][-1]
        print(f"  #{last['index']} — {last['type']} — {last['timestamp'][:19]}")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        chain = load_chain()
        total = len(chain['blocks'])
        
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  ⛓️  ZUHRI CHAIN — DECENTRALIZED DB                            ║
║  ──────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                       ║
║  Total Block: {GOLD}{total}{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  ➕ Tambah Block (Simpan Data)
  {GOLD}2.{RESET}  ⛓️  Lihat Blockchain
  {GOLD}3.{RESET}  🔍 Verifikasi Chain
  {GOLD}4.{RESET}  📊 Statistik
  {GOLD}5.{RESET}  📤 Export Chain
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-5): {RESET}").strip()
            if c == "0": break
            elif c == "1": add_block()
            elif c == "2": show_chain()
            elif c == "3": verify_chain()
            elif c == "4": stats()
            elif c == "5": export_chain()
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "verify": verify_chain()
        elif cmd == "show": show_chain()
        elif cmd == "stats": stats()
        else: menu()
    else: menu()
