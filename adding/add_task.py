from database import Database
from rules import Rules
from temporary import Connection
from kivy.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import SlideTransition

conn = Connection().get()
db = Database(conn['login'], conn['password'])
rules = Rules()

class Add_task(BoxLayout):
    def __init__(self, app):
        super().__init__()
        self.__app = app

        self.orientation = 'vertical'

        employee = BoxLayout(padding=50, size_hint=(1, .3))
        project = BoxLayout(padding=50, size_hint=(1, .3))
        position = BoxLayout(padding=50, size_hint=(1, .3))

        lbl = Label(
            text='Employee', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        values = [i[0] for i in db.get_employees_name()]
        values = tuple(values)
        self.employee = Spinner(
            text='Employee',
            values=values,
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={'center_x': .5, 'center_y': .5})

        employee.add_widget(lbl)
        employee.add_widget(self.employee)

        lbl = Label(
            text='Project', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        values = [i[0] for i in db.get_projects_name()]
        values = tuple(values)
        self.project = Spinner(
            text='Project',
            values=values,
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={'center_x': .5, 'center_y': .5})

        project.add_widget(lbl)
        project.add_widget(self.project)

        lbl = Label(
            text='Position', 
            color='black', 
            font_size=25,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(0.5, 0.1)
        )

        self.position = TextInput(
            multiline=False,
            pos_hint={"center_y": .5, "center_x": .5}, 
            size_hint=(1.5, .9)
        )

        position.add_widget(lbl)
        position.add_widget(self.position)

        return_btn = Button(text="Return")
        return_btn.bind(on_press=self.exit)

        add_btn = Button(text="Add")
        add_btn.bind(on_press=self.add)
        
        buttons = BoxLayout(padding=20, pos_hint={"center_y": 0.5, "center_x": 0.5}, size_hint=(1, .20))
        buttons.add_widget(return_btn)
        buttons.add_widget(add_btn)

        self.error = Label(text='', color='red', font_size=30, size_hint=(1, 0.08))

        self.add_widget(employee)
        self.add_widget(project)
        self.add_widget(position)
        self.add_widget(self.error)
        self.add_widget(buttons)

    def exit(self, instance):
        self.employee.text = 'Employee'
        self.project.text = 'Project'
        self.position.text = ''

        self.__app.screen_manager.transition = SlideTransition(direction = 'up')
        self.__app.screen_manager.current = 'tasks'

    def add(self, instance):
        if not self.employee.text == 'Employee' and not self.project.text == 'Project' and not self.position.text == '':
            
            if rules.team_lead(self.position.text, self.employee.text):
                self.error.text = 'Junior Team lead can not work!'
                return

            if rules.check_team(self.project.text, self.employee.text):
                self.error.text = 'No more developers!'
                return

            if rules.check_team_lead(self.project.text, self.position.text):
                self.error.text = 'Too many team leads!'
                return

            db.add_task(self.employee.text, self.project.text, self.position.text)

            self.employee.text = 'Employee'
            self.project.text = 'Project'
            self.position.text = ''

            self.__app.screen_manager.transition = SlideTransition(direction = 'up')
            self.__app.screen_manager.current = 'tasks'
        else:
            self.error.text = 'Fill in all the fields!'