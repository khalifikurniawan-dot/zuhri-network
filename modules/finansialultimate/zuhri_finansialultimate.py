#!/usr/bin/env python3
"""
ZUHRI FINANSIAL ULTIMATE — BOT KRIPTO + FINANSIAL PRO
Gabungan ekosistem keuangan lengkap
"""

import os, sys, json, hashlib, secrets, subprocess, time, random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False
    def log_verified(msg): pass

HOME = os.path.expanduser("~")
ULT_DIR = os.path.join(HOME, "zuhri_os", "finansialultimate")
DATA_DIR = os.path.join(ULT_DIR, "data")
LOG_DIR = os.path.join(ULT_DIR, "logs")
PRED_DIR = os.path.join(ULT_DIR, "predictions")
WATCH_DIR = os.path.join(ULT_DIR, "watchlist")
for d in [DATA_DIR, LOG_DIR, PRED_DIR, WATCH_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

def clear(): os.system('clear')
def pause():
    input(f"\n{DIM}━━━ Tekan Enter untuk lanjut ━━━{RESET}\n")

# ============================================================
# HARGA CRYPTO (dari Bot Kripto)
# ============================================================
def harga_crypto():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  🪙 HARGA CRYPTO — REAL-TIME                                            ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{CYAN}⏳ Mengambil data...{RESET}\n""")
    
    try:
        import requests
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin,cardano,ripple,dogecoin&vs_currencies=usd,idr&include_24hr_change=true",
            timeout=15
        )
        
        if r.status_code != 200:
            print(f"{RED}❌ API error: {r.status_code}{RESET}\n")
            pause(); return
        
        data = r.json()
        
        print(f"{BOLD}{'Coin':12} {'USD':>15} {'IDR':>20} {'24H':>10}{RESET}")
        print(f"{DIM}{'─' * 60}{RESET}")
        
        for coin, prices in data.items():
            usd = prices.get('usd', 0)
            idr = prices.get('idr', 0)
            change = prices.get('usd_24h_change', 0)
            color = GREEN if change > 0 else RED
            symbol = "▲" if change > 0 else "▼"
            print(f"{GOLD}{coin.upper():12}{RESET} ${usd:>13,.2f} Rp{idr:>18,.0f} {color}{symbol}{change:>6.2f}%{RESET}")
        
        print()
    except Exception as e:
        print(f"{RED}❌ Gagal ambil data: {e}{RESET}\n")
    
    pause()

# ============================================================
# PREDIKSI CRYPTO (Zuhri Formalism)
# ============================================================
def zuhri_predict(coin):
    try:
        import requests
        r = requests.get(
            f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=7",
            timeout=15
        )
        
        if r.status_code != 200:
            return {"error": f"API error: {r.status_code}"}
        
        data = r.json()
        prices = [p[1] for p in data.get('prices', [])]
        
        if len(prices) < 10:
            return {"error": "Data tidak cukup"}
        
        current = prices[-1]
        prev_24h = prices[-24] if len(prices) > 24 else prices[0]
        change_24h = ((current - prev_24h) / prev_24h) * 100
        
        h = hashlib.sha3_256(f"{coin}{current}{datetime.now().strftime('%Y%m%d')}".encode()).hexdigest()
        resonansi = (sum(int(c, 16) for c in h[:16]) % 10 + 8) % 10
        momentum = (prices[-1] - prices[0]) / prices[0] * 100
        
        if change_24h > 5:
            prediction = "TURUN (koreksi)"; reason = "Harga naik terlalu cepat"; confidence = min(70 + resonansi * 3, 95)
        elif change_24h < -5:
            prediction = "NAIK (rebound)"; reason = "Harga turun terlalu dalam"; confidence = min(65 + resonansi * 3, 90)
        elif momentum > 10:
            prediction = "NAIK (tren positif)"; reason = "Tren 7 hari positif"; confidence = min(60 + resonansi * 3, 85)
        elif momentum < -10:
            prediction = "TURUN (tren negatif)"; reason = "Tren 7 hari negatif"; confidence = min(60 + resonansi * 3, 85)
        else:
            prediction = "SIDEWAYS (konsolidasi)"; reason = "Harga stabil"; confidence = min(50 + resonansi * 3, 75)
        
        return {
            "coin": coin, "current_price": current,
            "change_24h": round(change_24h, 2), "momentum_7d": round(momentum, 2),
            "prediction": prediction, "reason": reason,
            "confidence": confidence, "resonansi": resonansi,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

def prediksi_crypto():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  🔮 PREDIKSI CRYPTO — ZUHRI FORMALISM                                   ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}Pilih coin:{RESET}
  {GOLD}1.{RESET} BITCOIN
  {GOLD}2.{RESET} ETHEREUM
  {GOLD}3.{RESET} SOLANA
  {GOLD}4.{RESET} BINANCECOIN
  {GOLD}5.{RESET} CARDANO
""")
    
    coins = ["bitcoin", "ethereum", "solana", "binancecoin", "cardano"]
    try:
        c = int(input(f"{CYAN}Pilih (1-5): {RESET}")) - 1
        if not (0 <= c < len(coins)): return
        
        coin = coins[c]
        print(f"\n{CYAN}⏳ Menganalisis {coin}...{RESET}\n")
        
        result = zuhri_predict(coin)
        
        if "error" in result:
            print(f"{RED}❌ {result['error']}{RESET}\n")
            pause(); return
        
        color = GREEN if "NAIK" in result['prediction'] else (RED if "TURUN" in result['prediction'] else YELLOW)
        
        print(f"""
{BOLD}📊 HASIL PREDIKSI:{RESET}

  {GOLD}Coin:{RESET}          {result['coin'].upper()}
  {GOLD}Harga:{RESET}         ${result['current_price']:,.2f}
  {GOLD}Perubahan 24H:{RESET} {result['change_24h']:+.2f}%
  {GOLD}Momentum 7D:{RESET}   {result['momentum_7d']:+.2f}%
  {GOLD}Resonansi:{RESET}     {result['resonansi']}/9

{BOLD}🔮 PREDIKSI:{RESET} {color}{result['prediction']}{RESET}
{BOLD}📋 ALASAN:{RESET}   {result['reason']}
{BOLD}📊 CONFIDENCE:{RESET} {result['confidence']}%

{YELLOW}⚠️  PREDIKSI, bukan jaminan. DYOR!{RESET}
""")
        
        f = os.path.join(PRED_DIR, f"{coin}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        try: json.dump(result, open(f, "w"), indent=2)
        except: pass
    except: pass
    
    pause()

# ============================================================
# PANDUAN KEUANGAN
# ============================================================
def panduan():
    while True:
        clear()
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  📚 PANDUAN DUNIA KEUANGAN                                              ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}1.{RESET}  📈 Saham
  {GOLD}2.{RESET}  💰 Investasi
  {GOLD}3.{RESET}  💱 Forex
  {GOLD}4.{RESET}  📜 Obligasi
  {GOLD}5.{RESET}  📊 Reksa Dana
  {GOLD}6.{RESET}  🏭 Komoditas
  {GOLD}7.{RESET}  📅 Berjangka
  {GOLD}8.{RESET}  🪙 Kripto
  {GOLD}9.{RESET}  🏛️  Pasar Modal Indonesia
  {GOLD}10.{RESET} 🏦 Bank Kustodian
  {GOLD}11.{RESET} 👥 Investor & Emiten
  {GOLD}0.{RESET}  Kembali
""")
        try:
            c = input(f"{GOLD}Pilih (0-11): {RESET}").strip()
            if c == "0": break
            elif c == "1": panduan_saham()
            elif c == "2": panduan_investasi()
            elif c == "3": panduan_forex()
            elif c == "4": panduan_obligasi()
            elif c == "5": panduan_reksadana()
            elif c == "6": panduan_komoditas()
            elif c == "7": panduan_berjangka()
            elif c == "8": panduan_kripto()
            elif c == "9": panduan_pasarmodal()
            elif c == "10": panduan_kustodian()
            elif c == "11": panduan_investor()
        except KeyboardInterrupt: break

def panduan_saham():
    clear()
    print(f"""
{BOLD}{CYAN}📈 SAHAM{RESET}

{BOLD}📖 Definisi:{RESET} Bukti kepemilikan perusahaan.

{BOLD}🎯 Jenis:{RESET}
  {GOLD}•{RESET} Blue Chip — stabil (BBCA, BBRI)
  {GOLD}•{RESET} Second Liner — menengah
  {GOLD}•{RESET} Third Liner — kecil, risiko tinggi

{BOLD}💡 Tips:{RESET}
  {GREEN}✅{RESET} Belajar fundamental & teknikal
  {GREEN}✅{RESET} Diversifikasi
  {RED}❌{RESET} Jangan FOMO

{BOLD}📱 Platform:{RESET} IDX, Stockbit, Bibit, Ajaib, Mirae
""")
    pause()

def panduan_investasi():
    clear()
    print(f"""
{BOLD}{CYAN}💰 INVESTASI{RESET}

{BOLD}📖 Definisi:{RESET} Menempatkan dana untuk keuntungan masa depan.

{BOLD}🎯 Jenis:{RESET}
  {GOLD}•{RESET} Saham — return tinggi, risiko tinggi
  {GOLD}•{RESET} Obligasi — return sedang
  {GOLD}•{RESET} Reksa Dana — dikelola MI
  {GOLD}•{RESET} Emas — lindung inflasi
  {GOLD}•{RESET} Kripto — volatil

{BOLD}💡 Prinsip:{RESET} High risk, high return. Diversifikasi!
""")
    pause()

def panduan_forex():
    clear()
    print(f"""
{BOLD}{CYAN}💱 FOREX{RESET}

{BOLD}📖 Definisi:{RESET} Perdagangan mata uang asing.

{BOLD}🎯 Pasangan:{RESET}
  {GOLD}•{RESET} Major: EUR/USD, GBP/USD
  {GOLD}•{RESET} Minor: EUR/GBP
  {GOLD}•{RESET} Exotic: USD/IDR

{BOLD}⚠️  Risiko:{RESET} {RED}Leverage tinggi, 70-90% trader rugi{RESET}

{BOLD}💡 Saran:{RESET} Belajar 6-12 bulan, broker berizin BAPPEBTI
""")
    pause()

def panduan_obligasi():
    clear()
    print(f"""
{BOLD}{CYAN}📜 OBLIGASI{RESET}

{BOLD}📖 Definisi:{RESET} Surat utang. Anda meminjamkan uang, dapat bunga.

{BOLD}🎯 Jenis:{RESET}
  {GOLD}•{RESET} SUN — pemerintah
  {GOLD}•{RESET} SBSN/Sukuk — syariah
  {GOLD}•{RESET} Obligasi Korporasi
  {GOLD}•{RESET} ORI, SR — ritel

{BOLD}📊 Istilah:{RESET} Kupon, Tenor, Yield, Rating

{BOLD}💡 Keuntungan:{RESET} Return stabil, risiko lebih rendah
""")
    pause()

def panduan_reksadana():
    clear()
    print(f"""
{BOLD}{CYAN}📊 REKSA DANA{RESET}

{BOLD}📖 Definisi:{RESET} Wadah investasi dikelola Manajer Investasi.

{BOLD}🎯 Jenis:{RESET}
  {GOLD}•{RESET} Pasar Uang — 4-6%
  {GOLD}•{RESET} Pendapatan Tetap — 6-8%
  {GOLD}•{RESET} Campuran — 8-12%
  {GOLD}•{RESET} Saham — 12-20%

{BOLD}📱 Platform:{RESET} Bibit, Bareksa, Ajaib, Tanamduit
""")
    pause()

def panduan_komoditas():
    clear()
    print(f"""
{BOLD}{CYAN}🏭 KOMODITAS{RESET}

{BOLD}📖 Definisi:{RESET} Barang mentah yang diperdagangkan.

{BOLD}🎯 Jenis:{RESET}
  {GOLD}•{RESET} Logam: Emas, Perak
  {GOLD}•{RESET} Energi: Minyak, Gas
  {GOLD}•{RESET} Pertanian: Kopi, CPO, Jagung

{BOLD}💡 Faktor Harga:{RESET} Supply-demand, geopolitik, cuaca
""")
    pause()

def panduan_berjangka():
    clear()
    print(f"""
{BOLD}{CYAN}📅 BERJANGKA (FUTURES){RESET}

{BOLD}📖 Definisi:{RESET} Kontrak beli/jual aset di masa depan.

{BOLD}⚠️  Risiko:{RESET} {RED}Leverage tinggi, bisa rugi lebih dari modal{RESET}

{BOLD}📱 Bursa:{RESET} BBJ, BKDI
""")
    pause()

def panduan_kripto():
    clear()
    print(f"""
{BOLD}{CYAN}🪙 KRIPTO{RESET}

{BOLD}📖 Definisi:{RESET} Mata uang digital berbasis blockchain.

{BOLD}🎯 Jenis:{RESET}
  {GOLD}•{RESET} Bitcoin (BTC) — pionir
  {GOLD}•{RESET} Ethereum (ETH) — smart contract
  {GOLD}•{RESET} Solana (SOL) — cepat
  {GOLD}•{RESET} Stablecoin — USDT, USDC
  {GOLD}•{RESET} Meme Coin — DOGE, SHIB (micin!)

{BOLD}💡 Strategi:{RESET} DCA, simpan di hardware wallet, jangan FOMO

{BOLD}📱 Exchange:{RESET} Indodax, Pintu, Binance, OKX
""")
    pause()

def panduan_pasarmodal():
    clear()
    print(f"""
{BOLD}{CYAN}🏛️  PASAR MODAL INDONESIA{RESET}

{BOLD}🏛️  Lembaga:{RESET}
  {GOLD}•{RESET} OJK — regulator
  {GOLD}•{RESET} IDX/BEI — bursa
  {GOLD}•{RESET} KPEI — kliring
  {GOLD}•{RESET} KSEI — kustodian sentral
  {GOLD}•{RESET} Sekuritas — broker

{BOLD}📈 Indeks:{RESET} IHSG, LQ45, IDX30, JII

{BOLD}💡 Cara Mulai:{RESET}
  1. Buka rekening sekuritas
  2. Setor dana (mulai Rp100.000)
  3. Download aplikasi
  4. Mulai beli
""")
    pause()

def panduan_kustodian():
    clear()
    print(f"""
{BOLD}{CYAN}🏦 BANK KUSTODIAN & SEKURITAS{RESET}

{BOLD}🏦 Bank Kustodian:{RESET}
  {GOLD}Definisi:{RESET} Menyimpan & mengadministrasikan aset investor.

  {GOLD}Contoh:{RESET} Bank Mandiri, BNI, CIMB Niaga, HSBC

{BOLD}📊 Sekuritas:{RESET}
  {GOLD}Definisi:{RESET} Perantara jual-beli efek.

  {GOLD}Contoh:{RESET} Mirae, Mandiri Sekuritas, BCA Sekuritas

{BOLD}💡 Perbedaan:{RESET}
  {GOLD}•{RESET} Sekuritas = tempat transaksi
  {GOLD}•{RESET} Kustodian = tempat penyimpanan
""")
    pause()

def panduan_investor():
    clear()
    print(f"""
{BOLD}{CYAN}👥 INVESTOR, EMITEN & PREDIKSI{RESET}

{BOLD}👤 Investor:{RESET} Pihak yang menanamkan dana.
  {GOLD}•{RESET} Retail, Institusi, Asing, Domestik

{BOLD}🏢 Emiten:{RESET} Perusahaan penerbit saham/obligasi.
  {GOLD}•{RESET} Blue Chip, Mid Cap, Small Cap

{BOLD}🔮 Prediksi 2026-2030:{RESET}

  {GOLD}📈 Saham:{RESET} IHSG 8.000-10.000
  {GOLD}📜 Obligasi:{RESET} Yield SUN 5-7%
  {GOLD}📊 Reksa Dana:{RESET} AUM tumbuh 15-20%/tahun
  {GOLD}🪙 Kripto:{RESET} Adopsi institusi naik, regulasi jelas
  {GOLD}🏭 Komoditas:{RESET} Emas safe haven, CPO permintaan naik
""")
    pause()

# ============================================================
# BERITA FINANSIAL
# ============================================================
def berita_finansial():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  📰 BERITA FINANSIAL — LOKAL & GLOBAL                                   ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}🇮🇩 LOKAL:{RESET}
  {GOLD}1.{RESET}  Kontan              → kontan.co.id
  {GOLD}2.{RESET}  Bisnis Indonesia    → bisnis.com
  {GOLD}3.{RESET}  CNBC Indonesia      → cnbcindonesia.com
  {GOLD}4.{RESET}  Detik Finance       → finance.detik.com
  {GOLD}5.{RESET}  IDX Channel         → idxchannel.com
  {GOLD}6.{RESET}  Katadata            → katadata.co.id

{BOLD}🌍 GLOBAL:{RESET}
  {GOLD}7.{RESET}  Bloomberg           → bloomberg.com
  {GOLD}8.{RESET}  Reuters             → reuters.com
  {GOLD}9.{RESET}  CNBC                → cnbc.com
  {GOLD}10.{RESET} Financial Times     → ft.com
  {GOLD}11.{RESET} Wall Street Journal → wsj.com
  {GOLD}12.{RESET} Yahoo Finance       → finance.yahoo.com
  {GOLD}13.{RESET} Investing.com       → investing.com
  {GOLD}14.{RESET} TradingView         → tradingview.com

{BOLD}🪙 KRIPTO:{RESET}
  {GOLD}15.{RESET} CoinDesk            → coindesk.com
  {GOLD}16.{RESET} Cointelegraph       → cointelegraph.com

{BOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih (0-16): {RESET}").strip()
        if c == "0": return
        urls = {
            "1": "https://kontan.co.id", "2": "https://bisnis.com",
            "3": "https://cnbcindonesia.com", "4": "https://finance.detik.com",
            "5": "https://idxchannel.com", "6": "https://katadata.co.id",
            "7": "https://bloomberg.com", "8": "https://reuters.com",
            "9": "https://cnbc.com", "10": "https://ft.com",
            "11": "https://wsj.com", "12": "https://finance.yahoo.com",
            "13": "https://investing.com", "14": "https://tradingview.com",
            "15": "https://coindesk.com", "16": "https://cointelegraph.com",
        }
        if c in urls:
            print(f"\n{CYAN}🌐 Membuka...{RESET}")
            try: subprocess.run(["termux-open-url", urls[c]], timeout=5)
            except: print(f"{YELLOW}Buka manual: {urls[c]}{RESET}")
    except: pass
    pause()

# ============================================================
# PREDIKSI SAHAM/OBLIGASI/REKSA DANA
# ============================================================
def prediksi_finansial():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  🔮 PREDIKSI SAHAM/OBLIGASI/REKSA DANA                                  ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}1.{RESET} Saham
  {GOLD}2.{RESET} Obligasi
  {GOLD}3.{RESET} Reksa Dana
  {GOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "0": return
        if c == "1":
            kode = input("Kode saham (BBCA): ").strip().upper()
            if kode:
                h = hashlib.sha3_256(f"{kode}{datetime.now().strftime('%Y%m%d')}".encode()).hexdigest()
                resonansi = (sum(int(x, 16) for x in h[:16]) % 10 + 8) % 10
                random.seed(resonansi)
                change = random.uniform(-10, 10)
                pred = "NAIK" if change > 3 else ("TURUN" if change < -3 else "SIDEWAYS")
                color = GREEN if "NAIK" in pred else (RED if "TURUN" in pred else YELLOW)
                print(f"""
{BOLD}📊 PREDIKSI: {kode}{RESET}
  Resonansi: {resonansi}/9
  Prediksi : {color}{pred}{RESET}
  Perubahan: {change:+.2f}%
  Confidence: {50 + resonansi * 4}%
""")
        elif c == "2":
            print(f"""
{BOLD}📜 PREDIKSI OBLIGASI{RESET}
  • SUN 10Y: 6.5-7.0%
  • Sukuk Ritel: 6.0-6.5%
  • {GREEN}STABIL — cenderung naik{RESET}
""")
        elif c == "3":
            print(f"""
{BOLD}📊 PREDIKSI REKSA DANA{RESET}
  • Pasar Uang: 4-6%
  • Pendapatan Tetap: 6-8%
  • Campuran: 8-12%
  • Saham: 12-18%
  • {GREEN}POSITIF{RESET}
""")
    except: pass
    pause()

# ============================================================
# KRIPTO MICIN
# ============================================================
def kripto_micin():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  🪙 KRIPTO TERBARU (MICIN) — MEME COINS                                 ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{RED}⚠️  SPEKULATIF TINGGI — BISA RUGI 100%{RESET}

{BOLD}🎯 DAFTAR:{RESET}
  {GOLD}•{RESET} DOGE — pionir
  {GOLD}•{RESET} SHIB — Shiba Inu
  {GOLD}•{RESET} PEPE — meme katak
  {GOLD}•{RESET} BONK — Solana
  {GOLD}•{RESET} WIF — dogwifhat
  {GOLD}•{RESET} FLOKI — Floki Inu
  {GOLD}•{RESET} BOME — Book of Meme

{BOLD}💡 Strategi:{RESET}
  {GREEN}✅{RESET} Beli early
  {GREEN}✅{RESET} Take profit bertahap
  {GREEN}✅{RESET} Siap rugi 100%
  {RED}❌{RESET} Jangan pakai leverage
  {RED}❌{RESET} Waspada honeypot

{BOLD}📱 Cara Beli:{RESET}
  1. Beli SOL/USDT
  2. Transfer ke Phantom wallet
  3. Swap di Jupiter/Raydium
""")
    pause()

# ============================================================
# WATCHLIST
# ============================================================
def watchlist():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  📋 WATCHLIST                                                           ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
""")
    wl_file = os.path.join(WATCH_DIR, "watchlist.json")
    wl = json.load(open(wl_file)) if os.path.exists(wl_file) else []
    
    if wl:
        print(f"{BOLD}Watchlist:{RESET}")
        for i, item in enumerate(wl, 1):
            print(f"  {GOLD}{i}.{RESET} [{item.get('tipe','?')}] {item.get('kode','?')}")
    else:
        print(f"{YELLOW}Kosong.{RESET}\n")
    
    print(f"\n{GOLD}1.{RESET} Tambah  {GOLD}2.{RESET} Hapus  {GOLD}0.{RESET} Kembali")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "1":
            tipe = input("Tipe: ").strip().lower()
            kode = input("Kode: ").strip().upper()
            if tipe and kode:
                wl.append({"tipe": tipe, "kode": kode, "added": datetime.now().isoformat()})
                json.dump(wl, open(wl_file, "w"), indent=2)
                print(f"{GREEN}✅ Ditambahkan{RESET}")
        elif c == "2" and wl:
            try:
                idx = int(input(f"Nomor: ")) - 1
                if 0 <= idx < len(wl):
                    wl.pop(idx)
                    json.dump(wl, open(wl_file, "w"), indent=2)
                    print(f"{GREEN}✅ Dihapus{RESET}")
            except: pass
    except: pass
    pause()

# ============================================================
# INFO
# ============================================================
def info():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  ℹ️  INFO ZUHRI FINANSIAL ULTIMATE                                       ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}🎯 GABUNGAN DARI:{RESET}
  {GOLD}•{RESET} Zuhri Bot Kriptografi
  {GOLD}•{RESET} Zuhri Finansial Pro

{BOLD}📚 FITUR LENGKAP:{RESET}
  {GOLD}1.{RESET} 🪙 Harga Crypto Real-time
  {GOLD}2.{RESET} 🔮 Prediksi Crypto (Zuhri Formalism)
  {GOLD}3.{RESET} 📚 Panduan Keuangan (11 topik)
  {GOLD}4.{RESET} 📰 Berita Finansial (16 sumber)
  {GOLD}5.{RESET} 🔮 Prediksi Saham/Obligasi/Reksa Dana
  {GOLD}6.{RESET} 🏭 Komoditas & Berjangka
  {GOLD}7.{RESET} 🪙 Kripto Micin (Meme Coins)
  {GOLD}8.{RESET} 📋 Watchlist

{BOLD}⚠️  DISCLAIMER:{RESET}
  {RED}❌ BUKAN SARAN INVESTASI{RESET}
  {RED}❌ Prediksi TIDAK 100% AKURAT{RESET}
  {RED}❌ Semua investasi ada risiko{RESET}
  {GREEN}✅ Gunakan sebagai EDUKASI{RESET}
  {GREEN}✅ DYOR (Do Your Own Research){RESET}
""")
    pause()

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        clear()
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  💰 ZUHRI FINANSIAL ULTIMATE — BOT KRIPTO + FINANSIAL PRO               ║
║  ──────────────────────────────────────────────────────────────────────  ║
║  Crypto • Saham • Obligasi • Forex • Reksa Dana • Komoditas • Kripto    ║
║  Waktu: {GOLD}{datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}{RESET}
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU UTAMA:{RESET}
  {GOLD}1.{RESET}  🪙 Harga Crypto Real-time
  {GOLD}2.{RESET}  🔮 Prediksi Crypto (Zuhri Formalism)
  {GOLD}3.{RESET}  📚 Panduan Keuangan (11 Topik)
  {GOLD}4.{RESET}  📰 Berita Finansial (Lokal & Global)
  {GOLD}5.{RESET}  🔮 Prediksi Saham/Obligasi/Reksa Dana
  {GOLD}6.{RESET}  🏭 Komoditas & Berjangka
  {GOLD}7.{RESET}  🪙 Kripto Micin (Meme Coins)
  {GOLD}8.{RESET}  📋 Watchlist Aset
  {GOLD}9.{RESET}  ℹ️  Info & Disclaimer
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-9): {RESET}").strip()
            if c == "0": break
            elif c == "1": harga_crypto()
            elif c == "2": prediksi_crypto()
            elif c == "3": panduan()
            elif c == "4": berita_finansial()
            elif c == "5": prediksi_finansial()
            elif c == "6":
                clear()
                print(f"""
{BOLD}🏭 KOMODITAS & BERJANGKA{RESET}

  {GOLD}🥇 Emas{X}    : $2.600-2.800/oz → {GREEN}NAIK{RESET}
  {GOLD}🛢️  Minyak{X}  : $70-90/barel  → {YELLOW}SIDEWAYS{RESET}
  {GOLD}🌴 CPO{RESET}     : RM 3.500-4.500 → {GREEN}NAIK{RESET}
  {GOLD}☕ Kopi{RESET}    : $200-300/lbs  → {GREEN}NAIK{RESET}

  {DIM}Alasan: ketidakpastian global, supply-demand{RESET}
""")
                pause()
            elif c == "7": kripto_micin()
            elif c == "8": watchlist()
            elif c == "9": info()
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "harga": harga_crypto()
        elif cmd == "prediksi": prediksi_crypto()
        elif cmd == "panduan": panduan()
        elif cmd == "berita": berita_finansial()
        else: menu()
    else: menu()
