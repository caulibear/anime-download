import os
import csv
import urllib
from urllib import request
from urllib.parse import unquote


def safe(name):
    forbid = [':', '\\', '/', '<', '>', '?', '|', '*', '"']
    for  x in forbid:
        name = name.replace(x, '')
    return name


def findFile(cat, id, ep, dir):
    r = urllib.request.urlopen(f'https://www.otaku-attitude.net/launch-download-{cat}-{id}-ddl-{ep}.html')
    fileURL = r.geturl()
    fileName = unquote(fileURL)
    if ']_' in fileName:
        fileName = fileName.split(']_', 1)[1]
    elif ']' in fileName:
        fileName = fileName.split(']', 1)[1]
    fileName = safe(fileName)
    filePath = os.path.join(dir, fileName)
    request.urlretrieve(fileURL, filePath)


def makeDir(title):
    path = os.path.join(os.getcwd(), title)
    if os.path.exists(path) == False:
        os.mkdir(path)
    return path


def checkCsv(url):
    with open('otaku.csv', 'r', encoding='utf-8') as csvFile:
        reader = csv.reader(csvFile)
        if 'fiche-anime' in url:
            cat = '1'
        elif 'fiche-drama' in url:
            cat = '2'
        elif 'fiche-film' in url:
            cat = '3'
        for line in reader:
            csvUrl = line[2]
            if csvUrl.split('/', 3)[3] in url:
                eps = line[1]
                epsMax = eps.split('/')[0]
                eps = int(epsMax) + 1
                id = csvUrl.split('-')[3]
                dirName = csvUrl.split('-', 4)[4].replace('.html', '')
                madeDir = makeDir(dirName)
                count = 1
                for episode in range(1, eps+5):
                    try:
                        findFile(cat, id, episode, madeDir)
                        print(f'Downloaded {count}/{epsMax}')
                        count+=1
                    except:
                        continue
                break


while True:
    url = input('URL: ')
    checkCsv(url)
    q = input('Download more? y/n ')
    if q != 'y':
        break
