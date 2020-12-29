import pandas as pd
from bs4 import BeautifulSoup, Comment
import requests


def get_roster(team, year):
    response = requests.get('https://www.basketball-reference.com/teams/{}/{}.html'.format(team, year))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        roster = soup.find('table')
        roster = pd.read_html(str(roster))[0]
        roster.columns = ['Number', 'Name', 'Pos', 'Height', 'Weight', 
                          'Birthday', 'Nationality', 'YearsExp', 'College']
        roster['YearsExp'] = roster['YearsExp'].replace('R', '0')
        roster['YearsExp'] = roster['YearsExp'].astype(int)
        roster['Birthday'] = roster['Birthday'].apply(lambda x: pd.to_datetime(x))
        roster['Nationality'] = roster['Nationality'].str.upper()
        # Need to fix if missing values are important
        roster['College'] = roster['College'].fillna('BallSoHardU')
    else:
        return "Error getting roster for {} in year {}".format(team, year)
    return roster

def get_player_stats(team, year, per):
    # per can be game, total, 36min, 100pos, shooting, playoffTotal, playoffGame, 
    # playoff36min, playoff100pos, playoffShooting
    per_dict = {'game': 'per_game', 'total': 'all_totals', '36min': 'all_per_minute', 
                '100pos': 'all_per_poss', 'shooting': 'all_shooting', 'playoffTotal': 'all_playoffs_totals', 
                'playoff_game': 'playoffs_per_game', 'playoff36min': 'all_playoffs_per_minute', 
                'playoff100pos': 'all_playoffs_per_poss', 'playoffShooting': 'all_playoffs_shooting'}
    response = requests.get('https://www.basketball-reference.com/teams/{}/{}.html'.format(team, year))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        if per in ['game', 'playoff_game']:
            player_stats = soup.find('table', id=per_dict[per])
        else:
            player_stats = soup.find('div', id=per_dict[per]).find(string=lambda tag: isinstance(tag, Comment))
        player_stats = pd.read_html(str(player_stats))[0]
        # May need to do something with the column names
        # player_stats.columns = ['Rank', 'Name', 'Age', ]
    else:
        return "Error getting {} stats for {} in year {}.".format(per, team, year)
    return player_stats

def main():
    # get_roster('TOR', '2019')
    print(get_player_stats('TOR', '2019', 'total'))


if __name__ == '__main__':
    # For debugging
    pd.set_option('display.max_columns', None)
    main()
