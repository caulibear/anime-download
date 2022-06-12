from string import ascii_uppercase
import csv
import requests
from bs4 import BeautifulSoup

ascii_uppercase = '-' + ascii_uppercase
l = ['animes', 'dramas', 'films']

with open('otaku.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',')
    for liste in l:
        for lettre in ascii_uppercase:
            for scroll in range(3):
                r = requests.get(f'https://www.otaku-attitude.net/liste-dl-{liste}.php?lettre={lettre}&scroll={scroll}')
                s = BeautifulSoup(r.text, 'lxml')
                aTags = s.find_all('a')
                if len(aTags) > 0:
                    for a in aTags:
                        link = f'https://otaku-attitude.net/{a["href"]}'
                        title = a.find('strong').text
                        field = a.find_all('div', class_='field')[1].text
                        eps = field.rsplit(' ', 2)[1].strip()
                        if 'cours' in eps:
                            eps = field.rsplit(' ', 3)
                            eps = f'{eps[1]} {eps[2]}'
                        writer.writerow([title,eps,link])
                else:
                    break
