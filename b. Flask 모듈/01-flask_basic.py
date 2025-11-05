# 1. 웹 서버의 이해 (실습+초기설정)
#---------------------------------------------
# [1] 패키지 참조 + 메인객체 생성

from flask import Flask, render_template
#---------------------------------------------
# [2] Flask 메인객체 생성 및 함수구현

    # '__name__': 지금 이 소스파일 이름
    # = '__ 01-flask-basic__'
app = Flask(__name__)
    # [2] 안에 url 요청에 의해 실행되는 함수들 넣을거임
    # 함수: 웹페이지 역할 수행 예정
    #----------------------------------------

# flask 기본 구조 실습
@app.route("/hello") # 라우팅(routing)
    # "/요청url" = http://컴퓨터주소:포트번호/요청url 
    # -> 함수를 웹 상에 url로 노출
        # http://127.0.0.1:포트번호/hello
def hello():
    # 웹브라우저에 전달할 본문:
    html = """Hello Flask~!~!
            This is test for Flask Webpage"""
    # 소스코드에선 줄바꿈 하지만 생성한 브라우저에서는 줄바꿈 처리 못함!
        # -> 바로 아래 world 에서 어케하는지 보셈
    return html # 웹 브라우저에게 문자열을 전달
    # ctrl + alt + n: open and activate cmd in vscode
        # 이거 안해주면 웹브에 생성안됨!
    # http://127.0.0.1:9091/hello -> 접속 후 결과화긴
    # 터미널 실행중단: 터미널 클릭상태에서 ctrl+c
    #----------------------------------------

# 웹브가 인식하는 줄바꿈, 글자색 실습
@app.route("/world") # 라우팅(routing)
    # http://127.0.0.1:포트번호/world
def world(): 
    # 웹브라우저가 줄바꿈, 글자색 인식 가능 문자열 연습
    html = """<h1> 안녕 플라스크~~~</h1>
            <p style='color: blue'>첫 번째 플라스크 웹페이지임!</p>"""
        # HTML = 웹브가 처리가능한 형태의 코드구조
    return html
    # ctrl + alt + n: open and activate cmd in vscode
        # 이거 안해주면 웹브에 생성안됨!
    # http://127.0.0.1:9091/world -> 접속 후 결과화긴
    # 터미널 실행중단: 터미널 클릭상태에서 ctrl+c
    #----------------------------------------

# render_template 실습
@app.route("/myfood")
def myfood():
    return render_template("myfood.html")
    # render_template: 별도로 완성된 HTML 소스코드 
    # 맨 처음에 flask에서 import 했던거임
        # Flask에선 HTML파일을 저장한 폴더 이름을
        # templates로 정해두고 있음
    #----------------------------------------

# JSON 구조 실습
    # JSON을 출력하는 형식의 웹페이지 출력방법
@app.route("/mydata")
def mydata():
    mydict = {
        "name": "LEE", 
        "age": 24, 
        "height": 175, 
        "weight": 82
    }
    return mydict
    # python의 딕셔너리랑 웹에서 호환되는 데이터 교환형식
    # 디자인 없이 데이터만 컨텐츠로 제공
        # to '데이터분석' or 모바일앱
        # -> 데이터분석가가 직접 데이터 활용해서
            # 디자인 구성 또는 분석에 활용함

#---------------------------------------------
# [3] Flask 웹 서버 가동

if __name__ == "__main__":
    # 가동할 주소, 포트번호 지정 및 디버그 모드 활성화
        # 포트번호: 80 (기본값)
        # 디버그 모드:
            # 프로그램의 실행 과정을 개발자가
            # 파악할 수 있게 상세하게 출력
    app.run(port=9091, debug=True)
