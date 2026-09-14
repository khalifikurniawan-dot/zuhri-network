#!/data/data/com.termux/files/usr/bin/bash
# ZUHRI NETWORK — AUTO INSTALLER v1.6
# Dengan perbaikan Tor config

GITHUB_REPO="https://github.com/khalifikurniawan-dot/zuhri-network/archive/refs/heads/main.tar.gz"

clear
echo ""
echo "  ╔══════════════════════════════════════════════════════════════════╗"
echo "  ║  🌌 ZUHRI NETWORK — AUTO INSTALLER v1.6                          ║"
echo "  ║  Protokol: K-8.0                                                ║"
echo "  ╚══════════════════════════════════════════════════════════════════╝"
echo ""
read -p "  Tekan Enter untuk mulai..."

echo ""
echo "  [1/8] Update repository..."
pkg update -y > /dev/null 2>&1

echo "  [2/8] Install dependensi..."
pkg install -y python python-pip git curl wget tar openssl tor torsocks lynx proxychains-ng obfs4proxy > /dev/null 2>&1

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
    [ -d "$SRC/echocore" ] && mkdir -p ~/zuhri_os/echocore && cp -r $SRC/echocore/* ~/zuhri_os/echocore/
    [ -d "$SRC/torshield" ] && mkdir -p ~/zuhri_os/torshield && cp -r $SRC/torshield/* ~/zuhri_os/torshield/
    [ -d "$SRC/social" ] && mkdir -p ~/zuhri_os/social && cp -r $SRC/social/* ~/zuhri_os/social/
    [ -d "$SRC/web3hub" ] && mkdir -p ~/zuhri_os/web3hub && cp -r $SRC/web3hub/* ~/zuhri_os/web3hub/
    [ -d "$SRC/web4" ] && mkdir -p ~/zuhri_os/web4 && cp -r $SRC/web4/* ~/zuhri_os/web4/
    [ -d "$SRC/tradisional" ] && mkdir -p ~/zuhri_os/tradisional && cp -r $SRC/tradisional/* ~/zuhri_os/tradisional/
    [ -d "$SRC/peringatan" ] && mkdir -p ~/zuhri_os/peringatan && cp -r $SRC/peringatan/* ~/zuhri_os/peringatan/
    [ -d "$SRC/spiritual" ] && mkdir -p ~/zuhri_os/spiritual && cp -r $SRC/spiritual/* ~/zuhri_os/spiritual/
    [ -d "$SRC/frekuensi" ] && mkdir -p ~/zuhri_os/frekuensi && cp -r $SRC/frekuensi/* ~/zuhri_os/frekuensi/
    [ -d "$SRC/predictive" ] && mkdir -p ~/zuhri_os/predictive && cp -r $SRC/predictive/* ~/zuhri_os/predictive/
    [ -d "$SRC/energi" ] && mkdir -p ~/zuhri_os/energi && cp -r $SRC/energi/* ~/zuhri_os/energi/
    [ -d "$SRC/botnet" ] && mkdir -p ~/zuhri_os/botnet && cp -r $SRC/botnet/* ~/zuhri_os/botnet/
    [ -d "$SRC/chain" ] && mkdir -p ~/zuhri_os/chain && cp -r $SRC/chain/* ~/zuhri_os/chain/
    [ -d "$SRC/did" ] && mkdir -p ~/zuhri_os/did && cp -r $SRC/did/* ~/zuhri_os/did/
    [ -d "$SRC/enkripsi" ] && mkdir -p ~/zuhri_os/enkripsi && cp -r $SRC/enkripsi/* ~/zuhri_os/enkripsi/
    [ -f "$SRC/zuhri.py" ] && cp $SRC/zuhri.py ~/
    [ -f "$SRC/health.py" ] && cp $SRC/health.py ~/
    [ -f "$SRC/updater.py" ] && cp $SRC/updater.py ~/
    echo "        ✅ Modul dicopy"
else
    echo "        ❌ Folder modules tidak ada"
    exit 1
fi

echo "  [6/8] Setup Tor config (STABIL)..."
mkdir -p ~/zuhri_os/torshield/config

cat > ~/zuhri_os/torshield/config/torrc << 'EOF'
# ZUHRI TOR SHIELD — CONFIG STABIL
SocksPort 9050
ControlPort 9051
DataDirectory /data/data/com.termux/files/home/zuhri_os/torshield/config/tor-data
Log notice file /data/data/com.termux/files/home/zuhri_os/torshield/config/tor.log
Log notice stdout
ClientOnly 1
AvoidDiskWrites 1
CircuitBuildTimeout 60
LearnCircuitBuildTimeout 0
NumEntryGuards 3
KeepalivePeriod 60
NewCircuitPeriod 30
MaxCircuitDirtiness 600
EOF

echo "        ✅ Tor config dibuat"

echo "  [7/8] Setup alias..."
cp ~/.bashrc ~/.bashrc.backup_$(date +%Y%m%d_%H%M%S) 2>/dev/null
sed -i '/# ===== ZUHRI NETWORK/d' ~/.bashrc
for a in ekosistem_zuhri ez z id crypto enkripsi mesh mesh-scan sos vote contract passport finance wallet edu library lib kurikulum chain did botnet hunter spiritual peringatan frekuensi predictive energi backup restore list-backup verify-backup export-backup docs panduan health dark-web darkweb deep zuhri-deep zuhri-search zsearch echocore echo-core quantum torshield tsh social zsocial web3 zweb3 web4 agent tradisional herbal jamu; do
    sed -i "/^alias $a=/d" ~/.bashrc
done

cat >> ~/.bashrc << 'EOF'

# ===== ZUHRI NETWORK v1.6 =====
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
alias dark-web="bash ~/zuhri_os/darkweb/dark-web"
alias darkweb="bash ~/zuhri_os/darkweb/dark-web"
alias deep="bash ~/zuhri_os/deepaccess/zuhri-deep"
alias zuhri-deep="bash ~/zuhri_os/deepaccess/zuhri-deep"
alias zuhri-search="bash ~/zuhri_os/formalism/zuhri-search"
alias zsearch="bash ~/zuhri_os/formalism/zuhri-search"
alias echocore="python ~/zuhri_os/echocore/zuhri_echocore.py"
alias echo-core="python ~/zuhri_os/echocore/zuhri_echocore.py"
alias quantum="python ~/zuhri_os/echocore/zuhri_echocore.py"
alias torshield="python ~/zuhri_os/torshield/zuhri_torshield.py"
alias tsh="python ~/zuhri_os/torshield/zuhri_torshield.py"
alias social="python ~/zuhri_os/social/zuhri_social.py"
alias zsocial="python ~/zuhri_os/social/zuhri_social.py"
alias web3="python ~/zuhri_os/web3hub/zuhri_web3.py"
alias zweb3="python ~/zuhri_os/web3hub/zuhri_web3.py"
alias web4="python ~/zuhri_os/web4/zuhri_web4.py"
alias agent="python ~/zuhri_os/web4/zuhri_web4.py"
alias tradisional="python ~/zuhri_os/tradisional/zuhri_tradisional.py"
alias herbal="python ~/zuhri_os/tradisional/zuhri_tradisional.py"
alias jamu="python ~/zuhri_os/tradisional/zuhri_tradisional.py"

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

# Copy dark-web ke PATH
[ -f ~/zuhri_os/darkweb/dark-web ] && cp ~/zuhri_os/darkweb/dark-web $PREFIX/bin/dark-web && chmod +x $PREFIX/bin/dark-web

clear
echo ""
echo "  ╔══════════════════════════════════════════════════════════════════╗"
echo "  ║                                                                  ║"
echo "  ║        ✅ ZUHRI NETWORK v1.6 — SIAP!                            ║"
echo "  ║                                                                  ║"
echo "  ╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "  📋 LANGKAH SELANJUTNYA:"
echo ""
echo "    1. Keluar Termux : exit"
echo "    2. Buka Termux lagi"
echo "    3. Ketik         : ekosistem_zuhri"
echo ""
echo "  🔧 UNTUK TOR:"
echo ""
echo "    1. Jalankan Tor  : tor -f ~/zuhri_os/torshield/config/torrc"
echo "    2. Tunggu 100%   : Bootstrapped 100%"
echo "    3. Test          : torsocks curl ifconfig.me"
echo ""
