#!/usr/bin/env python3
# Time Travel Protocol — Kosmik Key v8.0
# Sistem Perjalanan Waktu dan Stabilisasi Temporal

import json
import os
import random
import math
import time
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import uuid

class TimeTravelProtocol:
    def __init__(self):
        self.logs_dir = Path.home() / "kosmik" / "logs"
        self.protocol_file = self.logs_dir / "time_travel_logs.json"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Inisialisasi sistem
        self.eras = self.init_eras()
        self.timeline_rules = self.init_timeline_rules()
        self.anomalies = self.init_anomalies()
        self.travels = self.load_travels()
        self.current_travel = None
        self.temporal_stability = 1.0

    def init_eras(self):
        """Database Era Waktu"""
        return {
            'prehistoric': {
                'name': 'Prehistoric Era',
                'icon': '🦕',
                'years_ago': '65,000,000 - 10,000',
                'description': 'Zaman dinosaurus hingga awal peradaban manusia',
                'stability': 0.7,
                'danger_level': 'high',
                'notable_events': ['Dinosaur extinction', 'First humans']
            },
            'ancient': {
                'name': 'Ancient Era',
                'icon': '🏛️',
                'years_ago': '10,000 - 500',
                'description': 'Peradaban kuno Mesir, Yunani, Roma, dan lainnya',
                'stability': 0.85,
                'danger_level': 'medium',
                'notable_events': ['Pyramids built', 'Roman Empire', 'Greek philosophy']
            },
            'medieval': {
                'name': 'Medieval Era',
                'icon': '⚔️',
                'years_ago': '500 - 1500',
                'description': 'Zaman pertengahan di Eropa dan dunia',
                'stability': 0.8,
                'danger_level': 'medium',
                'notable_events': ['Crusades', 'Black Death', 'Mongol Empire']
            },
            'renaissance': {
                'name': 'Renaissance Era',
                'icon': '🎨',
                'years_ago': '1500 - 1800',
                'description': 'Kebangkitan seni, sains, dan eksplorasi',
                'stability': 0.9,
                'danger_level': 'medium',
                'notable_events': ['Da Vinci', 'Galileo', 'Discovery of Americas']
            },
            'industrial': {
                'name': 'Industrial Era',
                'icon': '🏭',
                'years_ago': '1800 - 1950',
                'description': 'Revolusi industri dan modernisasi',
                'stability': 0.95,
                'danger_level': 'low',
                'notable_events': ['Industrial Revolution', 'World Wars', 'Einstein']
            },
            'modern': {
                'name': 'Modern Era',
                'icon': '📱',
                'years_ago': '1950 - Present',
                'description': 'Era teknologi dan informasi',
                'stability': 0.98,
                'danger_level': 'low',
                'notable_events': ['Space Age', 'Internet', 'AI development']
            },
            'future': {
                'name': 'Future Era',
                'icon': '🚀',
                'years_ago': 'Present - 3000',
                'description': 'Masa depan yang belum terjadi',
                'stability': 0.4,
                'danger_level': 'extreme',
                'notable_events': ['Mars colonization', 'First Contact', 'Federation formation']
            },
            'distant_future': {
                'name': 'Distant Future',
                'icon': '🌌',
                'years_ago': '3000 - 100,000',
                'description': 'Masa depan jauh yang tidak pasti',
                'stability': 0.2,
                'danger_level': 'extreme',
                'notable_events': ['Galactic civilization', 'Dimensional integration']
            },
            'alternate': {
                'name': 'Alternate Timeline',
                'icon': '🌀',
                'years_ago': 'Variable',
                'description': 'Dimensi dengan sejarah alternatif',
                'stability': 0.3,
                'danger_level': 'extreme',
                'notable_events': ['Timeline divergence', 'Alternate history']
            },
            'quantum': {
                'name': 'Quantum Timeline',
                'icon': '⚛️',
                'years_ago': 'Variable',
                'description': 'Timeline quantum dengan banyak kemungkinan',
                'stability': 0.1,
                'danger_level': 'extreme',
                'notable_events': ['Quantum superposition', 'Probability collapse']
            }
        }

    def init_timeline_rules(self):
        """Aturan perjalanan waktu"""
        return {
            'no_paradox': 'Jangan menciptakan paradoks waktu — bisa merusak timeline',
            'fixed_points': 'Beberapa peristiwa tidak bisa diubah (fixed points in time)',
            'butterfly_effect': 'Perubahan kecil bisa berdampak besar di masa depan',
            'observer_effect': 'Kehadiranmu bisa mengubah sejarah',
            'temporal_insurance': 'Selalu buat checkpoint sebelum perubahan besar',
            'no_contact': 'Jangan kontak dengan dirimu sendiri',
            'limited_stay': 'Batas waktu di masa lalu adalah 24 jam',
            'return_window': 'Jendela kembali harus dihitung dengan tepat',
            'anchoring': 'Gunakan anchor temporal untuk kembali ke waktu sekarang'
        }

    def init_anomalies(self):
        """Anomali temporal yang diketahui"""
        return [
            {
                'id': 'ta_001',
                'name': 'Temporal Rift',
                'description': 'Celah waktu yang tidak stabil',
                'severity': 'high',
                'location': 'Near Black Holes'
            },
            {
                'id': 'ta_002',
                'name': 'Time Loop',
                'description': 'Lingkaran waktu yang berulang',
                'severity': 'critical',
                'location': 'Event Horizon'
            },
            {
                'id': 'ta_003',
                'name': 'Temporal Echo',
                'description': 'Gema dari masa lalu atau masa depan',
                'severity': 'medium',
                'location': 'Dimensional boundaries'
            },
            {
                'id': 'ta_004',
                'name': 'Grandfather Paradox Zone',
                'description': 'Zona di mana paradoks kakek bisa terjadi',
                'severity': 'critical',
                'location': 'Quantum states'
            },
            {
                'id': 'ta_005',
                'name': 'Temporal Vacuum',
                'description': 'Vakum temporal tanpa waktu',
                'severity': 'extreme',
                'location': 'Void regions'
            }
        ]

    def load_travels(self):
        """Load travel logs dari file"""
        if self.protocol_file.exists():
            try:
                with open(self.protocol_file, 'r') as f:
                    data = json.load(f)
                    return data.get('travels', [])
            except:
                return []
        return []

    def save_travels(self):
        """Simpan travel logs ke file"""
        data = {
            'last_updated': datetime.now().isoformat(),
            'total_travels': len(self.travels),
            'travels': self.travels
        }
        with open(self.protocol_file, 'w') as f:
            json.dump(data, f, indent=2)

    def calculate_temporal_energy(self, target_era, distance_years):
        """Hitung energi temporal yang dibutuhkan"""
        # Faktor era
        era_stability = self.eras.get(target_era, {}).get('stability', 0.5)
        
        # Energi dasar
        base_energy = 100
        
        # Faktor jarak waktu
        distance_factor = math.log10(distance_years + 1) * 10
        
        # Faktor stabilitas
        stability_factor = 1 / (era_stability + 0.1)
        
        # Total energi
        total_energy = base_energy * distance_factor * stability_factor
        
        return round(total_energy, 2)

    def calculate_temporal_coordinates(self, target_year, target_era):
        """Hitung koordinat temporal"""
        current_year = datetime.now().year
        
        # Jarak waktu
        if target_era in ['future', 'distant_future']:
            distance = target_year - current_year
        elif target_era in ['prehistoric', 'ancient', 'medieval', 'renaissance', 'industrial', 'modern']:
            distance = current_year - target_year
        else:
            distance = 0
        
        # Koordinat temporal
        coordinates = {
            'year': target_year,
            'era': target_era,
            'distance_years': abs(distance),
            'direction': 'forward' if distance > 0 else 'backward' if distance < 0 else 'stationary',
            'temporal_phase': random.uniform(0, 2 * math.pi),
            'stability': self.eras.get(target_era, {}).get('stability', 0.5)
        }
        
        return coordinates

    def calculate_return_window(self, target_era):
        """Hitung jendela kembali"""
        era = self.eras.get(target_era)
        if not era:
            return 24
        
        # Stabilitas era menentukan jendela
        stability = era['stability']
        
        # Jendela = 24 jam * stabilitas
        window_hours = 24 * stability
        
        # Tambah faktor keamanan
        if stability < 0.5:
            window_hours *= 0.5
        elif stability < 0.7:
            window_hours *= 0.75
        
        return round(window_hours, 2)

    def plan_travel(self, target_era, target_year, purpose):
        """Rencanakan perjalanan waktu"""
        era_info = self.eras.get(target_era)
        if not era_info:
            return {"error": "Era tidak ditemukan"}
        
        # Hitung energi
        energy = self.calculate_temporal_energy(target_era, abs(target_year - datetime.now().year))
        
        # Hitung koordinat
        coords = self.calculate_temporal_coordinates(target_year, target_era)
        
        # Hitung jendela kembali
        return_window = self.calculate_return_window(target_era)
        
        # Generate travel ID
        travel_id = f"tt_{uuid.uuid4().hex[:8]}"
        
        # Plan
        plan = {
            'id': travel_id,
            'era': target_era,
            'era_name': era_info['name'],
            'target_year': target_year,
            'purpose': purpose,
            'energy_required': energy,
            'coordinates': coords,
            'return_window_hours': return_window,
            'stability': era_info['stability'],
            'danger_level': era_info['danger_level'],
            'notable_events': era_info['notable_events'],
            'timestamp': datetime.now().isoformat(),
            'status': 'planned'
        }
        
        return plan

    def execute_travel(self, plan):
        """Eksekusi perjalanan waktu"""
        if not plan:
            return {"error": "No plan provided"}
        
        print(f"\n⏳ INITIATING TIME TRAVEL TO {plan['era_name']}")
        print("="*60)
        
        # Simulasi persiapan
        print("🔄 Initializing temporal generator...")
        time.sleep(1)
        print(f"⚡ Energy: {plan['energy_required']} units")
        time.sleep(0.5)
        print(f"📍 Target: Year {plan['target_year']}")
        time.sleep(0.5)
        print(f"🔄 Return Window: {plan['return_window_hours']} hours")
        time.sleep(0.5)
        
        # Risiko anomali
        anomaly_risk = self.calculate_anomaly_risk(plan)
        
        print(f"\n⚠️ Anomaly Risk: {anomaly_risk*100:.1f}%")
        
        if anomaly_risk > 0.7:
            print("🚨 HIGH ANOMALY RISK! Proceed with extreme caution.")
        
        # Mulai perjalanan
        print("\n🌀 Opening temporal portal...")
        time.sleep(1)
        print("🌌 Entering timeline...")
        time.sleep(1)
        
        # Update status
        plan['status'] = 'in_progress'
        plan['start_time'] = datetime.now().isoformat()
        plan['anomaly_risk'] = anomaly_risk
        self.current_travel = plan
        
        # Simpan ke log
        self.travels.append(plan)
        self.save_travels()
        
        print("\n✅ TIME TRAVEL INITIATED!")
        print(f"📋 Travel ID: {plan['id']}")
        print("="*60)
        
        return plan

    def return_from_travel(self, travel_id):
        """Kembali dari perjalanan waktu"""
        # Cari travel
        travel = None
        for t in self.travels:
            if t['id'] == travel_id:
                travel = t
                break
        
        if not travel:
            return {"error": "Travel not found"}
        
        print(f"\n⏳ RETURNING FROM {travel['era_name']}")
        print("="*60)
        
        # Simulasi kembali
        print("🔄 Stabilizing temporal anchor...")
        time.sleep(1)
        print("🌀 Closing temporal portal...")
        time.sleep(1)
        print("🌌 Returning to present...")
        time.sleep(1)
        
        # Update status
        travel['status'] = 'completed'
        travel['end_time'] = datetime.now().isoformat()
        
        # Hitung durasi
        start = datetime.fromisoformat(travel['start_time'])
        end = datetime.fromisoformat(travel['end_time'])
        duration = end - start
        
        travel['duration'] = str(duration)
        
        self.current_travel = None
        self.save_travels()
        
        print("\n✅ SUCCESSFULLY RETURNED TO PRESENT!")
        print(f"📋 Duration: {duration}")
        print("="*60)
        
        return travel

    def calculate_anomaly_risk(self, plan):
        """Hitung risiko anomali temporal"""
        era = self.eras.get(plan['era'])
        if not era:
            return 0.5
        
        # Faktor stabilitas
        stability = era['stability']
        risk = 1 - stability
        
        # Faktor jarak
        distance = abs(plan['target_year'] - datetime.now().year)
        distance_factor = min(1, distance / 1000000)
        risk += distance_factor * 0.2
        
        # Faktor quantum random
        risk += random.uniform(0, 0.1)
        
        # Faktor anomali aktif
        active_anomalies = len([a for a in self.anomalies if a['severity'] in ['high', 'critical', 'extreme']])
        risk += active_anomalies * 0.02
        
        return min(1, risk)

    def get_temporal_stability(self):
        """Dapatkan stabilitas temporal saat ini"""
        # Hitung berdasarkan log
        if not self.travels:
            return 1.0
        
        # Faktor dari travel terakhir
        last_travel = self.travels[-1]
        era = self.eras.get(last_travel.get('era'))
        if era:
            stability = era['stability']
        else:
            stability = 0.5
        
        # Faktor anomali
        anomaly_factor = len([a for a in self.anomalies if a['severity'] in ['critical', 'extreme']]) * 0.05
        
        return max(0.1, min(1, stability - anomaly_factor))

    def get_all_eras(self):
        """Dapatkan semua era yang tersedia"""
        return self.eras

    def get_era_info(self, era_id):
        """Dapatkan info era tertentu"""
        return self.eras.get(era_id)

    def get_travel_history(self):
        """Dapatkan semua riwayat perjalanan"""
        return self.travels

    def get_anomalies(self):
        """Dapatkan daftar anomali"""
        return self.anomalies

    def get_timeline_rules(self):
        """Dapatkan aturan timeline"""
        return self.timeline_rules

    def display_eras(self):
        """Tampilkan semua era"""
        print("\n" + "="*80)
        print("⏳ TIME TRAVEL — AVAILABLE ERAS")
        print("="*80)
        
        for era_id, info in self.eras.items():
            danger_icons = {
                'low': '🟢',
                'medium': '🟡',
                'high': '🔴',
                'extreme': '💀'
            }
            
            stability_bar = "█" * int(info['stability'] * 10)
            stability_empty = "░" * (10 - int(info['stability'] * 10))
            
            print(f"\n   {info['icon']} {info['name']} ({era_id})")
            print(f"      {info['description']}")
            print(f"      Years: {info['years_ago']}")
            print(f"      Stability: [{stability_bar}{stability_empty}] {info['stability']*100:.0f}%")
            print(f"      Danger: {danger_icons.get(info['danger_level'], '⚪')} {info['danger_level'].upper()}")
            print(f"      Events: {', '.join(info['notable_events'][:2])}...")
        print("\n" + "="*80)

    def display_anomalies(self):
        """Tampilkan anomali temporal"""
        print("\n" + "="*80)
        print("⚠️ TEMPORAL ANOMALIES")
        print("="*80)
        
        severity_icons = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🔴',
            'critical': '💀',
            'extreme': '☠️'
        }
        
        for anomaly in self.anomalies:
            print(f"\n   {severity_icons.get(anomaly['severity'], '⚪')} [{anomaly['id']}] {anomaly['name']}")
            print(f"      {anomaly['description']}")
            print(f"      Severity: {anomaly['severity'].upper()}")
            print(f"      Location: {anomaly['location']}")
        print("\n" + "="*80)

    def display_rules(self):
        """Tampilkan aturan timeline"""
        print("\n" + "="*80)
        print("📜 TIMELINE RULES")
        print("="*80)
        
        for rule_id, rule in self.timeline_rules.items():
            print(f"\n   📌 {rule_id.replace('_', ' ').title()}")
            print(f"      {rule}")
        print("\n" + "="*80)

    def display_stats(self):
        """Tampilkan statistik"""
        stats = {
            'total_travels': len(self.travels),
            'completed': len([t for t in self.travels if t.get('status') == 'completed']),
            'in_progress': len([t for t in self.travels if t.get('status') == 'in_progress']),
            'planned': len([t for t in self.travels if t.get('status') == 'planned']),
            'temporal_stability': self.get_temporal_stability(),
            'active_anomalies': len([a for a in self.anomalies if a['severity'] in ['high', 'critical', 'extreme']])
        }
        
        print("\n" + "="*80)
        print("📊 TIME TRAVEL STATISTICS")
        print("="*80)
        print(f"\n   🌀 Total Travels: {stats['total_travels']}")
        print(f"   ✅ Completed: {stats['completed']}")
        print(f"   ⏳ In Progress: {stats['in_progress']}")
        print(f"   📋 Planned: {stats['planned']}")
        print(f"   ⚡ Temporal Stability: {stats['temporal_stability']*100:.1f}%")
        print(f"   ⚠️ Active Anomalies: {stats['active_anomalies']}")
        
        # Recent travels
        if self.travels:
            print(f"\n   📋 Recent Travels:")
            for t in self.travels[-3:]:
                era_name = self.eras.get(t.get('era'), {}).get('name', 'Unknown')
                status_icon = {
                    'completed': '✅',
                    'in_progress': '⏳',
                    'planned': '📋'
                }.get(t.get('status'), '❓')
                print(f"      {status_icon} {t.get('id')}: {era_name} (Year {t.get('target_year', 'Unknown')})")
        
        print("\n" + "="*80)

    def interactive_mode(self):
        """Mode interaktif Time Travel Protocol"""
        print("\n" + "="*80)
        print("⏳ TIME TRAVEL PROTOCOL — INTERACTIVE MODE")
        print("="*80)
        
        while True:
            print("\n📋 COMMANDS:")
            print("   [E] View Eras")
            print("   [P] Plan Travel")
            print("   [T] Execute Travel (from plan)")
            print("   [R] Return from Travel")
            print("   [A] View Anomalies")
            print("   [L] Timeline Rules")
            print("   [H] Travel History")
            print("   [S] Statistics")
            print("   [I] Temporal Info")
            print("   [X] Exit")
            
            choice = input("\n📱 Enter choice: ").strip().upper()
            
            if choice == 'E':
                self.display_eras()
            
            elif choice == 'P':
                print("\n📌 Available Eras:")
                for era_id, info in self.eras.items():
                    print(f"   {era_id}: {info['name']} ({info['years_ago']})")
                
                era = input("\nTarget era: ").strip().lower()
                if era not in self.eras:
                    print("❌ Invalid era!")
                    continue
                
                year = input("Target year: ").strip()
                try:
                    year = int(year)
                except:
                    print("❌ Invalid year!")
                    continue
                
                purpose = input("Purpose of travel: ").strip() or "Exploration"
                
                plan = self.plan_travel(era, year, purpose)
                if 'error' in plan:
                    print(f"❌ {plan['error']}")
                else:
                    print("\n✅ TRAVEL PLAN CREATED!")
                    print(f"   ID: {plan['id']}")
                    print(f"   Era: {plan['era_name']}")
                    print(f"   Year: {plan['target_year']}")
                    print(f"   Energy: {plan['energy_required']} units")
                    print(f"   Return Window: {plan['return_window_hours']} hours")
                    print(f"   Danger Level: {plan['danger_level'].upper()}")
            
            elif choice == 'T':
                if not self.current_travel:
                    # Cari travel yang belum dieksekusi
                    pending = [t for t in self.travels if t.get('status') == 'planned']
                    if pending:
                        # Gunakan yang paling baru
                        plan = pending[-1]
                        self.execute_travel(plan)
                    else:
                        print("⚠️ No planned travel found. Create a plan first.")
                else:
                    print("⚠️ Travel already in progress!")
            
            elif choice == 'R':
                if self.current_travel:
                    travel_id = self.current_travel.get('id')
                    self.return_from_travel(travel_id)
                else:
                    print("⚠️ No active travel to return from.")
            
            elif choice == 'A':
                self.display_anomalies()
            
            elif choice == 'L':
                self.display_rules()
            
            elif choice == 'H':
                if self.travels:
                    print("\n📋 TRAVEL HISTORY:")
                    for t in self.travels[-10:]:
                        era_name = self.eras.get(t.get('era'), {}).get('name', 'Unknown')
                        status_icon = {
                            'completed': '✅',
                            'in_progress': '⏳',
                            'planned': '📋'
                        }.get(t.get('status'), '❓')
                        print(f"   {status_icon} {t.get('id')}: {era_name} → Year {t.get('target_year', 'Unknown')} ({t.get('status', 'Unknown')})")
                else:
                    print("⚠️ No travel history.")
            
            elif choice == 'S':
                self.display_stats()
            
            elif choice == 'I':
                print("\n🔮 TEMPORAL INFORMATION")
                print("="*60)
                print(f"   Temporal Stability: {self.get_temporal_stability()*100:.1f}%")
                print(f"   Active Travel: {'✅ Yes' if self.current_travel else '❌ No'}")
                if self.current_travel:
                    print(f"   Current Travel ID: {self.current_travel.get('id')}")
                    print(f"   Current Era: {self.current_travel.get('era_name')}")
                print(f"   Total Anomalies: {len(self.anomalies)}")
                print(f"   Total Travels: {len(self.travels)}")
                print("="*60)
            
            elif choice == 'X':
                print("👋 Exiting Time Travel Protocol...")
                print("⏳ Time is a river... navigate carefully.")
                break
            
            else:
                print("❌ Invalid command!")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    protocol = TimeTravelProtocol()
    
    # Test mode
    print("\n🧪 TEST MODE — Time Travel Protocol")
    print("="*80)
    
    # Display eras
    protocol.display_eras()
    
    # Display anomalies
    protocol.display_anomalies()
    
    # Display rules
    protocol.display_rules()
    
    # Test plan travel
    print("\n📋 TEST PLAN TRAVEL:")
    print("-"*80)
    
    plan = protocol.plan_travel('ancient', -5000, "Study ancient civilizations")
    if 'error' not in plan:
        print(f"\n   ✅ Plan Created:")
        print(f"      ID: {plan['id']}")
        print(f"      Era: {plan['era_name']}")
        print(f"      Year: {plan['target_year']}")
        print(f"      Energy: {plan['energy_required']} units")
        print(f"      Return Window: {plan['return_window_hours']} hours")
        print(f"      Danger Level: {plan['danger_level'].upper()}")
        print(f"      Stability: {plan['stability']*100:.1f}%")
    
    # Test execute travel
    print("\n🚀 TEST EXECUTE TRAVEL:")
    print("-"*80)
    
    # Cari travel yang sudah dibuat
    if protocol.travels:
        last_travel = protocol.travels[-1]
        protocol.execute_travel(last_travel)
        protocol.return_from_travel(last_travel['id'])
    
    # Display stats
    protocol.display_stats()
    
    # Start interactive
    protocol.interactive_mode()
