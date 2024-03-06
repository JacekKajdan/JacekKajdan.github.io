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
for i in range(1039,1056):
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

os.mkdir('ekstraklasa')

gpt_text = '''
# Dlaczego Ekstraklasa to najlepsza liga na świecie?
~~Stwierdzenie, że Ekstraklasa jest najlepszą ligą na świecie, jest kwestią subiektywną i zależy od wielu czynników oraz punktu widzenia~~ 
Niemniej jednak, można podać kilka argumentów, które mogłyby uzasadniać takie stwierdzenie dla osób kibicujących polskiej piłce nożnej:

1. Pasja i zaangażowanie kibiców: Polska ma bogatą tradycję w piłce nożnej, a kibice są znani z ogromnego zaangażowania i oddania swoim klubom. Atmosfera na stadionach podczas meczów Ekstraklasy może być niesamowicie elektryzująca i pasjonująca.

2. Rywalizacja: Ekstraklasa jest pełna zaciętej rywalizacji między różnymi klubami. Historia międzyklubowych pojedynków, jak również walka o mistrzostwo, utrzymanie lub awans, sprawiają, że każdy sezon jest ekscytujący.

3. Rozwój talentów: Ekstraklasa jest także areną, na której młodzi gracze mają szansę rozwijać swoje umiejętności i zdobywać doświadczenie. Niektórzy z tych graczy mogą potem przenieść się ~~do silniejszych lig europejskich.~~

4. Dynamika gry: Styl gry w Ekstraklasie może być bardzo dynamiczny i intensywny, co przyciąga wielu fanów futbolu.

5. Potencjał rozwoju: Mimo że Ekstraklasa ~~nie~~ jest obecnie uważana za jedną z najmocniejszych lig europejskich, istnieje potencjał do dalszego rozwoju, zarówno pod względem jakości gry, jak i popularności.

Mimo tych argumentów, trzeba również zauważyć, że inne ligi, takie jak angielska Premier League, hiszpańska La Liga czy niemiecka Bundesliga, również mają swoje unikalne cechy i argumenty, ~~które mogłyby uzasadniać ich uznania za najlepsze na świecie. Ostatecznie, to kwestia osobistych preferencji i doświadczeń kibiców.~~

~ChatGPT
'''

gpt_text +=f'\n\n## [Lista drużyn ekstraklasy]({my_web}ekstraklasa/lista_ekstraklasa)'

with open("ekstraklasa/index.md", "w") as text_file:
    text_file.write(gpt_text)

os.mkdir('ekstraklasa/lista_ekstraklasa/')

with open("ekstraklasa/lista_ekstraklasa/index.md", "w") as text_file:
    text_file.write(md_str)


#Tworzenie podstron
for i in range(len(teams)):
    os.mkdir('ekstraklasa/lista_ekstraklasa/'+sites[i])
    results = DDGS().news(teams[i]+ ' piłka nożna', max_results=5,region='pl-pl')
    news_str=f'# Wiadomości o klubie {teams[i]}\n\n'
    for news in results:
        news_str += f'{pd.to_datetime(news["date"]).strftime("%d/%m/%Y  %H:%M")} \n\n## {news["title"]} \n\n{news["body"]} \n\n[Link do całego artykułu]({news["url"]}) \n\n![Zdjęcie]({news["image"]}) \n\n'
    
    news_str+=f'[Powrót do listy]({my_web}ekstraklasa/lista_ekstraklasa)'
    with open(f"ekstraklasa/lista_ekstraklasa/{sites[i]}/index.md", "w") as text_file:
        text_file.write(news_str)
