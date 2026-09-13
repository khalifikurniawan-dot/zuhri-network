#!/usr/bin/env python3
"""
ZUHRI MONITORING SUITE — PUSAT MONITORING & ENERGI
Frekuensi • Predictive • Energi
"""

import os, sys, json, subprocess, time, hashlib, random
from datetime import datetime

HOME = os.path.expanduser("~")
MS_DIR = os.path.join(HOME, "zuhri_os", "monitoringsuite")
DATA_DIR = os.path.join(MS_DIR, "data")
LOG_DIR = os.path.join(MS_DIR, "logs")
for d in [DATA_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

def clear(): os.system('clear')
def pause():
    input(f"\n{DIM}━━━ Tekan Enter untuk lanjut ━━━{RESET}\n")

# ============================================================
# 1. ZUHRI FREKUENSI
# ============================================================
def zuhri_frekuensi():
    clear()
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════════╗
║  📡 ZUHRI FREKUENSI — RESONANSI & ANOMALI                               ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 MENU:{RESET}
  {GOLD}1.{RESET} 🌊 Resonansi Gelombang (Sonar/LIDAR)
  {GOLD}2.{RESET} 🧲 Medan Magnetik & Gravitasi
  {GOLD}3.{RESET} ⚛️  Anomali Quantum (Simulasi)
  {GOLD}4.{RESET} 📊 Visualisasi Hasil Anomali
  {GOLD}5.{RESET} 🔬 Cek Sensor HP
  {GOLD}6.{RESET} 🚨 Integrasi ke Zuhri Peringatan
  {GOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "0": return
        subprocess.run(["python", os.path.expanduser("~/zuhri_os/frekuensi/zuhri_frekuensi.py")])
        pause()
    except: pause()

# ============================================================
# 2. ZUHRI PREDICTIVE
# ============================================================
def zuhri_predictive():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  🔮 ZUHRI PREDICTIVE — TERMINAL PREDIKTIF                               ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 MENU:{RESET}
  {GOLD}1.{RESET} 🚀 Jalankan Shell Prediktif
  {GOLD}2.{RESET} 📊 Statistik Perintah
  {GOLD}3.{RESET} 🔍 Cari di Riwayat
  {GOLD}4.{RESET} ⚡ Lihat Shortcut
  {GOLD}5.{RESET} ✏️  Tambah Shortcut
  {GOLD}6.{RESET} 🧠 Test AI Predictor
  {GOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "0": return
        subprocess.run(["python", os.path.expanduser("~/zuhri_os/predictive/zuhri_predictive.py")])
        pause()
    except: pause()

# ============================================================
# 3. ZUHRI ENERGI
# ============================================================
def zuhri_energi():
    clear()
    print(f"""
{BOLD}{GREEN}╔══════════════════════════════════════════════════════════════════════════╗
║  ⚡ ZUHRI ENERGI — KEMANDIRIAN ENERGI DIGITAL                           ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 MENU:{RESET}
  {GOLD}1.{RESET} 🔋 Status Baterai
  {GOLD}2.{RESET} 📊 Statistik (7 hari)
  {GOLD}3.{RESET} ⚡ Optimasi Daya
  {GOLD}4.{RESET} 🔮 Prediksi Baterai
  {GOLD}5.{RESET} 📈 Monitor Real-time
  {GOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "0": return
        subprocess.run(["python", os.path.expanduser("~/zuhri_os/energi/zuhri_energi.py")])
        pause()
    except: pause()

# ============================================================
# STATUS SEMUA
# ============================================================
def status_semua():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  📊 STATUS SEMUA LAYER MONITORING                                       ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    # Cek file
    freq_ok = os.path.exists(os.path.expanduser("~/zuhri_os/frekuensi/zuhri_frekuensi.py"))
    pred_ok = os.path.exists(os.path.expanduser("~/zuhri_os/predictive/zuhri_predictive.py"))
    energy_ok = os.path.exists(os.path.expanduser("~/zuhri_os/energi/zuhri_energi.py"))
    
    print(f"  📡 Zuhri Frekuensi   : {GREEN + '✅' + RESET if freq_ok else RED + '❌' + RESET}")
    print(f"  🔮 Zuhri Predictive  : {GREEN + '✅' + RESET if pred_ok else RED + '❌' + RESET}")
    print(f"  ⚡ Zuhri Energi      : {GREEN + '✅' + RESET if energy_ok else RED + '❌' + RESET}")
    
    # Cek baterai
    print(f"\n  {GOLD}🔋 Baterai:{RESET} ", end="")
    try:
        r = subprocess.run(["termux-battery-status"], capture_output=True, text=True, timeout=5)
        if r.stdout:
            data = json.loads(r.stdout)
            pct = data.get('percentage', '?')
            status = data.get('status', '?')
            print(f"{pct}% ({status})")
        else:
            print("Tidak tersedia")
    except:
        print("Tidak tersedia")
    
    # Cek Tor
    tor_ok = subprocess.run(["pgrep", "-x", "tor"], capture_output=True).returncode == 0
    print(f"  {GOLD}🌐 Tor:{RESET} {GREEN + '✅ AKTIF' + RESET if tor_ok else RED + '❌ MATI' + RESET}")
    
    print()
    pause()

def info():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  ℹ️  INFO ZUHRI MONITORING SUITE                                         ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}🎯 3 KELOMPOK MONITORING:{RESET}

  {GOLD}1.{RESET} 📡 {BOLD}Zuhri Frekuensi{RESET}
     Monitoring gelombang, medan magnetik, anomali quantum.

  {GOLD}2.{RESET} 🔮 {BOLD}Zuhri Predictive{RESET}
     Terminal prediktif — belajar dari kebiasaan Anda.

  {GOLD}3.{RESET} ⚡ {BOLD}Zuhri Energi{RESET}
     Monitor baterai, optimasi daya, prediksi.

{BOLD}🎯 FILOSOFI:{RESET}
  {CYAN}"Dari gelombang hingga energi —${RESET}
  {CYAN}satu pusat monitoring untuk semua."{RESET}
""")
    pause()

# ============================================================
# MENU UTAMA
# ============================================================
def menu():
    while True:
        clear()
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  📡 ZUHRI MONITORING SUITE — PUSAT MONITORING & ENERGI                  ║
║  ──────────────────────────────────────────────────────────────────────  ║
║  Frekuensi • Predictive • Energi                                        ║
║  Waktu: {GOLD}{datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}{RESET}
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 KELOMPOK MONITORING:{RESET}

  {GOLD}1.{RESET}  📡 {BOLD}ZUHRI FREKUENSI{RESET}       → Gelombang, medan, anomali
  {GOLD}2.{RESET}  🔮 {BOLD}ZUHRI PREDICTIVE{RESET}      → Terminal prediktif
  {GOLD}3.{RESET}  ⚡ {BOLD}ZUHRI ENERGI{RESET}          → Baterai & optimasi daya

  {GOLD}4.{RESET}  📊 {BOLD}STATUS SEMUA{RESET}           → Cek semua layer
  {GOLD}5.{RESET}  ℹ️  {BOLD}INFO MONITORING SUITE{RESET}  → Penjelasan

  {GOLD}0.{RESET}  🚪 Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-5): {RESET}").strip()
            if c == "0": break
            elif c == "1": zuhri_frekuensi()
            elif c == "2": zuhri_predictive()
            elif c == "3": zuhri_energi()
            elif c == "4": status_semua()
            elif c == "5": info()
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    menu()
