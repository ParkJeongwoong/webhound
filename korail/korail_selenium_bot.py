from pickle import TRUE
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from pyvirtualdisplay import Display # 리눅스용
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep
import random
import os
import getpass

import korail_method as km

print('Korail KTX 자동 예매 봇 Start')

# Variables
URL = 'https://www.letskorail.com/korail/com/login.do'
month = input('월 입력 (숫자) : ')
day = input('일 입력 (숫자) : ')
first_time = input('가장 빠른 출발 시간 입력 (오전 7시 = 07, 오후 2시 = 14) : ')
last_time = input('가장 늦은 출발 시간 입력 (오전 7시 = 07, 오후 2시 = 14) : ')
is_find_ticket = False
timeout = 0
cnt = 0

botToken = input('Bot Token을 입력하세요 : ')
chatId = input('Chat Id를 입력하세요 : ')

pswd = getpass.getpass('비밀번호를 입력하세요')


# 드라이버 로드 (브라우저 실행)
virtual_display = Display(visible=0, size=(800, 600)) # 리눅스용
virtual_display.start() # 리눅스용

options = webdriver.ChromeOptions()
options.headless = TRUE
options.add_experimental_option("excludeSwitches", ["enable-logging"])
print(os.getcwd())
# driver = webdriver.Chrome(executable_path=r'{}'.format(os.getcwd()+'/chromedriver'), options=options)
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

# URL 설정
driver.get(url=URL)

# 로그인
print('로그인 중...')
id_box = driver.find_element(By.ID, r'txtMember')
id_box.send_keys('1373361352')
sleep(random.randint(1,5)/3)
password_box = driver.find_element(By.ID, r'txtPwd')
password_box.send_keys(pswd)
driver.find_element(By.XPATH, r'//*[@id="loginDisplay1"]/ul/li[3]/a').click()

# 로그인 후 페이지 이동
try:
    sleep(random.randint(1,5)/5)
    driver.get(url='https://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do')
    print('로그인 성공')

    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    # km.close_new_tabs(driver)
    departure = input('출발역 : ')
    arrival = input('도착역 : ')
except:
    print('로그인 실패')

driver.find_element(By.XPATH, r'//*[@id="s_month"]').send_keys(month)
driver.find_element(By.XPATH, r'//*[@id="s_day"]').send_keys(day)
driver.find_element(By.XPATH, r'//*//*[@id="s_hour"]').send_keys(int(first_time))
departure_box = driver.find_element(By.XPATH, r'//*[@id="start"]')
arrival_box = driver.find_element(By.XPATH, r'//*[@id="get"]')
departure_box.clear()
arrival_box.clear()
departure_box.send_keys(departure)
arrival_box.send_keys(arrival)

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
            start_time = result.find_element(By.XPATH, r'./td[3]').text
            if not start_time.startswith(departure):
                continue
            start_time = start_time.replace(departure+'\n','')
            if km.time_to_int(first_time+':00') < km.time_to_int(start_time) and km.time_to_int(start_time) < km.time_to_int(last_time+':00'):
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
        if not is_find_ticket:
            driver.find_element(By.XPATH, r'//*[@id="center"]/div[3]/p').click()
        timeout = 0
    except:
        timeout += 1
        print('로딩 지연 발생' + '(' + str(timeout) + ')')
        if timeout == 3:
            print('로딩 문제로 종료')
            break

# 예매 프로세스
if is_find_ticket:
    print('예매 성공!')
    km.send_telegram_message(botToken, chatId)
    sleep(random.randint(1,5)/3)
    km.close_alert(driver)
    km.close_alert(driver)

# 드라이버 종료 (브라우저 종료)
print('봇 종료')
driver.close()