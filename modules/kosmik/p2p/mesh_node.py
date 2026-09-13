#!/data/data/com.termux/files/usr/bin/python
"""ZUHRI P2P-MESH — Jaringan Darurat Offline"""
import json, time, random, os, sys
from datetime import datetime
try:
    from p2pnetwork.node import Node
except ImportError:
    print("Install: pip install p2pnetwork"); sys.exit(1)

HOST='0.0.0.0'
PORT=8000+random.randint(1,200)
HOME=os.path.expanduser("~")
ID_FILE=os.path.join(HOME,"zuhri_os","id","identity.json")

if os.path.exists(ID_FILE):
    NODE_NAME = json.load(open(ID_FILE))['name']
else:
    NODE_NAME = input("🔑 Nama node: ") or "Anonymous"

print(f"\n╔══════════════════════════════════════╗")
print(f"║  📡 P2P-MESH — {NODE_NAME}")
print(f"║  Port: {PORT}")
print(f"║  Status: 🟢 ONLINE")
print(f"╚══════════════════════════════════════╝\n")

class MeshNode(Node):
    def __init__(self,name,host,port):
        super().__init__(host,port)
        self.name=name; self.peers=[]
    def on_node_message(self,node,data):
        try:
            m=json.loads(data)
            print(f"\n📨 [{m.get('time','?')}] {m.get('from','?')}: {m.get('text','')}")
        except Exception as e: print(f"⚠️ {e}")
    def send_message(self,text,mt='chat'):
        m={'from':self.name,'text':text,'time':datetime.now().strftime('%H:%M:%S'),'type':mt}
        self.send_to_nodes(json.dumps(m))
        print(f"📤 Terkirim ke {len(self.peers)} node")
    def on_node_connected(self,node):
        self.peers.append(node); print(f"\n🔗 Terhubung: {node.id}")
    def on_node_disconnected(self,node):
        if node in self.peers: self.peers.remove(node)
        print(f"\n🔌 Terputus: {node.id}")

node=MeshNode(NODE_NAME,HOST,PORT)
import threading
def start():
    try:
        node.start(); print(f"✅ Node port {PORT}\n")
    except Exception as e: print(f"❌ {e}")
threading.Thread(target=start,daemon=True).start()
time.sleep(2)

while True:
    try:
        c=input("📡 > ").strip()
        if not c: continue
        if c=="/exit": node.stop(); break
        elif c=="/peers":
            print(f"\n📋 Node: {len(node.peers)}")
            for p in node.peers: print(f"  • {p.id}")
        elif c.startswith("/connect "):
            ip=c.split()[1]
            try: node.connect_with_node(ip,PORT); print(f"🔗 Ke {ip}:{PORT}")
            except Exception as e: print(f"❌ {e}")
        elif c.startswith("/msg "): node.send_message(c[5:])
        elif c=="/sos": node.send_message("SOS!",'sos')
        else: print("Commands: /connect /msg /sos /peers /exit")
    except KeyboardInterrupt: node.stop(); break
