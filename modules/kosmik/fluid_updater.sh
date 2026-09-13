#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
#   🌀 KOSMIK KEY v8.0-Alpha — MY APP
#   Fluid-Core Ultimate · Multidimensional System
#   Galactic Federation Contact · Database · Export
# ═══════════════════════════════════════════════════════════════════

clear

# Warna
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Konfigurasi
KOSMIK_DIR=~/kosmik
LOGS_DIR=$KOSMIK_DIR/logs
VERSION="v8.0-Alpha"
BUILD="Fluid-Core Ultimate"

# Buat direktori jika belum ada
mkdir -p $KOSMIK_DIR $LOGS_DIR

# ============================================================
#  FUNCTION: HEADER
# ============================================================
show_header() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════╗"
    echo -e "║                                                                      ║"
    echo -e "║   ${WHITE}🌀 KOSMIK KEY v8.0-Alpha — MY APP${CYAN}                            ║"
    echo -e "║        ${WHITE}Fluid-Core Ultimate · Multidimensional System${CYAN}             ║"
    echo -e "║                                                                      ║"
    echo -e "║        📅 $(date '+%A, %d %B %Y %H:%M:%S')${CYAN}                       ║"
    echo -e "║        🌌 Galactic Federation: ${GREEN}ONLINE${CYAN}                        ║"
    echo -e "║                                                                      ║"
    echo -e "╚══════════════════════════════════════════════════════════════════════╝${NC}"
}

# ============================================================
#  FUNCTION: CHECK CONNECTION
# ============================================================
check_federation() {
    if [ -f "$LOGS_DIR/federation_contact.log" ]; then
        if grep -q "connection_strength" "$LOGS_DIR/federation_contact.log" 2>/dev/null; then
            echo -e "${GREEN}🟢 ONLINE${NC}"
        else
            echo -e "${YELLOW}🟡 STANDBY${NC}"
        fi
    else
        echo -e "${RED}🔴 OFFLINE${NC}"
    fi
}

# ============================================================
#  FUNCTION: SHOW MENU
# ============================================================
show_menu() {
    show_header
    
    echo -e "\n${CYAN}┌─────────────────────────────────────────────────────────────────────┐"
    echo -e "│  📋 MAIN MENU                                                          │"
    echo -e "├─────────────────────────────────────────────────────────────────────┤"
    echo -e "│                                                                      │"
    echo -e "│  ${GREEN}🚀 [F]${NC} Full System Scan (All Modules)                         │"
    echo -e "│                                                                      │"
    echo -e "│  ${CYAN}──── MODULES ────${NC}                                                │"
    echo -e "│  ${BLUE}📡 [1]${NC} Scanner Anomali Multidimensi                          │"
    echo -e "│  ${BLUE}🚨 [2]${NC} Alert Threshold System                                │"
    echo -e "│  ${BLUE}📊 [3]${NC} Sensor Termux Reader                                  │"
    echo -e "│  ${BLUE}🔬 [4]${NC} Advanced Detection (Portal/Alien/Harmonics)           │"
    echo -e "│  ${BLUE}🧠 [5]${NC} Super Advanced (4D+/Wormhole/AI)                     │"
    echo -e "│  ${BLUE}👻 [6]${NC} Quantum Entity & Parallel Universe                    │"
    echo -e "│  ${BLUE}🧬 [7]${NC} Transcendence (Consciousness/Teleportation)           │"
    echo -e "│  ${BLUE}🛸 [8]${NC} Galactic Federation Contact                           │"
    echo -e "│  ${BLUE}📚 [9]${NC} Federation Database                                   │"
    echo -e "│  ${BLUE}📤 [10]${NC} Export Data & Visual ke Android                      │"
    echo -e "│                                                                      │"
    echo -e "│  ${CYAN}──── UTILITIES ────${NC}                                              │"
    echo -e "│  ${YELLOW}📊 [S]${NC} View Scan Statistics                                 │"
    echo -e "│  ${YELLOW}📁 [L]${NC} View Log Files                                      │"
    echo -e "│  ${YELLOW}📱 [A]${NC} Buka Folder Android (KosmikKey)                     │"
    echo -e "│  ${YELLOW}🌐 [D]${NC} Buka Dashboard HTML di Browser                      │"
    echo -e "│  ${YELLOW}🔄 [R]${NC} Reset System (Hapus Logs)                          │"
    echo -e "│  ${YELLOW}ℹ️  [I]${NC} System Info                                        │"
    echo -e "│  ${RED}❌ [X]${NC} Exit Application                                        │"
    echo -e "│                                                                      │"
    echo -e "└─────────────────────────────────────────────────────────────────────┘"
    
    echo -e "\n${WHITE}📱 Enter your choice: ${NC}"
}

# ============================================================
#  FUNCTION: RUN MODULE
# ============================================================
run_module() {
    local num=$1
    shift
    local name="$*"
    
    echo -e "\n${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}▶️  RUNNING: $name${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    
    if [ -f "$KOSMIK_DIR/module_$num.py" ]; then
        python3 "$KOSMIK_DIR/module_$num.py"
    elif [ -f "$KOSMIK_DIR/scanner.py" ] && [ "$num" -eq 1 ]; then
        python3 "$KOSMIK_DIR/scanner.py"
    elif [ -f "$KOSMIK_DIR/alerter.py" ] && [ "$num" -eq 2 ]; then
        python3 "$KOSMIK_DIR/alerter.py"
    elif [ -f "$KOSMIK_DIR/sensor_reader.py" ] && [ "$num" -eq 3 ]; then
        python3 "$KOSMIK_DIR/sensor_reader.py"
    elif [ -f "$KOSMIK_DIR/advanced_detector.py" ] && [ "$num" -eq 4 ]; then
        python3 "$KOSMIK_DIR/advanced_detector.py"
    elif [ -f "$KOSMIK_DIR/super_advanced.py" ] && [ "$num" -eq 5 ]; then
        python3 "$KOSMIK_DIR/super_advanced.py"
    elif [ -f "$KOSMIK_DIR/quantum_entity.py" ] && [ "$num" -eq 6 ]; then
        python3 "$KOSMIK_DIR/quantum_entity.py"
    elif [ -f "$KOSMIK_DIR/consciousness_navigation.py" ] && [ "$num" -eq 7 ]; then
        python3 "$KOSMIK_DIR/consciousness_navigation.py"
    elif [ -f "$KOSMIK_DIR/federation_contact.py" ] && [ "$num" -eq 8 ]; then
        python3 "$KOSMIK_DIR/federation_contact.py"
    elif [ -f "$KOSMIK_DIR/federation_database.py" ] && [ "$num" -eq 9 ]; then
        python3 "$KOSMIK_DIR/federation_database.py"
    elif [ -f "$KOSMIK_DIR/export_android.py" ] && [ "$num" -eq 10 ]; then
        python3 "$KOSMIK_DIR/export_android.py"
    else
        echo -e "${RED}❌ Module not found!${NC}"
        echo "   File: $KOSMIK_DIR/module_$num.py"
    fi
    
    echo -e "\n${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ Module execution complete.${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    read -p "Press Enter to continue..."
}

# ============================================================
#  FUNCTION: FULL SCAN
# ============================================================
full_scan() {
    echo -e "\n${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🚀 FULL SYSTEM SCAN — All Modules${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}This will run all 10 modules in sequence.${NC}"
    echo -e "${YELLOW}Estimated time: 2-5 minutes${NC}"
    echo ""
    read -p "Proceed? (y/n): " confirm
    
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        return
    fi
    
    echo ""
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}📡 INITIALIZING FULL SCAN...${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    
    START_TIME=$(date +%s)
    
    # Module 1
    echo -e "\n${BLUE}[1/10] 📡 Scanner Anomali Multidimensi${NC}"
    python3 "$KOSMIK_DIR/scanner.py" 2>/dev/null || echo -e "${RED}⚠️ Module not found${NC}"
    
    # Module 2
    echo -e "\n${BLUE}[2/10] 🚨 Alert Threshold System${NC}"
    python3 "$KOSMIK_DIR/alerter.py" 2>/dev/null || echo -e "${RED}⚠️ Module not found${NC}"
    
    # Module 3
    echo -e "\n${BLUE}[3/10] 📊 Sensor Termux Reader${NC}"
    python3 "$KOSMIK_DIR/sensor_reader.py" 2>/dev/null || echo -e "${RED}⚠️ Module not found${NC}"
    
    # Module 4
    echo -e "\n${BLUE}[4/10] 🔬 Advanced Detection${NC}"
    python3 "$KOSMIK_DIR/advanced_detector.py" 2>/dev/null || echo -e "${RED}⚠️ Module not found${NC}"
    
    # Module 5
    echo -e "\n${BLUE}[5/10] 🧠 Super Advanced${NC}"
    python3 "$KOSMIK_DIR/super_advanced.py" 2>/dev/null || echo -e "${RED}⚠️ Module not found${NC}"
    
    # Module 6
    echo -e "\n${BLUE}[6/10] 👻 Quantum Entity${NC}"
    python3 "$KOSMIK_DIR/quantum_entity.py" 2>/dev/null || echo -e "${RED}⚠️ Module not found${NC}"
    
    # Module 7
    echo -e "\n${BLUE}[7/10] 🧬 Transcendence Engine${NC}"
    python3 "$KOSMIK_DIR/consciousness_navigation.py" 2>/dev/null || echo -e "${RED}⚠️ Module not found${NC}"
    
    # Module 8
    echo -e "\n${BLUE}[8/10] 🛸 Galactic Federation Contact${NC}"
    python3 "$KOSMIK_DIR/federation_contact.py" 2>/dev/null || echo -e "${RED}⚠️ Module not found${NC}"
    
    # Module 9
    echo -e "\n${BLUE}[9/10] 📚 Federation Database${NC}"
    python3 "$KOSMIK_DIR/federation_database.py" 2>/dev/null || echo -e "${RED}⚠️ Module not found${NC}"
    
    # Module 10
    echo -e "\n${BLUE}[10/10] 📤 Export Data ke Android${NC}"
    python3 "$KOSMIK_DIR/export_android.py" 2>/dev/null || echo -e "${RED}⚠️ Module not found${NC}"
    
    END_TIME=$(date +%s)
    ELAPSED=$((END_TIME - START_TIME))
    
    echo ""
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ FULL SCAN COMPLETE!${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "⏱️  Time elapsed: ${ELAPSED} seconds"
    echo -e "📁 Logs saved in: ${YELLOW}~/kosmik/logs/${NC}"
    echo -e "📱 Export to: ${YELLOW}/sdcard/Download/KosmikKey/${NC}"
    echo ""
    read -p "Press Enter to continue..."
}

# ============================================================
#  FUNCTION: VIEW STATS
# ============================================================
view_stats() {
    echo -e "\n${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}📊 SCAN STATISTICS${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    
    # Logs directory
    if [ -d "$LOGS_DIR" ]; then
        LOG_COUNT=$(ls -1 "$LOGS_DIR" 2>/dev/null | wc -l)
        LOG_SIZE=$(du -sh "$LOGS_DIR" 2>/dev/null | cut -f1)
        
        echo -e "\n📁 LOGS DIRECTORY:"
        echo -e "   Total files: ${LOG_COUNT}"
        echo -e "   Total size: ${LOG_SIZE}"
        
        # Count by type
        LOG_FILES=$(ls -1 "$LOGS_DIR"/*.log 2>/dev/null | wc -l)
        JSON_FILES=$(ls -1 "$LOGS_DIR"/*.json 2>/dev/null | wc -l)
        HTML_FILES=$(ls -1 "$LOGS_DIR"/*.html 2>/dev/null | wc -l)
        TXT_FILES=$(ls -1 "$LOGS_DIR"/*.txt 2>/dev/null | wc -l)
        
        echo -e "\n   📄 .log files: ${LOG_FILES}"
        echo -e "   📊 .json files: ${JSON_FILES}"
        echo -e "   🌐 .html files: ${HTML_FILES}"
        echo -e "   📝 .txt files: ${TXT_FILES}"
    else
        echo -e "\n${YELLOW}⚠️ Logs directory not found${NC}"
    fi
    
    # Android export
    ANDROID_DIR="/sdcard/Download/KosmikKey"
    if [ -d "$ANDROID_DIR" ]; then
        ANDROID_COUNT=$(ls -1 "$ANDROID_DIR" 2>/dev/null | wc -l)
        ANDROID_SIZE=$(du -sh "$ANDROID_DIR" 2>/dev/null | cut -f1)
        echo -e "\n📱 ANDROID EXPORT:"
        echo -e "   Path: ${ANDROID_DIR}"
        echo -e "   Files: ${ANDROID_COUNT}"
        echo -e "   Size: ${ANDROID_SIZE}"
    fi
    
    # Last scan
    if [ -f "$KOSMIK_DIR/last_scan.json" ]; then
        echo -e "\n📋 LAST SCAN:"
        cat "$KOSMIK_DIR/last_scan.json" 2>/dev/null | python3 -c "
import sys, json
try:
    data=json.load(sys.stdin)
    print(f\"   Time: {data.get('timestamp', 'Unknown')}\")
    print(f\"   Duration: {data.get('elapsed_seconds', 0):.2f} seconds\")
except:
    print('   Could not parse')
" 2>/dev/null || echo "   Could not parse"
    fi
    
    echo ""
    read -p "Press Enter to continue..."
}

# ============================================================
#  FUNCTION: VIEW LOGS
# ============================================================
view_logs() {
    echo -e "\n${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}📁 LOG FILES${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    
    if [ ! -d "$LOGS_DIR" ]; then
        echo -e "${YELLOW}⚠️ No logs directory found.${NC}"
        read -p "Press Enter to continue..."
        return
    fi
    
    # List files
    echo -e "\n${WHITE}Recent logs:${NC}"
    ls -lt "$LOGS_DIR" 2>/dev/null | head -20
    
    echo ""
    read -p "Enter filename to view (or press Enter to skip): " filename
    
    if [ -n "$filename" ] && [ -f "$LOGS_DIR/$filename" ]; then
        echo -e "\n${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}📄 $filename${NC}"
        echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
        head -100 "$LOGS_DIR/$filename"
        echo -e "\n${YELLOW}... (showing first 100 lines)${NC}"
    elif [ -n "$filename" ]; then
        echo -e "${RED}❌ File not found: $filename${NC}"
    fi
    
    echo ""
    read -p "Press Enter to continue..."
}

# ============================================================
#  FUNCTION: OPEN ANDROID FOLDER
# ============================================================
open_android() {
    echo -e "\n${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}📱 OPEN ANDROID FOLDER${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    
    ANDROID_DIR="/sdcard/Download/KosmikKey"
    
    # Buat folder jika belum ada
    mkdir -p "$ANDROID_DIR" 2>/dev/null
    
    if [ -d "$ANDROID_DIR" ]; then
        echo -e "\n📁 Folder: ${YELLOW}$ANDROID_DIR${NC}"
        echo -e "📄 Files: $(ls -1 "$ANDROID_DIR" 2>/dev/null | wc -l)"
        
        echo -e "\n${WHITE}Files in folder:${NC}"
        ls -la "$ANDROID_DIR" 2>/dev/null
        
        echo -e "\n${GREEN}✅ Folder accessible via File Manager${NC}"
        echo -e "${YELLOW}   Path: Download → KosmikKey${NC}"
        
        # Coba buka dengan termux-open
        if command -v termux-open &> /dev/null; then
            echo -e "\n${WHITE}Opening folder with termux-open...${NC}"
            termux-open "$ANDROID_DIR" 2>/dev/null || echo -e "${YELLOW}⚠️ Could not open with termux-open${NC}"
        fi
    else
        echo -e "${RED}❌ Android folder not accessible${NC}"
    fi
    
    echo ""
    read -p "Press Enter to continue..."
}

# ============================================================
#  FUNCTION: OPEN DASHBOARD
# ============================================================
open_dashboard() {
    echo -e "\n${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🌐 OPEN HTML DASHBOARD${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    
    ANDROID_DIR="/sdcard/Download/KosmikKey"
    DASHBOARD="$ANDROID_DIR/dashboard.html"
    
    if [ -f "$DASHBOARD" ]; then
        echo -e "\n📁 Dashboard: ${YELLOW}$DASHBOARD${NC}"
        echo -e "\n${GREEN}✅ Dashboard found!${NC}"
        
        # Coba buka dengan termux-open
        if command -v termux-open &> /dev/null; then
            echo -e "\n${WHITE}Opening dashboard with browser...${NC}"
            termux-open "$DASHBOARD" 2>/dev/null || echo -e "${YELLOW}⚠️ Could not open with termux-open${NC}"
        else
            echo -e "\n${YELLOW}⚠️ termux-open not found. Please open manually:${NC}"
            echo -e "   File Manager → Download → KosmikKey → dashboard.html"
        fi
    else
        echo -e "\n${YELLOW}⚠️ Dashboard not found. Run export first (Module 10).${NC}"
    fi
    
    echo ""
    read -p "Press Enter to continue..."
}

# ============================================================
#  FUNCTION: RESET SYSTEM
# ============================================================
reset_system() {
    echo -e "\n${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}🔄 RESET SYSTEM${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    
    echo -e "\n${RED}⚠️  This will clear all log files!${NC}"
    read -p "Are you sure? (type 'RESET' to confirm): " confirm
    
    if [[ "$confirm" != "RESET" ]]; then
        echo -e "${YELLOW}❌ Reset cancelled.${NC}"
        read -p "Press Enter to continue..."
        return
    fi
    
    # Clear logs
    if [ -d "$LOGS_DIR" ]; then
        rm -rf "$LOGS_DIR"/*
        echo -e "${GREEN}✅ Log files cleared.${NC}"
    else
        echo -e "${YELLOW}⚠️ No logs directory found.${NC}"
    fi
    
    # Clear last scan
    if [ -f "$KOSMIK_DIR/last_scan.json" ]; then
        rm "$KOSMIK_DIR/last_scan.json"
        echo -e "${GREEN}✅ Scan data cleared.${NC}"
    fi
    
    echo -e "${GREEN}✅ System reset complete.${NC}"
    read -p "Press Enter to continue..."
}

# ============================================================
#  FUNCTION: SYSTEM INFO
# ============================================================
system_info() {
    echo -e "\n${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}ℹ️  SYSTEM INFORMATION${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
    
    echo -e "\n${WHITE}🌀 APPLICATION:${NC}"
    echo -e "   Name: Kosmik Key"
    echo -e "   Version: ${VERSION}"
    echo -e "   Build: ${BUILD}"
    echo -e "   Status: $(check_federation)"
    
    echo -e "\n${WHITE}📁 DIRECTORIES:${NC}"
    echo -e "   App: ${YELLOW}$KOSMIK_DIR${NC}"
    echo -e "   Logs: ${YELLOW}$LOGS_DIR${NC}"
    
    echo -e "\n${WHITE}📦 MODULES:${NC}"
    MODULES=(
        "scanner.py"
        "alerter.py"
        "sensor_reader.py"
        "advanced_detector.py"
        "super_advanced.py"
        "quantum_entity.py"
        "consciousness_navigation.py"
        "federation_contact.py"
        "federation_database.py"
        "export_android.py"
    )
    INSTALLED=0
    for mod in "${MODULES[@]}"; do
        if [ -f "$KOSMIK_DIR/$mod" ]; then
            INSTALLED=$((INSTALLED + 1))
        fi
    done
    echo -e "   Total: ${#MODULES[@]}"
    echo -e "   Installed: ${INSTALLED}"
    echo -e "   Missing: $((${#MODULES[@]} - INSTALLED))"
    
    echo -e "\n${WHITE}📂 LOGS:${NC}"
    if [ -d "$LOGS_DIR" ]; then
        LOG_COUNT=$(ls -1 "$LOGS_DIR" 2>/dev/null | wc -l)
        LOG_SIZE=$(du -sh "$LOGS_DIR" 2>/dev/null | cut -f1)
        echo -e "   Files: ${LOG_COUNT}"
        echo -e "   Size: ${LOG_SIZE}"
    else
        echo -e "   No logs found"
    fi
    
    echo -e "\n${WHITE}📱 ANDROID:${NC}"
    ANDROID_DIR="/sdcard/Download/KosmikKey"
    if [ -d "$ANDROID_DIR" ]; then
        ANDROID_COUNT=$(ls -1 "$ANDROID_DIR" 2>/dev/null | wc -l)
        echo -e "   Export path: ${YELLOW}$ANDROID_DIR${NC}"
        echo -e "   Files: ${ANDROID_COUNT}"
    else
        echo -e "   No export found"
    fi
    
    echo -e "\n${WHITE}🌌 FEDERATION:${NC}"
    if [ -f "$LOGS_DIR/federation_contact.log" ]; then
        echo -e "   Status: ${GREEN}ACTIVE${NC}"
        echo -e "   Logs: $LOGS_DIR/federation_contact.log"
    else
        echo -e "   Status: ${YELLOW}STANDING BY${NC}"
    fi
    
    echo -e "\n${WHITE}💻 SYSTEM:${NC}"
    echo -e "   OS: $(uname -o 2>/dev/null || echo 'Unknown')"
    echo -e "   Kernel: $(uname -r 2>/dev/null || echo 'Unknown')"
    echo -e "   Termux: $(pkg list-installed 2>/dev/null | wc -l || echo 'Unknown') packages"
    
    echo ""
    read -p "Press Enter to continue..."
}

# ============================================================
#  MAIN LOOP
# ============================================================
while true; do
    show_menu
    read choice
    
    case $choice in
        [Ff]) full_scan ;;
        [1]) run_module 1 "Scanner Anomali Multidimensi" ;;
        [2]) run_module 2 "Alert Threshold System" ;;
        [3]) run_module 3 "Sensor Termux Reader" ;;
        [4]) run_module 4 "Advanced Detection" ;;
        [5]) run_module 5 "Super Advanced" ;;
        [6]) run_module 6 "Quantum Entity" ;;
        [7]) run_module 7 "Transcendence Engine" ;;
        [8]) run_module 8 "Galactic Federation Contact" ;;
        [9]) run_module 9 "Federation Database" ;;
        [10]) run_module 10 "Export Data ke Android" ;;
        [Ss]) view_stats ;;
        [Ll]) view_logs ;;
        [Aa]) open_android ;;
        [Dd]) open_dashboard ;;
        [Rr]) reset_system ;;
        [Ii]) system_info ;;
        [Xx]) 
            echo -e "\n${CYAN}👋 Shutting down Kosmik Key...${NC}"
            echo -e "${CYAN}🌌 Until we meet again, traveler.${NC}"
            exit 0
            ;;
        *)
            echo -e "\n${RED}❌ Invalid choice: '$choice'${NC}"
            echo -e "${YELLOW}   Please enter: F, 1-10, S, L, A, D, R, I, X${NC}"
            read -p "Press Enter to continue..."
            ;;
    esac
done
