import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
import random
import os

import korail_method as km

print('Korail KTX 자동 예매 봇 Start')

# Variables
URL = 'https://www.letskorail.com/korail/com/login.do'
month = 9
day = 12
from_time = '09:10'
to_time = '14:00'
is_find_ticket = False
timeout = 0
cnt = 0

pswd = input('비밀번호를 입력하세요')


# 드라이버 로드 (브라우저 실행)
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
print(os.getcwd())
driver = webdriver.Chrome(executable_path=r'{}'.format(os.getcwd()+'/chromedriver'), options=options)

# URL 설정
driver.get(url=URL)

# 로그인
print('로그인 중...')
id_box = driver.find_element(By.ID, r'txtMember')
id_box.send_keys('1373361352')
sleep(random.randint(1,5)/3)
password_box = driver.find_element(By.ID, r'txtPwd')
password_box.send_keys(pswd)

# 로그인 후 페이지 이동
driver.find_element(By.XPATH, r'//*[@id="loginDisplay1"]/ul/li[3]/a').click()
print('로그인 성공')

sleep(random.randint(1,5)/5)
driver.get(url='https://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do')
driver.find_element(By.XPATH, r'//*[@id="s_month"]').send_keys(month)
driver.find_element(By.XPATH, r'//*[@id="s_day"]').send_keys(day)
driver.find_element(By.XPATH, r'//*[@id="center"]/form/div/p/a').click()

# 예약 시작
print('예약 시작')

# 객실 찾기
while not is_find_ticket:
    try:
        sleep(random.randint(1,5)/3)
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, r'//*[@id="tableResult"]/tbody/tr')))
        cnt += 1
        print(str(cnt) + '차 시도')
        results = driver.find_elements(By.XPATH, r'//*[@id="tableResult"]/tbody/tr')
        for result in results:
            start_time = result.find_element(By.XPATH, r'./td[3]').text.replace('신경주\n','')
            if km.time_to_int(from_time) < km.time_to_int(start_time) and km.time_to_int(start_time) < km.time_to_int(to_time):
                print('출발시간 : ' + start_time)
                # 일반실
                try:
                    norm_seat = result.find_element(By.XPATH, r'./td[6]/a[1]')
                    norm_seat.click()
                    is_find_ticket = True
                    print('일반실 예매')
                    break
                except:
                    print('일반실 매진')
                # 특실
                try:
                    premium_seat = result.find_element(By.XPATH, r'./td[5]/a[1]')
                    premium_seat.click()
                    is_find_ticket = True
                    print('특실 예매')
                    break
                except:
                    print('특실 매진')
        driver.find_element(By.XPATH, r'//*[@id="center"]/div[3]/p').click()
        timeout = 0
    except:
        timeout += 1
        print('로딩 지연 발생' + '(' + str(timeout) + ')')
        if timeout == 10:
            print('로딩 문제로 종료')
            break

# 예매 프로세스
if is_find_ticket:
    sleep(random.randint(1,5)/3)
    km.close_alert(driver)
    km.close_alert(driver)

# 드라이버 종료 (브라우저 종료)
print('봇 종료')
driver.close()