import psycopg2
from db_config import db_config

class StudentDAO:
    def __init__(self):
        self.config = db_config

    def connect(self):
        return psycopg2.connect(**self.config)

    def get_all_students(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT id, first_name, last_name FROM students")
        students = cur.fetchall()
        conn.close()
        return students

    def get_student_by_id(self, student_id):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cur.fetchone()
        conn.close()
        return student

    def create_student(self, first_name, last_name, birth_date, class_name, phone_number):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO students (first_name, last_name, birth_date, class_name, phone_number)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, birth_date, class_name, phone_number))
        conn.commit()
        conn.close()

    def update_student(self, student_id, first_name, last_name, birth_date, class_name, phone_number):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE students SET first_name=%s, last_name=%s, birth_date=%s, class_name=%s, phone_number=%s
            WHERE id=%s
        """, (first_name, last_name, birth_date, class_name, phone_number, student_id))
        conn.commit()
        conn.close()

    def delete_student(self, student_id):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
        conn.close()
