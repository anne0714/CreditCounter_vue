import mysql.connector

# 連線到資料庫
#def connect():
# con = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="anne0714",
#     database="credit_counter"
# )
# print("資料庫連線成功！")

# 建立一個游標物件，用來對資料庫下SQL指令
#cursor = con.cursor()
# return cursor, con

# 取得課程清單
def get_course():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")

    cursor = con.cursor()
    cursor.execute("select * from course")
    data = cursor.fetchall()
    print("課程清單：" + str(data))
    con.close()
    return data

# 新增課程到課程清單中
def insert_course(courseName,credit,hours, open):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")

    cursor = con.cursor()
    cursor.execute("insert into course(name,credit,hours, open) values(%s,%s,%s,%s)",
                    (courseName, credit, hours, open))
    con.commit() # 確定執行
    print(f'成功新增了課程：{courseName} 學分：{credit} 開課時數：{hours}, 開課單位：{open}')

# 修改課程資訊
def update_course(course_id, courseName,credit,hours, open):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")

    cursor = con.cursor()
    cursor.execute("update course set name = %s, credit = %s, hours = %s, open = %s where id = %s",
                    (courseName, credit, hours, open, course_id))
    con.commit() # 確定執行
    print(f'成功修改了課程ID為：{course_id} 的課名：{courseName} 學分：{credit} 開課時數：{hours}, 開課單位：{open}')

# 刪除課程
def delete_course(course_id):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")

    cursor = con.cursor()
    cursor.execute("delete from course where id = %s", (course_id,))
    con.commit() # 確定執行
    print(f'成功刪除課程ID為：{course_id}的課')

# 取得專門課程(主修/雙主修/輔系)
def get_major_course(class_name):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")

    cursor = con.cursor()
    # 查詢特定類型的課程
    if class_name == '藝設系設計組':
            cursor.execute('''select id, name, credit, hours, open_grade,required
                           from major_course inner join course on major_course.course_id = course.id 
                           where class like '藝設系%';''')
    else:
        cursor.execute('''select id, name, credit, hours, open_grade,required
                       from major_course inner join course on major_course.course_id = course.id 
                       where class = %s;''', (class_name,))
    data = cursor.fetchall()
    print(f'{class_name}專門課程清單：' + str(data))
    con.close()
    return data

# 新增專門課程
def insert_major_course(course_id, class_name, required, year, open_grade, second, minor, course_group):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")
    cursor = con.cursor()
    cursor.execute("insert into major_course(course_id, class, required, year, open_grade, second, minor, course_group) values(%s,%s,%s,%s,%s,%s,%s,%s)", (course_id, class_name, required, year, open_grade, second, minor, course_group))
    con.commit() # 確定執行
    print(f'成功新增了{class_name} 課程ID為：{course_id} 的課')

# 取得其他學程清單
def get_module():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")

    cursor = con.cursor()
    cursor.execute('''select module.name, year, course.name, credit, hours, required, course_group, open_grade
                       from module inner join course on module.course_id = course.id;''')
    data = cursor.fetchall()
    print("其他學程清單：" + str(data))
    con.close()
    return data

# 新增模組課程
def insert_module(course_id, name, required, year, open_grade, course_group):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")
    cursor = con.cursor()
    cursor.execute("insert into module(course_id, name, required, year, open_grade, course_group) values(%s,%s,%s,%s,%s,%s)", (course_id, name, required, year, open_grade, course_group))
    con.commit() # 確定執行
    print(f'成功新增了{name} 課程ID為：{course_id} 的課')

# 取得學生修過的課程清單
def get_study_list(student):
    if not student:
        con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
        )
        print("資料庫連線成功！")

        cursor = con.cursor()
        cursor.execute('''select study.student, course.id, course.name, course.credit, course.hours 
                       from course inner join study on course.id = study.course_id;''')
        
        data = cursor.fetchall()
        print("學生修過的課程清單：" + str(data))

        con.close()
        return data
    else:
        con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
        )
        print("資料庫連線成功！")

        cursor = con.cursor()
        # 用學號查詢某位學生修過的課程
        cursor.execute(
            '''select study.course_id, course.name, course.credit, major_course.open_grade, 
            GROUP_CONCAT(pre_course_name.name) AS prereq_courses_names, study.status, type

            from study join major_course on study.course_id = major_course.course_id
            join course on major_course.course_id = course.id
            left join pre_course on major_course.course_id = pre_course.course_id
            left join course AS pre_course_name ON pre_course.prereq = pre_course_name.id 
            where student = %s
            group by study.course_id, course.name, course.credit, major_course.open_grade, study.status;''', (student,))
        
        data = cursor.fetchall()
        print("學生修過的課程清單：" + str(data))

        con.close()
        return data
    
# 新增學生修課紀錄
def insert_study(student, class_name):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")
    cursor = con.cursor()
    cursor.execute('''INSERT INTO study (course_id, student, status, type)
    SELECT course_id, %s, '未修課', '主修' FROM major_course WHERE class = %s;''', (student, class_name))
    con.commit() # 確定執行
    print(f'新增了學生 {student} 的修課紀錄')

# 修改學生修課狀態紀錄
def update_study(student, course_id, status):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")
    cursor = con.cursor()
    cursor.execute("update study set status = %s where student = %s and course_id = %s", (status, student, course_id))
    con.commit() # 確定執行
    print(f'已修改學生 {student} 課程ID為： {course_id} 的修課狀態')

# 刪除學生修課紀錄
def delete_study(student, course_id):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")
    cursor = con.cursor()
    cursor.execute("delete from study where student = %s and course_id = %s", (student, course_id))
    con.commit() # 確定執行
    print(f'已刪除學生 {student} 課程ID為： {course_id} 的修課紀錄')

# 登入帳號密碼檢查
def login_check(account, password):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")
    cursor = con.cursor()
    cursor.execute("select major, access from user where account = %s and password = %s", (account, password))
    data = cursor.fetchone()
    if data:
        print("登入成功！")
        return data
    else:
        print("登入失敗！")
        return None
    
# 新增使用者
def insert_user(account, password, major, second_major, minor, education, access):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anne0714",
        database="credit_counter"
    )
    print("資料庫連線成功！")
    cursor = con.cursor()
    cursor.execute("insert into user(account, password, major, second_major, minor, education, access) values(%s,%s,%s,%s,%s,%s,%s)", (account, password, major, second_major, minor, education, access))
    con.commit() # 確定執行

# 關閉資料庫連線
#con.close()