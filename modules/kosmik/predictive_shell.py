#!/data/data/com.termux/files/usr/bin/python
"""
PREDICTIVE-SHELL — ZUHRI NETWORK
Terminal yang Tahu Sebelum Anda Mengetik
"""

import os
import sys
import json
import subprocess
from collections import Counter
from datetime import datetime

HISTORY_FILE = os.path.expanduser("~/.bash_history")
PREDICT_FILE = os.path.expanduser("~/.predictive_cache.json")
MAX_HISTORY = 1000

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RED = "\033[91m"
DIM = "\033[2m"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    commands = []
    for line in lines:
        cmd = line.strip()
        if cmd and not cmd.startswith('#') and len(cmd) > 1:
            commands.append(cmd)
    return commands[-MAX_HISTORY:]

def analyze_patterns(commands):
    if len(commands) < 3:
        return {}
    pairs = [(commands[i], commands[i+1]) for i in range(len(commands)-1)]
    pair_freq = Counter(pairs)
    single_freq = Counter(commands)
    arg_patterns = {}
    for cmd in commands:
        parts = cmd.split()
        if len(parts) >= 2:
            base = parts[0]
            args = ' '.join(parts[1:])
            if base not in arg_patterns:
                arg_patterns[base] = []
            arg_patterns[base].append(args)
    top_args = {}
    for base, args_list in arg_patterns.items():
        if len(args_list) > 1:
            top_args[base] = Counter(args_list).most_common(3)
    return {'pairs': pair_freq, 'singles': single_freq, 'args': top_args}

def predict_next(last_command, patterns):
    if not patterns or not last_command:
        return []
    suggestions = []
    for (cmd1, cmd2), freq in patterns.get('pairs', {}).items():
        if cmd1 == last_command:
            suggestions.append((cmd2, freq))
    suggestions.sort(key=lambda x: x[1], reverse=True)
    if last_command in patterns.get('args', {}):
        top_args = patterns['args'][last_command]
        for arg, freq in top_args[:3]:
            full_cmd = f"{last_command} {arg}"
            suggestions.append((full_cmd, freq + 0.5))
    return [s[0] for s in suggestions[:5]]

def display_suggestions(suggestions):
    if not suggestions:
        return
    print(f"\n{DIM}─────────────────────────────────────────────────{RESET}")
    print(f"{BOLD}{CYAN}🔮 PREDIKSI:{RESET}")
    for i, cmd in enumerate(suggestions[:5], 1):
        print(f"  {GREEN}{i}. {cmd}{RESET}")
    print(f"{DIM}─────────────────────────────────────────────────{RESET}\n")

def show_stats(patterns):
    if not patterns or not patterns.get('singles'):
        print(f"{YELLOW}Belum ada data.{RESET}")
        return
    print(f"\n{BOLD}{CYAN}📊 STATISTIK PENGGUNAAN{RESET}")
    print(f"{'─' * 40}")
    for cmd, count in patterns['singles'].most_common(5):
        print(f"  {count:4}x  {cmd}")
    print(f"\n{BOLD}Total perintah unik:{RESET} {len(patterns['singles'])}")
    print(f"{BOLD}Total terekam:{RESET} {sum(patterns['singles'].values())}\n")

def predictive_shell():
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🔮 PREDICTIVE-SHELL — ZUHRI NETWORK                            ║
║  ──────────────────────────────────────────────────────────────  ║
║  STATUS : ✅ AKTIF    PROTOKOL : K-8.0                        ║
║  GEN    : ZUH-8-9-0-K-8.0                                      ║
║  TIP    : Ketik perintah, dapatkan prediksi otomatis          ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    print(f"{DIM}📂 Memuat riwayat perintah...{RESET}")
    commands = load_history()
    print(f"{DIM}✅ {len(commands)} perintah dimuat.{RESET}")
    patterns = analyze_patterns(commands)
    print(f"{DIM}✅ Pola dianalisis.{RESET}\n")
    
    while True:
        try:
            user_input = input(f"{BOLD}{GREEN}➜ {RESET}")
            if not user_input:
                continue
            if user_input == "exit":
                print(f"{CYAN}👋 Sampai jumpa!{RESET}")
                break
            if user_input == "stats":
                show_stats(patterns)
                continue
            if user_input == "history":
                print(f"\n{BOLD}{CYAN}📜 RIWAYAT:{RESET}")
                for cmd in commands[-10:]:
                    print(f"  {cmd}")
                print()
                continue
            if user_input == "clear":
                os.system('clear')
                continue
            if user_input == "help":
                print(f"""
{BOLD}{CYAN}PREDICTIVE-SHELL — BANTUAN{RESET}
{'─' * 40}
  {BOLD}exit{RESET}     → Keluar
  {BOLD}stats{RESET}    → Statistik penggunaan
  {BOLD}history{RESET}  → Riwayat perintah
  {BOLD}clear{RESET}    → Bersihkan layar
  {BOLD}help{RESET}     → Bantuan
{'─' * 40}
""")
                continue
            
            suggestions = predict_next(user_input, patterns)
            if suggestions:
                display_suggestions(suggestions)
            
            try:
                print(f"{DIM}→ Menjalankan: {user_input}{RESET}")
                result = subprocess.run(user_input, shell=True, capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(f"{YELLOW}{result.stderr}{RESET}")
            except Exception as e:
                print(f"{RED}❌ Error: {e}{RESET}")
            
            commands.append(user_input)
            if len(commands) % 50 == 0:
                patterns = analyze_patterns(commands)
                
        except KeyboardInterrupt:
            print(f"\n{CYAN}👋 Sampai jumpa!{RESET}")
            break
        except Exception as e:
            print(f"{RED}❌ Error: {e}{RESET}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "stats":
            commands = load_history()
            patterns = analyze_patterns(commands)
            show_stats(patterns)
        elif sys.argv[1] == "help":
            print(f"{CYAN}🔮 Predictive-Shell — Terminal Prediktif{RESET}")
            print(f"  Jalankan: {BOLD}predictive{RESET}")
            print(f"  Statistik: {BOLD}predictive stats{RESET}")
        else:
            predictive_shell()
    else:
        predictive_shell()
