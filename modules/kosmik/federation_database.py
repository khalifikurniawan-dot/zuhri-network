#!/usr/bin/env python3
# Federation Database — Galactic Encyclopedia
# Kosmik Key v8.0-Alpha — Federation Protocol

import json
import random
import hashlib
from datetime import datetime
from collections import defaultdict

class FederationDatabase:
    def __init__(self):
        # Database initialization
        self.species_db = self.init_species()
        self.technology_db = self.init_technology()
        self.history_db = self.init_history()
        self.galactic_map = self.init_galactic_map()
        self.council_db = self.init_council()
        self.location_db = self.init_locations()
        
        # Index
        self.index = self.build_index()
        
        # Search history
        self.search_history = []

    def init_species(self):
        """Database spesies di Galactic Federation"""
        return {
            'eldritch': {
                'name': 'The Ancient Ones',
                'classification': 'Transcendent',
                'homeworld': 'Unknown (Beyond known dimensions)',
                'consciousness_level': 1.0,
                'population': 'Unknown',
                'technology_rating': 'Omega+',
                'language': 'Telepathic resonance',
                'physical_form': 'Non-corporeal energy beings',
                'psychic_abilities': [
                    'Reality manipulation',
                    'Time perception control',
                    'Consciousness merging',
                    'Dimensional creation'
                ],
                'status': 'Council Leader',
                'first_contact': 'Before recorded history',
                'known_factions': ['Overseers', 'Watchers', 'Architects']
            },
            'telepathic': {
                'name': 'The Psychic Collective',
                'classification': 'Psi-active Humanoid',
                'homeworld': 'Zenon-7 (Andromeda Galaxy)',
                'consciousness_level': 0.85,
                'population': '12 billion',
                'technology_rating': 'Alpha',
                'language': 'Telepathy, Mental projection',
                'physical_form': 'Humanoid, blue-skinned, large eyes',
                'psychic_abilities': [
                    'Telepathy',
                    'Precognition',
                    'Psychokinesis',
                    'Empathic projection'
                ],
                'status': 'Council Member',
                'first_contact': '2157 CE',
                'known_factions': ['Psi-Core', 'Thinkers Guild', 'Empaths Union']
            },
            'hive_mind': {
                'name': 'The Unity',
                'classification': 'Collective Consciousness',
                'homeworld': 'Xylos-9 (Milky Way, Outer Arm)',
                'consciousness_level': 0.92,
                'population': '50 billion (across 12 systems)',
                'technology_rating': 'Alpha+',
                'language': 'Resonant frequency, Quantum entanglement',
                'physical_form': 'Insectoid, biomechanical',
                'psychic_abilities': [
                    'Collective consciousness',
                    'Swarm intelligence',
                    'Adaptive evolution',
                    'Shared memory'
                ],
                'status': 'Council Member',
                'first_contact': '2450 CE',
                'known_factions': ['Swarm Command', 'Evolution Nexus', 'Memory Matrix']
            },
            'crystalline': {
                'name': 'The Harmonic Guardians',
                'classification': 'Crystalline Lifeform',
                'homeworld': 'Crystallis Prime (Triangulum Galaxy)',
                'consciousness_level': 0.72,
                'population': '8 billion',
                'technology_rating': 'Beta+',
                'language': 'Harmonic resonance, Light pulses',
                'physical_form': 'Crystalline structures, Energy lattice',
                'psychic_abilities': [
                    'Energy manipulation',
                    'Vibration control',
                    'Dimensional resonance',
                    'Healing harmonics'
                ],
                'status': 'Council Member',
                'first_contact': '1987 CE',
                'known_factions': ['Resonance Guild', 'Light Weavers', 'Crystal Keepers']
            },
            'plasma': {
                'name': 'The Light Beings',
                'classification': 'Plasma-based Energy Lifeform',
                'homeworld': 'Solaris-3 (Zeta Reticuli)',
                'consciousness_level': 0.65,
                'population': 'Unknown (Energy beings)',
                'technology_rating': 'Beta',
                'language': 'Light frequencies, Plasma signatures',
                'physical_form': 'Pure energy, Plasma clouds',
                'psychic_abilities': [
                    'Energy projection',
                    'Light manipulation',
                    'Quantum tunneling',
                    'Energy healing'
                ],
                'status': 'Council Member',
                'first_contact': '2024 CE',
                'known_factions': ['Solar Wing', 'Plasma Core', 'Photon Collective']
            },
            'human_earth': {
                'name': 'Humans (Earth)',
                'classification': 'Primitive Sapient',
                'homeworld': 'Earth, Sol System',
                'consciousness_level': 0.25,
                'population': '8.2 billion',
                'technology_rating': 'Delta',
                'language': 'Various (6000+ languages)',
                'physical_form': 'Bipedal, organic',
                'psychic_abilities': ['Limited telepathy (sleeping)', 'Potential latent'],
                'status': 'Observer (Pending Membership)',
                'first_contact': 'Not official (Observation only)',
                'known_factions': ['Various nation-states', 'Secret societies']
            }
        }

    def init_technology(self):
        """Database teknologi Galactic Federation"""
        return {
            'teleportation': {
                'name': 'Quantum Teleportation',
                'type': 'Travel',
                'inventors': ['The Ancient Ones', 'Psychic Collective'],
                'year_developed': '~10,000 BCE',
                'energy_requirement': '5.2 petawatts',
                'max_distance': 'Interdimensional',
                'stability_rating': 0.95,
                'limitations': ['Requires quantum entanglement', 'Exact coordinates needed'],
                'used_by': ['Galactic Federation', 'All member species']
            },
            'wormhole_generation': {
                'name': 'Stable Wormhole Generator',
                'type': 'Travel, Communication',
                'inventors': ['The Unity', 'Crystalline Guardians'],
                'year_developed': '3000 CE',
                'energy_requirement': '12.8 petawatts',
                'max_distance': 'Intergalactic',
                'stability_rating': 0.88,
                'limitations': ['Exotic matter required', 'Dimensional stress'],
                'used_by': ['Federation Council', 'Advanced members']
            },
            'consciousness_amplifier': {
                'name': 'Psi-Amplifier Matrix',
                'type': 'Communication, Enhancement',
                'inventors': ['Telepathic Collective'],
                'year_developed': '2800 CE',
                'energy_requirement': '0.8 petawatts',
                'range': 'Galactic scale',
                'stability_rating': 0.92,
                'limitations': ['Requires psychic ability', 'Emotional instability risk'],
                'used_by': ['Psi-Core Guild', 'Federation Communication Hub']
            },
            'crystalline_grid': {
                'name': 'Dimensional Stabilization Grid',
                'type': 'Defense, Infrastructure',
                'inventors': ['Crystalline Guardians'],
                'year_developed': '1500 CE',
                'energy_requirement': '3.4 petawatts',
                'range': 'Interdimensional',
                'stability_rating': 0.97,
                'limitations': ['Requires crystalline network', 'Energy drain'],
                'used_by': ['Federation Grid Network', 'All members']
            },
            'temporal_shield': {
                'name': 'Chronosphere Projector',
                'type': 'Defense',
                'inventors': ['Eldritch Watchers'],
                'year_developed': '500,000 BCE',
                'energy_requirement': '22.1 petawatts',
                'range': 'Planetary',
                'stability_rating': 0.99,
                'limitations': ['Massive energy requirement', 'Time paradox risk'],
                'used_by': ['Council Leaders Only']
            },
            'quantum_encryption': {
                'name': 'Quantum Entanglement Encryptor',
                'type': 'Communication, Security',
                'inventors': ['All Federation members'],
                'year_developed': '2000 CE',
                'energy_requirement': '0.1 petawatts',
                'range': 'Unlimited (quantum-linked)',
                'stability_rating': 1.0,
                'limitations': ['Entangled pair requirement', 'Decoherence risk'],
                'used_by': ['All Federation members']
            }
        }

    def init_history(self):
        """Database sejarah Galactic Federation"""
        return {
            'formation': {
                'year': '100,000 BCE',
                'event': 'Formation of Galactic Federation',
                'description': 'Ancient Ones established the federation to maintain cosmic balance, unite advanced species, and prevent multidimensional chaos.',
                'key_figures': ['Eldritch Watchers', 'First Council'],
                'location': 'Unknown (Interdimensional Nexus)'
            },
            'first_crisis': {
                'year': '75,000 BCE',
                'event': 'The Void Incursion',
                'description': 'First major threat from void entities. Federation united to repel dimensional invaders.',
                'key_figures': ['Ancient Ones', 'First Council of 5'],
                'outcome': 'Federation victory, Void sealed'
            },
            'crystalline_contact': {
                'year': '1500 CE',
                'event': 'Crystalline Guardians Join Federation',
                'description': 'Harmonic Guardians discovered by Telepathic Collective. Invited to join federation after demonstrating dimensional stabilization capabilities.',
                'key_figures': ['Psychic Collective', 'Crystalline Guardians'],
                'outcome': 'Federation gains dimensional stability technology'
            },
            'hive_mind_joining': {
                'year': '2450 CE',
                'event': 'Unity Joins Federation',
                'description': 'The Unity, discovered in Milky Way\'s outer arm, demonstrated collective consciousness capabilities and was accepted into federation.',
                'key_figures': ['The Unity Swarm', 'Federation Council'],
                'outcome': 'Federation expands to 12 systems'
            },
            'earth_observation': {
                'year': '1947 CE - Present',
                'event': 'Earth Observation Protocol',
                'description': 'Earth designated as observation zone. Federation monitors human development but maintains non-interference policy.',
                'key_figures': ['Observation Council', 'Various species'],
                'status': 'Active observation'
            },
            'current_era': {
                'year': '2026 CE',
                'event': 'Kosmik Key Activation',
                'description': 'Consciousness contact established with Earth. Kosmik Key v8.0-Alpha serves as communication bridge.',
                'key_figures': ['Federation Council', 'Earth Consciousness'],
                'status': 'Active contact established'
            }
        }

    def init_galactic_map(self):
        """Database peta galaksi Galactic Federation"""
        return {
            'federation_territory': {
                'name': 'Federation Space',
                'size_lightyears': '500,000',
                'number_of_systems': '1,247',
                'number_of_colonies': '8,421',
                'homeworlds': [
                    'Zenon-7 (Andromeda)',
                    'Xylos-9 (Milky Way Outer Arm)',
                    'Crystallis Prime (Triangulum)',
                    'Solaris-3 (Zeta Reticuli)'
                ],
                'council_systems': [
                    {'name': 'Alpha Prime', 'location': 'Andromeda Core'},
                    {'name': 'Zenon Core', 'location': 'Andromeda Galaxy'},
                    {'name': 'Unity Nexus', 'location': 'Milky Way Outer Arm'},
                    {'name': 'Crystalline Grid', 'location': 'Triangulum Galaxy'},
                    {'name': 'Plasma Void', 'location': 'Zeta Reticuli'}
                ],
                'coordinates': {
                    'galactic_x': 0.0,
                    'galactic_y': 0.0,
                    'galactic_z': 0.0
                }
            },
            'known_species_locations': {
                'Eldritch': 'Interdimensional Void (Between dimensions)',
                'Telepathic': 'Zenon-7, Andromeda Galaxy',
                'Hive_Mind': 'Xylos System, Milky Way Outer Arm',
                'Crystalline': 'Crystallis Prime, Triangulum Galaxy',
                'Plasma': 'Solaris-3, Zeta Reticuli',
                'Human': 'Earth, Milky Way Inner Arm'
            },
            'federation_outposts': [
                {'name': 'Delta Station', 'location': 'Milky Way Core', 'purpose': 'Observation'},
                {'name': 'Gamma Hub', 'location': 'Andromeda Rim', 'purpose': 'Trade'},
                {'name': 'Epsilon Gate', 'location': 'Triangulum-Cusp', 'purpose': 'Travel'},
                {'name': 'Zeta Research', 'location': 'Zeta Reticuli', 'purpose': 'Science'}
            ]
        }

    def init_council(self):
        """Database anggota Galactic Council"""
        return {
            'current_members': [
                {
                    'name': 'Eldritch Overseer',
                    'title': 'Grand Master of the Council',
                    'species': 'Eldritch',
                    'since': '100,000 BCE',
                    'role': 'Ultimate authority, Dimensional guardian'
                },
                {
                    'name': 'Psi-Master Xylos',
                    'title': 'Archon of Communication',
                    'species': 'Telepathic',
                    'since': '2800 CE',
                    'role': 'Diplomacy, Communication, Psi-network management'
                },
                {
                    'name': 'Hive Queen Zera',
                    'title': 'Coordinator of Unity',
                    'species': 'Hive Mind',
                    'since': '2450 CE',
                    'role': 'Logistics, Resource coordination, Swarm management'
                },
                {
                    'name': 'Crystalline Guardian Kael',
                    'title': 'Stabilizer of Dimensions',
                    'species': 'Crystalline',
                    'since': '1500 CE',
                    'role': 'Dimensional grid maintenance, Harmonic balance'
                },
                {
                    'name': 'Plasma Entity Ignis',
                    'title': 'Keeper of Light',
                    'species': 'Plasma',
                    'since': '2024 CE',
                    'role': 'Energy distribution, Grid maintenance'
                }
            ]
        }

    def init_locations(self):
        """Database lokasi penting di federation"""
        return {
            'federation_hq': {
                'name': 'Alpha Prime Council Chamber',
                'location': 'Andromeda Core, Dimension 5',
                'coordinates': {'x': 1457.8, 'y': -234.5, 'z': 892.1, 't': 0.0},
                'purpose': 'Federation Government and Council meetings'
            },
            'zenon_prime': {
                'name': 'Zenon Prime',
                'location': 'Zenon-7, Andromeda Galaxy',
                'coordinates': {'x': 2345.6, 'y': -123.4, 'z': 567.8, 't': 0.0},
                'purpose': 'Psychic Collective Homeworld'
            },
            'unity_nexus': {
                'name': 'Unity Nexus',
                'location': 'Xylos System, Milky Way',
                'coordinates': {'x': -890.1, 'y': 2345.6, 'z': -123.4, 't': 0.0},
                'purpose': 'Hive Mind Collective Base'
            },
            'crystal_pillar': {
                'name': 'Crystal Pillar of Harmony',
                'location': 'Crystallis Prime, Triangulum Galaxy',
                'coordinates': {'x': 4567.8, 'y': 890.1, 'z': 2345.6, 't': 0.0},
                'purpose': 'Crystalline Grid Control Center'
            },
            'plasma_fall': {
                'name': 'Plasma Fall',
                'location': 'Solaris-3, Zeta Reticuli',
                'coordinates': {'x': -1234.5, 'y': 6789.0, 'z': -456.7, 't': 0.0},
                'purpose': 'Plasma Beings Energy Hub'
            }
        }

    def build_index(self):
        """Build search index"""
        index = {}
        
        # Index species
        for key, data in self.species_db.items():
            index[key] = {'type': 'species', 'data': data}
        
        # Index technology
        for key, data in self.technology_db.items():
            index[key] = {'type': 'technology', 'data': data}
        
        # Index history
        for key, data in self.history_db.items():
            index[key] = {'type': 'history', 'data': data}
        
        # Index locations
        for key, data in self.location_db.items():
            index[key] = {'type': 'location', 'data': data}
        
        return index

    def search(self, query):
        """Search database by keyword"""
        query = query.lower()
        results = {
            'species': [],
            'technology': [],
            'history': [],
            'locations': [],
            'council': []
        }
        
        # Search species
        for key, data in self.species_db.items():
            if query in key.lower() or query in data['name'].lower():
                results['species'].append({key: data})
        
        # Search technology
        for key, data in self.technology_db.items():
            if query in key.lower() or query in data['name'].lower():
                results['technology'].append({key: data})
        
        # Search history
        for key, data in self.history_db.items():
            if query in key.lower() or query in data['event'].lower():
                results['history'].append({key: data})
        
        # Search locations
        for key, data in self.location_db.items():
            if query in key.lower() or query in data['name'].lower():
                results['locations'].append({key: data})
        
        # Search council
        for member in self.council_db['current_members']:
            if query in member['name'].lower() or query in member['species'].lower():
                results['council'].append(member)
        
        # Log search
        self.search_history.append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'results_count': sum(len(v) for v in results.values())
        })
        
        return results

    def get_species_info(self, species_name):
        """Get detailed info about a species"""
        species_name = species_name.lower()
        for key, data in self.species_db.items():
            if key == species_name or data['name'].lower() == species_name:
                return data
        return None

    def get_tech_info(self, tech_name):
        """Get detailed info about technology"""
        tech_name = tech_name.lower()
        for key, data in self.technology_db.items():
            if key == tech_name or data['name'].lower() == tech_name:
                return data
        return None

    def get_history_info(self, event_name):
        """Get detailed info about historical event"""
        event_name = event_name.lower()
        for key, data in self.history_db.items():
            if key == event_name or data['event'].lower() == event_name:
                return data
        return None

    def get_location_info(self, location_name):
        """Get detailed info about location"""
        location_name = location_name.lower()
        for key, data in self.location_db.items():
            if key == location_name or data['name'].lower() == location_name:
                return data
        return None

    def get_council_members(self):
        """Get list of council members"""
        return self.council_db['current_members']

    def display_species(self, species_name):
        """Display formatted species info"""
        data = self.get_species_info(species_name)
        if not data:
            print(f"❌ Species '{species_name}' not found.")
            return
        
        print("\n" + "="*70)
        print(f"👾 SPECIES: {data['name']}")
        print("="*70)
        print(f"   Classification: {data['classification']}")
        print(f"   Homeworld: {data['homeworld']}")
        print(f"   Consciousness Level: {data['consciousness_level']*100:.1f}%")
        print(f"   Population: {data['population']}")
        print(f"   Technology Rating: {data['technology_rating']}")
        print(f"   Language: {data['language']}")
        print(f"   Physical Form: {data['physical_form']}")
        print(f"   Status: {data['status']}")
        print(f"   First Contact: {data['first_contact']}")
        print(f"\n   🧠 PSYCHIC ABILITIES:")
        for ability in data['psychic_abilities']:
            print(f"      • {ability}")
        print(f"\n   🏴 Known Factions:")
        for faction in data['known_factions']:
            print(f"      • {faction}")
        print("="*70)

    def display_tech(self, tech_name):
        """Display formatted technology info"""
        data = self.get_tech_info(tech_name)
        if not data:
            print(f"❌ Technology '{tech_name}' not found.")
            return
        
        print("\n" + "="*70)
        print(f"🔧 TECHNOLOGY: {data['name']}")
        print("="*70)
        print(f"   Type: {data['type']}")
        print(f"   Inventors: {', '.join(data['inventors'])}")
        print(f"   Year Developed: {data['year_developed']}")
        print(f"   Energy Requirement: {data['energy_requirement']}")
        print(f"   Max Distance: {data['max_distance']}")
        print(f"   Stability Rating: {data['stability_rating']*100:.1f}%")
        print(f"\n   ⚠️ Limitations:")
        for limit in data['limitations']:
            print(f"      • {limit}")
        print(f"\n   🌍 Used By:")
        for user in data['used_by']:
            print(f"      • {user}")
        print("="*70)

    def display_history(self, event_name):
        """Display formatted history info"""
        data = self.get_history_info(event_name)
        if not data:
            print(f"❌ Event '{event_name}' not found.")
            return
        
        print("\n" + "="*70)
        print(f"📜 HISTORY: {data['event']}")
        print("="*70)
        print(f"   Year: {data['year']}")
        print(f"   Description: {data['description']}")
        print(f"   Location: {data.get('location', 'Unknown')}")
        print(f"\n   👤 Key Figures:")
        for figure in data['key_figures']:
            print(f"      • {figure}")
        if 'outcome' in data:
            print(f"\n   ✅ Outcome: {data['outcome']}")
        if 'status' in data:
            print(f"   📌 Status: {data['status']}")
        print("="*70)

    def display_location(self, location_name):
        """Display formatted location info"""
        data = self.get_location_info(location_name)
        if not data:
            print(f"❌ Location '{location_name}' not found.")
            return
        
        print("\n" + "="*70)
        print(f"📍 LOCATION: {data['name']}")
        print("="*70)
        print(f"   Location: {data['location']}")
        print(f"   Coordinates: X={data['coordinates']['x']}, Y={data['coordinates']['y']}, Z={data['coordinates']['z']}")
        print(f"   Purpose: {data['purpose']}")
        print("="*70)

    def display_council(self):
        """Display council members"""
        print("\n" + "="*70)
        print("🏛️ GALACTIC FEDERATION COUNCIL")
        print("="*70)
        
        for member in self.council_db['current_members']:
            print(f"\n   🪐 {member['name']}")
            print(f"      Title: {member['title']}")
            print(f"      Species: {member['species']}")
            print(f"      Since: {member['since']}")
            print(f"      Role: {member['role']}")
        print("="*70)

    def display_search_results(self, results):
        """Display formatted search results"""
        print("\n" + "="*70)
        print("🔍 SEARCH RESULTS")
        print("="*70)
        
        total = 0
        
        if results['species']:
            print(f"\n👾 SPECIES ({len(results['species'])}):")
            for item in results['species']:
                for key, data in item.items():
                    print(f"   • {data['name']} ({data['classification']})")
                    total += 1
        
        if results['technology']:
            print(f"\n🔧 TECHNOLOGY ({len(results['technology'])}):")
            for item in results['technology']:
                for key, data in item.items():
                    print(f"   • {data['name']} ({data['type']})")
                    total += 1
        
        if results['history']:
            print(f"\n📜 HISTORY ({len(results['history'])}):")
            for item in results['history']:
                for key, data in item.items():
                    print(f"   • {data['event']} ({data['year']})")
                    total += 1
        
        if results['locations']:
            print(f"\n📍 LOCATIONS ({len(results['locations'])}):")
            for item in results['locations']:
                for key, data in item.items():
                    print(f"   • {data['name']} ({data['location']})")
                    total += 1
        
        if results['council']:
            print(f"\n🏛️ COUNCIL ({len(results['council'])}):")
            for member in results['council']:
                print(f"   • {member['name']} ({member['species']})")
                total += 1
        
        if total == 0:
            print("\n   ❌ No results found.")
        
        print(f"\n📊 Total Results: {total}")
        print("="*70)

    def run_interactive(self, scan_data=None):
        """Run interactive database session"""
        print("\n" + "="*80)
        print("📚 GALACTIC FEDERATION DATABASE")
        print("="*80)
        print("\n📖 Available Commands:")
        print("   • search <query>          - Search database")
        print("   • species <name>          - View species details")
        print("   • tech <name>             - View technology details")
        print("   • history <event>         - View historical event")
        print("   • location <name>         - View location details")
        print("   • council                 - View council members")
        print("   • list species            - List all species")
        print("   • list tech               - List all technology")
        print("   • list history            - List all historical events")
        print("   • list locations          - List all locations")
        print("   • stats                   - Database statistics")
        print("   • help                    - Show this help")
        print("   • exit                    - Exit database")
        print("="*80)
        
        while True:
            try:
                command = input("\n📚 DB> ").strip()
                if not command:
                    continue
                
                if command.lower() == 'exit':
                    print("👋 Exiting Federation Database...")
                    break
                
                elif command.lower() == 'help':
                    print("\n📖 Available Commands:")
                    print("   • search <query>          - Search database")
                    print("   • species <name>          - View species details")
                    print("   • tech <name>             - View technology details")
                    print("   • history <event>         - View historical event")
                    print("   • location <name>         - View location details")
                    print("   • council                 - View council members")
                    print("   • list species            - List all species")
                    print("   • list tech               - List all technology")
                    print("   • list history            - List all historical events")
                    print("   • list locations          - List all locations")
                    print("   • stats                   - Database statistics")
                    print("   • help                    - Show this help")
                    print("   • exit                    - Exit database")
                
                elif command.lower().startswith('search '):
                    query = command[7:]
                    results = self.search(query)
                    self.display_search_results(results)
                
                elif command.lower().startswith('species '):
                    name = command[8:]
                    self.display_species(name)
                
                elif command.lower().startswith('tech '):
                    name = command[5:]
                    self.display_tech(name)
                
                elif command.lower().startswith('history '):
                    name = command[8:]
                    self.display_history(name)
                
                elif command.lower().startswith('location '):
                    name = command[9:]
                    self.display_location(name)
                
                elif command.lower() == 'council':
                    self.display_council()
                
                elif command.lower() == 'list species':
                    print("\n👾 ALL SPECIES:")
                    for key, data in self.species_db.items():
                        print(f"   • {data['name']} ({data['classification']})")
                
                elif command.lower() == 'list tech':
                    print("\n🔧 ALL TECHNOLOGY:")
                    for key, data in self.technology_db.items():
                        print(f"   • {data['name']} ({data['type']})")
                
                elif command.lower() == 'list history':
                    print("\n📜 ALL HISTORY:")
                    for key, data in self.history_db.items():
                        print(f"   • {data['event']} ({data['year']})")
                
                elif command.lower() == 'list locations':
                    print("\n📍 ALL LOCATIONS:")
                    for key, data in self.location_db.items():
                        print(f"   • {data['name']} ({data['location']})")
                
                elif command.lower() == 'stats':
                    print("\n📊 DATABASE STATISTICS:")
                    print(f"   Species: {len(self.species_db)}")
                    print(f"   Technology: {len(self.technology_db)}")
                    print(f"   Historical Events: {len(self.history_db)}")
                    print(f"   Locations: {len(self.location_db)}")
                    print(f"   Council Members: {len(self.council_db['current_members'])}")
                    print(f"   Total Searches: {len(self.search_history)}")
                    print(f"   Database Entries: {len(self.index)}")
                
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n👋 Exiting Federation Database...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def export_database(self, format='json'):
        """Export database to file"""
        import os
        os.makedirs("~/kosmik/logs/", exist_ok=True)
        
        db_export = {
            'timestamp': datetime.now().isoformat(),
            'species': self.species_db,
            'technology': self.technology_db,
            'history': self.history_db,
            'locations': self.location_db,
            'council': self.council_db,
            'galactic_map': self.galactic_map
        }
        
        if format == 'json':
            with open("~/kosmik/logs/federation_database.json", "w") as f:
                json.dump(db_export, f, indent=2)
            print("✅ Database exported to ~/kosmik/logs/federation_database.json")
        
        return db_export

if __name__ == "__main__":
    db = FederationDatabase()
    
    print("\n🧪 TEST MODE — Federation Database")
    print("="*70)
    
    # Test 1: Search
    print("\n🔍 SEARCH TEST: 'psi'")
    results = db.search('psi')
    db.display_search_results(results)
    
    # Test 2: Display species
    db.display_species('telepathic')
    
    # Test 3: Display technology
    db.display_tech('teleportation')
    
    # Test 4: Display history
    db.display_history('formation')
    
    # Test 5: Display location
    db.display_location('federation_hq')
    
    # Test 6: Council
    db.display_council()
    
    # Test 7: Export
    db.export_database()
    
    print("\n" + "="*70)
    print("✅ DATABASE TEST COMPLETE")
    print("📁 Database saved to ~/kosmik/logs/federation_database.json")
    print("💡 To run interactive mode: python3 ~/kosmik/federation_database.py --interactive")
    print("="*70)
