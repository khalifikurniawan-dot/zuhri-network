#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI KRIPTO — KELOMPOK KRIPTO
Quad-Core Bot + Exchange + Tools + News
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, subprocess

HOME = os.path.expanduser("~")

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

def clear(): os.system('clear')
def run(c): os.system(c)
def open_url(url): subprocess.run(["termux-open-url", url], timeout=5)

# ============================================================
# DATABASE EXCHANGE
# ============================================================
EXCHANGES = {
    "tier1": {
        "nama": "🏆 TIER 1 — Exchange Global (AA Rated)",
        "list": [
            {"nama":"Binance","url":"https://www.binance.com","desc":"Likuiditas terbesar, 500+ coin"},
            {"nama":"Coinbase","url":"https://www.coinbase.com","desc":"Regulasi US, ramah pemula"},
            {"nama":"Kraken","url":"https://www.kraken.com","desc":"Keamanan terbaik, PoR"},
            {"nama":"OKX","url":"https://www.okx.com","desc":"Derivatif dalam, DeFi"},
            {"nama":"Crypto.com","url":"https://crypto.com","desc":"Fiat on-ramp luas"},
        ]
    },
    "indonesia": {
        "nama": "🇮🇩 EXCHANGE INDONESIA (OJK)",
        "list": [
            {"nama":"Indodax","url":"https://indodax.com","desc":"IDR rails, retail access"},
            {"nama":"Tokocrypto","url":"https://tokocrypto.com","desc":"Binance-linked, trading tools"},
            {"nama":"Reku","url":"https://reku.com","desc":"Ramah pemula, IDR conversion"},
            {"nama":"Pintu","url":"https://pintu.co.id","desc":"Beginner-friendly"},
        ]
    },
    "tools": {
        "nama": "🛠️ TOOLS TRADING & DATA",
        "list": [
            {"nama":"CoinGecko","url":"https://www.coingecko.com","desc":"Harga, market cap, volume"},
            {"nama":"CoinMarketCap","url":"https://coinmarketcap.com","desc":"Ranking, exchange data"},
            {"nama":"TradingView","url":"https://www.tradingview.com","desc":"Chart, indikator, analisis"},
            {"nama":"DefiLlama","url":"https://defillama.com","desc":"TVL, yields, protocol stats"},
            {"nama":"CryptoQuant","url":"https://cryptoquant.com","desc":"Whale moves, exchange flows"},
            {"nama":"Dune Analytics","url":"https://dune.com","desc":"On-chain data dashboards"},
        ]
    },
    "news": {
        "nama": "📰 BERITA KRIPTO TERPERCAYA",
        "list": [
            {"nama":"CoinDesk","url":"https://www.coindesk.com","desc":"Tier 1 — Berita utama, regulasi"},
            {"nama":"The Block","url":"https://www.theblock.co","desc":"Tier 1 — Riset institusional"},
            {"nama":"CoinTelegraph","url":"https://cointelegraph.com","desc":"Tier 2 — Berita cepat"},
            {"nama":"Blockworks","url":"https://blockworks.co","desc":"Tier 2 — Institutional crypto"},
            {"nama":"Decrypt","url":"https://decrypt.co","desc":"Tier 2 — Ramah pemula"},
            {"nama":"Bankless","url":"https://www.bankless.com","desc":"Tier 2 — Ethereum/DeFi"},
        ]
    }
}

# ============================================================
# MENU EXCHANGE
# ============================================================
def menu_kategori(key):
    kategori = EXCHANGES[key]
    
    while True:
        clear()
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  {kategori['nama']}
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")
        
        for i, item in enumerate(kategori['list'], 1):
            print(f"  {GOLD}{i:2}.{RESET} {item['nama']:20} {DIM}{item['desc']}{RESET}")
        
        print(f"""
{BOLD}  {GOLD}0.{RESET}  Kembali
""")
        
        try:
            c = input(f"{GOLD}Pilih: {RESET}").strip()
            if c == "0": break
            
            idx = int(c) - 1
            if 0 <= idx < len(kategori['list']):
                item = kategori['list'][idx]
                print(f"\n{CYAN}🌐 Membuka {item['nama']}...{RESET}")
                open_url(item['url'])
                input(f"{DIM}Enter...{RESET}")
        except ValueError:
            pass
        except KeyboardInterrupt:
            break

# ============================================================
# MENU UTAMA
# ============================================================
def menu():
    while True:
        clear()
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  💰 ZUHRI KRIPTO — KELOMPOK KRIPTO                                 ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                            ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🤖 Quad-Core Bot (Loop)
  {GOLD}2.{RESET}  🔍 Quad-Core Bot (Sekali)
  {GOLD}3.{RESET}  📊 Quad-Core Status
  {GOLD}4.{RESET}  🏆 Exchange Global (Tier 1)
  {GOLD}5.{RESET}  🇮🇩 Exchange Indonesia
  {GOLD}6.{RESET}  🛠️  Tools Trading & Data
  {GOLD}7.{RESET}  📰 Berita Kripto Terpercaya
  {GOLD}8.{RESET}  🪙 Crypto Wallet (Harga)
  {GOLD}9.{RESET}  🔐 Zuhri Crypto (Enkripsi)
  {GOLD}0.{RESET}  Kembali
""")
        try:
            c = input(f"{GOLD}Pilih (0-9): {RESET}").strip()
            if c == "0": break
            elif c == "1": run("python ~/zuhri_os/kripto/quadcore/bot_loop.py run 60")
            elif c == "2": run("python ~/zuhri_os/kripto/quadcore/bot_loop.py once")
            elif c == "3": run("python ~/zuhri_os/kripto/quadcore/bot_loop.py status")
            elif c == "4": menu_kategori("tier1")
            elif c == "5": menu_kategori("indonesia")
            elif c == "6": menu_kategori("tools")
            elif c == "7": menu_kategori("news")
            elif c == "8": run("python ~/zuhri_os/wallet/wallet.py")
            elif c == "9": run("python ~/zuhri_os/crypto/zuhri_crypto.py")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    menu()
