from database import Database
from rules import Rules
from temporary import Connection
from kivy.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import SlideTransition

conn = Connection().get()
db = Database(conn['login'], conn['password'])
rules = Rules()

class Add_level(BoxLayout):
    def __init__(self, app):
        super().__init__()
        self.__app = app

        self.orientation = 'vertical'

        login = BoxLayout(padding=50, size_hint=(1, 0.3))
        passwd = BoxLayout(padding=50, size_hint=(1, 0.3))

        lbl = Label(
            text='Name', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        self.name = TextInput(
            multiline=False,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(1.5, 0.4)
        )

        login.add_widget(lbl)
        login.add_widget(self.name)

        lbl = Label(
            text='Salary', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        self.salary = TextInput(
            multiline=False,
            input_filter= 'int',
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(1.5, 0.4)
        )

        passwd.add_widget(lbl)
        passwd.add_widget(self.salary)

        return_btn = Button(text="Return")
        return_btn.bind(on_press=self.exit)

        add_btn = Button(text="Add")
        add_btn.bind(on_press=self.add)
        
        buttons = BoxLayout(padding=20, pos_hint={"center_y": 0.5, "center_x": 0.5}, size_hint=(1, .15))
        buttons.add_widget(return_btn)
        buttons.add_widget(add_btn)

        self.error = Label(text='', color='red', font_size=30, size_hint=(1, 0.08))

        self.add_widget(login)
        self.add_widget(passwd)
        self.add_widget(self.error)
        self.add_widget(buttons)

    def exit(self, instance):
        self.name.text = ''
        self.salary.text = ''
        self.error.text = ''

        self.__app.screen_manager.transition = SlideTransition(direction = 'up')
        self.__app.screen_manager.current = 'levels'

    def add(self, instance):
        if not self.name.text == '' and not self.salary.text == '':

            if rules.min_averange(self.name.text, int(self.salary.text)):
                self.error.text = 'Min averange salary is 2500$'
                return

            if rules.max_salary(int(self.salary.text)):
                self.error.text = 'Max salary is 10000$'
                return

            if rules.check_salarys(self.name.text, int(self.salary.text)):
                self.error.text = 'Is not correct salary!'
                return

            if self.name.text == 'Middle' or self.name.text == 'Senior' or self.name.text == 'Junior':
                db.add_level(self.name.text, int(self.salary.text))
            else:
                self.error.text = "Invalid name!"
                return

            self.error.text = ''
            self.name.text = ''
            self.salary.text = ''

            self.__app.screen_manager.transition = SlideTransition(direction = 'up')
            self.__app.screen_manager.current = 'levels'
        else:
            self.error.text = 'Fill in all the fields!'

