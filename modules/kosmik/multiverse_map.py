#!/usr/bin/env python3
# Multiverse Mapping System — Kosmik Key v8.0
# Peta Lengkap Multiverse + Hubungan Antar Dimensi

import json
import os
import time
import random
import math
from datetime import datetime
from pathlib import Path
import hashlib

class MultiverseMap:
    def __init__(self):
        self.map_dir = Path.home() / "kosmik" / "logs"
        self.map_file = self.map_dir / "multiverse_map.json"
        self.map_dir.mkdir(parents=True, exist_ok=True)
        
        # Inisialisasi peta multiverse
        self.multiverse = self.init_multiverse()
        self.connections = self.init_connections()
        self.routes = self.init_routes()
        self.anomalies = self.init_anomalies()
        self.timeline_branches = self.init_timeline_branches()
        
        # Load data jika ada
        self.load_map()
        
        # Update timestamp
        self.last_update = datetime.now().isoformat()

    def init_multiverse(self):
        """Inisialisasi semua dimensi di multiverse"""
        return {
            'prime': {
                'name': 'Prime Universe',
                'type': 'Core Reality',
                'coordinates': {'x': 0, 'y': 0, 'z': 0, 't': 0},
                'stability': 1.0,
                'inhabitants': ['Human', 'Various species'],
                'status': 'active',
                'color': '#00ffd5',
                'discovered': True,
                'accessible': True,
                'population': '8.2 billion',
                'technology_level': 'Delta',
                'description': 'Dimensi utama tempat kita berada'
            },
            'alpha': {
                'name': 'Alpha Dimension',
                'type': 'Parallel Reality',
                'coordinates': {'x': 1.5, 'y': 0.8, 'z': 0.3, 't': 0.1},
                'stability': 0.85,
                'inhabitants': ['Human variants', 'AI civilizations'],
                'status': 'active',
                'color': '#ff6b6b',
                'discovered': True,
                'accessible': True,
                'population': '12.5 billion',
                'technology_level': 'Beta+',
                'description': 'Dimensi paralel dengan perbedaan kecil'
            },
            'beta': {
                'name': 'Beta Dimension',
                'type': 'Technological Reality',
                'coordinates': {'x': 2.3, 'y': -1.2, 'z': 0.7, 't': 0.05},
                'stability': 0.92,
                'inhabitants': ['Techno-sapiens', 'Machine consciousness'],
                'status': 'active',
                'color': '#ffd93d',
                'discovered': True,
                'accessible': True,
                'population': '45.8 billion',
                'technology_level': 'Alpha',
                'description': 'Dimensi dengan teknologi maju'
            },
            'gamma': {
                'name': 'Gamma Dimension',
                'type': 'Federation Hub',
                'coordinates': {'x': 3.7, 'y': 2.1, 'z': -1.5, 't': 0.2},
                'stability': 0.98,
                'inhabitants': ['Eldritch', 'Telepathic', 'Hive Mind', 'Crystalline', 'Plasma'],
                'status': 'active',
                'color': '#6c5ce7',
                'discovered': True,
                'accessible': True,
                'population': 'Unknown',
                'technology_level': 'Omega',
                'description': 'Dimensi tempat Galactic Federation berkantor'
            },
            'delta': {
                'name': 'Delta Dimension',
                'type': 'Void Reality',
                'coordinates': {'x': -1.8, 'y': -0.5, 'z': -2.3, 't': -0.3},
                'stability': 0.15,
                'inhabitants': ['Void entities', 'Shadow beings'],
                'status': 'unstable',
                'color': '#2d3436',
                'discovered': True,
                'accessible': False,
                'population': 'Unknown',
                'technology_level': 'Unknown',
                'description': 'Dimensi yang dikuasai Void'
            },
            'epsilon': {
                'name': 'Epsilon Dimension',
                'type': 'Convergence Reality',
                'coordinates': {'x': 0.5, 'y': -2.8, 'z': 1.2, 't': 0.5},
                'stability': 0.65,
                'inhabitants': ['Mixed entities', 'All species'],
                'status': 'active',
                'color': '#fd79a8',
                'discovered': True,
                'accessible': True,
                'population': 'Unknown',
                'technology_level': 'Alpha+',
                'description': 'Dimensi gabungan semua dimensi'
            },
            'zeta': {
                'name': 'Zeta Dimension',
                'type': 'Crystalline Reality',
                'coordinates': {'x': 4.2, 'y': -3.1, 'z': 2.8, 't': -0.1},
                'stability': 0.95,
                'inhabitants': ['Crystalline beings', 'Light entities'],
                'status': 'active',
                'color': '#00b894',
                'discovered': True,
                'accessible': True,
                'population': '8.7 billion',
                'technology_level': 'Beta+',
                'description': 'Dimensi kristal murni'
            },
            'eta': {
                'name': 'Eta Dimension',
                'type': 'Temporal Reality',
                'coordinates': {'x': -2.3, 'y': 1.7, 'z': -0.8, 't': 2.5},
                'stability': 0.35,
                'inhabitants': ['Temporal beings', 'Time travelers'],
                'status': 'active',
                'color': '#e17055',
                'discovered': True,
                'accessible': False,
                'population': 'Unknown',
                'technology_level': 'Alpha',
                'description': 'Dimensi dengan waktu yang berbeda'
            },
            'theta': {
                'name': 'Theta Dimension',
                'type': 'Consciousness Reality',
                'coordinates': {'x': -3.5, 'y': -2.3, 'z': 0.5, 't': 0.3},
                'stability': 0.82,
                'inhabitants': ['Consciousness entities', 'Psychic beings'],
                'status': 'active',
                'color': '#a29bfe',
                'discovered': True,
                'accessible': True,
                'population': 'Unknown',
                'technology_level': 'Psi',
                'description': 'Dimensi kesadaran murni'
            },
            'iota': {
                'name': 'Iota Dimension',
                'type': 'Unknown Reality',
                'coordinates': {'x': 5.8, 'y': 3.2, 'z': -2.1, 't': -0.5},
                'stability': 0.45,
                'inhabitants': ['Unknown'],
                'status': 'exploring',
                'color': '#fab1a0',
                'discovered': True,
                'accessible': True,
                'population': 'Unknown',
                'technology_level': 'Unknown',
                'description': 'Dimensi baru yang belum dijelajahi'
            },
            'kappa': {
                'name': 'Kappa Dimension',
                'type': 'Hidden Reality',
                'coordinates': {'x': -4.5, 'y': 3.8, 'z': 1.5, 't': -0.2},
                'stability': 0.55,
                'inhabitants': ['Ancient beings', 'Watchers'],
                'status': 'hidden',
                'color': '#55efc4',
                'discovered': False,
                'accessible': False,
                'population': 'Unknown',
                'technology_level': 'Unknown',
                'description': 'Dimensi tersembunyi yang belum ditemukan'
            },
            'lambda': {
                'name': 'Lambda Dimension',
                'type': 'Quantum Reality',
                'coordinates': {'x': 6.2, 'y': -4.5, 'z': 3.8, 't': 1.2},
                'stability': 0.78,
                'inhabitants': ['Quantum entities', 'Probability beings'],
                'status': 'active',
                'color': '#74b9ff',
                'discovered': False,
                'accessible': False,
                'population': 'Unknown',
                'technology_level': 'Omega+',
                'description': 'Dimensi quantum murni'
            }
        }

    def init_connections(self):
        """Inisialisasi koneksi antar dimensi"""
        return [
            {'from': 'prime', 'to': 'alpha', 'strength': 0.85, 'type': 'portal', 'status': 'active'},
            {'from': 'prime', 'to': 'beta', 'strength': 0.75, 'type': 'portal', 'status': 'active'},
            {'from': 'prime', 'to': 'gamma', 'strength': 0.92, 'type': 'federation_gate', 'status': 'active'},
            {'from': 'prime', 'to': 'delta', 'strength': 0.15, 'type': 'void_breach', 'status': 'blocked'},
            {'from': 'prime', 'to': 'epsilon', 'strength': 0.65, 'type': 'convergence', 'status': 'active'},
            {'from': 'alpha', 'to': 'beta', 'strength': 0.70, 'type': 'portal', 'status': 'active'},
            {'from': 'alpha', 'to': 'zeta', 'strength': 0.60, 'type': 'portal', 'status': 'active'},
            {'from': 'beta', 'to': 'gamma', 'strength': 0.88, 'type': 'federation_gate', 'status': 'active'},
            {'from': 'beta', 'to': 'theta', 'strength': 0.55, 'type': 'consciousness', 'status': 'active'},
            {'from': 'gamma', 'to': 'zeta', 'strength': 0.90, 'type': 'crystalline_gate', 'status': 'active'},
            {'from': 'gamma', 'to': 'epsilon', 'strength': 0.80, 'type': 'federation_gate', 'status': 'active'},
            {'from': 'gamma', 'to': 'theta', 'strength': 0.85, 'type': 'psi_link', 'status': 'active'},
            {'from': 'delta', 'to': 'epsilon', 'strength': 0.30, 'type': 'void_leak', 'status': 'unstable'},
            {'from': 'eta', 'to': 'prime', 'strength': 0.25, 'type': 'temporal_rift', 'status': 'unstable'},
            {'from': 'epsilon', 'to': 'zeta', 'strength': 0.75, 'type': 'convergence', 'status': 'active'},
            {'from': 'theta', 'to': 'iota', 'strength': 0.50, 'type': 'consciousness', 'status': 'active'},
            {'from': 'iota', 'to': 'kappa', 'strength': 0.30, 'type': 'unknown', 'status': 'exploring'},
            {'from': 'kappa', 'to': 'lambda', 'strength': 0.20, 'type': 'hidden', 'status': 'undiscovered'}
        ]

    def init_routes(self):
        """Inisialisasi rute perjalanan yang diketahui"""
        return [
            {
                'name': 'Federation Highway',
                'path': ['prime', 'gamma', 'zeta', 'theta'],
                'type': 'safe',
                'length': 4,
                'description': 'Rute utama menuju Galactic Federation'
            },
            {
                'name': 'Crystalline Path',
                'path': ['prime', 'alpha', 'zeta'],
                'type': 'safe',
                'length': 3,
                'description': 'Rute menuju dimensi kristal'
            },
            {
                'name': 'Consciousness Bridge',
                'path': ['prime', 'beta', 'theta'],
                'type': 'safe',
                'length': 3,
                'description': 'Rute menuju dimensi kesadaran'
            },
            {
                'name': 'Void Caution',
                'path': ['prime', 'delta', 'epsilon'],
                'type': 'dangerous',
                'length': 3,
                'description': 'Rute berbahaya melalui Void'
            },
            {
                'name': 'Temporal Loop',
                'path': ['prime', 'eta'],
                'type': 'unstable',
                'length': 2,
                'description': 'Rute menuju dimensi temporal'
            },
            {
                'name': 'Explorer Path',
                'path': ['prime', 'iota', 'kappa', 'lambda'],
                'type': 'unknown',
                'length': 4,
                'description': 'Rute eksplorasi ke dimensi baru'
            }
        ]

    def init_anomalies(self):
        """Inisialisasi anomali di multiverse"""
        return [
            {
                'id': 'a001',
                'name': 'Temporal Rift',
                'location': 'eta',
                'severity': 'high',
                'status': 'active',
                'description': 'Celah temporal yang mengganggu aliran waktu'
            },
            {
                'id': 'a002',
                'name': 'Void Leak',
                'location': 'delta',
                'severity': 'critical',
                'status': 'active',
                'description': 'Kebocoran energi Void ke dimensi lain'
            },
            {
                'id': 'a003',
                'name': 'Consciousness Echo',
                'location': 'theta',
                'severity': 'medium',
                'status': 'active',
                'description': 'Gema kesadaran dari dimensi lain'
            },
            {
                'id': 'a004',
                'name': 'Crystalline Instability',
                'location': 'zeta',
                'severity': 'low',
                'status': 'monitoring',
                'description': 'Fluktuasi pada grid kristal'
            },
            {
                'id': 'a005',
                'name': 'Portal Collapse',
                'location': 'alpha',
                'severity': 'medium',
                'status': 'repairing',
                'description': 'Portal menuju beta mulai runtuh'
            }
        ]

    def init_timeline_branches(self):
        """Inisialisasi cabang timeline alternatif"""
        return {
            'prime': {
                'main': 'Sejarah utama',
                'branches': {
                    'alpha_timeline': 'Perbedaan kecil dalam sejarah',
                    'beta_timeline': 'Teknologi berkembang lebih cepat',
                    'gamma_timeline': 'Federation ditemukan lebih awal'
                }
            },
            'gamma': {
                'main': 'Federation history',
                'branches': {
                    'void_war': 'Perang melawan Void',
                    'crystalline_era': 'Era kristal damai',
                    'eldritch_awakening': 'Kebangkitan Ancient Ones'
                }
            },
            'delta': {
                'main': 'Void history',
                'branches': {
                    'void_victory': 'Void menang',
                    'void_contained': 'Void dikurung',
                    'void_merger': 'Void bergabung dengan Federation'
                }
            }
        }

    def load_map(self):
        """Load peta dari file jika ada"""
        if self.map_file.exists():
            try:
                with open(self.map_file, 'r') as f:
                    data = json.load(f)
                    self.multiverse = data.get('multiverse', self.multiverse)
                    self.connections = data.get('connections', self.connections)
                    self.routes = data.get('routes', self.routes)
                    self.anomalies = data.get('anomalies', self.anomalies)
                    self.timeline_branches = data.get('timeline_branches', self.timeline_branches)
                    self.last_update = data.get('last_update', datetime.now().isoformat())
            except:
                pass

    def save_map(self):
        """Simpan peta ke file"""
        data = {
            'last_update': datetime.now().isoformat(),
            'multiverse': self.multiverse,
            'connections': self.connections,
            'routes': self.routes,
            'anomalies': self.anomalies,
            'timeline_branches': self.timeline_branches
        }
        with open(self.map_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Map saved to {self.map_file}")

    def get_dimension(self, dim_id):
        """Dapatkan informasi dimensi"""
        return self.multiverse.get(dim_id)

    def get_connections(self, dim_id):
        """Dapatkan koneksi dari dimensi tertentu"""
        connections = []
        for conn in self.connections:
            if conn['from'] == dim_id or conn['to'] == dim_id:
                connections.append(conn)
        return connections

    def find_route(self, from_dim, to_dim):
        """Cari rute antar dimensi (BFS)"""
        visited = set()
        queue = [[from_dim]]
        
        while queue:
            path = queue.pop(0)
            node = path[-1]
            
            if node == to_dim:
                return path
            
            if node not in visited:
                visited.add(node)
                
                # Cari koneksi
                for conn in self.connections:
                    if conn['from'] == node and conn['to'] not in visited:
                        new_path = list(path)
                        new_path.append(conn['to'])
                        queue.append(new_path)
                    elif conn['to'] == node and conn['from'] not in visited:
                        new_path = list(path)
                        new_path.append(conn['from'])
                        queue.append(new_path)
        
        return None

    def get_route_details(self, route_path):
        """Dapatkan detail rute"""
        details = []
        for dim in route_path:
            dim_info = self.get_dimension(dim)
            if dim_info:
                details.append({
                    'dimension': dim,
                    'name': dim_info['name'],
                    'stability': dim_info['stability']
                })
        return details

    def update_dimension_status(self, dim_id, status):
        """Update status dimensi"""
        if dim_id in self.multiverse:
            self.multiverse[dim_id]['status'] = status
            self.save_map()
            print(f"✅ {dim_id} status updated to {status}")

    def add_anomaly(self, name, location, severity, description):
        """Tambahkan anomali baru"""
        anomaly = {
            'id': f"a{len(self.anomalies)+1:03d}",
            'name': name,
            'location': location,
            'severity': severity,
            'status': 'active',
            'description': description
        }
        self.anomalies.append(anomaly)
        self.save_map()
        print(f"✅ Anomaly added: {name}")

    def display_map(self):
        """Tampilkan peta multiverse"""
        print("\n" + "="*80)
        print("🗺️ MULTIVERSE MAP — KOSMIK KEY v8.0")
        print("="*80)
        print(f"📅 Last Updated: {self.last_update}")
        print(f"🌌 Total Dimensions: {len(self.multiverse)}")
        print(f"🔗 Total Connections: {len(self.connections)}")
        print(f"🗺️ Total Routes: {len(self.routes)}")
        print(f"⚠️ Active Anomalies: {len([a for a in self.anomalies if a['status'] == 'active'])}")
        print("="*80)
        
        # Dimensi yang diketahui
        print("\n🌌 KNOWN DIMENSIONS:")
        print("-"*80)
        for dim_id, info in self.multiverse.items():
            status_icon = {
                'active': '🟢',
                'unstable': '🟡',
                'exploring': '🔵',
                'hidden': '🔴',
                'blocked': '⚫'
            }.get(info['status'], '⚪')
            
            stability_bar = "█" * int(info['stability'] * 10)
            accessible = '✅' if info['accessible'] else '❌'
            
            print(f"\n   {status_icon} {info['name']} ({dim_id})")
            print(f"      Type: {info['type']}")
            print(f"      Stability: {stability_bar} {info['stability']*100:.0f}%")
            print(f"      Accessible: {accessible}")
            print(f"      Inhabitants: {', '.join(info['inhabitants'][:3])}...")
            print(f"      Coordinates: X={info['coordinates']['x']}, Y={info['coordinates']['y']}, Z={info['coordinates']['z']}, T={info['coordinates']['t']}")
        
        print("\n" + "="*80)

    def display_connections(self):
        """Tampilkan koneksi antar dimensi"""
        print("\n" + "="*80)
        print("🔗 DIMENSIONAL CONNECTIONS")
        print("="*80)
        
        for conn in self.connections:
            from_name = self.multiverse.get(conn['from'], {}).get('name', conn['from'])
            to_name = self.multiverse.get(conn['to'], {}).get('name', conn['to'])
            strength_bar = "█" * int(conn['strength'] * 10)
            
            status_icon = {
                'active': '🟢',
                'blocked': '🔴',
                'unstable': '🟡',
                'exploring': '🔵',
                'undiscovered': '⚪'
            }.get(conn['status'], '⚪')
            
            print(f"\n   {status_icon} {from_name} → {to_name}")
            print(f"      Type: {conn['type']}")
            print(f"      Strength: {strength_bar} {conn['strength']*100:.0f}%")
            print(f"      Status: {conn['status']}")
        
        print("\n" + "="*80)

    def display_routes(self):
        """Tampilkan rute perjalanan"""
        print("\n" + "="*80)
        print("🗺️ TRAVEL ROUTES")
        print("="*80)
        
        for route in self.routes:
            route_type_icon = {
                'safe': '🟢',
                'dangerous': '🔴',
                'unstable': '🟡',
                'unknown': '🔵'
            }.get(route['type'], '⚪')
            
            print(f"\n   {route_type_icon} {route['name']}")
            print(f"      Path: {' → '.join(route['path'])}")
            print(f"      Type: {route['type']}")
            print(f"      Length: {route['length']} dimensions")
            print(f"      Description: {route['description']}")
        
        print("\n" + "="*80)

    def display_anomalies(self):
        """Tampilkan anomali di multiverse"""
        print("\n" + "="*80)
        print("⚠️ MULTIVERSE ANOMALIES")
        print("="*80)
        
        for anomaly in self.anomalies:
            severity_icon = {
                'low': '🟢',
                'medium': '🟡',
                'high': '🔴',
                'critical': '💀'
            }.get(anomaly['severity'], '⚪')
            
            status_icon = {
                'active': '🟢',
                'monitoring': '🟡',
                'repairing': '🔵',
                'resolved': '✅'
            }.get(anomaly['status'], '⚪')
            
            location_name = self.multiverse.get(anomaly['location'], {}).get('name', anomaly['location'])
            
            print(f"\n   {severity_icon} [{anomaly['id']}] {anomaly['name']}")
            print(f"      Location: {location_name}")
            print(f"      Severity: {anomaly['severity'].upper()}")
            print(f"      Status: {anomaly['status']}")
            print(f"      Description: {anomaly['description']}")
        
        print("\n" + "="*80)

    def display_timeline_branches(self):
        """Tampilkan cabang timeline alternatif"""
        print("\n" + "="*80)
        print("🌿 TIMELINE BRANCHES")
        print("="*80)
        
        for dim_id, data in self.timeline_branches.items():
            dim_name = self.multiverse.get(dim_id, {}).get('name', dim_id)
            print(f"\n   🌌 {dim_name} ({dim_id})")
            print(f"      Main: {data['main']}")
            print(f"      Branches:")
            for branch_id, desc in data['branches'].items():
                print(f"         • {branch_id}: {desc}")
        
        print("\n" + "="*80)

    def display_federation_map(self):
        """Tampilkan peta khusus Galactic Federation"""
        print("\n" + "="*80)
        print("🛸 GALACTIC FEDERATION — MULTIVERSE MAP")
        print("="*80)
        
        # Federation dimensions
        fed_dims = ['gamma', 'prime', 'beta', 'zeta', 'theta']
        
        print("\n   🏛️ FEDERATION DIMENSIONS:")
        for dim in fed_dims:
            info = self.multiverse.get(dim)
            if info:
                print(f"      • {info['name']} — {info['type']}")
        
        # Federation routes
        print("\n   🗺️ FEDERATION ROUTES:")
        fed_routes = [r for r in self.routes if r['type'] in ['safe', 'federation']]
        for route in fed_routes:
            print(f"      • {route['name']}: {' → '.join(route['path'])}")
        
        print("\n" + "="*80)

    def interactive_mode(self):
        """Mode interaktif Multiverse Map"""
        print("\n" + "="*80)
        print("🗺️ MULTIVERSE MAPPING SYSTEM — INTERACTIVE MODE")
        print("="*80)
        
        while True:
            print("\n📋 COMMANDS:")
            print("   [M] Display Full Map")
            print("   [C] Display Connections")
            print("   [R] Display Routes")
            print("   [A] Display Anomalies")
            print("   [T] Display Timeline Branches")
            print("   [F] Display Federation Map")
            print("   [D] Dimension Details")
            print("   [S] Search Route")
            print("   [U] Update Dimension Status")
            print("   [N] Add Anomaly")
            print("   [X] Exit")
            
            choice = input("\n📱 Enter choice: ").strip().upper()
            
            if choice == 'M':
                self.display_map()
            
            elif choice == 'C':
                self.display_connections()
            
            elif choice == 'R':
                self.display_routes()
            
            elif choice == 'A':
                self.display_anomalies()
            
            elif choice == 'T':
                self.display_timeline_branches()
            
            elif choice == 'F':
                self.display_federation_map()
            
            elif choice == 'D':
                dim_id = input("Enter dimension ID: ").strip().lower()
                dim = self.get_dimension(dim_id)
                if dim:
                    print(f"\n📋 DIMENSION: {dim['name']} ({dim_id})")
                    for key, value in dim.items():
                        print(f"   {key}: {value}")
                else:
                    print("❌ Dimension not found!")
            
            elif choice == 'S':
                from_dim = input("From dimension: ").strip().lower()
                to_dim = input("To dimension: ").strip().lower()
                
                route = self.find_route(from_dim, to_dim)
                if route:
                    print(f"\n🗺️ Route found: {' → '.join(route)}")
                    details = self.get_route_details(route)
                    for d in details:
                        print(f"   • {d['name']} (Stability: {d['stability']*100:.0f}%)")
                else:
                    print("❌ No route found!")
            
            elif choice == 'U':
                dim_id = input("Dimension ID: ").strip().lower()
                status = input("Status (active/unstable/exploring/hidden/blocked): ").strip().lower()
                self.update_dimension_status(dim_id, status)
            
            elif choice == 'N':
                name = input("Anomaly name: ").strip()
                location = input("Location dimension: ").strip().lower()
                severity = input("Severity (low/medium/high/critical): ").strip().lower()
                description = input("Description: ").strip()
                self.add_anomaly(name, location, severity, description)
            
            elif choice == 'X':
                print("👋 Exiting Multiverse Map...")
                break
            
            else:
                print("❌ Invalid command!")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    map_system = MultiverseMap()
    
    # Test mode
    print("\n🧪 TEST MODE — Multiverse Mapping System")
    print("="*80)
    
    # Display map
    map_system.display_map()
    
    # Display connections
    map_system.display_connections()
    
    # Display routes
    map_system.display_routes()
    
    # Display anomalies
    map_system.display_anomalies()
    
    # Display timeline
    map_system.display_timeline_branches()
    
    # Display federation map
    map_system.display_federation_map()
    
    # Start interactive
    map_system.interactive_mode()
