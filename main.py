from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('modules', 'touchring', '')  
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from student_dao import StudentDAO
from save_student import StudentFormScreen



# Екран списку
class StudentListScreen(Screen):
    def __init__(self, dao, **kwargs):
        super().__init__(**kwargs)
        self.dao = dao
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        self.refresh_students()

    def refresh_students(self):
        self.layout.clear_widgets()

        students = self.dao.get_all_students()
        for student in students:
            student_label = Label(text=f"{student[0]}. {student[1]} {student[2]}")
            edit_button = Button(text="Редагувати", size_hint_x=0.3)
            edit_button.bind(on_press=lambda btn, sid=student[0]: self.edit_student(sid))
            delete_button = Button(text="Видалити", size_hint_x=0.3)
            delete_button.bind(on_press=lambda btn, sid=student[0]: self.delete_student(sid))

            row = BoxLayout(size_hint_y=None, height=40)
            row.add_widget(student_label)
            row.add_widget(edit_button)
            row.add_widget(delete_button)
            self.layout.add_widget(row)

        add_button = Button(text="Додати учня", size_hint_y=None, height=50)
        add_button.bind(on_press=self.add_student)
        self.layout.add_widget(add_button)

    def add_student(self, instance):
        self.manager.get_screen('student_form').set_student(None)
        self.manager.current = 'student_form'

    def edit_student(self, student_id):
        form_screen = self.manager.get_screen('student_form')
        form_screen.set_student(student_id)
        self.manager.current = 'student_form'

    def delete_student(self, student_id):
        self.dao.delete_student(student_id)
        self.refresh_students()

# Головний додаток
class StudentApp(App):
    def build(self):
        dao = StudentDAO()
        sm = ScreenManager()
        sm.add_widget(StudentListScreen(dao, name='student_list'))
        sm.add_widget(StudentFormScreen(dao, name='student_form'))
        return sm

if __name__ == '__main__':
    
    StudentApp().run()