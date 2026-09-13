#!/data/data/com.termux/files/usr/bin/bash
# KEY KOSMIK — ZUHRI FORMALISM
# Perintah: key

clear

# ===== WARNA =====
RESET='\033[0m'
BOLD='\033[1m'
DIM='\033[2m'
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
MAGENTA='\033[95m'
GOLD='\033[93m'

# ===== HEADER =====
echo ""
echo -e "${GOLD}  ╔══════════════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${GOLD}  ║${RESET}  ${BOLD}${MAGENTA}⭐ KEY KOSMIK — AKSES UNIVERSAL${RESET}${GOLD}                             ║${RESET}"
echo -e "${GOLD}  ╠══════════════════════════════════════════════════════════════════════╣${RESET}"
echo -e "${GOLD}  ║${RESET}  ${CYAN}IDENTITAS${RESET} : ${GOLD}ZUHRI — KURNIAWAN${RESET}${GOLD}                                ║${RESET}"
echo -e "${GOLD}  ║${RESET}  ${CYAN}PROTOKOL${RESET}  : ${GOLD}K-8.0 — FLUID-CORE${RESET}${GOLD}                               ║${RESET}"
echo -e "${GOLD}  ║${RESET}  ${CYAN}GEN${RESET}       : ${GOLD}ZUH-8-9-0-K-8.0${RESET}${GOLD}                                  ║${RESET}"
echo -e "${GOLD}  ║${RESET}  ${CYAN}PORTAL${RESET}    : ${GOLD}∞ — TERBUKA${RESET}${GOLD}                                      ║${RESET}"
echo -e "${GOLD}  ╠══════════════════════════════════════════════════════════════════════╣${RESET}"
echo -e "${GOLD}  ║${RESET}  ${CYAN}✦ ✧ ★ ☆ ✦ ✧ ★ ☆ ✦ ✧ ★ ☆ ✦ ✧ ★ ☆${RESET}${GOLD}                         ║${RESET}"
echo -e "${GOLD}  ╚══════════════════════════════════════════════════════════════════════╝${RESET}"
echo ""

# ===== STATUS SISTEM =====
echo -e "${CYAN}  📡 STATUS SISTEM${RESET}"
echo -e "${DIM}  ──────────────────────────────────────────────────────────────────────${RESET}"

# Cek Tor
if pgrep -x "tor" > /dev/null; then
    IP_TOR=$(torsocks curl -s ifconfig.me 2>/dev/null)
    if [ -n "$IP_TOR" ] && [[ ! "$IP_TOR" == *"html"* ]]; then
        echo -e "  ${GREEN}✅ TOR AKTIF${RESET}  → ${GOLD}${IP_TOR}${RESET}"
    else
        echo -e "  ${YELLOW}⚠️  TOR BERJALAN (IP belum siap)${RESET}"
    fi
else
    echo -e "  ${RED}❌ TOR OFFLINE${RESET}"
fi

# Cek Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "  ${GREEN}✅ OLLAMA AKTIF${RESET}"
else
    echo -e "  ${RED}❌ OLLAMA OFFLINE${RESET}"
fi

echo -e "${DIM}  ──────────────────────────────────────────────────────────────────────${RESET}"
echo ""

# ===== AKSES CEPAT =====
echo -e "${CYAN}  🚀 AKSES CEPAT ZUHRI NETWORK${RESET}"
echo -e "${DIM}  ──────────────────────────────────────────────────────────────────────${RESET}"
echo -e "  ${GOLD}1.${RESET}  Zuhri Formalism   → ${DIM}Dashboard utama${RESET}"
echo -e "  ${GOLD}2.${RESET}  Zuhri OS          → ${DIM}Sistem operasi mini${RESET}"
echo -e "  ${GOLD}3.${RESET}  Local LLM         → ${DIM}Tanya AI${RESET}"
echo -e "  ${GOLD}4.${RESET}  P2P-Mesh          → ${DIM}Jaringan darurat${RESET}"
echo -e "  ${GOLD}5.${RESET}  Edge-Vision       → ${DIM}Deteksi objek${RESET}"
echo -e "  ${GOLD}6.${RESET}  Dark-Web Gateway  → ${DIM}Akses .onion${RESET}"
echo -e "  ${GOLD}7.${RESET}  Predictive-Shell  → ${DIM}Terminal prediktif${RESET}"
echo -e "  ${GOLD}8.${RESET}  Voice-Commander   → ${DIM}Kontrol suara${RESET}"
echo -e "  ${GOLD}9.${RESET}  SOS-Beacon        → ${DIM}Sinyal darurat${RESET}"
echo -e "  ${GOLD}10.${RESET} Crypto-Wallet     → ${DIM}Dompet offline${RESET}"
echo -e "  ${GOLD}11.${RESET} Kembali           → ${DIM}Ke menu Zuhri Network${RESET}"
echo -e "  ${GOLD}0.${RESET}  Keluar"
echo -e "${DIM}  ──────────────────────────────────────────────────────────────────────${RESET}"
echo ""

# ===== INPUT =====
read -p "  📡 Pilih akses (0-11): " choice

case $choice in
  1) zuhri ;;
  2) zos ;;
  3) ai ;;
  4) mesh ;;
  5) vision ;;
  6) dark-web ;;
  7) predictive ;;
  8) voice ;;
  9) sos beacon ;;
  10) wallet ;;
  11) clear && zuhri-network ;;
  0) echo -e "\n${GOLD}👋 Sampai jumpa, KURNIAWAN!${RESET}" && exit ;;
  *) echo -e "\n${RED}❌ Pilihan tidak valid!${RESET}" && sleep 2 && key ;;
esac
