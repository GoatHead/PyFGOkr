from sys import exit
import sys
import os
fpath = os.path.dirname(__file__)
sys.path.insert(0, '../')
import shutil
import requests

def __init__():
    cmd = 'mode 143,30'
    os.system(cmd)
__init__()
def crawl_craftimg(MINRANGE=1, MAXRANGE=2000):
    for imgno in range(MINRANGE,MAXRANGE):
        url = 'http://appdata.hungryapp.co.kr/images/dbimg/fgo/cicon/cr{0:03d}.png'.format(imgno)
        response = requests.get(url, stream=True)
        if response.status_code == 404:
            break
        else:
            cpath = os.path.join(fpath, 'all_data/cr/cr{0:03d}.png'.format(imgno).replace('\\', '/'))
            with open(cpath, 'wb') as out_file:
                print('copy: {}'.format(out_file.name))
                shutil.copyfileobj(response.raw, out_file)
        del response

def crawl_servimg(MINRANGE=1, MAXRANGE=500):
    for imgno in range(MINRANGE,MAXRANGE):
        url = 'http://appdata.hungryapp.co.kr/images/dbimg/fgo/thum/{0:03d}.png'.format(imgno)
        response = requests.get(url, stream=True)
        if response.status_code == 404:
            break
        else:
            cpath = os.path.join(fpath, 'all_data/{0:03d}.png'.format(imgno).replace('\\', '/'))
            with open(cpath, 'wb') as out_file:
                print('copy: {}'.format(out_file.name))
                shutil.copyfileobj(response.raw, out_file)
        del response

def isYes():
    judge_dict = dict(zip(['예', '아니오'], [True, False]))
    print('(예, 아니오)')
    while True:
        ans = input()
        if ans in judge_dict:
            return judge_dict[ans]

title = [
    "'||''''|  ..|'''.|   ..|''||      '||' '||    ||'  ..|'''.|       ..|'''.| '||''|.       |     '|| '||'  '|' '||'      '||''''|  '||''|.   ",
    " ||  .   .|'     '  .|'    ||      ||   |||  |||  .|'     '     .|'     '   ||   ||     |||     '|. '|.  .'   ||        ||  .     ||   ||  ",
    " ||''|   ||    .... ||      ||     ||   |'|..'||  ||    ....    ||          ||''|'     |  ||     ||  ||  |    ||        ||''|     ||''|'   ",
    " ||      '|.    ||  '|.     ||     ||   | '|' ||  '|.    ||     '|.      .  ||   |.   .''''|.     ||| |||     ||        ||        ||   |.  ",
    ".||.      ''|...'|   ''|...|'     .||. .|. | .||.  ''|...'|      ''|....'  .||.  '|' .|.  .||.     |   |     .||.....| .||.....| .||.  '|' "
]
llength=len(title[0])
print('┌' + ('─'*llength) + '┐')
for line in title:
    print('│' + line + '│')
print('└' + ('─'*llength) + '┘')
print('='*(llength+2))
print('이미지 크롤링을 시작하시겠습니까?\n'
      '이미지는 헝그리앱에서 크롤링해오며 이용상에 일어나는 문제점에 대해서 제작자는 책임지지 않습니다.')
print('='*(llength+2))
if isYes():
    imgpath = fpath + '/all_data/'
    crpath = imgpath + 'cr/'
    if not os.path.exists(imgpath):
        os.mkdir(imgpath)
    srvnCrawl = False
    crCrawl = False
    print('서번트를 크롤링합니까?')
    srvnCrawl = isYes()
    print('예장을 크롤링합니까?')
    crCrawl = isYes()
    if srvnCrawl:
        minvalue = 0
        print('서번트 크롤링을 시작합니다.')
        print('='*(llength+2))
        while not minvalue > 0:
            print('최소 id를 설정해주세요. (기본값: 1)')
            minvalue = input()
            if minvalue == '': minvalue = 1
            else: minvalue = int(minvalue)
        minvalue = int(minvalue)
        maxvalue = 0
        while not (maxvalue > 0 and maxvalue > minvalue):
            print('최대 id를 설정해주세요. (기본값: 500)')
            maxvalue = input()
            if maxvalue == '': maxvalue = 500
            else: maxvalue = int(maxvalue)
        maxvalue = int(maxvalue)
        crawl_servimg(minvalue, maxvalue+1)
    if crCrawl:
        minvalue = 0
        print('개념예장 크롤링을 시작합니다.')
        if not os.path.exists(crpath):
            os.mkdir(crpath)
        print('=' * (llength + 2))
        while not minvalue > 0:
            print('최소 id를 설정해주세요. (기본값: 1)')
            minvalue = input()
            if minvalue == '': minvalue = 1
            else: minvalue = int(minvalue)
        minvalue = int(minvalue)
        maxvalue = 0
        while not (maxvalue > 0 and maxvalue > minvalue):
            print('최대 id를 설정해주세요. (기본값: 2000)')
            maxvalue = input()
            if maxvalue == '': maxvalue = 2000
            else : maxvalue = int(maxvalue)
        maxvalue = int(maxvalue)
        crawl_craftimg(minvalue, maxvalue+1)
    print('크롤링이 끝났습니다. 프로그램을 종료합니다.')
    print('Press enter to exit')
    input()
    exit()
else:
    exit()