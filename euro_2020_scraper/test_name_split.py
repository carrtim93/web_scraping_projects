import requests
import pandas as pd
from bs4 import BeautifulSoup

source = 'https://www.uefa.com/uefaeuro-2020/teams/players/250066156--raphael-guerreiro/'
url = requests.get(source).text
soup = BeautifulSoup(url, 'lxml')

first_name = soup.find('span', attrs={'class': 'player-header__name'}).text
surname = soup.find('span', attrs={'class': 'player-header__surname'}).text

top_stats_cont = soup.find('div', attrs={'class': 'top-stats grid_4'})
top_stats = top_stats_cont.findAll('div', attrs={'class': 'statistics--list--data'})
minutes_played = top_stats[1].text
minutes_played = int(minutes_played[:-1])

if not surname:
    names = first_name.split(' ')
    if len(names) == 2:
        first_name = names[0]
        surname = names[1]
    else:
        surname = first_name
print(f'First:{first_name} Second:{surname} \nMinutes: {minutes_played}')