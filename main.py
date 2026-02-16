# main.py (FINAL: ANIMATED COVER + ASSETS FOLDER SUPPORT)
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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.storage.jsonstore import JsonStore
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.core.audio import SoundLoader
from kivy.resources import resource_find
from kivy.metrics import dp

# Warna Background (Biru Gelap Modern)
Window.clearcolor = (0.1, 0.15, 0.22, 1)

kv_string = '''
#:import SlideTransition kivy.uix.screenmanager.SlideTransition

# Template Tombol Keren
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
    font_size: '18sp'
    bold: True
    color: 1, 1, 1, 1

ScreenManager:
    transition: SlideTransition()
    GradeScreen:
    MenuScreen:
    GameScreen:

<GradeScreen>:
    name: 'grade'
    
    # Layer 1: Background Animasi (Floating Math Symbols)
    FloatLayout:
        id: bg_anim_layer

    # Layer 2: Konten Utama
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 20

        # Label Judul dengan ID agar bisa dianimasi
        Label:
            id: title_lbl
            text: "MATH MASTER"
            font_size: '42sp'
            bold: True
            color: 1, 0.8, 0, 1
            size_hint: 1, 0.3

        # Tombol Load Game
        RoundedButton:
            id: btn_resume
            text: "LANJUTKAN GAME TERAKHIR"
            bg_color: 0.3, 0.3, 0.3, 1
            size_hint: 1, 0.15
            disabled: True
            on_release: 
                app.play_sound('click')
                app.load_last_game()

        Label:
            text: "PILIH KELAS BARU:"
            font_size: '16sp'
            color: 0.7, 0.7, 0.7, 1
            size_hint: 1, 0.1

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
                    root.manager.get_screen('game').start_new_game('tambah')

            RoundedButton:
                text: "Kurang (-)"
                bg_color: 0.2, 0.6, 0.8, 1
                on_release:
                    app.play_sound('click')
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_new_game('kurang')

            RoundedButton:
                text: "Kali (x)"
                bg_color: 0.7, 0.3, 0.6, 1
                on_release:
                    app.play_sound('click')
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_new_game('kali')

            RoundedButton:
                text: "Bagi (:)"
                bg_color: 0.7, 0.3, 0.6, 1
                on_release:
                    app.play_sound('click')
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_new_game('bagi')

        RoundedButton:
            text: "<< KEMBALI"
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
            size_hint: 1, 0.15
            
            # Info Kiri
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: root.level_text
                    font_size: '18sp'
                    color: 1, 1, 0, 1
                Label:
                    text: root.lives_text
                    font_size: '16sp'
                    color: 1, 0.3, 0.3, 1
                    bold: True

            # Info Tengah (Timer)
            Label:
                text: root.timer_text
                font_size: '35sp'
                bold: True
                color: (1, 0.2, 0.2, 1) if int(root.timer_text) <= 5 else (1, 1, 1, 1)

            # Info Kanan
            Label:
                text: root.score_text
                font_size: '18sp'
                color: 0, 1, 0.5, 1

        Label:
            text: root.status_text
            size_hint: 1, 0.05
            font_size: '14sp'
            color: 0.6, 0.6, 0.6, 1

        # --- SOAL ---
        Label:
            text: root.question_text
            font_size: '55sp'
            bold: True
            size_hint: 1, 0.35
            color: 1, 1, 1, 1

        # --- JAWABAN ---
        GridLayout:
            id: answer_grid
            cols: 2
            spacing: 15
            padding: [10, 0, 10, 10]
            size_hint: 1, 0.4

        # --- TOMBOL BAWAH ---
        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            size_hint: 1, 0.12

            RoundedButton:
                text: "SIMPAN & KELUAR"
                bg_color: 0.2, 0.6, 0.8, 1
                on_release: 
                    app.play_sound('click')
                    root.save_and_quit()

            RoundedButton:
                text: "BATAL / KELUAR"
                bg_color: 0.8, 0.2, 0.2, 1
                on_release: 
                    app.play_sound('click')
                    root.just_quit()
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

# ---------- Custom Widgets ----------
class RoundedButton(Button):
    bg_color = ListProperty([0.2, 0.6, 1, 1])

# ---------- Screens ----------
class GradeScreen(Screen):
    def on_enter(self):
        # 1. Cek Save Data
        self.check_save_data()
        
        # 2. Mulai Animasi Judul
        self.animate_title()
        
        # 3. Mulai Animasi Background (Simbol Matematika Terbang)
        self.start_floating_symbols()

    def on_leave(self):
        # Hentikan animasi saat pindah layar agar hemat resource
        Animation.cancel_all(self.ids.title_lbl)
        self.ids.bg_anim_layer.clear_widgets()

    def check_save_data(self):
        try:
            app = App.get_running_app()
            btn = self.ids.btn_resume
            if getattr(app, 'store', None) and app.store.exists('math_save'):
                data = app.store.get('math_save')
                lvl = data.get('level', 1)
                scr = data.get('score', 0)
                mode = data.get('mode', 'tambah').upper()
                btn.text = f"LANJUT: {mode} (Level {lvl}) - Skor {scr}"
                btn.disabled = False
                btn.bg_color = (0.2, 0.7, 0.2, 1) 
            else:
                btn.text = "TIDAK ADA SAVE DATA"
                btn.disabled = True
                btn.bg_color = (0.3, 0.3, 0.3, 1)
        except Exception as e:
            write_local_log(f"Error checking save: {e}")

    def animate_title(self):
        # Animasi Denyut (Pulse)
        lbl = self.ids.title_lbl
        # Reset ukuran dulu
        lbl.font_size = '42sp'
        
        # Animasi: Besar -> Kecil -> Ulangi
        anim = Animation(font_size='50sp', duration=1.0, t='in_out_quad') + \
               Animation(font_size='42sp', duration=1.0, t='in_out_quad')
        anim.repeat = True
        anim.start(lbl)

    def start_floating_symbols(self):
        # Buat simbol matematika melayang secara acak
        # Tambahkan simbol baru setiap 0.5 detik
        Clock.schedule_interval(self.spawn_symbol, 0.8)

    def spawn_symbol(self, dt):
        # Jika sudah pindah layar, hentikan spawn
        if self.manager.current != 'grade':
            return False

        bg = self.ids.bg_anim_layer
        
        # Batasi jumlah simbol agar tidak lag (max 15)
        if len(bg.children) > 15:
            return

        symbols = ['+', '-', 'x', ':', '?', '%', '=']
        txt = random.choice(symbols)
        
        # Posisi X acak, Y mulai dari bawah layar
        pos_x = random.random() # 0.0 - 1.0 (relative)
        
        lbl = Label(
            text=txt,
            font_size=f'{random.randint(20, 60)}sp',
            color=(1, 1, 1, 0.1), # Transparan (putih pudar)
            pos_hint={'x': pos_x, 'y': -0.1},
            size_hint=(None, None)
        )
        
        bg.add_widget(lbl)
        
        # Animasi: Gerak ke atas sambil memudar/hilang
        duration = random.uniform(3, 6)
        anim = Animation(pos_hint={'x': pos_x, 'y': 1.1}, duration=duration) # Terbang ke atas layar
        
        # Hapus widget setelah animasi selesai
        anim.bind(on_complete=lambda *args: bg.remove_widget(lbl))
        anim.start(lbl)

class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    level_text = StringProperty("Level: 1")
    lives_text = StringProperty("Nyawa: 3")
    timer_text = StringProperty("20")
    score_text = StringProperty("Skor: 0")
    status_text = StringProperty("Soal 1/10")
    question_text = StringProperty("Siap?")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons = []
        self.level = 1
        self.total_score = 0
        self.question_num = 1
        self.lives = 3
        self.game_mode = 'tambah'
        self.time_left = 20
        self.correct_answer = 0
        self.timer_event = None
        self.game_active = False 
        Clock.schedule_once(self.setup_buttons)

    def setup_buttons(self, dt):
        if 'answer_grid' not in self.ids:
            Clock.schedule_once(self.setup_buttons, 0.1)
            return
        grid = self.ids.answer_grid
        grid.clear_widgets()
        self.buttons = []
        for _ in range(4):
            btn = RoundedButton(text="", font_size='30sp')
            btn.bind(on_release=self.check_answer_anim)
            self.buttons.append(btn)
            grid.add_widget(btn)

    def start_new_game(self, mode):
        self.game_mode = mode
        self.level = 1
        self.total_score = 0
        self.question_num = 1
        self.lives = 3
        self.start_round()

    def resume_game(self, data):
        self.game_mode = data.get('mode', 'tambah')
        self.level = data.get('level', 1)
        self.total_score = data.get('score', 0)
        self.lives = data.get('lives', 3)
        self.question_num = data.get('question_num', 1)
        self.start_round()

    def start_round(self):
        self.update_ui_labels()
        self.next_question()

    def next_question(self):
        self.game_active = True
        if self.timer_event: self.timer_event.cancel()
        
        base = 20
        reduction = min(12, (self.level - 1))
        self.time_left = base - reduction
        
        self.timer_text = str(self.time_left)
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        self.update_ui_labels()
        self.generate_question()

    def update_ui_labels(self):
        self.level_text = f"Level: {self.level}"
        self.score_text = f"Skor: {self.total_score}"
        self.status_text = f"Soal {self.question_num}/10"
        self.lives_text = f"Nyawa: {self.lives}"

    def generate_question(self):
        app = App.get_running_app()
        grade = getattr(app, 'selected_grade', 3)
        diff = self.level
        
        if self.game_mode == 'tambah':
            max_v = 15 + (10 * diff) + (grade*2)
            n1, n2 = random.randint(1, max_v), random.randint(1, max_v)
            ans, sym = n1 + n2, '+'
        elif self.game_mode == 'kurang':
            max_v = 20 + (10 * diff)
            a, b = random.randint(1, max_v), random.randint(1, max_v)
            n1, n2 = max(a,b), min(a,b)
            ans, sym = n1 - n2, '-'
        elif self.game_mode == 'kali':
            max_v = 4 + diff + (grade//2)
            n1, n2 = random.randint(2, max_v), random.randint(2, max_v)
            ans, sym = n1 * n2, 'x'
        elif self.game_mode == 'bagi':
            max_q = 3 + diff
            n2 = random.randint(2, 10 + grade)
            q = random.randint(2, max_q)
            n1, ans, sym = n2 * q, q, ':'
        else:
            n1, n2, ans, sym = 1, 1, 2, '+'

        self.correct_answer = ans
        self.question_text = f"{n1} {sym} {n2} = ?"

        answers = [ans]
        while len(answers) < 4:
            fake = ans + random.randint(-5, 5)
            if fake != ans and fake not in answers:
                if fake < 0 and grade < 5: fake = abs(fake)
                answers.append(fake)
        random.shuffle(answers)

        for i, btn in enumerate(self.buttons):
            btn.text = str(answers[i])
            btn.disabled = False
            btn.bg_color = (0.2, 0.6, 1, 1)
            anim = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.3)
            anim.start(btn)

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

        if instance:
            anim = Animation(size_hint=(0.45, 0.9), duration=0.05) + Animation(size_hint=(0.5, 1), duration=0.05)
            anim.start(instance)

        Clock.schedule_once(lambda dt: self._process_result(instance, timeout), 0.15)

    def _process_result(self, instance, timeout):
        app = App.get_running_app()
        correct = False
        correct_btn = None
        for btn in self.buttons:
            if btn.text == str(self.correct_answer): correct_btn = btn

        if not timeout and instance:
            if int(instance.text) == self.correct_answer:
                correct = True
                self.total_score += 10
                app.play_sound('correct')
                self.animate_btn(instance, (0.2, 0.8, 0.2, 1))
            else:
                app.play_sound('wrong')
                self.animate_btn(instance, (0.8, 0.2, 0.2, 1))
        else:
            app.play_sound('wrong')

        if not correct:
            self.lives -= 1
            if correct_btn: self.animate_btn(correct_btn, (0.2, 0.8, 0.2, 1))
            if self.lives <= 0:
                self.update_ui_labels()
                Clock.schedule_once(self.show_game_over, 1.0)
                return

        self.update_ui_labels()
        for btn in self.buttons: btn.disabled = True
        Clock.schedule_once(self.finish_step, 1.0)

    def animate_btn(self, btn, color):
        Animation(bg_color=color, duration=0.2).start(btn)

    def finish_step(self, dt):
        if self.lives <= 0: return
        if self.question_num >= 10:
            self.question_num = 1
            self.level += 1
            self.save_data_internal()
            app = App.get_running_app()
            app.play_sound('win')
            self.show_level_complete()
        else:
            self.question_num += 1
            self.next_question()

    def save_data_internal(self):
        try:
            app = App.get_running_app()
            if getattr(app, 'store', None):
                app.store.put('math_save',
                              grade=app.selected_grade,
                              level=self.level,
                              score=self.total_score,
                              lives=self.lives,
                              question_num=self.question_num,
                              mode=self.game_mode)
        except Exception: pass

    def save_and_quit(self):
        if self.timer_event: self.timer_event.cancel()
        self.save_data_internal()
        popup = Popup(title='Disimpan!', content=Label(text='Progres aman.', font_size='18sp'), size_hint=(0.5, 0.3))
        popup.open()
        Clock.schedule_once(lambda dt: self.exit_to_menu(popup), 1.0)

    def just_quit(self):
        if self.timer_event: self.timer_event.cancel()
        self.manager.transition.direction = 'right'
        self.manager.current = 'grade'

    def exit_to_menu(self, popup):
        popup.dismiss()
        self.manager.transition.direction = 'right'
        self.manager.current = 'grade'

    def show_level_complete(self):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        content.add_widget(Label(text=f"LEVEL {self.level-1} SELESAI!", font_size='22sp', bold=True, color=(0,1,0,1)))
        
        btn = RoundedButton(text="LANJUT >>", bg_color=(0, 0.6, 0, 1))
        
        popup = Popup(title="HEBAT!", content=content, size_hint=(0.7, 0.4), auto_dismiss=False)
        btn.bind(on_release=lambda x: self.next_level_action(popup))
        content.add_widget(btn)
        popup.open()

    def next_level_action(self, popup):
        popup.dismiss()
        self.lives = 3
        self.start_round()

    def show_game_over(self, dt):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        content.add_widget(Label(text="GAME OVER", font_size='28sp', bold=True, color=(1,0,0,1)))
        
        btn_retry = RoundedButton(text="ULANGI LEVEL", bg_color=(0.2, 0.6, 1, 1))
        btn_exit = RoundedButton(text="KELUAR MENU", bg_color=(0.5, 0.2, 0.2, 1))

        popup = Popup(title="", content=content, size_hint=(0.8, 0.5), auto_dismiss=False)
        btn_retry.bind(on_release=lambda x: self.retry_action(popup))
        btn_exit.bind(on_release=lambda x: self.exit_game_over(popup))
        
        content.add_widget(btn_retry)
        content.add_widget(btn_exit)
        popup.open()

    def retry_action(self, popup):
        popup.dismiss()
        self.lives = 3
        self.question_num = 1
        self.start_round()

    def exit_game_over(self, popup):
        popup.dismiss()
        self.manager.transition.direction = 'right'
        self.manager.current = 'grade'

# ---------- App ----------
class MathApp(App):
    selected_grade = NumericProperty(3)
    grade_title = StringProperty("Kelas 3 SD")
    store = None
    sounds = {}

    def build(self):
        try:
            data_dir = self.user_data_dir
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)
            self.store = JsonStore(os.path.join(data_dir, 'math_save.json'))
        except Exception:
            self.store = None
        
        self.load_sounds()
        return Builder.load_string(kv_string)

    def load_sounds(self):
        # ANDROID SAFE: pakai resource_find dulu (cari di APK),
        # lalu fallback ke filesystem path (buat desktop/dev)
        files = {'click': 'click.wav', 'correct': 'correct.wav', 'wrong': 'wrong.wav', 'win': 'win.wav'}
        for k, filename in files.items():
            try:
                rel_path = os.path.join('assets', 'sounds', filename).replace('\\','/')
                real_path = resource_find(rel_path)
                if not real_path:
                    # fallback: try relative to script (desktop / dev)
                    try:
                        base_dir = os.path.dirname(os.path.abspath(__file__))
                        alt = os.path.join(base_dir, 'assets', 'sounds', filename)
                        if os.path.exists(alt):
                            real_path = alt
                    except Exception:
                        real_path = None

                if real_path:
                    try:
                        snd = SoundLoader.load(real_path)
                        if snd:
                            self.sounds[k] = snd
                        else:
                            write_local_log(f"Failed to load sound (SoundLoader returned None): {real_path}")
                    except Exception as e:
                        write_local_log(f"Error loading sound via SoundLoader: {real_path} -> {e}")
                else:
                    write_local_log(f"Sound missing: {rel_path}")
            except Exception as e:
                write_local_log(f"Err load sound: {e}")

    def play_sound(self, name):
        if name in self.sounds and self.sounds[name]:
            try:
                # many backends expect stop before play to reset
                try:
                    if getattr(self.sounds[name], 'state', None) == 'play':
                        self.sounds[name].stop()
                except Exception:
                    pass
                self.sounds[name].play()
            except Exception:
                pass

    def set_grade(self, grade):
        self.selected_grade = grade
        titles = {3: "Kelas 3 SD", 5: "Kelas 5 SD", 8: "Kelas 8 SMP"}
        self.grade_title = titles.get(grade, "")

    def load_last_game(self):
        if self.store and self.store.exists('math_save'):
            data = self.store.get('math_save')
            self.set_grade(data.get('grade', 3))
            self.root.transition.direction = 'left'
            self.root.current = 'game'
            self.root.get_screen('game').resume_game(data)

if __name__ == '__main__':
    try:
        MathApp().run()
    except Exception as e:
        # pastikan catat error fatal ke file agar bisa di-trace di device
        try:
            write_local_log(f"FATAL: {e}")
            write_local_log(traceback.format_exc())
        except:
            # fallback print
            print(traceback.format_exc())
