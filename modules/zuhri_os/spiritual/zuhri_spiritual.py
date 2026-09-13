


def baca_halaman(pdf_path, nama):
    """Baca PDF hybrid: teks + gambar"""
    try:
        import pdfplumber
        HAS_PLUMBER = True
    except ImportError:
        HAS_PLUMBER = False
    
    try:
        import PyPDF2
        HAS_PYPDF = True
    except ImportError:
        HAS_PYPDF = False
    
    if not HAS_PLUMBER and not HAS_PYPDF:
        print(f"{RED}❌ Install: pip install pdfplumber PyPDF2{RESET}")
        input(f"{DIM}Enter...{RESET}")
        return
    
    try:
        # Hitung total halaman
        if HAS_PLUMBER:
            with pdfplumber.open(pdf_path) as pdf:
                total = len(pdf.pages)
        else:
            with open(pdf_path, 'rb') as f:
                total = len(PyPDF2.PdfReader(f).pages)
        
        page = 1
        while True:
            os.system('clear')
            print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  📖 {nama[:50]}
║  Halaman {page}/{total}
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
            
            # Extract text
            text = ""
            try:
                if HAS_PLUMBER:
                    with pdfplumber.open(pdf_path) as pdf:
                        text = pdf.pages[page-1].extract_text() or ""
                else:
                    with open(pdf_path, 'rb') as f:
                        text = PyPDF2.PdfReader(f).pages[page-1].extract_text() or ""
            except: pass
            
            if text.strip():
                # Ada teks
                print(text[:3000])
                if len(text) > 3000:
                    print(f"\n{DIM}... (teks dipotong di 3000 karakter){RESET}")
            else:
                # Halaman gambar → extract jadi PNG
                print(f"{YELLOW}⚠️  Halaman ini berisi GAMBAR.{RESET}\n")
                print(f"{CYAN}🖼️  Mengekstrak gambar...{RESET}\n")
                
                # Extract pakai mutool
                img_path = f"/sdcard/Download/zuhri_page_{page}.png"
                result = subprocess.run(
                    ["mutool", "draw", "-o", img_path, "-r", "150", pdf_path, str(page)],
                    capture_output=True, text=True
                )
                
                if os.path.exists(img_path):
                    print(f"{GREEN}✅ Gambar tersimpan: {img_path}{RESET}\n")
                    print(f"{GOLD}Membuka di HP...{RESET}\n")
                    os.system(f"termux-open '{img_path}' 2>/dev/null")
                else:
                    print(f"{RED}❌ Gagal extract gambar{RESET}")
                    print(f"{DIM}Pastikan mutool terinstall: pkg install mutool{RESET}\n")
            
            print(f"\n{DIM}{'─'*60}{RESET}")
            print(f"{GOLD}[n]ext [p]rev [g]oto [r]efresh [o]pen-pdf [q]uit{RESET}")
            
            try:
                aksi = input(f"{CYAN}➜ {RESET}").strip().lower()
                if aksi in ["q","quit"]: break
                elif aksi in ["n","next"] and page < total: page += 1
                elif aksi in ["p","prev"] and page > 1: page -= 1
                elif aksi in ["r","refresh"]:
                    continue
                elif aksi in ["o","open","open-pdf"]:
                    # Buka PDF langsung di PDF Reader HP
                    print(f"\n{CYAN}📱 Membuka PDF di aplikasi HP...{RESET}")
                    os.system(f"termux-open '{pdf_path}' 2>/dev/null")
                    input(f"{DIM}Enter...{RESET}")
                elif aksi.startswith("g"):
                    try:
                        num = int(aksi.replace("g","").strip() or input("Halaman: "))
                        if 1 <= num <= total: page = num
                    except: pass
            except KeyboardInterrupt: break
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}")
        input(f"{DIM}Enter...{RESET}")







#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI SPIRITUAL — FATWA KEHIDUPAN & YOLHAN WIJAYA
Halaman + Buku PDF + AI Generate Offline
"""

import os, sys, subprocess, json, shutil
from datetime import datetime

HOME = os.path.expanduser("~")
SPIR_DIR = os.path.join(HOME, "zuhri_os", "spiritual")
DATA_DIR = os.path.join(SPIR_DIR, "data")
BOOKS_DIR = os.path.join(SPIR_DIR, "books")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BOOKS_DIR, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

# ===== KONTEN ASLI =====
AJARAN = {
    "allah": {
        "judul": "Tentang Allah — Ketiadaan Diri",
        "konten": """Yang disebut Allah itu sebenarnya adalah kekosongan diri pribadi, bukan Allah sebagaimana diangan angankan orang2, Allah seperti itu tidaklah ada.

Dalam kekosongan kita itu artinya kita ada dalam keadaan tanpa mendengar, tanpa melihat, tanpa suara, tanpa tahu, tanpa perasaan, tanpa rasa. Maka kekosongan itu menghisap kita kedalam ketiadaan diri, ketiadaan keakuan. dalam ketiadaan keakuan diri itulah lalu Allah menjadi ada/nyata.

Ketiadaanmu adalah adanya Allah. Seperti dua sisi yang berbolak balik, saat engkau ada, Allah menjadi tidak ada, saat engkau tidak ada, Allah menjadi ada."""
    },
    "multitasking": {
        "judul": "Multi-Tasking & Dua Alam",
        "konten": """Sekarang cobalah memikirkan 1 kata dibenakmu, misalnya "semut"....
Terus camkan kata "semut" itu dibenakmu....
Kalau sudah, mulailah memikirkan kata2 lain lagi....
Tapi tanpa kehilangan kata "semut" dibenakmu....
Kalau kamu bisa.... Itu disebut kemampuan "multi tasking"...

Kita bisa hidup di dua alam, yaitu ruhaniah dan jasmaniah secara sekaligus...."""
    },
    "pengaruh": {
        "judul": "Pengaruh Ruhani — Nurani Akan Menang",
        "konten": """Akan saya jelaskan bagaimana seorang Fatwa Kehidupan bisa merubah dan mempengaruhi satu negara ini........ Saya tidak perlu menjadi seorang Presiden secara de jure, utk merubah bangsa ini.......

Nurani akan menang, kerakusan akan hancur, kugulung habis......... Jaa'al haqqo wazahaqol batilu, innal batila kana zahuqo....."""
    },
    "identitas": {
        "judul": "Tentang Identitas — Nama & Ruh",
        "konten": """Nama asli saya adalah Yolhan Wijaya, ST...... Nama pemberian guruku adalah Muhammad Zuhri, dan nama akun saya adalah fatwa kehidupan.....

Semuanya adalah nama2 saya...... Namun ruhku tidak bernama dan bersebut lagi......"""
    },
    "perjalanan": {
        "judul": "Perjalanan Hidup",
        "konten": """Awalnya saya bikin akun facebook hanya mengisi waktu luang, Kadang ngobrol sana sini di grup, Sapa sana sini, umumnya orang orang saja, lalu saya mulai mengajar karena ada yg minta diajari...

Lalu saya buka padepokan online, dengan nama padepokan kebodohan fatwa kehidupan...

Karena murid murid saya makin tidak terhitung, saya kuwalahan dan mulai mengangkat 4 letnan membantu tugas saya, karna niatan bertemu dan belajar langsung dgn saya sangat banyak, maka saya bikin padepokan jabung paramitapura, di dunia nyata...

Itulah sejarahnya, sampai hari ini, episodenya sedang sampai disini..."""
    },
    "nurani": {
        "judul": "Tentang Nurani",
        "konten": """Nurani akan menang, kerakusan akan hancur. Mata rantai ilmu yang diajarkan akan bekerja otomatis, mengubah banyak orang tanpa perlu kekuasaan de jure."""
    },
    "sabar": {
        "judul": "Tentang Sabar",
        "konten": """Sabar adalah kunci. Dalam kesabaran, kita menemukan kekuatan sejati. Sabar bukan pasrah, tapi menerima dengan penuh kesadaran."""
    },
    "kesadaran": {
        "judul": "Tentang Kesadaran",
        "konten": """Kesadaran sejati adalah ketika engkau menyadari bahwa 'aku' tidak ada, dan yang ada hanyalah Allah. Dalam ketiadaan keakuan, kita menemukan kehadiran-Nya."""
    }
}

# ===== AI GENERATE =====
def ai_generate(pertanyaan):
    konteks = "\n\n".join([f"### {a['judul']}\n{a['konten']}" for a in AJARAN.values()])
    
    prompt = f"""Kamu asisten spiritual Fatwa Kehidupan, ajaran Syekh Muhammad Zuhri (Yolhan Wijaya).

KONTEKS:
{konteks}

PERTANYAAN: {pertanyaan}

Jawab Bahasa Indonesia, mengacu ajaran Fatwa Kehidupan. Maks 300 kata."""

    try:
        result = subprocess.run(["ollama","run","phi",prompt], capture_output=True, text=True, timeout=120)
        return result.stdout if result.stdout else "Maaf, jawaban tidak tersedia."
    except:
        return "AI timeout. Coba lagi."

# ===== PDF READER =====
def list_books():
    """Daftar buku PDF"""
    books = [f for f in os.listdir(BOOKS_DIR) if f.lower().endswith('.pdf')]
    return books

def baca_pdf():
    """Baca buku PDF"""
    books = list_books()
    
    if not books:
        print(f"\n{YELLOW}⚠️  Belum ada buku PDF.{RESET}")
        print(f"{DIM}Import dulu: pilih menu 9{RESET}\n")
        return
    
    print(f"\n{BOLD}{CYAN}📚 DAFTAR BUKU PDF:{RESET}\n")
    for i, b in enumerate(books, 1):
        size = os.path.getsize(os.path.join(BOOKS_DIR, b)) / 1024
        print(f"  {GOLD}{i}.{RESET} {b} {DIM}({size:.1f} KB){RESET}")
    
    try:
        c = int(input(f"\n{CYAN}Pilih buku: {RESET}")) - 1
        if not (0 <= c < len(books)):
            return
        
        pdf_path = os.path.join(BOOKS_DIR, books[c])
        baca_halaman(pdf_path, books[c])
    except:
        pass

def baca_halaman(pdf_path, nama):
    """Baca PDF per halaman"""
    try:
        import PyPDF2
    except ImportError:
        print(f"{RED}❌ PyPDF2 tidak terinstall{RESET}")
        print(f"{DIM}Install: pip install PyPDF2{RESET}")
        return
    
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            total = len(reader.pages)
        
        page = 1
        while True:
            os.system('clear')
            print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  📖 {nama[:50]}
║  Halaman {page}/{total}
╚══════════════════════════════════════════════════════════════════╝{RESET}

""")
            
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = reader.pages[page-1].extract_text()
                print(text[:3000] if text else f"{DIM}(Halaman kosong / gambar){RESET}")
            
            print(f"\n{DIM}{'─'*60}{RESET}")
            print(f"{GOLD}[n]ext [p]rev [g]oto [q]uit{RESET}")
            
            try:
                aksi = input(f"{CYAN}➜ {RESET}").strip().lower()
                if aksi in ["q", "quit"]: break
                elif aksi in ["n", "next"] and page < total: page += 1
                elif aksi in ["p", "prev"] and page > 1: page -= 1
                elif aksi.startswith("g"):
                    try:
                        num = int(aksi.replace("g", "").strip() or input("Halaman: "))
                        if 1 <= num <= total: page = num
                    except: pass
            except KeyboardInterrupt:
                break
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}")
        input(f"{DIM}Enter...{RESET}")

def import_pdf():
    """Import PDF ke library"""
    print(f"\n{BOLD}{CYAN}📥 IMPORT BUKU PDF{RESET}\n")
    path = input("📂 Path file PDF: ").strip()
    
    if not os.path.exists(path):
        print(f"{RED}❌ File tidak ditemukan{RESET}")
        return
    
    if not path.lower().endswith('.pdf'):
        print(f"{RED}❌ Harus file PDF{RESET}")
        return
    
    dest = os.path.join(BOOKS_DIR, os.path.basename(path))
    try:
        shutil.copy2(path, dest)
        print(f"\n{GREEN}✅ Buku di-import: {os.path.basename(path)}{RESET}")
        print(f"   Lokasi: {dest}\n")
    except Exception as e:
        print(f"{RED}❌ Gagal: {e}{RESET}")

# ===== CARI =====
def cari(query):
    query = query.lower()
    results = []
    for key, data in AJARAN.items():
        if query in key or query in data['judul'].lower() or query in data['konten'].lower():
            results.append(data)
    
    # Cari di PDF juga
    for b in list_books():
        try:
            import PyPDF2
            with open(os.path.join(BOOKS_DIR, b), 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text and query in text.lower():
                        results.append({"judul": f"📄 {b} — Hal {i+1}", "konten": text[:500]})
                        break
        except: pass
    
    return results

# ===== MENU =====
def menu():
    while True:
        os.system('clear')
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🕌 ZUHRI SPIRITUAL — FATWA KEHIDUPAN                          ║
║  ──────────────────────────────────────────────────────────────  ║
║  Yolhan Wijaya (Syekh Muhammad Zuhri)                          ║
║  📿 Ilmu Hati • Kesufian • Ketiadaan Diri                      ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  🌐 HALAMAN FACEBOOK:{RESET}
  {GOLD}1.{RESET}  👤 Buka Halaman Yolhan Wijaya
  {GOLD}2.{RESET}  🕌 Buka Halaman Fatwa Kehidupan

{BOLD}  📚 BUKU & AJARAN:{RESET}
  {GOLD}3.{RESET}  📖 Baca Buku PDF
  {GOLD}4.{RESET}  📥 Import Buku PDF
  {GOLD}5.{RESET}  📋 Daftar Buku PDF
  {GOLD}6.{RESET}  💬 Tanya AI (Fatwa Kehidupan)
  {GOLD}7.{RESET}  🔍 Cari Ajaran / Buku
  {GOLD}8.{RESET}  📖 Semua Ajaran Inti
  {GOLD}9.{RESET}  👤 Tentang Yolhan Wijaya
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-9): {RESET}").strip()
            
            if c == "0": break
            elif c == "1":
                print(f"\n{CYAN}🌐 Membuka halaman Yolhan Wijaya...{RESET}")
                os.system("termux-open-url 'https://www.facebook.com/yolhan.wijaya' 2>/dev/null")
                input(f"{DIM}Enter...{RESET}")
            elif c == "2":
                print(f"\n{CYAN}🌐 Membuka halaman Fatwa Kehidupan...{RESET}")
                os.system("termux-open-url 'https://www.facebook.com/fatwa.kehidupan' 2>/dev/null")
                input(f"{DIM}Enter...{RESET}")
            elif c == "3":
                baca_pdf()
            elif c == "4":
                import_pdf()
                input(f"{DIM}Enter...{RESET}")
            elif c == "5":
                books = list_books()
                print(f"\n{BOLD}{CYAN}📚 BUKU PDF ({len(books)}){RESET}\n")
                if books:
                    for i, b in enumerate(books, 1):
                        size = os.path.getsize(os.path.join(BOOKS_DIR, b)) / 1024
                        print(f"  {GOLD}{i}.{RESET} {b} {DIM}({size:.1f} KB){RESET}")
                else:
                    print(f"{YELLOW}Belum ada buku.{RESET}")
                input(f"\n{DIM}Enter...{RESET}")
            elif c == "6":
                q = input(f"\n{CYAN}💬 Pertanyaan: {RESET}").strip()
                if q:
                    print(f"\n{YELLOW}⏳ Mencari jawaban...{RESET}\n")
                    jawab = ai_generate(q)
                    print(f"{GREEN}🕌 Fatwa Kehidupan:{RESET}\n{jawab}\n")
                input(f"{DIM}Enter...{RESET}")
            elif c == "7":
                q = input(f"\n{CYAN}🔍 Kata kunci: {RESET}").strip()
                results = cari(q)
                if results:
                    for r in results[:5]:
                        print(f"\n{BOLD}{GOLD}📖 {r['judul']}{RESET}\n{r['konten'][:1000]}\n")
                else:
                    print(f"\n{YELLOW}⚠️  Tidak ditemukan.{RESET}\n")
                input(f"{DIM}Enter...{RESET}")
            elif c == "8":
                os.system('clear')
                for key, data in AJARAN.items():
                    print(f"\n{BOLD}{GOLD}▸ {data['judul']}{RESET}\n{data['konten']}\n{DIM}{'─'*60}{RESET}")
                input(f"\n{DIM}Enter...{RESET}")
            elif c == "9":
                os.system('clear')
                print(f"""
{BOLD}{MAGENTA}👤 YOLHAN WIJAYA (SYEKH MUHAMMAD ZUHRI){RESET}

{GOLD}Nama Asli:{RESET} Yolhan Wijaya, ST
{GOLD}Nama Pemberian Guru:{RESET} Muhammad Zuhri
{GOLD}Facebook:{RESET} fatwa.kehidupan

{BOLD}Perjalanan:{RESET}
- Aktif di Facebook sejak 2012
- Padepokan Kebodohan Fatwa Kehidupan (online)
- Padepokan Jabung Paramitapura (offline)
- Yayasan Padepokan Fatwa Kehidupan
- 124+ ribu pengikut

{BOLD}Ajaran:{RESET} Ilmu hati, kesufian, ketiadaan diri
""")
                input(f"\n{DIM}Enter...{RESET}")
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "cari": 
            for r in cari(" ".join(sys.argv[2:])): print(f"\n{r['judul']}\n{r['konten']}\n")
        elif cmd == "yolhan": os.system("termux-open-url 'https://www.facebook.com/yolhan.wijaya'")
        elif cmd == "fatwa": os.system("termux-open-url 'https://www.facebook.com/fatwa.kehidupan'")
        elif cmd == "buku": baca_pdf()
        elif cmd == "tanya": print(ai_generate(" ".join(sys.argv[2:])))
        else: menu()
    else: menu()
