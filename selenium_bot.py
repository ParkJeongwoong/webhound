import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep

# URL
URL = 'https://www.google.com/'

# 드라이버 로드 (브라우저 실행)
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(executable_path='chromedriver', options=options)

# URL 설정
driver.get(url=URL)

# 검색창 찾기
search_box = driver.find_element(By.XPATH, r'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')

# 검색어 입력
search_box.send_keys('parkjeongwoong.github.io')
search_box.send_keys(Keys.RETURN)

# results = driver.find_elements(By.XPATH, r'//*[@id="rso"]/div[2]/div/div/div[1]/div')
results = driver.find_elements(By.XPATH, r'//*[@id="rso"]/div')

# 검색 결과 파일 생성
print('검색 URL : ' + driver.current_url + '\n', file=open('parkjeongwoong.txt', 'w', encoding='utf-8'))
for result in results:
    print(result.text)
    # print(result.text, file=open('parkjeongwoong.txt', 'w', encoding='utf-8'))
    print(result.text, file=open('parkjeongwoong.txt', 'a', encoding='utf-8'))
    print('\n', file=open('parkjeongwoong.txt', 'a', encoding='utf-8'))

# 최상단 검색결과 접속
result = driver.find_element(By.XPATH, r'//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[1]/div/a')
result.click()

# 현재 URL 체크
print("Current URL : " + driver.current_url)

# 드라이버 종료 (브라우저 종료)
# sleep(3)
driver.close()