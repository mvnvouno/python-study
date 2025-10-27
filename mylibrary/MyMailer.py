## # 01. 메일 발송 모듈 제작
# (lab08 참조)
# 구글 앱비밀번호: uirh ysyy jfia ktlr

#--------------------------------------------
# 참조할 라이브러리 정의
import os
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

#--------------------------------------------
# 메일 발송 함수 만들기 (함수(및 이름) 정의)
#--------------------------------------------
def sendMail(from_addr, to_addr, subject, content, files=[]):
    content_type = "plain"

    username = "29alsdud@gmail.com"
    password = "uirh ysyy jfia ktlr"    # (구글 앱 비밀번호)

    smtp = "smtp.gmail.com"
    port = 587

    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr

    msg.attach(MIMEText(content, content_type))

    if files: # 여기서 file은 리스트임!
        for file_item in files:
            if os.path.exists(file_item):
                with open(file_item, 'rb') as f:
                    basename = os.path.basename(file_item)
                    part = MIMEApplication(f.read(), Name=basename)

                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename
                    msg.attach(part)

                    print(basename, "(이)가 첨부 되었습니다.")


    mail = SMTP(smtp)
    mail.ehlo()
    mail.starttls()
    mail.login(username, password)
    mail.sendmail(from_addr, to_addr, msg.as_string())
    mail.quit()
#--------------------------------------------
# 테스트 코드
#--------------------------------------------
if __name__ == "__main__":
    sendMail("29alsdud@gmail.com", "29alsdud@gmail.com", "오늘 점심 메뉴 추천이욥", "아아, mike check mike check, ok")