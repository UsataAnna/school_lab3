import re  
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from datetime import datetime

class StudentFormScreen(Screen):
    def __init__(self, dao, **kwargs):
        super().__init__(**kwargs)
        self.dao = dao
        self.current_student_id = None

        self.layout = BoxLayout(orientation='vertical')

        self.first_name = TextInput(hint_text="Ім'я")
        self.last_name = TextInput(hint_text="Прізвище")
        self.birth_date = TextInput(hint_text="Дата народження (YYYY-MM-DD)")
        self.class_name = TextInput(hint_text="Клас")
        self.phone_number = TextInput(hint_text="Телефон +380XXXXXXXXX")

        self.layout.add_widget(self.first_name)
        self.layout.add_widget(self.last_name)
        self.layout.add_widget(self.birth_date)
        self.layout.add_widget(self.class_name)
        self.layout.add_widget(self.phone_number)

        save_button = Button(text="Зберегти")
        save_button.bind(on_press=self.save_student)
        self.layout.add_widget(save_button)

        cancel_button = Button(text="Назад")
        cancel_button.bind(on_press=self.go_back)
        self.layout.add_widget(cancel_button)

        self.add_widget(self.layout)

    def set_student(self, student_id):
        self.current_student_id = student_id
        if student_id:
            student = self.dao.get_student_by_id(student_id)
            self.first_name.text = student[1]
            self.last_name.text = student[2]
            self.birth_date.text = str(student[3])
            self.class_name.text = student[4]
            self.phone_number.text = student[5]
        else:
            self.first_name.text = ""
            self.last_name.text = ""
            self.birth_date.text = ""
            self.class_name.text = ""
            self.phone_number.text = ""
    
    def show_error(self, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(
            text=message,
            text_size=(280, None),
            halign='center',
            valign='middle'
        )
        label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        content.add_widget(label)

        close_button = Button(text="OK", size_hint_y=None, height=40)
        content.add_widget(close_button)

        popup = Popup(
            title='Помилка',
            content=content,
            size_hint=(None, None),
            size=(320, 200),
            auto_dismiss=False 
        )

        close_button.bind(on_press=popup.dismiss)
        popup.open()


    def save_student(self, instance):
        first_name = self.first_name.text.strip()
        last_name = self.last_name.text.strip()
        birth_date = self.birth_date.text.strip()
        class_name = self.class_name.text.strip()
        phone_number = self.phone_number.text.strip()

        if not first_name or not last_name or not birth_date or not class_name or not phone_number:
            self.show_error("Усі поля обов'язкові для заповнення.")
            return
        
        if not re.fullmatch(r"[А-ЩЬЮЯЄІЇҐ][а-щьюяєіїґ']{1,}", first_name):
            self.show_error("Ім'я має починатися з великої української літери та містити не менше 2 літер.")
            return

        if not re.fullmatch(r"[А-ЩЬЮЯЄІЇҐ][а-щьюяєіїґ']{1,}", last_name):
            self.show_error("Прізвище має починатися з великої української літери та містити не менше 2 літер.")
            return

        try:
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d')
            today = datetime.today()
            if birth_date_obj.year < 2000:
                self.show_error("Дата народження має бути не раніше 2000 року.")
                return
            if birth_date_obj > today:
                self.show_error("Дата народження не може бути в майбутньому.")
                return
        except ValueError:
            self.show_error("Дата народження має бути у форматі YYYY-MM-DD.")
            return
        
        if not re.fullmatch(r"(1[0-2]|[1-9])-[А-Я]", class_name):
            self.show_error("Клас має бути у форматі 'цифра-буква' від 1 до 12, наприклад '11-А'.")
            return

        
        if not (phone_number.startswith("+380") and len(phone_number) == 13 and phone_number[1:].isdigit()):
            self.show_error("Номер телефону має бути у форматі +380XXXXXXXXX.")
            return

        # Збереження даних
        if self.current_student_id:
            self.dao.update_student(self.current_student_id, first_name, last_name, birth_date, class_name, phone_number)
        else:
            self.dao.create_student(first_name, last_name, birth_date, class_name, phone_number)

        self.go_back()

    def go_back(self, instance=None):
        self.manager.get_screen('student_list').refresh_students()
        self.manager.current = 'student_list'
