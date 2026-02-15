# main.py (REPLACE YOUR OLD main.py WITH THIS)
import random
import os
import sys
import traceback
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty
from kivy.storage.jsonstore import JsonStore

# Dark background
Window.clearcolor = (0.1, 0.1, 0.1, 1)

kv_string = '''
ScreenManager:
    GradeScreen:
    MenuScreen:
    GameScreen:

<GradeScreen>:
    name: 'grade'
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 20

        Label:
            text: "PILIH KELAS"
            font_size: '30sp'
            bold: True
            color: 0.2, 0.8, 1, 1
            size_hint: 1, 0.2

        Button:
            id: btn_resume
            text: "LANJUTKAN GAME TERAKHIR"
            font_size: '18sp'
            background_color: 0.5, 0.5, 0.5, 1
            size_hint: 1, 0.15
            disabled: True
            on_release:
                app.load_game()

        Label:
            size_hint: 1, 0.05

        Button:
            text: "KELAS 3 SD"
            font_size: '20sp'
            background_color: 0.2, 0.8, 0.2, 1
            on_release:
                app.set_grade(3)
                root.manager.current = 'menu'

        Button:
            text: "KELAS 5 SD"
            font_size: '20sp'
            background_color: 1, 0.8, 0, 1
            on_release:
                app.set_grade(5)
                root.manager.current = 'menu'

        Button:
            text: "KELAS 8 SMP"
            font_size: '20sp'
            background_color: 0.8, 0.2, 0.2, 1
            on_release:
                app.set_grade(8)
                root.manager.current = 'menu'

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 15

        Label:
            text: app.grade_title
            font_size: '20sp'
            size_hint: 1, 0.1

        Label:
            text: "MATH MASTER"
            font_size: '35sp'
            bold: True
            size_hint: 1, 0.2

        GridLayout:
            cols: 2
            spacing: 20
            size_hint: 1, 0.6

            MenuButton:
                text: "Tambah (+)"
                on_release:
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('tambah')

            MenuButton:
                text: "Kurang (-)"
                on_release:
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('kurang')

            MenuButton:
                text: "Kali (x)"
                on_release:
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('kali')

            MenuButton:
                text: "Bagi (:)"
                on_release:
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('bagi')

        Button:
            text: "<< Ganti Kelas"
            size_hint: 1, 0.1
            on_release: root.manager.current = 'grade'

<MenuButton@Button>:
    font_size: '18sp'
    bold: True
    background_normal: ''

<GameScreen>:
    name: 'game'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        GridLayout:
            cols: 3
            size_hint: 1, 0.1
            Label:
                text: root.level_text
            Label:
                text: root.timer_text
                font_size: '24sp'
            Label:
                text: root.score_text

        Label:
            text: root.status_text
            size_hint: 1, 0.1

        Label:
            text: root.question_text
            font_size: '45sp'
            size_hint: 1, 0.35

        GridLayout:
            id: answer_grid
            cols: 2
            spacing: 15
            size_hint: 1, 0.45
'''

# ---------- helper logging ----------
def write_local_log(msg):
    """Write a line to app_debug.log in user_data_dir if available."""
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
        # if even logging fails, silently ignore to avoid recursion
        pass

def log_exception(exc: Exception, where: str = ''):
    tb = traceback.format_exc()
    write_local_log(f"EXCEPTION at {where}: {repr(exc)}")
    write_local_log(tb)

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
                    btn.text = f"LANJUT: Kls {data.get('grade', '?')} - Level {data.get('level', '?')}"
            else:
                btn = self.ids.get('btn_resume', None)
                if btn:
                    btn.disabled = True
        except Exception as e:
            log_exception(e, 'GradeScreen.on_enter')

class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    level_text = StringProperty("Level: 1")
    timer_text = StringProperty("20")
    score_text = StringProperty("Total: 0")
    status_text = StringProperty("Soal 1/10")
    question_text = StringProperty("Siap?")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons = []
        self.level = 1
        self.total_score = 0
        self.level_score = 0
        self.question_num = 1
        self.time_left = 20
        self.correct_answer = 0
        self.timer_event = None
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
                btn = Button(text="", font_size='28sp', background_normal='', background_color=(0.2,0.6,1,1))
                btn.bind(on_release=self.check_answer)
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
                self.level_score = 0
                self.question_num = 1
            write_local_log(f"start_game mode={mode} is_resume={is_resume}")
            self.next_question()
        except Exception as e:
            log_exception(e, 'GameScreen.start_game')

    def next_question(self):
        try:
            if self.timer_event:
                try:
                    self.timer_event.cancel()
                except Exception:
                    pass
            self.time_left = 20
            self.timer_text = str(self.time_left)
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
            self.level_text = f"Level: {self.level}"
            self.score_text = f"Total: {self.total_score}"
            self.status_text = f"Soal {self.question_num}/10"
            self.generate_question()
        except Exception as e:
            log_exception(e, 'GameScreen.next_question')

    def generate_question(self):
        try:
            app = App.get_running_app()
            grade = getattr(app, 'selected_grade', 3) if app else 3

            # generate based on mode (kept simple & safe)
            if getattr(self, 'game_mode', 'tambah') == 'tambah':
                num1 = random.randint(1, 50)
                num2 = random.randint(1, 50)
                ans = num1 + num2
                symbol = '+'
            elif self.game_mode == 'kurang':
                a = random.randint(1,50)
                b = random.randint(1,50)
                num1, num2 = max(a,b), min(a,b)
                ans = num1 - num2
                symbol = '-'
            elif self.game_mode == 'kali':
                num1 = random.randint(2,12)
                num2 = random.randint(2,12)
                ans = num1 * num2
                symbol = 'x'
            elif self.game_mode == 'bagi':
                num2 = random.randint(2,10)
                quotient = random.randint(2,10)
                num1 = num2 * quotient
                ans = quotient
                symbol = ':'
            else:
                num1 = random.randint(1,20)
                num2 = random.randint(1,20)
                ans = num1 + num2
                symbol = '+'

            self.correct_answer = ans
            self.question_text = f"{num1} {symbol} {num2} = ?"

            answers = [ans]
            while len(answers) < 4:
                fake = ans + random.randint(-10, 10)
                if fake != ans and fake not in answers:
                    if fake < 0 and grade < 8:
                        fake = abs(fake)
                    answers.append(fake)
            random.shuffle(answers)

            for i, btn in enumerate(self.buttons):
                try:
                    btn.text = f"{chr(65+i)}. {answers[i]}"
                    btn.disabled = False
                    btn.background_color = (0.2,0.6,1,1)
                except Exception:
                    # if buttons not ready, schedule regenerate
                    Clock.schedule_once(lambda dt: self.generate_question(), 0.05)
                    return
        except Exception as e:
            log_exception(e, 'GameScreen.generate_question')

    def update_timer(self, dt):
        try:
            self.time_left -= 1
            self.timer_text = str(self.time_left)
            if self.time_left <= 0:
                # call check_answer with timeout
                self.check_answer(None, timeout=True)
        except Exception as e:
            log_exception(e, 'GameScreen.update_timer')

    def check_answer(self, instance, timeout=False):
        try:
            if self.timer_event:
                try:
                    self.timer_event.cancel()
                except Exception:
                    pass

            correct = False
            if not timeout and instance is not None:
                try:
                    parts = instance.text.split(". ", 1)
                    if len(parts) >= 2:
                        val = int(parts[1].strip())
                        if val == self.correct_answer:
                            correct = True
                            self.total_score += 1
                            self.level_score += 1
                            instance.background_color = (0,1,0,1)
                        else:
                            instance.background_color = (1,0,0,1)
                except Exception:
                    # parsing error -> mark red but don't crash
                    try:
                        instance.background_color = (1,0,0,1)
                    except Exception:
                        pass

            # reveal correct & disable
            for btn in self.buttons:
                try:
                    parts = btn.text.split(". ", 1)
                    if len(parts) >= 2:
                        val = int(parts[1].strip())
                        if val == self.correct_answer and timeout:
                            btn.background_color = (0,1,0,1)
                except Exception:
                    pass
                try:
                    btn.disabled = True
                except Exception:
                    pass

            # schedule finish
            Clock.schedule_once(self.finish_step, 1.0)
        except Exception as e:
            log_exception(e, 'GameScreen.check_answer')

    def finish_step(self, dt):
        try:
            if self.question_num >= 10:
                # save and go to menu safely
                try:
                    app = App.get_running_app()
                    if getattr(app, 'store', None):
                        try:
                            app.store.put('math_data', grade=app.selected_grade, level=self.level+1, score=self.total_score, mode=getattr(self, 'game_mode', 'tambah'))
                        except Exception as e:
                            log_exception(e, 'saving math_data')
                except Exception:
                    pass
                # for now go back to menu
                self.manager.current = 'menu'
            else:
                self.question_num += 1
                self.next_question()
        except Exception as e:
            log_exception(e, 'GameScreen.finish_step')

# ---------- App ----------
class MathApp(App):
    selected_grade = NumericProperty(3)
    grade_title = StringProperty("Kelas 3 SD")
    store = None

    def build(self):
        try:
            data_dir = self.user_data_dir
            write_local_log(f"user_data_dir: {data_dir}")
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)
            try:
                self.store = JsonStore(os.path.join(data_dir, 'math_data.json'))
            except Exception as e:
                log_exception(e, 'JsonStore.init')
                self.store = None
        except Exception as e:
            log_exception(e, 'MathApp.build (outer)')
            self.store = None

        return Builder.load_string(kv_string)

    def set_grade(self, grade):
        try:
            self.selected_grade = grade
            titles = {3: "Kelas 3 SD", 5: "Kelas 5 SD", 8: "Kelas 8 SMP"}
            self.grade_title = f"Mode: {titles.get(grade, '')}"
        except Exception as e:
            log_exception(e, 'MathApp.set_grade')

    def load_game(self):
        try:
            if self.store and self.store.exists('math_data'):
                data = self.store.get('math_data')
                self.set_grade(data.get('grade', 3))
                # switch screen safely
                try:
                    self.root.current = 'game'
                    game_screen = self.root.get_screen('game')
                    game_screen.level = data.get('level', 1)
                    game_screen.total_score = data.get('score', 0)
                    game_screen.start_game(data.get('mode', 'tambah'), is_resume=True)
                except Exception as e:
                    log_exception(e, 'MathApp.load_game -> screen ops')
        except Exception as e:
            log_exception(e, 'MathApp.load_game (outer)')

# ---------- Run with global exception capture ----------
def run_app():
    try:
        MathApp().run()
    except Exception as e:
        # Capture any uncaught exception and write full traceback to file
        tb = traceback.format_exc()
        try:
            # try write to user_data_dir if possible
            app = App.get_running_app()
            if app:
                data_dir = getattr(app, 'user_data_dir', None) or app.user_data_dir
            else:
                data_dir = os.path.expanduser('~')
        except Exception:
            data_dir = os.path.expanduser('~')
        try:
            if not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)
            logf = os.path.join(data_dir, 'app_debug.log')
            with open(logf, 'a', encoding='utf-8') as f:
                f.write("UNCAUGHT APP EXCEPTION:\n")
                f.write(tb + '\n')
        except Exception:
            # final fallback: print to stderr
            sys.stderr.write(tb)

if __name__ == '__main__':
    run_app()
