# flask 사용 시:
    # 모든 함수에서 공통으로 사용하는 기능 모듈화 하는곳
#------------------------------------------------
# 데이터베이스(DB) 접속 정보
from sqlalchemy import create_engine

config = {
    'username': 'root',         # 접속 사용자 이름
    'password': '1234',         # 접속 사용자 비번
    'hostname': 'localhost',    # 접속 시스템 주소 (내컴에 접속할거면 localhost)
    'port': 9090,               # 설치시 설정한 포트번호 (기본값: 3306)
    'database': 'myschool',     # 사용할 DB 이름
    'charset': 'utf8mb4'        # 한글깨짐방지
}

conn = None     # DB 접속 객체에 대한 전역변수 선언
#------------------------------------------------
# 데이터베이스(DB) 접속 함수
def connect():
    global conn
    # global: 함수 외부 변수 -> 함수 안으로 끌고오는 역할
        # -> 외부변수가 내부로 출입하면 '문자열'임!
    
    con_str_tpl = "mariadb+pymysql://{username}:{password}@{hostname}:{port}/{database}?charset={charset}"
    con_str = con_str_tpl.format(**config)  
    # 딕셔너리를 'key=value, key=value,..' 형식으로 나열해서 파라미터 일괄 설정
    engine = create_engine(con_str)
    conn = engine.connect()

    return conn
#------------------------------------------------
# 데이터베이스(DB) 접속 해제 함수
def disconnect():
    global conn
    #global: 함수 외부 변수 -> 함수 내부 끌고옴

    if conn != None:
        conn.close()
    # 모든 import하는 기능들은 실행 후 반드시 꺼줘야 해서 적는거임
#------------------------------------------------
# 모듈 작동 테스트 해보기 (출력결과 없음):
if __name__ == "__main__":
    connect()
    disconnect()