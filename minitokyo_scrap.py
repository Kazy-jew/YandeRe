from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyautogui
from tqdm import tqdm
import os


def minitokyo_download(idl):
    path = 'C:\\Users\\tokisaki\\Downloads'
    signal = 'confirm'
    circle_times = 0
    http_proxy = "127.0.0.1:7890"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={}'.format(http_proxy))
    driver = webdriver.Chrome() #chrome_options=chrome_options)
    url_origin = 'http://my.minitokyo.net/login'
    driver.get(url_origin)
    username = driver.find_element_by_xpath('//*[@id="username"]')
    username.send_keys('***********')
    password = driver.find_element_by_xpath('//*[@id="content"]/form/li[2]/input')
    password.send_keys('***********')
    log_in = driver.find_element_by_xpath('//*[@id="content"]/form/li[3]/input')
    log_in.click()
    time.sleep(3)
    while signal == 'confirm':
        circle_times += 1
        list1 = os.listdir(path)
        minitokyo_downloaded = []
        for name in list1:
            if name.endswith('jpg'):
                minitokyo_image = name.split('.')[0]
                minitokyo_downloaded.append(minitokyo_image)
        diff = list(set(idl) - set(minitokyo_downloaded))
        if len(diff) == 0:
            signal = 'deny'
            print('Finally, all pictures have been downloaded')
        elif circle_times == 5:
            signal = 'deny'
            print('Almost downloaded with some exceptions')
            print(diff)
        else:
            print('start downloading...')
            for _ in tqdm(diff):
                url = 'http://gallery.minitokyo.net/download/{}'.format(_)
                driver.get(url)
                # wait = WebDriverWait(driver, 1)
                location = driver.find_element_by_xpath('//*[@id="image"]/p/a')
                # location.send_keys(Keys.PAGE_DOWN)
                # driver.execute_script("arguments[0].scrollIntoView();", loaction)
                # driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(location, 100, 100).perform()
                actions.context_click().perform()
                pyautogui.typewrite(['down', 'down', 'enter'])
                time.sleep(0.8)
                pyautogui.typewrite(['enter'])
            print('download successful')
            time.sleep(3)
    driver.quit()


while True:
    minitokyo = input('please input an id range (id > 757945), q to quit:')
    minitokyo_list = []
    if minitokyo == 'q':
        exit()
    else:
        minitokyo_id = minitokyo.split(' ')
        minitokyo_delta = int(minitokyo_id[1]) - int(minitokyo_id[0])
        for _ in range(minitokyo_delta+1):
            minitokyo_list.append(str(int(minitokyo_id[0])+_))
        minitokyo_download(minitokyo_list)


