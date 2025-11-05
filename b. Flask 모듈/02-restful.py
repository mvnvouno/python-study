# Restful API의 이해 (실습+초기설정)
#---------------------------------------------------------
# Flask 웹 서버 기본 구조
#---------------------------------------------------------
# GET Method:
    # GET 요청문의 뼈대 만들어놓으면 이후에 try-except 따로 안적어도됨
    # in URL: 
        # QueryString 방식으로 GET요청 드감:
            # http://127.0.0.1:9091/라우팅경로?변수명=값&변수명=값&..
    # in Python:
        # Flask에서 QueryString 파라미터 수신함
            # -> Flask 라이브러리의 request객체를 import 해야됨 by:
                # 파이썬변수 = request.args.get('변수명')
                    # args for arguments.
#---------------------------------------------------------
# [1] 패키지 참조:
from flask import Flask, request # 이 request 기능이 GET Method임!

#---------------------------------------------------------
# [2] Flask 메인객체 생성
    # __name__: 지금 이 소스파일 이름!
app = Flask(__name__)

    # 이후 코드들은 이 위치에 구현될거임 ↓
    # 신규 메서드들 추가가능 (ex. 예외처리 전용 메서드)
    #----------------------------------------

# [4] HTTP GET방식 데이터 전달법: 
    # request.args.get('')
    # URL로 송출 목표: http://127.0.0.1:9091/parameter?num1=123&num2=456
@app.route("/parameter", methods=['GET'])
def get():
    my_num1 = request.args.get('num1')
    my_num2 = request.args.get('num2')
    # URL에 보낼 변수들 추출 (num1=123&num2=456)

    sum1 = my_num1 + my_num2
    # import 받은 변수들은 다 문자열인거 보여주려는 예시

    sum2 = int(my_num1) + int(my_num2)
    # 덧셈 위해서는 int()로 항변환 시켜줘야 되는거 보여주는 예시

    mydict = {
        "expr": "%s + %s" % (my_num1, my_num2),
        "sum1": sum1,
        "sum2": sum2
    }

    return mydict
    # 결과 확인법
        # 1. ctrl+alt+n(터미널 명령프롬프트 실행) 후 웹브로 결과 화긴
            # GET만 화긴가능
        # 또는 Thunder Client(Restful API 전용 클라이언트)로 쿼리
            # GET, POST, PUT, DELETE 다 화긴가능
    # 결과 확인 후에는 ctrl+c 로 터미널 실행 종료하기
    #----------------------------------------

# HTTP POST, PUT, DELETE 방식의 파라미터 전달법:
    # request.form.get('')
    # 이 세 요청은 URL에 변수 노출 안하는 형태로 전달됨
        # 변수들 목적이 저장/수정 등이라서임

# [4] POST 파라미터 요청 처리:
@app.route("/parameter", methods=['POST'])
def post():
    x = request.form.get("x")
    y = request.form.get("y")

    z = int(x) * int(y)
    return {
        "expr": "%s * %s" % (x, y),
        "z": z
    }
    # POST는 웹브로 요청 처리 불가 -> Thunder Client ㄱㄱ
    #----------------------------------------

# [5] PUT 파라미터 요청:
@app.route("/parameter", methods=['PUT'])
def put():
    a = request.form.get("a")
    b = request.form.get("b")

    c = int(a) - int(b)

    return {
        "expr": "%s - %s" % (a, b),
        "c": c
    }
    #----------------------------------------

# [6] DELETE 파라미터 요청:
@app.route("/parameter", methods=['DELETE'])
def delete():
    m = request.form.get("m")
    n = request.form.get("n")

    o = int(m) / int(n)

    return {
        "expr": "%s / %s" % (m, n),
        "o": o
    }
    #----------------------------------------

# [7] PATH 파라미터 처리하기
    # GET, POST, PUT, DELETE 다 형식이똑같음
@app.route("/parameter/<myname>/<myage>", methods=['GET'])
def path_params(myname, myage):
    msg = "안녕하세요 {name}님, 당신은 {age}세 입니다."

    return {
        "msg": msg.format(name = myname, age = myage)
    }

    # PATH문 결과처리 확인방법:
        # Thunder Client의 URL에 변수값 다 직접 입력
            # 한글데이터 처리가 불안정 -> 변수 다 영문으로 기입 ㄱ
    #----------------------------------------

# [8] 에러처리 함수
    # 예외 발생 시 호출되는 함수
    # try~except 효과랑 동일함
@app.errorhandler(Exception)
def error_handling(error):
    return ({'massage': str(error)}, 500)
    # 500: 웹서버에서 에러가 발생함을 클라이언트에게 알리는 코드값
    # 에러내용, 상태코드를 튜플 형식으로 변환함

    # 결과처리 확인방법:
        # Thunder Client -> get의 num2에 일부러 정수가 아닌 abc 넣어서 화긴 ㄱ
#---------------------------------------------------------
# [3] Flask 웹서버 가동:
if __name__ == "__main__":
    app.run(port=9091, debug=True)
    # for: 가동할 주소, 포트번호, 디버그 모드 활성
        # 포트번호 기본값: 80
        # 디버그 모드: 프로그램 실행과정을 개발자가 파악할 수 있게 상세하게 출력함