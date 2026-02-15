import random
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty

# Warna Background Gelap (Agar mata nyaman)
Window.clearcolor = (0.1, 0.1, 0.1, 1)

# --- Desain UI (KV Language) ---
kv_string = '''
ScreenManager:
    MenuScreen:
    GameScreen:

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 20
        
        Label:
            text: "JAGO MATEMATIKA"
            font_size: '32sp'
            bold: True
            color: 1, 0.8, 0, 1  # Warna Emas
            size_hint: 1, 0.3

        GridLayout:
            cols: 2
            spacing: 20
            size_hint: 1, 0.7
            
            MenuButton:
                text: "Penjumlahan (+)"
                background_color: 0.2, 0.8, 0.2, 1
                on_release: 
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('tambah')
            
            MenuButton:
                text: "Pengurangan (-)"
                background_color: 0.8, 0.2, 0.2, 1
                on_release: 
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('kurang')

            MenuButton:
                text: "Perkalian (x)"
                background_color: 0.2, 0.2, 0.8, 1
                on_release: 
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('kali')

            MenuButton:
                text: "Pembagian (:)"
                background_color: 0.8, 0.8, 0.2, 1
                on_release: 
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('bagi')

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

        # Info Bar (Level, Timer, Skor Total)
        GridLayout:
            cols: 3
            size_hint: 1, 0.1
            Label:
                text: root.level_text
                color: 1, 1, 0, 1
                bold: True
            Label:
                text: root.timer_text
                font_size: '24sp'
                bold: True
                color: 1, 1, 1, 1
            Label:
                text: root.score_text
                color: 0, 1, 0, 1
                bold: True
        
        Label:
            text: root.status_text
            size_hint: 1, 0.1
            color: 0.7, 0.7, 0.7, 1

        # Area Soal
        Label:
            text: root.question_text
            font_size: '45sp'
            bold: True
            size_hint: 1, 0.35

        # Grid Tombol Jawaban
        GridLayout:
            id: answer_grid
            cols: 2
            spacing: 15
            size_hint: 1, 0.45
'''

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
        self.game_mode = 'tambah'
        self.level = 1
        self.question_num = 1
        self.total_score = 0
        self.level_score = 0
        self.time_left = 20
        self.timer_event = None
        self.buttons = []
        
        Clock.schedule_once(self.setup_buttons)

    def setup_buttons(self, dt):
        grid = self.ids.answer_grid
        for i in range(4):
            btn = Button(
                text="", 
                font_size='28sp', 
                background_normal='',
                background_color=(0.2, 0.6, 1, 1),
                bold=True
            )
            btn.bind(on_release=self.check_answer)
            self.buttons.append(btn)
            grid.add_widget(btn)

    def start_game(self, mode):
        self.game_mode = mode
        self.level = 1
        self.question_num = 1
        self.total_score = 0
        self.level_score = 0
        self.next_question()

    def next_question(self):
        # Reset Timer
        if self.timer_event: self.timer_event.cancel()
        self.time_left = 20
        self.timer_text = str(self.time_left)
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        
        # Update Info UI
        self.level_text = f"Level: {self.level}"
        self.score_text = f"Total: {self.total_score}"
        self.status_text = f"Soal {self.question_num}/10"

        # Generate Logic
        self.generate_logic()

    def generate_logic(self):
        num1, num2 = 0, 0
        ans = 0
        op_symbol = ""

        # Logika Tingkat Kesulitan
        if self.game_mode == 'tambah':
            limit = 10 + (self.level * 9)
            num1 = random.randint(1, limit)
            num2 = random.randint(1, limit)
            ans = num1 + num2
            op_symbol = "+"
            
        elif self.game_mode == 'kurang':
            limit = 15 + (self.level * 8)
            a = random.randint(5, limit)
            b = random.randint(1, a)
            num1, num2 = a, b
            ans = num1 - num2
            op_symbol = "-"
            
        elif self.game_mode == 'kali':
            min_n = 1
            max_n = min(9, 2 + self.level)
            num1 = random.randint(min_n, max_n)
            num2 = random.randint(min_n, max_n)
            ans = num1 * num2
            op_symbol = "x"
            
        elif self.game_mode == 'bagi':
            divisor = random.randint(2, 9)
            max_quotient = 10 + self.level
            quotient = random.randint(1, max_quotient)
            while (divisor * quotient) > 99:
                quotient = random.randint(1, max_quotient)
            num1 = divisor * quotient
            num2 = divisor
            ans = quotient
            op_symbol = ":"

        self.correct_answer = ans
        self.question_text = f"{num1} {op_symbol} {num2} = ?"

        # Pilihan Jawaban
        answers = [ans]
        while len(answers) < 4:
            offset = random.randint(-5, 5)
            fake = ans + offset
            if fake >= 0 and fake not in answers:
                answers.append(fake)
        
        random.shuffle(answers)
        
        opts = ['A', 'B', 'C', 'D']
        for i, btn in enumerate(self.buttons):
            btn.text = f"{opts[i]}. {answers[i]}"
            btn.disabled = False
            btn.background_color = (0.2, 0.6, 1, 1)

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_text = str(self.time_left)
        if self.time_left <= 0:
            self.check_answer(None, timeout=True)

    def check_answer(self, instance, timeout=False):
        if self.timer_event: self.timer_event.cancel()

        correct = False
        if not timeout:
            val = int(instance.text.split('. ')[1])
            if val == self.correct_answer:
                correct = True
                self.total_score += 1
                self.level_score += 1
                instance.background_color = (0, 1, 0, 1)
            else:
                instance.background_color = (1, 0, 0, 1)
        
        for btn in self.buttons:
            val = int(btn.text.split('. ')[1])
            if val == self.correct_answer:
                if timeout: btn.background_color = (0, 1, 0, 1)
            btn.disabled = True
            
        Clock.schedule_once(self.finish_step, 1.0)

    def finish_step(self, dt):
        if self.question_num >= 10:
            self.show_level_complete()
        else:
            self.question_num += 1
            self.next_question()

    def show_level_complete(self):
        stars = ""
        msg = ""
        color = (1, 1, 1, 1)
        
        if self.level_score == 10:
            stars = "⭐⭐⭐"
            msg = "SEMPURNA!\nKamu Luar Biasa!"
            color = (0, 1, 0, 1)
        elif self.level_score >= 7:
            stars = "⭐⭐"
            msg = "HEBAT!\nTerus Pertahankan!"
            color = (1, 1, 0, 1)
        else:
            stars = "⭐"
            msg = "BAGUS!\nAyo Belajar Lagi!"
            color = (1, 0.5, 0, 1)

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        lbl_stars = Label(text=stars, font_size='40sp', size_hint=(1, 0.3))
        lbl_msg = Label(text=msg, font_size='20sp', halign='center', color=color)
        lbl_score = Label(text=f"Benar: {self.level_score}/10", font_size='18sp', color=(0.8, 0.8, 0.8, 1))
        
        btn_next = Button(
            text="Level Berikutnya >>", 
            size_hint=(1, 0.3),
            background_color=(0.2, 0.6, 1, 1),
            bold=True
        )
        
        popup = Popup(
            title=f'Level {self.level} Selesai', 
            content=content, 
            size_hint=(0.8, 0.5), 
            auto_dismiss=False
        )

        def next_action(inst):
            popup.dismiss()
            self.level += 1
            self.question_num = 1
            self.level_score = 0
            
            if self.level > 10:
                self.game_over()
            else:
                self.next_question()

        btn_next.bind(on_release=next_action)
        
        content.add_widget(lbl_stars)
        content.add_widget(lbl_msg)
        content.add_widget(lbl_score)
        content.add_widget(btn_next)
        popup.open()

    def game_over(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(
            text=f"TAMAT!\nTotal Skor Akhir: {self.total_score}", 
            font_size='20sp',
            halign='center'
        ))
        btn = Button(
            text="Ke Menu Utama", 
            size_hint=(1, 0.4),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        
        popup = Popup(title='Permainan Selesai', content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        
        def to_menu(inst):
            popup.dismiss()
            self.manager.current = 'menu'
            
        btn.bind(on_release=to_menu)
        content.add_widget(btn)
        popup.open()

class MathApp(App):
    def build(self):
        return Builder.load_string(kv_string)

if __name__ == '__main__':
    MathApp().run()
