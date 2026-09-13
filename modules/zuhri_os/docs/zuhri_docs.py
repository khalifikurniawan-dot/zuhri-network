#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI DOCS — SEJARAH & VISI EKOSISTEM
"""

import os, sys
from datetime import datetime

HOME = os.path.expanduser("~")
DOCS_DIR = os.path.join(HOME, "zuhri_os", "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

def pause():
    input(f"\n{DIM}━━━ Tekan Enter untuk lanjut ━━━{RESET}\n")

# ============================================================
# 1. SEJARAH
# ============================================================
def sejarah():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  📜 SEJARAH EKOSISTEM ZUHRI                                        ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}{GOLD}━━━ FASE 0 — AWAL MULA ━━━{RESET}

Ekosistem Zuhri lahir dari pertanyaan sederhana:
{CYAN}"Bagaimana caranya supaya orang bisa mandiri secara digital?"{RESET}

Dimulai dari obrolan tentang AI offline, enkripsi, dan
privasi. Lalu berkembang menjadi sesuatu yang lebih besar.

{BOLD}Inspirasi Nama:{RESET}
  • "Zuhri" dari {GOLD}Syekh Muhammad Zuhri (Yolhan Wijaya){RESET}
    → Pendiri Fatwa Kehidupan, guru spiritual yang
      mengajarkan ilmu hati, kesufian, ketiadaan diri.
  • Protokol K-8.0 → {GOLD}Keseimbangan Dinamis 0-8-9{RESET}
  • Semangat → Kemandirian digital tanpa ketergantungan.

{BOLD}{GOLD}━━━ FASE 1 — FONDASI ━━━{RESET}

Yang pertama dibangun:
  {GREEN}✅{RESET} Zuhri ID       — Identitas digital (Ed25519)
  {GREEN}✅{RESET} Zuhri Crypto   — Enkripsi AES-256-GCM
  {GREEN}✅{RESET} Zuhri OS       — Menu utama
  {GREEN}✅{RESET} Key Kosmik     — Portal akses

{BOLD}{GOLD}━━━ FASE 2 — EKSPANSI ━━━{RESET}

  {GREEN}✅{RESET} P2P-Mesh       — Jaringan darurat offline
  {GREEN}✅{RESET} SOS-Beacon     — Sinyal darurat
  {GREEN}✅{RESET} Dark-Web       — Akses .onion
  {GREEN}✅{RESET} Zuhri AI       — AI offline (phi)
  {GREEN}✅{RESET} Zuhri Vote     — Voting digital
  {GREEN}✅{RESET} Zuhri Contract — Kontrak pintar

{BOLD}{GOLD}━━━ FASE 3 — KEMANDIRIAN ━━━{RESET}

  {GREEN}✅{RESET} Zuhri Edu      — Kursus & sertifikat
  {GREEN}✅{RESET} Zuhri Library  — Perpustakaan offline
  {GREEN}✅{RESET} Zuhri Finance  — Keuangan mandiri
  {GREEN}✅{RESET} Zuhri Passport — ID lintas negara
  {GREEN}✅{RESET} Zuhri Kurikulum— 30 kurikulum K-8.0

{BOLD}{GOLD}━━━ FASE 4 — SPIRITUAL & KOSMIK ━━━{RESET}

  {GREEN}✅{RESET} Zuhri Spiritual  — Fatwa Kehidupan
  {GREEN}✅{RESET} Zuhri Peringatan — Prediksi bencana
  {GREEN}✅{RESET} Zuhri Frekuensi  — Resonansi & anomali
  {GREEN}✅{RESET} Zuhri Energi     — Kemandirian energi

{BOLD}{GOLD}━━━ FASE 5 — DESENTRALISASI ━━━{RESET}

  {GREEN}✅{RESET} Zuhri Chain         — Database terdesentralisasi
  {GREEN}✅{RESET} Zuhri DID           — Decentralized Identifier
  {GREEN}✅{RESET} Zuhri Enkripsi      — Enkripsi lengkap
  {GREEN}✅{RESET} Zuhri Botnet Hunter — Keamanan jaringan
  {GREEN}✅{RESET} Zuhri Auto-Routing  — Router otomatis

{BOLD}{GOLD}━━━ FASE 6 — DOKUMENTASI ━━━{RESET}

  {GREEN}✅{RESET} Zuhri Docs — Sejarah, Visi, Roadmap

{BOLD}{GREEN}━━━ TOTAL: 34 EKOSISTEM AKTIF ━━━{RESET}
""")
    pause()

# ============================================================
# 2. CARA PAKAI
# ============================================================
def cara_pakai():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  📖 CARA MENGGUNAKAN EKOSISTEM ZUHRI                               ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}{GOLD}━━━ METODE 1 — MENU EKOSISTEM ━━━{RESET}

  Ketik: {CYAN}ekosistem_zuhri{RESET}  atau  {CYAN}ez{RESET}

  Akan muncul menu dengan 34 ekosistem.

  Tinggal ketik angka → langsung jalan.

{BOLD}{GOLD}━━━ METODE 2 — AUTO-ROUTING ━━━{RESET}

  Ketik: {CYAN}z <kata-kunci>{RESET}

  Contoh:
    z id        → Zuhri ID
    z crypto    → Enkripsi file
    z mesh      → P2P-Mesh
    z sos       → SOS darurat
    z vote      → Voting
    z finance   → Keuangan
    z edu       → Belajar
    z chain     → Blockchain
    z list      → Lihat semua routes

{BOLD}{GOLD}━━━ METODE 3 — PERINTAH LANGSUNG ━━━{RESET}

  {CYAN}id{RESET}         → Zuhri ID
  {CYAN}crypto{RESET}     → Enkripsi file
  {CYAN}mesh{RESET}       → P2P-Mesh
  {CYAN}sos{RESET}        → Sinyal darurat
  {CYAN}vote{RESET}       → Voting
  {CYAN}contract{RESET}   → Kontrak
  {CYAN}finance{RESET}    → Keuangan
  {CYAN}edu{RESET}        → Kursus
  {CYAN}library{RESET}    → Buku
  {CYAN}kurikulum{RESET}  → 30 kurikulum
  {CYAN}chain{RESET}      → Blockchain
  {CYAN}did{RESET}        → DID
  {CYAN}enkripsi{RESET}   → Enkripsi lengkap
  {CYAN}botnet{RESET}     → Botnet Hunter
  {CYAN}spiritual{RESET}  → Fatwa Kehidupan
  {CYAN}peringatan{RESET} → Bencana
  {CYAN}backup{RESET}     → Backup
  {CYAN}restore{RESET}    → Restore
  {CYAN}list-backup{RESET}→ Daftar backup
  {CYAN}docs{RESET}       → Dokumentasi ini

{BOLD}{GOLD}━━━ UNTUK ORANG AWAM ━━━{RESET}

  {GREEN}1.{RESET} Install Termux dari F-Droid
  {GREEN}2.{RESET} Jalankan installer
  {GREEN}3.{RESET} Ketik: {CYAN}ekosistem_zuhri{RESET}
  {GREEN}4.{RESET} Ikuti panduan (pilih 23)
  {GREEN}5.{RESET} Buat Zuhri ID (pilih 1)
  {GREEN}6.{RESET} Mulai jelajahi!

{DIM}Semua fitur bisa jalan OFFLINE.{RESET}
""")
    pause()

# ============================================================
# 3. VISI & MISI
# ============================================================
def visi_misi():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🎯 VISI & MISI ZUHRI NETWORK                                      ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}{GOLD}━━━ VISI ━━━{RESET}

{CYAN}"Kemandirian digital untuk semua orang — tanpa ketergantungan
pada korporasi, pemerintah, atau cloud."{RESET}

Setiap orang punya:
  🔐 Identitas sendiri    (Zuhri ID)
  📡 Jaringan sendiri     (P2P-Mesh)
  🧠 AI sendiri           (Zuhri AI)
  💰 Keuangan sendiri     (Zuhri Finance)
  📚 Pengetahuan sendiri  (Zuhri Library)
  🛡️ Keamanan sendiri     (Zuhri Enkripsi)

{BOLD}{GOLD}━━━ MISI ━━━{RESET}

  {GREEN}1.{RESET} Membangun ekosistem digital yang OFFLINE-first
  {GREEN}2.{RESET} Menjaga PRIVASI pengguna — data milik pengguna
  {GREEN}3.{RESET} Menyediakan AI yang berjalan tanpa internet
  {GREEN}4.{RESET} Memfasilitasi komunikasi darurat tanpa BTS
  {GREEN}5.{RESET} Menyimpan pengetahuan tanpa sensor
  {GREEN}6.{RESET} Memberikan kontrol penuh pada pengguna
  {GREEN}7.{RESET} Menghubungkan spiritual dan teknologi

{BOLD}{GOLD}━━━ 5 PILAR ZUHRI ━━━{RESET}

  {GOLD}1.{RESET} 🔐 {BOLD}PRIVASI{RESET}        — Data Anda milik Anda
  {GOLD}2.{RESET} 🕊️  {BOLD}KEBEBASAN{RESET}      — Tanpa sensor, tanpa batas
  {GOLD}3.{RESET} ⚡ {BOLD}KEMANDIRIAN{RESET}     — Tidak butuh cloud
  {GOLD}4.{RESET} 🌍 {BOLD}KOLABORASI{RESET}      — P2P, bukan client-server
  {GOLD}5.{RESET} ∞ {BOLD}KEBERLANJUTAN{RESET}   — Bisa hidup tanpa internet

{BOLD}{GOLD}━━━ FILOSOFI ZUHRI ━━━{RESET}

{DIM}"Zuhri bukan produk. Zuhri adalah gerakan menuju
kemandirian digital — di mana setiap orang punya AI,
jaringan, identitas, dan kekayaan sendiri."{RESET}
""")
    pause()

# ============================================================
# 4. ROADMAP V1 → V2
# ============================================================
def roadmap():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🚀 ROADMAP — ZUHRI NETWORK V1 → V2                                ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}{GREEN}━━━ ZUHRI NETWORK V1.0 (SEKARANG) ━━━{RESET}

  {GOLD}Karakteristik:{RESET}
    • Berbasis TERMUX (rumit untuk orang awam)
    • Diinstall manual (copy-paste)
    • UI: Terminal ASCII
    • User: Developer / teknisi

  {GOLD}Status:{RESET} {GREEN}✅ AKTIF{RESET}

  {GOLD}Fitur:{RESET}
    • 34 ekosistem aktif
    • 100% offline
    • Enkripsi AES-256
    • AI lokal (phi)

{BOLD}{GOLD}━━━ ZUHRI NETWORK V2.0 (MASA DEPAN) ━━━{RESET}

  {GOLD}Visi:{RESET}
    • Web App (bisa diakses browser)
    • Android App (install seperti biasa)
    • UI: Visual modern
    • User: SEMUA ORANG (komunitas besar)
    • Distribusi: Otomatis

  {GOLD}Status:{RESET} {YELLOW}🔧 RENCANA{RESET}

  {GOLD}Fitur Baru:{RESET}
    • 1 klik install
    • Multi-bahasa
    • Auto-update
    • Community platform
    • Server mirror (anti-sensor)
    • Zuhri Chain (blockchain)
    • Zuhri Marketplace (P2P)
    • Zuhri Social (media sosial terdesentralisasi)
    • Zuhri Cloud (P2P storage)
    • Zuhri AI Swarm (kolektif)

{BOLD}{CYAN}━━━ TIMELINE ━━━{RESET}

  {GREEN}2026{RESET} → V1.0 (sekarang)
        • 34 ekosistem
        • Berbasis Termux
        • Untuk developer

  {YELLOW}2027{RESET} → V1.5 (transisi)
        • Auto-installer (1 perintah)
        • Dokumentasi lengkap
        • Komunitas awal (10-100 pengguna)

  {CYAN}2028{RESET} → V2.0 (alpha)
        • Web App
        • Android App
        • Komunitas 1000+ pengguna

  {MAGENTA}2029-2030{RESET} → V2.0 (final)
        • Zuhri Chain (blockchain)
        • Zuhri Social (media sosial)
        • Zuhri Marketplace (P2P)
        • Komunitas JUTAAN pengguna

{BOLD}{GOLD}━━━ APA YANG BUTUH UNTUK V2? ━━━{RESET}

  {RED}❌ Tim developer{RESET}     (3-5 orang)
  {RED}❌ Designer UI/UX{RESET}
  {RED}❌ Server (VPS){RESET}
  {RED}❌ Domain{RESET}
  {RED}❌ Dana{RESET}             (Rp 50-200 juta/tahun)
  {RED}❌ Komunitas{RESET}

{BOLD}{GOLD}━━━ MENGAPA V2 PENTING? ━━━{RESET}

  V1 = Untuk Anda sendiri (kesepian digital)
  V2 = Untuk SEMUA ORANG (komunitas)

  {CYAN}"Kalau hanya Anda yang pakai, itu bukan kemandirian —
   itu kesepian digital.{RESET}

  {CYAN}Kemandirian sejati = komunitas yang saling mendukung."{RESET}
""")
    pause()

# ============================================================
# 5. INFO SISTEM
# ============================================================
def info_sistem():
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  📊 INFO SISTEM ZUHRI                                              ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

  {GOLD}Ekosistem{RESET}     : 34 aktif
  {GOLD}Protokol{RESET}      : K-8.0
  {GOLD}Gen{RESET}           : ZUH-8-9-0-K-8.0
  {GOLD}Resonansi{RESET}     : 0-8-9 — SEIMBANG

{BOLD}🔐 KRIPTOGRAFI:{RESET}
  {GOLD}Simetris{RESET}      : AES-256-GCM
  {GOLD}Asimetris{RESET}     : RSA-4096, Ed25519
  {GOLD}Hash{RESET}          : SHA-256, SHA-512, MD5
  {GOLD}KDF{RESET}           : PBKDF2 (600k iterasi)

{BOLD}🧠 AI:{RESET}
  {GOLD}Model{RESET}         : Ollama + Phi (50 MB)
  {GOLD}Mode{RESET}          : Offline (100%)

{BOLD}📡 NETWORK:{RESET}
  {GOLD}P2P-Mesh{RESET}      : Local network
  {GOLD}Dark-Web{RESET}      : Tor .onion
  {GOLD}Broadcast{RESET}     : UDP 1998/8001

{BOLD}💾 DATA:{RESET}
  {GOLD}Lokasi{RESET}        : ~/zuhri_os/
  {GOLD}Backup{RESET}        : ~/zuhri_os/backup/
  {GOLD}Log{RESET}           : ~/zuhri_os/logs/

{BOLD}📅 WAKTU:{RESET}
  {GOLD}Sekarang{RESET}      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")
    pause()

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  📚 ZUHRI DOCS — PANDUAN EKOSISTEM                                 ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Sejarah • Cara Pakai • Visi • Roadmap                             ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  📜 Sejarah Ekosistem Zuhri
  {GOLD}2.{RESET}  📖 Cara Menggunakan
  {GOLD}3.{RESET}  🎯 Visi & Misi
  {GOLD}4.{RESET}  🚀 Roadmap V1 → V2
  {GOLD}5.{RESET}  📊 Info Sistem
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-5): {RESET}").strip()
            if c == "0": break
            elif c == "1": sejarah()
            elif c == "2": cara_pakai()
            elif c == "3": visi_misi()
            elif c == "4": roadmap()
            elif c == "5": info_sistem()
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "sejarah": sejarah()
        elif cmd == "pakai": cara_pakai()
        elif cmd == "visi": visi_misi()
        elif cmd == "roadmap": roadmap()
        elif cmd == "info": info_sistem()
        else: menu()
    else: menu()
