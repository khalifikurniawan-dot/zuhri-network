#!/data/data/com.termux/files/usr/bin/python
"""ZUHRI EDU — PENDIDIKAN MANDIRI"""
import os, sys, json, secrets
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, sign, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

HOME = os.path.expanduser("~")
EDU_DIR = os.path.join(HOME, "zuhri_os", "edu")
COURSES_DIR = os.path.join(EDU_DIR, "courses")
PROGRESS_DIR = os.path.join(EDU_DIR, "progress")
CERTS_DIR = os.path.join(EDU_DIR, "certs")
for d in [COURSES_DIR, PROGRESS_DIR, CERTS_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"

DEFAULT_COURSES = {
    "python_dasar": {"title":"Python Dasar","category":"Programming","level":"Pemula","lessons":[
        {"id":1,"title":"Pengenalan Python","content":"Python adalah bahasa pemrograman tingkat tinggi. Sintaksnya sederhana dan mudah dipelajari."},
        {"id":2,"title":"Variabel & Tipe Data","content":"Variabel = wadah data. Tipe: int, float, str, bool."},
        {"id":3,"title":"Operator","content":"Aritmatika: + - * / // % **\nPerbandingan: == != > < >= <=\nLogika: and or not"},
        {"id":4,"title":"Kondisi If-Else","content":"if kondisi:\n    aksi\nelif lain:\n    aksi\nelse:\n    aksi"},
        {"id":5,"title":"Perulangan","content":"for i in range(5):\nwhile kondisi:"},
    ]},
    "linux_dasar": {"title":"Linux Dasar","category":"Sistem","level":"Pemula","lessons":[
        {"id":1,"title":"Pengenalan Linux","content":"Linux = OS open source. Termux = Linux untuk Android."},
        {"id":2,"title":"Perintah Dasar","content":"ls, cd, pwd, cp, mv, rm, mkdir, cat"},
        {"id":3,"title":"Permission","content":"chmod, chown, ls -la"},
        {"id":4,"title":"Package Manager","content":"pkg install, pkg update"},
    ]},
    "kriptografi_dasar": {"title":"Kriptografi Dasar","category":"Keamanan","level":"Menengah","lessons":[
        {"id":1,"title":"Pengenalan","content":"Kriptografi = seni menjaga kerahasiaan pesan."},
        {"id":2,"title":"Hash","content":"SHA-256 = sidik jari digital. One-way."},
        {"id":3,"title":"Simetris","content":"AES-256. Satu kunci."},
        {"id":4,"title":"Asimetris","content":"RSA, Ed25519. Public + Private key."},
        {"id":5,"title":"Tanda Tangan","content":"Verifikasi keaslian dengan private key."},
    ]},
}

def init_courses():
    if not os.listdir(COURSES_DIR):
        for k,v in DEFAULT_COURSES.items():
            json.dump(v, open(os.path.join(COURSES_DIR,f"{k}.json"),"w"), indent=2)

def list_courses():
    init_courses()
    courses = []
    for f in os.listdir(COURSES_DIR):
        if f.endswith('.json'):
            d = json.load(open(os.path.join(COURSES_DIR,f)))
            d['id'] = f[:-5]
            courses.append(d)
    return courses

def load_progress():
    if not ZUHRI_ID_OK: return {}
    i = load_identity()
    if not i: return {}
    f = os.path.join(PROGRESS_DIR,f"{i['zuhri_id']}.json")
    return json.load(open(f)) if os.path.exists(f) else {}

def save_progress(d):
    if not ZUHRI_ID_OK: return
    i = load_identity()
    if not i: return
    json.dump(d, open(os.path.join(PROGRESS_DIR,f"{i['zuhri_id']}.json"),"w"), indent=2)

def show_courses():
    courses = list_courses()
    print(f"\n{BOLD}{CYAN}📚 ZUHRI EDU — DAFTAR KURSUS{RESET}\n")
    for i,c in enumerate(courses,1):
        print(f"  {GOLD}{i}.{RESET} {BOLD}{c['title']}{RESET}")
        print(f"     {DIM}📂 {c['category']} | 🎯 {c['level']} | 📖 {len(c['lessons'])} pelajaran{RESET}")
    print()

def learn():
    courses = list_courses()
    if not courses: print("Belum ada kursus"); return
    show_courses()
    try:
        ch = int(input(f"{CYAN}Pilih: {RESET}"))-1
        if not (0<=ch<len(courses)): return
        c = courses[ch]
        prog = load_progress()
        cp = prog.get(c['id'],{"completed":[]})
        while True:
            os.system('clear')
            done = cp.get('completed',[])
            print(f"\n{BOLD}{CYAN}📖 {c['title']}{RESET}")
            print(f"{DIM}Progress: {len(done)}/{len(c['lessons'])}{RESET}\n")
            for l in c['lessons']:
                st = f"{GREEN}✅{RESET}" if l['id'] in done else f"{DIM}◯{RESET}"
                print(f"  {st} {GOLD}{l['id']}.{RESET} {l['title']}")
            print(f"\n  {DIM}0. Kembali{RESET}")
            try:
                lc = input(f"\n{CYAN}Pilih: {RESET}").strip()
                if lc == "0": break
                lid = int(lc)
                les = next((x for x in c['lessons'] if x['id']==lid),None)
                if les:
                    os.system('clear')
                    print(f"\n{BOLD}{CYAN}📖 {les['title']}{RESET}\n{les['content']}\n")
                    if lid not in done:
                        done.append(lid); cp['completed']=done; prog[c['id']]=cp; save_progress(prog)
                        print(f"{GREEN}✅ Selesai!{RESET}\n")
                    input(f"{DIM}Enter...{RESET}")
            except: pass
    except: pass

def ai_tutor():
    print(f"\n{BOLD}{CYAN}🧠 ZUHRI EDU — AI TUTOR{RESET}\n")
    print(f"{DIM}Ketik 'exit' untuk keluar{RESET}\n")
    while True:
        try:
            q = input(f"{GOLD}🎓 Anda: {RESET}").strip()
            if not q: continue
            if q.lower() in ["exit","quit","keluar"]: break
            print(f"{CYAN}🧠 Tutor: {RESET}",end="",flush=True)
            os.system(f'ollama run phi "Kamu guru sabar. Jawab Bahasa Indonesia singkat: {q}"')
            print()
        except KeyboardInterrupt: break

def certificate():
    courses = list_courses()
    if not courses: print("Belum ada kursus"); return
    show_courses()
    try:
        ch = int(input(f"{CYAN}Pilih: {RESET}"))-1
        if not (0<=ch<len(courses)): return
        c = courses[ch]
        prog = load_progress()
        done = prog.get(c['id'],{}).get('completed',[])
        if len(done) < len(c['lessons']):
            print(f"\n{YELLOW}⚠️  Belum selesai: {len(done)}/{len(c['lessons'])}{RESET}\n")
            return
        i = load_identity() if ZUHRI_ID_OK else None
        cert = {"certificate_id":"CERT-"+secrets.token_hex(8).upper(),
                "zuhri_id":i['zuhri_id'] if i else "ANON",
                "name":i['name'] if i else "Anonymous",
                "course":c['title'],"category":c['category'],"level":c['level'],
                "issued":datetime.now().isoformat(),"protocol":"K-8.0"}
        if ZUHRI_ID_OK and i:
            sig = sign(json.dumps({k:v for k,v in cert.items()},sort_keys=True))
            if sig:
                cert['signature']=sig; cert['public_key']=i['public_key']
        json.dump(cert, open(os.path.join(CERTS_DIR,f"{cert['certificate_id']}.json"),"w"), indent=2)
        log_verified(f"EDU_CERT: {cert['certificate_id']}")
        print(f"\n{BOLD}{GREEN}✅ SERTIFIKAT DIBUAT!{RESET}\n")
        print(f"  ID   : {cert['certificate_id']}")
        print(f"  Nama : {cert['name']}")
        print(f"  Kursus: {c['title']}\n")
    except: pass

def show_help():
    print(f"""
{BOLD}{CYAN}📚 ZUHRI EDU — BANTUAN{RESET}
{'─'*50}
  {BOLD}edu list{RESET}    → Daftar kursus
  {BOLD}edu learn{RESET}   → Mulai belajar
  {BOLD}edu ai{RESET}      → AI Tutor
  {BOLD}edu cert{RESET}    → Sertifikat
  {BOLD}edu help{RESET}    → Bantuan
{'─'*50}
""")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv)>1 else "menu"
    if cmd=="list": show_courses()
    elif cmd=="learn": learn()
    elif cmd=="ai": ai_tutor()
    elif cmd=="cert": certificate()
    elif cmd=="help": show_help()
    else:
        print(f"\n{BOLD}{CYAN}📚 ZUHRI EDU{RESET}\n")
        print("  1. Daftar Kursus")
        print("  2. Belajar")
        print("  3. AI Tutor")
        print("  4. Sertifikat")
        print("  0. Keluar\n")
        c = input(f"{GOLD}Pilih: {RESET}").strip()
        if c=="1": show_courses()
        elif c=="2": learn()
        elif c=="3": ai_tutor()
        elif c=="4": certificate()
