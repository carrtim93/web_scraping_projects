import requests
import pandas as pd
from bs4 import BeautifulSoup

url = requests.get('https://www.uefa.com/uefaeuro-2020/teams/8--austria/squad/').text
url_root = 'https://www.uefa.com'

def get_team_urls():
    source = requests.get('https://www.uefa.com/uefaeuro-2020/teams/').text
    url_list = []
    soup = BeautifulSoup(source, 'lxml')

    for d in soup.findAll('div', attrs={'team team-is-team'}):
        country_url = d.find('a', attrs={'class': 'team-wrap'})['href']
        url_list.append(country_url)
    return url_list


def get_data(source):
    url = requests.get(source).text
    soup = BeautifulSoup(url, 'lxml')

    all_data = []
    country = soup.find('h1', attrs={'class': 'team-name desktop'}).text
    for c in soup.findAll('div', attrs={'class': 'squad--team-wrap'})[0:4]:
        # first get the position name
        pos_name = c.find('h5').text[:-1]

        for player_cont in c.findAll('tr')[1:]:
            # now find players in list
            atts = player_cont.findAll('td')
            player_name = atts[0].find('a', attrs={'class': 'player-name'}).text.strip()[:-6]
            age = atts[1].text
            games_played = atts[2].text
            goals = atts[3].text
            if games_played == '-':
                games_played = 0
            if goals == '-':
                goals = 0
            all_data.append([player_name, country, pos_name, age, games_played, goals])
    return all_data


url_list = get_team_urls()
url_list = [url_root + url + 'squad/' for url in url_list]
print(url_list)

data = []
for url in url_list:
    data.extend(get_data(url))
df = pd.DataFrame.from_records(data, columns=['Name', 'Country', 'Position', 'Age', 'Games Played', 'Goals'])
df.to_csv('euro_2020_players.csv', index=False, encoding='utf-8')


