#!/data/data/com.termux/files/usr/bin/python
"""
EKOSISTEM ZUHRI — MENU PREMIUM
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
ANSI 256 Color • ASCII Art • Animation
"""

import os, sys, json, subprocess, random, time

HOME = os.path.expanduser("~")
ID_FILE = os.path.join(HOME, "zuhri_os", "id", "identity.json")

# ===== ANSI 256 COLOR =====
R = "\033[0m"
B = "\033[1m"
D = "\033[2m"

# Warna dasar
CYAN = "\033[38;5;51m"
MAGENTA = "\033[38;5;201m"
GOLD = "\033[38;5;220m"
GREEN = "\033[38;5;46m"
RED = "\033[38;5;196m"
BLUE = "\033[38;5;21m"
PURPLE = "\033[38;5;141m"
PINK = "\033[38;5;213m"
ORANGE = "\033[38;5;208m"
WHITE = "\033[38;5;231m"
GRAY = "\033[38;5;244m"
NEON = "\033[38;5;118m"
ICE = "\033[38;5;159m"

# Gradasi
G1 = "\033[38;5;51m"
G2 = "\033[38;5;45m"
G3 = "\033[38;5;39m"
G4 = "\033[38;5;33m"

SYMBOLS = ["◈","◇","◆","◉","◎","●","○","✦","✧","★","☆"]

def clear(): os.system('clear')

def load_id():
    if not os.path.exists(ID_FILE): return None
    try: return json.load(open(ID_FILE))
    except: return None

def tor_ok():
    try: return subprocess.run(["pgrep","-x","tor"],capture_output=True).returncode==0
    except: return False

def ollama_ok():
    try: return subprocess.run(["pgrep","ollama"],capture_output=True).returncode==0
    except: return False

def run(c): os.system(c)

def animate_boot():
    """Animasi boot singkat"""
    clear()
    boot = [
        f"{G1}[BOOT]{R} Zuhri Core...",
        f"{G2}[BOOT]{R} Fluid-Core...",
        f"{G3}[BOOT]{R} Echo-Synapse...",
        f"{G4}[BOOT]{R} Resonansi 0-8-9...",
        f"{NEON}[BOOT]{R} ✅ ONLINE",
    ]
    for line in boot:
        print(f"  {line}")
        time.sleep(0.15)
    print()

def print_logo():
    """ASCII Logo Zuhri"""
    logo = f"""{G1}
  ╔══════════════════════════════════════════════════════════════════╗
  ║{MAGENTA}  ███████╗██╗   ██╗██╗  ██╗██████╗ ██╗                       {G1}║
  ║{MAGENTA}  ╚══███╔╝██║   ██║██║  ██║██╔══██╗██║                       {G1}║
  ║{MAGENTA}    ███╔╝ ██║   ██║███████║██████╔╝██║                       {G1}║
  ║{MAGENTA}   ███╔╝  ██║   ██║██╔══██║██╔══██╗██║                       {G1}║
  ║{MAGENTA}  ███████╗╚██████╔╝██║  ██║██║  ██║██║                       {G1}║
  ║{MAGENTA}  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝                       {G1}║
  ╠══════════════════════════════════════════════════════════════════╣
  ║{GOLD}        🌌 EKOSISTEM ZUHRI  •  PREMIUM EDITION  🌌              {G1}║
  ╠══════════════════════════════════════════════════════════════════╣
  ║{CYAN}  PROTOKOL: {GOLD}K-8.0{R}          {CYAN}GEN: {GOLD}ZUH-8-9-0-K-8.0{R}              {G1}║
  ║{CYAN}  RESONANSI: {NEON}0-8-9 — SEIMBANG{R}                                {G1}║
  ╚══════════════════════════════════════════════════════════════════╝{R}
"""
    print(logo)

def print_operator():
    i = load_id()
    print(f"  {D}{'─' * 66}{R}")
    if i:
        print(f"  {GOLD}👤{R} {B}{WHITE}{i['name']}{R}")
        print(f"  {GOLD}🆔{R} {GRAY}{i['zuhri_id'][:40]}...{R}")
    else:
        print(f"  {RED}⚠️  Belum punya Zuhri ID — pilih 1{R}")
    
    t = f"{NEON}✅{R}" if tor_ok() else f"{RED}❌{R}"
    o = f"{NEON}✅{R}" if ollama_ok() else f"{RED}❌{R}"
    print(f"  {GOLD}📊{R} Tor: {t}   {GOLD}Ollama:{R} {o}")
    print(f"  {D}{'─' * 66}{R}\n")

def section(title, color, items):
    """Cetak section dengan warna"""
    print(f"{color}  ┏━━━ {B}{title}{R} {color}{'━' * (55 - len(title))}┓{R}")
    for num, icon, name, desc in items:
        print(f"{color}  ┃{R} {GOLD}{num:>2}.{R} {icon} {B}{WHITE}{name:<20}{R} {GRAY}→ {desc}{R}")
    print(f"{color}  ┗{'━' * 64}┛{R}\n")

def print_menu():
    section("🚨 PRIORITAS — DARURAT", RED, [
        (22, "🚨", "ZUHRI PERINGATAN", "Prediksi bencana")
    ])
    
    section("🛡️  KEAMANAN & PERISAI", MAGENTA, [
        (40, "🛡️ ", "TOR SHIELD", "Perisai Tor 5 layer"),
        (39, "🛡️ ", "ECHO-CORE", "Post-Quantum Shield"),
        (4,  "🔐", "ZUHRI SECURITY", "Keamanan berlapis"),
    ])
    
    section("🎨 KREATIVITAS & KOMUNIKASI", PINK, [
        (41, "🎨", "ZUHRI ART", "Seni & kreativitas"),
        (42, "👥", "ZUHRI SOCIAL", "Media sosial P2P"),
        (43, "📧", "ZUHRI GMAIL", "Email lokal"),
    ])
    
    section("🏥 KEHIDUPAN", GREEN, [
        (44, "🏥", "ZUHRI MED", "Kesehatan dasar"),
        (45, "🌤️ ", "ZUHRI WEATHER", "Cuaca & iklim"),
        (46, "🗺️ ", "ZUHRI MAPS", "Peta & lokasi"),
        (38, "🌿", "ZUHRI TRADISIONAL", "Obat & jamu"),
    ])
    
    section("🕌 SPIRITUAL & KOSMIK", PURPLE, [
        (24, "🕌", "ZUHRI SPIRITUAL", "Fatwa Kehidupan"),
        (25, "📡", "ZUHRI FREKUENSI", "Resonansi & anomali"),
        (26, "🔮", "ZUHRI PREDICTIVE", "Terminal prediktif"),
        (27, "⚡", "ZUHRI ENERGI", "Monitor baterai"),
    ])
    
    section("🌟 IDENTITAS & NETWORK", CYAN, [
        (1,  "🆔", "ZUHRI ID", "Identitas digital"),
        (2,  "🛂", "ZUHRI PASSPORT", "Passport global"),
        (3,  "🔐", "ZUHRI KRIPTOGRAFI", "AES-256, Vault"),
        (5,  "📡", "ZUHRI P2P-MESH", "Jaringan offline"),
        (6,  "🔍", "ZUHRI MESH-SCAN", "Cari node"),
        (7,  "🆘", "ZUHRI SOS-BEACON", "Sinyal darurat"),
    ])
    
    section("🧠 AI & DEMOKRASI & FINANSIAL", GOLD, [
        (8,  "🧠", "ZUHRI AI", "AI offline"),
        (9,  "🔍", "ZUHRI VISION", "Deteksi objek"),
        (10, "🌍", "ZUHRI TRANSLATE", "Terjemahan"),
        (12, "🗳️ ", "ZUHRI VOTE", "Voting digital"),
        (13, "📜", "ZUHRI CONTRACT", "Kontrak pintar"),
        (14, "💰", "ZUHRI FINANSIAL", "Keuangan mandiri"),
        (15, "🪙", "ZUHRI WALLET", "Dompet crypto"),
    ])
    
    section("📚 PENGETAHUAN & CHAIN", BLUE, [
        (16, "🎓", "ZUHRI EDU", "Kursus & sertifikat"),
        (17, "📚", "ZUHRI LIBRARY", "Perpustakaan"),
        (21, "🧬", "ZUHRI KURIKULUM", "K-8.0 Komprehensif"),
        (29, "⛓️ ", "ZUHRI CHAIN", "Database terdesentralisasi"),
        (30, "🆔", "ZUHRI DID", "Decentralized ID"),
        (31, "🔐", "ZUHRI ENKRIPSI", "Enkripsi lengkap"),
    ])
    
    section("🌐 DEEP & DARK WEB", PURPLE, [
        (34, "🌐", "ZUHRI DEEP ACCESS", "Layer 2 & 3"),
        (35, "🌑", "ZUHRI DARK-WEB", "Gateway + panduan"),
        (36, "🧬", "FORMALISM SEARCH", "Logika+Data+Intuisi"),
        (37, "🪞", "CERMIN BAYANGAN", "Meta-pencarian"),
    ])
    
    section("⚙️  SISTEM & DOKUMENTASI", GRAY, [
        (18, "💻", "ZUHRI OS", "Sistem lengkap"),
        (19, "💻", "ZUHRI HEALTH", "RAM & storage"),
        (20, "💾", "ZUHRI BACKUP", "Backup konfigurasi"),
        (23, "📖", "PANDUAN", "Onboarding"),
        (32, "🚦", "AUTO-ROUTING", "Router otomatis"),
        (33, "📚", "ZUHRI DOCS", "Sejarah & visi"),
    ])

def print_footer():
    print(f"  {D}{'─' * 66}{R}")
    print(f"  {GOLD}0.{R} {RED}🚪 KELUAR{R}")
    print(f"  {D}{'─' * 66}{R}")
    print(f"  {D}📡 Pilih (0-46) atau ketik 'z <kata-kunci>' untuk auto-routing{R}\n")

def main():
    animate_boot()
    
    while True:
        clear()
        print_logo()
        print_operator()
        print_menu()
        print_footer()
        
        try:
            c = input(f"  {GOLD}🌌 Pilih Ekosistem{R}: ").strip()
            
            if c == "0":
                clear()
                print(f"\n  {GOLD}╔══════════════════════════════════════════════════════════════════╗")
                print(f"  ║{MAGENTA}            👋 SAMPAI JUMPA, OPERATOR!                          {GOLD}║")
                print(f"  ║{CYAN}            Resonansi tetap 0-8-9 — SEIMBANG                    {GOLD}║")
                print(f"  ╚══════════════════════════════════════════════════════════════════╝{R}\n")
                break
            
            # Auto-routing
            if c.startswith("z "):
                os.system(f"python ~/zuhri_os/autoroute/zuhri_autoroute.py {c[2:]}")
                input(f"  {D}Enter...{R}")
                continue
            
            commands = {
                "1": "python ~/zuhri_os/id/zuhri_id.py show",
                "2": "python ~/zuhri_os/passport/zuhri_passport.py",
                "3": "python ~/zuhri_os/crypto/zuhri_crypto.py",
                "4": "python ~/zuhri_os/security/security_shield.py",
                "5": "python ~/kosmik/p2p/mesh_node.py",
                "6": "python ~/kosmik/p2p/mesh_discovery.py",
                "7": "python ~/kosmik/sos_beacon.py beacon",
                "8": "ai",
                "9": "python ~/kosmik/vision/edge_vision.py",
                "10": "python ~/zuhri_os/translator/translator.py",
                "12": "python ~/zuhri_os/vote/zuhri_vote.py",
                "13": "python ~/zuhri_os/contract/zuhri_contract.py",
                "14": "python ~/zuhri_os/finance/zuhri_finance.py",
                "15": "python ~/zuhri_os/wallet/wallet.py",
                "16": "python ~/zuhri_os/edu/zuhri_edu.py",
                "17": "python ~/zuhri_os/library/zuhri_library.py",
                "18": "python ~/zuhri_os/zuhri_os.py",
                "19": "python ~/health.py",
                "20": "python ~/zuhri_os/backup/backup_manager.py",
                "21": "python ~/zuhri_os/kurikulum/zuhri_kurikulum.py",
                "22": "python ~/zuhri_os/peringatan/zuhri_peringatan.py",
                "23": "python ~/zuhri_os/onboarding/welcome.py",
                "24": "python ~/zuhri_os/spiritual/zuhri_spiritual.py",
                "25": "python ~/zuhri_os/frekuensi/zuhri_frekuensi.py",
                "26": "python ~/zuhri_os/predictive/zuhri_predictive.py",
                "27": "python ~/zuhri_os/energi/zuhri_energi.py",
                "28": "python ~/zuhri_os/botnet/zuhri_botnet.py",
                "29": "python ~/zuhri_os/chain/zuhri_chain.py",
                "30": "python ~/zuhri_os/did/zuhri_did.py",
                "31": "python ~/zuhri_os/enkripsi/zuhri_enkripsi.py",
                "32": "python ~/zuhri_os/autoroute/zuhri_autoroute.py",
                "33": "python ~/zuhri_os/docs/zuhri_docs.py",
                "34": "bash ~/zuhri_os/deepaccess/zuhri-deep",
                "35": "bash ~/zuhri_os/darkweb/dark-web",
                "36": "bash ~/zuhri_os/formalism/zuhri-search",
                "37": "bash ~/zuhri_os/formalism/zuhri-search",
                "38": "python ~/zuhri_os/tradisional/zuhri_tradisional.py",
                "39": "python ~/zuhri_os/echocore/zuhri_echocore.py",
                "40": "python ~/zuhri_os/torshield/zuhri_torshield.py",
                "41": "python ~/zuhri_os/art/zuhri_art.py",
                "42": "python ~/zuhri_os/social/zuhri_social.py",
                "43": "python ~/zuhri_os/gmail/zuhri_gmail.py",
                "44": "python ~/zuhri_os/med/zuhri_med.py",
                "45": "python ~/zuhri_os/weather/zuhri_weather.py",
                "46": "python ~/zuhri_os/maps/zuhri_maps.py",
            }
            
            if c in commands:
                clear()
                print(f"  {NEON}🚀 Menjalankan...{R}\n")
                time.sleep(0.3)
                run(commands[c])
                input(f"\n  {D}Enter untuk kembali...{R}")
            else:
                print(f"  {RED}❌ Pilihan tidak valid{R}")
                time.sleep(1)
        
        except KeyboardInterrupt:
            print(f"\n  {GOLD}👋 Sampai jumpa!{R}\n")
            break

if __name__ == "__main__":
    main()
