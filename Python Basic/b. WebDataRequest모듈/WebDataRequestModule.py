#--------------------------------------------------
# 웹데이터 요청문
    # 사이트에서 데이터를 규격에 맞게 요청, 응답 받기
#--------------------------------------------------
# GET request
#--------------------------------------------------
# 0. API 명세를 확인 -> 요청에 필요한 정보들 변수로 구성 ㄱ
    # -> QueryString은 params 파라미터에 딕셔너리 형식으로 구성됨
    # (POST, PUT, DELETE는 data로 파라미터 이름 지정)

# 1. 크롬 창에서 응답 구조 화긴
    # QueryString(규격URL/?규격변수=값$규격변수2=값..)
    # http://127.0.0.1:9091/라우팅경로?변수명=값&변수명=값&..

# 2. 참조할 라이브러리들 import 하기
import requests
import datetime as dt
from pandas import DataFrame # 이건 예시임

# 3. 요청할 것을 변수 설정
    # 요청 URL:
url = "요청 규격에 맞는 주소"

    # 발급받은 API 키:
API_KEY = "해당사이트의 API 키"

# 그 외의 요청 원하는 기타 값들은 변수, 함수, 식 등으로 정의 ㄱ
# "사이트규격변수2", 요청하고 싶은 변수 이름

# 4. 웹데이터 요청하기
with requests.Session() as session:
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})

    r = session.get(url, params={"해당사이트의 API 키(if QueryString)": API_KEY, "규격요청변수2": 요청하고 싶은 변수 이름(코딩에서 지정한거)})

    if r.status_code != 200:
        msg = "[%d Error] %s 에러가 발생함" % (r.status_code, r.reason)
        raise Exception(msg)
    
    print(r)

# 5. 응답결과 화긴
mydict = r.json()
print(mydict)

# 6. 응답결과를 프레임화
df = DataFrame(mydict["규격응답(1.에서 확인한거)"]["if dic-> dic(or list)일 때"])
df # df.to_excel("파일이름.xlsx") 만약 다음에 재사용 필요시 파일저장 
        # 저장 후 저장된 파일은 VScode Excel 익스텐션으로 화긴 ㄱ
#--------------------------------------------------

#--------------------------------------------------

#--------------------------------------------------

#--------------------------------------------------