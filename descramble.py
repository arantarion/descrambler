import re
import string
import requests
from lxml import html
import sys
from beautifultable import BeautifulTable

def RemoveFromList(thelist, val):
    return [value for value in thelist if value != val]

def GetDic():
    try:
        dicopen = open("german.dic", "r", encoding='ansi')
        dicraw = dicopen.read()
        dicopen.close()
        diclist = dicraw.split("\n")
        diclist = RemoveFromList(diclist, '')
        diclist = list(set([s.lower() for s in diclist]))
        return diclist
    except FileNotFoundError:
        print("No Dictionary!")
        return 
    
def Word2Vect(word):
    l = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ü','ä','ö']
    v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    w = word.lower()
    wl = list(w)
    for i in range(0, len(wl)):
        if wl[i] in l:
            ind = l.index(wl[i])
            v[ind] += 1
    return v

def Vect2Int(vect):
    pv = 0
    f = 0
    for i in range(0, len(vect)):
        wip = (vect[i]*(2**pv))
        f += wip
        pv += 4
    return f
    
def Ints2Dic(dic):
    d = {}
    for i in range(0, len(dic)):
        v = Word2Vect(dic[i])
        Int = Vect2Int(v)
        if Int in d:
            tat = d.get(Int)
            tat.append(dic[i])
            d[Int] = tat
        elif Int not in d:
            d[Int] = [dic[i]]
    return d


def readURL(url):
    page_html = requests.get(url)
    tree = html.fromstring(page_html.content)
    text = tree.xpath('//p[@class="text text-blurred"]/text()')
    text = "".join(text).replace("\n", "")
    return text.split()

@profile
def main():
    d = GetDic()
    ind = Ints2Dic(d)

    #url = sys.argv[1]
    url = "https://www.aachener-zeitung.de/lokales/aachen/mayersche-buchhandlung-macht-platz-fuer-das-kaffeehaus_aid-63538467"
    src = readURL(url)

    pattern = re.compile('[\W_]+')
    scr = [pattern.sub('', word) for word in src]
    scr = [x for x in scr if x]

    table = BeautifulTable()
    table.column_headers = ["Scrambled", "Descrambled"]

    for s in scr:
        if s.isdigit():
            table.append_row([s, s])
            continue

        v = Vect2Int(Word2Vect(s))
        tp = ind.get(v, 'Word Not in Dictionary.')
        if tp == 'Word Not in Dictionary.':
            table.append_row([s, s])
        else:
            tp = [item for item in tp if len(item) == len(s)]
            table.append_row([s, tp])

    #with open("Ergebnis.txt", "w") as f:
    #    f.write(table)
    print(table)

if __name__ == "__main__":
    main()