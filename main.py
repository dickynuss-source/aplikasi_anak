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

# Warna Background Gelap
Window.clearcolor = (0.1, 0.1, 0.1, 1)

# --- Desain UI (KV Language) ---
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

        # Tombol Resume
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
            size_hint: 1, 0.05 # Spacer

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
            color: 0.6, 0.6, 0.6, 1
            size_hint: 1, 0.1

        Label:
            text: "MATH MASTER"
            font_size: '35sp'
            bold: True
            color: 1, 0.84, 0, 1
            size_hint: 1, 0.2

        GridLayout:
            cols: 2
            spacing: 20
            size_hint: 1, 0.6
            
            MenuButton:
                text: "Tambah (+)"
                background_color: 0.2, 0.8, 0.2, 1
                on_release: 
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('tambah')
            
            MenuButton:
                text: "Kurang (-)"
                background_color: 0.8, 0.2, 0.2, 1
                on_release: 
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('kurang')

            MenuButton:
                text: "Kali (x)"
                background_color: 0.2, 0.2, 0.8, 1
                on_release: 
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('kali')

            MenuButton:
                text: "Bagi (:)"
                background_color: 0.8, 0.8, 0.2, 1
                on_release: 
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_game('bagi')
        
        Button:
            text: "<< Ganti Kelas"
            size_hint: 1, 0.1
            background_color: 0.3, 0.3, 0.3, 1
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

        # Info Bar
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

        Label:
            text: root.question_text
            font_size: '45sp'
            bold: True
            size_hint: 1, 0.35

        GridLayout:
            id: answer_grid
            cols: 2
            spacing: 15
            size_hint: 1, 0.45
'''

class GradeScreen(Screen):
    def on_enter(self):
        # Cek apakah store berhasil di-load
        app = App.get_running_app()
        if app.store and app.store.exists('math_game_data'):
            self.ids.btn_resume.disabled = False
            self.ids.btn_resume.background_color = (0.2, 0.6, 1, 1)
            try:
                data = app.store.get('math_game_data')
                self.ids.btn_resume.text = f"LANJUT: Kls {data['grade']} - Lvl {data['level']}"
            except:
                self.ids.btn_resume.text = "Data Corrupt"
        else:
            self.ids.btn_resume.disabled = True
            self.ids.btn_resume.text = "Tidak Ada Data Simpanan"

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
        self.current_anim = None
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

    def start_game(self, mode, is_loaded=False):
        self.game_mode = mode
        if not is_loaded:
            self.level = 1
            self.question_num = 1
            self.total_score = 0
            self.level_score = 0
        
        self.next_question()

    def next_question(self):
        if self.timer_event: self.timer_event.cancel()
        self.time_left = 20
        self.timer_text = str(self.time_left)
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        
        self.level_text = f"Level: {self.level}"
        self.score_text = f"Total: {self.total_score}"
        self.status_text = f"Soal {self.question_num}/10"
        self.generate_logic()

    def generate_logic(self):
        app = App.get_running_app()
        grade = app.selected_grade 
        
        num1, num2 = 0, 0
        ans = 0
        op_symbol = ""

        # --- LOGIKA SOAL ---
        if self.game_mode == 'tambah':
            multiplier = 10 if grade == 3 else (50 if grade == 5 else 100)
            base = 20 if grade == 3 else (50 if grade == 5 else 100)
            limit = base + (self.level * multiplier)
            
            num1 = random.randint(10, limit)
            num2 = random.randint(5, limit)
            ans = num1 + num2
            op_symbol = "+"

        elif self.game_mode == 'kurang':
            multiplier = 10 if grade == 3 else (50 if grade == 5 else 100)
            limit = (self.level * multiplier) + 20
            a = random.randint(10, limit)
            b = random.randint(5, limit)
            
            if grade == 8:
                num1, num2 = a, b 
            else:
                num1 = max(a, b)
                num2 = min(a, b)
                if num1 == num2: num1 += random.randint(1, 5)

            ans = num1 - num2
            op_symbol = "-"

        elif self.game_mode == 'kali':
            if grade == 3: limit = 10
            elif grade == 5: limit = 12 
            else: limit = 20

            num1 = random.randint(2, limit)
            
            if grade == 5:
                max_num2 = int(100 / num1)
                if max_num2 < 2: max_num2 = 2
                num2 = random.randint(2, max_num2)
            else:
                num2 = random.randint(2, limit)

            ans = num1 * num2
            op_symbol = "x"

        elif self.game_mode == 'bagi':
            if grade == 3:
                max_res = 10
                max_div = 10
            elif grade == 5:
                max_res = 10
                max_div = 10
            else:
                max_res = 25
                max_div = 20

            quotient = random.randint(2, max_res)
            divisor = random.randint(2, max_div)
            
            if grade == 5:
                while (divisor * quotient) > 100:
                    quotient = random.randint(2, 10)
                    divisor = random.randint(2, 10)

            num1 = divisor * quotient
            num2 = divisor
            ans = quotient
            op_symbol = ":"

        self.correct_answer = ans
        self.question_text = f"{num1} {op_symbol} {num2} = ?"

        # Generate Jawaban
        answers = [ans]
        while len(answers) < 4:
            offset = random.randint(-5, 5)
            if grade >= 5: offset = random.randint(-10, 10)
            fake = ans + offset
            if grade < 8 and fake < 0: fake = abs(fake)
            if fake != ans and fake not in answers:
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
            # Save Progres
            App.get_running_app().save_progress(
                self.level + 1,
                self.total_score,
                self.game_mode
            )
            
            if self.level >= 10:
                self.show_final_celebration()
            else:
                self.show_level_complete()
        else:
            self.question_num += 1
            self.next_question()

    def show_level_complete(self):
        stars = "⭐" * (1 if self.level_score < 7 else (2 if self.level_score < 10 else 3))
        msg = "Hebat!" if self.level_score >= 7 else "Ayo Lanjut!"
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        lbl_anim = Label(text=stars, font_size='50sp', size_hint=(1, 0.4))
        content.add_widget(lbl_anim)
        
        self.current_anim = Animation(font_size='70sp', duration=0.2) + Animation(font_size='50sp', duration=0.2)
        self.current_anim.repeat = True 
        self.current_anim.start(lbl_anim)

        content.add_widget(Label(text=msg, font_size='24sp', color=(1,1,0,1)))
        content.add_widget(Label(text=f"Skor Level: {self.level_score}/10", font_size='18sp'))
        
        btn_next = Button(text="LANJUT >>", size_hint=(1, 0.3), background_color=(0.2, 0.8, 0.2, 1))
        
        popup = Popup(title=f'Level {self.level} Selesai!', content=content, size_hint=(0.7, 0.5), auto_dismiss=False)

        def next_action(inst):
            if self.current_anim:
                self.current_anim.cancel(lbl_anim)
            popup.dismiss()
            self.level += 1
            self.question_num = 1
            self.level_score = 0
            self.next_question()

        btn_next.bind(on_release=next_action)
        content.add_widget(btn_next)
        popup.open()

    def show_final_celebration(self):
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        lbl_trophy = Label(text="🎉 🏆 🎉", font_size='60sp', size_hint=(1, 0.4))
        
        self.current_anim = Animation(font_size='80sp', duration=0.4) + Animation(font_size='60sp', duration=0.4)
        self.current_anim.repeat = True
        self.current_anim.start(lbl_trophy)
        
        lbl_msg = Label(
            text=f"LUAR BIASA!\nKAMU MENYELESAIKAN\nSEMUA LEVEL!", 
            font_size='22sp', 
            halign='center',
            bold=True,
            color=(1, 0.84, 0, 1)
        )
        
        anim_color = Animation(color=(1, 0, 0, 1), duration=0.5) + Animation(color=(0, 1, 0, 1), duration=0.5) + Animation(color=(0, 0, 1, 1), duration=0.5)
        anim_color.repeat = True
        anim_color.start(lbl_msg)

        btn_menu = Button(
            text="KEMBALI KE MENU", 
            size_hint=(1, 0.2), 
            background_color=(0.2, 0.6, 1, 1),
            bold=True
        )
        
        popup = Popup(
            title='🎉 CHAMPION! 🎉', 
            content=content, 
            size_hint=(0.9, 0.6), 
            auto_dismiss=False,
            separator_color=(1, 1, 0, 1)
        )
        
        def to_menu(inst):
            if self.current_anim:
                self.current_anim.cancel(lbl_trophy)
            anim_color.cancel(lbl_msg)
            popup.dismiss()
            App.get_running_app().clear_save()
            self.manager.current = 'grade' 
            
        btn_menu.bind(on_release=to_menu)
        
        content.add_widget(lbl_trophy)
        content.add_widget(lbl_msg)
        content.add_widget(Label(text=f"Total Skor: {self.total_score}", font_size='18sp'))
        content.add_widget(btn_menu)
        popup.open()

class MathApp(App):
    selected_grade = NumericProperty(3)
    grade_title = StringProperty("Kelas 3 SD")
    store = None # Inisialisasi awal None
    
    def build(self):
        # --- PERBAIKAN FATAL: SAFE STORAGE ---
        # Kita bungkus dalam Try-Except agar APK tidak crash kalau gagal load file
        try:
            data_dir = self.user_data_dir
            self.store = JsonStore(os.path.join(data_dir, 'math_game_data.json'))
        except Exception as e:
            print(f"Gagal memuat penyimpanan: {e}")
            self.store = None # Jika gagal, fitur save mati tapi game tetap jalan
        
        return Builder.load_string(kv_string)

    def set_grade(self, grade):
        self.selected_grade = grade
        titles = {3: "Kelas 3 SD", 5: "Kelas 5 SD", 8: "Kelas 8 SMP"}
        self.grade_title = f"Mode: {titles.get(grade, '')}"
    
    def save_progress(self, level, score, mode):
        # Hanya simpan jika store berhasil dimuat
        if self.store:
            try:
                self.store.put('math_game_data', 
                    grade=self.selected_grade,
                    level=level,
                    score=score,
                    mode=mode
                )
            except:
                pass # Abaikan error save agar tidak ganggu permainan

    def load_game(self):
        if self.store and self.store.exists('math_game_data'):
            data = self.store.get('math_game_data')
            self.set_grade(data['grade'])
            
            screen_manager = self.root
            screen_manager.current = 'game'
            game_screen = screen_manager.get_screen('game')
            
            game_screen.level = data['level']
            game_screen.total_score = data['score']
            game_screen.start_game(data['mode'], is_loaded=True)

    def clear_save(self):
        if self.store and self.store.exists('math_game_data'):
            self.store.delete('math_game_data')

if __name__ == '__main__':
    MathApp().run()
