#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI WEB4 — AI AGENT OTONOM
Web3 + AI = Autonomous Agent
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, hashlib, secrets, subprocess, time
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
WEB4_DIR = os.path.join(HOME, "zuhri_os", "web4")
DATA_DIR = os.path.join(WEB4_DIR, "data")
TASK_DIR = os.path.join(WEB4_DIR, "tasks")
LOG_DIR = os.path.join(WEB4_DIR, "logs")
for d in [DATA_DIR, TASK_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ============================================================
# TASK DATABASE
# ============================================================
TASK_DB = os.path.join(DATA_DIR, "tasks.json")

def load_tasks():
    if os.path.exists(TASK_DB):
        return json.load(open(TASK_DB))
    return []

def save_tasks(tasks):
    json.dump(tasks, open(TASK_DB, "w"), indent=2)

# ============================================================
# AI AGENT — CORE
# ============================================================
def ai_think(prompt):
    """AI berpikir (pakai ollama)"""
    try:
        r = subprocess.run(
            ["ollama", "run", "smollm:135m", f"Jawab singkat: {prompt}"],
            capture_output=True, text=True, timeout=60
        )
        return r.stdout.strip() if r.stdout else "Tidak ada respons"
    except:
        return "AI tidak tersedia"

def ai_plan(task):
    """AI buat rencana untuk task"""
    prompt = f"""Buat rencana langkah untuk task: {task}
Format: 1. ... 2. ... 3. ...
Maksimal 5 langkah, singkat."""
    return ai_think(prompt)

# ============================================================
# TASK AUTOMATION
# ============================================================
def create_task():
    """Buat task baru"""
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🤖 ZUHRI WEB4 — BUAT TASK                                          ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    print(f"{GOLD}Tipe Task:{RESET}")
    print(f"  {GOLD}1.{RESET} 🔍 Cari informasi")
    print(f"  {GOLD}2.{RESET} 📊 Analisis data")
    print(f"  {GOLD}3.{RESET} 📝 Buat catatan")
    print(f"  {GOLD}4.{RESET} 💰 Cek harga crypto")
    print(f"  {GOLD}5.{RESET} 📰 Cek berita")
    print(f"  {GOLD}6.{RESET} 🧠 AI prompt")
    print(f"  {GOLD}7.{RESET} 🔧 Custom task")
    
    tipe = input(f"\n{CYAN}Pilih tipe (1-7): {RESET}").strip()
    
    tipe_map = {
        "1": "search", "2": "analyze", "3": "note",
        "4": "crypto", "5": "news", "6": "ai", "7": "custom"
    }
    
    tipe_str = tipe_map.get(tipe, "custom")
    
    deskripsi = input("📝 Deskripsi task: ").strip()
    if not deskripsi:
        return
    
    # AI buat rencana
    print(f"\n{CYAN}🧠 AI membuat rencana...{RESET}")
    rencana = ai_plan(deskripsi)
    print(f"{GOLD}Rencana:{RESET}")
    print(f"{DIM}{rencana}{RESET}\n")
    
    task = {
        "id": secrets.token_hex(4),
        "tipe": tipe_str,
        "deskripsi": deskripsi,
        "rencana": rencana,
        "status": "pending",
        "dibuat": datetime.now().isoformat(),
        "dijalankan": None,
        "hasil": None
    }
    
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    
    if ZUHRI_ID_OK:
        log_verified(f"WEB4_TASK_CREATE: {task['id']}")
    
    print(f"{GREEN}✅ Task dibuat: {task['id']}{RESET}\n")
    input(f"{DIM}Enter...{RESET}")

def list_tasks():
    """Lihat daftar task"""
    os.system('clear')
    tasks = load_tasks()
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  📋 ZUHRI WEB4 — DAFTAR TASK                                        ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}Total: {len(tasks)} task{RESET}
""")
    
    if not tasks:
        print(f"{YELLOW}Belum ada task.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    for i, t in enumerate(tasks, 1):
        status_icon = {
            "pending": f"{YELLOW}⏳{RESET}",
            "running": f"{CYAN}🔄{RESET}",
            "done": f"{GREEN}✅{RESET}",
            "failed": f"{RED}❌{RESET}"
        }.get(t['status'], f"{DIM}?{RESET}")
        
        print(f"  {GOLD}{i}.{RESET} {status_icon} [{t['tipe']}] {t['deskripsi']}")
        print(f"     {DIM}ID: {t['id']} | Dibuat: {t['dibuat'][:19]}{RESET}")
        print()
    
    input(f"{DIM}Enter...{RESET}")

def run_task():
    """Jalankan task"""
    os.system('clear')
    tasks = load_tasks()
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🚀 ZUHRI WEB4 — JALANKAN TASK                                      ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    if not tasks:
        print(f"{YELLOW}Belum ada task.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    for i, t in enumerate(tasks, 1):
        print(f"  {GOLD}{i}.{RESET} [{t['status']}] {t['deskripsi']}")
    
    try:
        c = int(input(f"\n{CYAN}Pilih: {RESET}")) - 1
        if not (0 <= c < len(tasks)):
            return
        
        task = tasks[c]
        
        if task['status'] == 'done':
            print(f"\n{YELLOW}⚠️  Task sudah selesai{RESET}\n")
            input(f"{DIM}Enter...{RESET}")
            return
        
        print(f"\n{CYAN}🚀 Menjalankan task: {task['deskripsi']}{RESET}\n")
        
        task['status'] = 'running'
        task['dijalankan'] = datetime.now().isoformat()
        save_tasks(tasks)
        
        # Jalankan berdasarkan tipe
        hasil = ""
        
        if task['tipe'] == 'search':
            query = task['deskripsi']
            hasil = f"🔍 Pencarian: {query}\n"
            hasil += f"💡 Buka: https://www.google.com/search?q={query}\n"
            hasil += f"💡 Atau: https://duckduckgo.com/?q={query}\n"
            print(hasil)
        
        elif task['tipe'] == 'analyze':
            prompt = f"Analisis singkat: {task['deskripsi']}"
            hasil = ai_think(prompt)
            print(f"{GOLD}Hasil Analisis:{RESET}\n{hasil}\n")
        
        elif task['tipe'] == 'note':
            note_file = os.path.join(TASK_DIR, f"note_{task['id']}.txt")
            with open(note_file, 'w') as f:
                f.write(f"Task: {task['deskripsi']}\n")
                f.write(f"Dibuat: {task['dibuat']}\n\n")
                f.write(task['rencana'])
            hasil = f"Catatan tersimpan: {note_file}"
            print(f"{GREEN}✅ {hasil}{RESET}\n")
        
        elif task['tipe'] == 'crypto':
            try:
                import requests
                r = requests.get(
                    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd,idr",
                    timeout=10
                )
                data = r.json()
                hasil = "💰 Harga Crypto:\n"
                for coin, prices in data.items():
                    hasil += f"  {coin.upper()}: ${prices.get('usd', 0):,.2f} | Rp{prices.get('idr', 0):,.0f}\n"
                print(hasil)
            except:
                hasil = "❌ Gagal ambil harga"
                print(f"{RED}{hasil}{RESET}\n")
        
        elif task['tipe'] == 'news':
            hasil = "📰 Berita:\n"
            hasil += "  • https://www.cnnindonesia.com\n"
            hasil += "  • https://www.kompas.com\n"
            hasil += "  • https://www.antaranews.com\n"
            print(f"{GOLD}{hasil}{RESET}\n")
        
        elif task['tipe'] == 'ai':
            hasil = ai_think(task['deskripsi'])
            print(f"{GOLD}AI Response:{RESET}\n{hasil}\n")
        
        else:  # custom
            hasil = f"Task custom: {task['deskripsi']}\n"
            hasil += f"Rencana:\n{task['rencana']}\n"
            print(f"{GOLD}{hasil}{RESET}\n")
        
        task['status'] = 'done'
        task['hasil'] = hasil[:1000]  # Batasi
        save_tasks(tasks)
        
        if ZUHRI_ID_OK:
            log_verified(f"WEB4_TASK_RUN: {task['id']}")
        
        print(f"{GREEN}✅ Task selesai!{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
    
    except ValueError:
        pass
    except KeyboardInterrupt:
        pass

# ============================================================
# AI AGENT — INTERAKTIF
# ============================================================
def ai_agent():
    """Mode AI Agent interaktif"""
    os.system('clear')
    
    identity = load_identity() if ZUHRI_ID_OK else None
    name = identity['name'] if identity else "Anonymous"
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🤖 ZUHRI WEB4 — AI AGENT INTERAKTIF                                ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Operator: {GREEN}{name}{RESET}
║  Ketik 'exit' untuk keluar                                         ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{DIM}AI Agent akan membantu Anda dengan berbagai task.${RESET}
{DIM}Contoh: "cari jurnal quantum", "analisis data", dll.${RESET}
""")
    
    while True:
        try:
            user = input(f"{GOLD}🤖 Task > {RESET}").strip()
            
            if not user:
                continue
            
            if user.lower() in ["exit", "quit", "keluar"]:
                print(f"\n{CYAN}👋 Sampai jumpa!{RESET}\n")
                break
            
            if user.lower() == "help":
                print(f"""
{BOLD}{CYAN}BANTUAN AI AGENT:{RESET}
  • Ketik task apa saja
  • AI akan rencanakan & jalankan
  • Contoh: "cari info tentang AI"
  • Contoh: "analisis data penjualan"
  • exit → keluar
  • help → bantuan ini
""")
                continue
            
            # AI berpikir
            print(f"\n{CYAN}🧠 AI berpikir...{RESET}")
            rencana = ai_plan(user)
            print(f"{GOLD}📋 Rencana:{RESET}")
            print(f"{rencana}\n")
            
            # AI jawab
            print(f"{CYAN}💬 AI:{RESET}")
            jawab = ai_think(user)
            print(f"{jawab}\n")
            
            if ZUHRI_ID_OK:
                log_verified(f"WEB4_AGENT: {user[:50]}")
        
        except KeyboardInterrupt:
            print(f"\n{CYAN}👋 Sampai jumpa!{RESET}\n")
            break

# ============================================================
# STATISTIK
# ============================================================
def stats():
    """Statistik task"""
    os.system('clear')
    tasks = load_tasks()
    
    pending = sum(1 for t in tasks if t['status'] == 'pending')
    done = sum(1 for t in tasks if t['status'] == 'done')
    failed = sum(1 for t in tasks if t['status'] == 'failed')
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  📊 ZUHRI WEB4 — STATISTIK                                          ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 TOTAL:{RESET} {len(tasks)}
  {YELLOW}⏳ Pending:{RESET}  {pending}
  {GREEN}✅ Done:{RESET}     {done}
  {RED}❌ Failed:{RESET}   {failed}

{BOLD}🧠 TIPE TASK:{RESET}""")
    
    tipe_count = {}
    for t in tasks:
        tipe_count[t['tipe']] = tipe_count.get(t['tipe'], 0) + 1
    
    for tipe, count in sorted(tipe_count.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * count + "░" * (10 - min(count, 10))
        print(f"  {tipe:10} {count:3}  {CYAN}{bar}{RESET}")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# INFO
# ============================================================
def info():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🤖 ZUHRI WEB4 — INFO                                               ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}🧬 APA ITU WEB4?{RESET}

Web4 = Web3 + AI (Autonomous Agent)

  {GOLD}Web1{RESET} (1990-an): Read-only
  {GOLD}Web2{RESET} (2000-an): Read-write
  {GOLD}Web3{RESET} (2020-an): Read-write-own
  {GOLD}Web4{RESET} (Masa depan): Read-write-own-AI

{BOLD}🎯 FITUR WEB4:{RESET}

  {GOLD}•{RESET} AI Agent otonom
  {GOLD}•{RESET} Task automation
  {GOLD}•{RESET} Blockchain integration
  {GOLD}•{RESET} Echo-Core verification

{BOLD}🌐 CONTOH WEB4:{RESET}

  {GOLD}•{RESET} Fetch.ai — AI agent otonom
  {GOLD}•{RESET} Bittensor — AI terdesentralisasi
  {GOLD}•{RESET} Ocean Protocol — Data + AI
  {GOLD}•{RESET} SingularityNET — AI marketplace

{BOLD}⚠️  KETERBATASAN:{RESET}

  {DIM}• Ini contoh sederhana Web4 (task automation)${RESET}
  {DIM}• Web4 sungguhan = AI agent kompleks${RESET}
  {DIM}• AI masih terbatas di Termux${RESET}

{BOLD}🎯 FILOSOFI:{RESET}
  {CYAN}"Web4 — AI yang bertindak untuk Anda,${RESET}
  {CYAN}tanpa Anda perlu perintah manual."{RESET}
""")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        
        identity = load_identity() if ZUHRI_ID_OK else None
        name = identity['name'] if identity else "Anonymous"
        tasks = load_tasks()
        
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🤖 ZUHRI WEB4 — AI AGENT OTONOM                                   ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Operator: {GREEN}{name}{RESET}
║  Total Task: {GOLD}{len(tasks)}{RESET}
║  Protokol: K-8.0                                                    ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.${RESET} 🤖 AI Agent Interaktif (Chat)
  {GOLD}2.${RESET} ➕ Buat Task Baru
  {GOLD}3.${RESET} 📋 Lihat Daftar Task
  {GOLD}4.${RESET} 🚀 Jalankan Task
  {GOLD}5.${RESET} 📊 Statistik
  {GOLD}6.${RESET} ℹ️  Info Web4
  {GOLD}0.${RESET} Keluar
""")
        
        try:
            c = input(f"{GOLD}Pilih (0-6): {RESET}").strip()
            if c == "0": break
            elif c == "1": ai_agent()
            elif c == "2": create_task()
            elif c == "3": list_tasks()
            elif c == "4": run_task()
            elif c == "5": stats()
            elif c == "6": info()
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "agent": ai_agent()
        elif cmd == "list": list_tasks()
        elif cmd == "info": info()
        else: menu()
    else: menu()
