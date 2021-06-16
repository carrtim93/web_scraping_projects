import requests
import pandas as pd
from bs4 import BeautifulSoup

url_root = 'https://www.uefa.com'


def get_country_urls():
    """
    Scrape the url for each country's squad pageto be used to get
    the urls for each individual player
    :return: list of country urls
    """
    source = requests.get('https://www.uefa.com/uefaeuro-2020/teams/').text
    url_list = []
    soup = BeautifulSoup(source, 'lxml')

    for d in soup.findAll('div', attrs={'team team-is-team'}):
        country_url = d.find('a', attrs={'class': 'team-wrap'})['href']
        url_list.append(url_root + country_url + 'squad/')
    return url_list


def get_player_urls(country_url):
    """
    Scrape the url for each player from a coutnry squad page
    :param country_url:
    :return: list of player urls
    """
    source = requests.get(country_url).text
    soup = BeautifulSoup(source, 'lxml')
    player_url_list = []

    for a in soup.findAll('a', attrs={'class': 'player-name'}):
        player_url = url_root + a['href']
        player_url_list.append(player_url)

    return player_url_list


def get_player_stats(source):
    """
    Scrape individual player information and return each stat in a list
    :param source:
    :return: list of players' stats
    """
    url = requests.get(source).text

    soup = BeautifulSoup(url, 'lxml')

    first_name = soup.find('span', attrs={'class': 'player-header__name'}).text
    surname = soup.find('span', attrs={'class': 'player-header__surname'}).text

    # if they have two names in first name but none in surname, split names
    # if there is only one name, make it both first name and surname
    if not surname:
        names = first_name.split(' ')
        if len(names) == 2:
            first_name = names[0]
            surname = names[1]
        else:
            surname = first_name
    country = soup.find('span', attrs={'class': 'team-name__country-code'}).text
    pos = soup.find('span', attrs={'class': 'player-header_category'}).text
    profile_data = soup.findAll('span', attrs={'class': 'player-profile__data'})
    club = profile_data[0].text
    age = profile_data[1].text
    squad_num = profile_data[2].text
    top_stats_cont = soup.find('div', attrs={'class': 'top-stats grid_4'})
    # if a player has not played a game there will be no stats here
    # if this is the case, set the remaining stats to 0
    if top_stats_cont is not None:
        top_stats = top_stats_cont.findAll('div', attrs={'class': 'statistics--list--data'})
        matches_played = top_stats[0].text
        minutes_played = top_stats[1].text
        # change minutes from str to int
        minutes_played = int(minutes_played[:-1])
        # goalkeepers have a goals conceded stat instead of goals
        if pos == 'Goalkeeper':
            goals = 0
            goals_conceded = top_stats[2].text
        else:
            goals = top_stats[2].text
            goals_conceded = 0
        cards = top_stats_cont.find('span', attrs={'class', 'statistics--list--data'}).text.strip()
        y_cards = cards[0]
        r_cards = cards[-1]
    else:
        matches_played = 0
        minutes_played = 0
        goals = 0
        goals_conceded = 0
        y_cards = 0
        r_cards = 0

    stats = [surname, first_name, country, pos, club, age, squad_num, matches_played,
             minutes_played, goals, goals_conceded, y_cards, r_cards]

    return stats


if __name__ == "__main__":
    all_player_stats = []
    country_url_list = get_country_urls()
    for c in country_url_list:
        player_url_list = get_player_urls(c)
        for player in player_url_list:
            player_stats = get_player_stats(player)
            all_player_stats.append(player_stats)

    df = pd.DataFrame.from_records(all_player_stats, columns=['Surname', 'Name', 'Country', 'Position', 'Club', 'Age',
                                                              'SquadNo', 'Games Played', 'MinsPlayed', 'Goals',
                                                              'GoalsConceded', 'YCards', 'RCards'])
    df.to_csv('euro_2020_players_xtra_stats.csv', index=False, encoding='utf-8')


