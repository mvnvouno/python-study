# 03 ~ 04단원 한꺼번에 (실습+초기설정)

#-----------------------------------------------
# 3. 데이터 조회 API (sql SELECT)
#-----------------------------------------------
# 3.1 Flask 웹 서버 기본구성:
#-----------------------------------------------
# [1] 패키지 참조:

from flask import Flask, request
from sqlalchemy import text
import datetime as dt
from mylibrary import MyDB

#-----------------------------------------------
# [2] Flask 메인 객체 생성

app = Flask(__name__)
app.json.sort_keys = False
    # 키의 알파벳 순서대로 정렬됨을 방지하는 용도

# 이후 코드들은 여기 아래에 적기 ↓↓
    # (SELECT, INSERT, UPDATE, DELETE 다!)
# -----------------------------------
# [5] GET - 다중행 데이터 조회하기 (sql SELECT)

@app.route("/departments", methods=['GET'])
# departments 뒤에 '/~' 안오면 전체데이터 가꼬옴
def get_list():
    sql = text("SELECT id, dname, loc, phone, email FROM departments")
    # 실행할 sql문 정의임

    conn = MyDB.connect()       # DB 접속
    result = conn.execute(sql)  # SQL문 실행, 결과객체 받기
    MyDB.disconnect()           # DB 접속해제

    resultset = result.mappings().all()
    # 다중행 조회에 대한 결과집합 추출받는거

    for i in range(0, len(resultset)):
        resultset[i] = dict(resultset[i])
    # 반복문으로 탐색하면서 개별 레코드를 
    # 딕셔너리 형태로 변환해야 해서 쓰는 코드

    return {
        "resultset": resultset,
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    } # 다중행 결과 반환법

    # 다중행 조회결과 화긴:
        # 터미널 실행 후 접속: http://127.0.0.1:9091/departments

# -----------------------------------
# [6] GET - 단일행 데이터 조회하기 (sql SELECT)

@app.route("/departments/<id>", methods=['GET'])
def get_item(id):
    sql = text("""SELECT id, dname, loc, phone, email, established, homepage 
            FROM departments 
            WHERE id=:id""")
            # 실행할 sql문 정의임

    conn = MyDB.connect()                   # DB 접속
    result = conn.execute(sql, {"id": id})  # SQL문 실행, 결과객체 받기
    MyDB.disconnect()                       # DB 접속해제

    resultset = result.mappings().all()
    # 단일행 조회에 대한 결과집합 추출받는거

    return {
    "result": dict(resultset[0]),
    "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    } # 단일행 결과 반환법
        # line 66: Where절의 결과 갯수는 0 또는 1 밖에 없음!
            # 이유: 조건거는 객체가 PK니까.
            # -> 그래서 하나만 조회하는거임

    # 단일행 조회결과 화긴:
        # 터미널 실행 후 접속: http://127.0.0.1:9091/departments/201

#-----------------------------------------------
# [7] POST - 데이터 입력하기 (sql INSERT)
@app.route("/departments", methods=['POST'])
def post():
    # DB 접속하기:
    conn = MyDB.connect()
    #-------------------------------------------
    # 1) 데이터 저장하기
    #-------------------------------------------
    # POST 파라미터 수신하기
    dname = request.form.get("dname")
    loc = request.form.get("loc")
    phone = request.form.get("phone")
    email = request.form.get("email")
    established = request.form.get("established")
    homepage = request.form.get("homepage")

    # SQL문 적기
    sql = text("""INSERT INTO departments (
               dname, loc, phone, email, established, homepage)
               VALUES (
               :dname, :loc, :phone, :email, :established, :homepage)
               """)

    # POST 파라미터 -> SQL 맵핑하기 위해 딕셔너리로 묶기
    params = {
        "dname": dname, "loc": loc, "phone": phone, "email": email, 
        "established": established, "homepage": homepage
    }

    # SQL문 실행하기(feat. 자동 트렌젝션)
    conn.execute(sql, params)
    # 변경사항을 DB에 영구저장
    conn.commit()

    #-------------------------------------------
    # 2) 데이터 저장 결과 조회하기
    #-------------------------------------------
    # 생성된 PK값 추출하기
    pk_result = conn.execute(text("SELECT LAST_INSERT_ID()"))
    pk = pk_result.scalar()

    # SQL문 적기
    sql = text("""SELECT id, dname, loc, phone, email, established, homepage 
        FROM departments 
        WHERE id=:id""")
    
    # SQL 실행한 결과객체 받기
    result = conn.execute(sql, {"id": pk})
    # 단일행 조회의 결과집합 추출받기
    resultset = result.mappings().all()
    #-------------------------------------------
    # DB 접속 해제
    MyDB.disconnect()
    #-------------------------------------------
    # 응답결과 반환받기
    return {
        "result": dict(resultset[0]), # 일단 뼈대 먼저 구성 
                # -> 1),2) 적고 -> 다시 return으로 돌아와서 
                # None -> dict(resultset[0]) 수정하는 순서로 적자.
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
#-----------------------------------------------
# [8] PUT - 데이터 수정하기 (sql UPDATE)
    # WHERE절에 쓸 PK값: PATH 파라미터로 정의하기
@app.route("/departments/<id>", methods=['PUT'])
def put(id):
    # DB에 접속하기
    conn = MyDB.connect()
    #-------------------------------------------
    # 1) 데이터 수정하기
    #-------------------------------------------
    # PUT 파라미터 수신하기
    dname = request.form.get("dname")
    loc = request.form.get("loc")
    phone = request.form.get("phone")
    email = request.form.get("email")
    established = request.form.get("established")
    homepage = request.form.get("homepage")

    # SQL문 적기
    sql = text("""UPDATE departments 
               SET
               dname=:dname, loc=:loc, phone=:phone, email=:email, established=:established, homepage=:homepage
               WHERE id=:id""")

    # PUT 파라미터 -> SQL 맵핑하기 위해 딕셔너리로 묶고
    # -> WHERE절에 쓸 id값: PATH 파라미터
    params = {
        "id": id, "dname": dname, "loc": loc, "phone": phone, 
        "email": email, "established": established, "homepage": homepage
        }    
    
    # SQL문 실행하기(feat. 자동 트렌젝션)
    conn.execute(sql, params)
    # 변경사항을 DB에 영구저장
    conn.commit()
    #-------------------------------------------
    # 2) 데이터 수정 결과 조회하기
    #-------------------------------------------
    # SQL문 적기
    sql = text("""SELECT id, dname, loc, phone, email, established, homepage 
        FROM departments 
        WHERE id=:id""")
    
    # SQL 실행한 결과객체 받기
    result = conn.execute(sql, {"id": id})
    # 단일행 조회의 결과집합 추출받기
    resultset = result.mappings().all()
    #-------------------------------------------
    # DB 접속 해제
    MyDB.disconnect()
    #-------------------------------------------
    # 응답결과 반환받기
    return {
        "result": dict(resultset[0]), # 일단 뼈대 먼저 구성 
                # -> 1),2) 적고 -> 다시 return으로 돌아와서 
                # None -> dict(resultset[0]) 수정하는 순서로 적자.
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
#-----------------------------------------------
# [9] DELETE - 데이터 삭제하기 (sql DELETE)
    # WHERE절에 쓸 PK값: PATH 파라미터로 정의하기
@app.route("/departments/<id>", methods=['DELETE'])
def delete(id):
    conn = MyDB.connect()

    # 참조키를 고려하여 데이터 삭제구문 준비
    sql1 = text("""DELETE FROM enrollments 
                WHERE subject_id IN (
                SELECT id FROM subjects WHERE department_id=:id)
                OR student_if IN (
                SELECT id FROM students WHERE department_id=:id)""")
    sql2 = text("DELETE FROM subjects WHERE department_id=:id")
    sql3 = text("DELETE FROM students WHERE department_id=:id")
    sql4 = text("DELETE FROM professors WHERE department_id=:id")
    sql5 = text("DELETE FROM departments WHERE id=:id")

    params = {"id": id}

    conn.execute(sql1, params)
    conn.execute(sql2, params)
    conn.execute(sql3, params)
    conn.execute(sql4, params)
    conn.execute(sql5, params)

    conn.commit()       # 변경사항을 데이터베이스에 영구 저장
    MyDB.disconnect()

    return {'timestamp': dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

#-----------------------------------------------
# [3] 전역 예외 처리

@app.errorhandler(Exception)
def error_handling(error):
    MyDB.disconnect()
    return {
        'message': "".join(error.args),
        'timestamp': dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }, 500
        # timestamp 해주는 이유:
            # 데이터들이 시간 순으로 잘 나왔는지 확인하기 위함

#-----------------------------------------------
# [4] Flask 웹 서버 가동

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9091, debug=True)
    # host='127.0.01' -> 기본값이니까 굳이 안적어도 무방

#-----------------------------------------------
# 4. 데이터 저장/수정/삭제 API
#-----------------------------------------------
# 4.1 데이터 입력 API (sql INSERT)
#-----------------------------------------------
    # line 80 [7] 코드+내용 참고 (코드 큰 뼈대 순서 이슈)

    # 데이터 조회때랑 나머지 코드들은 다 순서 일정하고 
        # 변수만
            # 변수 = 'request.form.get('변수')'
            # flask를 쓰니까.
        # sql문만 INSERT로 변경
        # sqlalchemy는 자동으로 트렌젝션 실행됨
    # 결과조회는 Thunder client -> POST에서 조회하기

#-----------------------------------------------
# 4.2 데이터 수정 API (sql UPDATE)

#-----------------------------------------------
# 4.3 데이터 삭제 API (sql DELETE)
#-----------------------------------------------
    # '참조관계를 거슬러 올라가면서' 역순으로 삭제
    # -> 딸린 자식 데이터들이 다 삭제되어야 부모데이터가 삭제가능!
    # -> if department 삭제하려면:
        # departments의 딸린자식: 소속교수, 소속학생
        # 근데! 소속교수를 삭제하려니 교수가 담당하는 교과목(subjects)이 있음!
        # subjects: 교수에 딸린 자식데이터!
            # 결론적으로 삭제 순서: 
            # subject -> students, professors -> departments
#-----------------------------------------------