from selenium.webdriver.common.by import By
import requests

def time_to_int(time):
    return int(time.replace(':',''))

def close_alert(driver):
    try:
        alert = driver.switch_to.alert
        alert.accept() # 확인
        # alert.dismiss() # 취소
    except:
        print('no alert')

def close_new_tabs(driver):
    tabs = driver.window_handles
    while len(tabs) != 1:
        driver.switch_to.window(tabs[1])
        driver.close()
        tabs = driver.window_handles
    driver.switch_to.window(tabs[0])

def send_telegram_message(botToken, chatId):
    if (not botToken or not chatId):
        return
    
    message = '예약에 성공했습니다. Korail 예약을 확인해주세요'
    send_message_url = f'https://api.telegram.org/bot{botToken}/sendmessage?chat_id={chatId}&text={message}'

    requests.get(send_message_url)

def get_telegram_message(botToken, chatId):
    if (not botToken or not chatId):
        return
    
    get_message_url = f'https://api.telegram.org/bot{botToken}/getUpdates'
    recieved_message = requests.get(get_message_url).json()['result'][-1]['message']['text']
    print(recieved_message)