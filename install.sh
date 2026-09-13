#!/data/data/com.termux/files/usr/bin/bash
# ZUHRI NETWORK — AUTO INSTALLER v1.5
# Download dari GitHub

GITHUB_REPO="https://github.com/khalifikurniawan-dot/zuhri-network/archive/refs/heads/main.tar.gz"

clear
echo "🌌 ZUHRI NETWORK — INSTALLER v1.5"
echo ""

echo "[1/6] Update repository..."
pkg update -y > /dev/null 2>&1

echo "[2/6] Install dependensi..."
pkg install -y python python-pip git curl wget tar openssl tor torsocks lynx > /dev/null 2>&1

echo "[3/6] Install Python library..."
pip install --quiet cryptography p2pnetwork requests PyPDF2 2>/dev/null

echo "[4/6] Download Zuhri Network dari GitHub..."
cd ~
rm -f zuhri.tar.gz
rm -rf zuhri-network-main
wget -q -O zuhri.tar.gz "$GITHUB_REPO" 2>/dev/null

if [ ! -f zuhri.tar.gz ]; then
    echo "❌ Gagal download"
    exit 1
fi

tar -xzf zuhri.tar.gz
rm zuhri.tar.gz

echo "[5/6] Install modul..."
mkdir -p ~/zuhri_os ~/kosmik ~/kosmik/p2p
SRC=~/zuhri-network-main/modules

if [ -d "$SRC" ]; then
    [ -d "$SRC/zuhri_os" ] && cp -r $SRC/zuhri_os/* ~/zuhri_os/
    [ -d "$SRC/kosmik" ] && cp -r $SRC/kosmik/* ~/kosmik/
    [ -f "$SRC/zuhri.py" ] && cp $SRC/zuhri.py ~/
    [ -f "$SRC/health.py" ] && cp $SRC/health.py ~/
    echo "✅ Modul dicopy"
else
    echo "❌ Folder modules tidak ada"
    exit 1
fi

echo "[6/6] Setup alias..."
cp ~/.bashrc ~/.bashrc.backup_$(date +%Y%m%d_%H%M%S) 2>/dev/null
sed -i '/# ===== ZUHRI NETWORK/d' ~/.bashrc

cat >> ~/.bashrc << 'EOF'

# ===== ZUHRI NETWORK =====
alias ekosistem_zuhri="python ~/zuhri_os/menu.py"
alias ez="python ~/zuhri_os/menu.py"
alias z="python ~/zuhri_os/autoroute/zuhri_autoroute.py"
alias id="python ~/zuhri_os/id/zuhri_id.py"
alias crypto="python ~/zuhri_os/crypto/zuhri_crypto.py"
alias enkripsi="python ~/zuhri_os/enkripsi/zuhri_enkripsi.py"
alias mesh="python ~/kosmik/p2p/mesh_node.py"
alias sos="python ~/kosmik/sos_beacon.py beacon"
alias vote="python ~/zuhri_os/vote/zuhri_vote.py"
alias contract="python ~/zuhri_os/contract/zuhri_contract.py"
alias finance="python ~/zuhri_os/finance/zuhri_finance.py"
alias wallet="python ~/zuhri_os/wallet/wallet.py"
alias edu="python ~/zuhri_os/edu/zuhri_edu.py"
alias library="python ~/zuhri_os/library/zuhri_library.py"
alias kurikulum="python ~/zuhri_os/kurikulum/zuhri_kurikulum.py"
alias chain="python ~/zuhri_os/chain/zuhri_chain.py"
alias did="python ~/zuhri_os/did/zuhri_did.py"
alias botnet="python ~/zuhri_os/botnet/zuhri_botnet.py"
alias spiritual="python ~/zuhri_os/spiritual/zuhri_spiritual.py"
alias peringatan="python ~/zuhri_os/peringatan/zuhri_peringatan.py"
alias frekuensi="python ~/zuhri_os/frekuensi/zuhri_frekuensi.py"
alias predictive="python ~/zuhri_os/predictive/zuhri_predictive.py"
alias energi="python ~/zuhri_os/energi/zuhri_energi.py"
alias backup="python ~/zuhri_os/backup/backup_manager.py backup"
alias restore="python ~/zuhri_os/backup/backup_manager.py restore"
alias list-backup="python ~/zuhri_os/backup/backup_manager.py list"
alias docs="python ~/zuhri_os/docs/zuhri_docs.py"
alias panduan="python ~/zuhri_os/onboarding/welcome.py"
alias health="python ~/health.py"

export PYTHONPATH="$HOME/zuhri_os:$HOME/zuhri_os/id:$HOME/kosmik:$HOME/kosmik/p2p:$PYTHONPATH"
EOF

source ~/.bashrc 2>/dev/null

rm -rf ~/zuhri-network-main
echo ""
echo "✅ ZUHRI NETWORK SIAP!"
echo "Ketik: ekosistem_zuhri"
