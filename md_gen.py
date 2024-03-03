import requests
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import os
 
page_url = 'https://pl.wikipedia.org/wiki/Ekstraklasa_w_pi%C5%82ce_no%C5%BCnej_(2023/2024)'
page = requests.get(page_url)
	
soup = BeautifulSoup(page.content, 'html.parser')
 
#print(soup.prettify)
def fun(tag):
    return tag.has_attr('a href')


l = soup.find_all('a',{'href':re.compile('/wiki/')})#,'title': re.compile('(piłka nożna)')

for x in range(len(l)):
    print(f'-----{x}')
    print(l[x].string)
    #print(x,end='\n')

#print(l)

teams=[]
links=[]
#/wiki/Zag%C5%82%C4%99bie_Lubin_(pi%C5%82ka_no%C5%BCna)
beg='https://pl.wikipedia.org'
for i in range(1013,1031):
    #if l[i].string not in teams and len(l[i].string)>3:
    j=9
    while str(l[i])[j]!='\"':
        j+=1
    links.append(beg+str(l[i])[9:j])
    print(str(l[i]))
    print(type(l[i]))
    teams.append(l[i].string)
        
print(teams)
print(links)

from duckduckgo_search import DDGS

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
    for x in photo:
        print(x)
        photos.append(x['thumbnail'])
        break

my_web='https://jacekkajdan.github.io/'
pol_zn={'Ł':'L','ł':'l','ę':'e','ą':'a','ó':'o','ś':'s','Ś':'S','ś':'s','ń':'n','ć':'c','c':'c'}
pz=[]
sites=[]
for x in teams:
    space=0
    while space < len(x) and x[space]!=' ':
        space+=1
    sites.append(unidecode(x[0:space]+x[space+1:]))
print(sites)



md_str="# Drużyny polskiej ekstraklasy 2023/2034\n\n"

for i in range(len(teams)):
    md_str+=f'## {teams[i]}\n\n [Wikipedia]({links[i]})\n\n ![Zdjęcie]({photos[i]})\n\n [Newsy]({my_web+sites[i]})\n\n'
print(md_str)





with open("strona.md", "w") as text_file:
    text_file.write(md_str)

for i in range(len(teams)):
    try:
        os.mkdir(sites[i])
    except Exception:
        pass
    results = DDGS().news(teams[i]+ ' piłka nożna', max_results=5,region='pl-pl')
    news_str=f'# Wiadomości o klubie {teams[i]}\n\n'
    for news in results:
        news_str += f'{news["date"]} \n\n ## {news["title"]} \n\n {news["body"]} \n\n [Link do całego artykułu]({news["url"]}) \n\n ![Zdjęcie]({news["image"]}) \n\n'
        
    with open(f"{sites[i]}/index.md", "w") as text_file:
        text_file.write(news_str)

#![Alt text](https://darmowa-kasa.pl/wp-content/uploads/2015/12/Lech-Poznan-logo.png "a title")