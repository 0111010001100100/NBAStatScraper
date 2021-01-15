import pandas as pd
import numpy as np
import random
from bs4 import BeautifulSoup, Comment
import requests

# Depending on the team, home court advantage is anywhere from 2 to 4 points.
HOME_COURT_ADVANTAGE = 3
# The weight of player performance compared to team performance.
PLAYER_SCORE_WEIGHT = 0.6
# The weight of team performance compared to player performance.
TEAM_SCORE_WEIGHT = 0.4
# 12 - 15 players dress for the games and anywhere from 8-12 play.
# 10 was chosen somewhat arbitrarily but can be played with.
MAX_PLAYERS_IN_GAME = 10
MINUTES_IN_GAME = 48.0

class Team:
    '''
    Team object for player stats from a specific year.
    Args:
        team (str): The 3 letter identifier for an NBA team. 
        year (str): The year for which the team object is built.
    Attributes:
        team (str): The 3 letter identifier for an NBA team.
        year (str): The year for which the team object is built.
        pts_for (float): Mean points `team` scored in `year`.
        pts_for_std (float): Standard deviation of points `team` scored in `year`.
        pts_against (float): Mean points scored against `team` in `year`.
        pts_against_std (float): Standard deviation of points scored against `team` in `year`.
        pts_league_avg (float): Mean points scored in `year` for entire league.
        team_stats (DataFrame): `team` scoring stats for `year`.
    '''
    def __init__(self, team, year):
        self.team = team
        self.year = year 
        self.pts_for = None
        self.pts_for_std = None
        self.pts_against = None 
        self.pts_against_std = None
        self.pts_league_avg = None
        self.team_stats = None 

        self.set_pts_for_and_against()
        self.set_pts_league_avg()
        self.set_team_stats()


    def set_pts_for_and_against(self):
        '''
        Set `pts_for`, `pts_for_std`, `pts_against`, and `pts_against_std` attributes.   
        '''
        season_results = self._scrape_helper('https://d2cwpp38twqe55.cloudfront.net/teams/{}/{}_games.html'.format(self.team, self.year), 'games')
        season_results = season_results[season_results.G != 'G']
        season_results = season_results[['Tm', 'Opp']].astype({'Tm': int, 'Opp': int})
        self.pts_for = season_results['Tm'].mean()
        self.pts_for_std = season_results['Tm'].std()
        self.pts_against = season_results['Opp'].mean()
        self.pts_against_std = season_results['Opp'].std()


    def set_pts_league_avg(self):
        '''
        Set `pts_league_avg` attribute.
        '''
        league_ppg = self._scrape_helper('https://d2cwpp38twqe55.cloudfront.net/leagues/NBA_{}.html'.format(self.year), 'all_team-stats-per_game')
        self.pts_league_avg = float(league_ppg[league_ppg['Team'] == 'League Average']['PTS'])


    def set_team_stats(self):
        '''
        Set `team_stats` attribute.
        '''
        team_stats = self._scrape_helper('https://www.basketball-reference.com/teams/{}/{}.html'.format(self.team, self.year), 'per_game')
        team_stats = team_stats.rename(columns={'Unnamed: 1':'Player'})

        # Some per-game tables have the points column as PTS and some have it as PTS/G. There doesn't seem to be a pattern for this.
        try:
            team_stats = team_stats.rename(columns={'PTS/G':'PTS'})
        finally:
            pass

        team_stats = team_stats.sort_values(by=['MP'], ascending=False)[team_stats['Rk'] <= MAX_PLAYERS_IN_GAME][['Rk', 'Player', 'MP', 'PTS']]
        team_stats['MPRatio'] = team_stats['MP'] / MINUTES_IN_GAME
        sRatio = team_stats['MPRatio'].sum()
        team_stats['MPRatioAdj'] = team_stats['MPRatio'] - ((sRatio - 5) / float(MAX_PLAYERS_IN_GAME))
        team_stats['eMP'] = team_stats['MPRatioAdj'] * MINUTES_IN_GAME
        team_stats['ePPG'] = (team_stats['PTS'] / team_stats['MP']) * team_stats['eMP']
        self.team_stats = team_stats[['Player', 'MPRatioAdj', 'eMP', 'ePPG']]


    def _scrape_helper(self, url, table_id):
        '''
        Helper function to scrape statistics from basketball-reference.com.
        Args:
            url (str): The URL to scrape data from.
            table_id (str): The HTML id of the table or div to scrape.
        Returns:
            A Pandas dataframe containing the scraped table.
        '''
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            try:
                table = soup.find('table', id=table_id)
                df = pd.read_html(str(table))[0]
            except ValueError:
                table = soup.find('div', id=table_id).find(string=lambda tag: isinstance(tag, Comment))
                df = pd.read_html(str(table))[0]
            finally:
                return df
        else:
            print("Error in request to {}".format(url))

class Matchup:
    '''
    Matchup object to model the home team against the away team.
    Args:
        home (object): Team object of the home team.
        away (object): Team object of the away team.
    Attributes:
        home_team (object): Team object of the home team.
        away_team (object): Team object of the away team.
        home_weighted_pts (int): The mean points scored by the home team calculated with weights 
                                    given to team and individual performance.
        away_weighted_pts (int): The mean points scored by the away team calculated with weights
                                    given to team and individual performance.
    '''
    def __init__(self, home, away, home_adv=HOME_COURT_ADVANTAGE):
        self.home_team = home
        self.away_team = away 
        self.home_weighted_pts = None 
        self.away_weighted_pts = None
        self.home_adv = home_adv

        self.set_weighted_pts()

    
    def get_player_pts(self):
        '''
        Get the mean player points scored.
        Returns:
            A list containing the points scored by the players for the home and away teams with HOME_COURT_ADVANTAGE 
            pointed added to the home team.
        '''
        return [self.home_team.team_stats['ePPG'].sum() * (self.away_team.pts_against / self.away_team.pts_league_avg) + self.home_adv, 
                self.away_team.team_stats['ePPG'].sum() * (self.home_team.pts_against / self.home_team.pts_league_avg)]


    def get_team_pts(self):
        '''
        Get the mean team points scored.
        Returns:
            A list containing the points scored by the teams for the home and away teams with HOME_COURT_ADVANTAGE 
            pointed added to the home team.
        '''
        return [self.home_team.pts_for * (self.away_team.pts_against / self.away_team.pts_league_avg) + self.home_adv, 
                self.away_team.pts_for * (self.home_team.pts_against / self.home_team.pts_league_avg)]
    

    def set_weighted_pts(self):
        '''
        Set the weighted points for the home and away teams.
        '''
        player_pts = self.get_player_pts()
        team_pts = self.get_team_pts()
        self.home_weighted_pts = (team_pts[0] * TEAM_SCORE_WEIGHT) + (player_pts[0] * PLAYER_SCORE_WEIGHT)
        self.away_weighted_pts = (team_pts[1] * TEAM_SCORE_WEIGHT) + (player_pts[1] * PLAYER_SCORE_WEIGHT)


class Simulation:
    '''
    Simulation object to model a matchup.
    Args:
        matchup (object): A matchup object for the head-to-head to simulate.
    Attributes:
        matchup (object): A matchup object for the head-to-head to simulate.
        home_wins (int): The number of wins for the home team.
        away_wins (int): The number of wins for the away team.
    '''
    def __init__(self, matchup):
        self.matchup = matchup 
        self.home_wins = 0
        self.away_wins = 0

    
    def simulate_single_game(self):
        '''
        Simulates a single game by sampling from 2 Gaussian distributions for points scored and opponent's points against for each of home and away teams.
        '''
        home = (random.gauss(matchup.home_weighted_pts, matchup.home_team.pts_for_std) + random.gauss(matchup.away_team.pts_against, matchup.away_team.pts_against_std))/2
        away = (random.gauss(matchup.away_weighted_pts, matchup.away_team.pts_for_std) + random.gauss(matchup.home_team.pts_against, matchup.home_team.pts_against_std))/2
        if home > away:
            self.home_wins += 1
        else:
            self.away_wins += 1
    

    def simulate_matchup(self, n):
        '''
        Repeatedly simulates single games.
        Args:
            n (int): The number of games to simulate.
        '''
        for i in range(n):
            self.simulate_single_game()
        self.print_results(n)

    
    def print_results(self, n):
        '''
        Prints the results of the simulation.
        Args:
            n (int): The number of games that were simulated. 
        '''
        print("Simulated {} games...".format(n))
        print("{} won {}% of the games as the home team.".format(self.matchup.home_team.team, self.home_wins / float(n) * 100))
        print("{} won {}% of the games as the away team.".format(self.matchup.away_team.team, self.away_wins / float(n) * 100))


############
# Examples #
############

# Simulate 2019 finals game with Toronto Raptors at home
tor = Team('TOR', '2019')
gsw = Team('GSW', '2019')
matchup = Matchup(tor, gsw)
s = Simulation(matchup)
s.simulate_matchup(100000)

# Simulate Toronto Raptors 2019 championship team at home against LA Lakers 2020 championship team
lal = Team('LAL', '2020')
matchup = Matchup(tor, lal)
s = Simulation(matchup)
s.simulate_matchup(100000)

# Simulate Toronto Raptors 2019 championship team LA Lakers 2020 championship team with no home court advantage
matchup = Matchup(tor, lal, 0)
s = Simulation(matchup)
s.simulate_matchup(100000)
