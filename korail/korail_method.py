from selenium.webdriver.common.by import By

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