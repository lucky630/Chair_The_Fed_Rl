import os
from PIL import Image
import pytesseract
import selenium
from selenium import webdriver
import cv2
import time
from pywinauto import application
import pyautogui
import csv
from grabscreen import grab_screen

os.chdir('C:\\Users\\royal\\Downloads\\Compressed\\DeepGamingAI_FIFARL-master')

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

chromedriver = "C:\\Users\\royal\\Downloads\\Programs\\chromedriver_win32\\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

rate=[2.25, 2.50, 2.75, 3.00, 3.25, 3.50, 3.75, 4.00, 4.25, 4.50, 4.75, 5.00, 5.25, 5.50, 5.75, 6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00, 8.25, 8.50, 8.75, 9.00, 9.25, 9.50, 9.75]

def open_page_start(driver):
    #open the chrome browser with site and then maximize the window and click on play now.
    driver.get("https://sffed-education.org/chairthefed/WebGamePlay.html")
    driver.maximize_window()
    driver.find_elements_by_xpath('//*[@id="play_now_button"]')[0].click()
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 100)")

def get_to_foreground():
    ##get the window to foreground.
    app = application.Application()
    app.connect(title_re=".*%s.*" % "Chair the Fed")
    app_dialog = app.top_window_()
    app_dialog.Minimize()
    app_dialog.Restore()

def click_go():
    pyautogui.click(136,680)
    time.sleep(10)

def click_raise():
    pyautogui.click(95,569)
    time.sleep(2)

def click_cut():
    pyautogui.click(182,569)
    time.sleep(2)

def get_news(screen):
    news = screen[113:213,447:1080]
    i = Image.fromarray(news.astype('uint8'), 'RGB')
    st = pytesseract.image_to_string(i, lang = 'eng')
    return st

def get_quaters(screen):
    quat = screen[158:202,1190:1249]
    i = Image.fromarray(quat.astype('uint8'), 'RGB')
    st = pytesseract.image_to_string(i, lang = 'eng')
    return st

def get_fed_rates(screen):
    fed = screen[372:449,1108:1276]
    i = Image.fromarray(fed.astype('uint8'), 'RGB')
    st = pytesseract.image_to_string(i, lang = 'eng')
    return st

def get_unemploy_rate(screen):
    unemp = screen[521:599,1108:1276]
    i = Image.fromarray(unemp.astype('uint8'), 'RGB')
    st = pytesseract.image_to_string(i, lang = 'eng')
    return st

def get_inflate_rate(screen):
    inflat = screen[670:722,1108:1276]
    i = Image.fromarray(inflat.astype('uint8'), 'RGB')
    st = pytesseract.image_to_string(i, lang = 'eng')
    return st

def get_last_msg(driver):
    screen = grab_screen(region=None)
    last = screen[337:434,300:1072]
    i = Image.fromarray(last.astype('uint8'), 'RGB')
    st = pytesseract.image_to_string(i, lang = 'eng')
    return st

def set_fed_rate(curr,nex):
    mov=0
    if (curr>nex):
        mov=int((curr-nex)//0.25)
        for i in range(mov):
            click_cut()
    else:
        mov=int((nex-curr)//0.25)
        for i in range(mov):
            click_raise()

def record(i,screen):
    cv2.imwrite('record\\hh'+str(i)+'.jpg',screen)
    news=' '.join(get_news(screen).split('\n'))
    fed=''.join(get_fed_rates(screen).split()).split('%')[0]
    unemp=''.join(get_unemploy_rate(screen).split()).split('%')[0]
    infl=''.join(get_inflate_rate(screen).split()).split('%')[0]
    data=str(16-i)+','+fed+','+unemp+','+infl+','+news
    print(data)
    with open('record\\csvex.csv','a', encoding="utf-8") as myFile:
        myFile.write(data+'\n')

def play_again(driver):
    driver.find_elements_by_xpath('//*[@id="win_play_now_button_anchor"]')[0].click()
    
def play(driver):
    open_page_start(driver)
    rate=[4.00, 4.00, 4.00, 4.25, 4.25, 4.75, 4.25, 4.00, 4.25, 4.50, 4.75, 4.75, 4.25, 4.50, 4.75, 4.75]
    for i,j in enumerate(rate):
        screen = grab_screen(region=None)
        record(i,screen)
        fed = get_fed_rates(screen)
        fed=float(''.join(fed.split()).split('%')[0])
        print(fed)
        set_fed_rate(fed,j)
        click_go()

with open('record\\csvex.csv','a', encoding="utf-8") as myFile:
    myFile.write('Quarters,FedRate,Unemployment,Inflation,News'+'\n')

play(driver)
