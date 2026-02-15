# main.py (VERSI FINAL DENGAN SUARA & NYAWA)
import random
import os
import sys
import traceback
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.storage.jsonstore import JsonStore
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.core.audio import SoundLoader

# Konfigurasi Warna Background (Dark Blue-Grey)
Window.clearcolor = (0.1, 0.12, 0.2, 1)

kv_string = '''
#:import SlideTransition kivy.uix.screenmanager.SlideTransition

# Template Tombol Custom
<RoundedButton@Button>:
    background_color: 0,0,0,0  
    bg_color: 0.2, 0.6, 1, 1
    canvas.before:
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15,]
    font_size: '20sp'
    bold: True
    color: 1, 1, 1, 1

ScreenManager:
    transition: SlideTransition()
    GradeScreen:
    MenuScreen:
    GameScreen:

<GradeScreen>:
    name: 'grade'
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 20

        Label:
            text: "MATH MASTER"
            font_size: '42sp'
            bold: True
            color: 1, 0.8, 0, 1
            size_hint: 1, 0.25

        Label:
            text: "PILIH KELAS"
            font_size: '18sp'
            color: 0.8, 0.8, 0.8, 1
            size_hint: 1, 0.1

        RoundedButton:
            id: btn_resume
            text: "LANJUTKAN GAME"
            bg_color: 0.3, 0.3, 0.3, 1
            on_release: app.load_game()
            disabled: True

        RoundedButton:
            text: "KELAS 3 SD"
            bg_color: 0.2, 0.7, 0.3, 1
            on_release:
                app.play_sound('click')
                app.set_grade(3)
                root.manager.transition.direction = 'left'
                root.manager.current = 'menu'

        RoundedButton:
            text: "KELAS 5 SD"
            bg_color: 0.9, 0.5, 0.1, 1
            on_release:
                app.play_sound('click')
                app.set_grade(5)
                root.manager.transition.direction = 'left'
                root.manager.current = 'menu'

        RoundedButton:
            text: "KELAS 8 SMP"
            bg_color: 0.8, 0.2, 0.2, 1
            on_release:
                app.play_sound('click')
                app.set_grade(8)
                root.manager.transition.direction = 'left'
                root.manager.current = 'menu'

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 20

        Label:
            text: app.grade_title
            font_size: '22sp'
            bold: True
            color: 0.5, 0.8, 1, 1
            size_hint: 1, 0.15

        Label:
            text: "Pilih Operasi"
            font_size: '18sp'
            size_hint: 1, 0.1

        GridLayout:
            cols: 2
            spacing: 20
            size_hint: 1, 0.6

            RoundedButton:
                text: "Tambah (+)"
                bg_color: 0.2, 0.6, 0.8, 1
                on_release:
                    app.play_sound('click')
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('tambah')

            RoundedButton:
                text: "Kurang (-)"
                bg_color: 0.2, 0.6, 0.8, 1
                on_release:
                    app.play_sound('click')
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('kurang')

            RoundedButton:
                text: "Kali (x)"
                bg_color: 0.7, 0.3, 0.6, 1
                on_release:
                    app.play_sound('click')
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('kali')

            RoundedButton:
                text: "Bagi (:)"
                bg_color: 0.7, 0.3, 0.6, 1
                on_release:
                    app.play_sound('click')
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('bagi')

        RoundedButton:
            text: "<< Kembali"
            bg_color: 0.4, 0.4, 0.4, 1
            size_hint: 1, 0.15
            on_release: 
                app.play_sound('click')
                root.manager.transition.direction = 'right'
                root.manager.current = 'grade'

<GameScreen>:
    name: 'game'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        # --- HEADER INFO ---
        GridLayout:
            cols: 3
            size_hint: 1, 0.12
            
            # Level Box
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: root.level_text
                    font_size: '16sp'
                    color: 1, 1, 0, 1
                Label:
                    text: root.lives_text
                    font_size: '14sp'
                    color: 1, 0.3, 0.3, 1
                    bold: True

            # Timer Box (Tengah)
            Label:
                text: root.timer_text
                font_size: '30sp'
                bold: True
                color: (1, 0.2, 0.2, 1) if int(root.timer_text) <= 5 else (1, 1, 1, 1)

            # Score Box
            Label:
                text: root.score_text
                font_size: '16sp'
                color: 0, 1, 0.5, 1

        Label:
            text: root.status_text
            size_hint: 1, 0.05
            font_size: '14sp'
            color: 0.6, 0.6, 0.6, 1

        # --- SOAL ---
        Label:
            text: root.question_text
            font_size: '50sp'
            bold: True
            size_hint: 1, 0.35
            color: 1, 1, 1, 1

        # --- GRID JAWABAN ---
        GridLayout:
            id: answer_grid
            cols: 2
            spacing: 15
            padding: [10, 10, 10, 10]
            size_hint: 1, 0.45

        RoundedButton:
            text: "Keluar"
            size_hint: 1, 0.1
            bg_color: 0.6, 0.2, 0.2, 1
            on_release: 
                app.play_sound('click')
                root.quit_game()
'''

# ---------- Helper Logging ----------
def write_local_log(msg):
    try:
        app = App.get_running_app()
        if app:
            data_dir = getattr(app, 'user_data_dir', None) or app.user_data_dir
        else:
            data_dir = os.path.expanduser('~')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
        log_path = os.path.join(data_dir, 'app_debug.log')
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
    except Exception:
        pass

def log_exception(exc: Exception, where: str = ''):
    tb = traceback.format_exc()
    write_local_log(f"ERR {where}: {exc}\n{tb}")

# ---------- Custom Widgets ----------
class RoundedButton(Button):
    bg_color = ListProperty([0.2, 0.6, 1, 1])

# ---------- Screens ----------
class GradeScreen(Screen):
    def on_enter(self):
        # Cek apakah ada save data
        try:
            app = App.get_running_app()
            if getattr(app, 'store', None) and app.store.exists('math_data'):
                data = app.store.get('math_data')
                btn = self.ids.get('btn_resume', None)
                if btn:
                    btn.disabled = False
                    # Update teks tombol agar user tahu level mana
                    btn.text = f"LANJUT: Level {data.get('level', 1)} ({data.get('mode', 'Game').upper()})"
                    btn.bg_color = (0.2, 0.6, 0.2, 1)
            else:
                btn = self.ids.get('btn_resume', None)
                if btn:
                    btn.disabled = True
                    btn.bg_color = (0.3, 0.3, 0.3, 1)
        except Exception as e:
            log_exception(e, 'GradeScreen.on_enter')

class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    level_text = StringProperty("Level: 1")
    lives_text = StringProperty("Nyawa: 3")
    timer_text = StringProperty("20")
    score_text = StringProperty("0")
    status_text = StringProperty("Soal 1/10")
    question_text = StringProperty("Siap?")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons = []
        
        # Game State
        self.level = 1
        self.total_score = 0
        self.question_num = 1
        self.lives = 3         # Default 3 nyawa (max 2 salah)
        self.mistakes_in_level = 0
        
        self.time_left = 20
        self.correct_answer = 0
        self.timer_event = None
        self.game_active = False 
        Clock.schedule_once(self.setup_buttons)

    def setup_buttons(self, dt):
        try:
            if 'answer_grid' not in self.ids:
                Clock.schedule_once(self.setup_buttons, 0.1)
                return
            grid = self.ids.answer_grid
            grid.clear_widgets()
            self.buttons = []
            for _ in range(4):
                btn = RoundedButton(text="", font_size='28sp')
                btn.bind(on_release=self.check_answer_anim)
                self.buttons.append(btn)
                grid.add_widget(btn)
        except Exception as e:
            log_exception(e, 'GameScreen.setup_buttons')

    def start_game(self, mode, is_resume=False):
        try:
            self.game_mode = mode
            if not is_resume:
                self.level = 1
                self.total_score = 0
                self.question_num = 1
                self.lives = 3 
            
            # Jika resume, lives direset penuh untuk level tersebut (opsional)
            # atau simpan lives juga di json jika mau hardcore.
            # Disini kita reset lives ke 3 setiap kali load game biar fair.
            self.lives = 3
            self.mistakes_in_level = 0
            
            write_local_log(f"start_game mode={mode} lvl={self.level}")
            self.next_question()
        except Exception as e:
            log_exception(e, 'GameScreen.start_game')

    def next_question(self):
        try:
            self.game_active = True
            
            # Reset timer & visual
            if self.timer_event: self.timer_event.cancel()
            
            # Kesulitan Waktu: Level 1=20s, Level 10=10s
            base_time = 20
            reduction = min(10, (self.level - 1))
            self.time_left = base_time - reduction
            
            self.timer_text = str(self.time_left)
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
            
            self.level_text = f"Level: {self.level}"
            self.score_text = f"Skor: {self.total_score}"
            self.status_text = f"Soal {self.question_num}/10"
            self.lives_text = f"Nyawa: {self.lives}" # Update teks nyawa
            
            self.generate_question()
        except Exception as e:
            log_exception(e, 'GameScreen.next_question')

    def generate_question(self):
        try:
            app = App.get_running_app()
            grade = getattr(app, 'selected_grade', 3)
            diff = self.level
            
            # Logic Angka
            if self.game_mode == 'tambah':
                max_v = 15 + (10 * diff) + (grade*2)
                n1 = random.randint(1, max_v)
                n2 = random.randint(1, max_v)
                ans = n1 + n2
                sym = '+'
            elif self.game_mode == 'kurang':
                max_v = 15 + (10 * diff) + (grade*2)
                a = random.randint(1, max_v)
                b = random.randint(1, max_v)
                n1, n2 = max(a,b), min(a,b)
                ans = n1 - n2
                sym = '-'
            elif self.game_mode == 'kali':
                max_v = 4 + diff + (grade//2)
                n1 = random.randint(2, max_v)
                n2 = random.randint(2, max_v)
                ans = n1 * n2
                sym = 'x'
            elif self.game_mode == 'bagi':
                max_quotient = 3 + diff
                n2 = random.randint(2, 10 + grade)
                q = random.randint(2, max_quotient)
                n1 = n2 * q
                ans = q
                sym = ':'
            else:
                n1, n2, ans, sym = 1, 1, 2, '+'

            self.correct_answer = ans
            self.question_text = f"{n1} {sym} {n2} = ?"

            answers = [ans]
            while len(answers) < 4:
                fake = ans + random.randint(-5, 5)
                if fake != ans and fake not in answers:
                    if fake < 0 and grade < 8: fake = abs(fake)
                    answers.append(fake)
            random.shuffle(answers)

            for i, btn in enumerate(self.buttons):
                btn.text = str(answers[i])
                btn.disabled = False
                btn.bg_color = (0.2, 0.6, 1, 1) 
                # Animasi muncul
                anim = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.2)
                anim.start(btn)
                
        except Exception as e:
            log_exception(e, 'GameScreen.gen_q')

    def update_timer(self, dt):
        if not self.game_active: return
        self.time_left -= 1
        self.timer_text = str(self.time_left)
        if self.time_left <= 0:
            self.check_answer_anim(None, timeout=True)

    def check_answer_anim(self, instance, timeout=False):
        if not self.game_active: return
        self.game_active = False 

        if self.timer_event: self.timer_event.cancel()

        # Animasi klik
        if instance:
            anim = Animation(size_hint=(0.45, 0.9), duration=0.05) + Animation(size_hint=(0.5, 1), duration=0.05)
            anim.start(instance)

        Clock.schedule_once(lambda dt: self._process_answer(instance, timeout), 0.15)

    def _process_answer(self, instance, timeout):
        correct = False
        app = App.get_running_app()
        
        # Cari tombol benar untuk di-reveal nanti
        correct_btn = None
        for btn in self.buttons:
            if btn.text == str(self.correct_answer):
                correct_btn = btn

        if not timeout and instance:
            if int(instance.text) == self.correct_answer:
                correct = True
                self.total_score += 10
                app.play_sound('correct')
                self.animate_color(instance, (0.2, 0.8, 0.2, 1)) # Hijau
            else:
                correct = False
                app.play_sound('wrong')
                self.animate_color(instance, (0.8, 0.2, 0.2, 1)) # Merah
        else:
            # Timeout
            app.play_sound('wrong')

        # Logic Nyawa & Kalah
        if not correct:
            self.lives -= 1
            self.mistakes_in_level += 1
            self.lives_text = f"Nyawa: {self.lives}"
            
            # Reveal jawaban benar
            if correct_btn:
                self.animate_color(correct_btn, (0.2, 0.8, 0.2, 1))

            if self.lives <= 0:
                # GAME OVER TRIGGER
                Clock.schedule_once(self.show_game_over_popup, 1.0)
                return

        # Disable tombol
        for btn in self.buttons:
            btn.disabled = True

        # Lanjut ke next question
        Clock.schedule_once(self.finish_step, 1.2)

    def animate_color(self, widget, color):
        anim = Animation(bg_color=color, duration=0.3)
        anim.start(widget)

    def finish_step(self, dt):
        # Jika sudah game over (lives=0), jangan lanjut
        if self.lives <= 0: return

        if self.question_num >= 10:
            # Level Selesai -> Auto Save
            self.save_progress()
            app = App.get_running_app()
            app.play_sound('win')
            self.show_level_complete_popup()
        else:
            self.question_num += 1
            self.next_question()

    def show_level_complete_popup(self):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        lbl = Label(text=f"LEVEL {self.level} SELESAI!", font_size='24sp', bold=True, color=(0,1,0,1))
        lbl_info = Label(text=f"Sisa Nyawa: {self.lives}\nSkor: {self.total_score}", font_size='18sp', halign='center')
        
        btn_next = RoundedButton(text="LANJUT LEVEL BERIKUTNYA", bg_color=(0, 0.6, 0, 1), size_hint=(1, 0.4))
        btn_menu = RoundedButton(text="KEMBALI KE MENU", bg_color=(0.5, 0.5, 0.5, 1), size_hint=(1, 0.4))

        content.add_widget(lbl)
        content.add_widget(lbl_info)
        content.add_widget(btn_next)
        content.add_widget(btn_menu)

        popup = Popup(title="HEBAT!", content=content, size_hint=(0.85, 0.55), auto_dismiss=False, separator_height=0)
        
        btn_next.bind(on_release=lambda x: self.next_level_action(popup))
        btn_menu.bind(on_release=lambda x: self.menu_action(popup))
        popup.open()

    def show_game_over_popup(self, dt):
        """Popup jika nyawa habis"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        lbl = Label(text="GAME OVER", font_size='30sp', bold=True, color=(1,0,0,1))
        lbl_msg = Label(text="Yah, nyawa kamu habis.\nJangan menyerah!", font_size='18sp', halign='center')
        
        btn_retry = RoundedButton(text="ULANGI LEVEL INI", bg_color=(0.2, 0.6, 1, 1), size_hint=(1, 0.4))
        btn_quit = RoundedButton(text="KELUAR", bg_color=(0.6, 0.2, 0.2, 1), size_hint=(1, 0.4))

        content.add_widget(lbl)
        content.add_widget(lbl_msg)
        content.add_widget(btn_retry)
        content.add_widget(btn_quit)

        popup = Popup(title="", content=content, size_hint=(0.8, 0.5), auto_dismiss=False, separator_height=0)
        
        btn_retry.bind(on_release=lambda x: self.retry_level_action(popup))
        btn_quit.bind(on_release=lambda x: self.menu_action(popup))
        popup.open()

    def next_level_action(self, popup):
        popup.dismiss()
        self.level += 1
        self.question_num = 1
        self.lives = 3 # Reset nyawa di level baru
        self.mistakes_in_level = 0
        self.next_question()

    def retry_level_action(self, popup):
        popup.dismiss()
        # Reset ke awal level yang sama
        self.question_num = 1
        self.lives = 3
        self.mistakes_in_level = 0
        self.next_question()

    def menu_action(self, popup):
        popup.dismiss()
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    def save_progress(self):
        try:
            app = App.get_running_app()
            if getattr(app, 'store', None):
                # Simpan agar saat diload, pemain mulai di level selanjutnya
                app.store.put('math_data', 
                              grade=app.selected_grade, 
                              level=self.level + 1, 
                              score=self.total_score, 
                              mode=getattr(self, 'game_mode', 'tambah'))
                write_local_log(f"Saved: Lvl {self.level+1}")
        except Exception as e:
            log_exception(e, 'save_progress')

    def quit_game(self):
        if self.timer_event: self.timer_event.cancel()
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

# ---------- App ----------
class MathApp(App):
    selected_grade = NumericProperty(3)
    grade_title = StringProperty("Kelas 3 SD")
    store = None
    sounds = {}

    def build(self):
        # 1. Setup Storage
        try:
            data_dir = self.user_data_dir
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)
            self.store = JsonStore(os.path.join(data_dir, 'math_data.json'))
        except Exception:
            self.store = None
        
        # 2. Setup Sounds (Load di awal biar ringan)
        self.load_sounds()

        return Builder.load_string(kv_string)

    def load_sounds(self):
        """Mencoba load file suara. Jika file tidak ada, tidak akan error."""
        sound_files = {
            'click': 'click.wav',
            'correct': 'correct.wav',
            'wrong': 'wrong.wav',
            'win': 'win.wav'
        }
        for name, filename in sound_files.items():
            try:
                # Cek di folder asset atau root
                snd = SoundLoader.load(filename)
                if snd:
                    self.sounds[name] = snd
                else:
                    write_local_log(f"Sound file not found: {filename}")
            except Exception as e:
                write_local_log(f"Err loading sound {filename}: {e}")

    def play_sound(self, name):
        """Memutar suara jika ada."""
        if name in self.sounds and self.sounds[name]:
            try:
                if self.sounds[name].state == 'play':
                    self.sounds[name].stop()
                self.sounds[name].play()
            except Exception:
                pass

    def set_grade(self, grade):
        self.selected_grade = grade
        titles = {3: "Kelas 3 SD", 5: "Kelas 5 SD", 8: "Kelas 8 SMP"}
        self.grade_title = f"{titles.get(grade, '')}"

    def load_game(self):
        if self.store and self.store.exists('math_data'):
            self.play_sound('click')
            data = self.store.get('math_data')
            self.set_grade(data.get('grade', 3))
            
            self.root.transition.direction = 'left'
            self.root.current = 'game'
            
            game_screen = self.root.get_screen('game')
            game_screen.level = data.get('level', 1)
            game_screen.total_score = data.get('score', 0)
            game_screen.start_game(data.get('mode', 'tambah'), is_resume=True)

if __name__ == '__main__':
    try:
        MathApp().run()
    except Exception as e:
        with open("crash_log.txt", "w") as f:
            f.write(traceback.format_exc())
