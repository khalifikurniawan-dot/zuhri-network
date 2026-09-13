#!/usr/bin/env python3
# Alert System — Kosmik Key v8.0

import time
import json
from datetime import datetime

class AnomalyAlert:
    def __init__(self):
        self.thresholds = {
            'sinyal_kosmik': 8.5,
            'distorsi_magnetik': 'kritis',
            'resonansi_inti': 8.0,
            'celah_interdimensional': 2.5,
            'decoherence_rate': 0.4
        }
        self.log = []

    def check(self, data, category):
        alerts = []
        for key, value in data.items():
            if key in self.thresholds:
                threshold = self.thresholds[key]
                if isinstance(threshold, (int, float)):
                    if value > threshold:
                        alerts.append(f"[⚠️] {key}: {value} melewati batas {threshold}")
                elif isinstance(threshold, str):
                    if value == threshold:
                        alerts.append(f"[🚨] {key}: {value} — status kritis!")

        if alerts:
            alert_entry = {
                'timestamp': datetime.now().isoformat(),
                'category': category,
                'alerts': alerts
            }
            self.log.append(alert_entry)
            print("\n🔴 ALERT DETEKSI:")
            for a in alerts:
                print(a)
            print(f"📁 Log tersimpan di ~/kosmik/logs/\n")
            return True
        return False

    def save_log(self):
        import os
        os.makedirs("~/kosmik/logs/", exist_ok=True)
        with open("~/kosmik/logs/anomaly.log", "a") as f:
            for entry in self.log[-5:]:  # simpan 5 terakhir
                f.write(json.dumps(entry) + "\n")
