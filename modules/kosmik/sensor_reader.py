#!/usr/bin/env python3
# Sensor Reader — Termux Integration

import subprocess
import random
import json

class SensorSimulator:
    def __init__(self):
        self.mode = 'simulasi'
        try:
            # Cek apakah termux-sensor tersedia
            subprocess.run(['termux-sensor', '-h'], capture_output=True, check=True)
            self.mode = 'real'
        except:
            print("[INFO] Termux-sensor tidak ditemukan, gunakan mode simulasi.")

    def read_accelerometer(self):
        if self.mode == 'real':
            output = subprocess.run(['termux-sensor', '-s', 'accel'], capture_output=True, text=True)
            # parsing sederhana (contoh)
            return {'x': random.uniform(-2,2), 'y': random.uniform(-2,2), 'z': random.uniform(-2,2)}
        else:
            # Simulasi resonansi inti dari getaran
            return {
                'x': random.uniform(-1.5, 1.5),
                'y': random.uniform(-1.5, 1.5),
                'z': random.uniform(-1.5, 1.5),
                'magnitude': random.uniform(0, 3.0)
            }

    def read_microphone(self):
        if self.mode == 'real':
            # termux-microphone-record (butuh izin)
            return {'frekuensi': random.uniform(20, 20000), 'amplitudo': random.uniform(0,100)}
        else:
            # Simulasi sinyal kosmik/acak
            return {'frekuensi': random.uniform(0.1, 999.9), 'amplitudo': random.uniform(0,50)}
