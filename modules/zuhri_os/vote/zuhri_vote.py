#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI VOTE — VOTING DIGITAL
1 Zuhri ID = 1 Suara | Terverifikasi Ed25519
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os
import sys
import json
import base64
import hashlib
import secrets
from datetime import datetime

# ===== ZUHRI AUTH =====
sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, verify, log_verified, get_status
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

# ===== KONFIGURASI =====
HOME = os.path.expanduser("~")
VOTE_DIR = os.path.join(HOME, "zuhri_os", "vote")
POLLS_DIR = os.path.join(VOTE_DIR, "polls")
VOTES_DIR = os.path.join(VOTE_DIR, "votes")
os.makedirs(POLLS_DIR, exist_ok=True)
os.makedirs(VOTES_DIR, exist_ok=True)

# ===== WARNA =====
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GOLD = "\033[93m"

# ============================================================
# UTIL
# ============================================================
def get_id_badge():
    if not ZUHRI_ID_OK:
        return f"{YELLOW}⚠️  TANPA ZUHRI ID{RESET}"
    s = get_status()
    if s['active']:
        return f"{GREEN}✅ {s['name']} ({s['zuhri_id'][:20]}...){RESET}"
    return f"{YELLOW}⚠️  TANPA ZUHRI ID{RESET}"

def get_poll_id():
    return "poll_" + secrets.token_hex(8)

def list_polls():
    """Daftar semua voting"""
    polls = sorted([f.replace('.json', '') for f in os.listdir(POLLS_DIR) if f.endswith('.json')])
    return polls

# ============================================================
# BUAT VOTING
# ============================================================
def create_poll():
    """Buat voting baru"""
    if not ZUHRI_ID_OK:
        print(f"{RED}❌ Butuh Zuhri ID. Jalankan: id create{RESET}")
        return
    
    identity = load_identity()
    if not identity:
        print(f"{RED}❌ Zuhri ID tidak ditemukan{RESET}")
        return
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🗳️  ZUHRI VOTE — BUAT VOTING BARU                             ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    question = input("📝 Pertanyaan: ").strip()
    if not question:
        print(f"{RED}❌ Pertanyaan tidak boleh kosong{RESET}")
        return
    
    print(f"\n{CYAN}Masukkan pilihan (minimal 2, kosong untuk selesai):{RESET}")
    options = []
    i = 1
    while True:
        opt = input(f"  Pilihan {i}: ").strip()
        if not opt:
            break
        options.append(opt)
        i += 1
    
    if len(options) < 2:
        print(f"{RED}❌ Minimal 2 pilihan{RESET}")
        return
    
    poll_id = get_poll_id()
    poll = {
        "poll_id": poll_id,
        "question": question,
        "options": options,
        "creator": {
            "zuhri_id": identity['zuhri_id'],
            "name": identity['name']
        },
        "created": datetime.now().isoformat(),
        "expire": None,
        "status": "open"
    }
    
    # Tanda tangani poll
    poll_copy = poll.copy()
    poll_str = json.dumps(poll_copy, sort_keys=True)
    sig = sign(poll_str)
    if sig:
        poll['signature'] = sig
        poll['public_key'] = identity['public_key']
    
    # Simpan
    poll_file = os.path.join(POLLS_DIR, f"{poll_id}.json")
    with open(poll_file, 'w') as f:
        json.dump(poll, f, indent=2)
    
    # Buat folder votes
    poll_votes_dir = os.path.join(VOTES_DIR, poll_id)
    os.makedirs(poll_votes_dir, exist_ok=True)
    
    log_verified(f"VOTE_CREATE: {poll_id} — {question[:50]}")
    
    print(f"""
{BOLD}{GREEN}✅ VOTING DIBUAT!{RESET}

{GOLD}🆔 Poll ID:{RESET}  {poll_id}
{GOLD}📝 Pertanyaan:{RESET} {question}
{GOLD}📋 Pilihan:{RESET}""")
    
    for i, opt in enumerate(options, 1):
        print(f"     {i}. {opt}")
    
    print(f"""
{GOLD}👤 Dibuat oleh:{RESET} {identity['name']}
{GOLD}🔐 Ditandatangani:{RESET} ✅
""")

# ============================================================
# VOTE
# ============================================================
def do_vote():
    """Vote di poll"""
    if not ZUHRI_ID_OK:
        print(f"{RED}❌ Butuh Zuhri ID{RESET}")
        return
    
    identity = load_identity()
    if not identity:
        print(f"{RED}❌ Zuhri ID tidak ditemukan{RESET}")
        return
    
    polls = list_polls()
    if not polls:
        print(f"{YELLOW}⚠️  Belum ada voting.{RESET}")
        return
    
    # Pilih poll
    print(f"\n{BOLD}{CYAN}📋 DAFTAR VOTING:{RESET}\n")
    for i, p in enumerate(polls, 1):
        poll_data = json.load(open(os.path.join(POLLS_DIR, f"{p}.json")))
        print(f"  {GOLD}{i}.{RESET} {poll_data['question']}")
        print(f"     {DIM}ID: {p}{RESET}")
    
    try:
        choice = int(input(f"\n{CYAN}Pilih nomor: {RESET}").strip()) - 1
        if not (0 <= choice < len(polls)):
            return
        
        poll_id = polls[choice]
        poll_file = os.path.join(POLLS_DIR, f"{poll_id}.json")
        poll = json.load(open(poll_file))
        
        if poll['status'] != 'open':
            print(f"{RED}❌ Voting sudah ditutup{RESET}")
            return
        
        # Cek sudah vote belum
        vote_file = os.path.join(VOTES_DIR, poll_id, f"{identity['zuhri_id']}.json")
        if os.path.exists(vote_file):
            print(f"{YELLOW}⚠️  Anda sudah vote di polling ini!{RESET}")
            print(f"{DIM}1 Zuhri ID = 1 Suara{RESET}")
            return
        
        # Tampilkan pilihan
        print(f"\n{BOLD}{CYAN}📝 {poll['question']}{RESET}\n")
        for i, opt in enumerate(poll['options'], 1):
            print(f"  {GOLD}{i}.{RESET} {opt}")
        
        try:
            vote_choice = int(input(f"\n{CYAN}Pilih nomor (1-{len(poll['options'])}): {RESET}").strip()) - 1
            if not (0 <= vote_choice < len(poll['options'])):
                print(f"{RED}❌ Pilihan tidak valid{RESET}")
                return
            
            # Buat vote
            vote_data = {
                "poll_id": poll_id,
                "voter": {
                    "zuhri_id": identity['zuhri_id'],
                    "name": identity['name']
                },
                "choice": vote_choice,
                "choice_text": poll['options'][vote_choice],
                "voted_at": datetime.now().isoformat()
            }
            
            # Tanda tangani
            vote_str = json.dumps(vote_data, sort_keys=True)
            sig = sign(vote_str)
            if sig:
                vote_data['signature'] = sig
                vote_data['public_key'] = identity['public_key']
            
            # Simpan
            with open(vote_file, 'w') as f:
                json.dump(vote_data, f, indent=2)
            
            log_verified(f"VOTE_CAST: {poll_id} → {poll['options'][vote_choice]}")
            
            print(f"""
{BOLD}{GREEN}✅ VOTE BERHASIL!{RESET}

{GOLD}📝 Voting:{RESET} {poll['question']}
{GOLD}🗳️  Pilihan:{RESET} {poll['options'][vote_choice]}
{GOLD}🆔 Voter:{RESET} {identity['zuhri_id']}
{GOLD}🔐 Ditandatangani:{RESET} ✅
""")
        except ValueError:
            print(f"{RED}❌ Input tidak valid{RESET}")
    except ValueError:
        pass

# ============================================================
# HASIL VOTING
# ============================================================
def show_results():
    """Tampilkan hasil voting"""
    polls = list_polls()
    if not polls:
        print(f"{YELLOW}⚠️  Belum ada voting.{RESET}")
        return
    
    print(f"\n{BOLD}{CYAN}📋 DAFTAR VOTING:{RESET}\n")
    for i, p in enumerate(polls, 1):
        poll_data = json.load(open(os.path.join(POLLS_DIR, f"{p}.json")))
        print(f"  {GOLD}{i}.{RESET} {poll_data['question']}")
    
    try:
        choice = int(input(f"\n{CYAN}Pilih nomor: {RESET}").strip()) - 1
        if not (0 <= choice < len(polls)):
            return
        
        poll_id = polls[choice]
        poll = json.load(open(os.path.join(POLLS_DIR, f"{poll_id}.json")))
        
        # Hitung votes
        poll_votes_dir = os.path.join(VOTES_DIR, poll_id)
        votes = []
        if os.path.exists(poll_votes_dir):
            for vf in os.listdir(poll_votes_dir):
                if vf.endswith('.json'):
                    v = json.load(open(os.path.join(poll_votes_dir, vf)))
                    votes.append(v)
        
        # Hitung per pilihan
        counts = [0] * len(poll['options'])
        valid_votes = 0
        invalid_votes = 0
        
        for v in votes:
            # Verifikasi signature
            vote_copy = v.copy()
            sig = vote_copy.pop('signature', None)
            pub = vote_copy.pop('public_key', None)
            
            if sig and pub:
                vote_str = json.dumps(vote_copy, sort_keys=True)
                # Verifikasi pakai public key voter
                if verify(vote_str, sig, pub):
                    counts[v['choice']] += 1
                    valid_votes += 1
                else:
                    invalid_votes += 1
            else:
                counts[v['choice']] += 1
                valid_votes += 1
        
        total = sum(counts)
        
        print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📊 HASIL VOTING — ZUHRI VOTE                                  ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{GOLD}📝 Pertanyaan:{RESET} {poll['question']}
{GOLD}👤 Dibuat oleh:{RESET} {poll['creator']['name']}
{GOLD}📅 Dibuat:{RESET} {poll['created'][:19]}
{GOLD}📊 Status:{RESET} {poll['status'].upper()}
{GOLD}🗳️  Total Suara:{RESET} {total} (valid: {valid_votes}, invalid: {invalid_votes})

{'─' * 65}
{BOLD}  HASIL:{RESET}
{'─' * 65}""")
        
        # Urutkan berdasarkan count
        sorted_results = sorted(enumerate(counts), key=lambda x: x[1], reverse=True)
        
        for rank, (idx, count) in enumerate(sorted_results, 1):
            opt = poll['options'][idx]
            pct = (count / total * 100) if total > 0 else 0
            bar_len = int(pct / 5)  # 20 char max
            bar = "█" * bar_len + "░" * (20 - bar_len)
            
            # Warna
            if rank == 1 and count > 0:
                color = GREEN
            elif rank == 2:
                color = CYAN
            else:
                color = DIM
            
            print(f"  {GOLD}{idx+1}.{RESET} {color}{opt:30}{RESET}  {count:3} ({pct:5.1f}%)")
            print(f"     {color}{bar}{RESET}")
        
        print(f"{'─' * 65}\n")
        
        log_verified(f"VOTE_RESULT: {poll_id} — {total} suara")
        
    except ValueError:
        pass

# ============================================================
# VERIFIKASI VOTE
# ============================================================
def verify_votes():
    """Verifikasi semua vote di poll"""
    polls = list_polls()
    if not polls:
        print(f"{YELLOW}⚠️  Belum ada voting.{RESET}")
        return
    
    print(f"\n{BOLD}{CYAN}📋 DAFTAR VOTING:{RESET}\n")
    for i, p in enumerate(polls, 1):
        poll_data = json.load(open(os.path.join(POLLS_DIR, f"{p}.json")))
        print(f"  {GOLD}{i}.{RESET} {poll_data['question']}")
    
    try:
        choice = int(input(f"\n{CYAN}Pilih nomor: {RESET}").strip()) - 1
        if not (0 <= choice < len(polls)):
            return
        
        poll_id = polls[choice]
        poll_votes_dir = os.path.join(VOTES_DIR, poll_id)
        
        if not os.path.exists(poll_votes_dir):
            print(f"{YELLOW}⚠️  Belum ada vote{RESET}")
            return
        
        print(f"\n{BOLD}{CYAN}🔐 VERIFIKASI VOTE — {poll_id}{RESET}\n")
        
        valid = 0
        invalid = 0
        details = []
        
        for vf in os.listdir(poll_votes_dir):
            if vf.endswith('.json'):
                v = json.load(open(os.path.join(poll_votes_dir, vf)))
                
                vote_copy = v.copy()
                sig = vote_copy.pop('signature', None)
                pub = vote_copy.pop('public_key', None)
                
                if sig and pub:
                    vote_str = json.dumps(vote_copy, sort_keys=True)
                    is_valid = verify(vote_str, sig, pub)
                    
                    status = f"{GREEN}✅ VALID{RESET}" if is_valid else f"{RED}❌ INVALID{RESET}"
                    print(f"  {status} {v['voter']['name']:20} → {v['choice_text']}")
                    print(f"         {DIM}{v['voter']['zuhri_id'][:32]}...{RESET}")
                    
                    if is_valid:
                        valid += 1
                    else:
                        invalid += 1
                else:
                    print(f"  {YELLOW}⚠️  NO SIG{RESET} {v['voter']['name']}")
                    invalid += 1
        
        print(f"""
{'─' * 65}
{GOLD}📊 Hasil Verifikasi:{RESET}
   {GREEN}✅ Valid  : {valid}{RESET}
   {RED}❌ Invalid: {invalid}{RESET}
{'─' * 65}
""")
    except ValueError:
        pass

# ============================================================
# HAPUS VOTE
# ============================================================
def delete_vote():
    """Hapus polling (hanya creator)"""
    if not ZUHRI_ID_OK:
        print(f"{RED}❌ Butuh Zuhri ID{RESET}")
        return
    
    identity = load_identity()
    polls = list_polls()
    
    if not polls:
        print(f"{YELLOW}⚠️  Belum ada voting.{RESET}")
        return
    
    print(f"\n{BOLD}{CYAN}📋 DAFTAR VOTING:{RESET}\n")
    for i, p in enumerate(polls, 1):
        poll_data = json.load(open(os.path.join(POLLS_DIR, f"{p}.json")))
        creator = poll_data['creator']['name']
        mark = " ← [MILIK ANDA]" if poll_data['creator']['zuhri_id'] == identity['zuhri_id'] else ""
        print(f"  {GOLD}{i}.{RESET} {poll_data['question']} {DIM}oleh {creator}{RESET}{mark}")
    
    try:
        choice = int(input(f"\n{CYAN}Pilih nomor: {RESET}").strip()) - 1
        if not (0 <= choice < len(polls)):
            return
        
        poll_id = polls[choice]
        poll = json.load(open(os.path.join(POLLS_DIR, f"{poll_id}.json")))
        
        if poll['creator']['zuhri_id'] != identity['zuhri_id']:
            print(f"{RED}❌ Anda bukan pembuat voting ini{RESET}")
            return
        
        confirm = input(f"{YELLOW}⚠️  Hapus voting '{poll['question']}'? (y/n): {RESET}").strip().lower()
        if confirm == 'y':
            os.remove(os.path.join(POLLS_DIR, f"{poll_id}.json"))
            poll_votes_dir = os.path.join(VOTES_DIR, poll_id)
            if os.path.exists(poll_votes_dir):
                import shutil
                shutil.rmtree(poll_votes_dir)
            
            log_verified(f"VOTE_DELETE: {poll_id}", "WARN")
            print(f"{GREEN}✅ Voting dihapus{RESET}")
    except ValueError:
        pass

# ============================================================
# HELP
# ============================================================
def show_help():
    print(f"""
{BOLD}{CYAN}🗳️  ZUHRI VOTE — BANTUAN{RESET}
{'─' * 55}
  {BOLD}vote create{RESET}      → Buat voting baru
  {BOLD}vote list{RESET}        → Lihat daftar voting
  {BOLD}vote cast{RESET}        → Berikan suara
  {BOLD}vote result{RESET}      → Lihat hasil
  {BOLD}vote verify{RESET}      → Verifikasi semua vote
  {BOLD}vote delete{RESET}      → Hapus voting (creator)
  {BOLD}vote help{RESET}        → Bantuan
{'─' * 55}
  Operator: {get_id_badge()}
{'─' * 55}
""")

def list_polls_cmd():
    """List polls sederhana"""
    polls = list_polls()
    
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  🗳️  DAFTAR VOTING — ZUHRI VOTE                                ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
    
    if not polls:
        print(f"{YELLOW}Belum ada voting.{RESET}\n")
        return
    
    for i, p in enumerate(polls, 1):
        poll = json.load(open(os.path.join(POLLS_DIR, f"{p}.json")))
        
        # Hitung vote
        poll_votes_dir = os.path.join(VOTES_DIR, p)
        vote_count = 0
        if os.path.exists(poll_votes_dir):
            vote_count = len([f for f in os.listdir(poll_votes_dir) if f.endswith('.json')])
        
        print(f"  {GOLD}{i}.{RESET} {BOLD}{poll['question']}{RESET}")
        print(f"     {DIM}ID: {p}")
        print(f"     👤 {poll['creator']['name']} | 🗳️  {vote_count} suara | 📅 {poll['created'][:19]}{RESET}")
        print(f"     📋 Pilihan: {', '.join(poll['options'])}")
        print()

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "create":
        create_poll()
    elif cmd == "list":
        list_polls_cmd()
    elif cmd == "cast":
        do_vote()
    elif cmd == "result":
        show_results()
    elif cmd == "verify":
        verify_votes()
    elif cmd == "delete":
        delete_vote()
    elif cmd == "help":
        show_help()
    else:
        show_help()
