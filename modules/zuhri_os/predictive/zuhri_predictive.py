#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI PREDICTIVE — TERMINAL PREDIKTIF
Belajar dari kebiasaan, prediksi perintah selanjutnya
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, subprocess, readline
from datetime import datetime
from collections import Counter

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
PRED_DIR = os.path.join(HOME, "zuhri_os", "predictive")
os.makedirs(PRED_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(HOME, ".bash_history")
CACHE_FILE = os.path.join(PRED_DIR, "cache.json")
SHORTCUT_FILE = os.path.join(PRED_DIR, "shortcuts.json")
STATS_FILE = os.path.join(PRED_DIR, "stats.json")

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# LOAD HISTORY
# ============================================================
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r', errors='ignore') as f:
        lines = f.readlines()
    cmds = []
    for l in lines:
        c = l.strip()
        if c and not c.startswith('#') and len(c) > 1:
            cmds.append(c)
    return cmds[-2000:]

# ============================================================
# ANALISIS POLA
# ============================================================
def analyze(commands):
    if len(commands) < 3: return {}
    
    pairs = [(commands[i], commands[i+1]) for i in range(len(commands)-1)]
    pair_freq = Counter(pairs)
    single_freq = Counter(commands)
    
    # Argumen perintah
    args_map = {}
    for cmd in commands:
        parts = cmd.split()
        if len(parts) >= 2:
            base = parts[0]
            args = ' '.join(parts[1:])
            args_map.setdefault(base, []).append(args)
    
    top_args = {}
    for base, args_list in args_map.items():
        if len(args_list) > 1:
            top_args[base] = Counter(args_list).most_common(5)
    
    return {
        "pairs": pair_freq,
        "singles": single_freq,
        "args": top_args,
        "total": len(commands)
    }

# ============================================================
# PREDIKSI
# ============================================================
def predict_next(last_cmd, patterns):
    if not patterns or not last_cmd: return []
    
    suggestions = []
    
    # Berdasarkan bigram
    for (c1, c2), freq in patterns.get('pairs', {}).items():
        if c1 == last_cmd:
            suggestions.append((c2, freq))
    
    # Berdasarkan perintah sama + argumen
    if last_cmd in patterns.get('args', {}):
        for arg, freq in patterns['args'][last_cmd][:3]:
            full = f"{last_cmd} {arg}"
            suggestions.append((full, freq + 0.5))
    
    # Perintah sering
    for cmd, freq in patterns.get('singles', {}).most_common(5):
        if cmd != last_cmd:
            suggestions.append((cmd, freq * 0.3))
    
    # Sort & dedupe
    seen = set()
    result = []
    suggestions.sort(key=lambda x: x[1], reverse=True)
    for cmd, _ in suggestions:
        if cmd not in seen:
            seen.add(cmd)
            result.append(cmd)
        if len(result) >= 8:
            break
    
    return result

# ============================================================
# AI PREDICT
# ============================================================
def ai_predict(context):
    """Prediksi pakai AI phi"""
    try:
        prompt = f"""Kamu asisten terminal Linux/Android. Berdasarkan konteks perintah terakhir, sarankan 3 perintah selanjutnya (hanya nama perintah, satu per baris, tanpa penjelasan):

Konteks: {context}

Perintah selanjutnya:"""
        r = subprocess.run(["ollama","run","phi",prompt], capture_output=True, text=True, timeout=30)
        if r.stdout:
            lines = [l.strip() for l in r.stdout.split('\n') if l.strip()]
            return lines[:3]
    except: pass
    return []

# ============================================================
# STATISTIK
# ============================================================
def show_stats(patterns):
    if not patterns:
        print(f"{YELLOW}Belum ada data.{RESET}\n")
        return
    
    singles = patterns.get('singles', {})
    print(f"\n{BOLD}{CYAN}📊 STATISTIK{RESET}")
    print(f"{'─'*50}")
    print(f"  Total perintah : {patterns.get('total', 0)}")
    print(f"  Perintah unik  : {len(singles)}\n")
    
    print(f"{BOLD}🏆 Top 10 Perintah:{RESET}")
    for cmd, freq in singles.most_common(10):
        bar_len = int(freq / max(singles.values()) * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {CYAN}{bar}{RESET} {freq:3}x  {cmd[:40]}")
    print()

# ============================================================
# SHORTCUT
# ============================================================
def load_shortcuts():
    if os.path.exists(SHORTCUT_FILE):
        return json.load(open(SHORTCUT_FILE))
    return {
        "zz": "zuhri",
        "ez": "ekosistem_zuhri",
        "key": "key",
        "mesh": "mesh",
        "ai": "ai",
    }

def save_shortcuts(s):
    json.dump(s, open(SHORTCUT_FILE, "w"), indent=2)

def show_shortcuts():
    s = load_shortcuts()
    print(f"\n{BOLD}{CYAN}⚡ SHORTCUT{RESET}\n")
    for k, v in s.items():
        print(f"  {GOLD}{k:10}{RESET} → {v}")
    print()

# ============================================================
# CARI HISTORY
# ============================================================
def search_history(query):
    cmds = load_history()
    results = [c for c in cmds if query.lower() in c.lower()]
    
    print(f"\n{BOLD}{CYAN}🔍 Hasil: '{query}'{RESET}\n")
    if results:
        for c in results[-20:]:
            print(f"  {c}")
    else:
        print(f"  {YELLOW}Tidak ditemukan.{RESET}")
    print()

# ============================================================
# MAIN SHELL
# ============================================================
def predictive_shell():
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🔮 ZUHRI PREDICTIVE — TERMINAL PREDIKTIF                      ║
║  ──────────────────────────────────────────────────────────────  ║
║  Belajar dari kebiasaan • Prediksi perintah                    ║
║  Ketik 'help' untuk bantuan                                    ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{DIM}📂 Memuat riwayat...{RESET}""")
    
    commands = load_history()
    patterns = analyze(commands)
    print(f"{GREEN}✅ {len(commands)} perintah dimuat{RESET}\n")
    
    last_cmd = commands[-1] if commands else ""
    use_ai = False
    
    while True:
        try:
            # Prompt
            prompt = f"{GOLD}🔮 > {RESET}"
            cmd = input(prompt).strip()
            
            if not cmd:
                continue
            
            # Built-in commands
            if cmd == "exit":
                print(f"{CYAN}👋 Sampai jumpa!{RESET}\n")
                break
            elif cmd == "help":
                print(f"""
{BOLD}{CYAN}🔮 ZUHRI PREDICTIVE — BANTUAN{RESET}
{'─'*50}
  {GOLD}history{RESET}     → Lihat riwayat terakhir
  {GOLD}stats{RESET}       → Statistik perintah
  {GOLD}shortcut{RESET}    → Lihat shortcut
  {GOLD}search X{RESET}    → Cari di riwayat
  {GOLD}ai on/off{RESET}   → Aktifkan AI predictor
  {GOLD}clear{RESET}       → Bersihkan layar
  {GOLD}help{RESET}        → Bantuan
  {GOLD}exit{RESET}        → Keluar
{'─'*50}
""")
                continue
            elif cmd == "clear":
                os.system('clear'); continue
            elif cmd == "history":
                print(f"\n{BOLD}{CYAN}📜 Riwayat terakhir:{RESET}")
                for c in commands[-15:]:
                    print(f"  {c}")
                print()
                continue
            elif cmd == "stats":
                show_stats(patterns); continue
            elif cmd == "shortcut":
                show_shortcuts(); continue
            elif cmd.startswith("search "):
                search_history(cmd[7:]); continue
            elif cmd == "ai on":
                use_ai = True
                print(f"{GREEN}✅ AI predictor aktif{RESET}\n"); continue
            elif cmd == "ai off":
                use_ai = False
                print(f"{YELLOW}⚠️  AI predictor nonaktif{RESET}\n"); continue
            
            # Prediksi
            suggestions = predict_next(last_cmd, patterns) if last_cmd else []
            
            if suggestions:
                print(f"\n{DIM}🔮 Prediksi:{RESET}")
                for i, s in enumerate(suggestions[:5], 1):
                    print(f"  {CYAN}{i}.{RESET} {s}")
                print()
            
            # AI predict (opsional)
            if use_ai and last_cmd:
                ai_sug = ai_predict(last_cmd)
                if ai_sug:
                    print(f"{DIM}🧠 AI saran:{RESET}")
                    for s in ai_sug:
                        print(f"  {MAGENTA}→{RESET} {s}")
                    print()
            
            # Jika input angka, pilih prediksi
            if cmd.isdigit() and suggestions:
                idx = int(cmd) - 1
                if 0 <= idx < len(suggestions):
                    cmd = suggestions[idx]
                    print(f"{GREEN}→ Menjalankan: {cmd}{RESET}\n")
            
            # Jalankan perintah
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(f"{YELLOW}{result.stderr}{RESET}")
            except subprocess.TimeoutExpired:
                print(f"{RED}⏱️  Timeout{RESET}")
            except Exception as e:
                print(f"{RED}❌ {e}{RESET}")
            
            # Update
            commands.append(cmd)
            last_cmd = cmd
            if len(commands) % 20 == 0:
                patterns = analyze(commands)
        
        except KeyboardInterrupt:
            print(f"\n{CYAN}👋 Sampai jumpa!{RESET}\n")
            break
        except EOFError:
            break

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🔮 ZUHRI PREDICTIVE — TERMINAL PREDIKTIF                      ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🚀 Jalankan Shell Prediktif
  {GOLD}2.{RESET}  📊 Statistik Perintah
  {GOLD}3.{RESET}  🔍 Cari di Riwayat
  {GOLD}4.{RESET}  ⚡ Lihat Shortcut
  {GOLD}5.{RESET}  ✏️  Tambah Shortcut
  {GOLD}6.{RESET}  🧠 Test AI Predictor
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-6): {RESET}").strip()
            if c == "0": break
            elif c == "1":
                os.system('clear')
                predictive_shell()
            elif c == "2":
                patterns = analyze(load_history())
                os.system('clear')
                show_stats(patterns)
                input(f"{DIM}Enter...{RESET}")
            elif c == "3":
                q = input(f"\n{CYAN}🔍 Cari: {RESET}").strip()
                os.system('clear')
                search_history(q)
                input(f"{DIM}Enter...{RESET}")
            elif c == "4":
                os.system('clear')
                show_shortcuts()
                input(f"{DIM}Enter...{RESET}")
            elif c == "5":
                s = load_shortcuts()
                k = input(f"\n{CYAN}Shortcut (misal zz): {RESET}").strip()
                v = input(f"{CYAN}Perintah: {RESET}").strip()
                if k and v:
                    s[k] = v
                    save_shortcuts(s)
                    print(f"{GREEN}✅ Ditambahkan{RESET}\n")
                input(f"{DIM}Enter...{RESET}")
            elif c == "6":
                ctx = input(f"\n{CYAN}Konteks perintah: {RESET}").strip()
                print(f"\n{YELLOW}⏳ AI memprediksi...{RESET}\n")
                results = ai_predict(ctx)
                if results:
                    for r in results:
                        print(f"  {MAGENTA}→{RESET} {r}")
                else:
                    print(f"{YELLOW}⚠️  Tidak ada prediksi (Ollama tidak aktif?){RESET}")
                print()
                input(f"{DIM}Enter...{RESET}")
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "stats":
            show_stats(analyze(load_history()))
        elif cmd == "search":
            search_history(" ".join(sys.argv[2:]))
        elif cmd == "shortcut":
            show_shortcuts()
        else: menu()
    else: menu()
