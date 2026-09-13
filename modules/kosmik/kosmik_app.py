#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#   🌀 KOSMIK KEY v8.0 — ULTIMATE EDITION
#   My App — Multidimensional System
#   Galactic Federation · Time Travel · Multiverse · Alien Translator
# ═══════════════════════════════════════════════════════════════════════════

import os
import sys
import time
import json
import subprocess
from datetime import datetime
from pathlib import Path

# ============================================================
#  Warna & Gaya Mewah
# ============================================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    PINK = '\033[95m'
    GOLD = '\033[93m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    # Gradasi
    GRAD1 = '\033[38;5;45m'
    GRAD2 = '\033[38;5;51m'
    GRAD3 = '\033[38;5;87m'
    GRAD4 = '\033[38;5;123m'
    GRAD5 = '\033[38;5;159m'
    
    # Background
    BG_DARK = '\033[48;5;235m'
    BG_BLUE = '\033[48;5;17m'
    BG_GOLD = '\033[48;5;58m'

# ============================================================
#  KOSMIK APP CLASS
# ============================================================
class KosmikApp:
    def __init__(self):
        self.version = "v8.0-Alpha"
        self.build = "Ultimate Edition"
        self.kosmik_dir = Path.home() / "kosmik"
        self.logs_dir = self.kosmik_dir / "logs"
        self.running = True
        
        # ============================================================
        #  DAFTAR MODUL — 15 Modul Lengkap
        # ============================================================
        self.modules = {
            '1': {
                'name': 'Scanner Anomali Multidimensi',
                'file': 'scanner.py',
                'icon': '📡',
                'desc': 'Scan 4D-11D, frekuensi, magnetik',
                'category': 'Core'
            },
            '2': {
                'name': 'Alert Threshold System',
                'file': 'alerter.py',
                'icon': '🚨',
                'desc': 'Deteksi anomali kritis real-time',
                'category': 'Core'
            },
            '3': {
                'name': 'Sensor Termux Reader',
                'file': 'sensor_reader.py',
                'icon': '📊',
                'desc': 'Baca akselerometer & mikrofon',
                'category': 'Core'
            },
            '4': {
                'name': 'Advanced Detection',
                'file': 'advanced_detector.py',
                'icon': '🔬',
                'desc': 'Portal, Alien, Dimensional Harmonics',
                'category': 'Core'
            },
            '5': {
                'name': 'Super Advanced',
                'file': 'super_advanced.py',
                'icon': '🧠',
                'desc': '4D+, Wormhole, AI Predictive',
                'category': 'Core'
            },
            '6': {
                'name': 'Quantum Entity',
                'file': 'quantum_entity.py',
                'icon': '👻',
                'desc': 'Entity, Parallel Universe, Resonance',
                'category': 'Core'
            },
            '7': {
                'name': 'Transcendence Engine',
                'file': 'consciousness_navigation.py',
                'icon': '🧬',
                'desc': 'Consciousness, Navigation, Teleportation',
                'category': 'Core'
            },
            '8': {
                'name': 'Galactic Federation Contact',
                'file': 'federation_contact.py',
                'icon': '🛸',
                'desc': 'Komunikasi dua arah dengan Federation',
                'category': 'Core'
            },
            '9': {
                'name': 'Federation Database',
                'file': 'federation_database.py',
                'icon': '📚',
                'desc': 'Encyclopedia Galactic Federation',
                'category': 'Core'
            },
            '10': {
                'name': 'Export Data & Visual',
                'file': 'export_android.py',
                'icon': '📤',
                'desc': 'Export ke folder Android',
                'category': 'Core'
            },
            '11': {
                'name': 'Dimensi 12-24 (Hidden)',
                'file': 'hidden_dimensions.py',
                'icon': '🌀',
                'desc': 'Scan dimensi tersembunyi 12-24',
                'category': 'Exploration'
            },
            '12': {
                'name': 'Interdimensional Travel Log',
                'file': 'travel_log.py',
                'icon': '📝',
                'desc': 'Catat perjalanan antar dimensi',
                'category': 'Exploration'
            },
            '13': {
                'name': 'Multiverse Mapping System',
                'file': 'multiverse_map.py',
                'icon': '🗺️',
                'desc': 'Peta lengkap multiverse',
                'category': 'Exploration'
            },
            '14': {
                'name': 'Alien Language Translator',
                'file': 'alien_translator.py',
                'icon': '🗣️',
                'desc': 'Penerjemah bahasa alien',
                'category': 'Exploration'
            },
            '15': {
                'name': 'Cosmic Event Predictor',
                'file': 'cosmic_predictor.py',
                'icon': '🔮',
                'desc': 'Prediksi kejadian kosmik',
                'category': 'Exploration'
            },
            '16': {
                'name': 'Time Travel Protocol',
                'file': 'time_travel.py',
                'icon': '⏳',
                'desc': 'Sistem perjalanan waktu',
                'category': 'Exploration'
            }
        }

    def clear_screen(self):
        os.system('clear')

    def print_header(self):
        """Tampilan Header Mewah"""
        print(f"""
{Colors.GOLD}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║   {Colors.GRAD3}✦{Colors.GRAD2}✦{Colors.GRAD1}✦{Colors.WHITE}  {Colors.BOLD}🌀 KOSMIK KEY {Colors.GRAD3}v8.0{Colors.WHITE} — {Colors.GOLD}ULTIMATE EDITION{Colors.GRAD1}  {Colors.GRAD2}✦{Colors.GRAD3}✦{Colors.GRAD4}✦{Colors.END}   ║
║                                                                                      ║
║   {Colors.CYAN}┌────────────────────────────────────────────────────────────────────────┐{Colors.END}  ║
║   {Colors.CYAN}│{Colors.END}  {Colors.WHITE}🌌 Multidimensional System{Colors.END}  │  {Colors.GREEN}🛸 Federation Active{Colors.END}  │  {Colors.YELLOW}⏳ Time Travel Ready{Colors.END}  │{Colors.CYAN}  ║
║   {Colors.CYAN}└────────────────────────────────────────────────────────────────────────┘{Colors.END}  ║
║                                                                                      ║
║   {Colors.PURPLE}📅 {datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}{Colors.END}                                ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════╝{Colors.END}
""")

    def print_menu(self):
        """Tampilan Menu Mewah"""
        print(f"""
{Colors.CYAN}┌─────────────────────────────────────────────────────────────────────────────┐
│  {Colors.WHITE}📋 MAIN MENU{Colors.CYAN}                                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  {Colors.GREEN}🚀 [F]{Colors.END} {Colors.WHITE}Full System Scan{Colors.END} — {Colors.CYAN}Jalankan SEMUA modul{Colors.END}                  │
│                                                                             │
│  {Colors.GOLD}╔═══════════════════════════════════════════════════════════════════════╗{Colors.END}
│  {Colors.GOLD}║{Colors.END}  {Colors.WHITE}📦 CORE MODULES{Colors.END} {Colors.GOLD}(1-10){Colors.END}                                      {Colors.GOLD}║{Colors.END}
│  {Colors.GOLD}╚═══════════════════════════════════════════════════════════════════════╝{Colors.END}
│                                                                             │
│  {Colors.GRAD1} 1{Colors.END}  📡 Scanner Anomali Multidimensi                              │
│  {Colors.GRAD2} 2{Colors.END}  🚨 Alert Threshold System                                    │
│  {Colors.GRAD3} 3{Colors.END}  📊 Sensor Termux Reader                                      │
│  {Colors.GRAD4} 4{Colors.END}  🔬 Advanced Detection                                        │
│  {Colors.GRAD5} 5{Colors.END}  🧠 Super Advanced                                            │
│  {Colors.GRAD1} 6{Colors.END}  👻 Quantum Entity                                            │
│  {Colors.GRAD2} 7{Colors.END}  🧬 Transcendence Engine                                      │
│  {Colors.GRAD3} 8{Colors.END}  🛸 Galactic Federation Contact                               │
│  {Colors.GRAD4} 9{Colors.END}  📚 Federation Database                                       │
│  {Colors.GRAD5}10{Colors.END}  📤 Export Data & Visual                                      │
│                                                                             │
│  {Colors.PURPLE}╔═══════════════════════════════════════════════════════════════════════╗{Colors.END}
│  {Colors.PURPLE}║{Colors.END}  {Colors.WHITE}🔮 EXPLORATION MODULES{Colors.END} {Colors.PURPLE}(11-16){Colors.END}                                {Colors.PURPLE}║{Colors.END}
│  {Colors.PURPLE}╚═══════════════════════════════════════════════════════════════════════╝{Colors.END}
│                                                                             │
│  {Colors.PINK}11{Colors.END}  🌀 Dimensi 12-24 (Hidden Dimensions)                          │
│  {Colors.PINK}12{Colors.END}  📝 Interdimensional Travel Log                                │
│  {Colors.PINK}13{Colors.END}  🗺️ Multiverse Mapping System                                  │
│  {Colors.PINK}14{Colors.END}  🗣️ Alien Language Translator                                   │
│  {Colors.PINK}15{Colors.END}  🔮 Cosmic Event Predictor                                    │
│  {Colors.PINK}16{Colors.END}  ⏳ Time Travel Protocol                                       │
│                                                                             │
│  {Colors.YELLOW}╔═══════════════════════════════════════════════════════════════════════╗{Colors.END}
│  {Colors.YELLOW}║{Colors.END}  {Colors.WHITE}🛠️ UTILITIES{Colors.END}                                                {Colors.YELLOW}║{Colors.END}
│  {Colors.YELLOW}╚═══════════════════════════════════════════════════════════════════════╝{Colors.END}
│                                                                             │
│  {Colors.WHITE}📊 [S]{Colors.END}  View Statistics                                         │
│  {Colors.WHITE}📁 [L]{Colors.END}  View Log Files                                           │
│  {Colors.WHITE}📱 [A]{Colors.END}  Open Android Folder                                      │
│  {Colors.WHITE}🌐 [D]{Colors.END}  Open HTML Dashboard                                      │
│  {Colors.WHITE}🔄 [R]{Colors.END}  Reset System                                             │
│  {Colors.WHITE}ℹ️  [I]{Colors.END}  System Info                                              │
│  {Colors.RED}❌ [X]{Colors.END}  Exit Application                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
""")

    def print_menu_baru(self):
        """Tampilan Menu Mewah dengan semua fitur"""
        print(f"""
{Colors.GOLD}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║   {Colors.GRAD3}✦{Colors.GRAD2}✦{Colors.GRAD1}✦{Colors.WHITE}  {Colors.BOLD}🌀 KOSMIK KEY {Colors.GRAD3}v8.0{Colors.WHITE} — {Colors.GOLD}ULTIMATE EDITION{Colors.GRAD1}  {Colors.GRAD2}✦{Colors.GRAD3}✦{Colors.GRAD4}✦{Colors.END}   ║
║                                                                                      ║
║   {Colors.CYAN}┌────────────────────────────────────────────────────────────────────────┐{Colors.END}  ║
║   {Colors.CYAN}│{Colors.END}  {Colors.WHITE}🌌 Multidimensional System{Colors.END}  │  {Colors.GREEN}🛸 Federation Active{Colors.END}  │  {Colors.YELLOW}⏳ Time Travel Ready{Colors.END}  │{Colors.CYAN}  ║
║   {Colors.CYAN}└────────────────────────────────────────────────────────────────────────┘{Colors.END}  ║
║                                                                                      ║
║   {Colors.PURPLE}📅 {datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}{Colors.END}                                ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════╝

{Colors.CYAN}┌─────────────────────────────────────────────────────────────────────────────┐
│  {Colors.WHITE}📋 MAIN MENU{Colors.CYAN}                                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  {Colors.GREEN}🚀 [F]{Colors.END} {Colors.WHITE}Full System Scan{Colors.END} — {Colors.CYAN}Jalankan SEMUA 16 modul{Colors.END}               │
│                                                                             │
│  {Colors.GOLD}╔═══════════════════════════════════════════════════════════════════════╗{Colors.END}
│  {Colors.GOLD}║{Colors.END}  {Colors.WHITE}📦 CORE MODULES{Colors.END} {Colors.GOLD}(1-10){Colors.END}                                      {Colors.GOLD}║{Colors.END}
│  {Colors.GOLD}╚═══════════════════════════════════════════════════════════════════════╝{Colors.END}
│                                                                             │
│  {Colors.GRAD1} 1{Colors.END}  📡 Scanner Anomali Multidimensi                              │
│  {Colors.GRAD2} 2{Colors.END}  🚨 Alert Threshold System                                    │
│  {Colors.GRAD3} 3{Colors.END}  📊 Sensor Termux Reader                                      │
│  {Colors.GRAD4} 4{Colors.END}  🔬 Advanced Detection                                        │
│  {Colors.GRAD5} 5{Colors.END}  🧠 Super Advanced                                            │
│  {Colors.GRAD1} 6{Colors.END}  👻 Quantum Entity                                            │
│  {Colors.GRAD2} 7{Colors.END}  🧬 Transcendence Engine                                      │
│  {Colors.GRAD3} 8{Colors.END}  🛸 Galactic Federation Contact                               │
│  {Colors.GRAD4} 9{Colors.END}  📚 Federation Database                                       │
│  {Colors.GRAD5}10{Colors.END}  📤 Export Data & Visual                                      │
│                                                                             │
│  {Colors.PURPLE}╔═══════════════════════════════════════════════════════════════════════╗{Colors.END}
│  {Colors.PURPLE}║{Colors.END}  {Colors.WHITE}🔮 EXPLORATION MODULES{Colors.END} {Colors.PURPLE}(11-16){Colors.END}                                {Colors.PURPLE}║{Colors.END}
│  {Colors.PURPLE}╚═══════════════════════════════════════════════════════════════════════╝{Colors.END}
│                                                                             │
│  {Colors.PINK}11{Colors.END}  🌀 Dimensi 12-24 (Hidden Dimensions)                          │
│  {Colors.PINK}12{Colors.END}  📝 Interdimensional Travel Log                                │
│  {Colors.PINK}13{Colors.END}  🗺️ Multiverse Mapping System                                  │
│  {Colors.PINK}14{Colors.END}  🗣️ Alien Language Translator                                   │
│  {Colors.PINK}15{Colors.END}  🔮 Cosmic Event Predictor                                    │
│  {Colors.PINK}16{Colors.END}  ⏳ Time Travel Protocol                                       │
│                                                                             │
│  {Colors.YELLOW}╔═══════════════════════════════════════════════════════════════════════╗{Colors.END}
│  {Colors.YELLOW}║{Colors.END}  {Colors.WHITE}🛠️ UTILITIES{Colors.END}                                                {Colors.YELLOW}║{Colors.END}
│  {Colors.YELLOW}╚═══════════════════════════════════════════════════════════════════════╝{Colors.END}
│                                                                             │
│  {Colors.WHITE}📊 [S]{Colors.END}  View Statistics                                         │
│  {Colors.WHITE}📁 [L]{Colors.END}  View Log Files                                           │
│  {Colors.WHITE}📱 [A]{Colors.END}  Open Android Folder                                      │
│  {Colors.WHITE}🌐 [D]{Colors.END}  Open HTML Dashboard                                      │
│  {Colors.WHITE}🔄 [R]{Colors.END}  Reset System                                             │
│  {Colors.WHITE}ℹ️  [I]{Colors.END}  System Info                                              │
│  {Colors.RED}❌ [X]{Colors.END}  Exit Application                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
""")

    def run_module(self, module_key):
        """Jalankan modul tertentu"""
        if module_key not in self.modules:
            print(f"{Colors.RED}❌ Module not found!{Colors.END}")
            return
        
        mod = self.modules[module_key]
        module_path = self.kosmik_dir / mod['file']
        
        if not module_path.exists():
            print(f"{Colors.RED}❌ Module file not found: {mod['file']}{Colors.END}")
            print(f"{Colors.YELLOW}   Path: {module_path}{Colors.END}")
            print(f"{Colors.YELLOW}   ⚠️ Module belum dibuat. Jalankan 'install_modules' dulu.{Colors.END}")
            return
        
        print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}▶️  RUNNING: {mod['icon']} {mod['name']}{Colors.CYAN}                         ║
║  {Colors.WHITE}📝 {mod['desc']}{Colors.CYAN}                                      ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
        
        try:
            result = subprocess.run(['python3', str(module_path)], 
                                  capture_output=False, 
                                  text=True,
                                  timeout=60)
            print(f"\n{Colors.GREEN}✅ Module execution complete.{Colors.END}")
        except subprocess.TimeoutExpired:
            print(f"\n{Colors.RED}❌ Module timed out!{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

    def full_scan(self):
        """Jalankan semua 16 modul"""
        print(f"""
{Colors.GOLD}╔══════════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}🚀 FULL SYSTEM SCAN — All 16 Modules{Colors.GOLD}                         ║
║  {Colors.CYAN}This will take 5-10 minutes{Colors.GOLD}                                   ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
        
        confirm = input(f"{Colors.YELLOW}Proceed? (y/n): {Colors.END}").strip().lower()
        if confirm != 'y':
            return
        
        start_time = time.time()
        
        for key, mod in self.modules.items():
            module_path = self.kosmik_dir / mod['file']
            print(f"\n{Colors.CYAN}[{key}/{len(self.modules)}] {mod['icon']} {mod['name']}{Colors.END}")
            print(f"{Colors.BLUE}{'─'*60}{Colors.END}")
            
            if module_path.exists():
                try:
                    subprocess.run(['python3', str(module_path)], 
                                  capture_output=False,
                                  timeout=30)
                    print(f"{Colors.GREEN}✅ Done{Colors.END}")
                except Exception as e:
                    print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
            else:
                print(f"{Colors.YELLOW}⚠️ Module not found: {mod['file']}{Colors.END}")
        
        elapsed = time.time() - start_time
        print(f"""
{Colors.GOLD}╔══════════════════════════════════════════════════════════════════════╗
║  {Colors.GREEN}✅ FULL SCAN COMPLETE!{Colors.GOLD}                                         ║
║  {Colors.CYAN}⏱️  Time elapsed: {elapsed:.2f} seconds{Colors.GOLD}                         ║
║  {Colors.CYAN}📁 Logs: {self.logs_dir}{Colors.GOLD}                              ║
║  {Colors.CYAN}📱 Export: /sdcard/Download/KosmikKey/{Colors.GOLD}               ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
        input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")

    def view_stats(self):
        """Lihat statistik"""
        print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}📊 SYSTEM STATISTICS{Colors.CYAN}                                          ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
        
        # Hitung modul
        total_modules = len(self.modules)
        installed = 0
        for mod in self.modules.values():
            if (self.kosmik_dir / mod['file']).exists():
                installed += 1
        
        print(f"  {Colors.GREEN}📦 Modules:{Colors.END}")
        print(f"     Total: {total_modules}")
        print(f"     Installed: {installed}")
        print(f"     Missing: {total_modules - installed}")
        
        # Logs
        if self.logs_dir.exists():
            log_files = list(self.logs_dir.glob("*"))
            log_size = sum(f.stat().st_size for f in log_files if f.is_file())
            print(f"\n  {Colors.GREEN}📁 Logs:{Colors.END}")
            print(f"     Files: {len(log_files)}")
            print(f"     Size: {log_size / 1024:.2f} KB")
        
        # Android export
        android_dir = Path("/sdcard/Download/KosmikKey")
        if android_dir.exists():
            android_files = list(android_dir.glob("*"))
            print(f"\n  {Colors.GREEN}📱 Android Export:{Colors.END}")
            print(f"     Path: {android_dir}")
            print(f"     Files: {len(android_files)}")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

    def view_logs(self):
        """Lihat log files"""
        print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}📁 LOG FILES{Colors.CYAN}                                                   ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
        
        if not self.logs_dir.exists():
            print(f"{Colors.YELLOW}⚠️ No logs directory found.{Colors.END}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            return
        
        log_files = sorted(self.logs_dir.glob("*"), 
                          key=lambda x: x.stat().st_mtime, reverse=True)
        
        if not log_files:
            print(f"{Colors.YELLOW}⚠️ No log files found.{Colors.END}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}Recent logs:{Colors.END}")
        for i, f in enumerate(log_files[:15], 1):
            size = f.stat().st_size
            mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
            icon = "📄" if f.suffix == ".log" else "📊" if f.suffix == ".json" else "📝"
            print(f"  {i}. {icon} {f.name} ({size} bytes, {mtime})")
        
        if len(log_files) > 15:
            print(f"  ... and {len(log_files) - 15} more")
        
        choice = input(f"\n{Colors.YELLOW}View a file? (number or 'q' to skip): {Colors.END}")
        if choice.lower() == 'q':
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(log_files):
                f = log_files[idx]
                print(f"\n{Colors.CYAN}══════════════════════════════════════════════════════════════════════{Colors.END}")
                print(f"{Colors.WHITE}📄 {f.name}{Colors.END}")
                print(f"{Colors.CYAN}══════════════════════════════════════════════════════════════════════{Colors.END}")
                try:
                    with open(f, 'r') as fp:
                        content = fp.read()
                        print(content[:1500])
                        if len(content) > 1500:
                            print(f"\n{Colors.YELLOW}... (truncated, total {len(content)} characters){Colors.END}")
                except:
                    print(f"{Colors.RED}⚠️ Could not read file{Colors.END}")
        except:
            pass
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

    def open_android(self):
        """Buka folder Android"""
        android_dir = Path("/sdcard/Download/KosmikKey")
        android_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}📱 ANDROID FOLDER{Colors.CYAN}                                             ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
        print(f"  📁 Path: {android_dir}")
        print(f"  📄 Files: {len(list(android_dir.glob('*')))}")
        print(f"\n  {Colors.GREEN}✅ Folder accessible via File Manager{Colors.END}")
        print(f"  {Colors.YELLOW}   Path: Download → KosmikKey{Colors.END}")
        
        # Coba buka
        try:
            subprocess.run(['termux-open', str(android_dir)], capture_output=True)
        except:
            pass
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

    def open_dashboard(self):
        """Buka dashboard HTML"""
        android_dir = Path("/sdcard/Download/KosmikKey")
        dashboard = android_dir / "dashboard.html"
        
        if dashboard.exists():
            print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}🌐 HTML DASHBOARD{Colors.CYAN}                                              ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
            print(f"  📁 Dashboard: {dashboard}")
            print(f"  {Colors.GREEN}✅ Opening dashboard...{Colors.END}")
            
            try:
                subprocess.run(['termux-open', str(dashboard)], capture_output=True)
            except:
                print(f"  {Colors.YELLOW}⚠️ Could not open automatically{Colors.END}")
                print(f"  {Colors.YELLOW}   Open manually: File Manager → Download → KosmikKey → dashboard.html{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠️ Dashboard not found. Run Export first (Module 10).{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

    def reset_system(self):
        """Reset system"""
        print(f"""
{Colors.RED}╔══════════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}🔄 RESET SYSTEM{Colors.RED}                                                 ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
        print(f"{Colors.RED}⚠️  This will clear all log files!{Colors.END}")
        confirm = input(f"{Colors.YELLOW}Type 'RESET' to confirm: {Colors.END}")
        
        if confirm != 'RESET':
            print(f"{Colors.YELLOW}❌ Reset cancelled.{Colors.END}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            return
        
        import shutil
        if self.logs_dir.exists():
            shutil.rmtree(self.logs_dir)
            self.logs_dir.mkdir(parents=True)
            print(f"{Colors.GREEN}✅ Log files cleared.{Colors.END}")
        
        print(f"{Colors.GREEN}✅ System reset complete.{Colors.END}")
        input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")

    def system_info(self):
        """System info"""
        print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}ℹ️  SYSTEM INFORMATION{Colors.CYAN}                                         ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
        
        print(f"""
  {Colors.GREEN}🌀 APPLICATION:{Colors.END}
     Name: Kosmik Key
     Version: {self.version}
     Build: {self.build}
     Status: {Colors.GREEN}🟢 Active{Colors.END}

  {Colors.GREEN}📁 DIRECTORIES:{Colors.END}
     App: {self.kosmik_dir}
     Logs: {self.logs_dir}

  {Colors.GREEN}📦 MODULES:{Colors.END}
     Total: {len(self.modules)}
     Core: 10
     Exploration: 6

  {Colors.GREEN}📂 LOGS:{Colors.END}
""")
        if self.logs_dir.exists():
            log_files = list(self.logs_dir.glob("*"))
            log_size = sum(f.stat().st_size for f in log_files if f.is_file())
            print(f"     Files: {len(log_files)}")
            print(f"     Size: {log_size / 1024:.2f} KB")
        else:
            print(f"     No logs found")

        print(f"""
  {Colors.GREEN}🌌 FEDERATION:{Colors.END}
     Connection: {Colors.GREEN}🟢 Active{Colors.END}

  {Colors.GREEN}📱 ANDROID:{Colors.END}
""")
        android_dir = Path("/sdcard/Download/KosmikKey")
        if android_dir.exists():
            android_files = list(android_dir.glob("*"))
            print(f"     Export path: {android_dir}")
            print(f"     Files: {len(android_files)}")
        else:
            print(f"     No export found")

        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

    def run(self):
        """Main loop aplikasi"""
        while self.running:
            self.clear_screen()
            self.print_menu_baru()
            
            choice = input(f"\n{Colors.WHITE}📱 Enter your choice: {Colors.END}").strip().upper()
            
            if choice == 'F':
                self.full_scan()
            
            elif choice in self.modules:
                self.run_module(choice)
            
            elif choice == 'S':
                self.view_stats()
            
            elif choice == 'L':
                self.view_logs()
            
            elif choice == 'A':
                self.open_android()
            
            elif choice == 'D':
                self.open_dashboard()
            
            elif choice == 'R':
                self.reset_system()
            
            elif choice == 'I':
                self.system_info()
            
            elif choice == 'X':
                print(f"""
{Colors.GOLD}╔══════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║   {Colors.WHITE}👋 Goodbye, Traveler!{Colors.GOLD}                                                 ║
║   {Colors.CYAN}🌌 Kosmik Key v8.0 — Signing off...{Colors.GOLD}                              ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
                self.running = False
                time.sleep(1)
            
            else:
                print(f"{Colors.RED}❌ Invalid choice: '{choice}'{Colors.END}")
                print(f"{Colors.YELLOW}   Please enter: F, 1-16, S, L, A, D, R, I, X{Colors.END}")
                input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")

# ============================================================
#  INSTALL SEMUA MODUL YANG BELUM ADA
# ============================================================
def install_all_modules():
    """Install semua modul yang belum ada"""
    print(f"""
{Colors.GOLD}╔══════════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}📦 INSTALLING ALL MODULES{Colors.GOLD}                                     ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
    
    modules_to_install = [
        ('scanner.py', 'scanner'),
        ('alerter.py', 'alerter'),
        ('sensor_reader.py', 'sensor_reader'),
        ('advanced_detector.py', 'advanced_detector'),
        ('super_advanced.py', 'super_advanced'),
        ('quantum_entity.py', 'quantum_entity'),
        ('consciousness_navigation.py', 'consciousness_navigation'),
        ('federation_contact.py', 'federation_contact'),
        ('federation_database.py', 'federation_database'),
        ('export_android.py', 'export_android'),
        ('hidden_dimensions.py', 'hidden_dimensions'),
        ('travel_log.py', 'travel_log'),
        ('multiverse_map.py', 'multiverse_map'),
        ('alien_translator.py', 'alien_translator'),
        ('cosmic_predictor.py', 'cosmic_predictor'),
        ('time_travel.py', 'time_travel')
    ]
    
    kosmik_dir = Path.home() / "kosmik"
    kosmik_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, module_name in modules_to_install:
        filepath = kosmik_dir / filename
        if not filepath.exists():
            print(f"{Colors.YELLOW}⚠️ {filename} not found. Creating placeholder...{Colors.END}")
            with open(filepath, 'w') as f:
                f.write(f'''#!/usr/bin/env python3
# {module_name}.py — Kosmik Key v8.0
print("🌀 {module_name} — Running...")
print("📡 Scanning...")
print("✅ Done!")
''')
            filepath.chmod(0o755)
    
    print(f"{Colors.GREEN}✅ All modules installed!{Colors.END}")

# ============================================================
#  MAIN
# ============================================================
if __name__ == "__main__":
    try:
        # Install modules pertama kali
        install_all_modules()
        
        # Jalankan app
        app = KosmikApp()
        app.run()
    except KeyboardInterrupt:
        print(f"""
{Colors.GOLD}╔══════════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}👋 Kosmik Key v8.0 — Exiting{Colors.GOLD}                                  ║
║  {Colors.CYAN}🌌 Until we meet again, Traveler!{Colors.GOLD}                             ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
        sys.exit(0)
