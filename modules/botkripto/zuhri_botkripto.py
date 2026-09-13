#!/usr/bin/env python3
"""
ZUHRI BOT KRIPTOGRAFI — BOT KRIPTO TERBARU
Pasar Modal + Berita + Prediksi berbasis Zuhri Formalism
"""

import os, sys, json, hashlib, secrets, subprocess, time, random
from datetime import datetime, timedelta

# ===== ZUHRI AUTH (FIX) =====
sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False
    def log_verified(msg): pass

HOME = os.path.expanduser("~")
BOT_DIR = os.path.join(HOME, "zuhri_os", "botkripto")
DATA_DIR = os.path.join(BOT_DIR, "data")
LOG_DIR = os.path.join(BOT_DIR, "logs")
PRED_DIR = os.path.join(BOT_DIR, "predictions")
for d in [DATA_DIR, LOG_DIR, PRED_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

def clear(): os.system('clear')
def pause():
    input(f"\n{DIM}━━━ Tekan Enter untuk lanjut ━━━{RESET}\n")

# ============================================================
# ZUHRI FORMALISM — PREDIKSI
# ============================================================
def zuhri_predict(coin):
    """Prediksi berbasis Zuhri Formalism"""
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
        
        # Analisis
        current = prices[-1]
        prev_24h = prices[-24] if len(prices) > 24 else prices[0]
        change_24h = ((current - prev_24h) / prev_24h) * 100
        
        # Resonansi 0-8-9
        h = hashlib.sha3_256(f"{coin}{current}{datetime.now().strftime('%Y%m%d')}".encode()).hexdigest()
        resonansi = (sum(int(c, 16) for c in h[:16]) % 10 + 8) % 10
        
        # Momentum 7 hari
        momentum = (prices[-1] - prices[0]) / prices[0] * 100
        
        # Prediksi berdasarkan logika 0-8-9
        if change_24h > 5:
            prediction = "TURUN (koreksi)"
            reason = "Harga naik terlalu cepat — perlu koreksi"
            confidence = min(70 + resonansi * 3, 95)
        elif change_24h < -5:
            prediction = "NAIK (rebound)"
            reason = "Harga turun terlalu dalam — ada peluang rebound"
            confidence = min(65 + resonansi * 3, 90)
        elif momentum > 10:
            prediction = "NAIK (tren positif)"
            reason = "Tren 7 hari positif — momentum berlanjut"
            confidence = min(60 + resonansi * 3, 85)
        elif momentum < -10:
            prediction = "TURUN (tren negatif)"
            reason = "Tren 7 hari negatif — tekanan jual"
            confidence = min(60 + resonansi * 3, 85)
        else:
            prediction = "SIDEWAYS (konsolidasi)"
            reason = "Harga stabil — pasar menunggu"
            confidence = min(50 + resonansi * 3, 75)
        
        return {
            "coin": coin,
            "current_price": current,
            "change_24h": round(change_24h, 2),
            "momentum_7d": round(momentum, 2),
            "prediction": prediction,
            "reason": reason,
            "confidence": confidence,
            "resonansi": resonansi,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

# ============================================================
# HARGA CRYPTO
# ============================================================
def harga_crypto():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  💰 ZUHRI BOT KRIPTOGRAFI — HARGA CRYPTO                                ║
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
            pause()
            return
        
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
        if ZUHRI_ID_OK:
            try:
                log_verified("BOT_KRIPTO_PRICE")
            except:
                pass
    except Exception as e:
        print(f"{RED}❌ Gagal ambil data: {e}{RESET}\n")
    
    pause()

# ============================================================
# PREDIKSI ZUHRI FORMALISM (FIXED)
# ============================================================
def prediksi():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  🔮 PREDIKSI KRIPTO — ZUHRI FORMALISM                                   ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Basis: Logika + Data + Intuisi (0-8-9){RESET}
""")
    
    coins = ["bitcoin", "ethereum", "solana", "binancecoin", "cardano"]
    print(f"{BOLD}Pilih coin:{RESET}")
    for i, c in enumerate(coins, 1):
        print(f"  {GOLD}{i}.{RESET} {c.upper()}")
    
    try:
        c = int(input(f"\n{CYAN}Pilih (1-{len(coins)}): {RESET}")) - 1
        if not (0 <= c < len(coins)):
            return
        
        coin = coins[c]
        print(f"\n{CYAN}⏳ Menganalisis {coin}...{RESET}\n")
        
        result = zuhri_predict(coin)
        
        # CEK ERROR
        if "error" in result:
            print(f"{RED}❌ Error: {result['error']}{RESET}")
            print(f"{DIM}💡 Coba lagi nanti atau cek koneksi internet.{RESET}\n")
            pause()
            return
        
        # Tampilkan hasil
        if "NAIK" in result['prediction']:
            color = GREEN
        elif "TURUN" in result['prediction']:
            color = RED
        else:
            color = YELLOW
        
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

{DIM}Timestamp: {result['timestamp'][:19]}{RESET}

{BOLD}{YELLOW}⚠️  CATATAN:{RESET}
  {DIM}• Ini PREDIKSI, bukan jaminan${RESET}
  {DIM}• Crypto sangat volatil${RESET}
  {DIM}• DYOR (Do Your Own Research)${RESET}
  {DIM}• Jangan invest lebih dari kemampuan${RESET}
""")
        
        # Simpan prediksi
        try:
            f = os.path.join(PRED_DIR, f"{coin}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            json.dump(result, open(f, "w"), indent=2)
        except:
            pass
        
        if ZUHRI_ID_OK:
            try:
                log_verified(f"BOT_KRIPTO_PREDICT: {coin}")
            except:
                pass
    
    except ValueError:
        print(f"{RED}❌ Input tidak valid{RESET}\n")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}\n")
    
    pause()

# ============================================================
# BERITA KRIPTO
# ============================================================
def berita():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  📰 BERITA KRIPTO — SUMBER TERPERCAYA                                   ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📰 SUMBER BERITA:{RESET}

  {GOLD}1.{RESET} CoinDesk          → https://www.coindesk.com
  {GOLD}2.{RESET} Cointelegraph     → https://cointelegraph.com
  {GOLD}3.{RESET} The Block         → https://www.theblock.co
  {GOLD}4.{RESET} Blockworks        → https://blockworks.co
  {GOLD}5.{RESET} Decrypt           → https://decrypt.co
  {GOLD}6.{RESET} Bitcoin Magazine  → https://bitcoinmagazine.com
  {GOLD}7.{RESET} CoinMarketCap     → https://coinmarketcap.com
  {GOLD}8.{RESET} CoinGecko         → https://www.coingecko.com

{BOLD}0.{RESET} Kembali
""")
    
    try:
        c = input(f"{GOLD}Pilih (0-8): {RESET}").strip()
        if c == "0": return
        
        urls = {
            "1": "https://www.coindesk.com",
            "2": "https://cointelegraph.com",
            "3": "https://www.theblock.co",
            "4": "https://blockworks.co",
            "5": "https://decrypt.co",
            "6": "https://bitcoinmagazine.com",
            "7": "https://coinmarketcap.com",
            "8": "https://www.coingecko.com",
        }
        
        if c in urls:
            print(f"\n{CYAN}🌐 Membuka...{RESET}")
            try:
                subprocess.run(["termux-open-url", urls[c]], timeout=5)
            except:
                print(f"{YELLOW}⚠️  Buka manual: {urls[c]}{RESET}")
            
            if ZUHRI_ID_OK:
                try:
                    log_verified(f"BOT_KRIPTO_NEWS: {c}")
                except:
                    pass
    except:
        pass
    
    pause()

# ============================================================
# PASAR MODAL
# ============================================================
def pasar_modal():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  📈 PASAR MODAL — CRYPTO MARKET                                         ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📊 DATA GLOBAL:{RESET}
""")
    
    try:
        import requests
        r = requests.get("https://api.coingecko.com/api/v3/global", timeout=15)
        data = r.json().get('data', {})
        
        total_market = data.get('total_market_cap', {}).get('usd', 0)
        total_volume = data.get('total_volume', {}).get('usd', 0)
        btc_dominance = data.get('market_cap_percentage', {}).get('btc', 0)
        eth_dominance = data.get('market_cap_percentage', {}).get('eth', 0)
        active_coins = data.get('active_cryptocurrencies', 0)
        market_change = data.get('market_cap_change_percentage_24h_usd', 0)
        
        color = GREEN if market_change > 0 else RED
        symbol = "▲" if market_change > 0 else "▼"
        
        print(f"  {GOLD}Total Market Cap:{RESET}  ${total_market:,.0f}")
        print(f"  {GOLD}Total Volume 24H:{RESET}  ${total_volume:,.0f}")
        print(f"  {GOLD}BTC Dominance:{RESET}      {btc_dominance:.2f}%")
        print(f"  {GOLD}ETH Dominance:{RESET}      {eth_dominance:.2f}%")
        print(f"  {GOLD}Active Coins:{RESET}       {active_coins:,}")
        print(f"  {GOLD}Market Change 24H:{RESET}  {color}{symbol}{market_change:+.2f}%{RESET}")
        
        print(f"""
{BOLD}📈 TREN PASAR:{RESET}
  {GOLD}•{RESET} Fear & Greed: https://alternative.me/crypto/fear-and-greed-index/
  {GOLD}•{RESET} Trending: https://coingecko.com/en/trending
  {GOLD}•{RESET} Top Gainers: https://coinmarketcap.com/gainers-losers/

{BOLD}🔗 LINK:{RESET}
  {GOLD}•{RESET} CoinMarketCap: https://coinmarketcap.com
  {GOLD}•{RESET} CoinGecko: https://www.coingecko.com
  {GOLD}•{RESET} TradingView: https://www.tradingview.com
""")
        
        if ZUHRI_ID_OK:
            try:
                log_verified("BOT_KRIPTO_MARKET")
            except:
                pass
    except Exception as e:
        print(f"{RED}❌ Gagal ambil data: {e}{RESET}\n")
    
    pause()

# ============================================================
# PORTFOLIO
# ============================================================
def portfolio():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  💼 PORTFOLIO SEDERHANA                                                 ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    port_file = os.path.join(DATA_DIR, "portfolio.json")
    
    if os.path.exists(port_file):
        try:
            port = json.load(open(port_file))
        except:
            port = {}
    else:
        port = {}
    
    if not port:
        print(f"{YELLOW}Portfolio kosong.{RESET}\n")
        print(f"{GOLD}Tambah coin?{RESET}")
        coin = input("Coin (mis: bitcoin): ").strip().lower()
        amount = input("Jumlah: ").strip()
        
        if coin and amount:
            try:
                port[coin] = float(amount)
                json.dump(port, open(port_file, "w"), indent=2)
                print(f"{GREEN}✅ {coin}: {amount}{RESET}\n")
            except:
                pass
    else:
        print(f"{BOLD}Portfolio Anda:{RESET}\n")
        try:
            import requests
            ids = ",".join(port.keys())
            r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd,idr", timeout=15)
            data = r.json()
            
            total_usd = 0
            total_idr = 0
            
            for coin, amount in port.items():
                if coin in data:
                    usd = data[coin].get('usd', 0) * amount
                    idr = data[coin].get('idr', 0) * amount
                    total_usd += usd
                    total_idr += idr
                    print(f"  {GOLD}{coin.upper():12}{RESET} {amount} = ${usd:,.2f} | Rp{idr:,.0f}")
            
            print(f"\n  {BOLD}Total: ${total_usd:,.2f} | Rp{total_idr:,.0f}{RESET}\n")
        except:
            print(f"{RED}❌ Gagal ambil harga{RESET}\n")
    
    pause()

# ============================================================
# INFO
# ============================================================
def info():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  ℹ️  INFO BOT KRIPTOGRAFI                                                ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}🎯 FITUR:{RESET}
  {GOLD}•{RESET} Harga crypto real-time
  {GOLD}•{RESET} Prediksi berbasis Zuhri Formalism
  {GOLD}•{RESET} Berita dari sumber terpercaya
  {GOLD}•{RESET} Data pasar global
  {GOLD}•{RESET} Portfolio sederhana

{BOLD}🔮 PREDIKSI ZUHRI FORMALISM:{RESET}

  Prinsip {GOLD}0-8-9{RESET}:
  {GOLD}0{RESET} = Kosongkan asumsi
  {GOLD}8{RESET} = Buka kemungkinan
  {GOLD}9{RESET} = Temukan keseimbangan

  Analisis:
  {GOLD}•{RESET} Momentum 7 hari
  {GOLD}•{RESET} Perubahan 24 jam
  {GOLD}•{RESET} Resonansi (hash-based)

{BOLD}⚠️  DISCLAIMER:{RESET}
  {RED}❌ BUKAN SARAN INVESTASI{RESET}
  {RED}❌ Prediksi TIDAK 100% AKURAT{RESET}
  {RED}❌ Crypto SANGAT VOLATIL{RESET}
  {GREEN}✅ Gunakan sebagai REFERENSI{RESET}
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
║  🤖 ZUHRI BOT KRIPTOGRAFI — BOT KRIPTO TERBARU                          ║
║  ──────────────────────────────────────────────────────────────────────  ║
║  Pasar Modal + Berita + Prediksi Zuhri Formalism                        ║
║  Waktu: {GOLD}{datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}{RESET}
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  💰 Harga Crypto Real-time
  {GOLD}2.{RESET}  🔮 Prediksi (Zuhri Formalism)
  {GOLD}3.{RESET}  📰 Berita Kripto
  {GOLD}4.{RESET}  📈 Pasar Modal (Market Global)
  {GOLD}5.{RESET}  💼 Portfolio Sederhana
  {GOLD}6.{RESET}  ℹ️  Info & Disclaimer
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-6): {RESET}").strip()
            if c == "0": break
            elif c == "1": harga_crypto()
            elif c == "2": prediksi()
            elif c == "3": berita()
            elif c == "4": pasar_modal()
            elif c == "5": portfolio()
            elif c == "6": info()
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "harga": harga_crypto()
        elif cmd == "prediksi": prediksi()
        elif cmd == "berita": berita()
        elif cmd == "market": pasar_modal()
        else: menu()
    else: menu()
