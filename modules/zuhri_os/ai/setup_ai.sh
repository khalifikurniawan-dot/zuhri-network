#!/data/data/com.termux/files/usr/bin/bash
# ZUHRI AI — AUTO SETUP OLLAMA + PHI

clear
echo ""
echo "  ╔══════════════════════════════════════════════════════════════════╗"
echo "  ║  🧠 ZUHRI AI — AUTO SETUP                                       ║"
echo "  ║  ──────────────────────────────────────────────────────────────  ║"
echo "  ║  Akan menginstall:                                              ║"
echo "  ║  • Ollama (runtime AI)                                          ║"
echo "  ║  • Model phi (50 MB)                                            ║"
echo "  ╚══════════════════════════════════════════════════════════════════╝"
echo ""
read -p "  Tekan Enter untuk mulai..."

# STEP 1 — CEK OLLAMA
echo ""
echo "[1/4] Cek Ollama..."

if command -v ollama > /dev/null 2>&1; then
    echo "      ✅ Ollama sudah terinstall"
else
    echo "      📥 Install Ollama..."
    pkg install -y ollama 2>&1 | tail -2
    
    if ! command -v ollama > /dev/null 2>&1; then
        echo "      ⚠️  Ollama tidak tersedia di repo Termux"
        echo "      💡 Install manual dari: https://ollama.com/download"
    else
        echo "      ✅ Ollama terinstall"
    fi
fi

# STEP 2 — JALANKAN OLLAMA
echo ""
echo "[2/4] Jalankan Ollama..."

if pgrep ollama > /dev/null; then
    echo "      ✅ Ollama sudah berjalan"
else
    nohup ollama serve > /dev/null 2>&1 &
    sleep 5
    echo "      ✅ Ollama dijalankan"
fi

sleep 2

# STEP 3 — DOWNLOAD MODEL PHI
echo ""
echo "[3/4] Download model phi (50 MB)..."
echo "      📥 Mengunduh... mohon tunggu."

if command -v ollama > /dev/null 2>&1; then
    if ollama list 2>/dev/null | grep -q "phi"; then
        echo "      ✅ Model phi sudah ada"
    else
        ollama pull phi 2>&1 | tail -3
        
        if ollama list 2>/dev/null | grep -q "phi"; then
            echo "      ✅ Model phi terinstall"
        else
            echo "      ❌ Gagal. Coba manual: ollama pull phi"
        fi
    fi
else
    echo "      ❌ Ollama tidak terinstall"
fi

# STEP 4 — SETUP ALIAS
echo ""
echo "[4/4] Setup alias..."

sed -i '/^alias ai=/d' ~/.bashrc
sed -i '/^alias ai-chat=/d' ~/.bashrc
sed -i '/^alias ai-setup=/d' ~/.bashrc

cat >> ~/.bashrc << 'EOF'

# ===== ZUHRI AI =====
alias ai='python ~/zuhri_os/ai/zuhri_ai.py'
alias ai-chat='python ~/zuhri_os/ai/zuhri_ai.py'
alias ai-setup='bash ~/zuhri_os/ai/setup_ai.sh'

EOF

source ~/.bashrc

clear
echo ""
echo "  ╔══════════════════════════════════════════════════════════════════╗"
echo "  ║        ✅ ZUHRI AI — SIAP!                                     ║"
echo "  ╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "  📋 Cara pakai:"
echo "    ai                  → Chat interaktif"
echo "    ai \"pertanyaan\"      → Tanya langsung"
echo ""
