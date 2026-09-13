#!/data/data/com.termux/files/usr/bin/bash
# ZUHRI NETWORK — AUTO INSTALLER v1.5

clear
echo "🌌 ZUHRI NETWORK — AUTO INSTALLER v1.5"
echo "======================================="
echo ""

echo "[1/6] Update repository..."
pkg update -y > /dev/null 2>&1

echo "[2/6] Install dependensi..."
pkg install -y python python-pip git curl wget tar openssl tor torsocks lynx > /dev/null 2>&1

echo "[3/6] Install Python library..."
pip install --quiet cryptography p2pnetwork requests 2>/dev/null

echo "[4/6] Install modul..."
mkdir -p ~/zuhri_os ~/kosmik

INSTALLER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -d "$INSTALLER_DIR/modules" ]; then
    cd "$INSTALLER_DIR/modules"
    [ -d "zuhri_os" ] && cp -r zuhri_os/* ~/zuhri_os/ 2>/dev/null
    [ -d "kosmik" ] && cp -r kosmik/* ~/kosmik/ 2>/dev/null
    [ -f "zuhri.py" ] && cp zuhri.py ~/
    [ -f "health.py" ] && cp health.py ~/
    echo "      ✅ Modul dicopy"
else
    echo "      ⚠️  Folder modules kosong"
fi

echo "[5/6] Setup alias..."
cat >> ~/.bashrc << 'EOF'

# ===== ZUHRI NETWORK =====
alias ekosistem_zuhri="python ~/zuhri_os/menu.py"
alias ez="python ~/zuhri_os/menu.py"
alias id="python ~/zuhri_os/id/zuhri_id.py"
alias crypto="python ~/zuhri_os/crypto/zuhri_crypto.py"
alias mesh="python ~/kosmik/p2p/mesh_node.py"
alias sos="python ~/kosmik/sos_beacon.py beacon"
alias docs="python ~/zuhri_os/docs/zuhri_docs.py"

export PYTHONPATH="$HOME/zuhri_os:$HOME/zuhri_os/id:$HOME/kosmik:$HOME/kosmik/p2p:$PYTHONPATH"
EOF

source ~/.bashrc 2>/dev/null

echo "[6/6] Selesai!"
echo ""
echo "✅ ZUHRI NETWORK SIAP!"
echo "Ketik: ekosistem_zuhri"
