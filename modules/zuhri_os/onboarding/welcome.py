#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI ONBOARDING — PANDUAN UNTUK PEMULA
"""

import os, sys, time

HOME = os.path.expanduser("~")
ID_FILE = os.path.join(HOME, "zuhri_os", "id", "identity.json")

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

def clear(): os.system('clear')

def pause(msg="Tekan Enter untuk lanjut..."):
    input(f"\n{DIM}{msg}{RESET}")

def load_identity():
    if not os.path.exists(ID_FILE): return None
    try:
        import json
        return json.load(open(ID_FILE))
    except: return None

# ============================================================
# STEP 1 — WELCOME
# ============================================================
def step_welcome():
    clear()
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        🌌 SELAMAT DATANG DI EKOSISTEM ZUHRI                     ║
║                                                                  ║
║        Ekosistem Digital untuk Kemandirian & Privasi            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}Apa itu Ekosistem Zuhri?{RESET}

Ekosistem Zuhri adalah kumpulan aplikasi digital yang berjalan
di HP Anda. Tidak butuh internet, tidak butuh server,
tidak butuh cloud.

{BOLD}Yang bisa Anda lakukan:{RESET}

  {GOLD}🆔{RESET} Identitas digital tanpa KTP
  {GOLD}📡{RESET} Kirim pesan darurat tanpa internet
  {GOLD}🆘{RESET} Sinyal SOS ke perangkat sekitar
  {GOLD}🗳️{RESET}  Voting digital yang tidak bisa dicurangi
  {GOLD}📜{RESET} Kontrak digital
  {GOLD}🛂{RESET} Passport digital lintas negara
  {GOLD}🔐{RESET} Enkripsi file standar militer
  {GOLD}🌑{RESET} Akses dark web dengan aman
  {GOLD}🧠{RESET} AI pribadi tanpa internet
  {GOLD}🔍{RESET} Deteksi objek dengan kamera
  {GOLD}💰{RESET} Dompet crypto offline
  {GOLD}🌍{RESET} Terjemahan bahasa tanpa internet
  {GOLD}📚{RESET} Perpustakaan offline
  {GOLD}🎓{RESET} Kursus & sertifikat digital

{BOLD}{GREEN}Semua ini gratis. Semua ini milik Anda.{RESET}
""")
    pause()

# ============================================================
# STEP 2 — ZUHRI ID
# ============================================================
def step_id():
    clear()
    print(f"""
{BOLD}{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  LANGKAH 1 DARI 5 — IDENTITAS DIGITAL ANDA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

{BOLD}Zuhri ID{RESET} adalah identitas digital Anda.

Anggap seperti KTP, tapi:
  ✅ Tidak butuh KTP asli
  ✅ Tidak butuh email
  ✅ Tidak butuh nomor HP
  ✅ Tidak bisa dipalsukan
  ✅ Tidak bisa dihapus

{BOLD}Fungsinya:{RESET}
  {GOLD}•{RESET} Tanda tangan digital
  {GOLD}•{RESET} Login tanpa password
  {GOLD}•{RESET} Verifikasi identitas
  {GOLD}•{RESET} Voting digital
""")
    
    identity = load_identity()
    if identity:
        print(f"{GREEN}✅ Anda sudah punya Zuhri ID:{RESET}")
        print(f"   {GOLD}{identity['zuhri_id']}{RESET}")
        print(f"   Nama: {identity['name']}")
    else:
        print(f"{YELLOW}⚠️  Anda belum punya Zuhri ID.{RESET}")
        print(f"\n{BOLD}Buat sekarang?{RESET}")
        print(f"  {GOLD}1.{RESET} Ya, buat Zuhri ID")
        print(f"  {GOLD}2.{RESET} Nanti saja")
        
        try:
            c = input(f"\n{CYAN}Pilih (1/2): {RESET}").strip()
            if c == "1":
                os.system("python ~/zuhri_os/id/zuhri_id.py create")
        except: pass
    pause()

# ============================================================
# STEP 3 — APLIKASI
# ============================================================
def step_apps():
    clear()
    print(f"""
{BOLD}{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  LANGKAH 2 DARI 5 — APLIKASI YANG TERSEDIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

{BOLD}Ekosistem Zuhri punya 34 aplikasi. Ini yang utama:{RESET}

{GOLD}📡 P2P-MESH{RESET} — Jaringan Darurat
   Kirim pesan ke HP lain tanpa internet.

{GOLD}🆘 SOS-BEACON{RESET} — Sinyal Darurat
   Kirim sinyal SOS ke semua HP di sekitar.

{GOLD}🗳️ VOTE{RESET} — Voting Digital
   1 Zuhri ID = 1 Suara. Tidak bisa dicurangi.

{GOLD}📜 CONTRACT{RESET} — Kontrak Pintar
   Buat perjanjian digital yang tidak bisa diubah.

{GOLD}🛂 PASSPORT{RESET} — Identitas Lintas Negara
   Passport digital yang berlaku di mana saja.

{GOLD}🔐 CRYPTO{RESET} — Enkripsi Militer
   Enkripsi file dengan AES-256-GCM.

{GOLD}🌑 DARK-WEB{RESET} — Akses Anonim
   Akses .onion dengan Tor.

{GOLD}🧠 AI{RESET} — AI Pribadi
   Tanya AI tanpa internet.

{GOLD}🔍 VISION{RESET} — Deteksi Objek
   Deteksi objek dengan kamera HP.

{GOLD}💰 FINANCE{RESET} — Keuangan Mandiri
   Catat pemasukan & pengeluaran.

{GOLD}🎓 EDU{RESET} — Kursus & Sertifikat
   Belajar offline dengan AI tutor.

{GOLD}📚 LIBRARY{RESET} — Perpustakaan
   Baca buku & artikel offline.
""")
    pause()

# ============================================================
# STEP 4 — CARA PAKAI
# ============================================================
def step_howto():
    clear()
    print(f"""
{BOLD}{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  LANGKAH 3 DARI 5 — CARA MENGGUNAKAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

{BOLD}Ada 3 cara menggunakan Ekosistem Zuhri:{RESET}

{BOLD}{GOLD}CARA 1 — Menu Utama (Untuk Pemula){RESET}

  Ketik: {CYAN}ekosistem_zuhri{RESET}  atau  {CYAN}ez{RESET}

  Akan muncul menu dengan angka:
    {GOLD}1.{RESET} Zuhri ID
    {GOLD}2.{RESET} Passport
    {GOLD}3.{RESET} Enkripsi
    ... dst (34 fitur)

  Tinggal ketik angka, tidak perlu hafal perintah.

{BOLD}{GOLD}CARA 2 — Auto-Routing (Paling Cepat){RESET}

  Ketik: {CYAN}z <kata-kunci>{RESET}

  Contoh:
    {CYAN}z id{RESET}        → Zuhri ID
    {CYAN}z crypto{RESET}    → Enkripsi
    {CYAN}z mesh{RESET}      → P2P-Mesh
    {CYAN}z vote{RESET}      → Voting
    {CYAN}z list{RESET}      → Semua routes

{BOLD}{GOLD}CARA 3 — Perintah Langsung (Advanced){RESET}

  {CYAN}id{RESET}         → Zuhri ID
  {CYAN}crypto{RESET}     → Enkripsi
  {CYAN}mesh{RESET}       → P2P-Mesh
  {CYAN}vote{RESET}       → Voting
  {CYAN}finance{RESET}    → Keuangan
  {CYAN}docs{RESET}       → Dokumentasi
""")
    pause()

# ============================================================
# STEP 5 — KEAMANAN
# ============================================================
def step_safety():
    clear()
    print(f"""
{BOLD}{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  LANGKAH 4 DARI 5 — KEAMANAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

{BOLD}🔐 ATURAN KEAMANAN ZUHRI:{RESET}

{GREEN}✅ AMAN:{RESET}
  • Bagikan Zuhri ID Anda (public)
  • Bagikan Public Key Anda
  • Backup Private Key ke flashdisk
  • Simpan Private Key di HP

{RED}❌ JANGAN:{RESET}
  • Screenshot Private Key
  • Kirim Private Key via WhatsApp
  • Upload Private Key ke Google Drive
  • Copy Private Key ke Note Android
  • Tulis Private Key di chat

{BOLD}{YELLOW}INGAT:{RESET}
  Private Key = Kunci Rumah (jangan dibagikan)
  Public Key  = Alamat Rumah (boleh dibagikan)
""")
    pause()

# ============================================================
# STEP 6 — SELESAI
# ============================================================
def step_done():
    clear()
    identity = load_identity()
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        ✅ SELAMAT! ANDA SIAP MENGGUNAKAN EKOSISTEM ZUHRI        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    if identity:
        print(f"{GOLD}🆔 Zuhri ID Anda:{RESET}")
        print(f"   {BOLD}{identity['zuhri_id']}{RESET}")
        print(f"   Nama: {identity['name']}")
        print()
    
    print(f"""{BOLD}CARA MULAI:{RESET}

  {GOLD}1.{RESET} Ketik {CYAN}ekosistem_zuhri{RESET} untuk menu utama
  {GOLD}2.{RESET} Ketik {CYAN}z id{RESET} untuk Zuhri ID (cepat)
  {GOLD}3.{RESET} Ketik {CYAN}docs{RESET} untuk baca dokumentasi
  {GOLD}4.{RESET} Ketik {CYAN}z list{RESET} untuk lihat semua routes

{BOLD}DAFTAR LENGKAP PERINTAH:{RESET}

  {CYAN}ekosistem_zuhri{RESET}   → Menu utama (34 fitur)
  {CYAN}z <kata-kunci>{RESET}   → Auto-routing cepat
  {CYAN}id{RESET}               → Zuhri ID
  {CYAN}crypto{RESET}           → Enkripsi
  {CYAN}enkripsi{RESET}         → Enkripsi lengkap
  {CYAN}mesh{RESET}             → P2P-Mesh
  {CYAN}sos{RESET}              → Sinyal darurat
  {CYAN}vote{RESET}             → Voting
  {CYAN}contract{RESET}         → Kontrak
  {CYAN}finance{RESET}          → Keuangan
  {CYAN}edu{RESET}              → Kursus
  {CYAN}library{RESET}          → Perpustakaan
  {CYAN}kurikulum{RESET}        → 30 kurikulum
  {CYAN}chain{RESET}            → Blockchain
  {CYAN}did{RESET}              → DID
  {CYAN}botnet{RESET}           → Botnet Hunter
  {CYAN}spiritual{RESET}        → Fatwa Kehidupan
  {CYAN}peringatan{RESET}       → Bencana
  {CYAN}backup{RESET}           → Backup
  {CYAN}restore{RESET}          → Restore
  {CYAN}docs{RESET}             → Dokumentasi
  {CYAN}health{RESET}           → Cek sistem

{BOLD}{GREEN}Semua fitur ini GRATIS dan OFFLINE.{RESET}
{BOLD}{GREEN}Tidak butuh internet. Tidak butuh server.{RESET}
""")
    
    # Tandai selesai
    os.makedirs(os.path.dirname(os.path.join(HOME, "zuhri_os", "onboarding", ".completed")), exist_ok=True)
    open(os.path.join(HOME, "zuhri_os", "onboarding", ".completed"), "w").write("done")
    
    pause("Tekan Enter untuk selesai...")

# ============================================================
# MAIN
# ============================================================
def main():
    step_welcome()
    step_id()
    step_apps()
    step_howto()
    step_safety()
    step_done()
    
    clear()
    print(f"""
{BOLD}{GREEN}✅ ONBOARDING SELESAI!{RESET}

{BOLD}Selamat menjelajahi Ekosistem Zuhri,{RESET}
{BOLD}{GOLD}Operator Baru!{RESET}

Ketik {CYAN}ekosistem_zuhri{RESET} untuk mulai.
""")

if __name__ == "__main__":
    main()
