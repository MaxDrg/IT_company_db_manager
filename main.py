from kivymd.app import MDApp
from start import Start
from tables.employees import Employees
from tables.customers import Customers
from tables.projects import Projects
from tables.tasks import Tasks
from tables.levels import Levels
from adding.add_level import Add_level
from adding.add_employee import Add_employee
from adding.add_customer import Add_customer
from adding.add_project import Add_Project
from adding.add_task import Add_task
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.config import Config 
Config.set('graphics', 'width', '850')
Config.set('graphics', 'height', '550')
Config.set('graphics','resizable', False)
Config.write()

class IT_company(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()

        screen = Screen(name='start')
        self.start = Start(app)
        screen.add_widget(self.start)
        self.screen_manager.add_widget(screen)

        screen = Screen(name='employees')
        self.employees = Employees(app)
        screen.add_widget(self.employees)
        self.screen_manager.add_widget(screen)

        screen = Screen(name='customers')
        self.customers = Customers(app)
        screen.add_widget(self.customers)
        self.screen_manager.add_widget(screen)

        screen = Screen(name='projects')
        self.projects = Projects(app)
        screen.add_widget(self.projects)
        self.screen_manager.add_widget(screen)

        screen = Screen(name='tasks')
        self.tasks = Tasks(app)
        screen.add_widget(self.tasks)
        self.screen_manager.add_widget(screen)

        screen = Screen(name='levels')
        self.levels = Levels(app)
        screen.add_widget(self.levels)
        self.screen_manager.add_widget(screen)

        screen = Screen(name='add_level')
        self.add_level = Add_level(app)
        screen.add_widget(self.add_level)
        self.screen_manager.add_widget(screen)

        screen = Screen(name='add_employee')
        self.add_employee = Add_employee(app)
        screen.add_widget(self.add_employee)
        self.screen_manager.add_widget(screen)

        screen = Screen(name='add_customer')
        self.add_customer = Add_customer(app)
        screen.add_widget(self.add_customer)
        self.screen_manager.add_widget(screen)
        
        screen = Screen(name='add_project')
        self.add_project = Add_Project(app)
        screen.add_widget(self.add_project)
        self.screen_manager.add_widget(screen)

        screen = Screen(name='add_task')
        self.add_task = Add_task(app)
        screen.add_widget(self.add_task)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == "__main__":
    app = IT_company()
    app.run()