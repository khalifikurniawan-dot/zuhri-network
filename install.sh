#!/data/data/com.termux/files/usr/bin/bash
# ZUHRI NETWORK — AUTO INSTALLER v1.5

GITHUB_REPO="https://github.com/khalifikurniawan-dot/zuhri-network/archive/refs/heads/main.tar.gz"

clear
echo ""
echo "  ╔══════════════════════════════════════════════════════════════════╗"
echo "  ║  🌌 ZUHRI NETWORK — AUTO INSTALLER v1.5                          ║"
echo "  ║  Protokol: K-8.0                                                ║"
echo "  ╚══════════════════════════════════════════════════════════════════╝"
echo ""
read -p "  Tekan Enter untuk mulai..."

echo ""
echo "  [1/8] Update repository..."
pkg update -y > /dev/null 2>&1

echo "  [2/8] Install dependensi..."
pkg install -y python python-pip git curl wget tar openssl tor torsocks lynx > /dev/null 2>&1

echo "  [3/8] Install Python library..."
pip install --quiet cryptography p2pnetwork requests PyPDF2 2>/dev/null

echo "  [4/8] Download Zuhri Network dari GitHub..."
cd ~
rm -f zuhri.tar.gz
rm -rf zuhri-network-main
wget -q -O zuhri.tar.gz "$GITHUB_REPO" 2>/dev/null

if [ ! -f zuhri.tar.gz ]; then
    echo "        ❌ Gagal download. Cek internet."
    exit 1
fi

tar -xzf zuhri.tar.gz
rm zuhri.tar.gz
echo "        ✅ Download selesai"

echo "  [5/8] Install modul..."
mkdir -p ~/zuhri_os ~/kosmik ~/kosmik/p2p

SRC=~/zuhri-network-main/modules

if [ -d "$SRC" ]; then
    [ -d "$SRC/zuhri_os" ] && cp -r $SRC/zuhri_os/* ~/zuhri_os/
    [ -d "$SRC/kosmik" ] && cp -r $SRC/kosmik/* ~/kosmik/
    [ -d "$SRC/darkweb" ] && mkdir -p ~/zuhri_os/darkweb && cp -r $SRC/darkweb/* ~/zuhri_os/darkweb/
    [ -d "$SRC/deepaccess" ] && mkdir -p ~/zuhri_os/deepaccess && cp -r $SRC/deepaccess/* ~/zuhri_os/deepaccess/
    [ -d "$SRC/formalism" ] && mkdir -p ~/zuhri_os/formalism && cp -r $SRC/formalism/* ~/zuhri_os/formalism/
    [ -f "$SRC/zuhri.py" ] && cp $SRC/zuhri.py ~/
    [ -f "$SRC/health.py" ] && cp $SRC/health.py ~/
    echo "        ✅ Modul dicopy"
else
    echo "        ❌ Folder modules tidak ada"
    exit 1
fi

echo "  [6/8] Install Dark-Web, Deep Access, Formalism..."
chmod +x ~/zuhri_os/darkweb/dark-web 2>/dev/null
chmod +x ~/zuhri_os/deepaccess/zuhri-deep 2>/dev/null
chmod +x ~/zuhri_os/formalism/zuhri-search 2>/dev/null

# Copy ke PATH
[ -f ~/zuhri_os/darkweb/dark-web ] && cp ~/zuhri_os/darkweb/dark-web $PREFIX/bin/dark-web && chmod +x $PREFIX/bin/dark-web
[ -f ~/zuhri_os/deepaccess/zuhri-deep ] && cp ~/zuhri_os/deepaccess/zuhri-deep $PREFIX/bin/zuhri-deep && chmod +x $PREFIX/bin/zuhri-deep
[ -f ~/zuhri_os/formalism/zuhri-search ] && cp ~/zuhri_os/formalism/zuhri-search $PREFIX/bin/zuhri-search && chmod +x $PREFIX/bin/zuhri-search
echo "        ✅ Done"

echo "  [7/8] Setup alias..."
cp ~/.bashrc ~/.bashrc.backup_$(date +%Y%m%d_%H%M%S) 2>/dev/null
sed -i '/# ===== ZUHRI NETWORK/d' ~/.bashrc
for a in ekosistem_zuhri ez z id crypto enkripsi mesh mesh-scan sos vote contract passport finance wallet edu library lib kurikulum chain did botnet hunter spiritual peringatan frekuensi predictive energi backup restore list-backup verify-backup export-backup docs panduan health dark-web darkweb deep zuhri-deep zuhri-search zsearch; do
    sed -i "/^alias $a=/d" ~/.bashrc
done

cat >> ~/.bashrc << 'EOF'

# ===== ZUHRI NETWORK v1.5 =====
alias ekosistem_zuhri="python ~/zuhri_os/menu.py"
alias ez="python ~/zuhri_os/menu.py"
alias z="python ~/zuhri_os/autoroute/zuhri_autoroute.py"
alias id="python ~/zuhri_os/id/zuhri_id.py"
alias crypto="python ~/zuhri_os/crypto/zuhri_crypto.py"
alias enkripsi="python ~/zuhri_os/enkripsi/zuhri_enkripsi.py"
alias mesh="python ~/kosmik/p2p/mesh_node.py"
alias mesh-scan="python ~/kosmik/p2p/mesh_discovery.py"
alias sos="python ~/kosmik/sos_beacon.py beacon"
alias vote="python ~/zuhri_os/vote/zuhri_vote.py"
alias contract="python ~/zuhri_os/contract/zuhri_contract.py"
alias passport="python ~/zuhri_os/passport/zuhri_passport.py"
alias finance="python ~/zuhri_os/finance/zuhri_finance.py"
alias wallet="python ~/zuhri_os/wallet/wallet.py"
alias edu="python ~/zuhri_os/edu/zuhri_edu.py"
alias library="python ~/zuhri_os/library/zuhri_library.py"
alias lib="python ~/zuhri_os/library/zuhri_library.py"
alias kurikulum="python ~/zuhri_os/kurikulum/zuhri_kurikulum.py"
alias chain="python ~/zuhri_os/chain/zuhri_chain.py"
alias did="python ~/zuhri_os/did/zuhri_did.py"
alias botnet="python ~/zuhri_os/botnet/zuhri_botnet.py"
alias hunter="python ~/zuhri_os/botnet/zuhri_botnet.py"
alias spiritual="python ~/zuhri_os/spiritual/zuhri_spiritual.py"
alias peringatan="python ~/zuhri_os/peringatan/zuhri_peringatan.py"
alias frekuensi="python ~/zuhri_os/frekuensi/zuhri_frekuensi.py"
alias predictive="python ~/zuhri_os/predictive/zuhri_predictive.py"
alias energi="python ~/zuhri_os/energi/zuhri_energi.py"
alias backup="python ~/zuhri_os/backup/backup_manager.py backup"
alias restore="python ~/zuhri_os/backup/backup_manager.py restore"
alias list-backup="python ~/zuhri_os/backup/backup_manager.py list"
alias verify-backup="python ~/zuhri_os/backup/backup_manager.py verify"
alias export-backup="python ~/zuhri_os/backup/backup_manager.py export"
alias docs="python ~/zuhri_os/docs/zuhri_docs.py"
alias panduan="python ~/zuhri_os/onboarding/welcome.py"
alias health="python ~/health.py"

# Dark-Web & Deep Access
alias dark-web="bash ~/zuhri_os/darkweb/dark-web"
alias darkweb="bash ~/zuhri_os/darkweb/dark-web"
alias deep="bash ~/zuhri_os/deepaccess/zuhri-deep"
alias zuhri-deep="bash ~/zuhri_os/deepaccess/zuhri-deep"
alias zuhri-search="bash ~/zuhri_os/formalism/zuhri-search"
alias zsearch="bash ~/zuhri_os/formalism/zuhri-search"

export PYTHONPATH="$HOME/zuhri_os:$HOME/zuhri_os/id:$HOME/kosmik:$HOME/kosmik/p2p:$PYTHONPATH"
EOF

source ~/.bashrc 2>/dev/null
echo "        ✅ Alias ditambahkan"

echo "  [8/8] Finalisasi..."
rm -rf ~/zuhri-network-main
chmod +x ~/zuhri_os/id/*.py 2>/dev/null
chmod +x ~/zuhri_os/crypto/*.py 2>/dev/null
chmod +x ~/zuhri_os/menu.py 2>/dev/null
chmod +x ~/kosmik/p2p/*.py 2>/dev/null

if ! pgrep -x "tor" > /dev/null; then
    nohup tor > /dev/null 2>&1 &
fi

clear
echo ""
echo "  ╔══════════════════════════════════════════════════════════════════╗"
echo "  ║                                                                  ║"
echo "  ║        ✅ ZUHRI NETWORK v1.5 — SIAP!                            ║"
echo "  ║                                                                  ║"
echo "  ╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "  📋 LANGKAH SELANJUTNYA:"
echo ""
echo "    1. Keluar Termux : exit"
echo "    2. Buka Termux lagi"
echo "    3. Ketik         : ekosistem_zuhri"
echo ""
echo "  📡 PERINTAH BARU:"
echo ""
echo "    dark-web          → Dark-Web Gateway"
echo "    deep              → Deep Access (Layer 2 & 3)"
echo "    zuhri-search      → Formalism Search (Layer 4)"
echo ""
