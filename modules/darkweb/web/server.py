#!/usr/bin/env python3
"""
ZUHRI DARK-WEB WEB SERVER
Server lokal untuk interface Dark-Web
"""

import http.server
import socketserver
import os
import subprocess
import threading
import time
import sys

HOME = os.path.expanduser("~")
WEB_DIR = os.path.join(HOME, "zuhri_os", "darkweb", "web")
PORT = 8080

os.chdir(WEB_DIR)

# Update IP Tor ke file
def update_ip_file():
    while True:
        try:
            ip = subprocess.run(
                ["torsocks", "curl", "-s", "--max-time", "5", "ifconfig.me"],
                capture_output=True, text=True, timeout=10
            ).stdout.strip()
            if ip and not ip.startswith("<"):
                with open("ip.txt", "w") as f:
                    f.write(ip)
        except:
            pass
        time.sleep(10)

# Start IP updater
threading.Thread(target=update_ip_file, daemon=True).start()

# Server
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"\n🌐 Zuhri Dark-Web Web Server")
    print(f"   Buka: http://localhost:{PORT}")
    print(f"   Atau: http://127.0.0.1:{PORT}")
    print(f"\n   Tekan CTRL+C untuk stop\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server dihentikan")
