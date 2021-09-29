# 基于selenium的download核
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
from tqdm import tqdm
import pyautogui


def download_core(imgid):
    http_proxy = "http://127.0.0.1:7890"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={}'.format(http_proxy))
    driver = webdriver.Chrome(chrome_options=chrome_options)
    print('start downloading...')
    for _ in tqdm(imgid):
        url = 'https://yande.re/post/show/{}'.format(_)
        driver.get(url)
        wait = WebDriverWait(driver, 4)
        try:
            img = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="png"]')))
        except TimeoutException:
            try:
                img = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="highres"]')))
            except:
                continue
        actions = ActionChains(driver)
        actions.click(img)
        # actions.move_by_offset(-110, -610)
        # actions.context_click()
        actions.perform()
        time.sleep(1)
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1)
        pyautogui.typewrite(['enter'])
        time.sleep(1)
        if _ == imgid[-1]:
            time.sleep(15)
        if len(imgid) == 1:
            time.sleep(90)
    print('download successful')
    # WebDriverWait(driver, 8)
    driver.close()
    return
