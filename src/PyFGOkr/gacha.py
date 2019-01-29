import os, sys, inspect, shutil
sys.path.append(os.path.realpath('.'))
fpath = os.path.dirname(__file__)
respath = fpath + '/img/result/'
from PIL import Image
from datetime import datetime
import random
import time

#####global var
now = datetime.now()
class globe:
    prefix_str = ''
################function
def init_serv_star5():
    basepath = fpath + '/img/servant_star5'
    global serv_5s_list
    global serv_5s_pickup_list
    serv_5s_list = []
    for fname in os.listdir(basepath):
        path = os.path.join(basepath, fname)
        if os.path.isdir(path):
            continue
        serv_5s_list.append(fname)
    serv_5s_pickup_list = os.listdir(os.path.join(basepath,'pickup'))


def init_serv_star4():
    basepath = fpath + '/img/servant_star4'
    global serv_4s_list
    global serv_4s_pickup_list
    global not_pu_4s
    not_pu_4s = False
    serv_4s_list = []
    for fname in os.listdir(basepath):
        path = os.path.join(basepath, fname)
        if os.path.isdir(path):
            continue
        serv_4s_list.append(fname)
    serv_4s_pickup_list = os.listdir(os.path.join(basepath, 'pickup'))
    if not serv_4s_pickup_list:
        serv_4s_pickup_list = serv_4s_list
        not_pu_4s = True


def init_serv_star3():
    basepath = fpath + '/img/servant_star3'
    global serv_3s_list
    global serv_3s_pickup_list
    global not_pu_3s
    not_pu_3s = False
    serv_3s_list = []
    for fname in os.listdir(basepath):
        path = os.path.join(basepath, fname)
        if os.path.isdir(path):
            continue
        serv_3s_list.append(fname)
    serv_3s_pickup_list = os.listdir(os.path.join(basepath, 'pickup'))
    if not serv_3s_pickup_list:
        serv_3s_pickup_list = serv_3s_list
        not_pu_3s = True


def init_yej_star5():
    basepath = fpath + '/img/yejang_star5'
    global yej_5s_list
    global yej_5s_pickup_list
    global not_pu_5y
    not_pu_5y = False
    yej_5s_list = []
    for fname in os.listdir(basepath):
        path = os.path.join(basepath, fname)
        if os.path.isdir(path):
            continue
        yej_5s_list.append(fname)
    yej_5s_pickup_list= os.listdir(os.path.join(basepath,'pickup'))
    if not yej_5s_pickup_list:
        yej_5s_pickup_list = yej_5s_list
        not_pu_5y = True


def init_yej_star4():
    basepath = fpath + '/img/yejang_star4'
    global yej_4s_list
    global yej_4s_pickup_list
    global not_pu_4y
    not_pu_4y = False
    yej_4s_list = []
    for fname in os.listdir(basepath):
        path = os.path.join(basepath, fname)
        if os.path.isdir(path):
            continue
        yej_4s_list.append(fname)
    yej_4s_pickup_list = os.listdir(os.path.join(basepath,'pickup'))
    if not yej_4s_pickup_list:
        yej_4s_pickup_list = yej_4s_list
        not_pu_4y = True

def init_yej_star3():
    basepath = fpath + '/img/yejang_star3'
    global yej_3s_list
    global yej_3s_pickup_list
    global not_pu_3y
    not_pu_3y = False
    yej_3s_list = []
    for fname in os.listdir(basepath):
        path = os.path.join(basepath, fname)
        if os.path.isdir(path):
            continue
        yej_3s_list.append(fname)
    yej_3s_pickup_list = os.listdir(os.path.join(basepath,'pickup'))
    if not yej_3s_pickup_list:
        yej_3s_pickup_list = yej_3s_list
        not_pu_3y = True


def make_bg_folder(key):
    folder_path = fpath + '/img/result/{0}/'.format(key)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return folder_path


def result_composite(key, img):
    highimage = Image.open(fpath + '/img/now_pickup.png')
    lowimage = img
    hwidth, hheight = highimage.size
    lwidth, lheight = lowimage.size
    lowimage = lowimage.crop((0,15,lwidth,lheight))
    lwidth, lheight = lowimage.size
    hwidth, hheight = highimage.size
    canvas = Image.new("RGB", (lwidth, hheight+lheight))
    harea = (0, 0, hwidth, hheight)
    larea = (0, hheight, lwidth, hheight+lheight)
    canvas.paste(highimage, harea)
    canvas.paste(lowimage, larea)
    return canvas


##########################class
class gacha:
    chker_star_3 = 0

    prob_serv_5s = 0.01
    prob_serv_4s = 0.03
    prob_yej_5s = 0.04
    prob_yej_4s = 0.12

    prob_pu_serv_5s = 0.007
    prob_pu_serv_4s = 0.015
    prob_pu_yej_5s = 0.028
    prob_pu_yej_4s = 0.04

    prob_pu_serv_3s = 0.12
    prob_pu_yej_3s = 0.08

# 가챠 확률들. serv 서번트 yej 예장 pu 픽업을 의미

    def run(self, times, cl_crd):
        cl_crd.no = times
        if cl_crd.no == 9 and self.chker_star_3 == 9:
            chksum = 0
            chksum += int(self.prob_serv_5s * 100)
            chksum += int(self.prob_serv_4s * 100)
            chksum += int(self.prob_yej_5s * 100)
            chksum += int(self.prob_yej_4s * 100)
            gac = random.randrange(1, chksum)
        else:
            gac = random.randrange(1, 100)
        probsum = int(self.prob_serv_5s * 100)
        if gac <= probsum:
            #5성 뽑기 돌리기
            self.__serv_5s(cl_crd)
            return
        probsum += int(self.prob_serv_4s * 100)
        if gac <= probsum:
            #4성 뽑기 돌리기
            self.__serv_4s(cl_crd)
            return 
        probsum += int(self.prob_yej_5s * 100)
        if gac <= probsum:
            #5성 예장 뽑기 돌리기
            self.__yej_5s(cl_crd)
            return 
        probsum += int(self.prob_yej_4s * 100)
        if gac <= probsum:
            #4성 예장 뽑기 돌리기
            self.__yej_4s(cl_crd)
            return 
        else:
            self.chker_star_3 += 1
            self.__get_3s(cl_crd)
            return 
         #3성 뽑기 돌리기

    def __serv_5s(self, cl_crd):
        prob_pu = int(self.prob_pu_serv_5s / self.prob_serv_5s * 100)
        gac = random.randrange(1, 100)
        if gac <= prob_pu:
            #픽업 5성 뽑기
            i = random.randrange(0, len(serv_5s_pickup_list))
            cl_crd.fname = serv_5s_pickup_list[i-1]
            cl_crd.fpath = 's5pu'
            return
        else:
            i = random.randrange(0, len(serv_5s_list))
            cl_crd.fname = serv_5s_list[i-1]
            cl_crd.fpath = 's5'
            #픽뚫 5성 뽑기
            return

    def __serv_4s(self, cl_crd):
        prob_pu = int(self.prob_pu_serv_4s / self.prob_serv_4s * 100)
        gac = random.randrange(1, 100)
        if gac <= prob_pu:
            #픽업 4성 뽑기
            i = random.randrange(0, len(serv_4s_pickup_list))
            cl_crd.fname = serv_4s_pickup_list[i-1]
            cl_crd.fpath = 's4pu'
            return 
        else:
            #픽뚫 4성 뽑기
            i = random.randrange(0, len(serv_4s_list))
            cl_crd.fname = serv_4s_list[i-1]
            cl_crd.fpath = 's4'
            return

    def __yej_5s(self, cl_crd):
        prob_pu = int(self.prob_pu_yej_5s / self.prob_yej_5s * 100)
        gac = random.randrange(1, 100)
        if gac <= prob_pu:
            #픽업 5성 예장 뽑기
            i = random.randrange(0, len(yej_5s_pickup_list))
            cl_crd.fname = yej_5s_pickup_list[i-1]
            cl_crd.fpath = 'y5pu'
            return 
        else:
            #픽뚫 5성 예장 뽑기
            i = random.randrange(0, len(yej_5s_list))
            cl_crd.fname = yej_5s_list[i-1]
            cl_crd.fpath = 'y5'
            return

    def __yej_4s(self, cl_crd):
        prob_pu = int(self.prob_pu_yej_4s / self.prob_yej_4s * 100)
        gac = random.randrange(1, 100)
        if gac <= prob_pu:
            #픽업 4성 예장 뽑기
            i = random.randrange(0, len(yej_4s_pickup_list))
            cl_crd.fname = yej_4s_pickup_list[i-1]
            cl_crd.fpath = 'y4pu'
            return 
        else:
            #픽뚫 4성 예장 뽑기
            i = random.randrange(0, len(yej_4s_list))
            cl_crd.fname = yej_4s_list[i-1]
            cl_crd.fpath = 'y4'
            return

    def __get_3s(self, cl_crd ):
        gac = random.randrange(1, 100)
        prob_pu_yej = int(self.prob_pu_yej_3s * 100)
        prob_pu_serv = int(self.prob_pu_serv_3s * 100)
        probsum = 0
        if gac <= prob_pu_yej:
            i = random.randrange(0, len(yej_3s_pickup_list))
            cl_crd.fname = yej_3s_pickup_list[i-1]
            cl_crd.fpath = 'y3pu'
            return 
        probsum += prob_pu_yej
        if gac <= prob_pu_serv:
            i = random.randrange(0, len(serv_3s_pickup_list))
            cl_crd.fname = serv_3s_pickup_list[i-1]
            cl_crd.fpath = 's3pu'
            return 
        probsum += prob_pu_serv
        left_prob = int((100 - probsum) / 2)
        prob_yej = int(left_prob) + probsum
        if gac <= prob_yej:
            #3성 예장 뽑기
            i = random.randrange(0, len(yej_3s_list))
            cl_crd.fname = yej_3s_list[i-1]
            cl_crd.fpath = 'y3'
            return 
        else:
            #3성 서번트 뽑기
            i = random.randrange(0, len(serv_3s_list))
            cl_crd.fname = serv_3s_list[i-1]
            cl_crd.fpath = 's3'
            return

class card:
    no = 0
    fname = ''
    fpath = ''
    xpos = 0
    ypos = 0

    def fpath_convert(self):
        if self.fpath=='s3':
            self.fpath = fpath + '/img/servant_star3'
        elif self.fpath=='s4':
            self.fpath = fpath + '/img/servant_star4'
        elif self.fpath=='s5':
            self.fpath = fpath + '/img/servant_star5'
        elif self.fpath == 's3pu':
            if not_pu_3s == False:
                self.fpath = fpath + '/img/servant_star3/pickup'
            else:
                self.fpath = fpath + '/img/servant_star3'
        elif self.fpath == 's4pu':
            if not_pu_4s == False:
                self.fpath = fpath + '/img/servant_star4/pickup'
            else:
                self.fpath = fpath + '/img/servant_star4'
        elif self.fpath == 's5pu':
            self.fpath = fpath + '/img/servant_star5/pickup'
        elif self.fpath == 'y3':
            self.fpath = fpath + '/img/yejang_star3'
        elif self.fpath == 'y4':
            self.fpath = fpath + '/img/yejang_star4'
        elif self.fpath == 'y5':
            self.fpath = fpath + '/img/yejang_star5'
        elif self.fpath == 'y3pu':
            if not_pu_3y == False:
                self.fpath = fpath + '/img/yejang_star3/pickup'
            else:
                self.fpath = fpath + '/img/yejang_star3'
        elif self.fpath == 'y4pu':
            if not_pu_4y == False:
                self.fpath = fpath + '/img/yejang_star4/pickup'
            else:
                self.fpath = fpath + '/img/yejang_star4'
        elif self.fpath == 'y5pu':
            if not_pu_5y == False:
                self.fpath = fpath + '/img/yejang_star5/pickup'
            else:
                self.fpath = fpath + '/img/yejang_star5'
        else:
            return

class printer():
    def out(self, cl_crd, result_img):
        self.pos(cl_crd)
        gacha_path = os.path.join(cl_crd.fpath, cl_crd.fname)
        gacha_img = Image.open(gacha_path)
        result_img.paste(gacha_img, (cl_crd.xpos, cl_crd.ypos))
        return result_img

    def pos(self, cl_crd):
        if cl_crd.no <= 5:
            cl_crd.xpos = 35 + cl_crd.no * 98
            cl_crd.ypos = 75
        else:
            cl_crd.xpos = 133 + (cl_crd.no-6) * 98
            cl_crd.ypos = 190
#####가챠######

def gacha_simulate(args=[], np_lvl=1, star=5, option='string'):
    full_stone = 167 #최대 구매 돌의 개수
    full_stone_price = 9.32#최대 구매 돌의 가격
    if option == 'string':
        for s in args:
            if '보' in s:
                np_lvl = int(s[1:])
            elif s == '4성':
                star = 4
            elif s == '5성':
                star = 5
    num = 0
    star5_serv = 0
    star4_serv = 0
    star5_pick_serv = 0
    star4_pick_serv = 0
    ob_num = 0
    while ob_num < np_lvl:
        num = num + 1
        i = random.randrange(1,1001)
        if (i >= 0 and i <= 7):
            star5_pick_serv += 1
        elif (i >= 8 and i <= 10):
            star5_serv += 1
        elif (i >= 11 and i <= 25):
            star4_pick_serv += 1
        elif (i >= 26 and i <= 40):
            star4_serv += 1
        if star == 4:
            ob_num = star4_pick_serv
        elif star == 5:
            ob_num = star5_pick_serv
    res = ''
    price = num * 3 / full_stone * full_stone_price
    if star == 5:
        res = '5성 픽업 서번트 {0}번을 {1}회만에 뽑으셨습니다.'.format(star5_pick_serv, num)
        if (star5_serv > 0 or star4_pick_serv > 0 or star4_serv > 0):
            res += '\n그동안'
            if (star5_serv > 0):
                res += '\n5성 픽뚫 서번트는 {0}번,'.format(star5_serv)
            if (star4_pick_serv > 0):
                res += '\n4성 단독 픽업 서번트는 {0}번,'.format(star4_pick_serv)
            if (star4_serv > 0):
                res += '\n4성 픽뚫 서번트는 {0}번'.format(star4_serv)
            if (res[-1] == ','):
                res = res[:-1] + ' '
            res += ' 뽑으셨습니다.'
    elif star == 4:
        res = '4성 단독 픽업 서번트 {0}번을 {1}회만에 뽑으셨습니다.'.format(star4_pick_serv, num)
        if (star5_serv > 0 or star5_pick_serv > 0 or star4_serv > 0):
            res += '\n그동안'
            if (star5_pick_serv > 0):
                res += '\n5성 픽업 서번트는 {0}번,'.format(star5_pick_serv)
            if (star5_serv > 0):
                res += '\n5성 픽뚫 서번트는 {0}번,'.format(star5_serv)
            if (star4_serv > 0):
                res += '\n4성 픽뚫 서번트는 {0}번'.format(star4_serv)
            if (res[-1] == ','):
                res = res[:-1] + ' '
            res += ' 뽑으셨습니다.'
    res += '\n소모한 돌은 {}개({}만원)입니다.'.format(num * 3, round(price,2))
    if option == 'string':
        return res
    elif option == 'data':
        rdict = {'star5serv': star5_serv,
                 'pstar5serv': star5_pick_serv,
                 'star4serv': star4_serv,
                 'pstar4serv': star4_pick_serv,
                 'stone': num,
                 'price': round(price, 2)}
        return rdict
    return

def gacha_run(key='temp', test=False):
    if test:
        st = time.time()
    globe.prefix_str = str(now.year) + str(now.day) + str(now.minute) + str(now.second)
    key = str(key) + globe.prefix_str
    init_serv_star5()
    init_serv_star4()
    init_serv_star3()
    init_yej_star5()
    init_yej_star4()
    init_yej_star3()
    cardlist = []
    gachacl = gacha()
    printercl = printer()
    if test:
        print('Loop before:: ' + str(time.time() - st))
        st = time.time()
    result_img = Image.open(fpath + '/img/gacha_background.png')
    for i in range(10):
        cardlist.append(card())
        gachacl.run(i, cardlist[i])
        cardlist[i].fpath_convert()
        result_img = printercl.out(cardlist[i], result_img)
    canvas = result_composite(key, result_img)
    res_path = make_bg_folder(key) + '{}result.png'.format(globe.prefix_str)
    canvas.save(res_path)
    if test:
        print('Loop after:: ' + str(time.time() - st))
    return fpath + '/img/result/{0}/{1}result.png'.format(key,globe.prefix_str)

def gacha_clear(ipath=''):
    if ipath:
        folder = os.path.dirname(ipath)
        if os.path.isdir(folder):
            foldlist = os.listdir(folder)
            if '.png' in foldlist[0] and len(foldlist) == 1:
                shutil.rmtree(folder)
            return True
        else:
            return False
    else:
        flist = os.listdir(respath)
        if flist:
            for folder in flist:
                foldpath = respath + folder
                if os.path.isdir(foldpath):
                    foldlist = os.listdir(foldpath)
                    if '.png' in foldlist[0] and len(foldlist) == 1:
                        shutil.rmtree(foldpath)
            return True
        else:
            return False

###########테스팅############
#
# st = time.time()
# gacha_run('1111')
# print('function: ' + str(time.time() - st))
# print(gacha_simulate(np_lvl=5, star=4, option='data'))
# for i in range(10):
#     gacha_run('temp'+str(i))
# gacha_clear()