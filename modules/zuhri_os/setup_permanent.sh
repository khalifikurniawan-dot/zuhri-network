#!/data/data/com.termux/files/usr/bin/bash
# ZUHRI NETWORK — SETUP PERMANEN TOTAL
# Protokol K-8.0 | Gen ZUH-8-9-0-K-8.0

clear
echo ""
echo "  ╔══════════════════════════════════════════════════════════════════╗"
echo "  ║  🔧 ZUHRI NETWORK — SETUP PERMANEN TOTAL                       ║"
echo "  ║  ──────────────────────────────────────────────────────────────  ║"
echo "  ║  Protokol : K-8.0 — FLUID-CORE                                ║"
echo "  ║  Status   : MEMPROSES...                                       ║"
echo "  ╚══════════════════════════════════════════════════════════════════╝"
echo ""

# ===== BACKUP .BASHRC =====
echo "[1/7] Backup .bashrc..."
cp ~/.bashrc ~/.bashrc.backup_$(date +%Y%m%d_%H%M%S)
echo "      ✅ Backup dibuat"
echo ""

# ===== BUAT FOLDER =====
echo "[2/7] Buat folder..."
mkdir -p ~/zuhri_os/id
mkdir -p ~/zuhri_os/crypto/vault
mkdir -p ~/zuhri_os/crypto/keys
mkdir -p ~/zuhri_os/backup/data
mkdir -p ~/zuhri_os/backup/manifests
mkdir -p ~/zuhri_os/logs
mkdir -p ~/kosmik/p2p
mkdir -p ~/kosmik/vision
mkdir -p ~/kosmik/voice
echo "      ✅ Folder dibuat"
echo ""

# ===== SYMLINK AUTH =====
echo "[3/7] Buat symlink Zuhri Auth..."
ln -sf ~/zuhri_os/id/zuhri_auth.py ~/zuhri_os/zuhri_auth.py
ln -sf ~/zuhri_os/id/zuhri_auth.py ~/kosmik/zuhri_auth.py
ln -sf ~/zuhri_os/id/zuhri_auth.py ~/kosmik/p2p/zuhri_auth.py
echo "      ✅ Symlink dibuat"
echo ""

# ===== EXPORT PYTHONPATH =====
echo "[4/7] Setup PYTHONPATH..."
if ! grep -q "PYTHONPATH" ~/.bashrc; then
    cat >> ~/.bashrc << 'EOF'

# ===== ZUHRI NETWORK — PYTHONPATH =====
export PYTHONPATH="$HOME/zuhri_os:$HOME/zuhri_os/id:$HOME/kosmik:$HOME/kosmik/p2p:$PYTHONPATH"
EOF
    echo "      ✅ PYTHONPATH ditambahkan"
else
    echo "      ✅ PYTHONPATH sudah ada"
fi
echo ""

# ===== HAPUS ALIAS LAMA =====
echo "[5/7] Bersihkan alias lama..."
sed -i '/# ===== ZUHRI NETWORK/d' ~/.bashrc
sed -i '/alias zuhri=/d' ~/.bashrc
sed -i '/alias zos=/d' ~/.bashrc
sed -i '/alias zuhri-os=/d' ~/.bashrc
sed -i '/alias key=/d' ~/.bashrc
sed -i '/alias crypto=/d' ~/.bashrc
sed -i '/alias shield=/d' ~/.bashrc
sed -i '/alias scan=/d' ~/.bashrc
sed -i '/alias wipe=/d' ~/.bashrc
sed -i '/alias ai=/d' ~/.bashrc
sed -i '/alias mesh=/d' ~/.bashrc
sed -i '/alias mesh-scan=/d' ~/.bashrc
sed -i '/alias vision=/d' ~/.bashrc
sed -i '/alias dark-web=/d' ~/.bashrc
sed -i '/alias predictive=/d' ~/.bashrc
sed -i '/alias voice=/d' ~/.bashrc
sed -i '/alias sos=/d' ~/.bashrc
sed -i '/alias wallet=/d' ~/.bashrc
sed -i '/alias health=/d' ~/.bashrc
sed -i '/alias version=/d' ~/.bashrc
sed -i '/alias update=/d' ~/.bashrc
sed -i '/alias backup=/d' ~/.bashrc
sed -i '/alias restore=/d' ~/.bashrc
sed -i '/alias list-backup=/d' ~/.bashrc
sed -i '/alias manifest=/d' ~/.bashrc
sed -i '/alias verify-backup=/d' ~/.bashrc
sed -i '/alias translate=/d' ~/.bashrc
sed -i '/alias id=/d' ~/.bashrc
sed -i '/alias id-backup=/d' ~/.bashrc
echo "      ✅ Alias lama dibersihkan"
echo ""

# ===== TAMBAHKAN SEMUA ALIAS =====
echo "[6/7] Tambahkan semua alias permanen..."
cat >> ~/.bashrc << 'EOF'

# ===== ZUHRI NETWORK — PERMANEN =====
# Autentikasi terpusat
alias id="python ~/zuhri_os/id/zuhri_id.py"
alias id-backup="python ~/zuhri_os/id/id_backup.py"
alias auth="python ~/zuhri_os/id/zuhri_auth.py"

# Inti sistem
alias zuhri="python ~/zuhri.py"
alias zos="python ~/zuhri_os/zuhri_os.py"
alias zuhri-os="python ~/zuhri_os/zuhri_os.py"
alias key="bash ~/kosmik/key.sh"

# Keamanan & Kripto
alias shield="python ~/zuhri_os/security/security_shield.py"
alias scan="python ~/zuhri_os/security/security_shield.py scan"
alias wipe="python ~/zuhri_os/security/security_shield.py wipe"
alias crypto="python ~/zuhri_os/crypto/zuhri_crypto.py"

# AI
alias ai='ollama run tinyllama "Jawab dalam Bahasa Indonesia. "'

# Jaringan
alias mesh="python ~/kosmik/p2p/mesh_node.py"
alias mesh-scan="python ~/kosmik/p2p/mesh_discovery.py"

# Visi & Suara
alias vision="python ~/kosmik/vision/edge_vision.py"
alias voice="python ~/kosmik/voice/voice_commander.py"

# Dark Web
alias dark-web="dark-web"

# Prediktif
alias predictive="python ~/kosmik/predictive_shell.py"

# Darurat
alias sos="python ~/kosmik/sos_beacon.py"

# Keuangan
alias wallet="python ~/zuhri_os/wallet/wallet.py"

# Sistem
alias health="python ~/health.py"
alias version="python ~/zuhri_os/version/version_monitor.py"
alias update="python ~/updater.py"
alias backup="python ~/zuhri_os/backup/backup_manager.py backup"
alias restore="python ~/zuhri_os/backup/backup_manager.py restore"
alias list-backup="python ~/zuhri_os/backup/backup_manager.py list"
alias manifest="python ~/zuhri_os/backup/backup_manager.py manifest"
alias verify-backup="python ~/zuhri_os/backup/backup_manager.py verify"

# Bahasa
alias translate="python ~/zuhri_os/translator/translator.py"

# ===== AUTO-START =====
# Auto-start Tor (opsional)
if ! pgrep -x "tor" > /dev/null; then
    nohup tor > /dev/null 2>&1 &
    sleep 2
fi
EOF
echo "      ✅ Semua alias ditambahkan"
echo ""

# ===== RELOAD =====
echo "[7/7] Reload .bashrc..."
source ~/.bashrc 2>/dev/null
echo "      ✅ Reload selesai"
echo ""

echo "  ╔══════════════════════════════════════════════════════════════════╗"
echo "  ║  ✅ SEMUA MODUL PERMANEN!                                      ║"
echo "  ║  ──────────────────────────────────────────────────────────────  ║"
echo "  ║  Status  : READY                                               ║"
echo "  ║  Operator: KURNIAWAN                                           ║"
echo "  ║  Protocol: K-8.0 — FLUID-CORE                                  ║"
echo "  ║  Gen     : ZUH-8-9-0-K-8.0                                    ║"
echo "  ╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "  📋 DAFTAR PERINTAH PERMANEN:"
echo ""
echo "  🆔  Identitas     : id | id-backup | auth"
echo "  🌌  Inti          : zuhri | zos | key"
echo "  🔐  Keamanan      : shield | crypto"
echo "  🧠  AI            : ai"
echo "  📡  Jaringan      : mesh | mesh-scan"
echo "  🔍  Visi          : vision"
echo "  🎤  Suara         : voice"
echo "  🌑  Dark Web      : dark-web"
echo "  🔮  Prediktif     : predictive"
echo "  🆘  Darurat       : sos"
echo "  💰  Keuangan      : wallet"
echo "  💻  Sistem        : health | version | update"
echo "  💾  Backup        : backup | restore | list-backup | manifest | verify-backup"
echo "  🌍  Bahasa        : translate"
echo ""
echo "  ✅ Semua perintah siap dipakai kapan saja!"
echo ""
