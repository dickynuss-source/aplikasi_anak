import random
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.storage.jsonstore import JsonStore

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

class GradeScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        if app.store and app.store.exists('math_data'):
            try:
                data = app.store.get('math_data')
                self.ids.btn_resume.disabled = False
                self.ids.btn_resume.text = f"LANJUT: Kls {data['grade']} - Level {data['level']}"
            except:
                self.ids.btn_resume.disabled = True
        else:
            self.ids.btn_resume.disabled = True


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
        if 'answer_grid' not in self.ids:
            Clock.schedule_once(self.setup_buttons, 0.1)
            return

        grid = self.ids.answer_grid
        grid.clear_widgets()
        self.buttons = []

        for _ in range(4):
            btn = Button(
                text="",
                font_size='28sp',
                background_normal='',
                background_color=(0.2, 0.6, 1, 1)
            )
            btn.bind(on_release=self.check_answer)
            self.buttons.append(btn)
            grid.add_widget(btn)

    def start_game(self, mode, is_resume=False):
        self.game_mode = mode
        if not is_resume:
            self.level = 1
            self.total_score = 0
            self.level_score = 0
            self.question_num = 1
        self.next_question()

    def next_question(self):
        if self.timer_event:
            self.timer_event.cancel()

        self.time_left = 20
        self.timer_text = str(self.time_left)
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

        self.level_text = f"Level: {self.level}"
        self.score_text = f"Total: {self.total_score}"
        self.status_text = f"Soal {self.question_num}/10"

        self.generate_question()

    def generate_question(self):
        app = App.get_running_app()
        grade = app.selected_grade

        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        ans = num1 + num2
        symbol = "+"

        if self.game_mode == 'kurang':
            num1, num2 = max(num1, num2), min(num1, num2)
            ans = num1 - num2
            symbol = "-"
        elif self.game_mode == 'kali':
            ans = num1 * num2
            symbol = "x"
        elif self.game_mode == 'bagi':
            num2 = random.randint(1, 10)
            ans = random.randint(1, 10)
            num1 = num2 * ans
            symbol = ":"

        self.correct_answer = ans
        self.question_text = f"{num1} {symbol} {num2} = ?"

        answers = [ans]
        while len(answers) < 4:
            fake = ans + random.randint(-10, 10)
            if fake != ans:
                answers.append(fake)

        random.shuffle(answers)

        for i, btn in enumerate(self.buttons):
            btn.text = f"{chr(65+i)}. {answers[i]}"
            btn.disabled = False
            btn.background_color = (0.2, 0.6, 1, 1)

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_text = str(self.time_left)
        if self.time_left <= 0:
            self.check_answer(None, timeout=True)

    def check_answer(self, instance, timeout=False):
        if self.timer_event:
            self.timer_event.cancel()

        if instance and not timeout:
            try:
                val = int(instance.text.split(". ")[1])
                if val == self.correct_answer:
                    self.total_score += 1
                    instance.background_color = (0, 1, 0, 1)
                else:
                    instance.background_color = (1, 0, 0, 1)
            except:
                pass

        for btn in self.buttons:
            btn.disabled = True

        Clock.schedule_once(self.next_step, 1)

    def next_step(self, dt):
        if self.question_num >= 10:
            self.manager.current = 'menu'
        else:
            self.question_num += 1
            self.next_question()


class MathApp(App):
    selected_grade = NumericProperty(3)
    grade_title = StringProperty("Kelas 3 SD")

    def build(self):
        try:
            data_dir = self.user_data_dir
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            self.store = JsonStore(os.path.join(data_dir, 'math_data.json'))
        except:
            self.store = None

        return Builder.load_string(kv_string)

    def set_grade(self, grade):
        self.selected_grade = grade
        self.grade_title = f"Kelas {grade}"

    def load_game(self):
        if self.store and self.store.exists('math_data'):
            data = self.store.get('math_data')
            self.set_grade(data['grade'])
            self.root.current = 'game'


if __name__ == '__main__':
    MathApp().run()
