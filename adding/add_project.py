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

conn = Connection().get()
db = Database(conn['login'], conn['password'])
rules = Rules()

class Add_Project(BoxLayout):
    def __init__(self, app):
        super().__init__()
        self.__app = app

        self.orientation = 'vertical'

        name = BoxLayout(padding=50, size_hint=(1, 0.4))
        task = BoxLayout(padding=50, size_hint=(1, 0.4))
        price = BoxLayout(padding=50, size_hint=(1, 0.4))
        customer = BoxLayout(padding=50, size_hint=(1, 0.2))
        started = BoxLayout(padding=50, size_hint=(1, 0.2))

        lbl = Label(
            text='Project name', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        self.name = TextInput(
            multiline=False,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(1.5, 4)
        )

        name.add_widget(lbl)
        name.add_widget(self.name)

        lbl = Label(
            text='Technical task', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        self.task = TextInput(
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(1.5, 8)
        )

        task.add_widget(lbl)
        task.add_widget(self.task)

        lbl = Label(
            text='Price', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        self.price = TextInput(
            multiline=False,
            input_filter= 'int',
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(1.5, 4)
        )

        price.add_widget(lbl)
        price.add_widget(self.price)

        lbl = Label(
            text='Customer', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        values = [i[0] for i in db.get_customers_name()]
        values = tuple(values)
        self.customer = Spinner(
            text='Customer',
            values=values,
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={'center_x': .5, 'center_y': .5})

        customer.add_widget(lbl)
        customer.add_widget(self.customer)

        lbl = Label(
            text='Project started', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        date_now = datetime.now()

        self.started = Button(
            text=f"{date_now.month}-{date_now.day}-{date_now.year}",
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(None, None),
            size=(400, 50),
        )
        self.started.bind(on_press=self.set_date)

        started.add_widget(lbl)
        started.add_widget(self.started)

        return_btn = Button(text="Return")
        return_btn.bind(on_press=self.exit)

        add_btn = Button(text="Add")
        add_btn.bind(on_press=self.add)
        
        buttons = BoxLayout(padding=20, pos_hint={"center_y": 0.5, "center_x": 0.5}, size_hint=(1, .3))
        buttons.add_widget(return_btn)
        buttons.add_widget(add_btn)

        self.error = Label(text='', color='red', font_size=30, size_hint=(1, 0.08))

        self.add_widget(name)
        self.add_widget(task)
        self.add_widget(price)
        self.add_widget(customer)
        self.add_widget(started)
        self.add_widget(self.error)
        self.add_widget(buttons)

    def exit(self, instance):
        self.name.text = ''
        self.task.text = ''
        self.price.text = ''
        date_now = datetime.now()
        self.started.text = f"{date_now.month}-{date_now.day}-{date_now.year}"
        self.customer.text = 'Customer'

        self.__app.screen_manager.transition = SlideTransition(direction = 'up')
        self.__app.screen_manager.current = 'projects'

    def add(self, instance):
        
        if rules.min_cost(int(self.price.text)):
            self.error.text = 'Min cost is 20000$'
            return

        if not self.name.text == '' and not self.task.text == '' and not self.price.text == '' and not self.customer.text == 'Customer':
            db.add_project(self.name.text, self.task.text, self.customer.text, int(self.price.text), self.started.text)

            self.name.text = ''
            self.task.text = ''
            self.price.text = ''
            date_now = datetime.now()
            self.started.text = f"{date_now.month}-{date_now.day}-{date_now.year}"
            self.customer.text = 'Customer'

            self.__app.screen_manager.transition = SlideTransition(direction = 'up')
            self.__app.screen_manager.current = 'projects'
        else:
            self.error.text = 'Fill in all the fields!'

    def set_date(self, instance):
        date = MDDatePicker()
        date.bind(on_save=self.update_date)
        date.open()

    def update_date(self, instance, value, date_range):
        date: datetime = value
        self.started.text = f"{date.month}-{date.day}-{date.year}"
