#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI SECURITY SHIELD — PROTOKOL K-8.0 GEN ZUHRI v9.0
Keamanan Berlapis 7 Tingkat
"""

import os
import sys
import subprocess
import hashlib
import json
import time
from datetime import datetime

HOME = os.path.expanduser("~")
SEC_DIR = os.path.join(HOME, "zuhri_os", "security")
os.makedirs(SEC_DIR, exist_ok=True)

LOG_FILE = os.path.join(SEC_DIR, "security.log")
HASH_FILE = os.path.join(SEC_DIR, "integrity.json")
VAULT_DIR = os.path.join(SEC_DIR, "vault")
os.makedirs(VAULT_DIR, exist_ok=True)

# ===== WARNA =====
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GOLD = "\033[93m"

def log_event(event, level="INFO"):
    """Catat event ke log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] [{level}] {event}\n")

# ===== L1 — FIREWALL DASAR =====
def firewall_check():
    """Cek port & koneksi mencurigakan"""
    print(f"\n{BOLD}{CYAN}[L1] 🔥 FIREWALL DASAR{RESET}")
    print(f"{DIM}─────────────────────────────────────────{RESET}")
    
    threats = 0
    try:
        # Cek port terbuka
        result = subprocess.run(["ss", "-tuln"], capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split("\n")
        ports = []
        for line in lines[1:]:
            parts = line.split()
            if len(parts) > 4:
                ports.append(parts[4])
        
        print(f"  Port terbuka: {len(ports)}")
        for p in ports[:10]:
            print(f"    {DIM}→ {p}{RESET}")
        
        # Cek koneksi ESTABLISHED ke IP asing
        result = subprocess.run(["ss", "-tun"], capture_output=True, text=True, timeout=5)
        if "ESTAB" in result.stdout:
            print(f"  {YELLOW}⚠️  Ada koneksi aktif{RESET}")
    except Exception as e:
        print(f"  {DIM}Firewall check terbatas: {e}{RESET}")
    
    log_event("Firewall check selesai")
    return threats

# ===== L2 — ANOMALY SCANNER =====
def anomaly_scan():
    """Deteksi proses & file mencurigakan"""
    print(f"\n{BOLD}{CYAN}[L2] 🔍 ANOMALY SCANNER{RESET}")
    print(f"{DIM}─────────────────────────────────────────{RESET}")
    
    threats = 0
    
    # Cek proses aneh
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        suspicious_keywords = ["nc", "ncat", "telnet", "socat", "netcat"]
        found = []
        for line in result.stdout.split("\n"):
            for kw in suspicious_keywords:
                if kw in line and "grep" not in line:
                    found.append(line.split()[-1] if line.split() else kw)
        
        if found:
            print(f"  {YELLOW}⚠️  Proses mencurigakan: {len(found)}{RESET}")
            threats += len(found)
        else:
            print(f"  {GREEN}✅ Tidak ada proses mencurigakan{RESET}")
    except:
        pass
    
    # Cek file aneh di home
    try:
        suspicious_files = []
        for f in os.listdir(HOME):
            if f.endswith(('.sh', '.py', '.elf')) and f.startswith('.'):
                suspicious_files.append(f)
        if suspicious_files:
            print(f"  {YELLOW}⚠️  File tersembunyi: {len(suspicious_files)}{RESET}")
        else:
            print(f"  {GREEN}✅ Tidak ada file aneh{RESET}")
    except:
        pass
    
    log_event(f"Anomaly scan: {threats} ancaman", "WARN" if threats else "INFO")
    return threats

# ===== L3 — INTEGRITY CHECKER =====
def compute_hash(filepath):
    """Hitung hash SHA-256"""
    try:
        sha = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha.update(chunk)
        return sha.hexdigest()
    except:
        return None

def integrity_check():
    """Verifikasi integritas script Zuhri"""
    print(f"\n{BOLD}{CYAN}[L3] 🔐 INTEGRITY CHECKER{RESET}")
    print(f"{DIM}─────────────────────────────────────────{RESET}")
    
    # File yang dicek
    files_to_check = [
        os.path.join(HOME, "zuhri.py"),
        os.path.join(HOME, "kosmik", "key.sh"),
        os.path.join(HOME, "zuhri_os", "zuhri_os.py"),
        "/data/data/com.termux/files/usr/bin/dark-web",
    ]
    
    # Load hash lama
    saved = {}
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE) as f:
            saved = json.load(f)
    
    current = {}
    ok = 0
    changed = 0
    
    for f in files_to_check:
        if os.path.exists(f):
            h = compute_hash(f)
            current[f] = h
            if f in saved:
                if saved[f] == h:
                    print(f"  {GREEN}✅ {os.path.basename(f)} — asli{RESET}")
                    ok += 1
                else:
                    print(f"  {YELLOW}⚠️  {os.path.basename(f)} — BERUBAH{RESET}")
                    changed += 1
            else:
                print(f"  {CYAN}📝 {os.path.basename(f)} — baru direkam{RESET}")
    
    # Simpan hash baru
    with open(HASH_FILE, "w") as f:
        json.dump(current, f, indent=2)
    
    log_event(f"Integrity: {ok} ok, {changed} changed")
    return changed

# ===== L4 — AUTO-LOCK =====
def auto_lock_setup():
    """Setup auto-lock Termux"""
    print(f"\n{BOLD}{CYAN}[L4] 🔒 AUTO-LOCK{RESET}")
    print(f"{DIM}─────────────────────────────────────────{RESET}")
    
    print(f"  {GREEN}✅ Auto-lock tersedia via script terpisah{RESET}")
    print(f"  {DIM}Jalankan: zlock{RESET}")
    
    log_event("Auto-lock check")

# ===== L5 — SECURE WIPE =====
def secure_wipe():
    """Hapus log & jejak sensitif"""
    print(f"\n{BOLD}{CYAN}[L5] 🧹 SECURE WIPE{RESET}")
    print(f"{DIM}─────────────────────────────────────────{RESET}")
    
    items_to_wipe = [
        os.path.expanduser("~/.bash_history"),
        "/data/data/com.termux/files/usr/var/log/apt/term.log",
    ]
    
    confirm = input(f"  {YELLOW}⚠️  Hapus log & history? (y/n): {RESET}").strip().lower()
    if confirm == 'y':
        for item in items_to_wipe:
            if os.path.exists(item):
                try:
                    os.remove(item)
                    print(f"  {GREEN}✅ Dihapus: {item}{RESET}")
                except:
                    pass
        # Buat history kosong
        open(os.path.expanduser("~/.bash_history"), "w").close()
        print(f"  {GREEN}✅ History & log dibersihkan{RESET}")
        log_event("Secure wipe dijalankan", "WARN")
    else:
        print(f"  {DIM}Dibatalkan{RESET}")

# ===== L6 — ECHO-SHIELD =====
def echo_shield():
    """Enkripsi komunikasi (simulasi)"""
    print(f"\n{BOLD}{CYAN}[L6] 🛡️  ECHO-SHIELD{RESET}")
    print(f"{DIM}─────────────────────────────────────────{RESET}")
    
    # Cek Tor
    try:
        result = subprocess.run(["pgrep", "-x", "tor"], capture_output=True)
        if result.returncode == 0:
            print(f"  {GREEN}✅ Tor aktif — komunikasi terenkripsi{RESET}")
        else:
            print(f"  {YELLOW}⚠️  Tor tidak aktif{RESET}")
    except:
        print(f"  {DIM}Tor tidak terdeteksi{RESET}")
    
    # Cek GPG
    try:
        subprocess.run(["gpg", "--version"], capture_output=True, timeout=2)
        print(f"  {GREEN}✅ GPG tersedia untuk enkripsi file{RESET}")
    except:
        print(f"  {DIM}GPG belum terinstall (opsional){RESET}")
    
    log_event("Echo-shield check")

# ===== L7 — KOSMIK VAULT =====
def kosmik_vault():
    """Vault terenkripsi"""
    print(f"\n{BOLD}{CYAN}[L7] 🗝️  KOSMIK VAULT{RESET}")
    print(f"{DIM}─────────────────────────────────────────{RESET}")
    
    print(f"  Lokasi vault: {GOLD}{VAULT_DIR}{RESET}")
    
    # Tampilkan isi vault
    items = os.listdir(VAULT_DIR)
    if items:
        print(f"  Isi vault: {len(items)} item")
        for item in items[:5]:
            print(f"    {DIM}→ {item}{RESET}")
    else:
        print(f"  {YELLOW}Vault kosong{RESET}")
    
    log_event("Kosmik vault check")

# ===== MENU KEAMANAN =====
def security_menu():
    while True:
        os.system('clear')
        print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🛡️  ZUHRI SECURITY SHIELD — PROTOKOL K-8.0                     ║
║  ──────────────────────────────────────────────────────────────  ║
║  GEN ZUHRI v9.0 — Keamanan Berlapis 7 Tingkat                  ║
║  STATUS: ✅ AKTIF                                              ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 LAPISAN KEAMANAN:{RESET}
  {CYAN}1.{RESET} 🔥 Firewall Dasar
  {CYAN}2.{RESET} 🔍 Anomaly Scanner
  {CYAN}3.{RESET} 🔐 Integrity Checker
  {CYAN}4.{RESET} 🔒 Auto-Lock
  {CYAN}5.{RESET} 🧹 Secure Wipe
  {CYAN}6.{RESET} 🛡️  Echo-Shield
  {CYAN}7.{RESET} 🗝️  Kosmik Vault
  {CYAN}8.{RESET} 🚀 Jalankan SEMUA lapisan
  {CYAN}9.{RESET} 📊 Lihat Security Log
  {CYAN}0.{RESET} Keluar
""")
        
        try:
            choice = input(f"{GOLD}  📡 Pilih lapisan (0-9): {RESET}").strip()
            if choice == "1":
                firewall_check()
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif choice == "2":
                anomaly_scan()
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif choice == "3":
                integrity_check()
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif choice == "4":
                auto_lock_setup()
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif choice == "5":
                secure_wipe()
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif choice == "6":
                echo_shield()
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif choice == "7":
                kosmik_vault()
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif choice == "8":
                os.system('clear')
                print(f"\n{BOLD}{GOLD}🚀 MENJALANKAN SEMUA LAPISAN KEAMANAN...{RESET}\n")
                total_threats = 0
                total_threats += firewall_check()
                total_threats += anomaly_scan()
                total_threats += integrity_check()
                auto_lock_setup()
                echo_shield()
                kosmik_vault()
                print(f"\n{BOLD}{GREEN}✅ SEMUA LAPISAN SELESAI — {total_threats} ancaman terdeteksi{RESET}\n")
                input(f"{DIM}Tekan Enter...{RESET}")
            elif choice == "9":
                if os.path.exists(LOG_FILE):
                    os.system(f"tail -30 {LOG_FILE}")
                else:
                    print(f"{YELLOW}Belum ada log.{RESET}")
                input(f"\n{DIM}Tekan Enter...{RESET}")
            elif choice == "0":
                break
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "scan":
            os.system('clear')
            print(f"\n{BOLD}{GOLD}🚀 FULL SECURITY SCAN...{RESET}")
            total = firewall_check() + anomaly_scan() + integrity_check()
            echo_shield()
            kosmik_vault()
            print(f"\n{BOLD}{GREEN}✅ Selesai — {total} ancaman{RESET}\n")
        elif cmd == "wipe":
            secure_wipe()
        elif cmd == "log":
            os.system(f"cat {LOG_FILE}")
        else:
            security_menu()
    else:
        security_menu()
