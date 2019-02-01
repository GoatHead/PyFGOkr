from bs4 import BeautifulSoup
import requests
from webhangulquery import *
import os
import json
fdpath = os.path.dirname(__file__) + '/'
arealist = []
chapterlist = ['1부', '1.5부', '2부']
#'gowiki': https://grandorder.wiki/
#'fandom': https://fategrandorder.fandom.com/

def eng2kr_quest_make():
    global arealist
    global resdict
    # url = 'https://grandorder.wiki/Template:FreeQuestLinks'
    # r = requests.get(url)
    # html = r.text
    # soup = BeautifulSoup(html, 'html.parser')
    # p = soup.select('p > a')
    # for i in p:
    #     arealist.append(i.contents[0])
    url = 'https://fategrandorder.fandom.com/wiki/Quests'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.select('ul > li > a')
    for i in p:
        res = i.contents[0]
        if 'Free Quests: ' in res: arealist.append(res[13:].replace('\n', ''))
    isPassShimosa = False
    eng2jpdict = {}
    for area in arealist:
        if area == 'Shimosa':
            isPassShimosa = True
        if isPassShimosa:
            eng2jpdict.update(parseEngPage(area, "fandom"))
        else:
            eng2jpdict.update(parseEngPage(area))
    for key in eng2jpdict:
        print(f'key: {key}' + 'to_jp:' f' {eng2jpdict[key]}')
    jp2krdict = {}
    for chapter in chapterlist:
        jp2krdict.update(parseKrPage(chapter))
    resdict = {}
    errorlist = []
    for key in eng2jpdict:
        try:
            print(f'Success: {key} / key2jp> {eng2jpdict[key] } jp2kr> {jp2krdict[ eng2jpdict[key] ]}')
            resdict.update({key: jp2krdict[eng2jpdict[key]]})
        except KeyError as e:
            errorlist.append(key)
    resdict = update_manually(resdict, errorlist)
    with open(fdpath + 'eng2kr_quest.json', 'w', encoding='utf8') as f:
        json.dump(resdict, f, ensure_ascii=False, indent=4)

def wiki_quest_page(area, option='gowiki'):
    if option=='gowiki':
        url = 'https://grandorder.wiki/Quests/'
        res = f'{url}{area}/Free_Quests'
        return res
    elif option=='kr':
        url = 'https://namu.wiki/w/Fate/Grand%20Order/'
        res = f'{url}{queryconvertforweb("프리 퀘스트")}/{area}'
        return res
    elif option=='fandom':
        if area == '':
            area = 'S_I_N'
        url = 'https://fategrandorder.fandom.com/wiki/Free_Quests:_'
        res = f'{url}{area}'
        return res
    else:
        return False

def parseEngPage(area, option='gowiki'):
    if option == 'gowiki':
        soup = make_soup(wiki_quest_page(area))
        p = soup.select('.toctext')
        jplist = []
        englist = make_list(p)
        englist.pop(0)
        s = soup.find_all('td', {'style': 'font-weight:bold;'})
        for i in s:
            ele = i.contents[-1].replace('\n', '')
            if ele in jplist:
                continue
            jplist.append(i.contents[-1].replace('\n', ''))
        resdict = dict(zip(englist, jplist))
        return resdict
    elif option == 'fandom':
        soup = make_soup(wiki_quest_page(area, 'fandom'))
        p = soup.select('.mw-headline')
        jplist = []
        englist = make_list(p)
        s = soup.find_all('td', {'style': 'width: 25%; height: 50px; font-size: 130%;'})
        for i in s:
            ele = i.contents[-1].replace('\n', '')
            if ele in jplist:
                continue
            jplist.append(i.contents[-1].replace('\n', ''))
        resdict = dict(zip(englist, jplist))
        return resdict

def parseKrPage(chapter):
    soup = make_soup(wiki_quest_page(chapter, 'kr'))
    p = soup.select('p > div > div > div > span')
    key = []
    value = []
    for i in p:
        jpidx = []
        raw = i.contents[1]
        for idx in range(len(raw)):
            if raw[idx] == '(':
                jpidx.append(idx + 1)
            elif raw[idx] == ')':
                jpidx.append(idx)
                break
        key.append(raw[ jpidx[0] : jpidx[1] ].replace('\n', ''))
        value.append(raw[ 2 : jpidx[0] - 1].strip())
    rdict = dict(zip(key, value))
    return rdict

def make_soup(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def debug(soup, idx=0):
    for i in soup:
        print(i.contents[idx])

def make_list(soup):
    reslist = []
    for i in soup:
        reslist.append(i.contents[0].lower().strip())
    return reslist

def error_update(resdict, key, value, errorlist: list):
    key = key.lower()
    if key in errorlist:
        errorlist.remove(key)
    resdict.update({key : value})
    return errorlist

def update_manually(resdict, errorlist): # 에러난 부분 수작업
    update_key_value = {
        'Mobile Coordinate No.0' : '변동좌표점0호',
        'West Village Ruins': '서쪽 마을 옛터',
        'Party Hall': '파티 회장',
        'Barrel Tower': '배럴 타워',
        'Quiet Forest': '정적한 숲',
        'Anchor Point': '앵커 포인트',
        'Icicles Grotto': '풍혈빙굴',
        'Yaga Vyazma': '야가 뱌지마'
    }
    for key in update_key_value:
        errorlist = error_update(resdict, key, update_key_value[key], errorlist)
    for i in errorlist:
        print(f'error added: {i}')
    return resdict

eng2kr_quest_make()