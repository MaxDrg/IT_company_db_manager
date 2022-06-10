from kivy.metrics import dp
from database import Database
from temporary import Connection
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.datatables import MDDataTable
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.label import Label

class Tasks(BoxLayout):
    def __init__(self, app):
        super().__init__()
        self.__app = app
        self.checked_data = []

        conn = Connection().get()
        self.db = Database(conn['login'], conn['password'])
        
        row_data = []
        if self.db.success_connection:
            row_data = self.db.get_tasks()

        self.orientation = 'vertical'

        header = BoxLayout(padding=8, size_hint=(1, 0.1), orientation = 'vertical', spacing=10)

        page_name = Label(text='Tasks', color='black', font_size=25)
        head_btn = Button(text="Show all team leads", size_hint=(0.95, 1.5), pos_hint={"center_y": 0.5, "center_x": 0.5})
        head_btn.bind(on_press=self.get_team_leads)
        
        header.add_widget(page_name)
        header.add_widget(head_btn)
        
        self.table = MDDataTable(
            use_pagination=True,
            check=True,
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            size_hint=(0.95, 0.5),
            column_data=[('ID', dp(20)), ('Employee', dp(50)), ('Project', dp(50)), ('Position', dp(50))],
            rows_num=50,
            row_data=row_data,
        )
        self.table.bind(on_check_press=self.checked)

        left = Button(text="Exp. levels")
        left.bind(on_press=self.turn_left)

        add = Button(text="Add", pos =(20, 20))
        add.bind(on_press=self.add)

        update = Button(text="Update", pos =(20, 20))
        update.bind(on_press=self.update)

        delete = Button(text="Delete", pos =(20, 20))
        delete.bind(on_press=self.dialog_delete)

        right = Button(text="Projects", pos =(20, 20))
        right.bind(on_press=self.turn_right)
        
        buttons = BoxLayout(padding=8, size_hint=(1, 0.08))
        buttons.add_widget(left)
        buttons.add_widget(add)
        buttons.add_widget(update)
        buttons.add_widget(delete)
        buttons.add_widget(right)

        self.add_widget(header)
        self.add_widget(self.table)
        self.add_widget(buttons)

    def update(self, instance):
        conn = Connection().get()
        self.db = Database(conn['login'], conn['password'])

        self.table.row_data = self.db.get_tasks()

    def turn_left(self, instance):
        self.__app.screen_manager.transition = SlideTransition(direction = 'right')
        self.__app.screen_manager.current = 'levels'

    def turn_right(self, instance):
        self.__app.screen_manager.transition = SlideTransition(direction = 'left')
        self.__app.screen_manager.current = 'projects'

    def checked(self, instance_table, current_row):
        if not current_row[0] in self.checked_data:
            self.checked_data.append(current_row[0])
        else:
            self.checked_data.remove(current_row[0])

    def add(self, instance):
        self.__app.screen_manager.transition = SlideTransition(direction = 'down')
        self.__app.screen_manager.current = 'add_task'

    def dialog_delete(self, instance):
        
        self.dialog = self.dialog = MDDialog(
				title = "Deletion",
				text = "Are you sure that you want to delete this record(s) and all relative?",
				buttons =[
					MDFlatButton(
						text="CANCEL", on_release = self.close_dialog
						),
					MDRectangleFlatButton(
						text="DELETE", on_release = self.delete
						),
					],
				)
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def delete(self, instance):
        self.dialog.dismiss()
        for id in self.checked_data:
            self.db.del_task(id)
        self.checked_data = []
        self.table.row_data = self.db.get_tasks()

    def get_team_leads(self, instance):
        self.checked_data = []
        self.table.row_data = self.db.get_team_leads()