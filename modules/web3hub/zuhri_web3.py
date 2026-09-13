#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI WEB3 HUB — PUSAT SITUS WEB3
Berita, Media Sosial, Tools, Belajar
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, subprocess, time
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
WEB3_DIR = os.path.join(HOME, "zuhri_os", "web3hub")
DATA_DIR = os.path.join(WEB3_DIR, "data")
LOG_DIR = os.path.join(WEB3_DIR, "logs")
for d in [DATA_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# DATABASE WEB3 SITES
# ============================================================
WEB3_SITES = {
    "berita": {
        "nama": "📰 BERITA WEB3",
        "sites": [
            {"nama":"CoinDesk","url":"https://www.coindesk.com","trust":10},
            {"nama":"Cointelegraph","url":"https://cointelegraph.com","trust":9},
            {"nama":"The Block","url":"https://www.theblock.co","trust":9},
            {"nama":"Blockworks","url":"https://blockworks.co","trust":9},
            {"nama":"Bankless","url":"https://www.bankless.com","trust":8},
            {"nama":"RSS3","url":"https://rss3.io","trust":9,"desc":"Protokol berita terdesentralisasi"},
            {"nama":"Leviathan News","url":"https://leviathannews.xyz","trust":8,"desc":"Crowdsourced news"},
            {"nama":"Olas Protocol","url":"https://olas.network","trust":8,"desc":"Trustworthy information protocol"},
        ]
    },
    "sosial": {
        "nama": "👥 MEDIA SOSIAL WEB3",
        "sites": [
            {"nama":"Farcaster","url":"https://farcaster.xyz","trust":9,"desc":"Social protocol terdesentralisasi"},
            {"nama":"Lens Protocol","url":"https://lens.xyz","trust":9,"desc":"Social graph Web3"},
            {"nama":"Mirror","url":"https://mirror.xyz","trust":9,"desc":"Platform publishing Web3"},
            {"nama":"GM Farcaster","url":"https://gm.xyz","trust":8,"desc":"News show Farcaster"},
        ]
    },
    "tools": {
        "nama": "🛠️ TOOLS WEB3",
        "sites": [
            {"nama":"IPFS Gateway","url":"https://ipfs.io","trust":10,"desc":"Akses konten IPFS"},
            {"nama":"Orbitor Gateway","url":"https://ipfs.orbitor.dev","trust":9,"desc":"IPFS gateway regional"},
            {"nama":"OpenSea","url":"https://opensea.io","trust":9,"desc":"NFT marketplace"},
            {"nama":"Rarible","url":"https://rarible.com","trust":9,"desc":"NFT marketplace"},
            {"nama":"Decentraland","url":"https://decentraland.org","trust":8,"desc":"Virtual world Web3"},
            {"nama":"Aave","url":"https://aave.com","trust":9,"desc":"DeFi lending"},
        ]
    },
    "belajar": {
        "nama": "📚 BELAJAR WEB3 (GRATIS)",
        "sites": [
            {"nama":"LearnWeb3","url":"https://learnweb3.io","trust":10,"desc":"Structured Web3 learning"},
            {"nama":"Alchemy University","url":"https://university.alchemy.com","trust":10,"desc":"Free blockchain courses"},
            {"nama":"Binance Academy","url":"https://academy.binance.com","trust":9,"desc":"Crypto & Web3 education"},
            {"nama":"Coinbase Learn","url":"https://www.coinbase.com/learn","trust":9,"desc":"Crypto basics"},
            {"nama":"CryptoZombies","url":"https://cryptozombies.io","trust":9,"desc":"Interactive Solidity learning"},
            {"nama":"freeCodeCamp","url":"https://www.freecodecamp.org","trust":10,"desc":"Free coding tutorials"},
        ]
    },
    "infrastruktur": {
        "nama": "🌐 INFRASTRUKTUR WEB3",
        "sites": [
            {"nama":"Termux + Tor (Stackedge)","url":"https://github.com/Frost-bit-star/stackedge","trust":9,"desc":"Hosting app di Termux + Tor"},
            {"nama":"Termux + IPFS","url":"https://github.com/ipfs/kubo","trust":9,"desc":"Full node IPFS di Termux"},
            {"nama":"Aryan Proxy","url":"https://github.com/Aryandmpa/aryan_proxy","trust":8,"desc":"Proxy management Termux"},
        ]
    }
}

def clear(): os.system('clear')

# ============================================================
# BUKA URL
# ============================================================
def open_url(url, nama):
    """Buka URL di browser"""
    print(f"\n{CYAN}🌐 Membuka {nama}...{RESET}")
    print(f"{DIM}{url}{RESET}\n")
    
    try:
        subprocess.run(["termux-open-url", url], timeout=5)
        print(f"{GREEN}✅ Dibuka di browser{RESET}\n")
    except:
        print(f"{YELLOW}⚠️  Buka manual: {url}{RESET}\n")
    
    if ZUHRI_ID_OK:
        log_verified(f"WEB3_OPEN: {nama}")

# ============================================================
# MENU KATEGORI
# ============================================================
def menu_kategori(key):
    """Menu per kategori"""
    kategori = WEB3_SITES[key]
    
    while True:
        clear()
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  {kategori['nama']}
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")
        
        for i, site in enumerate(kategori['sites'], 1):
            trust = "★" * site.get('trust', 5) + "☆" * (10 - site.get('trust', 5))
            desc = site.get('desc', '')
            print(f"  {GOLD}{i:2}.{RESET} {site['nama']:25} {CYAN}{trust}{RESET}")
            if desc:
                print(f"      {DIM}{desc}{RESET}")
        
        print(f"""
{BOLD}  {GOLD}0.{RESET}  Kembali
""")
        
        try:
            c = input(f"{GOLD}Pilih: {RESET}").strip()
            if c == "0":
                break
            
            idx = int(c) - 1
            if 0 <= idx < len(kategori['sites']):
                site = kategori['sites'][idx]
                open_url(site['url'], site['nama'])
                input(f"{DIM}Enter...{RESET}")
        except ValueError:
            pass
        except KeyboardInterrupt:
            break

# ============================================================
# CEK KONTEN IPFS
# ============================================================
def check_ipfs():
    """Cek konten IPFS via gateway"""
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🌐 CEK KONTEN IPFS                                                 ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Masukkan CID (Content Identifier) untuk akses konten IPFS.${RESET}
{DIM}Contoh: Qm... atau bafy...${RESET}
""")
    
    cid = input("🔍 CID: ").strip()
    if not cid:
        return
    
    gateways = [
        f"https://ipfs.io/ipfs/{cid}",
        f"https://ipfs.orbitor.dev/ipfs/{cid}",
        f"https://cloudflare-ipfs.com/ipfs/{cid}",
    ]
    
    print(f"\n{CYAN}🌐 Gateway tersedia:{RESET}\n")
    for i, gw in enumerate(gateways, 1):
        print(f"  {GOLD}{i}.{RESET} {gw}")
    
    try:
        c = int(input(f"\n{CYAN}Pilih gateway (1-3): {RESET}")) - 1
        if 0 <= c < len(gateways):
            open_url(gateways[c], f"IPFS: {cid[:20]}...")
    except ValueError:
        pass
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# INFO WEB3
# ============================================================
def info():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  📚 INFO ZUHRI WEB3 HUB                                             ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}🎯 FITUR:{RESET}
  {GOLD}•{RESET} Berita Web3 (8 sumber terpercaya)
  {GOLD}•{RESET} Media Sosial Web3 (Farcaster, Lens, Mirror)
  {GOLD}•{RESET} Tools Web3 (IPFS, NFT, DeFi)
  {GOLD}•{RESET} Belajar Web3 (6 platform gratis)
  {GOLD}•{RESET} Infrastruktur (Termux + Tor, Termux + IPFS)

{BOLD}🌐 WEB3 vs WEB2:{RESET}

  {RED}Web2 (Sekarang):{RESET}
    • Data di server pusat
    • Korporasi kontrol
    • Sensor mungkin
    • Iklan & tracking

  {GREEN}Web3 (Masa Depan):{RESET}
    • Data di blockchain
    • User kontrol
    • Sensor-resistant
    • Privasi terjaga

{BOLD}🔗 KONSEP WEB3:{RESET}
  {GOLD}•{RESET} IPFS: File system terdesentralisasi
  {GOLD}•{RESET} Blockchain: Database terdistribusi
  {GOLD}•{RESET} Smart Contract: Kontrak otomatis
  {GOLD}•{RESET} DAO: Organisasi terdesentralisasi
  {GOLD}•{RESET} DeFi: Keuangan terdesentralisasi

{BOLD}📰 RSS3 — BERITA TERDESENTRALISASI:{RESET}
  {DIM}RSS3 adalah protokol yang membuat konten${RESET}
  {DIM}tersedia di semua platform tanpa sensor.${RESET}
  {DIM}Jurnalis publish, RSS3 index, pembaca akses.${RESET}

{BOLD}👥 OLAS PROTOCOL — INFO TERPERCAYA:{RESET}
  {DIM}Protokol untuk informasi terpercaya.${RESET}
  {DIM}Ad-free, decentralised, micropayment.${RESET}

{BOLD}⚠️  CATATAN:{RESET}
  {DIM}• Beberapa situs butuh wallet (MetaMask)${RESET}
  {DIM}• Selalu verifikasi dari 3+ sumber${RESET}
  {DIM}• Jangan share private key${RESET}
  {DIM}• Web3 masih berkembang${RESET}
""")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU UTAMA
# ============================================================
def menu():
    while True:
        clear()
        
        identity = load_identity() if ZUHRI_ID_OK else None
        name = identity['name'] if identity else "Anonymous"
        
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🌐 ZUHRI WEB3 HUB — PUSAT SITUS WEB3                               ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Operator: {GREEN}{name}{RESET}
║  Protokol: K-8.0                                                    ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 KATEGORI:{RESET}
  {GOLD}1.{RESET}  📰 Berita Web3 (CoinDesk, RSS3, dll)
  {GOLD}2.{RESET}  👥 Media Sosial Web3 (Farcaster, Lens)
  {GOLD}3.{RESET}  🛠️  Tools Web3 (IPFS, NFT, DeFi)
  {GOLD}4.{RESET}  📚 Belajar Web3 (Gratis)
  {GOLD}5.{RESET}  🌐 Infrastruktur (Termux + Tor/IPFS)
  {GOLD}6.{RESET}  🔍 Cek Konten IPFS
  {GOLD}7.{RESET}  ℹ️  Info Web3
  {GOLD}0.{RESET}  Keluar
""")
        
        try:
            c = input(f"{GOLD}Pilih (0-7): {RESET}").strip()
            if c == "0": break
            elif c == "1": menu_kategori("berita")
            elif c == "2": menu_kategori("sosial")
            elif c == "3": menu_kategori("tools")
            elif c == "4": menu_kategori("belajar")
            elif c == "5": menu_kategori("infrastruktur")
            elif c == "6": check_ipfs()
            elif c == "7": info()
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "info": info()
        elif cmd == "berita": menu_kategori("berita")
        elif cmd == "sosial": menu_kategori("sosial")
        elif cmd == "tools": menu_kategori("tools")
        elif cmd == "belajar": menu_kategori("belajar")
        else: menu()
    else: menu()
