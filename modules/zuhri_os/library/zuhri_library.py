#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI LIBRARY — PERPUSTAKAAN OFFLINE
Baca buku, artikel, dan pengetahuan tanpa internet
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os
import sys
import json
import subprocess
from datetime import datetime

# ===== ZUHRI AUTH =====
sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

# ===== KONFIGURASI =====
HOME = os.path.expanduser("~")
LIB_DIR = os.path.join(HOME, "zuhri_os", "library")
BOOKS_DIR = os.path.join(LIB_DIR, "books")
ARTICLES_DIR = os.path.join(LIB_DIR, "articles")
READ_DIR = os.path.join(LIB_DIR, "read_log")
os.makedirs(BOOKS_DIR, exist_ok=True)
os.makedirs(ARTICLES_DIR, exist_ok=True)
os.makedirs(READ_DIR, exist_ok=True)

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

# ============================================================
# ARTIKEL DEFAULT
# ============================================================
DEFAULT_ARTICLES = {
    "pengenalan_zuhri": {
        "title": "Pengenalan Zuhri Network",
        "category": "Zuhri",
        "content": """ZUHRI NETWORK adalah ekosistem digital mandiri yang berjalan di HP Anda.

Dibangun dengan protokol K-8.0 dan filosofi 0-8-9 (Keseimbangan Dinamis).

Fitur utama:
- Zuhri ID: Identitas digital tanpa KTP
- P2P-Mesh: Komunikasi tanpa internet
- Zuhri Crypto: Enkripsi AES-256
- Zuhri Edu: Pendidikan offline
- Zuhri Finance: Keuangan mandiri

Prinsip:
1. Privasi — Data milik Anda
2. Kebebasan — Tanpa sensor
3. Kemandirian — Tanpa cloud
4. Kolaborasi — P2P
5. Keberlanjutan — Bisa hidup tanpa internet

"Zuhri bukan produk. Zuhri adalah gerakan." """
    },
    "kriptografi_dasar": {
        "title": "Kriptografi Dasar untuk Pemula",
        "category": "Keamanan",
        "content": """KRIPTOGRAFI adalah seni menjaga kerahasiaan pesan.

1. HASH FUNCTION
- SHA-256: Menghasilkan sidik jari 256-bit
- Tidak bisa dikembalikan (one-way)
- Digunakan untuk verifikasi

2. ENKRIPSI SIMETRIS
- AES-256-GCM: Standar militer
- Satu kunci untuk enkripsi & dekripsi
- Cepat & efisien

3. ENKRIPSI ASIMETRIS
- RSA-4096, Ed25519
- Public key untuk enkripsi
- Private key untuk dekripsi

4. TANDA TANGAN DIGITAL
- Ed25519: Tanda tangan tidak bisa dipalsukan
- Digunakan untuk verifikasi identitas
- Dasar dari Zuhri ID

"Kriptografi = matematika yang melindungi privasi Anda." """
    },
    "linux_dasar": {
        "title": "Linux Dasar untuk Termux",
        "category": "Sistem Operasi",
        "content": """LINUX adalah sistem operasi open source yang jadi dasar Termux.

1. STRUKTUR FILE
- / = root
- /home = folder user
- /bin = program
- /etc = konfigurasi

2. PERINTAH DASAR
- ls = lihat isi folder
- cd = pindah folder
- pwd = lihat lokasi sekarang
- cp = copy
- mv = pindah/ganti nama
- rm = hapus

3. PERMISSION
- chmod 600 = hanya owner
- chmod 755 = owner + read all

4. PACKAGE MANAGER
- pkg install = install program
- pkg update = update

"Linux memberi Anda kontrol penuh atas komputer." """
    }
}

# ============================================================
# UTIL
# ============================================================
def get_id_badge():
    if not ZUHRI_ID_OK:
        return f"{YELLOW}⚠️  TANPA ZUHRI ID{RESET}"
    i = load_identity()
    if i:
        return f"{GREEN}✅ {i['name']}{RESET}"
    return f"{YELLOW}⚠️  TANPA ZUHRI ID{RESET}"

def init_articles():
    """Buat artikel default jika kosong"""
    if not os.listdir(ARTICLES_DIR):
        for key, art in DEFAULT_ARTICLES.items():
            with open(os.path.join(ARTICLES_DIR, f"{key}.json"), "w") as f:
                json.dump(art, f, indent=2)

def log_read(item_type, title):
    """Catat item yang dibaca"""
    if not ZUHRI_ID_OK:
        return
    i = load_identity()
    if not i:
        return
    log_file = os.path.join(READ_DIR, f"{i['zuhri_id']}.json")
    data = []
    if os.path.exists(log_file):
        try:
            data = json.load(open(log_file))
        except:
            data = []
    data.append({"type": item_type, "title": title, "time": datetime.now().isoformat()})
    json.dump(data, open(log_file, "w"), indent=2)
    log_verified(f"LIBRARY_READ: {title}")

# ============================================================
# LIST
# ============================================================
def list_all():
    init_articles()
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📚 ZUHRI LIBRARY — DAFTAR KOLEKSI                              ║
║  Operator: {get_id_badge()}
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    # Buku
    books = [f for f in os.listdir(BOOKS_DIR) if f.endswith(('.txt', '.md', '.epub', '.pdf'))]
    print(f"{BOLD}{GOLD}📖 BUKU ({len(books)}){RESET}")
    if books:
        for i, b in enumerate(books, 1):
            size = os.path.getsize(os.path.join(BOOKS_DIR, b))
            print(f"  {GOLD}{i}.{RESET} {b} {DIM}({size/1024:.1f} KB){RESET}")
    else:
        print(f"  {DIM}(Belum ada buku — import dengan: library import){RESET}")
    
    print()
    
    # Artikel
    articles = [f.replace('.json', '') for f in os.listdir(ARTICLES_DIR) if f.endswith('.json')]
    print(f"{BOLD}{GOLD}📄 ARTIKEL ({len(articles)}){RESET}")
    for i, a in enumerate(articles, 1):
        art = json.load(open(os.path.join(ARTICLES_DIR, f"{a}.json")))
        print(f"  {GOLD}{i}.{RESET} {art['title']} {DIM}[{art['category']}]{RESET}")
    
    print()

# ============================================================
# BACA ARTIKEL
# ============================================================
def read_article():
    init_articles()
    articles = [f.replace('.json', '') for f in os.listdir(ARTICLES_DIR) if f.endswith('.json')]
    
    if not articles:
        print(f"{YELLOW}Belum ada artikel.{RESET}")
        return
    
    print(f"\n{BOLD}{CYAN}📄 PILIH ARTIKEL:{RESET}\n")
    for i, a in enumerate(articles, 1):
        art = json.load(open(os.path.join(ARTICLES_DIR, f"{a}.json")))
        print(f"  {GOLD}{i}.{RESET} {art['title']}")
    
    try:
        c = int(input(f"\n{CYAN}Pilih: {RESET}").strip()) - 1
        if not (0 <= c < len(articles)):
            return
        
        art = json.load(open(os.path.join(ARTICLES_DIR, f"{articles[c]}.json")))
        
        os.system('clear')
        print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📄 {art['title']}
║  Kategori: {art['category']}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{art['content']}

{DIM}─────────────────────────────────────────────────────────────{RESET}
""")
        log_read("artikel", art['title'])
        input(f"{DIM}Tekan Enter untuk kembali...{RESET}")
    except (ValueError, IndexError):
        pass

# ============================================================
# BACA BUKU
# ============================================================
def read_book():
    books = [f for f in os.listdir(BOOKS_DIR) if f.endswith(('.txt', '.md'))]
    
    if not books:
        print(f"\n{YELLOW}Belum ada buku teks (.txt/.md).{RESET}")
        print(f"{DIM}Import dengan: library import /path/file.txt{RESET}\n")
        return
    
    print(f"\n{BOLD}{CYAN}📖 PILIH BUKU:{RESET}\n")
    for i, b in enumerate(books, 1):
        print(f"  {GOLD}{i}.{RESET} {b}")
    
    try:
        c = int(input(f"\n{CYAN}Pilih: {RESET}").strip()) - 1
        if not (0 <= c < len(books)):
            return
        
        book_file = os.path.join(BOOKS_DIR, books[c])
        
        os.system('clear')
        print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📖 {books[c]}
╚══════════════════════════════════════════════════════════════════╝{RESET}

""")
        
        # Tampilkan 50 baris pertama
        with open(book_file, 'r', errors='ignore') as f:
            lines = f.readlines()[:50]
            print("".join(lines))
        
        if len(lines) >= 50:
            print(f"\n{DIM}... (menampilkan 50 baris pertama){RESET}")
        
        print(f"\n{DIM}─────────────────────────────────────────────────────────────{RESET}")
        log_read("buku", books[c])
        input(f"{DIM}Tekan Enter...{RESET}")
    except (ValueError, IndexError):
        pass

# ============================================================
# IMPORT BUKU
# ============================================================
def import_book():
    print(f"\n{BOLD}{CYAN}📥 IMPORT BUKU{RESET}\n")
    path = input("📂 Path file buku (.txt/.md): ").strip()
    
    if not os.path.exists(path):
        print(f"{RED}❌ File tidak ditemukan{RESET}")
        return
    
    import shutil
    filename = os.path.basename(path)
    dest = os.path.join(BOOKS_DIR, filename)
    
    try:
        shutil.copy2(path, dest)
        print(f"\n{GREEN}✅ Buku di-import: {filename}{RESET}")
        print(f"   Lokasi: {dest}\n")
        log_verified(f"LIBRARY_IMPORT: {filename}")
    except Exception as e:
        print(f"{RED}❌ Gagal import: {e}{RESET}")

# ============================================================
# CARI
# ============================================================
def search():
    print(f"\n{BOLD}{CYAN}🔍 CARI DI PERPUSTAKAAN{RESET}\n")
    query = input("🔍 Kata kunci: ").strip().lower()
    
    if not query:
        return
    
    results = []
    
    # Cari di artikel
    init_articles()
    for f in os.listdir(ARTICLES_DIR):
        if f.endswith('.json'):
            art = json.load(open(os.path.join(ARTICLES_DIR, f)))
            if query in art['title'].lower() or query in art['content'].lower():
                results.append(("Artikel", art['title']))
    
    # Cari di buku
    for f in os.listdir(BOOKS_DIR):
        if f.endswith(('.txt', '.md')):
            try:
                content = open(os.path.join(BOOKS_DIR, f), 'r', errors='ignore').read().lower()
                if query in content:
                    results.append(("Buku", f))
            except:
                pass
    
    print(f"\n{BOLD}Hasil pencarian '{query}':{RESET}\n")
    
    if results:
        for i, (t, title) in enumerate(results, 1):
            print(f"  {GOLD}{i}.{RESET} [{t}] {title}")
    else:
        print(f"  {YELLOW}Tidak ada hasil.{RESET}")
    
    print()

# ============================================================
# STATISTIK
# ============================================================
def show_stats():
    books = [f for f in os.listdir(BOOKS_DIR) if f.endswith(('.txt', '.md', '.epub', '.pdf'))]
    articles = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.json')]
    
    read_count = 0
    if ZUHRI_ID_OK:
        i = load_identity()
        if i:
            log_file = os.path.join(READ_DIR, f"{i['zuhri_id']}.json")
            if os.path.exists(log_file):
                read_count = len(json.load(open(log_file)))
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📊 STATISTIK ZUHRI LIBRARY                                    ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{GOLD}📖 Buku:{RESET}        {len(books)}
{GOLD}📄 Artikel:{RESET}     {len(articles)}
{GOLD}📚 Total:{RESET}       {len(books) + len(articles)}
{GOLD}👁️  Sudah dibaca:{RESET} {read_count}
""")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        
        print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📚 ZUHRI LIBRARY — PERPUSTAKAAN OFFLINE                       ║
║  ──────────────────────────────────────────────────────────────  ║
║  Operator: {get_id_badge()}
║  Protocol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                       ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  📚 Lihat Koleksi
  {GOLD}2.{RESET}  📄 Baca Artikel
  {GOLD}3.{RESET}  📖 Baca Buku
  {GOLD}4.{RESET}  📥 Import Buku
  {GOLD}5.{RESET}  🔍 Cari
  {GOLD}6.{RESET}  📊 Statistik
  {GOLD}7.{RESET}  🌐 Info Kiwix (Wikipedia Offline)
  {GOLD}0.{RESET}  Keluar
""")
        
        try:
            c = input(f"{GOLD}Pilih (0-7): {RESET}").strip()
            
            if c == "0": break
            elif c == "1": list_all()
            elif c == "2": read_article()
            elif c == "3": read_book()
            elif c == "4": import_book()
            elif c == "5": search()
            elif c == "6": show_stats()
            elif c == "7":
                print(f"""
{BOLD}{CYAN}🌐 KIWIX — WIKIPEDIA OFFLINE{RESET}

Kiwix adalah aplikasi untuk membaca Wikipedia offline.

Cara install:
  1. Download Kiwix Android dari F-Droid/Play Store
  2. Download file Wikipedia Indonesia (.zim) — ~5-20 GB
  3. Buka Kiwix → Import file

Atau via Termux:
  pkg install kiwix-tools
  kiwix-serve /path/ke/wikipedia.zim

{LINK}https://www.kiwix.org/en/downloads/{RESET}
""")
            
            if c != "0":
                input(f"{DIM}Tekan Enter...{RESET}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "list": list_all()
        elif cmd == "stats": show_stats()
        elif cmd == "search": search()
        elif cmd == "help":
            print("""
📚 ZUHRI LIBRARY — BANTUAN
─────────────────────────
  library          → Menu interaktif
  library list     → Lihat koleksi
  library stats    → Statistik
  library search   → Cari
""")
        else: menu()
    else:
        menu()
