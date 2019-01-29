# PyFGOkr

PyFGOkr은 넷마블이 서비스하는 게임 Fate Grand Order에 관한 프로그램 개발을 편하게 하기 위해 만든 패키지입니다. [Discord.py](https://discordpy.readthedocs.io/en/rewrite/index.html)를 이용해 만든 채팅 봇에 각종 기능을 추가하다가, 나 말고 다른 사람들도 이용할 수 있으면 좋겠다는 생각에 패키지화 시켜서 만들게 되었습니다.

사용하기 위해선 Python 3.6+와 다음과 같은 모듈과 패키지가 필요합니다.

* sqlite3
* bs4
* requests
* Pillow

> pip install <패키지 명>

윈도우즈의 `명령 프롬프트`나 리눅스의 `터미널`을 열어 위의 명령어를 입력하여 설치해주세요.



## 각 모듈에 대한 설명

[다음 문서](./src/PyFGOkr/DOCUMENTATION.MD)를 참고해주세요.



## 모듈 외의 내장 프로그램

|   프로그램 이름    |     경로     |                             기능                             |
| :----------------: | :----------: | :----------------------------------------------------------: |
| gacha_imgresize.py |   PyFGOkr/   | 실행 시 뽑기 시뮬레이션을 할 수 있도록 img 폴더의 리소스 이미지들을 리사이즈시킵니다. 애플리케이션이 실행될 때마다 리소스를 리사이즈 시키고 싶다면 이 프로그램을 import 시켜주세요. |
|   imgcrawling.py   | PyFGOkr/img/ | 뽑기 최신화를 위한 리소스 이미지를 크롤링하기 위해 만들어진 프로그램입니다. all_data란 폴더가 만들어지고 서번트 이미지가, all_data 하위에 만들어지는 cr 폴더엔 예장 정보가 저장됩니다. 이 프로그램은 [바이너리 파일](https://github.com/GoatHead/PyFGOkr/releases/download/19.01.30/imgcrawling.exe)로도 다운 받을 수 있습니다. |



## 저작권

[MIT License](https://ko.wikipedia.org/wiki/MIT_%ED%97%88%EA%B0%80%EC%84%9C)를 따릅니다.
