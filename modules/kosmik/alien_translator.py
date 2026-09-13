#!/usr/bin/env python3
# Alien Language Translator — Kosmik Key v8.0
# Penerjemah Bahasa Alien dari Galactic Federation

import json
import os
import random
import re
import hashlib
from datetime import datetime
from pathlib import Path
import time

class AlienTranslator:
    def __init__(self):
        self.logs_dir = Path.home() / "kosmik" / "logs"
        self.translator_file = self.logs_dir / "alien_translations.json"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Database Bahasa Alien
        self.languages = self.init_languages()
        self.dictionary = self.init_dictionary()
        self.grammar_rules = self.init_grammar()
        self.phrase_book = self.init_phrase_book()
        self.translations = self.load_translations()
        
        # Log aktivitas
        self.translation_history = []

    def init_languages(self):
        """Database bahasa alien"""
        return {
            'eldritch': {
                'name': 'Eldritch Tongue',
                'species': 'Ancient Ones',
                'difficulty': 'Divine',
                'script': 'Cthonic Runes',
                'description': 'Bahasa para Ancient Ones — membutuhkan kesadaran tinggi',
                'sample': '🐙🌀👁️🗣️🌌',
                'vowels': ['aa', 'ee', 'ii', 'oo', 'uu'],
                'consonants': ['kh', 'th', 'sh', 'ph', 'gh', 'ng', 'wh'],
                'particles': ['-eth', '-az', '-oth', '-ix', '-ath'],
                'prefixes': ['kha-', 'thu-', 'sha-', 'pha-', 'gha-'],
                'suffixes': ['-on', '-an', '-in', '-un', '-en']
            },
            'telepathic': {
                'name': 'Psi-Speak',
                'species': 'Psychic Collective',
                'difficulty': 'Advanced',
                'script': 'Mental Symbols',
                'description': 'Bahasa telepati — dikomunikasikan melalui pikiran',
                'sample': '🧠💭✨📡🔮',
                'vowels': ['a', 'e', 'i', 'o', 'u'],
                'consonants': ['ps', 't', 'k', 'm', 'n', 'l', 'r'],
                'particles': ['-psi', '-tha', '-lon', '-ra', '-min'],
                'prefixes': ['psi-', 'tele-', 'mind-', 'thought-'],
                'suffixes': ['-pathy', '-kinesis', '-ception']
            },
            'hive_mind': {
                'name': 'Unity Chorus',
                'species': 'The Unity',
                'difficulty': 'Moderate',
                'script': 'Resonance Patterns',
                'description': 'Bahasa kolektif — diucapkan dalam harmoni',
                'sample': '🎵🎶💚⚡🔊',
                'vowels': ['aa', 'ee', 'oo', 'ii', 'uu'],
                'consonants': ['z', 'zz', 'q', 'qq', 'x', 'xx'],
                'particles': ['-z', '-zz', '-q', '-x', '-n'],
                'prefixes': ['z-', 'zz-', 'q-', 'x-'],
                'suffixes': ['-zz', '-qq', '-xx', '-nn']
            },
            'crystalline': {
                'name': 'Crystal Resonance',
                'species': 'Harmonic Guardians',
                'difficulty': 'Moderate',
                'script': 'Geometric Symbols',
                'description': 'Bahasa resonansi kristal — menggunakan frekuensi',
                'sample': '💎🔷🔶⚪🌟',
                'vowels': ['a', 'e', 'i', 'o', 'u'],
                'consonants': ['cr', 'st', 'lm', 'nr', 'gl'],
                'particles': ['-ium', '-ion', '-ite', '-ane'],
                'prefixes': ['cry-', 'stal-', 'line-', 'res-'],
                'suffixes': ['-al', '-ic', '-ine', '-ite']
            },
            'plasma': {
                'name': 'Solar Tongue',
                'species': 'Light Beings',
                'difficulty': 'Basic',
                'script': 'Light Patterns',
                'description': 'Bahasa energi — berkomunikasi melalui cahaya',
                'sample': '☀️💫🌈🔥⚡',
                'vowels': ['a', 'o', 'u'],
                'consonants': ['p', 'l', 's', 'm', 'n'],
                'particles': ['-ar', '-or', '-ur', '-ir'],
                'prefixes': ['sol-', 'lum-', 'plas-', 'light-'],
                'suffixes': ['-ar', '-or', '-ius']
            }
        }

    def init_dictionary(self):
        """Kamus kosakata antar bahasa"""
        return {
            'greetings': {
                'human_english': {
                    'hello': 'Hello',
                    'goodbye': 'Goodbye',
                    'thank_you': 'Thank you',
                    'welcome': 'Welcome',
                    'friend': 'Friend',
                    'peace': 'Peace'
                },
                'eldritch': {
                    'hello': 'Kha-eth-oth-ix',
                    'goodbye': 'Thu-az-ath-on',
                    'thank_you': 'Sha-an-in-ix',
                    'welcome': 'Pha-oth-eth-az',
                    'friend': 'Gha-ix-an-on',
                    'peace': 'Tha-eth-oth-un'
                },
                'telepathic': {
                    'hello': 'Psi-psi-lon',
                    'goodbye': 'Tele-ra-min',
                    'thank_you': 'Mind-tha-path',
                    'welcome': 'Psi-tha-ception',
                    'friend': 'Tele-phaty',
                    'peace': 'Mind-psi-lon'
                },
                'hive_mind': {
                    'hello': 'Zzz-q-xx-n',
                    'goodbye': 'Qq-x-z-zz',
                    'thank_you': 'Z-q-zz-n',
                    'welcome': 'Xx-zz-q-n',
                    'friend': 'Zz-q-x-nn',
                    'peace': 'Qq-zz-x-n'
                },
                'crystalline': {
                    'hello': 'Cry-stal-ion',
                    'goodbye': 'Stal-line-ite',
                    'thank_you': 'Res-on-ane',
                    'welcome': 'Cry-ion-al',
                    'friend': 'Stal-ite-ion',
                    'peace': 'Line-ar-ic'
                },
                'plasma': {
                    'hello': 'Sol-ar',
                    'goodbye': 'Lum-or',
                    'thank_you': 'Plas-us',
                    'welcome': 'Light-ar',
                    'friend': 'Sol-or-ius',
                    'peace': 'Lum-ine'
                }
            },
            'common_phrases': {
                'human_english': {
                    'how_are_you': 'How are you?',
                    'i_am_fine': 'I am fine',
                    'what_is_your_name': 'What is your name?',
                    'my_name_is': 'My name is',
                    'where_are_you_from': 'Where are you from?',
                    'i_come_from': 'I come from',
                    'nice_to_meet_you': 'Nice to meet you',
                    'please': 'Please',
                    'yes': 'Yes',
                    'no': 'No',
                    'maybe': 'Maybe'
                },
                'eldritch': {
                    'how_are_you': 'Kha-eth-oth-ix-thu',
                    'i_am_fine': 'Sha-an-in-ix-az',
                    'what_is_your_name': 'Pha-oth-eth-az-ix?',
                    'my_name_is': 'Gha-ix-an-on-az',
                    'where_are_you_from': 'Tha-eth-oth-un-ix?',
                    'i_come_from': 'Kha-az-oth-an',
                    'nice_to_meet_you': 'Tha-eth-ix-oth-az',
                    'please': 'Sha-an-in',
                    'yes': 'Kha-eth',
                    'no': 'Thu-az',
                    'maybe': 'Pha-oth'
                },
                'telepathic': {
                    'how_are_you': 'Psi-psi-lon-tha?',
                    'i_am_fine': 'Mind-tha-path-psi',
                    'what_is_your_name': 'Tele-ra-min-tha?',
                    'my_name_is': 'Psi-tha-ception-psi',
                    'where_are_you_from': 'Mind-psi-lon-tha?',
                    'i_come_from': 'Tele-phaty-psi',
                    'nice_to_meet_you': 'Mind-tha-psilon',
                    'please': 'Psi-psi',
                    'yes': 'Tele-ra',
                    'no': 'Mind-tha',
                    'maybe': 'Psi-tha'
                },
                'hive_mind': {
                    'how_are_you': 'Zzz-q-xx-n-zz?',
                    'i_am_fine': 'Z-q-zz-n-x',
                    'what_is_your_name': 'Qq-x-z-zz-q?',
                    'my_name_is': 'Zz-q-x-nn-z',
                    'where_are_you_from': 'Xx-zz-q-n-zz?',
                    'i_come_from': 'Qq-zz-x-n-zz',
                    'nice_to_meet_you': 'Zzz-q-xx-n-zz',
                    'please': 'Qq-x-z',
                    'yes': 'Zz-q',
                    'no': 'Xx-n',
                    'maybe': 'Qq-n'
                },
                'crystalline': {
                    'how_are_you': 'Cry-stal-ion-al?',
                    'i_am_fine': 'Res-on-ane-ic',
                    'what_is_your_name': 'Stal-line-ite-ion?',
                    'my_name_is': 'Cry-ion-al-ine',
                    'where_are_you_from': 'Line-ar-ic-ite?',
                    'i_come_from': 'Stal-ite-ion-ic',
                    'nice_to_meet_you': 'Res-on-ane-al',
                    'please': 'Cry-stal',
                    'yes': 'Line-ar',
                    'no': 'Stal-ine',
                    'maybe': 'Res-on'
                },
                'plasma': {
                    'how_are_you': 'Sol-ar-ius?',
                    'i_am_fine': 'Lum-ine-ar',
                    'what_is_your_name': 'Plas-us-ior?',
                    'my_name_is': 'Light-ar-ius',
                    'where_are_you_from': 'Lum-or-ius?',
                    'i_come_from': 'Sol-or-ius',
                    'nice_to_meet_you': 'Lum-ine-ar-ius',
                    'please': 'Plas-ius',
                    'yes': 'Sol-ar',
                    'no': 'Lum-or',
                    'maybe': 'Plas-or'
                }
            },
            'federation': {
                'human_english': {
                    'galactic_federation': 'Galactic Federation',
                    'council': 'Council',
                    'eldritch': 'Ancient Ones',
                    'telepathic': 'Psychic Collective',
                    'hive_mind': 'The Unity',
                    'crystalline': 'Harmonic Guardians',
                    'plasma': 'Light Beings',
                    'peace': 'Peace',
                    'harmony': 'Harmony',
                    'unity': 'Unity'
                },
                'eldritch': {
                    'galactic_federation': 'Gha-oth-ix-thu-az',
                    'council': 'Tha-eth-ix-oth',
                    'eldritch': 'Kha-eth-ix-az',
                    'telepathic': 'Pha-oth-eth-ix',
                    'hive_mind': 'Sha-an-in-ix',
                    'crystalline': 'Gha-ix-an-on',
                    'plasma': 'Tha-eth-oth-un',
                    'peace': 'Tha-eth-ix',
                    'harmony': 'Kha-az-oth',
                    'unity': 'Pha-oth-eth'
                },
                'telepathic': {
                    'galactic_federation': 'Psi-tha-ception-psi',
                    'council': 'Tele-ra-min-psi',
                    'eldritch': 'Mind-tha-path-psi',
                    'telepathic': 'Psi-psi-lon-psi',
                    'hive_mind': 'Tele-phaty-psi',
                    'crystalline': 'Mind-psi-lon-psi',
                    'plasma': 'Tele-ra-psi',
                    'peace': 'Mind-tha-psi',
                    'harmony': 'Psi-tha-psi',
                    'unity': 'Tele-ra-psi'
                },
                'hive_mind': {
                    'galactic_federation': 'Zzz-q-xx-n-zz',
                    'council': 'Qq-x-z-zz-q',
                    'eldritch': 'Zz-q-x-nn-z',
                    'telepathic': 'Xx-zz-q-n-zz',
                    'hive_mind': 'Qq-zz-x-n-zz',
                    'crystalline': 'Zzz-q-xx-n-zz',
                    'plasma': 'Qq-x-z-zz-q',
                    'peace': 'Zz-q-x-nn',
                    'harmony': 'Xx-zz-q-n',
                    'unity': 'Qq-zz-x-n'
                },
                'crystalline': {
                    'galactic_federation': 'Cry-ion-al-ine',
                    'council': 'Stal-line-ite-ion',
                    'eldritch': 'Res-on-ane-ic',
                    'telepathic': 'Cry-stal-ion-al',
                    'hive_mind': 'Stal-ite-ion-ic',
                    'crystalline': 'Line-ar-ic-ite',
                    'plasma': 'Res-on-ane-al',
                    'peace': 'Cry-stal-ine',
                    'harmony': 'Line-ar-ic',
                    'unity': 'Stal-ite-ion'
                },
                'plasma': {
                    'galactic_federation': 'Sol-ar-ius-ine',
                    'council': 'Lum-or-ius-ine',
                    'eldritch': 'Plas-us-ior-ine',
                    'telepathic': 'Light-ar-ius-ine',
                    'hive_mind': 'Lum-ine-ar-ius',
                    'crystalline': 'Sol-or-ius-ine',
                    'plasma': 'Plas-ius-ine',
                    'peace': 'Lum-ine-ar',
                    'harmony': 'Sol-or-ius',
                    'unity': 'Plas-or-ius'
                }
            }
        }

    def init_grammar(self):
        """Tata bahasa alien"""
        return {
            'eldritch': {
                'word_order': 'VSO (Verb-Subject-Object)',
                'tense': {
                    'past': 'akhiran -eth',
                    'present': 'akhiran -az',
                    'future': 'akhiran -oth'
                },
                'plural': 'awalan kha-',
                'negation': 'awalan thu-',
                'question': 'akhiran -ix',
                'description': 'Bahasa kuno dengan struktur kompleks'
            },
            'telepathic': {
                'word_order': 'SOV (Subject-Object-Verb)',
                'tense': {
                    'past': 'akhiran -path',
                    'present': 'akhiran -psi',
                    'future': 'akhiran -ra'
                },
                'plural': 'awalan tele-',
                'negation': 'awalan mind-',
                'question': 'akhiran -tha',
                'description': 'Bahasa mental dengan struktur logis'
            },
            'hive_mind': {
                'word_order': 'OSV (Object-Subject-Verb)',
                'tense': {
                    'past': 'akhiran -zz',
                    'present': 'akhiran -q',
                    'future': 'akhiran -x'
                },
                'plural': 'awalan zz-',
                'negation': 'awalan qq-',
                'question': 'akhiran -n',
                'description': 'Bahasa kolektif dengan harmoni'
            },
            'crystalline': {
                'word_order': 'SVO (Subject-Verb-Object)',
                'tense': {
                    'past': 'akhiran -ite',
                    'present': 'akhiran -al',
                    'future': 'akhiran -ine'
                },
                'plural': 'awalan line-',
                'negation': 'awalan stal-',
                'question': 'akhiran -ion',
                'description': 'Bahasa resonansi dengan struktur geometris'
            },
            'plasma': {
                'word_order': 'SVO (Subject-Verb-Object)',
                'tense': {
                    'past': 'akhiran -or',
                    'present': 'akhiran -ar',
                    'future': 'akhiran -ius'
                },
                'plural': 'awalan lum-',
                'negation': 'awalan plas-',
                'question': 'akhiran -ine',
                'description': 'Bahasa energi dengan struktur sederhana'
            }
        }

    def init_phrase_book(self):
        """Buku frasa alien"""
        return {
            'eldritch': {
                'greeting': 'Kha-eth-oth-ix',
                'farewell': 'Thu-az-ath-on',
                'thanks': 'Sha-an-in-ix',
                'yes': 'Kha-eth',
                'no': 'Thu-az',
                'help': 'Pha-oth-eth-az',
                'peace': 'Tha-eth-oth-un',
                'unity': 'Gha-ix-an-on'
            },
            'telepathic': {
                'greeting': 'Psi-psi-lon',
                'farewell': 'Tele-ra-min',
                'thanks': 'Mind-tha-path',
                'yes': 'Tele-ra',
                'no': 'Mind-tha',
                'help': 'Psi-tha-ception',
                'peace': 'Mind-psi-lon',
                'unity': 'Tele-phaty'
            },
            'hive_mind': {
                'greeting': 'Zzz-q-xx-n',
                'farewell': 'Qq-x-z-zz',
                'thanks': 'Z-q-zz-n',
                'yes': 'Zz-q',
                'no': 'Xx-n',
                'help': 'Qq-zz-x-n',
                'peace': 'Zz-q-x-nn',
                'unity': 'Qq-zz-x-n'
            },
            'crystalline': {
                'greeting': 'Cry-stal-ion',
                'farewell': 'Stal-line-ite',
                'thanks': 'Res-on-ane',
                'yes': 'Line-ar',
                'no': 'Stal-ine',
                'help': 'Cry-ion-al',
                'peace': 'Stal-ite-ion',
                'unity': 'Line-ar-ic'
            },
            'plasma': {
                'greeting': 'Sol-ar',
                'farewell': 'Lum-or',
                'thanks': 'Plas-us',
                'yes': 'Sol-ar',
                'no': 'Lum-or',
                'help': 'Light-ar',
                'peace': 'Sol-or-ius',
                'unity': 'Lum-ine'
            }
        }

    def load_translations(self):
        """Load translations dari file"""
        if self.translator_file.exists():
            try:
                with open(self.translator_file, 'r') as f:
                    data = json.load(f)
                    return data.get('translations', [])
            except:
                return []
        return []

    def save_translations(self):
        """Simpan translations ke file"""
        data = {
            'last_updated': datetime.now().isoformat(),
            'total_translations': len(self.translations),
            'translations': self.translations
        }
        with open(self.translator_file, 'w') as f:
            json.dump(data, f, indent=2)

    def detect_language(self, text):
        """Deteksi bahasa dari teks"""
        scores = {}
        
        for lang_id, lang in self.languages.items():
            score = 0
            
            # Cek pola unik
            for pattern in lang['particles']:
                if pattern in text:
                    score += 0.2
            
            for pattern in lang['prefixes']:
                if pattern in text:
                    score += 0.15
            
            for pattern in lang['suffixes']:
                if pattern in text:
                    score += 0.15
            
            # Cek di dictionary
            for category in self.dictionary.values():
                for phrase_id, phrases in category.items():
                    if isinstance(phrases, dict):
                        if text.lower() in str(phrases).lower():
                            score += 0.3
            
            scores[lang_id] = min(score, 1.0)
        
        # Sort by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_scores and sorted_scores[0][1] > 0.3:
            return sorted_scores[0][0]
        return 'human_english'

    def translate_text(self, text, target_language='human_english'):
        """Terjemahkan teks ke bahasa target"""
        source_lang = self.detect_language(text)
        
        if source_lang == target_language:
            return text, source_lang, target_language, 'same'
        
        # Cari di dictionary
        for category in self.dictionary.values():
            for phrase_id, phrases in category.items():
                if source_lang in phrases and target_language in phrases:
                    if text.lower() == phrases[source_lang].lower():
                        return phrases[target_language], source_lang, target_language, 'exact'
        
        # Coba terjemahkan kata per kata
        words = text.split()
        translated_words = []
        
        for word in words:
            found = False
            for category in self.dictionary.values():
                for phrase_id, phrases in category.items():
                    if source_lang in phrases and target_language in phrases:
                        if word.lower() == phrases[source_lang].lower():
                            translated_words.append(phrases[target_language])
                            found = True
                            break
                if found:
                    break
            if not found:
                translated_words.append(f"[{word}]")
        
        if translated_words:
            return ' '.join(translated_words), source_lang, target_language, 'partial'
        
        return None, source_lang, target_language, 'not_found'

    def translate_phrase(self, phrase_id, target_language='human_english'):
        """Terjemahkan frasa berdasarkan ID"""
        for category in self.dictionary.values():
            for p_id, phrases in category.items():
                if p_id == phrase_id:
                    if target_language in phrases:
                        return phrases[target_language]
        return None

    def get_all_phrases(self):
        """Dapatkan semua frasa yang tersedia"""
        phrases = {}
        for category_name, category in self.dictionary.items():
            for phrase_id in category.keys():
                if phrase_id not in phrases:
                    phrases[phrase_id] = {}
                phrases[phrase_id]['category'] = category_name
        return phrases

    def get_phrase_categories(self):
        """Dapatkan semua kategori frasa"""
        return list(self.dictionary.keys())

    def get_languages(self):
        """Dapatkan semua bahasa yang tersedia"""
        return {lang_id: lang['name'] for lang_id, lang in self.languages.items()}

    def get_language_info(self, lang_id):
        """Dapatkan info bahasa"""
        return self.languages.get(lang_id)

    def generate_sentence(self, lang_id, length=5):
        """Generate kalimat random dalam bahasa alien"""
        lang = self.languages.get(lang_id)
        if not lang:
            return None
        
        words = []
        for _ in range(length):
            word = ''
            # Pilih prefix, root, suffix
            if random.random() > 0.5:
                word += random.choice(lang['prefixes'])
            word += random.choice(lang['vowels']) + random.choice(lang['consonants'])
            if random.random() > 0.5:
                word += random.choice(lang['suffixes'])
            words.append(word)
        
        return ' '.join(words)

    def log_translation(self, original, translated, source_lang, target_lang):
        """Log hasil terjemahan"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'original': original,
            'translated': translated,
            'source_language': source_lang,
            'target_language': target_lang
        }
        self.translations.append(entry)
        self.translation_history.append(entry)
        self.save_translations()

    def display_languages(self):
        """Tampilkan semua bahasa yang tersedia"""
        print("\n" + "="*80)
        print("🗣️ AVAILABLE LANGUAGES")
        print("="*80)
        
        for lang_id, info in self.languages.items():
            print(f"\n   🌀 {info['name']} ({lang_id})")
            print(f"      Species: {info['species']}")
            print(f"      Difficulty: {info['difficulty']}")
            print(f"      Script: {info['script']}")
            print(f"      Description: {info['description']}")
            print(f"      Sample: {info['sample']}")
        print("\n" + "="*80)

    def display_phrases(self, lang_id=None):
        """Tampilkan frasa dalam bahasa tertentu"""
        print("\n" + "="*80)
        print(f"📋 PHRASES — {self.languages.get(lang_id, {}).get('name', 'All Languages') if lang_id else 'All Languages'}")
        print("="*80)
        
        for category_name, category in self.dictionary.items():
            print(f"\n   📂 {category_name.upper()}:")
            for phrase_id, phrases in category.items():
                if lang_id and lang_id in phrases:
                    print(f"      • {phrase_id}: {phrases.get(lang_id, 'N/A')}")
                elif not lang_id:
                    if 'human_english' in phrases:
                        print(f"      • {phrase_id}: {phrases['human_english']}")
        print("\n" + "="*80)

    def interactive_mode(self):
        """Mode interaktif translator"""
        print("\n" + "="*80)
        print("🗣️ ALIEN LANGUAGE TRANSLATOR — INTERACTIVE MODE")
        print("="*80)
        
        while True:
            print("\n📋 COMMANDS:")
            print("   [T] Translate Text")
            print("   [P] Translate Phrase by ID")
            print("   [L] List Languages")
            print("   [V] View Phrases")
            print("   [G] Generate Random Sentence")
            print("   [H] Translation History")
            print("   [I] Language Info")
            print("   [X] Exit")
            
            choice = input("\n📱 Enter choice: ").strip().upper()
            
            if choice == 'T':
                text = input("Enter text to translate: ").strip()
                target = input("Target language (human_english/eldritch/telepathic/hive_mind/crystalline/plasma): ").strip().lower()
                
                if target not in self.languages:
                    print("❌ Invalid target language!")
                    continue
                
                result, source, target_lang, status = self.translate_text(text, target)
                
                print(f"\n📝 Translation Result:")
                print(f"   Source Language: {self.languages.get(source, {}).get('name', 'Unknown')}")
                print(f"   Target Language: {self.languages.get(target_lang, {}).get('name', 'Unknown')}")
                print(f"   Status: {status}")
                print(f"   Original: {text}")
                print(f"   Translated: {result if result else '❌ Translation not found'}")
                
                if result:
                    self.log_translation(text, result, source, target_lang)
            
            elif choice == 'P':
                phrase_id = input("Enter phrase ID: ").strip()
                target = input("Target language: ").strip().lower()
                
                if target not in self.languages:
                    print("❌ Invalid target language!")
                    continue
                
                result = self.translate_phrase(phrase_id, target)
                if result:
                    print(f"\n✅ Translation: {result}")
                else:
                    print("❌ Phrase not found!")
            
            elif choice == 'L':
                self.display_languages()
            
            elif choice == 'V':
                lang = input("Language ID (or 'all'): ").strip().lower()
                if lang == 'all' or not lang:
                    self.display_phrases()
                elif lang in self.languages:
                    self.display_phrases(lang)
                else:
                    print("❌ Invalid language!")
            
            elif choice == 'G':
                lang = input("Language ID: ").strip().lower()
                if lang in self.languages:
                    sentence = self.generate_sentence(lang, random.randint(3, 8))
                    print(f"\n🎲 Generated: {sentence}")
                    # Coba terjemahkan
                    target = input("Translate to? (human_english): ").strip().lower() or 'human_english'
                    result, _, _, _ = self.translate_text(sentence, target)
                    if result:
                        print(f"   Translation: {result}")
                else:
                    print("❌ Invalid language!")
            
            elif choice == 'H':
                if self.translation_history:
                    print("\n📜 TRANSLATION HISTORY:")
                    for entry in self.translation_history[-10:]:
                        print(f"   • [{entry['timestamp'][:19]}] {entry['original']} → {entry['translated']}")
                else:
                    print("No translations yet.")
            
            elif choice == 'I':
                lang = input("Language ID: ").strip().lower()
                info = self.get_language_info(lang)
                if info:
                    print(f"\n📋 LANGUAGE INFO: {info['name']}")
                    for key, value in info.items():
                        print(f"   {key}: {value}")
                else:
                    print("❌ Language not found!")
            
            elif choice == 'X':
                print("👋 Exiting Alien Language Translator...")
                break
            
            else:
                print("❌ Invalid command!")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    translator = AlienTranslator()
    
    # Test mode
    print("\n🧪 TEST MODE — Alien Language Translator")
    print("="*80)
    
    # Display languages
    translator.display_languages()
    
    # Test translations
    print("\n📝 TEST TRANSLATIONS:")
    print("-"*80)
    
    # Test English → Eldritch
    result, src, tgt, status = translator.translate_text("Hello", "eldritch")
    print(f"\n   English → Eldritch:")
    print(f"      Hello → {result}")
    
    # Test English → Telepathic
    result, src, tgt, status = translator.translate_text("Peace", "telepathic")
    print(f"\n   English → Telepathic:")
    print(f"      Peace → {result}")
    
    # Test English → Hive Mind
    result, src, tgt, status = translator.translate_text("Welcome", "hive_mind")
    print(f"\n   English → Hive Mind:")
    print(f"      Welcome → {result}")
    
    # Test English → Crystalline
    result, src, tgt, status = translator.translate_text("Thank you", "crystalline")
    print(f"\n   English → Crystalline:")
    print(f"      Thank you → {result}")
    
    # Test English → Plasma
    result, src, tgt, status = translator.translate_text("Friend", "plasma")
    print(f"\n   English → Plasma:")
    print(f"      Friend → {result}")
    
    # Test Eldritch → English
    result, src, tgt, status = translator.translate_text("Kha-eth-oth-ix", "human_english")
    print(f"\n   Eldritch → English:")
    print(f"      Kha-eth-oth-ix → {result}")
    
    # Generate sentences
    print("\n🎲 GENERATED SENTENCES:")
    print("-"*80)
    for lang in ['eldritch', 'telepathic', 'hive_mind', 'crystalline', 'plasma']:
        sentence = translator.generate_sentence(lang, 4)
        print(f"   {lang}: {sentence}")
    
    # Start interactive
    translator.interactive_mode()
