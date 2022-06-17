from database import Database
from datetime import datetime
from rules import Rules
from temporary import Connection
from kivy.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.picker import MDDatePicker
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import SlideTransition

rules = Rules()
conn = Connection().get()
db = Database(conn['login'], conn['password'])

class Add_employee(BoxLayout):
    def __init__(self, app):
        super().__init__()
        self.__app = app

        self.orientation = 'vertical'

        name = BoxLayout(padding=50, size_hint=(1, 0.2))
        age = BoxLayout(padding=50, size_hint=(1, 0.2))
        accepted = BoxLayout(padding=50, size_hint=(1, 0.2))
        level = BoxLayout(padding=50, size_hint=(1, 0.2))

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
            size_hint=(1.5, 5)
        )

        name.add_widget(lbl)
        name.add_widget(self.name)

        lbl = Label(
            text='Age', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        self.age = TextInput(
            multiline=False,
            input_filter= 'int',
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(1.5, 5)
        )

        age.add_widget(lbl)
        age.add_widget(self.age)

        lbl = Label(
            text='Accepted', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        date_now = datetime.now()

        self.accepted = Button(
            text=f"{date_now.month}-{date_now.day}-{date_now.year}",
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(None, None),
            size=(400, 50),
        )
        self.accepted.bind(on_press=self.set_date)

        accepted.add_widget(lbl)
        accepted.add_widget(self.accepted)

        lbl = Label(
            text='Level', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        values = [i[0] for i in db.get_levels_name()]
        values = tuple(values)
        self.level = Spinner(
            text='Level',
            values=values,
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={'center_x': .5, 'center_y': .5})

        level.add_widget(lbl)
        level.add_widget(self.level)

        return_btn = Button(text="Return")
        return_btn.bind(on_press=self.exit)

        add_btn = Button(text="Add")
        add_btn.bind(on_press=self.add)
        
        buttons = BoxLayout(padding=20, pos_hint={"center_y": 0.5, "center_x": 0.5}, size_hint=(1, .15))
        buttons.add_widget(return_btn)
        buttons.add_widget(add_btn)

        self.error = Label(text='', color='red', font_size=30, size_hint=(1, 0.08))

        self.add_widget(name)
        self.add_widget(age)
        self.add_widget(accepted)
        self.add_widget(level)
        self.add_widget(self.error)
        self.add_widget(buttons)

    def exit(self, instance):
        self.error.text = ''
        self.name.text = ''
        self.age.text = ''
        self.level.text == 'Level'
        date_now = datetime.now()
        self.accepted.text = f"{date_now.month}-{date_now.day}-{date_now.year}"
        self.__app.screen_manager.transition = SlideTransition(direction = 'up')
        self.__app.screen_manager.current = 'employees'

    def add(self, instance):
        if not self.name.text == '' and not self.age.text == '' and not self.level.text == 'Level':

            if rules.age(int(self.age.text)):
                self.error.text = 'Employee too young!'
                return
            
            db.add_employee(self.name.text, self.level.text, int(self.age.text), self.accepted.text)

            self.error.text = ''
            self.name.text = ''
            self.age.text = ''
            self.level.text == 'Level'
            date_now = datetime.now()
            self.accepted.text = f"{date_now.month}-{date_now.day}-{date_now.year}"
            self.__app.screen_manager.transition = SlideTransition(direction = 'up')
            self.__app.screen_manager.current = 'employees'
        else:
            self.error.text = 'Fill in all the fields!'

    def set_date(self, instance):
        date = MDDatePicker()
        date.bind(on_save=self.update_date)
        date.open()

    def update_date(self, instance, value, date_range):
        date: datetime = value
        self.accepted.text = f"{date.month}-{date.day}-{date.year}"