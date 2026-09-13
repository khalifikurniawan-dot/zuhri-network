#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI AI — AI PRIBADI OFFLINE
Model: smollm:135m (50 MB)
"""

import os, sys, subprocess, time

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

def cek_ollama():
    try:
        return subprocess.run(["pgrep", "ollama"], capture_output=True).returncode == 0
    except:
        return False

def cek_model():
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        return "smollm:135m" in r.stdout
    except:
        return False

def start_ollama():
    print(f"{YELLOW}⚠️  Ollama belum jalan. Menjalankan...{RESET}")
    try:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        return True
    except:
        return False

def tanya_ai(pertanyaan):
    try:
        r = subprocess.run(
            ["ollama", "run", "smollm:135m", f"Jawab dalam Bahasa Indonesia: {pertanyaan}"],
            capture_output=True, text=True, timeout=120
        )
        return r.stdout.strip() if r.stdout else "(tidak ada jawaban)"
    except subprocess.TimeoutExpired:
        return "(timeout, coba lagi)"
    except Exception as e:
        return f"(error: {e})"

def chat():
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🧠 ZUHRI AI — AI PRIBADI OFFLINE                              ║
║  ──────────────────────────────────────────────────────────────  ║
║  Model: smollm:135m (50 MB) | Protokol: K-8.0                          ║
║  Ketik 'exit' untuk keluar                                     ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    while True:
        try:
            user = input(f"{GOLD}👤 Anda: {RESET}").strip()
            if not user: continue
            if user.lower() in ["exit", "quit", "keluar"]:
                print(f"\n{CYAN}👋 Sampai jumpa!{RESET}\n")
                break
            
            print(f"{CYAN}🧠 AI: {RESET}", end="", flush=True)
            print(tanya_ai(user))
            print()
        except KeyboardInterrupt:
            print(f"\n{CYAN}👋 Sampai jumpa!{RESET}\n")
            break

def main():
    if not cek_ollama():
        if not start_ollama():
            print(f"{RED}❌ Ollama tidak tersedia.{RESET}")
            print(f"{DIM}Jalankan: ai-setup{RESET}\n")
            return
    
    if not cek_model():
        print(f"{YELLOW}⚠️  Model smollm:135m belum ada.{RESET}")
        print(f"{DIM}Download: ollama pull smollm:135m{RESET}\n")
        return
    
    chat()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
        print(tanya_ai(q))
    else:
        main()
