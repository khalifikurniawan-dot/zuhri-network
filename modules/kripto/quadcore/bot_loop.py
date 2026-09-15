#!/data/data/com.termux/files/usr/bin/python
"""
QUAD-CORE BOT — ZUHRI KRIPTO
Bot trading dengan 4 core: SENTINEL, ORACLE, WARDEN, HERALD
Data real dari CoinGecko
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, time, requests
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
BOT_DIR = os.path.join(HOME, "zuhri_os", "kripto", "quadcore")
DATA_DIR = os.path.join(BOT_DIR, "data")
LOG_DIR = os.path.join(BOT_DIR, "logs")
for d in [DATA_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

STATE_FILE = os.path.join(DATA_DIR, "state.json")
LOG_FILE = os.path.join(LOG_DIR, "bot.log")

# ============================================================
# WARNA
# ============================================================
RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

# ============================================================
# STATE
# ============================================================
def load_state():
    if os.path.exists(STATE_FILE):
        try: return json.load(open(STATE_FILE))
        except: pass
    return {
        "coins": ["bitcoin", "ethereum", "solana", "binancecoin"],
        "history": {},
        "signals": [],
        "started": datetime.now().isoformat(),
        "cycle": 0
    }

def save_state(state):
    json.dump(state, open(STATE_FILE, "w"), indent=2)

def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] [{level}] {msg}\n")

# ============================================================
# CORE 1 — SENTINEL (Monitor Pasar)
# ============================================================
def sentinel_fetch(state):
    """Ambil data real dari CoinGecko"""
    coins = state['coins']
    ids = ",".join(coins)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd,idr&include_24hr_change=true"
    
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        log(f"SENTINEL error: {e}", "ERROR")
    return None

def sentinel_analyze(data, state):
    """Analisis data pasar"""
    alerts = []
    
    for coin, prices in data.items():
        usd = prices.get('usd', 0)
        change = prices.get('usd_24h_change', 0)
        
        # Simpan history
        if coin not in state['history']:
            state['history'][coin] = []
        
        state['history'][coin].append({
            "time": datetime.now().isoformat(),
            "usd": usd,
            "change": change
        })
        
        # Batasi history
        state['history'][coin] = state['history'][coin][-100:]
        
        # Deteksi anomali
        if abs(change) > 5:
            alerts.append({
                "coin": coin,
                "type": "VOLATILE",
                "change": change,
                "severity": "HIGH" if abs(change) > 10 else "MEDIUM"
            })
    
    return alerts

# ============================================================
# CORE 2 — ORACLE (Analisis & Prediksi)
# ============================================================
def oracle_predict(state):
    """Prediksi sederhana dari history"""
    predictions = []
    
    for coin, history in state['history'].items():
        if len(history) < 3:
            continue
        
        # Ambil 3 data terakhir
        recent = history[-3:]
        changes = [h['change'] for h in recent]
        
        # Simple moving average
        avg_change = sum(changes) / len(changes)
        
        # Prediksi
        if avg_change > 2:
            signal = "BUY"
            confidence = min(abs(avg_change) * 10, 95)
        elif avg_change < -2:
            signal = "SELL"
            confidence = min(abs(avg_change) * 10, 95)
        else:
            signal = "HOLD"
            confidence = 50
        
        predictions.append({
            "coin": coin,
            "signal": signal,
            "confidence": round(confidence, 1),
            "avg_change": round(avg_change, 2),
            "price": history[-1]['usd']
        })
    
    return predictions

# ============================================================
# CORE 3 — WARDEN (Manajemen Risiko)
# ============================================================
def warden_check(predictions, state):
    """Check risiko"""
    warnings = []
    
    # Portfolio config (simulasi)
    config = {
        "max_allocation": 0.3,  # Max 30% per coin
        "stop_loss": -10,       # -10%
        "take_profit": 20       # +20%
    }
    
    for p in predictions:
        # Cek confidence
        if p['confidence'] < 30:
            warnings.append({
                "coin": p['coin'],
                "type": "LOW_CONFIDENCE",
                "message": f"Sinyal {p['signal']} confidence rendah ({p['confidence']}%)"
            })
        
        # Cek volatilitas
        if abs(p['avg_change']) > 15:
            warnings.append({
                "coin": p['coin'],
                "type": "HIGH_VOLATILITY",
                "message": f"Volatilitas tinggi ({p['avg_change']}%)"
            })
    
    return warnings

# ============================================================
# CORE 4 — HERALD (Laporan & Notifikasi)
# ============================================================
def herald_report(data, predictions, warnings, cycle):
    """Tampilkan laporan"""
    os.system('clear')
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🤖 QUAD-CORE BOT — ZUHRI KRIPTO                                   ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Siklus: #{cycle} | Waktu: {datetime.now().strftime('%H:%M:%S')}                        ║
║  Data: CoinGecko API (Real-time)                                   ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    # SENTINEL — Monitor
    print(f"{BOLD}{CYAN}🛡️  SENTINEL — Monitor Pasar{RESET}")
    print(f"{DIM}{'─' * 65}{RESET}")
    for coin, prices in data.items():
        usd = prices.get('usd', 0)
        idr = prices.get('idr', 0)
        change = prices.get('usd_24h_change', 0)
        
        color = GREEN if change >= 0 else RED
        arrow = "▲" if change >= 0 else "▼"
        
        print(f"  {GOLD}{coin.upper():12}{RESET} ${usd:>12,.2f}  {color}{arrow} {change:>+6.2f}%{RESET}")
    print()
    
    # ORACLE — Prediksi
    print(f"{BOLD}{MAGENTA}🔮 ORACLE — Sinyal Trading{RESET}")
    print(f"{DIM}{'─' * 65}{RESET}")
    for p in predictions:
        if p['signal'] == 'BUY':
            signal_color = GREEN
            icon = "🟢"
        elif p['signal'] == 'SELL':
            signal_color = RED
            icon = "🔴"
        else:
            signal_color = YELLOW
            icon = "🟡"
        
        print(f"  {icon} {GOLD}{p['coin'].upper():12}{RESET} {signal_color}{p['signal']:5}{RESET}  Confidence: {p['confidence']:>5.1f}%  Avg: {p['avg_change']:>+5.2f}%")
    print()
    
    # WARDEN — Risiko
    if warnings:
        print(f"{BOLD}{YELLOW}⚠️  WARDEN — Peringatan Risiko{RESET}")
        print(f"{DIM}{'─' * 65}{RESET}")
        for w in warnings:
            print(f"  {YELLOW}⚠️{RESET} {w['coin'].upper():12} {w['message']}")
        print()
    else:
        print(f"{BOLD}{GREEN}✅ WARDEN — Tidak ada peringatan risiko{RESET}")
        print()
    
    # HERALD — Status
    print(f"{BOLD}{GREEN}📢 HERALD — Status{RESET}")
    print(f"{DIM}{'─' * 65}{RESET}")
    print(f"  ✅ Bot berjalan | Siklus: #{cycle}")
    print(f"  📊 Data: {len(data)} coin")
    print(f"  🔮 Sinyal: {len(predictions)}")
    print(f"  ⚠️  Warning: {len(warnings)}")
    print(f"  📁 Log: {LOG_FILE}")
    print()
    print(f"{DIM}━━━ Tekan CTRL+C untuk stop ━━━{RESET}")

# ============================================================
# MAIN LOOP
# ============================================================
def bot_loop(interval=60):
    """Loop utama bot"""
    state = load_state()
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🤖 QUAD-CORE BOT — STARTING                                        ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{DIM}Bot akan berjalan setiap {interval} detik.${RESET}
{DIM}Data diambil dari CoinGecko (real-time).${RESET}
{DIM}Tekan CTRL+C untuk stop.${RESET}
""")
    time.sleep(2)
    
    if ZUHRI_ID_OK:
        log_verified("QUADCORE_BOT_START")
    
    try:
        while True:
            state['cycle'] += 1
            cycle = state['cycle']
            
            # CORE 1 — SENTINEL: Fetch data
            data = sentinel_fetch(state)
            
            if not data:
                print(f"{RED}❌ Gagal ambil data. Coba lagi...{RESET}")
                time.sleep(interval)
                continue
            
            # CORE 1 — SENTINEL: Analisis
            alerts = sentinel_analyze(data, state)
            
            # CORE 2 — ORACLE: Prediksi
            predictions = oracle_predict(state)
            
            # CORE 3 — WARDEN: Check risiko
            warnings = warden_check(predictions, state)
            warnings.extend([{"coin": a['coin'], "message": f"Volatilitas {a['change']:.2f}%", "type": a['type']} for a in alerts])
            
            # CORE 4 — HERALD: Report
            herald_report(data, predictions, warnings, cycle)
            
            # Save state
            state['signals'] = predictions[-20:]
            save_state(state)
            
            # Log
            log(f"Cycle #{cycle} complete | Coins: {len(data)} | Signals: {len(predictions)} | Warnings: {len(warnings)}")
            
            # Wait
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}🛑 Bot dihentikan oleh user{RESET}")
        save_state(state)
        log("Bot stopped by user", "WARN")
        if ZUHRI_ID_OK:
            log_verified("QUADCORE_BOT_STOP")
        print(f"{GREEN}✅ State tersimpan{RESET}\n")

# ============================================================
# CLI MODE — Single Run
# ============================================================
def single_run():
    """Jalankan sekali (test)"""
    state = load_state()
    state['cycle'] += 1
    
    print(f"{CYAN}🔍 Fetching data dari CoinGecko...{RESET}\n")
    data = sentinel_fetch(state)
    
    if not data:
        print(f"{RED}❌ Gagal ambil data{RESET}")
        return
    
    alerts = sentinel_analyze(data, state)
    predictions = oracle_predict(state)
    warnings = warden_check(predictions, state)
    warnings.extend([{"coin": a['coin'], "message": f"Volatilitas {a['change']:.2f}%"} for a in alerts])
    
    herald_report(data, predictions, warnings, state['cycle'])
    save_state(state)

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "run":
            # Loop terus
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            bot_loop(interval)
        
        elif cmd == "once":
            # Sekali saja
            single_run()
        
        elif cmd == "status":
            state = load_state()
            print(f"""
{BOLD}{CYAN}📊 QUAD-CORE BOT — STATUS{RESET}

  Started: {state.get('started', 'N/A')[:19]}
  Cycle:   {state.get('cycle', 0)}
  Coins:   {', '.join(state.get('coins', []))}
  Signals: {len(state.get('signals', []))}
""")
        
        elif cmd == "reset":
            if os.path.exists(STATE_FILE):
                os.remove(STATE_FILE)
                print(f"{GREEN}✅ State direset{RESET}")
        
        else:
            print(f"""
{BOLD}{CYAN}QUAD-CORE BOT — COMMANDS{RESET}
  python bot_loop.py run [interval]  → Loop (default 60s)
  python bot_loop.py once            → Sekali saja
  python bot_loop.py status          → Status
  python bot_loop.py reset           → Reset state
""")
    else:
        # Default: single run
        single_run()
