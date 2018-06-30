import os
from PIL import Image
import pytesseract
import selenium
from selenium import webdriver
import cv2
import time
from pywinauto import application
import csv
from grabscreen import grab_screen
import io
import numpy as np

"""
os.chdir('C:\\Users\\royal\\Downloads\\Compressed\\DeepGamingAI_FIFARL-master')

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

chromedriver = "C:\\Users\\royal\\Downloads\\Programs\\chromedriver_win32\\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

"""
rate=[2.25, 2.50, 2.75, 3.00, 3.25, 3.50, 3.75, 4.00, 4.25, 4.50, 4.75, 5.00, 5.25, 5.50, 5.75, 6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00, 8.25, 8.50, 8.75, 9.00, 9.25, 9.50, 9.75]

def open_page_start(driver):
    #open the chrome browser with site and then maximize the window and click on play now.
    driver.get("https://sffed-education.org/chairthefed/WebGamePlay.html")
    driver.maximize_window()
    driver.find_elements_by_xpath('//*[@id="play_now_button"]')[0].click()
    #time.sleep(5)
    #driver.execute_script("window.scrollTo(0, 100)")

def get_to_foreground():
    ##get the window to foreground.
    app = application.Application()
    app.connect(title_re=".*%s.*" % "Chair the Fed")
    app_dialog = app.top_window_()
    app_dialog.Minimize()
    app_dialog.Restore()

def click_go(driver):
    driver.find_elements_by_xpath('//*[@id="go_button_anchor"]')[0].click()
    time.sleep(8)

def click_raise(driver):
    driver.find_elements_by_xpath('//*[@id="increase_button_anchor"]')[0].click()
    time.sleep(1)

def click_cut(driver):
    driver.find_elements_by_xpath('//*[@id="decrease_button_anchor"]')[0].click()
    time.sleep(1)

def get_news(screen):
    news = screen[2:100,451:1086]
    i = Image.fromarray(news.astype('uint8'), 'RGB')
    st = pytesseract.image_to_string(i, lang = 'eng')
    return st

def get_quaters(screen):
    quat = screen[158:202,1190:1249]
    i = Image.fromarray(quat.astype('uint8'), 'RGB')
    st = pytesseract.image_to_string(i, lang = 'eng')
    return st

def get_fed_rates(screen):
    fed = screen[263:341,1108:1277]
    i = Image.fromarray(fed.astype('uint8'), 'RGB')
    st = pytesseract.image_to_string(i, lang = 'eng')
    return st

def get_unemploy_rate(screen):
    unemp = screen[411:488,1108:1277]
    i = Image.fromarray(unemp.astype('uint8'), 'RGB')
    st = pytesseract.image_to_string(i, lang = 'eng')
    return st

def get_inflate_rate(screen):
    inflat = screen[559:610,1108:1277]
    i = Image.fromarray(inflat.astype('uint8'), 'RGB')
    st = pytesseract.image_to_string(i, lang = 'eng')
    return st

def get_last_msg(driver):
    screen = screen_grab(driver)
    #cv2.imwrite('record\\last'+'.PNG',screen)
    last = screen[45:137,327:1045]
    i = Image.fromarray(last.astype('uint8'), 'RGB')
    st = pytesseract.image_to_string(i, lang = 'eng')
    if st=='Congratulations!':
        play_again_win(driver)
        time.sleep(12)
    if st=='Sorry.':
        play_again_loss(driver)
        time.sleep(12)
    return st

def set_fed_rate(driver,curr,nex):
    mov=0
    if (curr>nex):
        mov=int((curr-nex)//0.25)
        for i in range(mov):
            click_cut(driver)
    else:
        mov=int((nex-curr)//0.25)
        for i in range(mov):
            click_raise(driver)
    ##not for hardcoded action
    click_go(driver)

def record(i,screen):
    cv2.imwrite('record\\hh'+str(i)+'.PNG',screen)
    news=' '.join(get_news(screen).split('\n'))
    fed=''.join(get_fed_rates(screen).split()).split('%')[0]
    unemp=''.join(get_unemploy_rate(screen).split()).split('%')[0]
    infl=''.join(get_inflate_rate(screen).split()).split('%')[0]
    data=str(16-i)+','+fed+','+unemp+','+infl+','+news
    print(data)
    with open('record\\csvex.csv','a', encoding="utf-8") as myFile:
        myFile.write(data+'\n')

def play_again_win(driver):
    driver.find_elements_by_xpath('//*[@id="win_play_now_button_anchor"]')[0].click()

def play_again_loss(driver):
    driver.find_elements_by_xpath('//*[@id="lose_play_now_button_anchor"]')[0].click()

def screen_grab(driver):
    driver.execute_script("window.scrollTo(0, 100)")
    data = driver.get_screenshot_as_png()
    img = Image.open(io.BytesIO(data))
    return cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)

def play(driver):
    time.sleep(18)
    driver.execute_script("window.scrollTo(0, 100)")
    rate=[4.00, 4.00, 4.00, 4.25, 4.25, 4.75, 4.25, 4.00, 4.25, 4.50, 4.75, 4.75, 4.25, 4.50, 4.75, 4.75]
    for i,j in enumerate(rate):
        #screen = grab_screen(region=None)
        screen = screen_grab(driver)
        record(i,screen)
        fed = get_fed_rates(screen)
        fed=float(''.join(fed.split()).split('%')[0])
        print(fed)
        set_fed_rate(driver,fed,j)
        click_go(driver)
"""
with open('record\\csvex.csv','a', encoding="utf-8") as myFile:
    myFile.write('Quarters,FedRate,Unemployment,Inflation,News'+'\n')

print('started!!!')
open_page_start(driver)
for i in range(3):
    play(driver)
    st = get_last_msg(driver)
    if st=='Congratulations!':
        play_again_win(driver)
    else:
        play_again_loss(driver)
    
print('finished!!!')
"""
