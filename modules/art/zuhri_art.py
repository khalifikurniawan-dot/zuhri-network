#!/data/data/com.termux/files/usr/bin/python
"""
ZUHRI ART — KREATIVITAS DIGITAL
AI Image + Music + Video + ASCII Art
Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0
"""

import os, sys, json, secrets, subprocess, random, math
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zuhri_os/id"))
try:
    from zuhri_auth import load_identity, log_verified
    ZUHRI_ID_OK = True
except ImportError:
    ZUHRI_ID_OK = False

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    PIL_OK = True
except ImportError:
    PIL_OK = False

import numpy as np

HOME = os.path.expanduser("~")
ART_DIR = os.path.join(HOME, "zuhri_os", "art")
DATA_DIR = os.path.join(ART_DIR, "data")
GALLERY_DIR = os.path.join(ART_DIR, "gallery")
MUSIC_DIR = os.path.join(ART_DIR, "music")
VIDEO_DIR = os.path.join(ART_DIR, "video")
for d in [DATA_DIR, GALLERY_DIR, MUSIC_DIR, VIDEO_DIR]:
    os.makedirs(d, exist_ok=True)

RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; GOLD="\033[93m"; MAGENTA="\033[95m"
BLUE="\033[94m"

def clear(): os.system('clear')

# ============================================================
# 1. GENERATIVE ART — Zuhri Formalism Pattern
# ============================================================
def generate_pattern():
    """Generate pattern art berbasis 0-8-9"""
    if not PIL_OK:
        print(f"{RED}❌ Pillow tidak terinstall{RESET}\n")
        return
    
    clear()
    print(f"{BOLD}{CYAN}🎨 GENERATIVE ART — ZUHRI FORMALISM{RESET}\n")
    
    width = int(input("Lebar (default 800): ").strip() or "800")
    height = int(input("Tinggi (default 800): ").strip() or "800")
    seed = input("Seed (angka, Enter=random): ").strip()
    
    if not seed:
        seed = random.randint(1, 99999)
    else:
        try:
            seed = int(seed)
        except:
            seed = 42
    
    random.seed(seed)
    np.random.seed(seed)
    
    print(f"\n{CYAN}🎨 Generate pattern...{RESET}")
    print(f"{DIM}Size: {width}x{height} | Seed: {seed}{RESET}\n")
    
    img = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Zuhri Formalism pattern
    for i in range(0, width, 10):
        for j in range(0, height, 10):
            # Hitung resonansi
            resonance = ((i * 8 + j * 9) % 10)
            
            if resonance >= 7:
                color = (255, 215, 0)  # Gold
            elif resonance >= 4:
                color = (0, 255, 255)  # Cyan
            else:
                color = (50, 50, 100)  # Dark blue
            
            # Draw shape
            if random.random() > 0.7:
                draw.ellipse([i, j, i+5, j+5], fill=color)
            elif random.random() > 0.5:
                draw.rectangle([i, j, i+4, j+4], fill=color)
            else:
                draw.point([i, j], fill=color)
    
    # Add circle center
    center_x, center_y = width // 2, height // 2
    for r in range(50, min(width, height)//2, 20):
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        draw.ellipse([center_x-r, center_y-r, center_x+r, center_y+r], outline=color, width=2)
    
    # Save
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(GALLERY_DIR, f"pattern_{seed}_{ts}.png")
    img.save(out)
    
    print(f"{GREEN}✅ Pattern tersimpan: {out}{RESET}\n")
    
    if ZUHRI_ID_OK:
        log_verified(f"ART_PATTERN: seed={seed}")
    
    # Buka
    try:
        subprocess.run(["termux-open", out], timeout=5)
    except:
        pass
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# 2. TEXT-TO-ART — ASCII & FIGlet
# ============================================================
def text_to_ascii():
    """Generate ASCII art dari teks"""
    clear()
    print(f"{BOLD}{CYAN}✍️  TEXT-TO-ASCII ART{RESET}\n")
    
    text = input("📝 Teks: ").strip()
    if not text:
        return
    
    print(f"\n{CYAN}Pilih font:{RESET}")
    print(f"  {GOLD}1.{RESET} Standard")
    print(f"  {GOLD}2.{RESET} Big")
    print(f"  {GOLD}3.{RESET} Block")
    print(f"  {GOLD}4.{RESET} Banner")
    print(f"  {GOLD}5.{RESET} Cosmic (figlet)")
    
    font_choice = input(f"\n{CYAN}Pilih (1-5): {RESET}").strip()
    
    font_map = {"1":"standard","2":"big","3":"block","4":"banner","5":"cosmic"}
    font = font_map.get(font_choice, "standard")
    
    print()
    
    # Coba figlet
    try:
        r = subprocess.run(["figlet", "-f", font, text], capture_output=True, text=True, timeout=5)
        if r.stdout:
            print(f"{GOLD}{r.stdout}{RESET}")
        else:
            # Fallback: manual ASCII
            print_ascii_manual(text)
    except:
        print_ascii_manual(text)
    
    if ZUHRI_ID_OK:
        log_verified(f"ART_ASCII: {text[:30]}")
    
    input(f"{DIM}Enter...{RESET}")

def print_ascii_manual(text):
    """ASCII art manual"""
    width = len(text) + 4
    print(f"{GOLD}")
    print("┌" + "─" * width + "┐")
    print("│ " + text + " │")
    print("└" + "─" * width + "┘")
    print(f"{RESET}")

# ============================================================
# 3. MUSIC GENERATOR — Tone & Melody
# ============================================================
def music_generator():
    """Generate musik sederhana"""
    clear()
    print(f"{BOLD}{CYAN}🎵 MUSIC GENERATOR{RESET}\n")
    
    print(f"  {GOLD}1.{RESET} Nada tunggal (tone)")
    print(f"  {GOLD}2.{RESET} Melodi acak")
    print(f"  {GOLD}3.{RESET} Chord progression")
    
    c = input(f"\n{CYAN}Pilih: {RESET}").strip()
    
    if c == "1":
        freq = input("Frekuensi (Hz, default 440): ").strip() or "440"
        duration = input("Durasi (detik, default 3): ").strip() or "3"
        generate_tone(float(freq), float(duration))
    elif c == "2":
        generate_melody()
    elif c == "3":
        generate_chord()
    
    input(f"{DIM}Enter...{RESET}")

def generate_tone(freq, duration=3):
    """Generate nada tunggal"""
    try:
        import wave
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        
        # Generate sine wave
        samples = []
        for i in range(n_samples):
            value = int(32767 * 0.3 * math.sin(2 * math.pi * freq * i / sample_rate))
            samples.append(value)
        
        # Save WAV
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = os.path.join(MUSIC_DIR, f"tone_{int(freq)}Hz_{ts}.wav")
        
        with wave.open(out, 'w') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sample_rate)
            
            import struct
            data = struct.pack('<' + 'h' * len(samples), *samples)
            w.writeframes(data)
        
        print(f"\n{GREEN}✅ Nada tersimpan: {out}{RESET}\n")
        
        if ZUHRI_ID_OK:
            log_verified(f"ART_TONE: {freq}Hz")
        
        try:
            subprocess.run(["termux-open", out], timeout=5)
        except:
            pass
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}\n")

def generate_melody():
    """Generate melodi acak"""
    # Nada dasar (C major scale)
    notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]
    note_names = ["C", "D", "E", "F", "G", "A", "B", "C5"]
    
    duration_per_note = 0.5
    melody_length = 10
    
    print(f"\n{CYAN}🎵 Generate melodi ({melody_length} nada)...{RESET}\n")
    
    try:
        import wave, struct
        sample_rate = 44100
        all_samples = []
        
        melodi = []
        for _ in range(melody_length):
            idx = random.randint(0, len(notes)-1)
            freq = notes[idx]
            melodi.append(note_names[idx])
            
            n_samples = int(sample_rate * duration_per_note)
            for i in range(n_samples):
                value = int(32767 * 0.3 * math.sin(2 * math.pi * freq * i / sample_rate))
                all_samples.append(value)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = os.path.join(MUSIC_DIR, f"melody_{ts}.wav")
        
        with wave.open(out, 'w') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sample_rate)
            data = struct.pack('<' + 'h' * len(all_samples), *all_samples)
            w.writeframes(data)
        
        print(f"{GREEN}✅ Melodi: {' '.join(melodi)}{RESET}")
        print(f"{GREEN}✅ Tersimpan: {out}{RESET}\n")
        
        if ZUHRI_ID_OK:
            log_verified("ART_MELODY")
        
        try:
            subprocess.run(["termux-open", out], timeout=5)
        except:
            pass
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}\n")

def generate_chord():
    """Generate chord progression"""
    chords = {
        "C": [261.63, 329.63, 392.00],
        "Dm": [293.66, 349.23, 440.00],
        "Em": [329.63, 392.00, 493.88],
        "F": [349.23, 440.00, 523.25],
        "G": [392.00, 493.88, 587.33],
        "Am": [440.00, 523.25, 659.25],
    }
    
    progression = random.sample(list(chords.keys()), 4)
    
    print(f"\n{CYAN}🎵 Chord progression: {' - '.join(progression)}{RESET}\n")
    
    try:
        import wave, struct
        sample_rate = 44100
        all_samples = []
        
        for chord_name in progression:
            freqs = chords[chord_name]
            duration = 1.0
            n_samples = int(sample_rate * duration)
            
            for i in range(n_samples):
                value = 0
                for freq in freqs:
                    value += int(32767 * 0.1 * math.sin(2 * math.pi * freq * i / sample_rate))
                all_samples.append(max(-32767, min(32767, value)))
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = os.path.join(MUSIC_DIR, f"chord_{ts}.wav")
        
        with wave.open(out, 'w') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sample_rate)
            data = struct.pack('<' + 'h' * len(all_samples), *all_samples)
            w.writeframes(data)
        
        print(f"{GREEN}✅ Tersimpan: {out}{RESET}\n")
        
        if ZUHRI_ID_OK:
            log_verified(f"ART_CHORD: {'-'.join(progression)}")
        
        try:
            subprocess.run(["termux-open", out], timeout=5)
        except:
            pass
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}\n")

# ============================================================
# 4. IMAGE FILTER — Menggunakan ImageMagick
# ============================================================
def image_filter():
    """Apply filter ke gambar"""
    clear()
    print(f"{BOLD}{CYAN}🖼️  IMAGE FILTER{RESET}\n")
    
    path = input("📂 Path gambar: ").strip()
    if not os.path.exists(path):
        print(f"{RED}❌ File tidak ada{RESET}\n")
        return
    
    print(f"\n{CYAN}Pilih filter:{RESET}")
    print(f"  {GOLD}1.{RESET} Grayscale")
    print(f"  {GOLD}2.{RESET} Sepia")
    print(f"  {GOLD}3.{RESET} Invert")
    print(f"  {GOLD}4.{RESET} Blur")
    print(f"  {GOLD}5.{RESET} Sharpen")
    print(f"  {GOLD}6.{RESET} Oil Paint")
    print(f"  {GOLD}7.{RESET} Charcoal")
    print(f"  {GOLD}8.{RESET} Posterize")
    
    choice = input(f"\n{CYAN}Pilih (1-8): {RESET}").strip()
    
    filters = {
        "1": "grayscale",
        "2": "sepia-tone 80%",
        "3": "negate",
        "4": "blur 0x8",
        "5": "sharpen 0x2",
        "6": "paint 4",
        "7": "charcoal 2",
        "8": "posterize 8",
    }
    
    filter_name = filters.get(choice, "grayscale")
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(GALLERY_DIR, f"filtered_{ts}.png")
    
    try:
        subprocess.run(
            ["convert", path, "-" + filter_name, out],
            timeout=30, capture_output=True
        )
        print(f"\n{GREEN}✅ Tersimpan: {out}{RESET}\n")
        
        if ZUHRI_ID_OK:
            log_verified(f"ART_FILTER: {filter_name}")
        
        try:
            subprocess.run(["termux-open", out], timeout=5)
        except:
            pass
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# 5. VIDEO TOOLS — Via ffmpeg
# ============================================================
def video_tools():
    """Tool video via ffmpeg"""
    clear()
    print(f"{BOLD}{CYAN}🎬 VIDEO TOOLS{RESET}\n")
    
    print(f"  {GOLD}1.{RESET} Extract audio dari video")
    print(f"  {GOLD}2.{RESET} Convert format")
    print(f"  {GOLD}3.{RESET} Trim video")
    print(f"  {GOLD}4.{RESET} Compress video")
    print(f"  {GOLD}5.{RESET} Extract frame")
    
    c = input(f"\n{CYAN}Pilih: {RESET}").strip()
    
    path = input("📂 Path video: ").strip()
    if not os.path.exists(path):
        print(f"{RED}❌ File tidak ada{RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        if c == "1":
            out = os.path.join(VIDEO_DIR, f"audio_{ts}.mp3")
            subprocess.run(["ffmpeg", "-i", path, "-vn", "-acodec", "libmp3lame", out, "-y"],
                          capture_output=True, timeout=120)
        elif c == "2":
            fmt = input("Format tujuan (mp4/avi/mkv): ").strip() or "mp4"
            out = os.path.join(VIDEO_DIR, f"converted_{ts}.{fmt}")
            subprocess.run(["ffmpeg", "-i", path, out, "-y"],
                          capture_output=True, timeout=300)
        elif c == "3":
            start = input("Start (HH:MM:SS): ").strip() or "00:00:00"
            end = input("End (HH:MM:SS): ").strip() or "00:00:30"
            out = os.path.join(VIDEO_DIR, f"trimmed_{ts}.mp4")
            subprocess.run(["ffmpeg", "-i", path, "-ss", start, "-to", end, "-c", "copy", out, "-y"],
                          capture_output=True, timeout=120)
        elif c == "4":
            out = os.path.join(VIDEO_DIR, f"compressed_{ts}.mp4")
            subprocess.run(["ffmpeg", "-i", path, "-vcodec", "libx264", "-crf", "28", out, "-y"],
                          capture_output=True, timeout=600)
        elif c == "5":
            time_pos = input("Timestamp (HH:MM:SS): ").strip() or "00:00:05"
            out = os.path.join(GALLERY_DIR, f"frame_{ts}.png")
            subprocess.run(["ffmpeg", "-i", path, "-ss", time_pos, "-vframes", "1", out, "-y"],
                          capture_output=True, timeout=60)
        
        if os.path.exists(out):
            print(f"\n{GREEN}✅ Tersimpan: {out}{RESET}\n")
            if ZUHRI_ID_OK:
                log_verified(f"ART_VIDEO: {c}")
            
            try:
                subprocess.run(["termux-open", out], timeout=5)
            except:
                pass
        else:
            print(f"{RED}❌ Gagal{RESET}\n")
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}\n")
    
    input(f"{DIM}Enter...{RESET}")

# ============================================================
# 6. GALLERY — Lihat Hasil
# ============================================================
def gallery():
    """Lihat galeri art"""
    clear()
    print(f"{BOLD}{CYAN}🖼️  GALERI ART{RESET}\n")
    
    files = []
    for d in [GALLERY_DIR, MUSIC_DIR, VIDEO_DIR]:
        if os.path.exists(d):
            for f in os.listdir(d):
                files.append((d, f))
    
    if not files:
        print(f"{YELLOW}Belum ada karya.${RESET}\n")
        input(f"{DIM}Enter...{RESET}")
        return
    
    print(f"{BOLD}Total: {len(files)} file{RESET}\n")
    
    for i, (d, f) in enumerate(files[-20:], 1):
        size = os.path.getsize(os.path.join(d, f)) / 1024
        print(f"  {GOLD}{i}.{RESET} {f} {DIM}({size:.1f} KB){RESET}")
    
    print()
    try:
        c = int(input(f"{CYAN}Buka nomor (0=keluar): {RESET}")) - 1
        if 0 <= c < len(files):
            d, f = files[-(20-c)] if len(files) > 20 else files[c]
            subprocess.run(["termux-open", os.path.join(d, f)])
    except:
        pass

# ============================================================
# MENU
# ============================================================
def menu():
    while True:
        clear()
        print(f"""
{BOLD}{MAGENTA}╔══════════════════════════════════════════════════════════════════════╗
║  🎨 ZUHRI ART — KREATIVITAS DIGITAL                                 ║
║  ──────────────────────────────────────────────────────────────────  ║
║  Protokol: K-8.0 | Gen: ZUH-8-9-0-K-8.0                            ║
║  Tool: Pillow + ImageMagick + ffmpeg + figlet                       ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}  📋 MENU:{RESET}
  {GOLD}1.{RESET}  🎨 Generative Art (Zuhri Formalism Pattern)
  {GOLD}2.{RESET}  ✍️  Text-to-ASCII Art
  {GOLD}3.{RESET}  🎵 Music Generator (Tone/Melody/Chord)
  {GOLD}4.{RESET}  🖼️  Image Filter (8 filter)
  {GOLD}5.{RESET}  🎬 Video Tools (ffmpeg)
  {GOLD}6.{RESET}  📂 Galeri Art
  {GOLD}0.{RESET}  Keluar
""")
        try:
            c = input(f"{GOLD}Pilih (0-6): {RESET}").strip()
            if c == "0": break
            elif c == "1": generate_pattern()
            elif c == "2": text_to_ascii()
            elif c == "3": music_generator()
            elif c == "4": image_filter()
            elif c == "5": video_tools()
            elif c == "6": gallery()
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "pattern": generate_pattern()
        elif cmd == "ascii":
            if len(sys.argv) > 2:
                text = " ".join(sys.argv[2:])
                try:
                    r = subprocess.run(["figlet", text], capture_output=True, text=True)
                    print(r.stdout)
                except:
                    print_ascii_manual(text)
        elif cmd == "music": music_generator()
        elif cmd == "gallery": gallery()
        else: menu()
    else: menu()
