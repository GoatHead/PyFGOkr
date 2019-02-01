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

def queryconvertforweb(text):
    result = ''
    for i in range(len(text)):
        if isKoreanChar(text[i]):
            result = result + text[i]
        else:
            result = result + urllib.parse.quote(text[i])
    return result