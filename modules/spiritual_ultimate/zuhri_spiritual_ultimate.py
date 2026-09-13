#!/usr/bin/env python3
"""
ZUHRI SPIRITUAL ULTIMATE — PENGINGAT KEBESARAN TUHAN
Bukan simulasi penciptaan — ini media muhasabah & dzikir
"""

import os, sys, json, time, random
from datetime import datetime

HOME = os.path.expanduser("~")
SPIR_DIR = os.path.join(HOME, "zuhri_os", "spiritual_ultimate")
DATA_DIR = os.path.join(SPIR_DIR, "data")
LOG_DIR = os.path.join(SPIR_DIR, "logs")
DZIKIR_DIR = os.path.join(SPIR_DIR, "dzikir")
for d in [DATA_DIR, LOG_DIR, DZIKIR_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

def clear(): os.system('clear')

def pause():
    input(f"\n{DIM}━━━ Tekan Enter untuk lanjut ━━━{RESET}\n")

# ============================================================
# MODUL 1 — SKALA ALAM SEMESTA
# ============================================================
def skala_alam():
    clear()
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  🌌 SKALA ALAM SEMESTA — MENGAGUMI KEBESARAN ALLAH                  ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📏 SKALA UKURAN (meter):{RESET}

  {DIM}10⁻¹⁵ m{RESET}  → Partikel subatomik (proton)
  {DIM}10⁻¹⁰ m{RESET}  → Atom
  {DIM}10⁻⁹ m{RESET}   → Molekul DNA
  {DIM}10⁻⁶ m{RESET}   → Bakteri
  {DIM}10⁻³ m{RESET}   → Sarang semut
  {DIM}10⁰ m{RESET}    → Manusia
  {DIM}10³ m{RESET}    → Gunung Everest (8.848 m)
  {DIM}10⁵ m{RESET}    → Atmosfer bumi
  {DIM}10⁷ m{RESET}    → Bumi (diameter 12.742 km)
  {DIM}10⁸ m{RESET}    → Jarak Bumi-Bulan (384.400 km)
  {DIM}10⁹ m{RESET}    → Matahari (diameter 1,39 juta km)
  {DIM}10¹² m{RESET}   → Tata Surya (Pluto)
  {DIM}10¹⁶ m{RESET}   → 1 tahun cahaya
  {DIM}10¹⁷ m{RESET}   → Bintang terdekat (Proxima Centauri)
  {DIM}10²¹ m{RESET}   → Galaksi Bima Sakti (100.000 tahun cahaya)
  {DIM}10²³ m{RESET}   → Jarak ke Andromeda
  {DIM}10²⁶ m{RESET}   → Alam semesta teramati (93 miliar tahun cahaya)

{BOLD}{GOLD}📖 RENUNGAN:{RESET}

  {CYAN}"Dan langit itu Kami bangun dengan kekuasaan (Kami),
  dan sesungguhnya Kami benar-benar meluaskannya."
  (QS. Adz-Dzariyat: 47){RESET}

  {DIM}Betapa kecilnya kita di hadapan Allah.{RESET}
  {DIM}Dari atom hingga alam semesta — semua atas kehendak-Nya.{RESET}
""")
    pause()

# ============================================================
# MODUL 2 — STRUKTUR LANGIT (7 LANGIT)
# ============================================================
def tujuh_langit():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🌌 7 LANGIT — DALAM AL-QURAN & SAINS                               ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📖 DALAM AL-QURAN:{RESET}

  {GOLD}1.{RESET} QS. Al-Baqarah: 29
     "Kemudian Dia menuju langit dan langit itu masih berupa asap..."
  
  {GOLD}2.{RESET} QS. Al-Mulk: 3
     "Yang menciptakan tujuh langit berlapis-lapis..."
  
  {GOLD}3.{RESET} QS. Nuh: 15
     "Tidakkah kamu melihat bagaimana Allah menciptakan tujuh langit berlapis-lapis?"

{BOLD}🌌 DALAM SAINS (Kemungkinan Tafsir):{RESET}

  {DIM}Lapisan 1:{RESET} Troposfer (0-12 km)
  {DIM}Lapisan 2:{RESET} Stratosfer (12-50 km)
  {DIM}Lapisan 3:{RESET} Mesosfer (50-85 km)
  {DIM}Lapisan 4:{RESET} Termosfer (85-600 km)
  {DIM}Lapisan 5:{RESET} Eksosfer (600+ km)
  {DIM}Lapisan 6:{RESET} Magnetosfer
  {DIM}Lapisan 7:{RESET} Heliosfer

{BOLD}{GOLD}⚠️  CATATAN:{RESET}
  {DIM}Tafsir sains atas "7 langit" masih dipelajari.{RESET}
  {DIM}Yang jelas: Allah menciptakan berlapis-lapis.{RESET}
  {DIM}Manusia hanya diberi sedikit ilmu (QS. Al-Isra: 85).{RESET}
""")
    pause()

# ============================================================
# MODUL 3 — AYAT QURAN TENTANG ALAM
# ============================================================
def ayat_alam():
    clear()
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  📖 AYAT QURAN TENTANG ALAM SEMESTA                                 ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    ayat = [
        ("Langit & Bumi", "Dan langit itu Kami bangun dengan kekuasaan (Kami), dan sesungguhnya Kami benar-benar meluaskannya.", "QS. Adz-Dzariyat: 47"),
        ("Bintang & Planet", "Dan Dialah yang menjadikan bintang-bintang bagimu, agar kamu menjadikannya petunjuk dalam kegelapan di darat dan di laut.", "QS. Al-An'am: 97"),
        ("Gunung", "Dan gunung-gunung dipancangkan dengan teguh.", "QS. An-Naba: 7"),
        ("Laut", "Dan Dialah yang membiarkan dua laut mengalir (berdampingan); yang ini tawar lagi segar dan yang lain asin lagi pahit.", "QS. Al-Furqan: 53"),
        ("Tumbuhan", "Dan Kami turunkan air dari langit, lalu Kami tumbuhkan padanya segala macam tumbuh-tumbuhan yang baik.", "QS. Thaha: 53"),
        ("Hewan", "Dan pada penciptaan kamu dan pada binatang-binatang yang melata yang bertebaran (di muka bumi) terdapat tanda-tanda (kekuasaan Allah) untuk kaum yang meyakini.", "QS. Al-Jatsiyah: 4"),
        ("Matahari & Bulan", "Matahari dan bulan (beredar) menurut perhitungan.", "QS. Ar-Rahman: 5"),
        ("Angin", "Dan Dialah yang meniupkan angin (sebagai) pembawa kabar gembira dekat sebelum kedatangan rahmat-Nya.", "QS. Al-Furqan: 48"),
        ("Hujan", "Dan Dialah yang menurunkan hujan setelah mereka berputus asa, dan Dia menyebarkan rahmat-Nya.", "QS. Asy-Syura: 28"),
        ("Malam & Siang", "Dan Dialah yang menjadikan malam dan siang silih berganti bagi orang yang ingin mengambil pelajaran.", "QS. Al-Furqan: 62"),
    ]
    
    for i, (judul, isi, sumber) in enumerate(ayat, 1):
        print(f"{GOLD}{i}. {judul}{RESET}")
        print(f"   {CYAN}\"{isi}\"{RESET}")
        print(f"   {DIM}({sumber}){RESET}\n")
    
    pause()

# ============================================================
# MODUL 4 — HADITS PILIHAN
# ============================================================
def hadits():
    clear()
    print(f"""
{BOLD}{GREEN}╔══════════════════════════════════════════════════════════════════════╗
║  📖 HADITS TENTANG KEBESARAN ALLAH                                   ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    hadits_list = [
        ("Keindahan", "Sesungguhnya Allah itu indah dan mencintai keindahan.", "HR. Muslim"),
        ("Kebesaran", "Allah itu Maha Besar, dan tidak ada yang lebih besar dari-Nya.", "HR. Bukhari"),
        ("Kasih Sayang", "Sesungguhnya Allah itu Maha Pengasih lagi Maha Penyayang.", "HR. Tirmidzi"),
        ("Taqwa", "Sesungguhnya Allah tidak melihat bentuk dan harta kalian, tetapi Dia melihat hati dan amal kalian.", "HR. Muslim"),
        ("Zikir", "Barangsiapa berzikir kepada-Ku dalam dirinya, maka Aku akan berzikir kepadanya dalam diri-Ku.", "HR. Bukhari"),
        ("Syukur", "Barangsiapa tidak bersyukur kepada manusia, maka dia tidak bersyukur kepada Allah.", "HR. Ahmad"),
        ("Sabda", "Sebaik-baik manusia adalah yang paling bermanfaat bagi manusia lain.", "HR. Ahmad"),
        ("Akhlaq", "Sesungguhnya aku diutus untuk menyempurnakan akhlak.", "HR. Ahmad"),
    ]
    
    for i, (judul, isi, sumber) in enumerate(hadits_list, 1):
        print(f"{GOLD}{i}. {judul}{RESET}")
        print(f"   {CYAN}\"{isi}\"{RESET}")
        print(f"   {DIM}({sumber}){RESET}\n")
    
    pause()

# ============================================================
# MODUL 5 — ASMAUL HUSNA
# ============================================================
def asmaul_husna():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🕌 ASMAUL HUSNA — 99 NAMA ALLAH (PILIHAN)                          ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    asma = [
        ("Ar-Rahman", "Maha Pengasih"),
        ("Ar-Rahim", "Maha Penyayang"),
        ("Al-Malik", "Maha Raja"),
        ("Al-Quddus", "Maha Suci"),
        ("As-Salam", "Maha Pemberi Kesejahteraan"),
        ("Al-Mu'min", "Maha Pemberi Keamanan"),
        ("Al-'Aziz", "Maha Perkasa"),
        ("Al-Jabbar", "Maha Memaksa"),
        ("Al-Mutakabbir", "Maha Megah"),
        ("Al-Khaliq", "Maha Pencipta"),
        ("Al-Bari'", "Maha Mengadakan"),
        ("Al-Mushawwir", "Maha Membentuk Rupa"),
        ("Al-Ghaffar", "Maha Pengampun"),
        ("Al-Qahhar", "Maha Menundukkan"),
        ("Al-Wahhab", "Maha Pemberi Karunia"),
        ("Ar-Razzaq", "Maha Pemberi Rezeki"),
        ("Al-Fattah", "Maha Pembuka Rahmat"),
        ("Al-'Alim", "Maha Mengetahui"),
        ("Al-Hayy", "Maha Hidup"),
        ("Al-Qayyum", "Maha Berdiri Sendiri"),
    ]
    
    for i, (arab, arti) in enumerate(asma, 1):
        print(f"  {GOLD}{i:2}.{RESET} {BOLD}{arab:15}{RESET} → {CYAN}{arti}{RESET}")
    
    print(f"\n{DIM}... dan 79 nama lainnya.{RESET}")
    print(f"{DIM}Baca lengkap: https://id.wikipedia.org/wiki/Asmaul_Husna{RESET}\n")
    pause()

# ============================================================
# MODUL 6 — DZIKIR HARIAN
# ============================================================
def dzikir_harian():
    clear()
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  📿 DZIKIR HARIAN — PAGI, SORE, MALAM                               ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}{GOLD}🌅 DZIKIR PAGI:{RESET}

  {GOLD}1.{RESET} Subhanallah wa bihamdihi (100x)
  {GOLD}2.{RESET} La ilaha illallah wahdahu la syarika lah (10x)
  {GOLD}3.{RESET} Ayat Kursi (1x)
  {GOLD}4.{RESET} Al-Ikhlas, Al-Falaq, An-Nas (3x)

{BOLD}{GOLD}🌇 DZIKIR SORE:{RESET}

  {GOLD}1.{RESET} Subhanallah wa bihamdihi (100x)
  {GOLD}2.{RESET} Astaghfirullah wa atubu ilaih (100x)
  {GOLD}3.{RESET} Ayat Kursi (1x)
  {GOLD}4.{RESET} Al-Ikhlas, Al-Falaq, An-Nas (3x)

{BOLD}{GOLD}🌙 DZIKIR MALAM:{RESET}

  {GOLD}1.{RESET} Ayat Kursi (1x)
  {GOLD}2.{RESET} Al-Ikhlas, Al-Falaq, An-Nas (3x)
  {GOLD}3.{RESET} Subhanallah (33x), Alhamdulillah (33x), Allahu Akbar (34x)
  {GOLD}4.{RESET} Doa sebelum tidur

{BOLD}📖 DALIL:{RESET}
  {CYAN}"Ingatlah, hanya dengan mengingat Allah hati menjadi tenang."
  (QS. Ar-Ra'd: 28){RESET}
""")
    pause()

# ============================================================
# MODUL 7 — MUHASABAH
# ============================================================
def muhasabah():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🤲 MUHASABAH — INTROSPEKSI DIRI                                    ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}📋 RENUNGKAN (jawab dalam hati):{RESET}

  {GOLD}1.{RESET} Berapa banyak nikmat Allah hari ini?
     {DIM}(Napas, kesehatan, keluarga, rezeki){RESET}

  {GOLD}2.{RESET} Apa yang sudah disyukuri?
     {DIM}(Tulis di catatan){RESET}

  {GOLD}3.{RESET} Apa yang perlu diperbaiki?
     {DIM}(Sholat, sedekah, akhlak){RESET}

  {GOLD}4.{RESET} Apa target ibadah esok hari?
     {DIM}(Tilawah, dzikir, sedekah){RESET}

  {GOLD}5.{RESET} Sudahkah memaafkan orang lain?
     {DIM}(Termasuk diri sendiri){RESET}

{BOLD}📖 AYAT:{RESET}
  {CYAN}"Hai orang-orang yang beriman, bertakwalah kepada Allah
  dan hendaklah setiap diri memperhatikan apa yang telah
  diperbuatnya untuk hari esok."
  (QS. Al-Hasyr: 18){RESET}

{BOLD}✍️  CATATAN MUHASABAH:{RESET}
""")
    
    catatan = input("📝 Tulis muhasabah Anda: ").strip()
    if catatan:
        f = os.path.join(DATA_DIR, f"muhasabah_{datetime.now().strftime('%Y%m%d')}.txt")
        with open(f, "a") as fp:
            fp.write(f"\n[{datetime.now().strftime('%H:%M:%S')}] {catatan}\n")
        print(f"\n{GREEN}✅ Tersimpan: {f}{RESET}\n")
    
    pause()

# ============================================================
# MODUL 8 — KITAB IRFANI (RUJUKAN)
# ============================================================
def kitab_irfani():
    clear()
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  📚 KITAB IRFANI — RUJUKAN TASAWUF                                 ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}⚠️  CATATAN:{RESET}
  {DIM}Ini hanya daftar rujukan. Untuk pemahaman mendalam,${RESET}
  {DIM}wajib berguru pada ulama yang mu'tabar.${RESET}

{BOLD}📖 KITAB KLASIK TASAWUF:{RESET}

  {GOLD}1.{RESET} Ihya' Ulumuddin — Imam Al-Ghazali
     {DIM}Ringkasan: Menghidupkan ilmu agama${RESET}

  {GOLD}2.{RESET} Risalah Qusyairiyah — Imam Al-Qusyairi
     {DIM}Ringkasan: Prinsip-prinsip tasawuf${RESET}

  {GOLD}3.{RESET} Al-Hikam — Ibnu Atha'illah
     {DIM}Ringkasan: Hikmah-hikmah spiritual${RESET}

  {GOLD}4.{RESET} Futuhul Ghaib — Syaikh Abdul Qadir Al-Jailani
     {DIM}Ringkasan: Rahasia-rahasia spiritual${RESET}

  {GOLD}5.{RESET} Kimiya'us Sa'adah — Imam Al-Ghazali
     {DIM}Ringkasan: Kimia kebahagiaan${RESET}

{BOLD}📖 KITAB IBNU ARABI (KONTROVERSIAL — RUJUK ULAMA):{RESET}

  {GOLD}•{RESET} Futuhat Al-Makkiyyah
  {GOLD}•{RESET} Fusus Al-Hikam
     {DIM}⚠️  Perlu bimbingan guru${RESET}

{BOLD}📖 KITAB TASAWUF MODERN:{RESET}

  {GOLD}•{RESET} Mengenal Tasawuf — Dr. Abdul Halim Mahmud
  {GOLD}•{RESET} Sufi Modern — Dr. Said Hawwa

{BOLD}⚠️  ADAB PEMBACA:{RESET}
  {GOLD}1.{RESET} Niat untuk mendekat kepada Allah
  {GOLD}2.{RESET} Dengan bimbingan guru
  {GOLD}3.{RESET} Tidak mencampur aduk syariat
  {GOLD}4.{RESET} Diskusi dengan ahlinya
""")
    pause()

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        clear()
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🕌 ZUHRI SPIRITUAL ULTIMATE — PENGINGAT KEBESARAN TUHAN           ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Bukan simulasi penciptaan — media muhasabah & dzikir              ║
║  Waktu: {GOLD}{datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}{RESET}
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🌌 Skala Alam Semesta
  {GOLD}2.{RESET}  🌌 7 Langit (Quran & Sains)
  {GOLD}3.{RESET}  📖 Ayat Quran tentang Alam
  {GOLD}4.{RESET}  📖 Hadits Pilihan
  {GOLD}5.{RESET}  🕌 Asmaul Husna
  {GOLD}6.{RESET}  📿 Dzikir Harian
  {GOLD}7.{RESET}  🤲 Muhasabah
  {GOLD}8.{RESET}  📚 Kitab Irfani (Rujukan)
  {GOLD}9.{RESET}  ℹ️  Info & Adab
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-9): {RESET}").strip()
            if c == "0": break
            elif c == "1": skala_alam()
            elif c == "2": tujuh_langit()
            elif c == "3": ayat_alam()
            elif c == "4": hadits()
            elif c == "5": asmaul_husna()
            elif c == "6": dzikir_harian()
            elif c == "7": muhasabah()
            elif c == "8": kitab_irfani()
            elif c == "9":
                clear()
                print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  ℹ️  INFO & ADAB                                                     ║
╚══════════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}🎯 TUJUAN:{RESET}
  Mengingat kebesaran Allah melalui:
  {GOLD}•{RESET} Renungan alam semesta
  {GOLD}•{RESET} Ayat & Hadits
  {GOLD}•{RESET} Dzikir & Muhasabah

{BOLD}📖 DALIL UTAMA:{RESET}
  {CYAN}"Kami akan memperlihatkan kepada mereka tanda-tanda
  (kebesaran) Kami di segenap penjuru dan pada diri mereka
  sendiri, sehingga jelaslah bagi mereka bahwa Al-Quran itu
  adalah benar."
  (QS. Fussilat: 53){RESET}

{BOLD}⚠️  ADAB:{RESET}
  {GOLD}1.{RESET} Niat untuk mengingat Allah
  {GOLD}2.{RESET} Tidak mencampur aduk akidah
  {GOLD}3.{RESET} Rujuk ulama untuk pemahaman
  {GOLD}4.{RESET} Tidak menafsir tanpa ilmu
  {GOLD}5.{RESET} Berdoa setelah membaca

{BOLD}🚫 TIDAK UNTUK:{RESET}
  {RED}❌{RESET} Simulasi penciptaan makhluk
  {RED}❌{RESET} "Menjadi" Tuhan
  {RED}❌{RESET} Tafsir tanpa ilmu
  {RED}❌{RESET} Campur aduk kitab suci

{BOLD}✅ UNTUK:{RESET}
  {GREEN}✅{RESET} Muhasabah
  {GREEN}✅{RESET} Dzikir
  {GREEN}✅{RESET} Tadabbur alam
  {GREEN}✅{RESET} Pengingat harian
""")
                pause()
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "dzikir": dzikir_harian()
        elif cmd == "muhasabah": muhasabah()
        elif cmd == "info":
            print("Zuhri Spiritual Ultimate — Pengingat Kebesaran Tuhan")
        else: menu()
    else: menu()
