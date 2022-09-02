사용 전 ! root 폴더에 chromedriver.exe 필요

```sh
$ python -m venv venv
$ source venv/scripts/activate
(venv)  --> 이거 뜨고 나서
$ pip install -r requirements.txt --> 이러면 requirements.txt에 있는 라이브러리 설치

$ deactivate --> 가상환경 해제
```

requirements.txt 예시
```
asgiref==3.3.1
beautifulsoup4==4.9.3
Django==3.1.7
django-bootstrap-v5==1.0.1
django-extensions==3.1.1
importlib-metadata==2.1.1
pytz==2021.1
soupsieve==2.2.1
sqlparse==0.4.1
zipp==3.4.1
```

서버환경의 리눅스에서 chromedriver를 사용하려면 HEADLESS 작업이 필요하므로 xvbf(리눅스의 가상 디스플레이 버퍼)와 pyvirtualdisplay(파이썬에서 xvbf 활용)가 필요
```sh
$ sudo apt-get install xvfb
$ sudo pip install pyvirtualdisplay
```
이후 chromedriver 실행코드에 다음을 추가해야 함
```python
from selenium import webdriver
from pyvirtualdisplay import Display

virtual_display = Display(visible=0, size=(800, 600))
virtual_display.start()
driver = webdriver.Chrome()
driver.get(주소)
driver.quit()
virtual_display.stop()
```