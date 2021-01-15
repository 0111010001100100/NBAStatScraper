import pandas as pd
from bs4 import BeautifulSoup, Comment
import requests


def get_roster(team, year):
    '''
    Scrape the roster of a team from a given year.
        Parameters:
            team (string): The 3 letter abbreviation of a team (e.g. 'BOS')
            year (string): The roster year (e.g. '2005')
        Returns:
            A Pandas dataframe containing the roster.
    '''
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

def get_team_stats(team, year, per):
    '''
    Scrape the team stats for each player for a given year.
        Parameters:
            team (string): The 3 letter abbreviation of a team (e.g. 'TOR')
            year (string): The year to get the team stats for (e.g. '2009')
            per (string): The method in which the statistics are calculated. Can be any one of:
                ['game', 'total', 'min', 'pos', 'shooting', 'playoffTotal', 'playoffGame', 'playoffMin', 
                'playoffPos', 'playoffShooting']
        Returns:
            A Pandas dataframe containing the team stats.
    note::
        I think this may be redundant because players does the same thing just not aggregated by team. 
    '''
    per_dict = {'game': 'per_game', 'total': 'all_totals', 'min': 'all_per_minute', 
                'pos': 'all_per_poss', 'shooting': 'all_shooting', 'playoffTotal': 'all_playoffs_totals', 
                'playoffGame': 'playoffs_per_game', 'playoffMin': 'all_playoffs_per_minute', 
                'playoffPos': 'all_playoffs_per_poss', 'playoffShooting': 'all_playoffs_shooting'}
    response = requests.get('https://www.basketball-reference.com/teams/{}/{}.html'.format(team, year))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        if per in ['game', 'playoffGame']:
            player_stats = soup.find('table', id=per_dict[per])
        else:
            player_stats = soup.find('div', id=per_dict[per]).find(string=lambda tag: isinstance(tag, Comment))
        player_stats = pd.read_html(str(player_stats))[0]
        if per in ['shooting', 'playoffShooting']:
            player_stats.columns = player_stats.columns.droplevel()
            player_stats = player_stats.rename(columns={'Unnamed: 1_level_1':'Player'})
        player_stats = player_stats.rename(columns={'Unnamed: 1':'Player'})
        player_stats = player_stats.drop(player_stats.columns[player_stats.columns.str.contains('unnamed',case = False)],axis = 1)
        try:
            player_stats = player_stats.rename(columns={'PTS/G':'PTS'})
        finally:
            pass
    else:
        return "Error getting {} stats for {} in year {}.".format(per, team, year)
    return player_stats

def get_team_stats_per_game(team):
    '''
    Scrape the per game team stats for each year.
        Parameters:
            team (string): The 3 letter abbreviation of a team (e.g. 'TOR')
        Returns:
            A Pandas dataframe containing the per game team stats.
    '''
    response = requests.get('https://d2cwpp38twqe55.cloudfront.net/teams/{}/stats_basic_totals.html'.format(team))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        team_stats = soup.find('table', id='stats')
        team_stats = pd.read_html(str(team_stats))[0]
        team_stats = team_stats.dropna(how='all', axis='columns')
        team_stats = team_stats.fillna(0)
        team_stats = team_stats[team_stats.Season != 'Season']
    else:
        return "Error getting stats for {}".format(team)
    return team_stats

def get_league_avg_ppg(year):
    response = requests.get('https://d2cwpp38twqe55.cloudfront.net/leagues/NBA_{}.html'.format(year))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        league_ppg = soup.find('div', id='all_team-stats-per_game').find(string=lambda tag: isinstance(tag, Comment))
        league_ppg = pd.read_html(str(league_ppg))[0]
    else:
        return "Error getting league avg points per game for {}.".format(year)
    return float(league_ppg[league_ppg['Team'] == 'League Average']['PTS'])

# print(get_team_stats('BOS', '2019', 'shooting'))
print(get_league_avg_ppg('2019'))