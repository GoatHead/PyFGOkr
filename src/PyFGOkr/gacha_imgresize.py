import os
from PIL import Image

def resize(path, flist):
    for file in flist:
        if '.png' in file:
            fpath = path + file
            gacha_img = Image.open(fpath)
            gacha_img = gacha_img.resize((int(75 * 1.24), int(82 * 1.24)))
            print('resize saved: {}'.format(fpath))
            gacha_img.save(fpath)
        else:
            ppath = path + file + '/'
            plist = os.listdir(ppath)
            if plist:
                return resize(ppath, plist)

def __init__():
    fpath = os.path.dirname(__file__)
    img_path = fpath + '/img/'
    path_list = [img_path + 'servant_star3/',
                 img_path + 'servant_star4/',
                 img_path + 'servant_star5/',
                 img_path + 'yejang_star3/',
                 img_path + 'yejang_star4/',
                 img_path + 'yejang_star5/']
    for path in path_list:
        flist = os.listdir(path)
        resize(path, flist)
    highimage_path = img_path + 'now_pickup.png'
    lowimage_path = img_path + 'gacha_background.png'
    highimage = Image.open(highimage_path)
    lowimage = Image.open(lowimage_path)
    hwidth, hheight = highimage.size
    lwidth, lheight = lowimage.size
    highimage = highimage.resize((int(lwidth / hwidth * hwidth), int(lwidth / hwidth * hheight)))
    highimage.save(highimage_path)

__init__()