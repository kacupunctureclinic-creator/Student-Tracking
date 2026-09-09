import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class StudentTrackerApp:
    def __init__(self, root):
        self.root = root
        # 1. 페이지 제목 설정 (A page title labeled “Student Tracking.”)
        self.root.title("Student Tracking")
        self.root.geometry("800x500")
        
        # 데이터베이스 초기화 메서드 실행
        self.create_db()
        
        # 화면 레이아웃(GUI) 생성 메서드 실행
        self.create_gui()
        
        # 프로그램 시작 시 기존 데이터 불러오기
        self.fetch_students()

    # --- 데이터베이스 관련 메서드 ---
    def create_db(self):
        # 데이터베이스 연결 및 테이블 생성
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                email TEXT,
                course TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_student(self):
        # 입력칸(Entry)에서 값을 가져옵니다.
        fname = self.entry_fname.get()
        lname = self.entry_lname.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        course = self.entry_course.get()

        # 빈칸이 있는지 확인
        if not (fname and lname and phone and email and course):
            messagebox.showerror("Error", "모든 입력칸을 채워주세요.")
            return

        # 데이터베이스에 데이터 삽입 (Submit)
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Student (first_name, last_name, phone, email, course)
            VALUES (?, ?, ?, ?, ?)
        ''', (fname, lname, phone, email, course))
        conn.commit()
        conn.close()

        # 입력 성공 후 입력칸 비우기 및 목록 새로고침
        self.clear_form()
        self.fetch_students()

    def delete_student(self):
        # 목록(Treeview)에서 선택된 항목 찾기
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "삭제할 학생을 목록에서 선택해주세요.")
            return

        # 선택된 항목의 ID 가져오기
        student_id = self.tree.item(selected_item)['values'][0]

        # 데이터베이스에서 해당 ID 삭제
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Student WHERE id=?", (student_id,))
        conn.commit()
        conn.close()

        # 목록 새로고침
        self.fetch_students()

    def fetch_students(self):
        # 기존 목록 지우기
        for row in self.tree.get_children():
            self.tree.delete(row)

        # 데이터베이스에서 모든 데이터 불러오기
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Student")
        rows = cursor.fetchall()
        conn.close()

        # 목록(Treeview)에 데이터 추가
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_form(self):
        # 입력 양식 비우기
        self.entry_fname.delete(0, tk.END)
        self.entry_lname.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_course.delete(0, tk.END)

    # --- GUI(화면) 생성 메서드 ---
    def create_gui(self):
        # 2. 정보 입력 폼 프레임 (A form to submit student information)
        form_frame = tk.Frame(self.root, pady=10)
        form_frame.pack(fill=tk.X, padx=20)

        # 라벨 및 입력칸 생성
        tk.Label(form_frame, text="First Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_fname = tk.Entry(form_frame)
        self.entry_fname.grid(row=0, column=1, pady=2)

        tk.Label(form_frame, text="Last Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_lname = tk.Entry(form_frame)
        self.entry_lname.grid(row=1, column=1, pady=2)

        tk.Label(form_frame, text="Phone Number:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.entry_phone = tk.Entry(form_frame)
        self.entry_phone.grid(row=2, column=1, pady=2)

        tk.Label(form_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.entry_email = tk.Entry(form_frame)
        self.entry_email.grid(row=3, column=1, pady=2)

        tk.Label(form_frame, text="Current Course:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.entry_course = tk.Entry(form_frame)
        self.entry_course.grid(row=4, column=1, pady=2)

        # 3. Submit 및 Delete 버튼
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        submit_btn = tk.Button(btn_frame, text="Submit", command=self.add_student, bg="lightblue")
        submit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(btn_frame, text="Delete Selected", command=self.delete_student, bg="salmon")
        delete_btn.pack(side=tk.LEFT, padx=5)

        # 4. 학생 목록 표시 섹션 (A section that displays the list of students)
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Treeview (표 형태의 위젯) 설정
        columns = ("ID", "First Name", "Last Name", "Phone", "Email", "Course")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # 컬럼 헤딩 설정
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        self.tree.column("ID", width=40) # ID 열은 조금 좁게 설정

        self.tree.pack(fill=tk.BOTH, expand=True)

# 메인 실행 부분
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentTrackerApp(root)
    root.mainloop()