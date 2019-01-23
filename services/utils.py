# author: tiankai
# copywrite 2019

import time
from selenium import webdriver

def init_webdriver():

    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': '/Users/tiankai/projects/BaiduWK/services/static/tmp'}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    driver.get('https://wenku.baidu.com/')

    # 先获得登陆界面
    login_box = driver.find_element_by_id('login')

    # 跳转到登陆界面
    driver.get(login_box.get_attribute('href'))

    # 采用用户名登陆
    driver.execute_script("document.getElementById('login').style='display: block; visibility: visible; opacity: 1;';")
    time.sleep(1)
    # 找到输入框
    driver.execute_script("document.getElementById('TANGRAM__PSP_3__userName').value='593014895@qq.com';")
    time.sleep(5)
    driver.execute_script("document.getElementById('TANGRAM__PSP_3__password').value='ABcd593014895';")
    time.sleep(5)

    # 登陆
    login_btn = driver.find_element_by_id('TANGRAM__PSP_3__submit')
    login_btn.submit()
    time.sleep(5)

    return driver

# 下载百度文库文件
def download(driver, fileURL):

    driver.get(fileURL)

    # 下载按钮
    download_btn = driver.find_element_by_css_selector('.reader-download.btn-download')
    download_btn.click()
    time.sleep(1)

    # 需要再次确认的情况(非自己账号的文档, 未下载过)
    try:
        download_btn = driver.find_element_by_css_selector('.ui-bz-btn-senior.btn-diaolog-downdoc')
    # 下载过的情况
    except:
        download_btn = driver.find_element_by_id('WkDialogOk')
    download_btn.click()

    print("下载完成")
