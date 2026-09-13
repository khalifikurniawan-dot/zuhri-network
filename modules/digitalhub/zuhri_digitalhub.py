#!/usr/bin/env python3
"""
ZUHRI DIGITAL HUB — PUSAT DIGITAL & KOMUNITAS
Social • Web3 • Web4 • Community
"""

import os, sys, json, subprocess, time
from datetime import datetime

HOME = os.path.expanduser("~")
DH_DIR = os.path.join(HOME, "zuhri_os", "digitalhub")
DATA_DIR = os.path.join(DH_DIR, "data")
LOG_DIR = os.path.join(DH_DIR, "logs")
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
# 1. ZUHRI SOCIAL
# ============================================================
def zuhri_social():
    clear()
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════════╗
║  🌐 ZUHRI SOCIAL — MEDIA SOSIAL & CHAT                                  ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 MENU:{RESET}
  {GOLD}1.{RESET} 💬 Chat Offline (P2P-Mesh)
  {GOLD}2.{RESET} 👥 Grup (Buat/Gabung)
  {GOLD}3.{RESET} 📰 Berita Online (Verified)
  {GOLD}4.{RESET} 🔍 Cek Hoax
  {GOLD}5.{RESET} 📊 Info
  {GOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "0": return
        subprocess.run(["python", os.path.expanduser("~/zuhri_os/social/zuhri_social.py")])
        pause()
    except: pause()

# ============================================================
# 2. ZUHRI WEB3 HUB
# ============================================================
def zuhri_web3():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  🌐 ZUHRI WEB3 HUB — PUSAT SITUS WEB3                                   ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 MENU:{RESET}
  {GOLD}1.{RESET} 📰 Berita Web3
  {GOLD}2.{RESET} 👥 Media Sosial Web3 (Farcaster, Lens)
  {GOLD}3.{RESET} 🛠️  Tools Web3 (IPFS, NFT)
  {GOLD}4.{RESET} 📚 Belajar Web3
  {GOLD}5.{RESET} 🌐 Infrastruktur Web3
  {GOLD}6.{RESET} 🔍 Cek Konten IPFS
  {GOLD}7.{RESET} ℹ️  Info Web3
  {GOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "0": return
        subprocess.run(["python", os.path.expanduser("~/zuhri_os/web3hub/zuhri_web3.py")])
        pause()
    except: pause()

# ============================================================
# 3. ZUHRI WEB4
# ============================================================
def zuhri_web4():
    clear()
    print(f"""
{BOLD}{BLUE}╔══════════════════════════════════════════════════════════════════════════╗
║  🤖 ZUHRI WEB4 — AI AGENT OTONOM                                        ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 MENU:{RESET}
  {GOLD}1.{RESET} 🤖 AI Agent Interaktif (Chat)
  {GOLD}2.{RESET} ➕ Buat Task Baru
  {GOLD}3.{RESET} 📋 Lihat Daftar Task
  {GOLD}4.{RESET} 🚀 Jalankan Task
  {GOLD}5.{RESET} 📊 Statistik
  {GOLD}6.{RESET} ℹ️  Info Web4
  {GOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "0": return
        subprocess.run(["python", os.path.expanduser("~/zuhri_os/web4/zuhri_web4.py")])
        pause()
    except: pause()

# ============================================================
# 4. ZUHRI COMMUNITY
# ============================================================
def zuhri_community():
    clear()
    print(f"""
{BOLD}{GOLD}╔══════════════════════════════════════════════════════════════════════════╗
║  🌌 ZUHRI COMMUNITY — KOMUNITAS ZUHRI NETWORK                           ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 MENU:{RESET}
  {GOLD}1.{RESET} 📜 Tulisan Indah Komunitas
  {GOLD}2.{RESET} 🚀 Roadmap 3 Tahun (V2)
  {GOLD}3.{RESET} 📱 Nama Akun Media Sosial
  {GOLD}4.{RESET} 🔗 Link Media Sosial
  {GOLD}5.{RESET} 📝 Versi Pendek (sharing)
  {GOLD}6.{RESET} ℹ️  Info Komunitas
  {GOLD}0.{RESET} Kembali
""")
    try:
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c == "0": return
        subprocess.run(["python", os.path.expanduser("~/zuhri_os/community/zuhri_community.py")])
        pause()
    except: pause()

# ============================================================
# MENU UTAMA
# ============================================================
def menu():
    while True:
        clear()
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  🌐 ZUHRI DIGITAL HUB — PUSAT DIGITAL & KOMUNITAS                       ║
║  ──────────────────────────────────────────────────────────────────────  ║
║  Social • Web3 • Web4 • Community                                       ║
║  Waktu: {GOLD}{datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}{RESET}
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 KELOMPOK DIGITAL:{RESET}

  {GOLD}1.{RESET}  🌐 {BOLD}ZUHRI SOCIAL{RESET}             → Chat offline + Berita
  {GOLD}2.{RESET}  🌐 {BOLD}ZUHRI WEB3 HUB{RESET}         → Situs Web3, IPFS, NFT
  {GOLD}3.{RESET}  🤖 {BOLD}ZUHRI WEB4{RESET}             → AI Agent Otonom
  {GOLD}4.{RESET}  🌌 {BOLD}ZUHRI COMMUNITY{RESET}        → Komunitas & Media Sosial

  {GOLD}5.{RESET}  📊 {BOLD}STATUS SEMUA{RESET}            → Cek semua layer
  {GOLD}6.{RESET}  ℹ️  {BOLD}INFO DIGITAL HUB{RESET}        → Penjelasan

  {GOLD}0.{RESET}  🚪 Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-6): {RESET}").strip()
            if c == "0": break
            elif c == "1": zuhri_social()
            elif c == "2": zuhri_web3()
            elif c == "3": zuhri_web4()
            elif c == "4": zuhri_community()
            elif c == "5": status_semua()
            elif c == "6": info()
        except KeyboardInterrupt:
            break

def status_semua():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  📊 STATUS SEMUA LAYER DIGITAL                                          ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    # Cek file
    social_ok = os.path.exists(os.path.expanduser("~/zuhri_os/social/zuhri_social.py"))
    web3_ok = os.path.exists(os.path.expanduser("~/zuhri_os/web3hub/zuhri_web3.py"))
    web4_ok = os.path.exists(os.path.expanduser("~/zuhri_os/web4/zuhri_web4.py"))
    comm_ok = os.path.exists(os.path.expanduser("~/zuhri_os/community/zuhri_community.py"))
    
    print(f"  🌐 Zuhri Social    : {GREEN + '✅' + RESET if social_ok else RED + '❌' + RESET}")
    print(f"  🌐 Zuhri Web3 Hub  : {GREEN + '✅' + RESET if web3_ok else RED + '❌' + RESET}")
    print(f"  🤖 Zuhri Web4      : {GREEN + '✅' + RESET if web4_ok else RED + '❌' + RESET}")
    print(f"  🌌 Zuhri Community : {GREEN + '✅' + RESET if comm_ok else RED + '❌' + RESET}")
    print()
    pause()

def info():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║  ℹ️  INFO ZUHRI DIGITAL HUB                                              ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}🎯 4 KELOMPOK DIGITAL:{RESET}

  {GOLD}1.{RESET} 🌐 {BOLD}Zuhri Social{RESET}
     Chat offline + Berita terverifikasi + Cek hoax

  {GOLD}2.{RESET} 🌐 {BOLD}Zuhri Web3 Hub{RESET}
     Situs Web3, IPFS, NFT, Belajar Web3

  {GOLD}3.{RESET} 🤖 {BOLD}Zuhri Web4{RESET}
     AI Agent Otonom, Task Automation

  {GOLD}4.{RESET} 🌌 {BOLD}Zuhri Community{RESET}
     Komunitas, Media Sosial, Roadmap V2

{BOLD}🎯 FILOSOFI:{RESET}
  {CYAN}"Dari Social sampai Web4 — semua dalam satu pusat."{RESET}
""")
    pause()

if __name__ == "__main__":
    menu()
