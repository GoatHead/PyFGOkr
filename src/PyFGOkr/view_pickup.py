import os
fpath = os.path.dirname(__file__)
import sqlite3
import math
import string
import datetime

last_update = '18.12.23'
pid_max = 0
db_path = fpath + '/db/fgo_db.sqlite'
cache = {} #dict 자료형을 이용한 cache
err = {'err' : '[오류 발생]',
       'year' : "[올바른 년도를 입력해주세요.]",
       'id' : '[올바른 ID 값을 입력해주세요.]',
       'value' : '[올바른 값을 입력해주세요.]'}

def rare2star(str):
    return str+'★'

def tuple2str(str):
    for x in str:
        val = x
        val = val.replace('(', '')
        val = val.replace(',', '')
        val = val.replace(')', '')
        return val


def int2id(num):
    num = int(num)
    return str('{0:03d}'.format(num))


class View:
    alphabet_l = list(string.ascii_lowercase)
    year_sel = {} # 픽업 연도값을 저장함. dict 자료형 {a: 2015, b:2016 등}
    conn, curs = 0, 0

    def __init__(self):
        global pid_max
        self.conn = sqlite3.connect(db_path)
        self.curs = self.conn.cursor()
        query = "select distinct start_year from pickup_list"
        self.curs.execute(query)
        res = self.curs.fetchall()
        year_l = []
        for x in res:
            val = str(x)
            val = val.replace('(','')
            val = val.replace(',', '')
            val = val.replace(')', '')
            year_l.append(val)
        self.year_sel = dict(zip(self.alphabet_l, year_l))
        #총 년도 저장
        query = "select max(pickup_id) from pickup_list"
        self.curs.execute(query)
        res = self.curs.fetchone()
        pid_max = int(tuple2str(res))
        #최대 pid 개수 저장

    def show_list(self, style=''):
        if 'start' in cache:
            return cache['start']
        else:
            res_str = ['', '', '']
            res_str[0] = 'Fate/Grand Order 픽업 목록'
            res_str[2] = '- Last Update - ' + last_update
            try:
                for x in range(len(self.year_sel)):
                    selectedYear = self.year_sel[self.alphabet_l[x]]
                    res_str[1] += '{0}. {1}\n'.format(self.alphabet_l[x], selectedYear)
                res_str[1] = res_str[1][:-1]
                if style == 'discord':
                    res_str[0] = conv_discord_style(res_str[0], 'yaml')
                    res_str[1] = conv_discord_style(res_str[1])
                    res_str[2] = conv_discord_style(res_str[2], 'diff')
                cache[('start')] = res_str
                return res_str
            except ValueError:
                return err['err']

    def show_list_year(self, param='a', page=1, style='', year=0):
        global cache
        if param not in self.year_sel:
            return err['year']
        if (param, page) in cache:
            return cache[param, page]
        try:
            # 시작 부분 타이틀 만들기
            pYear = self.year_sel[param]
            if year > 0:
                pYear = str(year)
            res_str = ['', '', '']
            res_str[0] = 'Fate/Grand Order ' + pYear + '년 픽업 목록' + ' <' + param + '>'
            #DB 쿼리해서 불러올 값 목록 만들기
            query = "select distinct * from pickup_list where start_year =" + pYear
            self.curs.execute(query)
            res = self.curs.fetchall()
            reslist = []
            for row in res:
                dt = row[2]
                dt = dt.replace('-', ' ')
                dt = datetime.datetime.strptime(dt, '%Y %m %d')
                dt = dt.strftime("%m.%d")
                reslist.append([row[0], row[1], dt])
            # for x in reslist:
            #     print(x)
            showlist = []
            for x in range(7):
                paging_pick_num = x + 7 *(page - 1)
                if 0 <= paging_pick_num < len(reslist):
                    showlist.append(reslist[paging_pick_num])
                else:
                    break
            # for x in showlist:
            #     print(x)
            #값 불러오기
            if showlist:
                for x in showlist:
                    res_str[1] += '[{0}] {1} / #{2}\n'.format(x[0], x[1], x[2])
                res_str[1] = res_str[1][:-1]
            else:
                res_str[1] += '[존재하지 않는 페이지입니다.]'
            #페이징 하기
            total_page = math.ceil(len(reslist) / 7)
            for x in range(1, total_page + 1):
                if x == page:
                    res_str[2] += '<' + str(x) + '>' + ' '
                else:
                    res_str[2] += str(x) + ' '
            res_str[2] = res_str[2].strip()
            # for x in res_str:
            #     print(x)
            if style == 'discord':
                res_str[0] = conv_discord_style(res_str[0], 'yaml')
                res_str[1] = conv_discord_style(res_str[1])
                res_str[2] = conv_discord_style(res_str[2], '')
            cache[(param, page)] = res_str
            return res_str
        except ValueError:
            return err['err']

    def show_ob_pickup(self, param, style=''): #픽업 id를 받아서 대상 픽업 서번트와 예장을 출력함
        try:
            if not 1 <= int(param) <= pid_max:
                return err['id']
            param = int2id(param)
            #캐쉬
            if ('pickup', param) in cache:
                return cache['pickup', param]
            else:
                #타이틀부
                res_str = ['', '', '']
                pid = '' #픽업 아이디
                pname = '' # 픽업 이름
                pdate = '' # 픽업 날짜
                pyear = '' # 픽업 년도
                query = "select distinct * from pickup_list where pickup_id =" + "'" + param + "'"
                self.curs.execute(query)
                res = self.curs.fetchone()
                pid = res[0]
                pname = res[1]
                pdate = res[2].replace('-', ' ')
                pdate = datetime.datetime.strptime(pdate, '%Y %m %d')
                pdate = pdate.strftime("%m.%d")
                pyear = str(res[3])[2:]
                res = "<{0}> {1} #{3}.{2}".format(pid, pname, pdate, pyear)
                res_str[0] = res
                #본문
                query = "select s.name, s.class, s.rarity from servants s, pickup_list p, pickup_serv ps where " \
                        "ps.pickup_id = p.pickup_id and p.pickup_id=? and ps.serv_id = s.serv_id order by " \
                        "s.rarity desc, s.name asc;"
                self.curs.execute(query, (pid, ))
                rs = self.curs.fetchall()
                if len(rs) > 0:
                    res_str[1] += '[픽업 서번트]\n'
                    for record in rs:
                        rname = record[0]
                        rclass = record[1]
                        rrarity = rare2star(record[2])
                        res = '{0} {1} / {2}\n'.format(rrarity, rname, rclass, )
                        res_str[1] += res
                query = "select y.yejang_name from pickup_list p, pickup_yej y where p.pickup_id" \
                        " = y.pickup_id and p.pickup_id = ?"
                self.curs.execute(query, (pid, ))
                rs = self.curs.fetchall()
                if len(rs) > 0:
                    res_str[1] += '[픽업 예장]\n'
                    for record in rs:
                        yname = record[0]
                        res_str[1] += yname +'\n'
                res_str[1] = res_str[1][:-1]
                #종료
                pid = int(pid)
                pid_former, pid_next = 0, 0
                pname_former, pname_next = '', ''
                if (pid-1) > 0:
                    pid_former = pid - 1
                if (pid+1) <= pid_max:
                    pid_next = pid + 1
                query = "select pickup_id, name from pickup_list where pickup_id = '" + '{0:03d}'.format(
                    pid_former) + "' or " \
                                  "pickup_id = '" + '{0:03d}'.format(pid_next) + "'"
                self.curs.execute(query)
                rs = self.curs.fetchall()
                for row in rs:
                    if row[0] == '{0:03d}'.format(pid_former):
                        pname_former = row[1]
                    elif row[0] == '{0:03d}'.format(pid_next):
                        pname_next = row[1]
                if pid_former and pid_next:
                    res_str[2] += '←{0:03d}    ＊{1:03d}    {2:03d}→'.format(pid-1, pid, pid+1)
                elif pid_former:
                    res_str[2] += '←{0:03d}    ＊{1:03d}'.format(pid_former, pid)
                elif pid_next:
                    res_str[2] += '        ＊{0:03d}    {1:03d}→'.format(pid, pid_next)
                if pid_former:
                    res_str[2] += '\n#{0:03d} / [{1}]'.format(pid_former, pname_former)
                if pid_next:
                    res_str[2] += '\n#{0:03d} / [{1}]'.format(pid_next, pname_next)
                if style == 'discord':
                    res_str[0] = conv_discord_style(res_str[0])
                    res_str[1] = conv_discord_style(res_str[1])
                    res_str[2] = conv_discord_style(res_str[2])
                cache[('pickup', param)] = res_str
                return res_str
        except ValueError:
            return err['id']

    def data_pickup_list(self, year):
        pYear = str(year)
        # DB 쿼리해서 불러올 값 목록 만들기
        query = "select distinct * from pickup_list where start_year =" + pYear
        self.curs.execute(query)
        res = self.curs.fetchall()
        rdict = {}
        reslist = []
        for row in res:
            dt = row[2]
            dt = dt.replace('-', ' ')
            dt = datetime.datetime.strptime(dt, '%Y %m %d')
            dt = dt.strftime("%m.%d")
            reslist.append({'id' : row[0], 'name' : row[1], 'date' : dt})
        rdict.update({'pickup' : {year : reslist}})
        return rdict


    def data_pickup(self, pid):
        rdict = {}
        param = int2id(pid)
        pid = ''  # 픽업 아이디
        pname = ''  # 픽업 이름
        pdate = ''  # 픽업 날짜
        pyear = ''  # 픽업 년도
        query = "select distinct * from pickup_list where pickup_id =" + "'" + param + "'"
        self.curs.execute(query)
        res = self.curs.fetchone()
        pid = res[0]
        pname = res[1]
        pdate = res[2].replace('-', ' ')
        pdate = datetime.datetime.strptime(pdate, '%Y %m %d')
        pdate = pdate.strftime("%m.%d")
        pyear = str(res[3])[2:]
        rdict.update({'header' : { 'id' : pid , 'name' : pname, 'year' : pyear, 'date' : pdate}})
        #서번트
        query = "select s.name, s.class, s.rarity from servants s, pickup_list p, pickup_serv ps where " \
                "ps.pickup_id = p.pickup_id and p.pickup_id=? and ps.serv_id = s.serv_id order by " \
                "s.rarity desc, s.name asc;"
        self.curs.execute(query, (pid,))
        rs = self.curs.fetchall()
        rdict_servant = []
        if len(rs) > 0:
            for record in rs:
                rname = record[0]
                rclass = record[1]
                rrarity = rare2star(record[2])
                rdict_servant.append({'name' : rname, 'class' : rclass, 'rarity' : rrarity})
            rdict.update({ 'servants' : rdict_servant})
        #예장
        query = "select y.yejang_name from pickup_list p, pickup_yej y where p.pickup_id" \
                " = y.pickup_id and p.pickup_id = ?"
        self.curs.execute(query, (pid,))
        rs = self.curs.fetchall()
        rdict_yejang = []
        if len(rs) > 0:
            for record in rs:
                yname = record[0]
            rdict_yejang.append({'craft' : {'name' : yname}})
        # 종료
        pid = int(pid)
        pid_former, pid_next = 0, 0
        pname_former, pname_next = '', ''
        if (pid - 1) > 0:
            pid_former = pid - 1
        if (pid + 1) <= pid_max:
            pid_next = pid + 1
        query = "select pickup_id, name from pickup_list where pickup_id = '" + '{0:03d}'.format(
            pid_former) + "' or " \
                          "pickup_id = '" + '{0:03d}'.format(pid_next) + "'"
        self.curs.execute(query)
        rs = self.curs.fetchall()
        rdict_pickup_list = []
        for row in rs:
            if row[0] == '{0:03d}'.format(pid_former):
                pname_former = row[1]
            elif row[0] == '{0:03d}'.format(pid_next):
                pname_next = row[1]
        if pid_former:
            rdict['header'].update({'formerid': {'id': pid_former, 'name': pname_former}})
        if pid_next:
            rdict['header'].update({'nextid': {'id': pid_next, 'name': pname_next}})
        return rdict

    def data_servant_search(self, sclass, sname):
        rdict = {}
        query = "select p.pickup_id, p.name, p.start_date from pickup_list p, pickup_serv ps, servants s where" \
                " p.pickup_id = ps.pickup_id and ps.serv_id = s.serv_id and s.name = ?" \
                " and  s.class = ?"
        self.curs.execute(query, (sname, sclass))
        rs = self.curs.fetchall()
        if not len(rs) > 0:
            query = "select p.pickup_id, p.name, p.start_date from pickup_list p, pickup_serv ps, servants s where" \
                    " p.pickup_id = ps.pickup_id and ps.serv_id = s.serv_id and s.name like ?" \
                    " and  s.class = ?"
            sname = sname.replace(' ', '%')
            self.curs.execute(query, ('%' + sname + '%', sclass))
            rs = self.curs.fetchall()
            if not len(rs) > 0:
                return err['value']
        num_chk = 0
        rdict_pickup_list = []
        for row in rs:
            num_chk += 1
            pid = row[0]
            pname = row[1]
            pdate = row[2].replace('-', ' ')
            pdate = datetime.datetime.strptime(pdate, '%Y %m %d')
            pdate = pdate.strftime('#%y.%m.%d')
            rdict_pickup_list.append({'id' : pid, 'name' : pname, 'date' : pdate})
        rdict.update({'pickups': rdict_pickup_list, 'pickuptimes' : num_chk})
        return rdict

    def show_pickup_by_serv(self, sclass, sname, style=''):
        if (sclass, sname) in cache:
            return cache[sclass, sname]
        query = "select p.pickup_id, p.name, p.start_date from pickup_list p, pickup_serv ps, servants s where" \
                " p.pickup_id = ps.pickup_id and ps.serv_id = s.serv_id and s.name = ?" \
                " and  s.class = ?"
        self.curs.execute(query, (sname, sclass))
        rs = self.curs.fetchall()
        if not len(rs) > 0:
            query = "select p.pickup_id, p.name, p.start_date from pickup_list p, pickup_serv ps, servants s where" \
                    " p.pickup_id = ps.pickup_id and ps.serv_id = s.serv_id and s.name like ?" \
                    " and  s.class = ?"
            sname = sname.replace(' ', '%')
            self.curs.execute(query, ('%' + sname + '%', sclass))
            rs = self.curs.fetchall()
            if not len(rs) > 0:
                return err['value']
        res = ''
        num_chk = 0
        for row in rs:
            num_chk += 1
            pid = row[0]
            pname = row[1]
            pdate = row[2].replace('-', ' ')
            pdate = datetime.datetime.strptime(pdate, '%Y %m %d')
            pdate = pdate.strftime('#%y.%m.%d')
            res += '[{0}] {1} {2}\n'.format(pid, pname, pdate)
        res += '총 <{0}>회의 픽업 소환이 있습니다.'.format(num_chk)
        if style == 'discord':
            res = conv_discord_style(res)
        cache[(sclass, sname)] = res
        return res

    def _view_debug_(self):
        print('===cache===')
        print(cache)


view = View()

def data_servant_pickup(sclass, sname):
    return view.data_servant_search(sclass, sname)

def data_pickups(year):
    return view.data_pickup_list(year)

def data_pickup(id):
    return view.data_pickup(id)

# @Discord용
# 인자 args는 '세이버 알트리아 펜드래건' 같은 식으로,
# 서번트 "클래스명 이름"으로 입력하면 된다.
def search_pickup_discord(args):
    sclass = ''
    class_list = ['세이버', '아처', '랜서', '라이더', '어새신', '캐스터', '버서커',
                  '실더', '룰러', '어벤저', '얼터 에고', '문 캔서', '포리너', '비스트']
    convlist = args
    for s in class_list:
        if s in convlist:
            sclass = s
            convlist = convlist.replace(s, '', 1)
            convlist = convlist.strip()
            break
    sname = convlist
    #view._view_debug_() # 캐쉬 디버그
    try:
        return view.show_pickup_by_serv(sclass, sname, style='discord')
    except:
        return err['value']


# 년도는 처음 모듈이 실행될 때 알파벳으로 대응되서 저장됨 {'a' : 2015, 'b' : 2016,  ... }
# ===인자 값===
# 연도별 픽업/ -a(연도 설정) ex) -a를 인자로 줄 경우 2015년의 픽업 1페이지가 출력
# 연도별 픽업/ =1(페이지 설정) ex) -a =2를 인자로 줄 경우 2015년의 2페이지가 출력
# 픽업 보기/  :1 ex) :67을 인자로 줄 경우 67번째 픽업이 출력
# 인자가 없을 경우 선택 가능한 연도가 출력됨
def call_discord(input_str):
    res=''
    parseStr = []
    parseStr = input_str.split(' ')
    param_year = -1
    param_page = -1
    param_pickup = -1
    for param in parseStr:
        if '-' in param: #년도 뷰
            param_year = param[1:]
            continue
        elif '=' in param: #페이지 뷰
            param_page = param[1:]
            continue
        elif ':' in param: #픽업 뷰
            param_pickup = param[1:]
            continue
    if param_pickup != -1:
        res = view.show_ob_pickup(param_pickup, style='discord')
    elif param_page != -1 and param_year != -1:
        res = view.show_list_year(param_year, int(param_page), style='discord')
    elif param_year != -1:
        res = view.show_list_year(param_year, style='discord')
    else:
        res = view.show_list(style='discord')
    return res

def conv_discord_style(str, style='css'):
    res = '```{}\n'.format(style)
    res += str
    res += '\n```'
    return res
# Discord 끝
# #
# Discord 스타일로 불러오는 함수. 사용할 필요는 없고 단지 참고용
# 인자 args는 '세이버 알트리아 펜드래건' 같은 식으로,
# 서번트 "클래스명 이름"으로 입력하면 된다.
# def search_pickup(servant='세이버 알트리아 펜드래건'):
#     sclass = ''
#     class_list = ['세이버', '아처', '랜서', '라이더', '어새신', '캐스터', '버서커',
#                   '실더', '룰러', '어벤저', '얼터 에고', '문 캔서', '포리너', '비스트']
#     convlist = servant
#     for s in class_list:
#         if s in convlist:
#             sclass = s
#             convlist = convlist.replace(s, '', 1)
#             convlist = convlist.strip()
#             break
#     sname = convlist
#     #view._view_debug_() # 캐쉬 디버그
#     try:
#         return view.show_pickup_by_serv(sclass, sname)
#     except:
#         return err['value']
# # 픽업 목록을 반환
# def call_listview(year=2015, page=1):
#     return view.show_list_year(year=year, page=page)
#
# # 해당 번호의 픽업을 불러온다.
# def call_pickup(pid=1):
#     return view.show_ob_pickup(pid)
#
# # 픽업 메인 페이지를 불러온다.
# def call_total_list():
#     return view.show_list()
# #