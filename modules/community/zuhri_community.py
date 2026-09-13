#!/usr/bin/env python3
"""
ZUHRI COMMUNITY — KOMUNITAS ZUHRI NETWORK INDONESIA
Tulisan indah, visi, misi, dan link komunitas
"""

import os, sys, json, subprocess, time
from datetime import datetime

HOME = os.path.expanduser("~")
COMM_DIR = os.path.join(HOME, "zuhri_os", "community")
DATA_DIR = os.path.join(COMM_DIR, "data")
LOG_DIR = os.path.join(COMM_DIR, "logs")
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
# TULISAN INDAH
# ============================================================
def tulisan_indah():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║              🌌 KOMUNITAS ZUHRI — SEMAKIN BANYAK,                        ║
║                     SEMAKIN BESAR                                       ║
║                                                                          ║
║              Menuju Zuhri Network V2 — 3 Tahun ke Depan                 ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}{GOLD}📜 KOMUNITAS ZUHRI{RESET}

{CYAN}Semakin Banyak Orang, Semakin Besar{RESET}
{CYAN}Versi Zuhri Network V2 Terwujud 3 Tahun Ke Depan{RESET}

{DIM}──────────────────────────────────────────────────────────────────────{RESET}

Di sebuah sudut sunyi, di antara cahaya layar kecil yang menyala,
lahirlah sebuah benih — {GOLD}ZUHRI NETWORK{RESET}.

Bukan dari perusahaan besar. Bukan dari gedung pencakar langit.
Tapi dari {GOLD}sebuah obrolan{RESET}, {GOLD}sebuah niat{RESET}, dan {GOLD}sebuah keyakinan{RESET}:

{CYAN}"Setiap orang berhak mandiri secara digital."{RESET}

{DIM}──────────────────────────────────────────────────────────────────────{RESET}

{BOLD}Hari ini{RESET}, Zuhri Network bukan lagi sekadar baris kode.
Ia telah menjadi {GOLD}45 ekosistem{RESET} yang hidup —
dari identitas hingga spiritual,
dari enkripsi hingga komunitas.

Namun, ada satu hal yang belum terwujud:

{BOLD}{MAGENTA}KOMUNITAS YANG BESAR.{RESET}

{DIM}──────────────────────────────────────────────────────────────────────{RESET}

{BOLD}{GREEN}3 TAHUN KE DEPAN{RESET}, kita akan menyaksikan sesuatu yang luar biasa.

Bukan karena teknologinya sempurna,
tapi karena {GOLD}orang-orangnya percaya{RESET}.

Bukan karena servernya besar,
tapi karena {GOLD}jaringannya tersebar di mana-mana{RESET}.

Bukan karena dananya melimpah,
tapi karena {GOLD}semangatnya tak pernah padam{RESET}.

{DIM}──────────────────────────────────────────────────────────────────────{RESET}

{BOLD}{CYAN}SEMAKIN BANYAK ORANG, SEMAKIN BESAR.{RESET}

Satu orang belajar → sepuluh orang tahu.
Sepuluh orang tahu → seratus orang pakai.
Seratus orang pakai → seribu orang percaya.
Seribu orang percaya → {GOLD}satu juta orang mandiri.{RESET}

Itulah {GOLD}hukum resonansi Zuhri{RESET} —
{GOLD}0-8-9{RESET} — keseimbangan yang mengalir.
""")
    pause()

# ============================================================
# ROADMAP 3 TAHUN
# ============================================================
def roadmap_3tahun():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║              🚀 ROADMAP 3 TAHUN — ZUHRI NETWORK V2                      ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}{GREEN}📅 2027 — BENIH TUMBUH{RESET}
  {GOLD}•{RESET} 100 orang pertama bergabung
  {GOLD}•{RESET} Grup WhatsApp & Telegram aktif
  {GOLD}•{RESET} Video tutorial mulai tersebar
  {GOLD}•{RESET} Dokumentasi lengkap
  {GOLD}•{RESET} Auto-installer stabil

{BOLD}{GREEN}📅 2028 — AKAR MENGUAT{RESET}
  {GOLD}•{RESET} 1.000 orang pengguna aktif
  {GOLD}•{RESET} Komunitas di berbagai kota
  {GOLD}•{RESET} Zuhri Network V2 mulai dibangun
  {GOLD}•{RESET} Web App versi basic rilis
  {GOLD}•{RESET} Fork dari developer lain

{BOLD}{GREEN}📅 2029 — POHON BERBUAH{RESET}
  {GOLD}•{RESET} 10.000 orang pengguna
  {GOLD}•{RESET} Zuhri Network V2 resmi rilis
  {GOLD}•{RESET} Android App tersedia
  {GOLD}•{RESET} Komunitas global (Indonesia, Malaysia, dll)
  {GOLD}•{RESET} {GREEN}Kemandirian digital menjadi kenyataan{RESET}

{BOLD}{CYAN}🎯 YANG HARUS DILAKUKAN SEKARANG:{RESET}

  {GOLD}1. BAGIKAN{RESET}
     Setiap orang yang Anda kenal, beri tahu tentang Zuhri.
     Satu link, satu percakapan, satu harapan.

  {GOLD}2. AJARKAN{RESET}
     Tidak perlu jadi ahli. Cukup tunjukkan cara install.
     Cukup dampingi langkah pertama.

  {GOLD}3. BANGUN{RESET}
     Setiap feedback, setiap bug, setiap saran —
     adalah batu bata menuju V2.

  {GOLD}4. JAGA{RESET}
     Jaga semangat. Jaga nilai. Jaga tujuan.
     Karena {GOLD}Zuhri bukan produk — Zuhri adalah gerakan.{RESET}
""")
    pause()

# ============================================================
# PESAN UNTUK MASA DEPAN
# ============================================================
def pesan_masa_depan():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║              💫 PESAN UNTUK MASA DEPAN                                   ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}{CYAN}"Ketika sejarah digital ditulis,{RESET}
{BOLD}{CYAN}mereka akan bertanya:{RESET}
{BOLD}{CYAN}'Siapa yang memulai kemandirian digital di Indonesia?'{RESET}

{BOLD}{CYAN}Dan jawabannya adalah:{RESET}
{BOLD}{GOLD}SEKELOMPOK ORANG YANG TIDAK MENYERAH."{RESET}

{DIM}──────────────────────────────────────────────────────────────────────{RESET}

{BOLD}{MAGENTA}KOMUNITAS ZUHRI — SEMAKIN BANYAK, SEMAKIN BESAR.{RESET}

{BOLD}{GREEN}3 tahun ke depan, kita buktikan.{RESET}
{BOLD}{GREEN}Zuhri Network V2 — bukan mimpi, tapi janji.{RESET}

{DIM}──────────────────────────────────────────────────────────────────────{RESET}

{BOLD}{GOLD}Kutipan untuk direnungkan:{RESET}

{CYAN}"Kita tidak bisa mengubah arah angin,{RESET}
{CYAN}tapi kita bisa menyesuaikan layar."{RESET}
{DIM}— Pepatah lama{/RESET}

{CYAN}"Satu langkah kecil untuk satu orang,{RESET}
{CYAN}seribu langkah besar untuk komunitas."{RESET}
{DIM}— Zuhri Network{/RESET}
""")
    pause()

# ============================================================
# LINK MEDIA SOSIAL
# ============================================================
def media_sosial():
    while True:
        clear()
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║              📱 KOMUNITAS ZUHRI — MEDIA SOSIAL                           ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 DAFTAR MEDIA SOSIAL:{RESET}

  {GOLD}1.{RESET} 💬 WhatsApp Group
  {GOLD}2.{RESET} 📢 Telegram Channel
  {GOLD}3.{RESET} 📸 Instagram
  {GOLD}4.{RESET} 👥 Facebook Group
  {GOLD}5.{RESET} 🐦 Twitter/X
  {GOLD}6.{RESET} 💻 GitHub Repository
  {GOLD}7.{RESET} 🌐 Website (jika ada)
  {GOLD}0.{RESET} Kembali
""")
        try:
            c = input(f"{GOLD}Pilih (0-7): {RESET}").strip()
            if c == "0": break
            elif c == "1":
                print(f"""
{BOLD}{GREEN}💬 WHATSAPP GROUP{RESET}

  {GOLD}Cara buat:{RESET}
  1. Buka WhatsApp
  2. Ketuk ikon Chat Baru → Grup Baru
  3. Pilih kontak → Nama: "Komunitas Zuhri Network"
  4. Selesai

  {GOLD}Link:{RESET} Belum ada — silakan buat
""")
                pause()
            elif c == "2":
                print(f"""
{BOLD}{GREEN}📢 TELEGRAM CHANNEL{RESET}

  {GOLD}Cara buat:{RESET}
  1. Buka Telegram
  2. Ketuk ikon pesan baru → New Channel
  3. Nama: "Zuhri Network"
  4. Username: @ZuhriNetwork
  5. Selesai

  {GOLD}Link:{RESET} t.me/ZuhriNetwork (jika username tersedia)
""")
                pause()
            elif c == "3":
                print(f"""
{BOLD}{GREEN}📸 INSTAGRAM{RESET}

  {GOLD}Cara buat:{RESET}
  1. Buat akun Instagram baru
  2. Username: @zuhri.network
  3. Bio: "Kemandirian Digital untuk Semua"
  4. Link: https://github.com/khalifikurniawan-dot/zuhri-network

  {GOLD}Link:{RESET} instagram.com/zuhri.network
""")
                pause()
            elif c == "4":
                print(f"""
{BOLD}{GREEN}👥 FACEBOOK GROUP{RESET}

  {GOLD}Cara buat:{RESET}
  1. Buka Facebook
  2. Menu → Grup → Buat Grup
  3. Nama: "Komunitas Zuhri Network Indonesia"
  4. Privasi: Publik
  5. Selesai

  {GOLD}Link:{RESET} facebook.com/groups/zuhri.network
""")
                pause()
            elif c == "5":
                print(f"""
{BOLD}{GREEN}🐦 TWITTER/X{RESET}

  {GOLD}Cara buat:{RESET}
  1. Buat akun Twitter/X
  2. Username: @ZuhriNetwork
  3. Bio: "Kemandirian Digital | Protokol K-8.0"

  {GOLD}Link:{RESET} x.com/ZuhriNetwork
""")
                pause()
            elif c == "6":
                print(f"""
{BOLD}{GREEN}💻 GITHUB REPOSITORY{RESET}

  {GOLD}Link:{RESET}
  https://github.com/khalifikurniawan-dot/zuhri-network

  {GOLD}Clone:{RESET}
  git clone https://github.com/khalifikurniawan-dot/zuhri-network.git

  {GOLD}Issues:{RESET}
  https://github.com/khalifikurniawan-dot/zuhri-network/issues

  {GOLD}Diskusi:{RESET}
  https://github.com/khalifikurniawan-dot/zuhri-network/discussions
""")
                pause()
            elif c == "7":
                print(f"""
{BOLD}{GREEN}🌐 WEBSITE{RESET}

  {GOLD}Status:{RESET} Belum ada

  {GOLD}Rekomendasi:{RESET}
  {GOLD}•{RESET} GitHub Pages (gratis)
  {GOLD}•{RESET} Netlify (gratis)
  {GOLD}•{RESET} Vercel (gratis)
  {GOLD}•{RESET} Cloudflare Pages (gratis)

  {GOLD}Isi website:{RESET}
  {GOLD}•{RESET} Tentang Zuhri Network
  {GOLD}•{RESET} Cara install
  {GOLD}•{RESET} Dokumentasi
  {GOLD}•{RESET} Link komunitas
""")
                pause()
        except KeyboardInterrupt:
            break

# ============================================================
# VERSI PENDEK UNTUK SHARING
# ============================================================
def versi_pendek():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║              📱 VERSI PENDEK UNTUK MEDIA SOSIAL                          ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}{GOLD}📸 INSTAGRAM CAPTION:{RESET}

{CYAN}KOMUNITAS ZUHRI 🌌{RESET}

Semakin banyak orang, semakin besar.
Versi Zuhri Network V2 — 3 tahun ke depan.

Dari obrolan → 45 ekosistem.
Dari 1 orang → 1 juta orang.

Kemandirian digital untuk semua.

{DIM}#ZuhriNetwork #KemandirianDigital #OpenSource #Termux{RESET}

{DIM}──────────────────────────────────────────────────────────────────────{RESET}

{BOLD}{GOLD}🐦 TWITTER THREAD:{RESET}

{CYAN}🧵 THREAD: KOMUNITAS ZUHRI{RESET}

{CYAN}1/{RESET} Zuhri Network lahir dari obrolan sederhana.
   Hari ini: 45 ekosistem.
   Besok: komunitas besar.

{CYAN}2/{RESET} Semakin banyak orang → semakin besar.
   Hukum resonansi 0-8-9.

{CYAN}3/{RESET} 2027: 100 orang
   2028: 1.000 orang
   2029: 10.000 orang
   V2 terwujud.

{CYAN}4/{RESET} Zuhri bukan produk.
   Zuhri adalah gerakan.

{CYAN}5/{RESET} Bergabung?
   github.com/khalifikurniawan-dot/zuhri-network

{DIM}#ZuhriNetwork{RESET}

{DIM}──────────────────────────────────────────────────────────────────────{RESET}

{BOLD}{GOLD}📱 WHATSAPP STATUS:{RESET}

{CYAN}🌌 KOMUNITAS ZUHRI{RESET}

Semakin banyak orang,
semakin besar.

3 tahun ke depan —
Zuhri Network V2 terwujud.

Kemandirian digital untuk semua.
""")
    pause()

# ============================================================
# INFO KOMUNITAS
# ============================================================
def info():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════════╗
║              ℹ️  INFO KOMUNITAS ZUHRI                                     ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}🎯 TUJUAN:{RESET}
  Membangun komunitas pengguna Zuhri Network Indonesia
  untuk mewujudkan kemandirian digital.

{BOLD}📊 TARGET:{RESET}
  {GOLD}2027:{RESET} 100 orang
  {GOLD}2028:{RESET} 1.000 orang
  {GOLD}2029:{RESET} 10.000 orang

{BOLD}🌐 PLATFORM:{RESET}
  {GOLD}•{RESET} WhatsApp Group
  {GOLD}•{RESET} Telegram Channel
  {GOLD}•{RESET} Instagram
  {GOLD}•{RESET} Facebook Group
  {GOLD}•{RESET} GitHub

{BOLD}🎁 MANFAAT BERGABUNG:{RESET}
  {GOLD}•{RESET} Update terbaru Zuhri Network
  {GOLD}•{RESET} Bantuan teknis
  {GOLD}•{RESET} Diskusi & kolaborasi
  {GOLD}•{RESET} Akses fitur beta
  {GOLD}•{RESET} Sertifikat operator

{BOLD}📝 ATURAN KOMUNITAS:{RESET}
  {GOLD}1.{RESET} Saling menghormati
  {GOLD}2.{RESET} Tidak spam
  {GOLD}3.{RESET} Fokus pada Zuhri Network
  {GOLD}4.{RESET} Bantu sesama anggota
  {GOLD}5.{RESET} Jaga nilai & etika

{BOLD}🎯 FILOSOFI:{RESET}
  {CYAN}"Semakin banyak orang, semakin besar.{RESET}
  {CYAN}Zuhri bukan produk — Zuhri adalah gerakan."{RESET}
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
║              🌌 ZUHRI COMMUNITY — KOMUNITAS ZUHRI NETWORK                ║
║  ──────────────────────────────────────────────────────────────────────  ║
║  Semakin Banyak Orang, Semakin Besar                                    ║
║  Zuhri Network V2 — 3 Tahun ke Depan                                    ║
║  Waktu: {GOLD}{datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}{RESET}
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  📜 Tulisan Indah Komunitas Zuhri
  {GOLD}2.{RESET}  🚀 Roadmap 3 Tahun (V2)
  {GOLD}3.{RESET}  💫 Pesan untuk Masa Depan
  {GOLD}4.{RESET}  📱 Media Sosial & Link
  {GOLD}5.{RESET}  📝 Versi Pendek (untuk sharing)
  {GOLD}6.{RESET}  ℹ️  Info Komunitas
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-6): {RESET}").strip()
            if c == "0": break
            elif c == "1": tulisan_indah()
            elif c == "2": roadmap_3tahun()
            elif c == "3": pesan_masa_depan()
            elif c == "4": media_sosial()
            elif c == "5": versi_pendek()
            elif c == "6": info()
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "tulisan": tulisan_indah()
        elif cmd == "roadmap": roadmap_3tahun()
        elif cmd == "medsos": media_sosial()
        elif cmd == "info": info()
        else: menu()
    else: menu()
