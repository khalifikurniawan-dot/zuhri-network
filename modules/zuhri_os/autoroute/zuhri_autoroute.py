#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI AUTO-ROUTING — SMART ROUTER
Arahkan kata kunci ke ekosistem Zuhri
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, subprocess
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
AR_DIR = os.path.join(HOME, "zuhri_os", "autoroute")
LOG_DIR = os.path.join(AR_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# ROUTING TABLE
# ============================================================
ROUTES = {
    # ID & Identitas
    "id": "python ~/zuhri_os/id/zuhri_id.py show",
    "zuhri id": "python ~/zuhri_os/id/zuhri_id.py show",
    "identitas": "python ~/zuhri_os/id/zuhri_id.py show",
    "did": "python ~/zuhri_os/did/zuhri_did.py",
    "passport": "python ~/zuhri_os/passport/zuhri_passport.py",
    
    # Keamanan
    "crypto": "python ~/zuhri_os/crypto/zuhri_crypto.py",
    "kripto": "python ~/zuhri_os/crypto/zuhri_crypto.py",
    "enkripsi": "python ~/zuhri_os/enkripsi/zuhri_enkripsi.py",
    "encrypt": "python ~/zuhri_os/enkripsi/zuhri_enkripsi.py",
    "security": "python ~/zuhri_os/security/security_shield.py",
    "shield": "python ~/zuhri_os/security/security_shield.py",
    "botnet": "python ~/zuhri_os/botnet/zuhri_botnet.py",
    "hunter": "python ~/zuhri_os/botnet/zuhri_botnet.py",
    
    # Network
    "mesh": "python ~/kosmik/p2p/mesh_node.py",
    "p2p": "python ~/kosmik/p2p/mesh_node.py",
    "scan": "python ~/kosmik/p2p/mesh_discovery.py",
    "sos": "python ~/kosmik/sos_beacon.py beacon",
    
    # AI
    "ai": "ai",
    "vision": "python ~/kosmik/vision/edge_vision.py",
    "translate": "python ~/zuhri_os/translator/translator.py",
    "terjemah": "python ~/zuhri_os/translator/translator.py",
    
    # Dark Web
    "dark": "dark-web",
    "darkweb": "dark-web",
    "onion": "dark-web",
    
    # Demokrasi
    "vote": "python ~/zuhri_os/vote/zuhri_vote.py",
    "voting": "python ~/zuhri_os/vote/zuhri_vote.py",
    "contract": "python ~/zuhri_os/contract/zuhri_contract.py",
    "kontrak": "python ~/zuhri_os/contract/zuhri_contract.py",
    
    # Finansial
    "finance": "python ~/zuhri_os/finance/zuhri_finance.py",
    "finansial": "python ~/zuhri_os/finance/zuhri_finance.py",
    "keuangan": "python ~/zuhri_os/finance/zuhri_finance.py",
    "wallet": "python ~/zuhri_os/wallet/wallet.py",
    "dompet": "python ~/zuhri_os/wallet/wallet.py",
    
    # Edu & Library
    "edu": "python ~/zuhri_os/edu/zuhri_edu.py",
    "belajar": "python ~/zuhri_os/edu/zuhri_edu.py",
    "library": "python ~/zuhri_os/library/zuhri_library.py",
    "lib": "python ~/zuhri_os/library/zuhri_library.py",
    "buku": "python ~/zuhri_os/library/zuhri_library.py",
    "kurikulum": "python ~/zuhri_os/kurikulum/zuhri_kurikulum.py",
    "k8": "python ~/zuhri_os/kurikulum/zuhri_kurikulum.py",
    
    # Sistem
    "os": "python ~/zuhri_os/zuhri_os.py",
    "health": "python ~/health.py",
    "backup": "python ~/zuhri_os/backup/backup_manager.py backup",
    "restore": "python ~/zuhri_os/backup/backup_manager.py restore",
    "list-backup": "python ~/zuhri_os/backup/backup_manager.py list",
    "menu": "python ~/zuhri_os/menu.py",
    "ekosistem": "python ~/zuhri_os/menu.py",
    "panduan": "python ~/zuhri_os/onboarding/welcome.py",
    
    # Ekosistem Khusus
    "peringatan": "python ~/zuhri_os/peringatan/zuhri_peringatan.py",
    "spiritual": "python ~/zuhri_os/spiritual/zuhri_spiritual.py",
    "fatwa": "python ~/zuhri_os/spiritual/zuhri_spiritual.py",
    "frekuensi": "python ~/zuhri_os/frekuensi/zuhri_frekuensi.py",
    "predictive": "python ~/zuhri_os/predictive/zuhri_predictive.py",
    "energi": "python ~/zuhri_os/energi/zuhri_energi.py",
    "chain": "python ~/zuhri_os/chain/zuhri_chain.py",
}

# ============================================================
# FUZZY MATCH
# ============================================================
def find_route(query):
    """Cari route berdasarkan kata kunci"""
    query = query.lower().strip()
    
    # Exact match
    if query in ROUTES:
        return query, ROUTES[query]
    
    # Partial match
    matches = []
    for key in ROUTES:
        if query in key or key in query:
            matches.append(key)
    
    if len(matches) == 1:
        return matches[0], ROUTES[matches[0]]
    elif len(matches) > 1:
        return matches, None
    
    return None, None

# ============================================================
# ROUTE
# ============================================================
def route(query):
    """Arahkan query ke ekosistem yang tepat"""
    os.system('clear')
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🚦 ZUHRI AUTO-ROUTING                                          ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Query: {query}{RESET}
""")
    
    result = find_route(query)
    
    if isinstance(result[0], list):
        # Multiple matches
        matches = result[0]
        print(f"{YELLOW}⚠️  Multiple matches, pilih satu:{RESET}\n")
        for i, m in enumerate(matches, 1):
            print(f"  {GOLD}{i}.{RESET} {m}")
        
        try:
            c = int(input(f"\n{CYAN}Pilih: {RESET}")) - 1
            if 0 <= c < len(matches):
                key = matches[c]
                cmd = ROUTES[key]
                print(f"\n{GREEN}🚀 Menjalankan: {key}{RESET}\n")
                os.system(cmd)
                
                if ZUHRI_ID_OK:
                    log_verified(f"AUTOROUTE: {key}")
        except: pass
    
    elif result[1]:
        # Single match
        key, cmd = result
        print(f"{GREEN}✅ Route: {GOLD}{key}{RESET}")
        print(f"{DIM}Command: {cmd}{RESET}\n")
        print(f"{CYAN}🚀 Menjalankan...{RESET}\n")
        
        if ZUHRI_ID_OK:
            log_verified(f"AUTOROUTE: {key}")
        
        os.system(cmd)
    
    else:
        # No match
        print(f"{RED}❌ Tidak ada route untuk: '{query}'{RESET}\n")
        print(f"{BOLD}Contoh query:{RESET}")
        examples = ["id", "crypto", "mesh", "sos", "vote", "finance", "edu", "chain", "enkripsi"]
        for e in examples:
            print(f"  {GOLD}z{e}{RESET} → {ROUTES[e]}")
        print()

# ============================================================
# LIST ROUTES
# ============================================================
def list_routes():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🚦 ZUHRI AUTO-ROUTING — DAFTAR ROUTES                         ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 {len(ROUTES)} Routes Tersedia:{RESET}
""")
    
    for key in sorted(ROUTES.keys()):
        print(f"  {GOLD}z{key:20}{RESET} → {DIM}{ROUTES[key]}{RESET}")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🚦 ZUHRI AUTO-ROUTING                                          ║
║  ──────────────────────────────────────────────────────────────  ║
║  Ketik kata kunci → otomatis diarahkan ke ekosistem            ║
║  Total Routes: {GOLD}{len(ROUTES)}{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 CARA PAKAI:{RESET}
  Ketik: {CYAN}z <kata-kunci>{RESET}
  
  Contoh:
    {GOLD}z id{RESET}         → Zuhri ID
    {GOLD}z crypto{RESET}     → Zuhri Crypto
    {GOLD}z mesh{RESET}       → P2P-Mesh
    {GOLD}z sos{RESET}        → SOS-Beacon
    {GOLD}z vote{RESET}       → Zuhri Vote
    {GOLD}z edu{RESET}        → Zuhri Edu
    {GOLD}z chain{RESET}      → Zuhri Chain
    {GOLD}z enkripsi{RESET}   → Zuhri Enkripsi

  Atau langsung:
    {GOLD}z list{RESET}       → Lihat semua routes
    {GOLD}z menu{RESET}       → Menu ekosistem
""")
        
        try:
            query = input(f"{GOLD}🚦 z > {RESET}").strip()
            
            if not query:
                continue
            
            if query.lower() in ["exit", "quit", "keluar"]:
                break
            elif query.lower() == "list":
                list_routes()
            else:
                route(query)
                input(f"\n{DIM}Enter...{RESET}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        if query.lower() == "list":
            for k in sorted(ROUTES.keys()):
                print(f"z{k:20} → {ROUTES[k]}")
        else:
            route(query)
    else:
        menu()
