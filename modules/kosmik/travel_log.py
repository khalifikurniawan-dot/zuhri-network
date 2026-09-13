#!/usr/bin/env python3
# Interdimensional Travel Log — Kosmik Key v8.0
# Mencatat setiap perjalanan antar dimensi

import json
import os
import time
import random
import hashlib
from datetime import datetime
from pathlib import Path
import uuid

class TravelLog:
    def __init__(self):
        self.logs_dir = Path.home() / "kosmik" / "logs"
        self.travel_file = self.logs_dir / "travel_log.json"
        self.travels = []
        self.current_travel = None
        
        # Buat direktori jika belum ada
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Load data jika ada
        self.load_travels()
        
        # Daftar dimensi yang diketahui
        self.known_dimensions = {
            'prime': {
                'name': 'Prime Universe',
                'description': 'Dimensi utama tempat kita berada',
                'stability': 1.0,
                'inhabitants': ['Human', 'Various species']
            },
            'alpha': {
                'name': 'Alpha Dimension',
                'description': 'Dimensi paralel dengan perbedaan kecil',
                'stability': 0.9,
                'inhabitants': ['Human variants', 'AI civilizations']
            },
            'beta': {
                'name': 'Beta Dimension',
                'description': 'Dimensi dengan teknologi maju',
                'stability': 0.85,
                'inhabitants': ['Techno-sapiens', 'Machine consciousness']
            },
            'gamma': {
                'name': 'Gamma Dimension',
                'description': 'Dimensi tempat Galactic Federation berkantor',
                'stability': 0.95,
                'inhabitants': ['Eldritch', 'Telepathic', 'Hive Mind', 'Crystalline', 'Plasma']
            },
            'delta': {
                'name': 'Delta Dimension',
                'description': 'Dimensi yang dikuasai Void',
                'stability': 0.3,
                'inhabitants': ['Void entities', 'Shadow beings']
            },
            'epsilon': {
                'name': 'Epsilon Dimension',
                'description': 'Dimensi gabungan semua dimensi',
                'stability': 0.7,
                'inhabitants': ['All species', 'Mixed entities']
            },
            'zeta': {
                'name': 'Zeta Dimension',
                'description': 'Dimensi kristal murni',
                'stability': 0.92,
                'inhabitants': ['Crystalline beings', 'Light entities']
            },
            'eta': {
                'name': 'Eta Dimension',
                'description': 'Dimensi waktu yang berbeda',
                'stability': 0.4,
                'inhabitants': ['Temporal beings', 'Time travelers']
            },
            'theta': {
                'name': 'Theta Dimension',
                'description': 'Dimensi kesadaran murni',
                'stability': 0.8,
                'inhabitants': ['Consciousness entities', 'Psychic beings']
            },
            'iota': {
                'name': 'Iota Dimension',
                'description': 'Dimensi baru yang belum dijelajahi',
                'stability': 0.5,
                'inhabitants': ['Unknown']
            }
        }

    def load_travels(self):
        """Load travel log dari file"""
        if self.travel_file.exists():
            try:
                with open(self.travel_file, 'r') as f:
                    data = json.load(f)
                    self.travels = data.get('travels', [])
            except:
                self.travels = []

    def save_travels(self):
        """Simpan travel log ke file"""
        data = {
            'last_updated': datetime.now().isoformat(),
            'total_travels': len(self.travels),
            'travels': self.travels
        }
        with open(self.travel_file, 'w') as f:
            json.dump(data, f, indent=2)

    def start_travel(self, origin, destination, method='portal'):
        """Mulai perjalanan interdimensional"""
        travel_id = str(uuid.uuid4())[:8]
        
        # Generate random travel signature
        signature = hashlib.md5(f"{travel_id}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        # Cek apakah dimensi dikenal
        origin_info = self.known_dimensions.get(origin, {'name': origin, 'description': 'Unknown dimension'})
        dest_info = self.known_dimensions.get(destination, {'name': destination, 'description': 'Unknown dimension'})
        
        self.current_travel = {
            'id': travel_id,
            'signature': signature,
            'origin': {
                'id': origin,
                'name': origin_info.get('name', origin),
                'description': origin_info.get('description', 'Unknown')
            },
            'destination': {
                'id': destination,
                'name': dest_info.get('name', destination),
                'description': dest_info.get('description', 'Unknown')
            },
            'method': method,
            'start_time': datetime.now().isoformat(),
            'status': 'in_progress',
            'events': [],
            'anomalies': [],
            'artifacts': []
        }
        
        print(f"\n🌀 STARTING TRAVEL: {origin} → {destination}")
        print(f"   🆔 ID: {travel_id}")
        print(f"   🔑 Signature: {signature}")
        print(f"   🚀 Method: {method}")
        print(f"   ⏰ Started: {self.current_travel['start_time']}")
        
        # Log event
        self.add_event('travel_started', f"Travel from {origin} to {destination} initiated")
        
        return self.current_travel

    def add_event(self, event_type, description, data=None):
        """Tambahkan event selama perjalanan"""
        if not self.current_travel:
            print("⚠️ No active travel. Start a travel first.")
            return
        
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'description': description,
            'data': data or {}
        }
        self.current_travel['events'].append(event)
        print(f"   📝 {event_type}: {description}")

    def record_anomaly(self, anomaly_type, description, severity='medium'):
        """Catat anomali selama perjalanan"""
        if not self.current_travel:
            print("⚠️ No active travel. Start a travel first.")
            return
        
        anomaly = {
            'timestamp': datetime.now().isoformat(),
            'type': anomaly_type,
            'description': description,
            'severity': severity
        }
        self.current_travel['anomalies'].append(anomaly)
        
        icons = {'low': '🟢', 'medium': '🟡', 'high': '🔴', 'critical': '💀'}
        print(f"   ⚠️ {icons.get(severity, '⚠️')} ANOMALY: {description}")

    def collect_artifact(self, name, description, origin_dimension):
        """Kumpulkan artifact dari dimensi"""
        if not self.current_travel:
            print("⚠️ No active travel. Start a travel first.")
            return
        
        artifact = {
            'timestamp': datetime.now().isoformat(),
            'id': str(uuid.uuid4())[:8],
            'name': name,
            'description': description,
            'origin': origin_dimension,
            'collected_from': self.current_travel['destination']['id']
        }
        self.current_travel['artifacts'].append(artifact)
        print(f"   📦 ARTIFACT COLLECTED: {name}")

    def end_travel(self, status='completed'):
        """Akhiri perjalanan interdimensional"""
        if not self.current_travel:
            print("⚠️ No active travel.")
            return
        
        self.current_travel['end_time'] = datetime.now().isoformat()
        self.current_travel['status'] = status
        self.current_travel['duration'] = self.calculate_duration()
        
        # Simpan ke log
        self.travels.append(self.current_travel)
        self.save_travels()
        
        print(f"\n✅ TRAVEL COMPLETED: {self.current_travel['id']}")
        print(f"   📊 Status: {status}")
        print(f"   ⏱️  Duration: {self.current_travel['duration']}")
        print(f"   📝 Events: {len(self.current_travel['events'])}")
        print(f"   ⚠️ Anomalies: {len(self.current_travel['anomalies'])}")
        print(f"   📦 Artifacts: {len(self.current_travel['artifacts'])}")
        
        travel = self.current_travel
        self.current_travel = None
        return travel

    def calculate_duration(self):
        """Hitung durasi perjalanan"""
        start = datetime.fromisoformat(self.current_travel['start_time'])
        end = datetime.fromisoformat(self.current_travel['end_time'])
        diff = end - start
        return str(diff)

    def get_travel_by_id(self, travel_id):
        """Cari travel berdasarkan ID"""
        for travel in self.travels:
            if travel['id'] == travel_id:
                return travel
        return None

    def get_travels_by_dimension(self, dimension):
        """Cari travel berdasarkan dimensi"""
        results = []
        for travel in self.travels:
            if travel['origin']['id'] == dimension or travel['destination']['id'] == dimension:
                results.append(travel)
        return results

    def get_all_travels(self):
        """Dapatkan semua travel"""
        return self.travels

    def get_statistics(self):
        """Statistik perjalanan"""
        stats = {
            'total_travels': len(self.travels),
            'unique_dimensions_visited': set(),
            'most_visited': {},
            'total_artifacts': 0,
            'total_anomalies': 0,
            'successful_travels': 0,
            'failed_travels': 0
        }
        
        for travel in self.travels:
            # Unique dimensions
            stats['unique_dimensions_visited'].add(travel['origin']['id'])
            stats['unique_dimensions_visited'].add(travel['destination']['id'])
            
            # Most visited
            dest = travel['destination']['id']
            stats['most_visited'][dest] = stats['most_visited'].get(dest, 0) + 1
            
            # Artifacts
            stats['total_artifacts'] += len(travel.get('artifacts', []))
            
            # Anomalies
            stats['total_anomalies'] += len(travel.get('anomalies', []))
            
            # Status
            if travel['status'] == 'completed':
                stats['successful_travels'] += 1
            else:
                stats['failed_travels'] += 1
        
        stats['unique_dimensions_visited'] = len(stats['unique_dimensions_visited'])
        
        return stats

    def display_travel(self, travel):
        """Tampilkan detail travel"""
        print("\n" + "="*70)
        print(f"🌀 TRAVEL: {travel['id']} — {travel['signature']}")
        print("="*70)
        print(f"   Origin: {travel['origin']['name']} ({travel['origin']['id']})")
        print(f"   Destination: {travel['destination']['name']} ({travel['destination']['id']})")
        print(f"   Method: {travel['method']}")
        print(f"   Status: {travel['status']}")
        print(f"   Duration: {travel.get('duration', 'In progress')}")
        print(f"   Started: {travel['start_time']}")
        if 'end_time' in travel:
            print(f"   Ended: {travel['end_time']}")
        
        if travel.get('events'):
            print(f"\n   📝 EVENTS ({len(travel['events'])}):")
            for event in travel['events'][-5:]:
                print(f"      • {event['type']}: {event['description']}")
            if len(travel['events']) > 5:
                print(f"      ... and {len(travel['events']) - 5} more")
        
        if travel.get('anomalies'):
            print(f"\n   ⚠️ ANOMALIES ({len(travel['anomalies'])}):")
            for anomaly in travel['anomalies']:
                icons = {'low': '🟢', 'medium': '🟡', 'high': '🔴', 'critical': '💀'}
                print(f"      {icons.get(anomaly['severity'], '⚠️')} {anomaly['type']}: {anomaly['description']}")
        
        if travel.get('artifacts'):
            print(f"\n   📦 ARTIFACTS ({len(travel['artifacts'])}):")
            for artifact in travel['artifacts']:
                print(f"      • {artifact['name']}: {artifact['description']}")
        
        print("="*70)

    def display_stats(self):
        """Tampilkan statistik perjalanan"""
        stats = self.get_statistics()
        print("\n" + "="*70)
        print("📊 INTERDIMENSIONAL TRAVEL STATISTICS")
        print("="*70)
        print(f"   🌀 Total Travels: {stats['total_travels']}")
        print(f"   🌌 Unique Dimensions: {stats['unique_dimensions_visited']}")
        print(f"   ✅ Successful: {stats['successful_travels']}")
        print(f"   ❌ Failed: {stats['failed_travels']}")
        print(f"   📦 Artifacts Collected: {stats['total_artifacts']}")
        print(f"   ⚠️ Anomalies Detected: {stats['total_anomalies']}")
        
        if stats['most_visited']:
            print(f"\n   🎯 MOST VISITED DIMENSIONS:")
            sorted_dims = sorted(stats['most_visited'].items(), key=lambda x: x[1], reverse=True)
            for dim, count in sorted_dims[:5]:
                dim_info = self.known_dimensions.get(dim, {'name': dim})
                print(f"      • {dim_info.get('name', dim)}: {count} times")
        
        print("="*70)

    def show_known_dimensions(self):
        """Tampilkan daftar dimensi yang dikenal"""
        print("\n" + "="*70)
        print("🌌 KNOWN DIMENSIONS")
        print("="*70)
        for dim_id, info in self.known_dimensions.items():
            stability_bar = "█" * int(info['stability'] * 10)
            print(f"\n   🌀 {info['name']} ({dim_id})")
            print(f"      {info['description']}")
            print(f"      Stability: {stability_bar} {info['stability']*100:.0f}%")
            print(f"      Inhabitants: {', '.join(info['inhabitants'])}")
        print("="*70)

    def interactive_mode(self):
        """Mode interaktif Travel Log"""
        print("\n" + "="*70)
        print("🌀 INTERDIMENSIONAL TRAVEL LOG — INTERACTIVE MODE")
        print("="*70)
        
        while True:
            print("\n📋 COMMANDS:")
            print("   [S] Start Travel")
            print("   [E] End Current Travel")
            print("   [A] Add Event")
            print("   [M] Record Anomaly")
            print("   [C] Collect Artifact")
            print("   [L] List All Travels")
            print("   [V] View Travel by ID")
            print("   [D] Show Known Dimensions")
            print("   [T] Show Statistics")
            print("   [X] Exit")
            
            choice = input("\n📱 Enter choice: ").strip().upper()
            
            if choice == 'S':
                print("\n📌 Available Dimensions:")
                for dim_id, info in self.known_dimensions.items():
                    print(f"   {dim_id}: {info['name']}")
                
                origin = input("Origin dimension: ").strip().lower()
                destination = input("Destination dimension: ").strip().lower()
                method = input("Travel method (portal/teleport/consciousness/wormhole): ").strip().lower()
                
                if origin in self.known_dimensions and destination in self.known_dimensions:
                    self.start_travel(origin, destination, method)
                else:
                    print("❌ Invalid dimension!")

            elif choice == 'E':
                if self.current_travel:
                    status = input("Status (completed/failed/aborted): ").strip().lower()
                    self.end_travel(status)
                else:
                    print("⚠️ No active travel.")

            elif choice == 'A':
                if self.current_travel:
                    event_type = input("Event type: ").strip()
                    description = input("Description: ").strip()
                    self.add_event(event_type, description)
                else:
                    print("⚠️ No active travel.")

            elif choice == 'M':
                if self.current_travel:
                    anomaly_type = input("Anomaly type: ").strip()
                    description = input("Description: ").strip()
                    severity = input("Severity (low/medium/high/critical): ").strip().lower()
                    self.record_anomaly(anomaly_type, description, severity)
                else:
                    print("⚠️ No active travel.")

            elif choice == 'C':
                if self.current_travel:
                    name = input("Artifact name: ").strip()
                    description = input("Description: ").strip()
                    origin_dim = input("Origin dimension: ").strip()
                    self.collect_artifact(name, description, origin_dim)
                else:
                    print("⚠️ No active travel.")

            elif choice == 'L':
                travels = self.get_all_travels()
                if travels:
                    print(f"\n📋 Total Travels: {len(travels)}")
                    for i, t in enumerate(travels[:10], 1):
                        print(f"   {i}. {t['id']} — {t['origin']['name']} → {t['destination']['name']} ({t['status']})")
                    if len(travels) > 10:
                        print(f"   ... and {len(travels) - 10} more")
                else:
                    print("⚠️ No travels recorded yet.")

            elif choice == 'V':
                travel_id = input("Enter travel ID: ").strip()
                travel = self.get_travel_by_id(travel_id)
                if travel:
                    self.display_travel(travel)
                else:
                    print("❌ Travel not found.")

            elif choice == 'D':
                self.show_known_dimensions()

            elif choice == 'T':
                self.display_stats()

            elif choice == 'X':
                print("👋 Exiting Interdimensional Travel Log...")
                break

            else:
                print("❌ Invalid command.")

if __name__ == "__main__":
    travel = TravelLog()
    
    # Test mode
    print("\n🧪 TEST MODE — Interdimensional Travel Log")
    print("="*70)
    
    # Test travel
    travel.start_travel('prime', 'gamma', 'portal')
    time.sleep(1)
    travel.add_event('dimensional_shift', 'Crossing dimensional barrier')
    time.sleep(0.5)
    travel.record_anomaly('temporal_glitch', 'Time fluctuation detected', 'medium')
    time.sleep(0.5)
    travel.collect_artifact('Crystal Shard', 'Shard from Crystalline dimension', 'gamma')
    travel.end_travel('completed')
    
    # Show statistics
    travel.display_stats()
    
    # Start interactive
    travel.interactive_mode()
