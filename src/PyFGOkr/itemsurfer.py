import os
fpath = os.path.dirname(__file__) + '/'
import string
import gspread
from collections import deque
from oauth2client.service_account import ServiceAccountCredentials
from PyFGOkr import trans_key
import json

apijson = 'scret_credentials.json'

tkey = list(string.ascii_uppercase) + list(['A' + x for x in list(string.ascii_uppercase)])
tvalue = list(range(1,len(tkey)+1))
conv_col = dict(zip(tkey, tvalue))

_convitem = {}
_convlocation = {}
try:
    with open(fpath + 'kr2eng_item.json', 'r', encoding='utf8') as f:
        _convitem.update(json.load(f))
except:
    print('모듈과 같은 폴더에 kr2eng_item.json 파일이 존재하지 않습니다.')

try:
    with open(fpath + 'eng2kr_area.json', 'r', encoding='utf8') as f:
        _convlocation.update(json.load(f))
except:
    print('모듈과 같은 폴더에 eng2kr_area.json 파일이 존재하지 않습니다.')

try:
    with open(fpath + 'eng2kr_quest.json', 'r', encoding='utf8') as f:
        _convlocation.update(json.load(f))
except:
    print('모듈과 같은 폴더에 eng2kr_quest.json 파일이 존재하지 않습니다.')

try:
    with open(fpath + 'man_eng2kr_quest.json', 'r', encoding='utf8') as f:
        _convlocation.update(json.load(f))
except:
    print('모듈과 같은 폴더에 man_eng2kr_quest.json 파일이 존재하지 않습니다.')


def debug(data : dict):
    print(data['item'])
    print(data['effRank'])
    print(data['area'])
    print(data['quest'])
    print(data['takeAp'])
    print(data['apPerDrop'])
    print(data['Dropchance'])

def col2deq(sheet: object, alphabet: str):
    return deque(sheet.col_values(conv_col[alphabet]))


def rmvBlank(deque: deque):
    for _ in range(4):
        deque.popleft()

class Pickup_data:
    def __init__(self, datajson=False, apijson=apijson ):
        if datajson:
            try:
                with open(fpath + 'fgo_item.json', encoding='utf8') as f:
                    self.data = json.load(f)
                    return
            except:
                print('이용 가능한 파일이 아닙니다.')
        self.make_json()

        '''
        1. item 이름에 대응되게 각 밸류들을 dict 자료형으로 저장(클래스의 목표)
        2. 지정된 동작을 수행하되 구분 인덱스를 만나면 지나침
        3. 공백을 만나면 역시 지나침
        4. 두 인덱스를 합침(pridata[0] pridata[1]
        5. 합친 데이터를 기반으로 자료형을 만들어줌
        2-1. { 'name' : { 'rank' : [ { 'area' : '지역', 'quest' : '퀘스트', 'takeap' : '21', 'apPerDrop' : '20.1'
                                        , 'dropchance' : '0.263' }, {} ] } }
        3. dict 자료형 완성!
        '''

    def make_json(self):
        print("아이템 검색을 위한 json 파일 생성 시작")
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(fpath + apijson, scope)
        self.gc = gspread.authorize(credentials)
        self.sht1 = self.gc.open_by_url(
            'https://docs.google.com/spreadsheets/d/1_SlTjrVRTgHgfS7sRqx4CeJMqlz687HdSlYqiW-JvQA/').sheet1
        print("일본 페이트 그랜드 오더 데이터 시트에 접속 성공")
        pridata = {'item': [col2deq(self.sht1, 'C'), col2deq(self.sht1, 'S')],
                   'effRank': [col2deq(self.sht1, 'D'), col2deq(self.sht1, 'T')],
                   'area': [col2deq(self.sht1, 'F'), col2deq(self.sht1, 'V')],
                   'quest': [col2deq(self.sht1, 'G'), col2deq(self.sht1, 'W')],
                   'takeAp': [col2deq(self.sht1, 'H'), col2deq(self.sht1, 'X')],
                   'apPerDrop': [col2deq(self.sht1, 'J'), col2deq(self.sht1, 'Z')],
                   'Dropchance': [col2deq(self.sht1, 'L'), col2deq(self.sht1, 'AB')]
                   }
        print("원시 데이터 생성 완료")
        self._rmvblank(pridata)
        categoryidxlist = []
        for i in range(2):
            categoryidxlist.append(self._get_seperator_idx(pridata['effRank'][i], 'No.'))
        print("원시 데이터를 dict 자료형으로 변환 시작")
        self.data = self._data_analyze(pridata, categoryidxlist)
        print("변환 완료")
        self.resdata = { 'jp' : self.data }
        print('일본 페이트 그랜드 오더 정보 작성 완료')
        del self.data
        self.sht1 = self.gc.open_by_url(
            'https://docs.google.com/spreadsheets/d/1_SlTjrVRTgHgfS7sRqx4CeJMqlz687HdSlYqiW-JvQA/').worksheet('Best 5 AP/Drop (NA)')
        print("한국 페이트 그랜드 오더 데이터 시트에 접속 성공")
        pridata = {'item': [col2deq(self.sht1, 'C'), col2deq(self.sht1, 'S')],
                   'effRank': [col2deq(self.sht1, 'D'), col2deq(self.sht1, 'T')],
                   'area': [col2deq(self.sht1, 'F'), col2deq(self.sht1, 'V')],
                   'quest': [col2deq(self.sht1, 'G'), col2deq(self.sht1, 'W')],
                   'takeAp': [col2deq(self.sht1, 'H'), col2deq(self.sht1, 'X')],
                   'apPerDrop': [col2deq(self.sht1, 'J'), col2deq(self.sht1, 'Z')],
                   'Dropchance': [col2deq(self.sht1, 'L'), col2deq(self.sht1, 'AB')]
                   }
        print("원시 데이터 생성 완료")
        self._rmvblank(pridata)
        categoryidxlist = []
        for i in range(2):
            categoryidxlist.append(self._get_seperator_idx(pridata['effRank'][i], 'No.'))
        print("원시 데이터를 dict 자료형으로 변환 시작")
        self.data = self._data_analyze(pridata, categoryidxlist)
        print("변환 완료")
        self.resdata.update({'kr' : self.data})
        print('한국 페이트 그랜드 오더 정보 작성 완료')
        del self.data
        self.data = self.resdata
        # 한국 페이트 그랜드 오버 정보 작성 완료
        with open(fpath + 'fgo_item.json', 'w', encoding='utf8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
            print('fgo_item.json 생성 완료')

    def _rmvblank(self, data : dict):
        for key in data:
            for idx in range(2):
                rmvBlank(data[key][idx])

    def _data_analyze(self, data : dict, category : list):
        resdict = {}
        for idx in range(2):
            ddict = {}
            item = data['item'][idx]
            area = data['area'][idx]
            quest = data['quest'][idx]
            takeap = data['takeAp'][idx]
            ap_per_drop = data['apPerDrop'][idx]
            dropchance = data['Dropchance'][idx]
            categoryidxlist = category[idx]
            for ele in range(len(item)):
                if ele in categoryidxlist:
                    continue
                if item[ele]:
                    ranklist = []
                    for otele in range(ele, ele+5):
                        if area[otele]:
                            ranklist.append({ 'area' : area[otele], 'quest' : quest[otele], 'takeap' : takeap[otele],
                                              'ap_per_drop' : ap_per_drop[otele], 'dropchance' : f'{dropchance[otele]}%'})
                        else:
                            break
                    ddict.update({item[ele] : { 'rank' : ranklist}})
            resdict.update(ddict)
        return resdict

    def _get_seperator_idx(self, seplist: list, seperator : str):
        category_idxlist = []
        for idx in range(len(seplist)):
            if seplist[idx] == seperator:
                category_idxlist.append(idx)
        return category_idxlist

    def make_keyfile(self, option='all', recur_data=[]):
        if recur_data:
            key_data = recur_data[0]
            area_data = recur_data[1]
            quest_data = recur_data[2]
        else:
            area_data = []
            quest_data = []
            key_data = []
            data = self.data['jp']
            for key in data:
                key_data.append(key)
                ele_data = data[key]
                rank = ele_data['rank']
                for sub_data in rank:
                    area_data.append(sub_data['area'])
                    quest_data.append(sub_data['quest'])
            recur_data = [key_data, area_data, quest_data]
        if option == 'item':
            with open(fpath + 'raw_kr2eng_item.txt', 'w', encoding='utf8') as fp:
                raw_item = fp
                isFirst = True
                for line in key_data:
                    if isFirst:
                        isFirst = False
                    else:
                        fp.write('\n')
                    fp.write(line)
            trans_key.make_raw_json('item')
            os.remove(raw_item.name)
        elif option == 'area':
            with open(fpath + 'raw_eng2kr_area.txt', 'w', encoding='utf8') as f:
                raw_area = f
                isFirst = True
                for line in area_data:
                    if isFirst:
                        isFirst = False
                    else:
                        f.write('\n')
                    f.write(line)
            trans_key.make_raw_json('area')
            os.remove(raw_area.name)
        elif option == 'quest':
            with open(fpath + 'raw_eng2kr_quest.txt', 'w', encoding='utf8') as f:
                raw_quest = f
                isFirst = True
                for line in quest_data:
                    if isFirst:
                        isFirst = False
                    else:
                        f.write('\n')
                    f.write(line)
            trans_key.make_raw_json('quest')
            os.remove(raw_quest.name)
        elif option == 'manquest':
            with open(fpath + 'raw_eng2kr_quest.txt', 'w', encoding='utf8') as f:
                raw_quest = f
                isFirst = True
                for line in quest_data:
                    if isFirst:
                        isFirst = False
                    else:
                        f.write('\n')
                    f.write(line)
            trans_key.make_manual_eng2kr_quest()
            os.remove(raw_quest.name)
        elif option == 'all':
            self.make_keyfile('item', recur_data)
            self.make_keyfile('area', recur_data)
            self.make_keyfile('quest', recur_data)

    def search_item(self, name, option='jp'):
        if option == 'jp': item_data = self.data['jp']
        if option == 'kr': item_data = self.data['kr']
        sub_data = item_data[_convitem[name]]
        ranklist = sub_data['rank']
        convlist = []
        for d in ranklist:
            try:
                area = _convlocation[d['area']]
            except:
                area = d['area']
            try:
                quest = _convlocation[d['quest'].lower()]
            except:
                quest = d['quest']
            ele_dict = d.copy()
            ele_dict.update({'area': area, 'quest': quest})
            convlist.append(ele_dict)
        return convlist

'''
검색시엔 한글 -> 영어로 키값을 받지만
지역, 퀘스트 해석은 '영어' 입력 -> '한글'로 return 하는 식으로 짜야한다.
'''
# pd = Pickup_data(apijson, True)
# print(pd.search_item('지혜의 스카라베'))
# pd.make_keyfile()