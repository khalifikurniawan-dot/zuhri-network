from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import QLabel
import subprocess
import os

class KosmikApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.label = QLabel(text="Status: Siap Menjalankan Kosmik", font_size=18)
        
        btn = Button(text="Jalankan launch.sh", font_size=20, size_hint=(1, 0.4))
        btn.bind(on_press=self.run_script)
        
        layout.add_widget(self.label)
        layout.add_widget(btn)
        return layout

    def run_script(self, instance):
        try:
            script_path = os.path.expanduser("~/kosmik/launch.sh")
            subprocess.Popen(["bash", script_path])
            self.label.text = "Berhasil Memicu launch.sh!"
        except Exception as e:
            self.label.text = f"Gagal: {str(e)}"

if __name__ == '__main__':
    KosmikApp().run()
