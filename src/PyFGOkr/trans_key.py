import os
fpath = os.path.dirname(__file__) + '/'
import json

# # # 첫 데이터(나무위키 목차 긁어서 제작) 만들 때 이용
# with open((fpath + 'raw_kr_item.txt').replace('\\', '/'), 'r', encoding='utf8') as f:
#     origin = f.readlines()
#     after = []
#     for line in origin:
#         parsingStart = True
#         parsingIndex = []
#         for idx in range(len(line)):
#             if line[idx] == ' ' and parsingStart:
#                 parsingStart = False
#                 parsingIndex.append(idx+1)
#             if line[idx] == '(':
#                 parsingIndex.append(idx)
#                 break
#             if idx == len(line) - 1:
#                 parsingIndex.append(idx + 1)
#         print(parsingIndex)
#         after.append(line[parsingIndex[0]:parsingIndex[1]].replace('\n', ''))
# with open((fpath + 'kr_item.txt').replace('\\', '/'), 'w', encoding='utf8') as f:
#     isFirst = True
#     for line in after:
#         if isFirst:
#             isFirst = False
#         else:
#             f.write('\n')
#         f.write(line)
# # #
def make_item_json(option='item'):
    if option=='item':
        with open((fpath + 'hangulitem.txt').replace('\\', '/'), 'r', encoding='utf8') as f:
            key = []
            lines = f.readlines()
            for line in lines:
                key.append(line.replace('\n', ''))
        with open((fpath + 'raw_kr2eng_item.txt').replace('\\', '/'), 'r', encoding='utf8') as f:
            value = []
            lines = f.readlines()
            for line in lines:
                value.append(line.replace('\n', ''))
        resjson = dict(zip(key,value))
        with open((fpath + 'kr2eng_item.json').replace('\\', '/'), 'w', encoding='utf8') as f:
            json.dump(resjson, f, ensure_ascii=False, indent=4)

def make_raw_json(option='all'):
    if option=='all':
        make_raw_json('quest')
        make_raw_json('area')
        make_raw_json('item')
    elif option=='quest':
        with open((fpath + 'raw_eng2kr_quest.txt').replace('\\', '/'), 'r', encoding='utf8') as f:
            lines = f.readlines()
            questlist = []
            for line in lines:
                questlist.append(line.replace('\n', ''))
        rawdict = dict(zip(questlist, [' ' for x in range(len(questlist))]))
        with open((fpath + 'raw_eng2kr_quest.json').replace('\\', '/'), 'w', encoding='utf8') as f:
            json.dump(rawdict, f, ensure_ascii=False, indent=4)
    elif option=='item':
        with open((fpath + 'raw_kr2eng_item.txt').replace('\\', '/'), 'r', encoding='utf8') as f:
            lines = f.readlines()
            itemlist = []
            for line in lines:
                itemlist.append(line.replace('\n', ''))
        rawdict = dict(zip(itemlist, [' ' for x in range(len(itemlist))]))
        with open((fpath + 'raw_kr2eng_item.json').replace('\\', '/'), 'w', encoding='utf8') as f:
            json.dump(rawdict, f, ensure_ascii=False, indent=4)
    elif option == 'area':
        with open((fpath + 'raw_eng2kr_area.txt').replace('\\', '/'), 'r', encoding='utf8') as f:
            lines = f.readlines()
            arealist = []
            for line in lines:
                arealist.append(line.replace('\n', ''))
        rawdict = dict(zip(arealist, [' ' for x in range(len(arealist))]))
        with open((fpath + 'raw_eng2kr_area.json').replace('\\', '/'), 'w', encoding='utf8') as f:
            json.dump(rawdict, f, ensure_ascii=False, indent=4)
    else: return False

def make_manual_eng2kr_quest():
    with open((fpath + 'raw_eng2kr_quest.txt').replace('\\', '/'), 'r', encoding='utf8') as f:
        raw = f.readlines()
    with open((fpath + 'eng2kr_quest.json').replace('\\', '/'), 'r', encoding='utf8') as f:
        obdata = json.load(f)
    notlist = []
    for key in raw:
        key = key.lower()
        try:
            obdata[key.replace('\n', '')]
        except:
            notlist.append(key.replace('\n', ''))
    try:
        with open((fpath + 'man_eng2kr_quest.json').replace('\\', '/'), 'r', encoding='utf8') as f:
            data = json.load(f)
            print('json loaded')
            for key in notlist:
                try:
                    data[key]
                    try:
                        if conv_key(key):
                            data.update({key: conv_key(key)})
                            print(f'filled data: {key}')
                        else:
                            print(f'key exist: {key}')
                    except:
                        print(f'key exist: {key}')
                except:
                    print(f'key added: {key}')
                    data.update({ key : '' })
        with open((fpath + 'man_eng2kr_quest.json').replace('\\', '/'), 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        with open((fpath + 'man_eng2kr_quest.json').replace('\\', '/'), 'w', encoding='utf8') as f:
            resdic = dict(zip(notlist, ['' for x in range(len(notlist))]))
            for key in notlist:
                try:
                    resdic.update({key: conv_key(key)})
                    print(f'added data: {key}')
                except:
                    0
            json.dump(resdic, f, ensure_ascii=False, indent=4)

def conv_key(key):
    convtkey = {
        'mon' : '월요일 궁의 수련장- ',
        'tue' : '화요일 창의 수련장- ',
        'wed' : '수요일 광의 수련장- ',
        'thu' : '목요일 기의 수련장- ',
        'fri' : '금요일 술의 수련장- ',
        'sat' : '토요일 살의 수련장- ',
        'sun' : '일요일 검의 수련장- '
    }
    convtdiff = {
        'nov' : '초급',
        'int' : '중급',
        'adv' : '상급',
        'exp' : '초월급'
    }
    try:
        reskey = ''
        reskey += convtkey[key[:3]]
        reskey += convtdiff[key[-3:]]
        return reskey
    except:
        return ''
'''
검색시엔 한글 -> 영어로 키값을 받지만
지역, 퀘스트 해석은 '영어' 입력 -> '한글'로 return 하는 식으로 짜야한다.

quest 직접 타이핑하기엔 너무 반복적임
1. grandorder wiki에서 지역 이름(영문)을 { '영문' : '일본어' } 형태로받아옴
-> 2. 나무위키 프리퀘스트 페이지에서 적절히 파싱해서 { '일본어' : '한글' } 형태로 dict을 만듬
-> 3. { '영어' : '한글' } 자료형을 만들고 raw.json을 update 해보고 이상 여부 확인하면 종료
'''
# make_raw_json()
# make_item_json()
# make_manual_eng2kr_quest()