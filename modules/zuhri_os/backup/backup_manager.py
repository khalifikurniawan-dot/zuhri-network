#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI BACKUP & RESTORE MANAGER
Backup Lengkap + Signature + Manifest + List
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, shutil, hashlib, tarfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
BACKUP_DIR = os.path.join(HOME, "zuhri_os", "backup", "data")
MANIFEST_DIR = os.path.join(HOME, "zuhri_os", "backup", "manifests")
LOG_DIR = os.path.join(HOME, "zuhri_os", "backup", "logs")
SDCARD_DIR = "/sdcard/backup_zuhri"

for d in [BACKUP_DIR, MANIFEST_DIR, LOG_DIR, SDCARD_DIR]:
    try: os.makedirs(d, exist_ok=True)
    except: pass

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

# ===== FILE YANG DI-BACKUP =====
BACKUP_ITEMS = {
    "bashrc": os.path.join(HOME, ".bashrc"),
    "menu": os.path.join(HOME, "zuhri_os", "menu.py"),
    "zuhri_os": os.path.join(HOME, "zuhri_os", "zuhri_os.py"),
    "zuhri_id": os.path.join(HOME, "zuhri_os", "id", "zuhri_id.py"),
    "zuhri_auth": os.path.join(HOME, "zuhri_os", "id", "zuhri_auth.py"),
    "zuhri_crypto": os.path.join(HOME, "zuhri_os", "crypto", "zuhri_crypto.py"),
    "backup_mgr": os.path.join(HOME, "zuhri_os", "backup", "backup_manager.py"),
    "key_sh": os.path.join(HOME, "kosmik", "key.sh"),
    "mesh_node": os.path.join(HOME, "kosmik", "p2p", "mesh_node.py"),
    "mesh_scan": os.path.join(HOME, "kosmik", "p2p", "mesh_discovery.py"),
    "sos_beacon": os.path.join(HOME, "kosmik", "sos_beacon.py"),
    "zuhri_py": os.path.join(HOME, "zuhri.py"),
    "health_py": os.path.join(HOME, "health.py"),
    "updater_py": os.path.join(HOME, "updater.py"),
    "darkweb_bin": "/data/data/com.termux/files/usr/bin/dark-web",
    "chain": os.path.join(HOME, "zuhri_os", "chain", "zuhri_chain.py"),
    "edu": os.path.join(HOME, "zuhri_os", "edu", "zuhri_edu.py"),
    "finance": os.path.join(HOME, "zuhri_os", "finance", "zuhri_finance.py"),
    "library": os.path.join(HOME, "zuhri_os", "library", "zuhri_library.py"),
    "spiritual": os.path.join(HOME, "zuhri_os", "spiritual", "zuhri_spiritual.py"),
    "kurikulum": os.path.join(HOME, "zuhri_os", "kurikulum", "zuhri_kurikulum.py"),
    "peringatan": os.path.join(HOME, "zuhri_os", "peringatan", "zuhri_peringatan.py"),
    "frekuensi": os.path.join(HOME, "zuhri_os", "frekuensi", "zuhri_frekuensi.py"),
    "predictive": os.path.join(HOME, "zuhri_os", "predictive", "zuhri_predictive.py"),
    "energi": os.path.join(HOME, "zuhri_os", "energi", "zuhri_energi.py"),
    "botnet": os.path.join(HOME, "zuhri_os", "botnet", "zuhri_botnet.py"),
    "passport": os.path.join(HOME, "zuhri_os", "passport", "zuhri_passport.py"),
    "vote": os.path.join(HOME, "zuhri_os", "vote", "zuhri_vote.py"),
    "contract": os.path.join(HOME, "zuhri_os", "contract", "zuhri_contract.py"),
    "wallet": os.path.join(HOME, "zuhri_os", "wallet", "wallet.py"),
    "security": os.path.join(HOME, "zuhri_os", "security", "security_shield.py"),
    "translator": os.path.join(HOME, "zuhri_os", "translator", "translator.py"),
    "version": os.path.join(HOME, "zuhri_os", "version", "version_monitor.py"),
}

# ============================================================
# UTIL
# ============================================================
def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024: return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"

def get_sha256(filepath):
    sha = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha.update(chunk)
        return sha.hexdigest()
    except: return None

def get_id_badge():
    if not ZUHRI_ID_OK: return f"{YELLOW}⚠️  TANPA ID{RESET}"
    i = load_identity()
    return f"{GREEN}✅ {i['name']}{RESET}" if i else f"{YELLOW}⚠️{RESET}"

# ============================================================
# BACKUP
# ============================================================
def do_backup():
    os.system('clear')
    
    if not ZUHRI_ID_OK:
        print(f"{YELLOW}⚠️  Tidak ada Zuhri ID — backup tanpa signature{RESET}\n")
    
    identity = load_identity() if ZUHRI_ID_OK else None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"zuhri_backup_{timestamp}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    os.makedirs(backup_path, exist_ok=True)
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  💾 ZUHRI BACKUP MANAGER — MEMBUAT BACKUP                      ║
║  ──────────────────────────────────────────────────────────────  ║
║  Waktu    : {GOLD}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}
║  Operator : {get_id_badge()}
║  Tujuan   : {GOLD}{backup_path}{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    total_size = 0
    success = 0
    failed = 0
    file_hashes = {}
    
    for name, path in BACKUP_ITEMS.items():
        if os.path.exists(path):
            try:
                dest = os.path.join(backup_path, name)
                shutil.copy2(path, dest)
                size = os.path.getsize(path)
                total_size += size
                success += 1
                fh = get_sha256(path)
                if fh: file_hashes[name] = fh
                print(f"  {GREEN}✅{RESET} {name:15} → {format_size(size)}")
            except Exception as e:
                failed += 1
                print(f"  {RED}❌{RESET} {name}: {e}")
        else:
            print(f"  {YELLOW}⚠️ {RESET} {name} (tidak ada)")
    
    # Manifest
    manifest = {
        "backup_name": backup_name,
        "timestamp": timestamp,
        "date": datetime.now().isoformat(),
        "operator": {
            "zuhri_id": identity['zuhri_id'] if identity else None,
            "name": identity['name'] if identity else "Anonymous",
            "role": identity.get('role', 'Operator') if identity else None
        },
        "files": file_hashes,
        "total_size": total_size,
        "success": success,
        "failed": failed,
        "version": "2.0"
    }
    
    # Tanda tangan
    if ZUHRI_ID_OK and identity:
        manifest_str = json.dumps(manifest, sort_keys=True)
        sig = sign(manifest_str)
        if sig:
            manifest['signature'] = sig
            print(f"\n  {GREEN}🔐 Manifest ditandatangani Zuhri ID{RESET}")
    
    # Simpan manifest
    manifest_file = os.path.join(backup_path, "manifest.json")
    json.dump(manifest, open(manifest_file, "w"), indent=2)
    
    manifest_archive = os.path.join(MANIFEST_DIR, f"{backup_name}_manifest.json")
    json.dump(manifest, open(manifest_archive, "w"), indent=2)
    
    # Buat arsip
    archive = os.path.join(BACKUP_DIR, f"{backup_name}.tar.gz")
    try:
        with tarfile.open(archive, "w:gz") as tar:
            tar.add(backup_path, arcname=backup_name)
        archive_size = os.path.getsize(archive)
        print(f"\n  {GREEN}📦 Arsip:{RESET} {format_size(archive_size)}")
    except Exception as e:
        print(f"  {RED}❌ Gagal buat arsip: {e}{RESET}")
    
    # Copy ke sdcard
    try:
        shutil.copy2(archive, os.path.join(SDCARD_DIR, f"{backup_name}.tar.gz"))
        shutil.copy2(manifest_archive, os.path.join(SDCARD_DIR, f"{backup_name}_manifest.json"))
        print(f"  {GOLD}💾 Di HP:{RESET} {SDCARD_DIR}/")
    except: pass
    
    if ZUHRI_ID_OK:
        log_verified(f"BACKUP: {backup_name} ({success} file)")
    
    print(f"""
{DIM}{'─' * 65}{RESET}
{GREEN}✅ BACKUP SELESAI!{RESET}
   Berhasil : {success}
   Gagal    : {failed}
   Total    : {format_size(total_size)}
{DIM}{'─' * 65}{RESET}
""")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# LIST BACKUP (Informatif)
# ============================================================
def list_backups():
    os.system('clear')
    archives = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.tar.gz')], reverse=True)
    
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  📂 DAFTAR BACKUP — ZUHRI BACKUP MANAGER                        ║
║  ──────────────────────────────────────────────────────────────  ║
║  Operator: {get_id_badge()}
║  Total Backup: {GOLD}{len(archives)}{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    if not archives:
        print(f"{YELLOW}Belum ada backup.{RESET}")
        print(f"{DIM}Buat backup dengan: backup{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return []
    
    total_size = sum(os.path.getsize(os.path.join(BACKUP_DIR, a)) for a in archives)
    print(f"{BOLD}📊 Total ukuran:{RESET} {format_size(total_size)}\n")
    
    for i, a in enumerate(archives, 1):
        path = os.path.join(BACKUP_DIR, a)
        size = format_size(os.path.getsize(path))
        
        manifest_name = a.replace('.tar.gz', '_manifest.json')
        manifest_file = os.path.join(MANIFEST_DIR, manifest_name)
        
        operator = "N/A"
        operator_id = "N/A"
        signed = f"{RED}❌{RESET}"
        date = "N/A"
        files = 0
        
        if os.path.exists(manifest_file):
            try:
                m = json.load(open(manifest_file))
                operator = m.get('operator', {}).get('name', 'N/A')
                operator_id = m.get('operator', {}).get('zuhri_id', 'N/A')
                date = m.get('date', 'N/A')[:19]
                signed = f"{GREEN}✅ VALID{RESET}" if 'signature' in m else f"{YELLOW}⚠️  NO SIG{RESET}"
                files = m.get('success', 0)
            except: pass
        
        print(f"{BOLD}{GOLD}━━━ #{i} ━━━{RESET}")
        print(f"  {CYAN}📦 Nama{RESET}      : {a}")
        print(f"  {CYAN}📅 Tanggal{RESET}   : {date}")
        print(f"  {CYAN}💾 Ukuran{RESET}    : {size}")
        print(f"  {CYAN}📄 Files{RESET}     : {files} file")
        print(f"  {CYAN}👤 Operator{RESET}  : {operator}")
        print(f"  {CYAN}🔐 Signature{RESET} : {signed}")
        print()
    
    print(f"{DIM}{'─' * 65}{RESET}")
    print(f"{GOLD}Total:{RESET} {len(archives)} backup")
    print(f"{GOLD}Total Ukuran:{RESET} {format_size(total_size)}")
    print(f"{DIM}{'─' * 65}{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")
    return archives

# ============================================================
# RESTORE
# ============================================================
def do_restore():
    archives = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.tar.gz')], reverse=True)
    
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🔄 ZUHRI RESTORE MANAGER — RESTORE BACKUP                     ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    if not archives:
        print(f"{YELLOW}Belum ada backup.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    for i, a in enumerate(archives, 1):
        path = os.path.join(BACKUP_DIR, a)
        size = format_size(os.path.getsize(path))
        print(f"  {GOLD}{i}.{RESET} {a} {DIM}({size}){RESET}")
    
    try:
        c = int(input(f"\n{CYAN}Pilih backup: {RESET}")) - 1
        if not (0 <= c < len(archives)): return
        
        archive = os.path.join(BACKUP_DIR, archives[c])
        manifest_name = archives[c].replace('.tar.gz', '_manifest.json')
        manifest_file = os.path.join(MANIFEST_DIR, manifest_name)
        
        # Verifikasi manifest
        if os.path.exists(manifest_file) and ZUHRI_ID_OK:
            m = json.load(open(manifest_file))
            if 'signature' in m:
                m_copy = m.copy()
                sig = m_copy.pop('signature')
                m_str = json.dumps(m_copy, sort_keys=True)
                
                my_id = load_identity()
                if my_id and my_id['zuhri_id'] == m['operator']['zuhri_id']:
                    if verify(m_str, sig, my_id['public_key']):
                        print(f"\n{GREEN}✅ Manifest terverifikasi (by {m['operator']['name']}){RESET}")
                    else:
                        print(f"\n{YELLOW}⚠️  Manifest signature tidak valid{RESET}")
                else:
                    print(f"\n{YELLOW}⚠️  Backup dibuat oleh: {m['operator']['name']}{RESET}")
        
        confirm = input(f"\n{YELLOW}⚠️  Restore akan menimpa file saat ini. Lanjutkan? (y/n): {RESET}").strip().lower()
        if confirm != 'y':
            print(f"{CYAN}❌ Dibatalkan{RESET}\n")
            input(f"{DIM}Enter...{RESET}")
            return
        
        temp_dir = os.path.join(BACKUP_DIR, "_temp_restore")
        if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        try:
            with tarfile.open(archive, "r:gz") as tar:
                tar.extractall(temp_dir)
            
            extracted = os.listdir(temp_dir)
            if extracted:
                src_dir = os.path.join(temp_dir, extracted[0])
                
                success = 0
                failed = 0
                
                for name, path in BACKUP_ITEMS.items():
                    src = os.path.join(src_dir, name)
                    if os.path.exists(src):
                        try:
                            if os.path.exists(path):
                                backup_old = path + f".before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                                shutil.copy2(path, backup_old)
                            
                            shutil.copy2(src, path)
                            success += 1
                            print(f"  {GREEN}✅{RESET} {name}")
                        except Exception as e:
                            failed += 1
                            print(f"  {RED}❌{RESET} {name}: {e}")
                
                print(f"""
{DIM}{'─' * 65}{RESET}
{GREEN}✅ RESTORE SELESAI!{RESET}
   Berhasil : {success}
   Gagal    : {failed}
{DIM}{'─' * 65}{RESET}
""")
                
                if ZUHRI_ID_OK:
                    log_verified(f"RESTORE: {archives[c]} ({success} file)", "WARN")
            
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"{RED}❌ Gagal extract: {e}{RESET}")
    except ValueError: pass
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# VERIFIKASI
# ============================================================
def verify_backup():
    archives = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.tar.gz')], reverse=True)
    
    os.system('clear')
    print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  🔐 VERIFIKASI BACKUP                                          ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    if not archives:
        print(f"{YELLOW}Belum ada backup.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    for i, a in enumerate(archives, 1):
        print(f"  {GOLD}{i}.{RESET} {a}")
    
    try:
        c = int(input(f"\n{CYAN}Pilih: {RESET}")) - 1
        if not (0 <= c < len(archives)): return
        
        archive = archives[c]
        manifest_name = archive.replace('.tar.gz', '_manifest.json')
        manifest_file = os.path.join(MANIFEST_DIR, manifest_name)
        
        print(f"\n{BOLD}{CYAN}📊 INFORMASI BACKUP{RESET}\n")
        print(f"  File: {archive}")
        print(f"  Path: {BACKUP_DIR}/{archive}")
        
        if os.path.exists(manifest_file):
            m = json.load(open(manifest_file))
            print(f"\n  {GOLD}Operator:{RESET} {m['operator']['name']}")
            print(f"  {GOLD}Zuhri ID:{RESET} {m['operator']['zuhri_id']}")
            print(f"  {GOLD}Tanggal:{RESET}  {m['date'][:19]}")
            print(f"  {GOLD}Files:{RESET}    {m['success']}")
            print(f"  {GOLD}Size:{RESET}     {format_size(m['total_size'])}")
            
            if 'signature' in m and ZUHRI_ID_OK:
                m_copy = m.copy()
                sig = m_copy.pop('signature')
                m_str = json.dumps(m_copy, sort_keys=True)
                my_id = load_identity()
                
                if my_id and my_id['zuhri_id'] == m['operator']['zuhri_id']:
                    if verify(m_str, sig, my_id['public_key']):
                        print(f"\n  {GREEN}✅ Tanda tangan VALID — Backup ASLI{RESET}")
                    else:
                        print(f"\n  {RED}❌ Tanda tangan TIDAK VALID!{RESET}")
                else:
                    print(f"\n  {YELLOW}⚠️  Backup dibuat oleh orang lain{RESET}")
        else:
            print(f"\n  {YELLOW}⚠️  Manifest tidak ada{RESET}")
    except ValueError: pass
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# EXPORT
# ============================================================
def export_backup():
    archives = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.tar.gz')], reverse=True)
    
    os.system('clear')
    print(f"\n{BOLD}{CYAN}📤 EXPORT BACKUP KE SDCARD{RESET}\n")
    
    if not archives:
        print(f"{YELLOW}Belum ada backup.{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    for i, a in enumerate(archives, 1):
        print(f"  {GOLD}{i}.{RESET} {a}")
    
    print(f"  {GOLD}a.{RESET} Semua")
    
    try:
        c = input(f"\n{CYAN}Pilih: {RESET}").strip().lower()
        
        if c == "a":
            for a in archives:
                shutil.copy2(os.path.join(BACKUP_DIR, a), os.path.join(SDCARD_DIR, a))
                manifest_name = a.replace('.tar.gz', '_manifest.json')
                mf = os.path.join(MANIFEST_DIR, manifest_name)
                if os.path.exists(mf):
                    shutil.copy2(mf, os.path.join(SDCARD_DIR, manifest_name))
            print(f"\n{GREEN}✅ Semua backup di-export ke {SDCARD_DIR}/{RESET}\n")
        else:
            idx = int(c) - 1
            if 0 <= idx < len(archives):
                a = archives[idx]
                shutil.copy2(os.path.join(BACKUP_DIR, a), os.path.join(SDCARD_DIR, a))
                print(f"\n{GREEN}✅ {a} di-export{RESET}\n")
    except: pass
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# CLEANUP
# ============================================================
def cleanup():
    archives = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.tar.gz')])
    
    os.system('clear')
    print(f"\n{BOLD}{CYAN}🗑️  HAPUS BACKUP LAMA{RESET}\n")
    
    if len(archives) <= 5:
        print(f"{GREEN}✅ Backup ≤ 5, tidak perlu hapus{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    old = archives[:-5]
    print(f"{YELLOW}⚠️  Akan menghapus {len(old)} backup lama:{RESET}\n")
    for a in old:
        print(f"  {DIM}• {a}{RESET}")
    
    confirm = input(f"\n{CYAN}Lanjutkan? (y/n): {RESET}").strip().lower()
    if confirm == "y":
        for a in old:
            try:
                os.remove(os.path.join(BACKUP_DIR, a))
                manifest_name = a.replace('.tar.gz', '_manifest.json')
                mf = os.path.join(MANIFEST_DIR, manifest_name)
                if os.path.exists(mf): os.remove(mf)
            except: pass
        print(f"\n{GREEN}✅ {len(old)} backup lama dihapus (sisa 5){RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        os.system('clear')
        archives = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.tar.gz')] if os.path.exists(BACKUP_DIR) else []
        
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  💾 ZUHRI BACKUP & RESTORE MANAGER                             ║
║  ──────────────────────────────────────────────────────────────  ║
║  Operator: {get_id_badge()}
║  Total Backup: {GOLD}{len(archives)}{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  💾 Buat Backup Baru
  {GOLD}2.{RESET}  📂 List Backup (Daftar Lengkap)
  {GOLD}3.{RESET}  🔄 Restore dari Backup
  {GOLD}4.{RESET}  🔐 Verifikasi Backup
  {GOLD}5.{RESET}  📤 Export ke Sdcard
  {GOLD}6.{RESET}  🗑️  Hapus Backup Lama
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-6): {RESET}").strip()
            if c == "0": break
            elif c == "1": do_backup()
            elif c == "2": list_backups()
            elif c == "3": do_restore()
            elif c == "4": verify_backup()
            elif c == "5": export_backup()
            elif c == "6": cleanup()
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "backup": do_backup()
        elif cmd == "list": list_backups()
        elif cmd == "restore": do_restore()
        elif cmd == "verify": verify_backup()
        elif cmd == "export": export_backup()
        elif cmd == "cleanup": cleanup()
        else: menu()
    else: menu()
