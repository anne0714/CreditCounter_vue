from flask import Flask, render_template, request 
from flask.views import MethodView
import json 
import CreditCounter
from flask_cors import CORS

app = Flask(__name__) # 建立 Flask 物件
CORS(app) # 啟用跨域資源共享

@app.route('/')
def index(): # 用來回應網站首頁連線的函式 
    data = CreditCounter.get_study_list()
    return render_template('index.html', course1 = data) # 呼叫 index.html 網頁


#@app.cli.command() # 建立一個指令

class StudyApi(MethodView): # 建立一個類別，用來處理 API 請求，得到學生修課清單
    def get(self,student):
        if not student:
            courses = CreditCounter.get_study_list(None)
            results = [
                {
                    '學號': course[0],
                    '課程ID': course[1],
                    '課程名稱': course[2],
                    '學分數': course[3],
                    '時數': course[4],
                } for course in courses
            ]
            return json.dumps({'status': 'success',
                    'massage': '取得學生修課清單成功',
                    'results': results}, ensure_ascii=False) # 回傳 JSON 格式的學生修課清單
        else: # 取得特定學生修課清單
            courses = CreditCounter.get_study_list(student)
            results = [
                {
                    '課程ID': course[0],
                    '課程名稱': course[1],
                    '學分數': course[2],
                    '開課年級': course[3],
                    '先修課程名稱': course[4].split(',') if course[4] else [], # 將逗號分隔的字符串轉換為列表
                    '修課狀態': course[5],
                    '課程類型': course[6],
                } for course in courses # 列表推導式
            ]
            return json.dumps(
                {'status': 'success',
                'massage': '取得學生修課清單成功',
                'results': results}, ensure_ascii=False) # 回傳 JSON 格式的學生修課清單
        
    def put(self,student):
        form = request.json # 取得前端傳送的資料
        course_id = form.get('course_id')
        status = form.get('status')
        CreditCounter.update_study(student, course_id, status)
        return json.dumps(
            {'status': 'success',
            'massage': '更新學生修課成功'}, 
            ensure_ascii=False) # 回傳 JSON 格式的更新學生修課成功訊息
    
    def post(self,student):
        form = request.json # 取得前端傳送的資料
        class_name = form.get('class_name')
        CreditCounter.insert_study(student, class_name)
        return json.dumps(
            {'status': 'success',
            'massage': '新增學生修課成功'}, 
            ensure_ascii=False) # 回傳 JSON 格式的新增學生修課成功訊息
    
    def delete(self,student,course_id):
        CreditCounter.delete_study(student, course_id)
        return json.dumps(
            {'status': 'success',
            'massage': '刪除學生修課成功'}, 
            ensure_ascii=False) # 回傳 JSON 格式的刪除學生修課成功訊息
    
study_view = StudyApi.as_view('study_api') # 建立一個路由，用來處理 API 請求
app.add_url_rule('/api/study', defaults={'student': None}, view_func=study_view, methods=['GET',]) # 設定路由
app.add_url_rule('/api/study/<student>', view_func=study_view, methods=['GET','PUT', 'POST',]) # 設定特定學生修課清單的路由
app.add_url_rule('/api/study/<student>/<course_id>', view_func=study_view, methods=['DELETE',]) # 刪除特定學生修的某課程的路由

class CourseApi(MethodView): # 課程清單的API
    # 取得所有課程清單
    def get(self):
        courses = CreditCounter.get_course()
        results = [
            {
                '課程ID': course[0],
                '課程名稱': course[1],
                '學分數': course[2],
                '時數': course[3],
                '開課單位': course[4],
            } for course in courses
        ]
        return json.dumps({'status': 'success',
                'massage': '取得課程清單成功',
                'results': results}, ensure_ascii=False) # 回傳 JSON 格式的課程清單

    def post(self):
        form = request.json # 取得前端傳送的資料
        course_name = form.get('course_name')
        credit = form.get('credit')
        hours = form.get('hours')
        open = form.get('open')
        CreditCounter.insert_course(course_name, credit, hours, open)
        return json.dumps(
            {'status': 'success',
            'massage': '新增課程成功'}, 
            ensure_ascii=False) # 回傳 JSON 格式的新增課程成功訊息
    
    def put(self):
        form = request.json # 取得前端傳送的資料
        course_id = form.get('id')
        course_name = form.get('course_name')
        credit = form.get('credit')
        hours = form.get('hours')
        open = form.get('open')
        CreditCounter.update_course(course_id, course_name, credit, hours, open)
        return json.dumps(
            {'status': 'success',
            'massage': '更新課程成功'}, 
            ensure_ascii=False) # 回傳 JSON 格式的更新課程成功訊息
    
    def delete(self,course_id):
        CreditCounter.delete_course(course_id)
        return json.dumps(
            {'status': 'success',
            'massage': '刪除課程成功'}, 
            ensure_ascii=False) # 回傳 JSON 格式的刪除課程成功訊息

course_view = CourseApi.as_view('course_api') # 建立一個路由，用來處理課程 API 請求
app.add_url_rule('/api/course', view_func=course_view, methods=['GET','POST','PUT',]) # 取得課程、新增、修改課程的路由
app.add_url_rule('/api/course/<course_id>', view_func=course_view, methods=['DELETE',]) # 刪除課程的路由

class MajorApi(MethodView): # 取得專門課程的API

    def get(self,class_name):    
        courses = CreditCounter.get_major_course(class_name)
        results = [
            {
                '課程ID': course[0],
                '課程名稱': course[1],
                '學分數': course[2],
                '時數': course[3],
                '開課年級': course[4],
                '必修/選修': "必修" if course[5] == 1 else "選修",
            } for course in courses
        ]
        return json.dumps({'status': 'success',
                'massage': '取得專門課程清單成功',
                'results': results}, ensure_ascii=False) # 回傳 JSON 格式的專門課程清單
    
    def post(self):
        form = request.json # 取得前端傳送的資料
        course_id = form.get('course_id')
        class_name = form.get('class')
        required = form.get('required')
        year = form.get('year')
        open_grade = form.get('open_grade')
        second = form.get('second')
        minor = form.get('minor')
        course_group = form.get('course_group')
        CreditCounter.insert_major_course(course_id, class_name, required, year, open_grade, second, minor, course_group)
        return json.dumps(
            {'status': 'success',
            'massage': '新增專門課程成功'}, 
            ensure_ascii=False) # 回傳 JSON 格式的新增專門課程成功訊息

major_view = MajorApi.as_view('major_api') # 專門課程 API 
app.add_url_rule('/api/major_course/<class_name>', view_func=major_view, methods=['GET',]) # 取得專門課程的路由
app.add_url_rule('/api/major_course', view_func=major_view, methods=['POST',]) 

class ModuleApi(MethodView): # 模組清單的API

    def get(self):
        modules = CreditCounter.get_module()
        results = [
            {
                '學程名稱': module[0],
                '適用年度': module[1],
                '課程名稱': module[2],
                '學分數': module[3],
                '時數': module[4],
                # 如果是1，表示必修，如果是0，表示選修
                '必修/選修': "必修" if module[5] == 1 else "選修",
                '必選修子群組': module[6],
                '開課年級': module[7],
            } for module in modules
        ]
        return json.dumps({'status': 'success',
                'massage': '取得模組清單成功',
                'results': results}, ensure_ascii=False) # 回傳 JSON 格式的模組清單
    
    def post(self):
        form = request.json # 取得前端傳送的資料
        course_id = form.get('course_id')
        name = form.get('name')
        required = form.get('required')
        year = form.get('year')
        open_grade = form.get('open_grade')
        course_group = form.get('course_group')
        CreditCounter.insert_module(course_id, name, required, year, open_grade, course_group)
        return json.dumps(
            {'status': 'success',
            'massage': '新增模組成功'}, 
            ensure_ascii=False) # 回傳 JSON 格式的新增模組成功訊息

module_view = ModuleApi.as_view('module_api') # 建立一個路由，用來處理模組 API 請求
app.add_url_rule('/api/module', view_func=module_view, methods=['GET','POST',]) # 取得模組、新增模組的路由

class LoginApi(MethodView): # 登入API
    def post(self):
        form = request.json # 取得前端傳送的資料
        account = form.get('account')
        password = form.get('password')
        data =CreditCounter.login_check(account, password)
        if data:
            return json.dumps(
                {'status': 'success',
                'massage': '登入成功',
                'major': data[0],
                'access': data[1]}, 
                ensure_ascii=False) # 回傳 JSON 格式的登入成功訊息
        else:
            return json.dumps(
                {'status': 'fail',
                'massage': '登入失敗'}, 
                ensure_ascii=False) # 回傳 JSON 格式的登入失敗訊息

login_view = LoginApi.as_view('login_api') # 建立一個路由，用來處理登入 API 請求
app.add_url_rule('/api/login', view_func=login_view, methods=['POST',]) # 登入的路由

class SignupApi(MethodView): # 註冊API
    def post(self):
        form = request.json # 取得前端傳送的資料
        account = form.get('account')
        password = form.get('password')
        major = form.get('major')
        second_major = form.get('second_major')
        minor = form.get('minor')
        education = form.get('education')
        access = form.get('access')
        CreditCounter.insert_user(account, password, major, second_major, minor, education, access)
        return json.dumps(
            {'status': 'success',
            'massage': '註冊成功'}, 
            ensure_ascii=False) # 回傳 JSON 格式的註冊成功訊息

signup_view = SignupApi.as_view('signup_api') # 建立一個路由，用來處理註冊 API 請求
app.add_url_rule('/api/signup', view_func=signup_view, methods=['POST',]) # 註冊的路由

# 網站啟動，可透過port改變埠號
app.run(port=9527)