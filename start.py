from database import Database
from temporary import Connection
from kivy.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import SlideTransition

class Start(BoxLayout):
    def __init__(self, app):
        super().__init__()
        self.__app = app
        self.orientation = 'vertical'

        login = BoxLayout(padding=50, size_hint=(1, 0.3))
        passwd = BoxLayout(padding=50, size_hint=(1, 0.3))

        lbl = Label(
            text='Login', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        self.log = TextInput(
            multiline=False,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(1.5, 0.4)
        )

        login.add_widget(lbl)
        login.add_widget(self.log)

        lbl = Label(
            text='Password', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        self.pas = TextInput(
            multiline=False,
            password=True,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(1.5, 0.4)
        )

        passwd.add_widget(lbl)
        passwd.add_widget(self.pas)

        connect_btn = Button(text="Connect database")
        connect_btn.bind(on_press=self.update_date)
        
        buttons = BoxLayout(padding=20, pos_hint={"center_y": 0.5, "center_x": 0.5}, size_hint=(1, .15))
        buttons.add_widget(connect_btn)

        self.error = Label(text='', color='red', font_size=30, size_hint=(1, 0.08))

        self.add_widget(login)
        self.add_widget(passwd)
        self.add_widget(self.error)
        self.add_widget(buttons)

    def update_date(self, instance):
        conn = Database(self.log.text, self.pas.text)
        if conn.success_connection:
            conn = Connection()
            conn.set(self.log.text, self.pas.text)

            self.__app.screen_manager.transition = SlideTransition(direction = 'up')
            self.__app.screen_manager.current = 'employees'
        else:
            self.error.text = 'ERROR'