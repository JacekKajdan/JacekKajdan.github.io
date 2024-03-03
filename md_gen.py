import requests
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import os
import pandas as pd
from duckduckgo_search import DDGS

#Pobieranie strony
page_url = 'https://pl.wikipedia.org/wiki/Ekstraklasa_w_pi%C5%82ce_no%C5%BCnej_(2023/2024)'
page = requests.get(page_url)
	
soup = BeautifulSoup(page.content, 'html.parser')


#Zbieranie danych o drużynach
l = soup.find_all('a',{'href':re.compile('/wiki/')})

teams=[]
links=[]
beg='https://pl.wikipedia.org'
for i in range(1013,1031):
    j=9
    while str(l[i])[j]!='\"':
        j+=1
    links.append(beg+str(l[i])[9:j])
    teams.append(l[i].string)


#Zbieranie zdjęć
photos=[]

for team in teams:
    
    photo = DDGS().images(
        keywords=f'\"herb {team}\"',
        region="pl-pl",
        safesearch="off",
        size='small',
        color=None,
        type_image='transparent',
        layout=None,
        license_image=None,
        max_results=1,
    )
    photos.append(next(photo)['thumbnail'])


#Tworzenie nazw podstron
sites=[]
for x in teams:
    space=0
    while space < len(x) and x[space]!=' ':
        space+=1
    sites.append(unidecode(x[0:space]+x[space+1:]))


#Tworzenie strony głównej
my_web='https://jacekkajdan.github.io/'
md_str="# Drużyny polskiej ekstraklasy 2023/2034\n\n"

for i in range(len(teams)):
    md_str+=f'## {teams[i]}\n\n [Wikipedia]({links[i]})\n\n ![Zdjęcie]({photos[i]})\n\n [Newsy]({my_web+sites[i]})\n\n'

with open("ekstraklasa.md", "w") as text_file:
    text_file.write(md_str)


#Tworzenie podstron
for i in range(len(teams)):
    os.mkdir(sites[i])
    results = DDGS().news(teams[i]+ ' piłka nożna', max_results=5,region='pl-pl')
    news_str=f'# Wiadomości o klubie {teams[i]}\n\n'
    for news in results:
        news_str += f'{pd.to_datetime(news["date"]).strftime("%d/%m/%Y  %H:%M")} \n\n## {news["title"]} \n\n{news["body"]} \n\n[Link do całego artykułu]({news["url"]}) \n\n![Zdjęcie]({news["image"]}) \n\n'
        
    with open(f"{sites[i]}/index.md", "w") as text_file:
        text_file.write(news_str)
