# main.py
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

# Konfigurasi Warna Background (Dark Grey)
Window.clearcolor = (0.1, 0.12, 0.15, 1)

kv_string = '''
#:import SlideTransition kivy.uix.screenmanager.SlideTransition

# Template Tombol dengan Sudut Membulat
<RoundedButton@Button>:
    background_color: 0,0,0,0  # Transparan agar canvas bisa menggambar
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
        spacing: 25

        Label:
            text: "MATH MASTER"
            font_size: '40sp'
            bold: True
            color: 1, 0.8, 0, 1
            size_hint: 1, 0.3

        Label:
            text: "PILIH KELAS"
            font_size: '20sp'
            size_hint: 1, 0.1

        RoundedButton:
            id: btn_resume
            text: "LANJUTKAN GAME"
            bg_color: 0.4, 0.4, 0.4, 1
            on_release: app.load_game()
            disabled: True

        RoundedButton:
            text: "KELAS 3 SD"
            bg_color: 0.2, 0.8, 0.2, 1
            on_release:
                app.set_grade(3)
                root.manager.transition.direction = 'left'
                root.manager.current = 'menu'

        RoundedButton:
            text: "KELAS 5 SD"
            bg_color: 1, 0.6, 0, 1
            on_release:
                app.set_grade(5)
                root.manager.transition.direction = 'left'
                root.manager.current = 'menu'

        RoundedButton:
            text: "KELAS 8 SMP"
            bg_color: 0.8, 0.2, 0.2, 1
            on_release:
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
            font_size: '24sp'
            color: 0.6, 0.8, 1, 1
            size_hint: 1, 0.15

        Label:
            text: "Pilih Mode Operasi"
            font_size: '20sp'
            size_hint: 1, 0.1

        GridLayout:
            cols: 2
            spacing: 20
            size_hint: 1, 0.6

            RoundedButton:
                text: "Tambah (+)"
                bg_color: 0.3, 0.7, 0.9, 1
                on_release:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('tambah')

            RoundedButton:
                text: "Kurang (-)"
                bg_color: 0.3, 0.7, 0.9, 1
                on_release:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('kurang')

            RoundedButton:
                text: "Kali (x)"
                bg_color: 0.9, 0.4, 0.8, 1
                on_release:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('kali')

            RoundedButton:
                text: "Bagi (:)"
                bg_color: 0.9, 0.4, 0.8, 1
                on_release:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('bagi')

        RoundedButton:
            text: "<< Ganti Kelas"
            bg_color: 0.3, 0.3, 0.3, 1
            size_hint: 1, 0.15
            on_release: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'grade'

<GameScreen>:
    name: 'game'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        # Header Info
        GridLayout:
            cols: 3
            size_hint: 1, 0.1
            Label:
                text: root.level_text
                font_size: '18sp'
                color: 1, 1, 0, 1
            Label:
                text: root.timer_text
                font_size: '28sp'
                bold: True
                color: (1, 0.2, 0.2, 1) if int(root.timer_text) <= 5 else (1, 1, 1, 1)
            Label:
                text: root.score_text
                font_size: '18sp'
                color: 0, 1, 0.5, 1

        Label:
            text: root.status_text
            size_hint: 1, 0.05
            font_size: '16sp'
            color: 0.7, 0.7, 0.7, 1

        # Pertanyaan Area
        Label:
            text: root.question_text
            font_size: '50sp'
            bold: True
            size_hint: 1, 0.35

        # Grid Jawaban
        GridLayout:
            id: answer_grid
            cols: 2
            spacing: 20
            padding: [0, 10, 0, 10]
            size_hint: 1, 0.45

        RoundedButton:
            text: "Keluar"
            size_hint: 1, 0.1
            bg_color: 0.8, 0.2, 0.2, 1
            on_release: root.quit_game()
'''

# ---------- Helper Logging ----------
def write_local_log(msg):
    try:
        app = App.get_running_app()
        if app:
            data_dir = getattr(app, 'user_data_dir', None) or app.user_data_dir
        else:
            data_dir = os.path.expanduser('~')
        if not data_dir:
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
    write_local_log(f"EXCEPTION at {where}: {repr(exc)}\n{tb}")

# ---------- Custom Widgets ----------
class RoundedButton(Button):
    bg_color = ListProperty([0.2, 0.6, 1, 1])

# ---------- Screens ----------
class GradeScreen(Screen):
    def on_enter(self):
        try:
            app = App.get_running_app()
            if getattr(app, 'store', None) and app.store.exists('math_data'):
                data = app.store.get('math_data')
                btn = self.ids.get('btn_resume', None)
                if btn:
                    btn.disabled = False
                    btn.text = f"LANJUT: Level {data.get('level', '?')} ({data.get('mode', '').upper()})"
                    btn.bg_color = (0.2, 0.5, 0.2, 1)
            else:
                btn = self.ids.get('btn_resume', None)
                if btn:
                    btn.disabled = True
                    btn.bg_color = (0.4, 0.4, 0.4, 1)
        except Exception as e:
            log_exception(e, 'GradeScreen.on_enter')

class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    level_text = StringProperty("Level: 1")
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
        self.time_left = 20
        self.correct_answer = 0
        self.timer_event = None
        self.game_active = False # Mencegah double click
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
                # Gunakan RoundedButton custom
                btn = RoundedButton(text="", font_size='32sp')
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
            
            write_local_log(f"start_game mode={mode} is_resume={is_resume}")
            self.next_question()
        except Exception as e:
            log_exception(e, 'GameScreen.start_game')

    def next_question(self):
        try:
            self.game_active = True
            # Reset timer
            if self.timer_event:
                self.timer_event.cancel()
            
            # Waktu berkurang sedikit setiap level naik (min 5 detik)
            base_time = 20
            time_reduction = min(15, (self.level - 1) * 1) 
            self.time_left = base_time - time_reduction
            
            self.timer_text = str(self.time_left)
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
            
            self.level_text = f"Level: {self.level}"
            self.score_text = f"Skor: {self.total_score}"
            self.status_text = f"Soal {self.question_num}/10"
            
            self.generate_question()
        except Exception as e:
            log_exception(e, 'GameScreen.next_question')

    def generate_question(self):
        try:
            app = App.get_running_app()
            grade = getattr(app, 'selected_grade', 3)
            
            # Logic Kesulitan: Angka makin besar seiring Level naik
            diff_factor = self.level
            
            if self.game_mode == 'tambah':
                max_val = 20 + (10 * diff_factor) + (grade * 5)
                num1 = random.randint(1, max_val)
                num2 = random.randint(1, max_val)
                ans = num1 + num2
                symbol = '+'
            elif self.game_mode == 'kurang':
                max_val = 20 + (10 * diff_factor) + (grade * 5)
                a = random.randint(1, max_val)
                b = random.randint(1, max_val)
                num1, num2 = max(a,b), min(a,b)
                ans = num1 - num2
                symbol = '-'
            elif self.game_mode == 'kali':
                max_val = 5 + diff_factor + (grade // 2)
                num1 = random.randint(2, max_val)
                num2 = random.randint(2, max_val)
                ans = num1 * num2
                symbol = 'x'
            elif self.game_mode == 'bagi':
                max_quotient = 5 + diff_factor
                num2 = random.randint(2, 10 + (grade//2))
                quotient = random.randint(2, max_quotient)
                num1 = num2 * quotient
                ans = quotient
                symbol = ':'
            else:
                num1, num2, ans, symbol = 1, 1, 2, '+'

            self.correct_answer = ans
            self.question_text = f"{num1} {symbol} {num2} = ?"

            answers = [ans]
            while len(answers) < 4:
                # Membuat jawaban pengecoh yang cerdas (dekat dengan jawaban asli)
                offset = random.randint(-5, 5)
                fake = ans + offset
                if fake != ans and fake not in answers:
                    if fake < 0 and grade < 8:
                        fake = abs(fake)
                    answers.append(fake)
            random.shuffle(answers)

            # Update Buttons dengan Animasi muncul
            for i, btn in enumerate(self.buttons):
                btn.text = str(answers[i])
                btn.disabled = False
                btn.bg_color = (0.2, 0.6, 1, 1) # Reset warna biru
                
                # Animasi kecil saat tombol muncul
                anim = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.3)
                anim.start(btn)
                
        except Exception as e:
            log_exception(e, 'GameScreen.generate_question')

    def update_timer(self, dt):
        if not self.game_active: return
        self.time_left -= 1
        self.timer_text = str(self.time_left)
        if self.time_left <= 0:
            self.check_answer_anim(None, timeout=True)

    def check_answer_anim(self, instance, timeout=False):
        """Wrapper untuk animasi sebelum logika check_answer"""
        if not self.game_active: return
        self.game_active = False # Stop interaksi lain

        if self.timer_event:
            self.timer_event.cancel()

        # Animasi tombol yang ditekan
        if instance:
            # Animasi bounce
            anim = Animation(size_hint=(0.45, 0.9), duration=0.1) + Animation(size_hint=(0.5, 1), duration=0.1)
            anim.start(instance)

        # Jalankan logika pengecekan setelah jeda singkat animasi
        Clock.schedule_once(lambda dt: self._process_answer(instance, timeout), 0.2)

    def _process_answer(self, instance, timeout):
        correct = False
        
        # 1. Cari tombol jawaban benar
        correct_btn = None
        for btn in self.buttons:
            try:
                if int(btn.text) == self.correct_answer:
                    correct_btn = btn
            except: pass

        # 2. Logika Cek
        if not timeout and instance:
            try:
                val = int(instance.text)
                if val == self.correct_answer:
                    correct = True
                    self.total_score += 10 # Skor lebih besar
                    # Animasi Warna Hijau (Benar)
                    self.animate_color(instance, (0.2, 0.8, 0.2, 1)) 
                else:
                    # Animasi Warna Merah (Salah)
                    self.animate_color(instance, (0.8, 0.2, 0.2, 1))
            except:
                pass
        
        # Jika timeout, atau salah jawab, reveal jawaban benar
        if (timeout or not correct) and correct_btn:
             self.animate_color(correct_btn, (0.2, 0.8, 0.2, 1))

        # Disable semua tombol
        for btn in self.buttons:
            btn.disabled = True

        # Pindah langkah berikutnya
        Clock.schedule_once(self.finish_step, 1.5)

    def animate_color(self, widget, target_color):
        """Animasi perubahan warna"""
        anim = Animation(bg_color=target_color, duration=0.3)
        anim.start(widget)

    def finish_step(self, dt):
        try:
            if self.question_num >= 10:
                # LEVEL SELESAI
                self.save_progress()
                self.show_level_complete_popup()
            else:
                self.question_num += 1
                self.next_question()
        except Exception as e:
            log_exception(e, 'GameScreen.finish_step')

    def show_level_complete_popup(self):
        """Popup menarik saat level selesai"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        lbl_congrats = Label(text="LEVEL SELESAI!", font_size='30sp', bold=True, color=(1,1,0,1))
        lbl_score = Label(text=f"Skor Total: {self.total_score}", font_size='24sp')
        
        btn_next = RoundedButton(text="LEVEL BERIKUTNYA >>", bg_color=(0, 0.7, 0, 1), size_hint=(1, 0.4))
        btn_menu = RoundedButton(text="KEMBALI KE MENU", bg_color=(0.7, 0, 0, 1), size_hint=(1, 0.4))

        content.add_widget(lbl_congrats)
        content.add_widget(lbl_score)
        content.add_widget(btn_next)
        content.add_widget(btn_menu)

        popup = Popup(title="", content=content, size_hint=(0.8, 0.6), auto_dismiss=False, separator_height=0)
        
        # Bind tombol popup
        btn_next.bind(on_release=lambda x: self.next_level_action(popup))
        btn_menu.bind(on_release=lambda x: self.menu_action(popup))
        
        popup.open()

    def next_level_action(self, popup):
        popup.dismiss()
        self.level += 1
        self.question_num = 1
        # Animasi transisi reset
        self.next_question()

    def menu_action(self, popup):
        popup.dismiss()
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    def save_progress(self):
        try:
            app = App.get_running_app()
            if getattr(app, 'store', None):
                app.store.put('math_data', 
                              grade=app.selected_grade, 
                              level=self.level+1, # Simpan level berikutnya
                              score=self.total_score, 
                              mode=getattr(self, 'game_mode', 'tambah'))
        except Exception as e:
            log_exception(e, 'saving math_data')

    def quit_game(self):
        if self.timer_event: self.timer_event.cancel()
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

# ---------- App ----------
class MathApp(App):
    selected_grade = NumericProperty(3)
    grade_title = StringProperty("Kelas 3 SD")
    store = None

    def build(self):
        try:
            data_dir = self.user_data_dir
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)
            self.store = JsonStore(os.path.join(data_dir, 'math_data.json'))
        except Exception:
            self.store = None
        return Builder.load_string(kv_string)

    def set_grade(self, grade):
        self.selected_grade = grade
        titles = {3: "Kelas 3 SD", 5: "Kelas 5 SD", 8: "Kelas 8 SMP"}
        self.grade_title = f"{titles.get(grade, '')}"

    def load_game(self):
        if self.store and self.store.exists('math_data'):
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
        # Emergency logging to file if app crashes completely
        with open("crash_log.txt", "w") as f:
            f.write(traceback.format_exc())
