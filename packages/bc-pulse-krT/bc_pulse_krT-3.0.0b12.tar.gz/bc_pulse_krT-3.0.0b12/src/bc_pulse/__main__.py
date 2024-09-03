import sys
import requests
import os
from datetime import datetime, timedelta
from colorama import init, Fore, Style
import bc_pulse
from bc_pulse import cli
import traceback 

init()
# 털묵스, a-shell 기준
# # 홈 디렉토리를 기준으로 설정
KEY_DIR = "./key"
KEY_FILE_PATH = os.path.join(KEY_DIR, "key.txt")

def check_key_with_server(key, check_key=False):
    data = {'resultText': key, 'check_key': 'true' if check_key else 'false'}
    response = requests.post("https://www.mod-mon.com/bctest/checkKey.php", data=data)
    return response

# 키 폴더가 없으면 생성
if not os.path.exists(KEY_DIR):
    os.makedirs(KEY_DIR)
    
    
#로컬기준
# KEY_DIR = "key"
# KEY_FILE_PATH = os.path.join(KEY_DIR, "key.txt")

# def check_key_with_server(key, check_key=False):
#     data = {'resultText': key, 'check_key': 'true' if check_key else 'false'}
#     response = requests.post("https://www.mod-mon.com/bcsfe_pulse/checkKey.php", data=data)
#     return response
# # # 키 폴더가 없으면 생성
# if not os.path.exists(KEY_DIR):
#     os.makedirs(KEY_DIR)
    
# 키 파일이 있는지 확인
if os.path.exists(KEY_FILE_PATH):
    # 파일 생성 시간을 확인
    creation_time = os.path.getctime(KEY_FILE_PATH)
    creation_date = datetime.fromtimestamp(creation_time)

    # 파일이 3일이 지났으면 삭제
    if datetime.now() - creation_date > timedelta(days=3):
        os.remove(KEY_FILE_PATH)
    else:
        with open(KEY_FILE_PATH, 'r') as file:
            saved_key = file.read().strip()
            # 서버에 키 확인 요청, 파일이 있을 때 check_key=True
            response = check_key_with_server(saved_key, check_key=True)
            if response.status_code == 200:
                print("프로그램을 정상적으로 실행합니다.")
                cli.main.Main().main()
                sys.exit(0)
            else:
                print(response.text)
                print("에러 001 : 작동이 안되면 \"쿠지티비\" 사이트에 문의")
                sys.exit(1)

# 키 입력 받기
user_input = input(f"\n{Fore.GREEN}구글에서 {Fore.RESET}{Fore.RED}\"쿠지티비\"{Fore.RESET}{Fore.GREEN}를 검색 해주세요!{Fore.RESET}\n{Fore.GREEN}또는 {Fore.RESET}{Fore.RED}\"www.mod-mon.com\"{Fore.RESET}{Fore.GREEN}으로 접속 해주세요!\n\n{Fore.RESET}{Fore.RED}\"쿠지티비\"{Fore.RESET}{Fore.GREEN}에서 발급받은 키를 붙여넣으세요:{Fore.RESET}\n")

# 키 서버에 전송 및 확인
response = check_key_with_server(user_input)
if response.status_code == 200:
    print("키가 유효하며 프로그램을 실행합니다.")
    
    update_response = requests.post("https://www.mod-mon.com/bcsfe_pulse/updateKey.php", data={'resultText': user_input})
    if update_response.status_code == 200:
        if os.path.exists(KEY_FILE_PATH):
            os.remove(KEY_FILE_PATH)

        try:
            with open(KEY_FILE_PATH, 'w') as file:
                file.write(user_input)
        except Exception as e:
            print(f"에러 002 : 작동이 안되면 \"쿠지티비\" 사이트에 문의")
            sys.exit(1)
    else:
        print("에러 003 : 작동이 안되면 \"쿠지티비\" 사이트에 문의")
        sys.exit(1)
else:
    print(f"\n{Fore.GREEN}키가 틀렸거나 이미 사용되었습니다.\n{Fore.RED}\"쿠지티비\"{Fore.RESET} {Fore.GREEN}사이트에서 {Fore.RED}키{Fore.RESET}{Fore.GREEN}를 재발급 받으세요.{Fore.RESET}")
    sys.exit(1)



cli.main.Main().main()






args = sys.argv[1:]
for arg in args:
    if arg.lower() in ["--version", "-v"]:
        print(bc_pulse.__version__)
        exit()
