#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI FINANCE FULL — KEMANDIRIAN FINANSIAL
Sistem Keuangan Pribadi Lengkap
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, secrets, csv
from datetime import datetime, timedelta

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
FIN_DIR = os.path.join(HOME, "zuhri_os", "finance", "data")
os.makedirs(FIN_DIR, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

# ============================================================
# UTIL
# ============================================================
def get_id_badge():
    if not ZUHRI_ID_OK: return f"{YELLOW}⚠️  TANPA ID{RESET}"
    i = load_identity()
    return f"{GREEN}✅ {i['name']}{RESET}" if i else f"{YELLOW}⚠️{RESET}"

def fpath():
    if not ZUHRI_ID_OK: return None
    i = load_identity()
    if not i: return None
    return os.path.join(FIN_DIR, f"{i['zuhri_id']}.json")

def load_data():
    f = fpath()
    if f and os.path.exists(f):
        return json.load(open(f))
    return {
        "accounts": {"kas": {"nama":"Kas","saldo":0},"bank": {"nama":"Bank","saldo":0},"ewallet": {"nama":"E-Wallet","saldo":0}},
        "transactions": [],
        "budgets": {},
        "goals": [],
        "categories": ["makanan","transport","belanja","tagihan","gaji","bonus","lainnya"],
        "debts": [],
        "assets": []
    }

def save_data(d):
    f = fpath()
    if f: json.dump(d, open(f, "w"), indent=2)

def rp(n):
    return f"Rp {n:,.0f}".replace(",", ".")

def clear(): os.system('clear')

# ============================================================
# TRANSAKSI
# ============================================================
def tambah_transaksi():
    d = load_data()
    clear()
    print(f"\n{BOLD}{CYAN}💰 TAMBAH TRANSAKSI{RESET}\n")
    print(f"  {GOLD}1.{RESET} Pemasukan")
    print(f"  {GOLD}2.{RESET} Pengeluaran")
    print(f"  {GOLD}3.{RESET} Transfer antar akun\n")
    
    t = input(f"{CYAN}Pilih (1/2/3): {RESET}").strip()
    
    if t == "3":
        transfer(d); return
    
    if t not in ["1","2"]: return
    
    # Akun
    print(f"\n{BOLD}Akun:{RESET}")
    accounts = list(d['accounts'].keys())
    for i, a in enumerate(accounts, 1):
        print(f"  {GOLD}{i}.{RESET} {d['accounts'][a]['nama']} ({rp(d['accounts'][a]['saldo'])})")
    
    try:
        a_idx = int(input(f"\n{CYAN}Pilih akun: {RESET}")) - 1
        acc = accounts[a_idx]
    except: return
    
    try:
        amount = float(input("💰 Jumlah (Rp): ").strip().replace(".","").replace(",",""))
    except: 
        print(f"{RED}❌ Jumlah tidak valid{RESET}")
        input(f"{DIM}Enter...{RESET}"); return
    
    cat = input("📂 Kategori: ").strip() or "lainnya"
    note = input("📝 Catatan: ").strip()
    
    trans = {
        "id": secrets.token_hex(4),
        "type": "income" if t == "1" else "expense",
        "amount": amount,
        "category": cat,
        "note": note,
        "account": acc,
        "date": datetime.now().isoformat()
    }
    
    d['transactions'].append(trans)
    
    # Update saldo
    if t == "1":
        d['accounts'][acc]['saldo'] += amount
    else:
        d['accounts'][acc]['saldo'] -= amount
    
    save_data(d)
    if ZUHRI_ID_OK:
        log_verified(f"FINANCE: {'+' if t=='1' else '-'}{rp(amount)}")
    
    color = GREEN if t == "1" else RED
    sign = "+" if t == "1" else "-"
    print(f"\n{color}✅ {sign}{rp(amount)} di {d['accounts'][acc]['nama']}{RESET}")
    print(f"   Saldo: {rp(d['accounts'][acc]['saldo'])}\n")
    input(f"{DIM}Enter...{RESET}")

def transfer(d):
    clear()
    print(f"\n{BOLD}{CYAN}🔄 TRANSFER ANTAR AKUN{RESET}\n")
    accounts = list(d['accounts'].keys())
    for i, a in enumerate(accounts, 1):
        print(f"  {GOLD}{i}.{RESET} {d['accounts'][a]['nama']} ({rp(d['accounts'][a]['saldo'])})")
    
    try:
        src = int(input(f"\n{CYAN}Dari akun: {RESET}")) - 1
        dst = int(input(f"{CYAN}Ke akun: {RESET}")) - 1
        amount = float(input("💰 Jumlah: ").strip().replace(".","").replace(",",""))
    except: return
    
    if src == dst: return
    
    src_a = accounts[src]
    dst_a = accounts[dst]
    
    d['accounts'][src_a]['saldo'] -= amount
    d['accounts'][dst_a]['saldo'] += amount
    
    d['transactions'].append({
        "id": secrets.token_hex(4),
        "type": "transfer",
        "amount": amount,
        "from": src_a,
        "to": dst_a,
        "date": datetime.now().isoformat()
    })
    
    save_data(d)
    print(f"\n{GREEN}✅ Transfer {rp(amount)}{RESET}")
    print(f"   {d['accounts'][src_a]['nama']} → {d['accounts'][dst_a]['nama']}\n")
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# LAPORAN
# ============================================================
def laporan():
    d = load_data()
    clear()
    
    print(f"\n{BOLD}{CYAN}📊 LAPORAN KEUANGAN{RESET}\n")
    print(f"  {GOLD}1.{RESET} Hari ini")
    print(f"  {GOLD}2.{RESET} Bulan ini")
    print(f"  {GOLD}3.{RESET} Tahun ini")
    print(f"  {GOLD}4.{RESET} Semua")
    
    p = input(f"\n{CYAN}Pilih: {RESET}").strip()
    
    now = datetime.now()
    trans = d['transactions']
    
    if p == "1":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        label = f"Hari ini ({now.strftime('%d/%m/%Y')})"
        trans = [t for t in trans if 'date' in t and datetime.fromisoformat(t['date']) >= start]
    elif p == "2":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        label = f"Bulan ini ({now.strftime('%B %Y')})"
        trans = [t for t in trans if 'date' in t and datetime.fromisoformat(t['date']) >= start]
    elif p == "3":
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        label = f"Tahun ini ({now.year})"
        trans = [t for t in trans if 'date' in t and datetime.fromisoformat(t['date']) >= start]
    else:
        label = "Semua"
    
    income = sum(t['amount'] for t in trans if t.get('type') == 'income')
    expense = sum(t['amount'] for t in trans if t.get('type') == 'expense')
    balance = income - expense
    
    # Kategori
    cats = {}
    for t in trans:
        if t.get('type') == 'expense':
            c = t.get('category', 'lainnya')
            cats[c] = cats.get(c, 0) + t['amount']
    
    clear()
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  📊 LAPORAN — {label}
║  Operator: {get_id_badge()}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}💰 RINGKASAN:{RESET}
  Pemasukan    : {GREEN}{rp(income)}{RESET}
  Pengeluaran  : {RED}{rp(expense)}{RESET}
  {'─' * 50}
  Saldo        : {GREEN if balance >= 0 else RED}{rp(balance)}{RESET}
  Transaksi    : {len(trans)}

{BOLD}💼 SALDO AKUN:{RESET}""")
    
    total_saldo = 0
    for a, info in d['accounts'].items():
        print(f"  {info['nama']:15} {GOLD}{rp(info['saldo'])}{RESET}")
        total_saldo += info['saldo']
    print(f"  {'─' * 50}")
    print(f"  {'TOTAL':15} {BOLD}{GOLD}{rp(total_saldo)}{RESET}\n")
    
    print(f"{BOLD}📂 PENGELUARAN PER KATEGORI:{RESET}")
    if cats:
        for c, amount in sorted(cats.items(), key=lambda x: x[1], reverse=True):
            pct = amount / expense * 100 if expense else 0
            bar_len = int(pct / 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            print(f"  {c:15} {rp(amount):>15} ({pct:5.1f}%) {CYAN}{bar}{RESET}")
    else:
        print(f"  {DIM}(Belum ada pengeluaran){RESET}")
    
    # Transaksi terakhir
    print(f"\n{BOLD}📅 TRANSAKSI TERAKHIR:{RESET}")
    for t in trans[-10:]:
        if t.get('type') == 'transfer':
            date = datetime.fromisoformat(t['date']).strftime("%d/%m %H:%M")
            print(f"  {DIM}{date}{RESET} 🔄 Transfer {rp(t['amount'])}")
        else:
            date = datetime.fromisoformat(t['date']).strftime("%d/%m %H:%M")
            color = GREEN if t['type'] == 'income' else RED
            sign = "+" if t['type'] == 'income' else "-"
            cat = t.get('category', '-')
            print(f"  {DIM}{date}{RESET} {color}{sign} {rp(t['amount']):>15}{RESET}  {cat}")
    
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# BUDGET
# ============================================================
def menu_budget():
    d = load_data()
    clear()
    print(f"\n{BOLD}{CYAN}📅 BUDGET{RESET}\n")
    print(f"  {GOLD}1.{RESET} Atur budget")
    print(f"  {GOLD}2.{RESET} Lihat budget")
    print(f"  {GOLD}3.{RESET} Hapus budget")
    
    p = input(f"\n{CYAN}Pilih: {RESET}").strip()
    
    if p == "1":
        cat = input("📂 Kategori: ").strip() or "umum"
        try:
            amount = float(input("💰 Budget (Rp): ").strip().replace(".","").replace(",",""))
            d['budgets'][cat] = amount
            save_data(d)
            print(f"\n{GREEN}✅ Budget '{cat}': {rp(amount)}/bulan{RESET}\n")
        except: pass
    elif p == "2":
        if not d['budgets']:
            print(f"\n{YELLOW}Belum ada budget.{RESET}\n"); input(f"{DIM}Enter...{RESET}"); return
        
        now = datetime.now()
        month_trans = [t for t in d['transactions'] 
                      if t.get('type') == 'expense' and 'date' in t
                      and datetime.fromisoformat(t['date']).month == now.month
                      and datetime.fromisoformat(t['date']).year == now.year]
        
        print(f"\n{BOLD}📅 BUDGET — {now.strftime('%B %Y')}{RESET}\n")
        for cat, budget in d['budgets'].items():
            spent = sum(t['amount'] for t in month_trans if t.get('category') == cat)
            pct = spent / budget * 100 if budget else 0
            color = GREEN if pct < 70 else (YELLOW if pct < 100 else RED)
            bar_len = int(min(pct, 100) / 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            status = "✅" if pct < 100 else "❌"
            print(f"  {status} {cat:15} {rp(spent):>15} / {rp(budget):>15}")
            print(f"     {color}{bar}{RESET} {pct:.0f}%")
    elif p == "3":
        if not d['budgets']: return
        cats = list(d['budgets'].keys())
        for i, c in enumerate(cats, 1):
            print(f"  {GOLD}{i}.{RESET} {c}")
        try:
            idx = int(input(f"\n{CYAN}Hapus: {RESET}")) - 1
            del d['budgets'][cats[idx]]
            save_data(d)
            print(f"\n{GREEN}✅ Dihapus{RESET}\n")
        except: pass
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# TARGET
# ============================================================
def menu_goals():
    d = load_data()
    clear()
    print(f"\n{BOLD}{CYAN}🎯 TARGET FINANSIAL{RESET}\n")
    print(f"  {GOLD}1.{RESET} Tambah target")
    print(f"  {GOLD}2.{RESET} Lihat target")
    print(f"  {GOLD}3.{RESET} Tabung ke target")
    
    p = input(f"\n{CYAN}Pilih: {RESET}").strip()
    
    if p == "1":
        name = input("🎯 Nama: ").strip()
        try:
            target = float(input("💰 Target: ").strip().replace(".","").replace(",",""))
            deadline = input("📅 Deadline (YYYY-MM-DD, opsional): ").strip()
            d['goals'].append({
                "id": secrets.token_hex(4),
                "name": name, "target": target, "saved": 0,
                "deadline": deadline or None,
                "created": datetime.now().isoformat()
            })
            save_data(d)
            print(f"\n{GREEN}✅ Target '{name}': {rp(target)}{RESET}\n")
        except: pass
    elif p == "2":
        if not d['goals']:
            print(f"\n{YELLOW}Belum ada target.{RESET}\n"); input(f"{DIM}Enter...{RESET}"); return
        print()
        for g in d['goals']:
            pct = g['saved'] / g['target'] * 100 if g['target'] else 0
            bar_len = int(min(pct, 100) / 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            print(f"  {GOLD}🎯 {g['name']}{RESET}")
            print(f"     {rp(g['saved'])} / {rp(g['target'])} ({pct:.0f}%)")
            print(f"     {CYAN}{bar}{RESET}\n")
    elif p == "3":
        if not d['goals']: return
        for i, g in enumerate(d['goals'], 1):
            print(f"  {GOLD}{i}.{RESET} {g['name']} ({rp(g['saved'])}/{rp(g['target'])})")
        try:
            idx = int(input(f"\n{CYAN}Pilih: {RESET}")) - 1
            amount = float(input("💰 Tabung: ").strip().replace(".","").replace(",",""))
            d['goals'][idx]['saved'] += amount
            save_data(d)
            g = d['goals'][idx]
            print(f"\n{GREEN}✅ Tabung {rp(amount)} → {g['name']}{RESET}")
            print(f"   Progress: {(g['saved']/g['target']*100):.1f}%\n")
        except: pass
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# HUTANG & ASET
# ============================================================
def menu_debts_assets():
    d = load_data()
    clear()
    print(f"\n{BOLD}{CYAN}💳 HUTANG & ASET{RESET}\n")
    print(f"  {GOLD}1.{RESET} Tambah hutang")
    print(f"  {GOLD}2.{RESET} Tambah aset")
    print(f"  {GOLD}3.{RESET} Lihat semua")
    
    p = input(f"\n{CYAN}Pilih: {RESET}").strip()
    
    if p == "1":
        name = input("👤 Nama: ").strip()
        try:
            amount = float(input("💰 Jumlah: ").strip().replace(".","").replace(",",""))
            tipe = input("📝 Tipe (hutang/piutang): ").strip() or "hutang"
            d['debts'].append({"nama":name,"amount":amount,"tipe":tipe,"date":datetime.now().isoformat()})
            save_data(d)
            print(f"\n{GREEN}✅ Ditambahkan{RESET}\n")
        except: pass
    elif p == "2":
        name = input("🏠 Nama aset: ").strip()
        try:
            amount = float(input("💰 Nilai: ").strip().replace(".","").replace(",",""))
            d['assets'].append({"nama":name,"nilai":amount,"date":datetime.now().isoformat()})
            save_data(d)
            print(f"\n{GREEN}✅ Ditambahkan{RESET}\n")
        except: pass
    elif p == "3":
        print(f"\n{BOLD}💳 HUTANG & PIUTANG:{RESET}")
        if d['debts']:
            for x in d['debts']:
                color = RED if x['tipe'] == 'hutang' else GREEN
                print(f"  {color}•{RESET} {x['nama']}: {rp(x['amount'])} ({x['tipe']})")
        else:
            print(f"  {DIM}(kosong){RESET}")
        
        print(f"\n{BOLD}🏠 ASET:{RESET}")
        total = 0
        if d['assets']:
            for x in d['assets']:
                print(f"  • {x['nama']}: {rp(x['nilai'])}")
                total += x['nilai']
            print(f"  {GOLD}Total: {rp(total)}{RESET}")
        else:
            print(f"  {DIM}(kosong){RESET}")
    
    input(f"\n{DIM}Enter...{RESET}")

# ============================================================
# EXPORT
# ============================================================
def export_data():
    d = load_data()
    clear()
    print(f"\n{BOLD}{CYAN}📤 EXPORT DATA{RESET}\n")
    print(f"  {GOLD}1.{RESET} Export CSV")
    print(f"  {GOLD}2.{RESET} Export JSON")
    
    p = input(f"\n{CYAN}Pilih: {RESET}").strip()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if p == "1":
        f = os.path.join(FIN_DIR, f"export_{ts}.csv")
        with open(f, "w", newline='') as fp:
            w = csv.writer(fp)
            w.writerow(["Tanggal","Tipe","Kategori","Jumlah","Catatan","Akun"])
            for t in d['transactions']:
                w.writerow([
                    t.get('date','')[:19],
                    t.get('type',''),
                    t.get('category',''),
                    t.get('amount',0),
                    t.get('note',''),
                    t.get('account','')
                ])
        print(f"\n{GREEN}✅ CSV: {f}{RESET}\n")
    elif p == "2":
        f = os.path.join(FIN_DIR, f"export_{ts}.json")
        json.dump(d, open(f, "w"), indent=2)
        print(f"\n{GREEN}✅ JSON: {f}{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# CRYPTO TRACKER
# ============================================================
def crypto_tracker():
    import subprocess
    clear()
    print(f"\n{BOLD}{CYAN}🪙 CRYPTO TRACKER{RESET}\n")
    try:
        r = subprocess.run(["curl","-s","https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin&vs_currencies=usd,idr"],
                          capture_output=True, text=True, timeout=15)
        data = json.loads(r.stdout)
        print(f"{BOLD}{'Coin':12} {'USD':>15} {'IDR':>20}{RESET}")
        print(f"{DIM}{'─' * 50}{RESET}")
        for c, p in data.items():
            print(f"{GOLD}{c.upper():12}{RESET} ${p.get('usd',0):>13,.2f} Rp{p.get('idr',0):>18,.0f}")
    except:
        print(f"{RED}❌ Gagal ambil harga. Cek internet.{RESET}")
    print()
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        clear()
        d = load_data()
        total = sum(a['saldo'] for a in d['accounts'].values())
        
        print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║  💰 ZUHRI FINANCE FULL — KEMANDIRIAN FINANSIAL                 ║
║  ──────────────────────────────────────────────────────────────  ║
║  Operator: {get_id_badge()}
║  Total Saldo: {GOLD}{rp(total)}{RESET}
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  💰 Tambah Transaksi
  {GOLD}2.{RESET}  📊 Laporan
  {GOLD}3.{RESET}  📅 Budget
  {GOLD}4.{RESET}  🎯 Target
  {GOLD}5.{RESET}  💳 Hutang & Aset
  {GOLD}6.{RESET}  🪙 Crypto Tracker
  {GOLD}7.{RESET}  📤 Export Data
  {GOLD}8.{RESET}  💼 Lihat Akun
  {GOLD}0.{RESET}  Keluar
""")
        
        try:
            c = input(f"{GOLD}Pilih (0-8): {RESET}").strip()
            if c == "0": break
            elif c == "1": tambah_transaksi()
            elif c == "2": laporan()
            elif c == "3": menu_budget()
            elif c == "4": menu_goals()
            elif c == "5": menu_debts_assets()
            elif c == "6": crypto_tracker()
            elif c == "7": export_data()
            elif c == "8":
                clear()
                print(f"\n{BOLD}💼 DAFTAR AKUN{RESET}\n")
                for a, info in d['accounts'].items():
                    print(f"  {GOLD}•{RESET} {info['nama']:15} {rp(info['saldo'])}")
                print(f"\n  {BOLD}Total: {rp(total)}{RESET}\n")
                input(f"{DIM}Enter...{RESET}")
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "laporan": laporan()
        elif cmd == "crypto": crypto_tracker()
        elif cmd == "help":
            print("""
💰 ZUHRI FINANCE FULL
  finance         → Menu interaktif
  finance laporan → Laporan
  finance crypto  → Harga crypto
""")
        else: menu()
    else: menu()
