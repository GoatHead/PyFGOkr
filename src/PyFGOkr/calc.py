import math
from datetime import datetime


def parse_percent(s):
    s = s.rstrip("%")
    s = s.replace("%", "")
    s = str(eval(s))
    if "." not in s:
        return int(s) / 100
    if s.startswith("-"):
        return -parse_percent(s.lstrip("-"))
    i, j = s.split(".", 2)
    i = int(i)
    s = "0.00" + j if i == 0 else str(i / 100) + j
    return float(s)

class Np_dmg_calc:
    def fgo_np_dmg(self, isSolo, isNpQuest, card, npLvl):
        res = 1.0
        if isSolo == True:  # 대인
            if isNpQuest == True:  # 보퀘
                if card == 'B':  # 카드
                    if npLvl == 1:  # 보렙
                        res = 8.0
                    elif npLvl == 2:  # 보렙
                        res = 10.0
                    elif npLvl == 3:  # 보렙
                        res = 11.0
                    elif npLvl == 4:  # 보렙
                        res = 11.5
                    elif npLvl == 5:  # 보렙
                        res = 12.0
                if card == 'A':  # 카드
                    if npLvl == 1:  # 보렙
                        res = 12.0
                    elif npLvl == 2:  # 보렙
                        res = 15.0
                    elif npLvl == 3:  # 보렙
                        res = 16.5
                    elif npLvl == 4:  # 보렙
                        res = 17.25
                    elif npLvl == 5:  # 보렙
                        res = 18.0
                if card == 'Q':  # 카드
                    if npLvl == 1:  # 보렙
                        res = 16.0
                    elif npLvl == 2:  # 보렙
                        res = 20.0
                    elif npLvl == 3:  # 보렙
                        res = 22.0
                    elif npLvl == 4:  # 보렙
                        res = 23.0
                    elif npLvl == 5:  # 보렙
                        res = 24.0
            if isNpQuest == False:  # 노보퀘
                if card == 'B':  # 카드
                    if npLvl == 1:  # 보렙
                        res = 6.0
                    elif npLvl == 2:  # 보렙
                        res = 8.0
                    elif npLvl == 3:  # 보렙
                        res = 9.0
                    elif npLvl == 4:  # 보렙
                        res = 9.5
                    elif npLvl == 5:  # 보렙
                        res = 10.0
                if card == 'A':  # 카드
                    if npLvl == 1:  # 보렙
                        res = 9.0
                    elif npLvl == 2:  # 보렙
                        res = 12.0
                    elif npLvl == 3:  # 보렙
                        res = 13.5
                    elif npLvl == 4:  # 보렙
                        res = 14.25
                    elif npLvl == 5:  # 보렙
                        res = 15.0
                if card == 'Q':  # 카드
                    if npLvl == 1:  # 보렙
                        res = 12.0
                    elif npLvl == 2:  # 보렙
                        res = 16.0
                    elif npLvl == 3:  # 보렙
                        res = 18.0
                    elif npLvl == 4:  # 보렙
                        res = 19.0
                    elif npLvl == 5:  # 보렙
                        res = 20.0
        elif isSolo == False:  # 대군
            if isNpQuest == True:  # 보퀘
                if card == 'B':  # 카드
                    if npLvl == 1:  # 보렙
                        res = 4.0
                    elif npLvl == 2:  # 보렙
                        res = 5.0
                    elif npLvl == 3:  # 보렙
                        res = 5.5
                    elif npLvl == 4:  # 보렙
                        res = 5.75
                    elif npLvl == 5:  # 보렙
                        res = 6.0
                if card == 'A':  # 카드
                    if npLvl == 1:  # 보렙
                        res = 6.0
                    elif npLvl == 2:  # 보렙
                        res = 7.5
                    elif npLvl == 3:  # 보렙
                        res = 8.25
                    elif npLvl == 4:  # 보렙
                        res = 8.625
                    elif npLvl == 5:  # 보렙
                        res = 9.0
                if card == 'Q':  # 카드
                    if npLvl == 1:  # 보렙
                        res = 8.0
                    elif npLvl == 2:  # 보렙
                        res = 10.0
                    elif npLvl == 3:  # 보렙
                        res = 11.0
                    elif npLvl == 4:  # 보렙
                        res = 11.5
                    elif npLvl == 5:  # 보렙
                        res = 12.0
            if isNpQuest == False:  # 노보퀘
                if card == 'B':  # 카드
                    if npLvl == 1:  # 보렙
                        res = 3.0
                    elif npLvl == 2:  # 보렙
                        res = 4.0
                    elif npLvl == 3:  # 보렙
                        res = 4.5
                    elif npLvl == 4:  # 보렙
                        res = 4.75
                    elif npLvl == 5:  # 보렙
                        res = 5.0
                if card == 'A':  # 카드
                    if npLvl == 1:  # 보렙
                        res = 4.5
                    elif npLvl == 2:  # 보렙
                        res = 6
                    elif npLvl == 3:  # 보렙
                        res = 6.75
                    elif npLvl == 4:  # 보렙
                        res = 7.13
                    elif npLvl == 5:  # 보렙
                        res = 7.5
                if card == 'Q':  # 카드
                    if npLvl == 1:  # 보렙
                        res = 6.0
                    elif npLvl == 2:  # 보렙
                        res = 8.0
                    elif npLvl == 3:  # 보렙
                        res = 9.0
                    elif npLvl == 4:  # 보렙
                        res = 9.5
                    elif npLvl == 5:  # 보렙
                        res = 10.0
        return res
    def fgo_class_coeff(self, className):
        res = 1.0
        if className in ['세이버', '라이더', '실더', '문캔서', '얼터에고', '얼터 에고', '포리너']:
            res = 1.0
        elif className in ['버서커', '룰러', '어벤저']:
            res = 1.1
        elif className in ['캐스터', '어새신']:
            res = 0.9
        elif className == '아처':
            res = 0.95
        elif className == '랜서':
            res = 1.05
        return res
    def calc(self, input_str):
        parseStr = []
        parseStr = input_str.split(' ')
        atk, cardValue, npValue, className, classValue, berserkAdv, = 0, 0, 0, 0, 0, 0
        card = 'B'
        hiddenValue, randValue, npLvl = 1, 1, 1
        atkBuff, colorBuff, npBuff, extraBuff, npExtraBuff, bonusDmg, npCustom, advJudger = 1, 1, 0, 0, 1, 0, 0, 0
        isSolo = False
        isNpQuest = False
        for str in parseStr:
            if '공:' == str[0:2]:
                atk = eval(str[2:])
                continue
            elif '클래스:' in str:
                className = str[4:]
                continue
            elif '난수:' in str:
                judger = str[3:]
                if judger == '최대':
                    randValue = 1.1
                elif judger == '최소':
                    randValue = 0.9
                else:
                    randValue = 1.0
                continue
            elif '히든:' in str:
                judger = str[3:]
                if judger == '유리':
                    hiddenValue = 1.1
                elif judger == '불리':
                    hiddenValue = 0.9
                else:
                    hiddenValue = 1.0
                continue
            elif '공뻥:' in str:
                buffValue = parse_percent(str[3:])
                atkBuff = 1.0 + buffValue
            elif '색뻥:' in str:
                buffValue = parse_percent(str[3:])
                colorBuff = 1.0 + buffValue
            elif '보뻥:' in str:
                buffValue = parse_percent(str[3:])
                npBuff = buffValue
            elif '특공:' == str[0:3]:
                buffValue = parse_percent(str[3:])
                extraBuff = buffValue
            elif '보구특공:' in str:
                buffValue = parse_percent(str[5:])
                npExtraBuff = 1.0 + buffValue
            elif str in ['버스트', '버', 'b', 'B']:
                card = 'B'
                continue
            elif str in ['아츠', '아', 'a', 'A']:
                card = 'A'
                continue
            elif str in ['퀵', 'q', 'Q']:
                card = 'Q'
                continue
            elif str == '대인':
                isSolo = True
                continue
            elif str == '대군':
                isSolo = False
                continue
            elif str == '보퀘':
                isNpQuest = True
                continue
            elif '보렙:' in str:
                npLvl = int(str[3:])
                if npLvl >= 5:
                    npLvl = 5
                elif npLvl <= 1:
                    npLvl = 1
                continue
            elif '추가데미지:' in str:
                res = int(str[6:])
                bonusDmg = res
                continue
            elif '배율:' in str:
                mulValue = parse_percent(str[3:])
                npCustom = mulValue
            elif str == '상성':
                advJudger = '상성'
            elif str == '역상성':
                advJudger = '역상성'

        npValue = self.fgo_np_dmg(isSolo, isNpQuest, card, npLvl)  # 보구 배율 설정
        if npCustom > 0:
            npValue = npCustom
        classValue = self.fgo_class_coeff(className)
        berserkAdv = 1.0
        if advJudger == '상성':
            berserkAdv = 2.0
        if className in ['얼터에고', '얼터 에고', '버서커']:
            berserkAdv = 1.5
        if advJudger == '역상성':
            berserkAdv = 0.5
        if card == 'B':
            cardValue = 1.5
        elif card == 'A':
            cardValue = 1
        elif card == 'Q':
            cardValue = 0.8
        # atk = atk + 1786
        NP = atk * 0.23 * cardValue * npValue * classValue
        NP = NP * berserkAdv * hiddenValue * randValue
        NP = NP * atkBuff * colorBuff
        NP = NP * (1 + npBuff + extraBuff) * npExtraBuff + bonusDmg
        return NP
class Np_gain_calc:
    def np_enemy_serv(self, className):
        res = 1
        if className in ['캐스터', '스켈톤', '좀비', '용아병', '문캔서']:
            res = 1.2
        elif className in ['라이더']:
            res = 1.1
        elif className in ['용아병(어새신)', '고스트']:
            res = 1.08
        elif className in ['세이버', '아처', '랜서', '마신주', '어벤저', '룰러', '얼터 에고', '얼터에고', '비스트']:
            res = 1
        elif className in ['해적좀비(버서커)']:
            res = 0.96
        elif className in ['어새신']:
            res = 0.9
        elif className in ['버서커']:
            res = 0.8
        return res

    def card_convert(self, str):
        card = 0
        if str in ['버스트', '버', 'b', 'B']:
            card = 'B'
        elif str in ['아츠', '아', 'a', 'A']:
            card = 'A'
        elif str in ['퀵', 'q', 'Q', '엑스트라']:
            card = 'Q'
        else:
            card = 'E'
        return card

    def card_np_calc(self, card, attack_order):
        res = 0
        order = 1
        if (attack_order == 1):
            order = 1
        elif (attack_order == 2):
            order = 1.5
        elif (attack_order == 3):
            order = 2
        if (card == 'B'):
            return 0
        elif (card == 'A'):
            res = 3
        elif (card == 'Q'):
            res = 1
        return res * order

    def calc(self, input_str):
        parseStr = []
        basic_atk_gain = '0.86%'
        card = 'A'
        first_cd_bonus, card_np = 0, 0
        card_buff, card_resist = 0, 0
        enemy_class = 1
        np_buff, critical, overkill = 0, 1, 1
        attack_list = [0, 0, 0, 0]
        attack_num = 1
        attack_order = 1
        className = 0
        parseStr = input_str.split(' ')
        for str in parseStr:
            if '수급:' == str[0:3]:
                basic_atk_gain = parse_percent(str[3:])
                continue
            if '타수:' == str[0:3]:
                attack_num = eval(str[3:])
                continue
            elif '순:' == str[0:2]:
                if (str[2:] == '보구' or str[2:] == '엑스트라'):
                    attack_order = 1
                    continue
                else:
                    attack_order = eval(str[2:])
                    if (attack_order >= 3):
                        attack_order = 3
                    elif (attack_order <= 1):
                        attack_order = 1
                    continue
            elif '적:' in str:
                className = str[2:]
                continue
            elif '색뻥:' in str:
                card_buff = parse_percent(str[3:])
                continue
            elif '색깎:' in str:
                card_resist = parse_percent(str[3:])
                continue
            elif '수급뻥:' in str:
                np_buff = parse_percent(str[4:])
                continue
            elif '카드:' in str:
                card = self.card_convert(str[3:])
                continue
            elif '크리티컬' in str:
                critical = 2
                continue
            elif '오버킬' in str:
                overkill = 1.5
                continue
            elif '첫수:' in str:
                definer = self.card_convert(str[3:])
                if definer == 'A':
                    first_cd_bonus = 1
                else:
                    first_cd_bonus = 0
                continue
        if card == 'E':
            return '올바른 카드를 입력해주세요.'
        enemy_class = self.np_enemy_serv(className)
        card_np = self.card_np_calc(card, attack_order)
        gain_np = basic_atk_gain * 100 * (card_np * (min(5, 1 + card_buff) - card_resist) + first_cd_bonus) * \
                  enemy_class * min(5, 1 + np_buff) * critical * \
                  overkill * attack_num
        return gain_np
class Exp_calc:
    req_exp = []

    def exp_gen(self, n):
        i = 0
        for i in range(n):
            yield i*100
            i+=1

    def __init__(self):
        p=0
        for x in range(2, 91):
            sum = 0
            for y in self.exp_gen(x):
                sum += y
            self.req_exp.append(sum)
        for x in range(10):
            p += 18000 + (400 * x)
            self.req_exp.append(self.req_exp[-1] + p)

    def serv_calc(self, templvl, oblvl):
        difflvl = oblvl - templvl
        templvl = templvl - 1
        need_exp = 0
        star4_exp = 27000
        star4_exp_b = 32400
        for idx in range(templvl, templvl+difflvl):
            need_exp += self.req_exp[idx]
        res1 = math.ceil(need_exp / star4_exp)
        res2 = math.ceil(need_exp / star4_exp_b)
        return [res1, res2]
## 계산기 생성
npDmgCalc = Np_dmg_calc()
npGainCalc = Np_gain_calc()
###
##
#
def fgo_req_exp(from_int, to_int):
    expc = Exp_calc()
    reslist = expc.serv_calc(from_int, to_int)
    return reslist

##fgo_np_calc 함수의 인자값 설명
#atk: 서번트의 공격력
#card: 'B', 'A', 'Q'. 각각 버스트, 아츠, 퀵
#issingle: False라면 대군보구, True라면 대인보구
#nplevel: 보구 레벨
#npupgrade: False는 보구퀘 X, True는 보구퀘
#sclass: 서번트의 클래스를 나타냄
#rand: 난수값. '최대'와 '최소' 옵션이 있음
#hidden: 히든상성. '불리'와 '유리' 옵션이 있음
#atkbuff: 공격 버프
#colorbuff: 색 버프(버,퀵,아)
#npbuff: 보구 데미지 버프
#satk: 특공 버프
#npsatk: 보구에 달린 특공 버프
#atkconst: 고정 데미지 증가 버프(ex: 공명 3스킬)
#advantage: 상성 여부. '상성'과 '역상성' 옵션이 존재
#times: 배율을 조정. '100%', '200%', '300%' 따위로 입력
def fgo_np_calc(atk=14323, card='B', issingle=False, nplevel=1, npupgrade=False, sclass='세이버',
                rand='', hidden='', atkbuff='0%', colorbuff='0%', npbuff='0%', satk='0%',
                npsatk='0%', atkconst='0', advantage='', times=''):
    input_str = ''
    input_str += '공:{} '.format(str(atk))
    input_str += '{} '.format(card)
    if issingle:
        input_str += '대인 '
    else:
        input_str += '대군 '
    input_str += '보렙:{} '.format(nplevel)
    if npupgrade:
        input_str += '보퀘 '
    input_str += '클래스:{} '.format(sclass)
    if rand:
        input_str += '난수:{} '.format(rand)
    if hidden:
        input_str += '히든:{} '.format(hidden)
    input_str += '공뻥:{} '.format(atkbuff)
    input_str += '색뻥:{} '.format(colorbuff)
    input_str += '보뻥:{} '.format(npbuff)
    input_str += '일반특공:{} '.format(satk)
    input_str += '보구특공:{} '.format(npsatk)
    input_str += '추가데미지:{} '.format(atkconst)
    if times:
        input_str += '배율:{} '.format(times)
    if advantage in ['상성', '역상성']:
        input_str += ' '.format(advantage)
    NP = npDmgCalc.calc(input_str)
    if (NP > 0):
        return(int(NP))
    else:
        return('인자값을 확인해주세요.')


#fgo_gain_np_calc 함수 인자 설명
#efficiency: 수급률
#hit: 타수
#card: 카드 (버스트 'B', 아츠  'A', 퀵 'Q')
#eclass: 적의 클래스
#firstcard: 첫수 카드. 아츠 'A', 퀵 'Q', 버스트 'B'
#order: 카드 타순. 엑스트라 어택 및 보구는 1
#colorbuff: 카드 색 버프
#gainbuff: 수급률 버프
#iscritical: True일 경우 크리티컬일 때 수급률을 반환
#isoverkill: True일 경우 오버킬일 때 수급률을 반환
def fgo_gain_np_calc(efficiency='0.86%', hit=2, card='A', eclass='세이버', firstcard='A',
                     order=1, colorbuff='0%', gainbuff='0%', iscritical=False, isoverkill=False):
    input_str = ''
    input_str += '수급:{} '.format(efficiency)
    input_str += '타수:{} '.format(str(hit))
    input_str += '카드:{} '.format(card)
    input_str += '적:{} '.format(eclass)
    input_str += '첫수:{} '.format(firstcard)
    input_str += '순:{} '.format(str(order))
    input_str += '색뻥:{} '.format(colorbuff)
    input_str += '수급뻥:{} '.format(gainbuff)
    if iscritical:
        input_str += '크리티컬 '
    if isoverkill:
        input_str += '오버킬 '
    gain_np = npGainCalc.calc(input_str)
    gain_np = math.ceil(gain_np)
    return gain_np

def fgo_ap_recover_calc(nowap, maxap):
    now = datetime.now()
    if nowap<0 or maxap<=nowap:
        return False
    else:
        hour = now.hour
        min =  now.minute
        day = 0
        chargeap = maxap - nowap
        chargemin = chargeap * 5
        chargehour = int(chargemin / 60)
        chargemin = int(chargemin % 60)
        hour = hour+chargehour
        min = min+chargemin
        if min >= 60:
            while min>=60:
                hour += 1
                min -= 60
        if hour >= 24:
            while hour>=24:
                day += 1
                hour -= 24
        return({'day': day, 'hour': hour, 'min': min})
# Discord용
# 입력예제 '1 80' (디스코드에서 입력된 문자열을 ['1', '80'] 리스트로 받아온다.)
def fgo_req_exp_out_discord(args):
    templvl = eval(args[0])
    oblvl = eval(args[1])
    expc = Exp_calc()
    reslist = expc.serv_calc(templvl, oblvl)
    rstr = '```css\n[Lv{0}에서 Lv{1}까지 필요한 종화 개수]\n4성 종화(일반): {2}개\n4성 종화(클래스 보너스): {3}개\n```'.format(templvl, oblvl, reslist[0],  reslist[1])
    return rstr


# 입력 예제
# '공:14323  버스트  대인|대군   보렙:1~5  보퀘  클래스:세이버  난수:최소|입력안함|최대  ' \
# '히든:불리|입력안함|유리  공뻥:30%  색뻥:20%  보뻥:20% 일반특공:10%  보구특공:50%  추가데미지:100  배율:600%  상성|역상성 '
def fgo_np_calc_discord(input_str):
    NP = npDmgCalc.calc(input_str)
    if (NP > 0):
        return(int(NP))
    else:
        return('인자값을 확인해주세요.')
#보딜 계산


# 입력 예제 : '수급:0.87% 색뻥:44% 수급뻥:25% 적:라이더 타수:6 카드:아츠 순:3 첫수:아츠 크리티컬 오버킬'
def fgo_gain_np_calc_discord(input_str):
    gain_np = npGainCalc.calc(input_str)
    gain_np = math.ceil(gain_np)
    return 'NP수급량: {}%'.format(gain_np)
#Discord 종료


#보딜 체크
#
# print(fgo_gain_np_calc_discord('수급:0.56% 적:랜서 첫수:아츠 카드:아츠 순:2 타수:3'))
# print(fgo_gain_np_calc_discord('수급:0.87% 색뻥:44% 수급뻥:25% 적:라이더 타수:6 카드:아츠 순:3 첫수:아츠 크리티컬 오버킬'))
# print(fgo_np_calc_discord('공:12280+1786  버스트  대군  보렙:1  클래스:아처  공뻥:10%+11%  보뻥:15+15%  보퀘  보구특공:50%'))
# print(fgo_req_exp(1, 80))
# print(fgo_np_calc())
# print(fgo_gain_np_calc())