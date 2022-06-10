from database import Database
from datetime import datetime
from temporary import Connection
from kivy.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.picker import MDDatePicker
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import SlideTransition


conn = Connection().get()
db = Database(conn['login'], conn['password'])

class Add_customer(BoxLayout):
    def __init__(self, app):
        super().__init__()
        self.__app = app

        self.orientation = 'vertical'

        name = BoxLayout(padding=50, size_hint=(1, 0.2))
        contact = BoxLayout(padding=50, size_hint=(1, 0.2))
        owner_name = BoxLayout(padding=50, size_hint=(1, 0.2))
        started = BoxLayout(padding=50, size_hint=(1, 0.2))

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
            text='Contact', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        self.contact = TextInput(
            multiline=False,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(1.5, 5)
        )

        contact.add_widget(lbl)
        contact.add_widget(self.contact)

        lbl = Label(
            text='Owner name', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        self.owner_name = TextInput(
            multiline=False,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(1.5, 5)
        )

        owner_name.add_widget(lbl)
        owner_name.add_widget(self.owner_name)

        lbl = Label(
            text='Cooperation started', 
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

        started.add_widget(lbl)
        started.add_widget(self.accepted)

        return_btn = Button(text="Return")
        return_btn.bind(on_press=self.exit)

        add_btn = Button(text="Add")
        add_btn.bind(on_press=self.add)
        
        buttons = BoxLayout(padding=20, pos_hint={"center_y": 0.5, "center_x": 0.5}, size_hint=(1, .15))
        buttons.add_widget(return_btn)
        buttons.add_widget(add_btn)

        self.error = Label(text='', color='red', font_size=30, size_hint=(1, 0.08))

        self.add_widget(name)
        self.add_widget(owner_name)
        self.add_widget(contact)
        self.add_widget(started)
        self.add_widget(self.error)
        self.add_widget(buttons)

    def exit(self, instance):
        self.name.text = ''
        self.contact.text = ''
        self.owner_name.text = ''
        date_now = datetime.now()
        self.accepted.text = f"{date_now.month}-{date_now.day}-{date_now.year}"
        self.error.text = ''
        self.__app.screen_manager.transition = SlideTransition(direction = 'up')
        self.__app.screen_manager.current = 'customers'

    def add(self, instance):
        if not self.name.text == '' and not self.contact.text == '' and not self.owner_name.text == '':
            self.error.text = ''
            db.add_customer(self.name.text, self.contact.text, self.owner_name.text, self.accepted.text)

            self.name.text = ''
            self.contact.text = ''
            self.owner_name.text = ''
            date_now = datetime.now()
            self.accepted.text = f'{date_now.month}-{date_now.day}-{date_now.year}'
            self.__app.screen_manager.transition = SlideTransition(direction = 'up')
            self.__app.screen_manager.current = 'customers'
        else:
            self.error.text = 'Fill in all the fields!'

    def set_date(self, instance):
        date = MDDatePicker()
        date.bind(on_save=self.update_date)
        date.open()

    def update_date(self, instance, value, date_range):
        date: datetime = value
        self.accepted.text = f"{date.month}-{date.day}-{date.year}"