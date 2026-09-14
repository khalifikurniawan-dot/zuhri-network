#!/data/data/com.termux/files/usr/bin/bash
# ZUHRI TOR FAST v2.0 — Cepat Aktif + Keamanan Berlapis

CONF_DIR="$HOME/zuhri_os/torfast/config"
LOG_DIR="$HOME/zuhri_os/torfast/logs"
mkdir -p "$CONF_DIR" "$LOG_DIR"

RESET='\033[0m'; BOLD='\033[1m'; DIM='\033[2m'
RED='\033[91m'; GREEN='\033[92m'; YELLOW='\033[93m'
CYAN='\033[96m'; GOLD='\033[93m'

# ===== CEK TOR =====
if ! command -v tor > /dev/null 2>&1; then
    echo -e "${YELLOW}📥 Install Tor...${RESET}"
    pkg install tor torsocks -y
fi

# ===== KONFIGURASI TOR CEPAT =====
cat > "$CONF_DIR/torrc" << 'EOF'
# ZUHRI TOR FAST CONFIG
SocksPort 9050
ControlPort 9051
Log notice file /data/data/com.termux/files/home/zuhri_os/torfast/logs/tor.log

# Optimization: Faster bootstrap
CircuitBuildTimeout 10
LearnCircuitBuildTimeout 0
NumEntryGuards 3
KeepalivePeriod 60
NewCircuitPeriod 30
MaxCircuitDirtiness 600

# Performance
ConnectionPadding 0
ReducedConnectionPadding 1
UseEntryGuards 1
StrictNodes 0

# Bridge (opsional — untuk bypass blokir)
# UseBridges 1
EOF

# ===== FUNGSI START TOR =====
start_tor_fast() {
    # Cek sudah jalan?
    if pgrep -x "tor" > /dev/null; then
        IP=$(torsocks curl -s --max-time 5 ifconfig.me 2>/dev/null)
        if [ -n "$IP" ] && [[ ! "$IP" == *"<"* ]]; then
            echo -e "${GREEN}✅ Tor sudah aktif — IP: $IP${RESET}"
            return 0
        fi
    fi
    
    # Kill Tor lama
    pkill -x tor 2>/dev/null
    sleep 1
    
    # Start Tor baru
    echo -e "${CYAN}🚀 Menjalankan Tor Cepat...${RESET}"
    nohup tor -f "$CONF_DIR/torrc" > /dev/null 2>&1 &
    
    # Wait + monitor (max 20 detik)
    echo -e "${DIM}Bootstrap (max 20 detik)...${RESET}"
    for i in $(seq 1 20); do
        sleep 1
        IP=$(torsocks curl -s --max-time 2 ifconfig.me 2>/dev/null)
        if [ -n "$IP" ] && [[ ! "$IP" == *"<"* ]]; then
            echo -e "${GREEN}✅ Tor aktif dalam ${i}s — IP: $IP${RESET}"
            return 0
        fi
        echo -ne "\r${DIM}   ${i}s${RESET}"
    done
    
    echo ""
    echo -e "${YELLOW}⚠️  Tor lambat. Coba bridge mode?${RESET}"
    return 1
}

# ===== FUNGSI BRIDGE MODE (Kalau diblokir) =====
start_tor_bridge() {
    echo -e "${CYAN}🌉 Menggunakan Bridge Mode...${RESET}"
    
    cat > "$CONF_DIR/torrc" << 'EOF'
SocksPort 9050
ControlPort 9051
Log notice file /data/data/com.termux/files/home/zuhri_os/torfast/logs/tor.log
UseBridges 1
ClientTransportPlugin obfs4 exec /data/data/com.termux/files/usr/bin/obfs4proxy
Bridge obfs4 192.95.36.142:443 CDF2E852BF539B82BD10E27E9115A31734E378C2 cert=qUVQ0srL1JI/vO6V6m/24anYXiJD3+N/OA7W+9jXMxKNZ7qc8YhJrGgg
EOF
    
    pkill -x tor 2>/dev/null
    sleep 1
    nohup tor -f "$CONF_DIR/torrc" > /dev/null 2>&1 &
    
    for i in $(seq 1 30); do
        sleep 1
        IP=$(torsocks curl -s --max-time 2 ifconfig.me 2>/dev/null)
        if [ -n "$IP" ] && [[ ! "$IP" == *"<"* ]]; then
            echo -e "${GREEN}✅ Tor Bridge aktif — IP: $IP${RESET}"
            return 0
        fi
    done
    echo -e "${RED}❌ Bridge gagal${RESET}"
    return 1
}

# ===== CEK STATUS =====
status_tor() {
    if pgrep -x "tor" > /dev/null; then
        IP=$(torsocks curl -s --max-time 5 ifconfig.me 2>/dev/null)
        echo -e "${GREEN}✅ Tor: AKTIF${RESET}"
        echo -e "  IP: ${GOLD}$IP${RESET}"
        echo -e "  PID: $(pgrep -x tor)"
    else
        echo -e "${RED}❌ Tor: MATI${RESET}"
    fi
}

# ===== MAIN =====
case "$1" in
    start) start_tor_fast ;;
    bridge) start_tor_bridge ;;
    status) status_tor ;;
    stop)
        pkill -x tor
        echo -e "${YELLOW}🛑 Tor dihentikan${RESET}"
        ;;
    *)
        echo "Usage: tor-fast {start|bridge|status|stop}"
        start_tor_fast
        ;;
esac
