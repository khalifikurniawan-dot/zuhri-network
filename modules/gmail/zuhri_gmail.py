#!/data/data/com.termux/files/usr/bin/python
"""ZUHRI GMAIL — EMAIL LOKAL"""
import os, sys, json, secrets
from datetime import datetime

R="\033[0m"; B="\033[1m"; D="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"

MAIL_DIR = os.path.expanduser("~/zuhri_os/gmail/data")
os.makedirs(MAIL_DIR, exist_ok=True)
def clear(): os.system('clear')

def kirim():
    clear()
    print(f"{B}{CYAN}📧 KIRIM EMAIL LOKAL{R}\n")
    ke = input("👤 Kepada: ").strip()
    subjek = input("📌 Subjek: ").strip()
    print("📝 Isi (ketik 'END' untuk selesai):")
    lines = []
    while True:
        l = input()
        if l == "END": break
        lines.append(l)
    email = {
        "id": secrets.token_hex(4),
        "from": "operator@zuhri.local",
        "to": ke, "subject": subjek,
        "body": "\n".join(lines),
        "date": datetime.now().isoformat()
    }
    f = os.path.join(MAIL_DIR, f"email_{email['id']}.json")
    json.dump(email, open(f, "w"), indent=2)
    print(f"\n{GREEN}✅ Email tersimpan!{R}\n")
    input(f"{D}Enter...{R}")

def inbox():
    clear()
    print(f"{B}{CYAN}📥 INBOX{R}\n")
    emails = sorted([f for f in os.listdir(MAIL_DIR) if f.endswith('.json')], reverse=True)
    if not emails:
        print(f"{YELLOW}Belum ada email.{R}\n")
        input(f"{D}Enter...{R}"); return
    for i, f in enumerate(emails[:20], 1):
        e = json.load(open(os.path.join(MAIL_DIR, f)))
        print(f"  {GOLD}{i}.{R} {e['subject'][:40]}")
        print(f"     {D}Dari: {e['from']} | {e['date'][:16]}{R}")
    print()
    try:
        c = int(input(f"{CYAN}Baca (0=keluar): {R}"))
        if c > 0 and c <= len(emails):
            e = json.load(open(os.path.join(MAIL_DIR, emails[c-1])))
            clear()
            print(f"\n{B}{CYAN}📧 EMAIL{R}")
            print(f"{'-'*60}")
            print(f"{D}Dari:{R}    {e['from']}")
            print(f"{D}Kepada:{R}  {e['to']}")
            print(f"{D}Subjek:{R}  {e['subject']}")
            print(f"{D}Tanggal:{R} {e['date'][:19]}")
            print(f"{'-'*60}\n{e['body']}\n{'-'*60}\n")
            input(f"{D}Enter...{R}")
    except: pass

def menu():
    while True:
        clear()
        print(f"""
{B}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  📧 ZUHRI GMAIL — EMAIL LOKAL                                       ║
╚══════════════════════════════════════════════════════════════════════╝{R}

{B}  📋 MENU:{R}
  {GOLD}1.{R}  ✉️  Kirim Email
  {GOLD}2.{R}  📥 Inbox
  {GOLD}0.{R}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih: {R}").strip()
            if c == "0": break
            elif c == "1": kirim()
            elif c == "2": inbox()
        except KeyboardInterrupt: break

if __name__ == "__main__":
    menu()
