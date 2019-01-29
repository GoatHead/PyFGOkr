from bs4 import BeautifulSoup
import requests
import json
import logging
import re
import urllib.parse

def isKoreanChar(text):
    hangul = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    for i in range(len(text)):
        chk = (hangul.findall(text[i]))
        if not chk: #특수 문자거나 빈 문자열
            return False
        else:
            return True
    return

def QurreyNamuWiki(text):
    result = ''
    for i in range(len(text)):
        if isKoreanChar(text[i]):
            result = result + text[i]
        else:
            result = result + urllib.parse.quote(text[i])
    return result

def get_html(url):
    _html = ''
    r = requests.get(url)
    if r.status_code == 200:
        _html = r.text
        return _html
    return '존재하지 않는 주소입니다.'

def listSrchAsString(plist, pstring, pint):
    dum_list_index = 0
    try:
        dum_list_index =  plist.index(pstring) + pint
        return plist[dum_list_index]
    except dum_list_index > len(plist):
        return 0

def inListString(obj_input, string):
        if string in obj_input:
            return True
        else:
            return False

def deletecolon(string):
    if ':' in string:
        ind = string.index(':')
        string = string[ind+1:].strip()
        return string

def deletecomment(string):
    for i in range(10):
        ch_s = '[{}]'.format(i)
        string = string.replace(ch_s, '')
    return string

def deletejlist(list):
    retu_list = []
    for s in list:
        s = deletecomment(s)
        retu_list.append(s)
    return retu_list

class printer:
    class_name = ''
    servant_name = ''
    statlist = []

    def __make_out_string(self, option=''):
        out_str = ''
        out_str += self.__show_serv_name()
        if option == 'debug':
            return ''
        elif option == 'stat':
            out_str += self.__show_upg_stat()
            out_str += self.__show_command_card()
            out_str += self.__show_hidden_stat()
            out_str += self.__show_class_skill()
        elif option == 'skill':
            out_str += self.__show_skill()
        elif option == 'noble':
            out_str += self.__show_noble()
        else:
            out_str += self.__show_upg_stat()
            out_str += self.__show_skill()
            out_str += self.__show_noble()
            out_str += self.__show_command_card()
            out_str += self.__show_hidden_stat()
            out_str += self.__show_class_skill()
        return out_str

    def __make_stat_list(self, cln, srvn):
        self.class_name = cln
        self.servant_name = srvn
        if cln in ['세이버', '아처', '랜서', '라이더', '어새신', '캐스터', '버서커']:
            convClass = cln
        else:
            convClass = '엑스트라%20클래스/' + cln
        convServ = QurreyNamuWiki(self.servant_name)
        qry_url = 'https://namu.wiki/w/Fate/Grand%20Order/서번트/' + convClass + '/' + convServ
        return self.__get_status_list(qry_url)

    def out(self, cln, srvn):
        self.statlist = self.__make_stat_list(cln, srvn)
        # self.__list_see_easy(self.statlist) # 디버그용
        out_str = self.__make_out_string()
        return out_str

    def out_stat(self, cln, srvn):
        self.statlist = self.__make_stat_list(cln, srvn)
        #self.__list_see_easy(self.statlist) #디버그용
        out_str = self.__make_out_string('stat')
        return out_str


    def out_debug(self, cln, srvn):
        self.statlist = self.__make_stat_list(cln, srvn)
        self.__list_see_easy(self.statlist) # 디버그용
        out_str = self.__make_out_string('debug')
        return out_str


    def out_skill(self, cln, srvn):
        self.statlist = self.__make_stat_list(cln, srvn)
        # self.__list_see_easy(self.statlist) # 디버그용
        out_str = self.__make_out_string('skill')
        return out_str


    def out_noble(self, cln, srvn):
        self.statlist = self.__make_stat_list(cln, srvn)
        # self.__list_see_easy(self.statlist) # 디버그용
        out_str = self.__make_out_string('noble')
        return out_str

    def out_data(self, cln, srvn):
        self.statlist = self.__make_stat_list(cln, srvn)
        serv_dic = {}
        serv_dic.update(self.__show_serv_name(returnData=True))
        serv_dic.update(self.__show_upg_stat(returnData=True))
        serv_dic.update(self.__show_skill(returnData=True))
        serv_dic.update(self.__show_noble(returnData=True))
        serv_dic.update(self.__show_command_card(returnData=True))
        serv_dic.update(self.__show_hidden_stat(returnData=True))
        serv_dic.update(self.__show_class_skill(returnData=True))
        return serv_dic

    def __get_status_list(self, url):
        namu = get_html(url)
        soup = BeautifulSoup(namu, 'html.parser')
        a = soup.find_all('td')
        tes_a = soup.find_all('td', {"style" : "background-color:white; text-align:center;"})
        subjlist = []
        for link in tes_a:
            subjlist.append(link.text.strip())
        b = ''
        for link in a:
            b = b + ''.join(map(str, (link)))
        b = BeautifulSoup(b, 'html.parser')
        textlist = []
        for link in b:
            textlist.append(link.text.strip())
        sstart_index = textlist.index('영기재림 구간 별 스테이터스')
        if '즉사 내성' in textlist:
            send_index = textlist.index(('즉사 내성')) + 5
        else:
            for x in textlist:
                if '즉사율' in x:
                    send_index = textlist.index(x) + 5
        statlist = textlist[sstart_index:send_index]
        for link in subjlist:
            if link in statlist:
                statlist[statlist.index(link)] = 's' + statlist[statlist.index(link)]
        #버스터 업 등의 스킬은 s로 구분할 수 있음.
        for s in statlist:
            if s == 's':
                statlist[statlist.index('s')] = ''
        return statlist

    def __show_serv_name(self, returnData=False):
        out_str = ''
        cln = self.class_name
        srvn = self.servant_name
        serv_dic = {'name' : srvn, 'class' : cln}
        out_str = '[{}]{}\n'.format(cln,srvn)
        if returnData: return serv_dic
        return out_str
    def __show_upg_stat(self, returnData=False):
        #인덱스의 0,1,2,3 = LV1,80,90,100을 의미(5성일시)
        serv_dic = {'status' : {}}
        isStar5 = True
        atk_i = self.statlist.index('Atk')
        hp_i = self.statlist.index('Hp')
        if (hp_i - atk_i) == 9: #칼럼 개수가 다르므로 인덱스값의 차로 4성,5성을 판별
            isStar5 = False
        ATK = [0] * 4
        HP = [0] * 4
        ATK[0] = self.statlist[atk_i + 1]
        # Atk 값 찾기.
        levellist = [1, 80, 90, 100]
        if isStar5:
            for x in range(1, 4):
                ATK[x] = self.statlist[atk_i + 4 + x]
        else:
            for x in range(1, 4):
                if x == 1:
                    ATK[x] = self.statlist[atk_i + 5 + x]
                else:
                    ATK[x] = self.statlist[atk_i + 5 + x]
        serv_dic['status'].update({'atk' : dict(zip(levellist, ATK))})
        #Hp 값 찾기
        HP[0] = self.statlist[hp_i+1]
        if isStar5:
            for x in range(1, 4):
                HP[x] = self.statlist[hp_i + 4 + x]
        else:
            for x in range(1, 4):
                if x == 1:
                    HP[x] = self.statlist[hp_i + 5 + x]
                else:
                    HP[x] = self.statlist[hp_i + 5 + x]
        serv_dic['status'].update({'hp' : dict(zip(levellist, HP))})
        #출력 스트링 만들기
        out_str = '|Lv001|ATK: {} HP: {}\n|Lv080|ATK: {} HP: {}\n|Lv090|ATK: {} HP: {}\n' \
                  '|Lv100|ATK: {} HP: {}\n'.format(ATK[0],HP[0],ATK[1],HP[1],ATK[2],HP[2],ATK[3],HP[3])
        if returnData: return serv_dic
        return  out_str

    def __show_skill(self, returnData=False):
        ##기본 스킬##
        serv_dic = { 'skill' : {}}
        index_start = self.statlist.index('보유 스킬')
        index_end = self.statlist.index('클래스 스킬')
        parsing_list = self.statlist[index_start:index_end]
        effect_count = 0
        out_str = ''
        std_index = [index for index, value in enumerate(parsing_list) if value == '효과']
        dic_skill_list = []
        for i in parsing_list:
            if i == '효과':
                effect_count += 1
        subdic = {}
        for i in range(0, effect_count): ##스킬 출력을 반복
            subdic.update({i : {}})
            check_upg_quest = parsing_list[std_index[i]-3]
            skill_name = parsing_list[std_index[i]+2]
            if inListString(skill_name, 's') == True:
                parsing_list[parsing_list.index(skill_name)] = parsing_list[parsing_list.index(skill_name)][1:]
                skill_name = skill_name[1:]
            skill_desc =  parsing_list[std_index[i]+3]
            if inListString(check_upg_quest, '▼'): #강화퀘를 체크/스킬 이름을 붙이기
                subdic[i].update({'name': '[▼{}]'.format(skill_name)})
            else:
                subdic[i].update({'name': skill_name})
            out_str += subdic[i]['name'] + '\n'
            subdic[i].update({'desc' : skill_desc})
            out_str += subdic[i]['desc'] + '\n' # 스킬 설명을 붙이기
            if i != effect_count-1: #i가 끝까지 안 가면
                skill_effect_list = parsing_list[std_index[i]:std_index[i + 1]]
            else:
                skill_effect_list = parsing_list[std_index[i]:]
            skill_effect_index =[index for index, value in enumerate(skill_effect_list) if 's' in value]
            dic_skill_effect_list = []
            dic_skill_cooldown_list = []
            for _i in range(len(skill_effect_index)): #스킬 효과 개수
                if skill_effect_index[_i] == skill_effect_index[-1]: #쿨다운 설명(3개까지)
                    effect_inte = 3
                    skill_effect = []
                    for j in range(1, effect_inte+1): #스킬 효과 레벨(ex:1~10)
                        skill_effect.append(skill_effect_list[skill_effect_index[_i]+j])
                    out_str += '<쿨다운>\n|{}|{}|{}|\n'.format(skill_effect[0], skill_effect[1], skill_effect[2])
                    dic_skill_cooldown_list = [int(x) for x in skill_effect]
                else: #쿨다운 외 기타 설명
                    effect_inte = skill_effect_index[_i+1] - skill_effect_index[_i] - 1
                    skill_effect_name = skill_effect_list[skill_effect_index[_i]][1:]
                    out_str += '<{}>\n'.format(skill_effect_name)
                    dic_skill_effect_list.append({'effectname' : skill_effect_name})
                    if not effect_inte == 1:
                        out_str += '|'
                        for j in range(1, effect_inte+1): #스킬 효과 레벨(ex:1~10)
                            idx = skill_effect_index[_i]+j
                            skill_effect = skill_effect_list[idx]
                            dic_skill_effect_list[_i].update({ j : skill_effect})
                            out_str += 'LV{:02}|{}|'.format(j ,skill_effect)
                    else:
                        skill_effect = skill_effect_list[skill_effect_index[_i] + 1]
                        dic_skill_effect_list[_i].update({1: skill_effect})
                        out_str += '{}'.format(skill_effect)
                    out_str += '\n'
            subdic[i].update({'effect' : dic_skill_effect_list})
            subdic[i].update({'cooldown': dic_skill_cooldown_list})
        serv_dic = {'skill' : subdic}
        ##클래스 스킬##
        if returnData: return serv_dic
        return out_str

    def __show_noble(self, returnData=False):
        serv_dic = {}
        #보구 문구 찾기
        self.statlist = deletejlist(self.statlist)
        index_start = self.statlist.index('보구')
        index_end = self.statlist.index('커맨드 카드')
        parsing_list = self.statlist[index_start:index_end]
        match = [s for s in parsing_list if '랭크' in s] #문자열 추출
        match = parsing_list.index(''.join(match)) #리스트를 문자열로
        sr_i = match
        noble_name = parsing_list[sr_i-1][1:].strip() #보구 이름
        noble_rank = deletecolon(parsing_list[sr_i].strip())
        noble_type = deletecolon(parsing_list[sr_i + 1].strip())
        noble_card = deletecolon(parsing_list[sr_i + 2].strip())
        noble_effect = listSrchAsString(parsing_list, '효과', 1)[1:]
        noble_power = [0]*5
        noble_power_name = listSrchAsString(parsing_list, '효과', 8)[1:]
        for x in range(5):
            noble_power[x] = listSrchAsString(parsing_list,'보구 레벨',7+x)
        noble_overcharge = [0]*5
        noble_ovch_name = listSrchAsString(parsing_list,'오버차지', 6)[1:].strip()
        for x in range(5):
            noble_overcharge[x] = listSrchAsString(parsing_list,'오버차지',7+x)
        #보구 효과 문자열 추출
        sindex_start = self.statlist.index('보구 레벨')
        sindex_end = self.statlist.index('오버차지')
        sub_list = self.statlist[sindex_start:sindex_end]
        serv_dic.update({ 'name' : noble_name, 'rank' : noble_rank,
                          'card' : noble_card, 'category' : noble_type,
                          'power' : { 'effectname' : noble_effect },
                          'overcharge' : { 'effectname' : noble_ovch_name}})
        for i in range(0,5):
            serv_dic['power'].update({ (i+1) : noble_power[i]})
        for i in range(0,5):
            serv_dic['overcharge'].update({ (i+1) : noble_overcharge[i]})
        out_str = '[보구]{} {}\n[{}]{}\n'.format(noble_name, noble_rank,noble_card,noble_type)
        out_str = out_str + '<효과>\n{}\n'.format(noble_effect)
        out_str += '<위력>\n|LV1|{}|LV2|{}|LV3|{}|LV4|{}|LV5|{}|\n'.format(
            noble_power[0], noble_power[1], noble_power[2], noble_power[3], noble_power[4])
        out_str += '<{}>\n|LV1|{}|LV2|{}|LV3|{}|LV4|{}|LV5|{}|\n'.format(
            noble_ovch_name, noble_overcharge[0], noble_overcharge[1], noble_overcharge[2], noble_overcharge[3],
            noble_overcharge[4]
        )
        #보구 강화 받기 전 보구만
        #보구 강화 후
        if '보구 강화 후' in self.statlist:
            serv_dic = [serv_dic, {}]
            index_start = self.statlist.index('보구 강화 후')
            index_end = self.statlist.index('커맨드 카드')
            parsing_list = self.statlist[index_start:index_end]
            sr_i = parsing_list.index('보구 강화 후')
            noble_effect = parsing_list[sr_i + 1][3:].strip()
            noble_power = [0] * 5
            for x in range(5):
                noble_power[x] = listSrchAsString(parsing_list, '보구 레벨', 7 + x)
            noble_overcharge = [0] * 5
            noble_ovch_name = listSrchAsString(parsing_list, '오버차지', 6)[1:].strip()
            for x in range(5):
                noble_overcharge[x] = listSrchAsString(parsing_list, '오버차지', 7 + x)
            serv_dic[1].update({'name': noble_name, 'rank': noble_rank,
                             'card': noble_card, 'category': noble_type,
                             'power': {'effectname': noble_effect},
                             'overcharge': {'effectname': noble_ovch_name}})
            for i in range(0, 5):
                serv_dic[1]['power'].update({(i + 1): noble_power[i]})
            for i in range(0, 5):
                serv_dic[1]['overcharge'].update({(i + 1): noble_overcharge[i]})
            plus_str = '[보구 강화 후]\n'
            plus_str += '<효과>\n{}\n'.format(noble_effect)
            plus_str += '<위력>\n|LV1|{}|LV2|{}|LV3|{}|LV4|{}|LV5|{}|\n'.format(
                noble_power[0], noble_power[1], noble_power[2], noble_power[3], noble_power[4])
            plus_str += '<{}>\n|LV1|{}|LV2|{}|LV3|{}|LV4|{}|LV5|{}|\n'.format(
                noble_ovch_name, noble_overcharge[0], noble_overcharge[1], noble_overcharge[2], noble_overcharge[3],
                noble_overcharge[4]
            )
            out_str += plus_str
        serv_dic = {'np': serv_dic}
        if returnData: return serv_dic
        return out_str

    def __show_command_card(self, returnData=False):
        serv_dic = {}
        index_start = self.statlist.index('커맨드 카드')
        index_end = self.statlist.index('속성')
        parsing_list = self.statlist[index_start:index_end]
        ccard_list = [0] * 5 # 커맨드 카드 저장
        for x in range(5):
            ccard_list[x] = listSrchAsString(parsing_list, '커맨드 카드', 1 + x)
        strike_times = [0] * 5 # 타격 횟수. Q A B E 보구 순서
        for x in range(5):
            if x == 4 and parsing_list[-1][0] == 'E':
                break
            strike_times[x] = listSrchAsString(parsing_list, '타격 횟수', 1 + x)
        out_str = '[커맨드 카드]\n'
        serv_dic.update({ 'card' : [ccard_list[x] for x in range(0,5)] })
        out_str += '<구성>\n「{}」「{}」「{}」「{}」「{}」\n'.format(
            ccard_list[0],ccard_list[1],ccard_list[2],ccard_list[3],ccard_list[4]
        )
        if strike_times[4]:
            serv_dic.update({'hit': dict(zip(['Q', 'A', 'B', 'E', 'N'],[eval(strike_times[x][-2:]) for x in range(0, 5)]))})
            out_str += '<타격 횟수>\n|{}|{}|{}|{}|{}|\n'.format(
                strike_times[0],strike_times[1],strike_times[2],strike_times[3],strike_times[4]
        )
        else:
            serv_dic.update({'hit': dict(zip(['Q', 'A', 'B', 'E'], [eval(strike_times[x][-2:]) for x in range(0, 4)]))})
            out_str += '<타격 횟수>\n|{}|{}|{}|{}|\n'.format(
                strike_times[0],strike_times[1],strike_times[2],strike_times[3])
        if returnData: return serv_dic
        return out_str

    def __show_hidden_stat(self, returnData=False):
        serv_dic = {}
        index_start = self.statlist.index('속성')
        parsing_list = self.statlist[index_start:]
        np_gain = parsing_list[-4]
        star_concent = parsing_list[-3]
        star_create = parsing_list[-2]
        if '즉사 내성' in parsing_list:
            insta_name = '즉사 내성'
        else:
            insta_name = '즉사율'
        insta_death = parsing_list[-1]
        hidden_attr = parsing_list[1]
        hidden_attr = hidden_attr[0] + ", " + hidden_attr[1:]
        out_str = '[히든 스테이터스]\n'
        serv_dic.update({'hidden' : {'attribute' : hidden_attr.split(', ')}})
        serv_dic['hidden'].update({'npgain' : np_gain})
        serv_dic['hidden'].update({'starconcent': star_concent})
        serv_dic['hidden'].update({'starmake': star_create})
        serv_dic['hidden'].update({'instadeathrate': insta_death})
        out_str += '<속성>\n{}\n'.format(hidden_attr)
        out_str += '|NP 획득량|{}|스타 집중도|{}|스타 발생률|{}|{}|{}|\n'.format(np_gain,star_concent,star_create,insta_name,insta_death)
        if returnData: return serv_dic
        return out_str
    #디버그용

    def __show_class_skill(self, returnData=False):
        serv_dic = {'classskill' : []}
        index_start = self.statlist.index('클래스 스킬')
        index_end = self.statlist.index('보구')
        parsing_list = self.statlist[index_start:index_end]
        out_str = ''
        std_index = 2
        skill_num = int((len(parsing_list) + 1 - 2) / 3)
        out_str += '[클래스 스킬]\n'
        for i in range(skill_num):
            clskill = parsing_list[std_index + 3*i]
            if inListString(clskill, 's') == True:
                parsing_list[parsing_list.index(clskill)] = parsing_list[parsing_list.index(clskill)][1:]
                clskill = clskill[1:]
            clskilldes = parsing_list[std_index + 3*i + 1]
            serv_dic['classskill'].append({'name' : clskill, 'desc' : clskilldes})
            out_str += '|{}|{}\n'.format(clskill, clskilldes)
        if returnData: return serv_dic
        return out_str

    def __list_see_easy(self, statlist):
        for i in statlist:
            print('[',str(statlist.index(i)),']' + i)

def out_all(cln, srvn, style=''):
    try:
        clprinter = printer()
        out_str = clprinter.out(cln, srvn)
        out_str = deletecomment(out_str)
        if style == 'discord':
            out_str = conv_discord(out_str)
        return out_str
    except Exception as e:
        # logger = logging.getLogger()
        # logger.exception()
        # raise
        return '올바른 명칭을 입력하세요.'

def out_stat(cln, srvn, style=''):
    # try:
    clprinter = printer()
    out_str = clprinter.out_stat(cln, srvn)
    out_str = deletecomment(out_str)
    if style == 'discord':
        out_str = conv_discord(out_str)
    return out_str
    # except:
    #     return '올바른 명칭을 입력하세요.'

def out_noble(cln, srvn, style=''):
    # try:
        clprinter = printer()
        out_str = clprinter.out_noble(cln, srvn)
        out_str = deletecomment(out_str)
        if style == 'discord':
            out_str = conv_discord(out_str)
        return out_str
    # except:
    #     return '올바른 명칭을 입력하세요.'

def out_skill(cln, srvn, style=''):
    try:
        clprinter = printer()
        out_str = clprinter.out_skill(cln, srvn)
        out_str = deletecomment(out_str)
        if style == 'discord':
            out_str = conv_discord(out_str)
        return out_str
    except:
        return '올바른 명칭을 입력하세요.'

def out_debug(cln, srvn, style=''):
    try:
        clprinter = printer()
        out_str = clprinter.out_debug(cln, srvn)
        out_str = deletecomment(out_str)
        if style == 'discord':
            out_str = conv_discord(out_str)
        return out_str
    except:
        return '올바른 명칭을 입력하세요.'


def out_servants(sclass='세이버', sname='알트리아 펜드래건'):
    return

##data 반환
def out_dict(cls, srvn):
    class_list = ['세이버', '아처', '랜서', '라이더', '어새신', '캐스터', '버서커',
                  '실더', '룰러', '어벤저', '얼터 에고', '문 캔서', '포리너', '비스트']
    if cls in class_list:
        clprinter = printer()
        serv_dic = clprinter.out_data(cls, srvn)
        return serv_dic
    else:
        return '서번트 클래스 이름을 제대로 써주세요.'

##discord용 함수들
def conv_discord(str):
    return '```css\n{}\n```'.format(str)

def out_discord(args):
    return check_string(args)

def check_string(args):
    # try:
        setting = ''
        class_list = ['세이버', '아처', '랜서', '라이더', '어새신', '캐스터', '버서커',
                      '실더', '룰러', '어벤저', '얼터 에고', '문 캔서', '포리너', '비스트']
        setting_list = ['보구', '스탯', '스킬']
        convlist = ' '.join(args)
        args = []
        for s in class_list:
            if s in convlist:
                args.append(s)
                convlist = convlist.replace(s, '')
                break
        for s in setting_list:
            if s in convlist:
                args.append(s)
                convlist = convlist.replace(s, '')
        convlist = convlist.strip()
        args.insert(1, convlist)
        if args[-1] == '보구':
            args.remove('보구')
            setting = '보구'
        elif args[-1] == '스탯':
            args.remove('스탯')
            setting = '스탯'
        elif args[-1] == '스킬':
            args.remove('스킬')
            setting = '스킬'
        elif args[-1] == '디버그':
            args.remove('디버그')
            setting = '디버그'
        retu_str = ''
        if setting == '보구':
            retu_str = out_noble(args[0], args[1], style='discord')
        elif setting == '스탯':
            retu_str = out_stat(args[0], args[1], style='discord')
        elif setting == '스킬':
            retu_str = out_skill(args[0], args[1], style='discord')
        elif setting == '디버그':
            retu_str = out_debug(args[0], args[1], style='discord')
        else:
            retu_str = out_all(args[0], args[1], style='discord')
        return retu_str
    # except:
    #     return '올바른 값을 입력해주세요2.'
#discord용 끝
# print(out_dict('아처', '에미야'))
# with open('res.json', 'w', encoding='utf8') as fp:
#     json.dump(out_dict('아처', '에미야'), fp, ensure_ascii=False)