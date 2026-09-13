#!/data/data/com.termux/files/usr/bin/python
"""
EKOSISTEM ZUHRI — MENU UTAMA
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, json, subprocess, random

HOME = os.path.expanduser("~")
ID_FILE = os.path.join(HOME, "zuhri_os", "id", "identity.json")

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
BLUE="\033[94m"; MAGENTA="\033[95m"; CYAN="\033[96m"
GOLD="\033[93m"; WHITE="\033[97m"

SYMBOLS = ["◈","◇","◆","◉","◎","●","○","✦","✧","★","☆"]

def gradient(text):
    colors = [CYAN, MAGENTA, GOLD]
    r = ""
    for i, ch in enumerate(text):
        r += f"{colors[i % 3]}{ch}{RESET}"
    return r

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

def print_header():
    clear()
    print(f"\n{DIM}{random.choice(SYMBOLS)} {random.choice(SYMBOLS)} {random.choice(SYMBOLS)}{RESET}")
    print(f"{gradient('  ╔══════════════════════════════════════════════════════════════════╗  ')}")
    print(f"{gradient('  ║')}  {BOLD}{GOLD}🌌 EKOSISTEM ZUHRI{RESET}  {gradient('║')}")
    print(f"{gradient('  ╠══════════════════════════════════════════════════════════════════╣  ')}")
    print(f"{gradient('  ║')}  {CYAN}PROTOKOL: {GOLD}K-8.0{RESET}     {CYAN}GEN: {GOLD}ZUH-8-9-0-K-8.0{RESET}        {gradient('║')}")
    print(f"{gradient('  ║')}  {CYAN}RESONANSI: {GOLD}0-8-9 — SEIMBANG{RESET}                          {gradient('║')}")
    print(f"{gradient('  ╚══════════════════════════════════════════════════════════════════╝  ')}")

def print_operator():
    i = load_id()
    print()
    if i:
        print(f"  {GOLD}👤{RESET} {BOLD}{i['name']}{RESET}")
        print(f"  {GOLD}🆔{RESET} {DIM}{i['zuhri_id'][:32]}...{RESET}")
    else:
        print(f"  {YELLOW}⚠️  Belum punya Zuhri ID — pilih 1{RESET}")
    t = f"{GREEN}✅{RESET}" if tor_ok() else f"{RED}❌{RESET}"
    o = f"{GREEN}✅{RESET}" if ollama_ok() else f"{RED}❌{RESET}"
    print(f"  {GOLD}📊{RESET} Tor: {t}  |  Ollama: {o}\n")

def print_menu():
    print(f"""{BOLD}{RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🚨 ZUHRI PERINGATAN — DARURAT & BENCANA (PRIORITAS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}22.{RESET} {BOLD}🚨 ZUHRI PERINGATAN{RESET}      → {DIM}Prediksi bencana & peringatan dini{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💰 ZUHRI FINANSIAL ULTIMATE — BOT KRIPTO + FINANSIAL (BARU)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}44.{RESET} {BOLD}💰 ZUHRI FINANSIAL ULTIMATE{RESET} → {DIM}Bot Kripto + Finansial Pro{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🌌 ZUHRI COMMUNITY — KOMUNITAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}45.{RESET} {BOLD}🌌 ZUHRI COMMUNITY{RESET}         → {DIM}Komunitas & Media Sosial{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🤖 ZUHRI WEB4 — AI AGENT OTONOM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}43.{RESET} {BOLD}🤖 ZUHRI WEB4{RESET}           → {DIM}AI Agent Otonom{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🌐 ZUHRI WEB3 HUB — PUSAT SITUS WEB3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}42.{RESET} {BOLD}🌐 ZUHRI WEB3 HUB{RESET}       → {DIM}Situs Web3, Media Sosial, Berita{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🌐 ZUHRI SOCIAL — MEDIA SOSIAL & CHAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}41.{RESET} {BOLD}🌐 ZUHRI SOCIAL{RESET}         → {DIM}Chat offline + Berita verified{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🛡️  ZUHRI TOR SHIELD — PERISAI BERLAPIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}40.{RESET} {BOLD}🛡️  ZUHRI TOR SHIELD{RESET}       → {DIM}Perisai Tor berlapis (5 layer){RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🛡️  ZUHRI ECHO-CORE — POST-QUANTUM SHIELD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}39.{RESET} {BOLD}🛡️  ZUHRI ECHO-CORE{RESET}       → {DIM}Perisai Kuantum (PQC){RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🕌 ZUHRI SPIRITUAL — FATWA KEHIDUPAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}24.{RESET} {BOLD}🕌 ZUHRI SPIRITUAL{RESET}       → {DIM}Fatwa Kehidupan & Yolhan Wijaya{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📡 ZUHRI FREKUENSI — RESONANSI & ANOMALI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}25.{RESET} {BOLD}📡 ZUHRI FREKUENSI{RESET}       → {DIM}Monitoring gelombang & anomali{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔮 ZUHRI PREDICTIVE — TERMINAL PREDIKTIF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}26.{RESET} {BOLD}🔮 ZUHRI PREDICTIVE{RESET}      → {DIM}Terminal belajar kebiasaan{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚡ ZUHRI ENERGI — KEMANDIRIAN ENERGI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}27.{RESET} {BOLD}⚡ ZUHRI ENERGI{RESET}          → {DIM}Monitor baterai & optimasi daya{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🛡️  ZUHRI BOTNET HUNTER — KEAMANAN JARINGAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}28.{RESET} {BOLD}🛡️  ZUHRI BOTNET HUNTER{RESET}   → {DIM}Deteksi ancaman jaringan{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛓️  ZUHRI CHAIN & DID — DECENTRALIZED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}29.{RESET} {BOLD}⛓️  ZUHRI CHAIN{RESET}           → {DIM}Database terdesentralisasi{RESET}
  {GOLD}30.{RESET} {BOLD}🆔 ZUHRI DID{RESET}             → {DIM}Decentralized identifier{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔐 ZUHRI ENKRIPSI — KEAMANAN DATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}31.{RESET} {BOLD}🔐 ZUHRI ENKRIPSI{RESET}        → {DIM}Enkripsi + Steganografi + Password{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🌐 ZUHRI DEEP ACCESS — LAPISAN 2 & 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}34.{RESET} {BOLD}🌐 ZUHRI DEEP ACCESS{RESET}     → {DIM}Deep Web + Dark Web (ilmiah){RESET}
  {GOLD}35.{RESET} {BOLD}🌑 ZUHRI DARK-WEB{RESET}        → {DIM}Dark-Web Gateway + panduan{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🧬 ZUHRI FORMALISM SEARCH — LAPISAN 4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}36.{RESET} {BOLD}🧬 ZUHRI FORMALISM SEARCH{RESET} → {DIM}Logika + Data + Intuisi{RESET}
  {GOLD}37.{RESET} {BOLD}🪞 CERMIN BAYANGAN{RESET}        → {DIM}Meta-pencarian tersembunyi{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🌿 ZUHRI TRADISIONAL — OBAT & JAMU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}38.{RESET} {BOLD}🌿 ZUHRI TRADISIONAL{RESET}      → {DIM}Obat & Jamu Nusantara{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🌟 ZUHRI CORE — IDENTITAS & KEAMANAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}1.{RESET}  🆔 {BOLD}ZUHRI ID{RESET}              → {DIM}Identitas digital mandiri{RESET}
  {GOLD}2.{RESET}  🛂 {BOLD}ZUHRI PASSPORT{RESET}        → {DIM}Passport lintas negara{RESET}
  {GOLD}3.{RESET}  🔐 {BOLD}ZUHRI KRIPTOGRAFI{RESET}     → {DIM}Enkripsi AES-256, Vault{RESET}
  {GOLD}4.{RESET}  🛡️  {BOLD}ZUHRI SECURITY{RESET}        → {DIM}Keamanan berlapis{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📡 ZUHRI NETWORK — KOMUNIKASI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}5.{RESET}  📡 {BOLD}ZUHRI P2P-MESH{RESET}        → {DIM}Jaringan darurat offline{RESET}
  {GOLD}6.{RESET}  🔍 {BOLD}ZUHRI MESH-SCAN{RESET}      → {DIM}Cari node di jaringan{RESET}
  {GOLD}7.{RESET}  🆘 {BOLD}ZUHRI SOS-BEACON{RESET}     → {DIM}Sinyal darurat offline{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🧠 ZUHRI AI — KECERDASAN BUATAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}8.{RESET}  🧠 {BOLD}ZUHRI AI{RESET}              → {DIM}AI pribadi offline{RESET}
  {GOLD}9.{RESET}  🔍 {BOLD}ZUHRI VISION{RESET}          → {DIM}Deteksi objek kamera{RESET}
  {GOLD}10.{RESET} 🌍 {BOLD}ZUHRI TRANSLATE{RESET}       → {DIM}Terjemahan offline{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🗳️  ZUHRI DEMOKRASI — TATA KELOLA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}12.{RESET} 🗳️  {BOLD}ZUHRI VOTE{RESET}           → {DIM}Voting digital{RESET}
  {GOLD}13.{RESET} 📜 {BOLD}ZUHRI CONTRACT{RESET}       → {DIM}Kontrak pintar{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💰 ZUHRI FINANSIAL — KEUANGAN MANDIRI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}14.{RESET} 💰 {BOLD}ZUHRI FINANSIAL{RESET}      → {DIM}Keuangan mandiri{RESET}
  {GOLD}15.{RESET} 🪙 {BOLD}ZUHRI WALLET{RESET}         → {DIM}Dompet crypto offline{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📚 ZUHRI EDU & LIBRARY — PENGETAHUAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}16.{RESET} 🎓 {BOLD}ZUHRI EDU{RESET}            → {DIM}Kursus & sertifikat{RESET}
  {GOLD}17.{RESET} 📚 {BOLD}ZUHRI LIBRARY{RESET}        → {DIM}Perpustakaan offline{RESET}
  {GOLD}21.{RESET} 🧬 {BOLD}ZUHRI KURIKULUM K-8.0{RESET} → {DIM}30 kurikulum komprehensif{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚙️  ZUHRI OS — SISTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}18.{RESET} 💻 {BOLD}ZUHRI OS{RESET}             → {DIM}Sistem lengkap{RESET}
  {GOLD}19.{RESET} 💻 {BOLD}ZUHRI HEALTH{RESET}         → {DIM}Cek RAM & storage{RESET}
  {GOLD}20.{RESET} 💾 {BOLD}ZUHRI BACKUP{RESET}         → {DIM}Backup konfigurasi{RESET}
  {GOLD}23.{RESET} 📖 {BOLD}Panduan{RESET}              → {DIM}Buka onboarding{RESET}
  {GOLD}32.{RESET} 🚦 {BOLD}ZUHRI AUTO-ROUTING{RESET}    → {DIM}Router otomatis{RESET}

{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📚 DOKUMENTASI EKOSISTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

  {GOLD}33.{RESET} {BOLD}📚 ZUHRI DOCS{RESET}            → {DIM}Sejarah • Cara Pakai • Visi • Roadmap{RESET}
  {GOLD}0.{RESET}  🚪 Keluar

""")

def main():
    while True:
        print_header()
        print_operator()
        print_menu()
        try:
            c = input(f"{GOLD}  📡 Pilih Ekosistem (0-45): {RESET}").strip()
            if c == "0":
                print(f"\n{GOLD}👋 Sampai jumpa, Operator!{RESET}\n"); break
            elif c == "1": run("python ~/zuhri_os/id/zuhri_id.py show")
            elif c == "2": run("python ~/zuhri_os/passport/zuhri_passport.py")
            elif c == "3": run("python ~/zuhri_os/crypto/zuhri_crypto.py")
            elif c == "4": run("python ~/zuhri_os/security/security_shield.py")
            elif c == "5": run("python ~/kosmik/p2p/mesh_node.py")
            elif c == "6": run("python ~/kosmik/p2p/mesh_discovery.py")
            elif c == "7": run("python ~/kosmik/sos_beacon.py beacon")
            elif c == "8": run("ai")
            elif c == "9": run("python ~/kosmik/vision/edge_vision.py")
            elif c == "10": run("python ~/zuhri_os/translator/translator.py")
            elif c == "12": run("python ~/zuhri_os/vote/zuhri_vote.py")
            elif c == "13": run("python ~/zuhri_os/contract/zuhri_contract.py")
            elif c == "14": run("python ~/zuhri_os/finance/zuhri_finance.py")
            elif c == "15": run("python ~/zuhri_os/wallet/wallet.py")
            elif c == "16": run("python ~/zuhri_os/edu/zuhri_edu.py")
            elif c == "17": run("python ~/zuhri_os/library/zuhri_library.py")
            elif c == "18": run("python ~/zuhri_os/zuhri_os.py")
            elif c == "19": run("python ~/health.py")
            elif c == "20": run("python ~/zuhri_os/backup/backup_manager.py")
            elif c == "21": run("python ~/zuhri_os/kurikulum/zuhri_kurikulum.py")
            elif c == "22": run("python ~/zuhri_os/peringatan/zuhri_peringatan.py")
            elif c == "23": run("python ~/zuhri_os/onboarding/welcome.py")
            elif c == "24": run("python ~/zuhri_os/spiritual/zuhri_spiritual.py")
            elif c == "25": run("python ~/zuhri_os/frekuensi/zuhri_frekuensi.py")
            elif c == "26": run("python ~/zuhri_os/predictive/zuhri_predictive.py")
            elif c == "27": run("python ~/zuhri_os/energi/zuhri_energi.py")
            elif c == "28": run("python ~/zuhri_os/botnet/zuhri_botnet.py")
            elif c == "29": run("python ~/zuhri_os/chain/zuhri_chain.py")
            elif c == "30": run("python ~/zuhri_os/did/zuhri_did.py")
            elif c == "31": run("python ~/zuhri_os/enkripsi/zuhri_enkripsi.py")
            elif c == "32": run("python ~/zuhri_os/autoroute/zuhri_autoroute.py")
            elif c == "33": run("python ~/zuhri_os/docs/zuhri_docs.py")
            elif c == "34": run("bash ~/zuhri_os/deepaccess/zuhri-deep")
            elif c == "35": run("bash ~/zuhri_os/darkweb/dark-web")
            elif c == "36": run("bash ~/zuhri_os/formalism/zuhri-search")
            elif c == "37": run("bash ~/zuhri_os/formalism/zuhri-search")
            elif c == "38": run("python ~/zuhri_os/tradisional/zuhri_tradisional.py")
            elif c == "39": run("python ~/zuhri_os/echocore/zuhri_echocore.py")
            elif c == "40": run("python ~/zuhri_os/torshield/zuhri_torshield.py")
            elif c == "41": run("python ~/zuhri_os/social/zuhri_social.py")
            elif c == "42": run("python ~/zuhri_os/web3hub/zuhri_web3.py")
            elif c == "43": run("python ~/zuhri_os/web4/zuhri_web4.py")
            elif c == "44": run("python ~/zuhri_os/finansialultimate/zuhri_finansialultimate.py")
            elif c == "45": run("python ~/zuhri_os/community/zuhri_community.py")
            else: print(f"{RED}  ❌ Pilihan tidak valid{RESET}")
            if c != "0":
                input(f"\n{DIM}  Tekan Enter untuk kembali...{RESET}")
        except KeyboardInterrupt:
            print(f"\n{GOLD}👋 Sampai jumpa, Operator!{RESET}\n"); break

if __name__ == "__main__":
    main()
