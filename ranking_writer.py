# -*- coding: utf-8 -*-
 
import sys
import io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import random
import re
import requests
from bs4 import BeautifulSoup

#chromedriverの場所を指定
options = webdriver.ChromeOptions()
options.add_argument("") #chromedriverの場所

#chromedriver.exeを使う
driver = webdriver.Chrome("./chromedriver.exe", chrome_options=options) 
driver.implicitly_wait(5)

#detailかmemberで切り替え
lists = ["detail", "member"]

#1から1000までとりあえず様子見
driver.get("")　#一度ゲームのメイン画面を開く
time.sleep(2.0)


raw_str1 = r"" #団ランキング用のフォルダ
#ファイル名に日付をつける
f = open(raw_str1+datetime.now().strftime("%Y%m%d %H%M%S")+'.csv','a',encoding='UTF-8-sig')
f.write(datetime.now().strftime("%Y/%m/%d %H:%M:%S")+",,,,,"+"\n")



print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
for guild_id in range(1, 11):

    rn = random.uniform(1.15, 1.24)
    
    urls = "" + str(guild_id)　#イベントランキングのURLを入力
    driver.get(urls)
    time.sleep(rn)


    page_source = driver.page_source
    link_soup = BeautifulSoup(page_source, 'html.parser')
    div = link_soup.find_all('div', class_='txt-name')
    div2 = link_soup.find_all('div', class_='txt-rank')
    div3 = link_soup.find_all('div', class_='txt-total-record')
    div4 = link_soup.find_all('div', class_='btn-ranking-profile')

    #ページの1~10番目までの団それぞれに対してのループ
    for v in range(0, 10):

        #Rankと体を正規表現で消す
        try:
            div2[v] = re.sub(r"Rank", "", div2[v].text)
        
            div3[v] = re.sub(r"体", "", div3[v].text)
        
        
            
        #div classの中のhrefの中にあるprofileをひっぱりだす
            div4[v] = div4[v].get('data-href')
            
            div4[v] = re.sub(r"guild/detail/", "", div4[v])
        except IndexError:
            continue

        #この時点でdiv2[v]とdiv3[2*v]はstringになっているので.textを付ける必要はない
        #結果の出力　足すだけ
        #guild_idはページ番号　
        phrase3 = str((guild_id-1)*10+v+1)+",\""+div[v].text+"\",\""+div2[v]+"\",\""+div3[v]+ "\"," + div4[v]+",guild_total_detail_38"
        print(phrase3)
        f.write(phrase3 +"\n")



f.close()
