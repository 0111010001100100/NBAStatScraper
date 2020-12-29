import pandas as pd
from bs4 import BeautifulSoup, Comment
import requests
from requests_html import HTMLSession  
import pyppdf.patch_pyppeteer

def get_conference_standings(conference, year):
	response = requests.get('https://www.basketball-reference.com/leagues/NBA_{}_standings.html'.format(year))
	if response.status_code == 200:
		soup = BeautifulSoup(response.content, 'lxml')
		standings = soup.find('table', id='confs_standings_{}'.format(conference.upper()))
		standings = pd.read_html(str(standings))[0]
	else:
		return "Error getting {} conference standings for {}".format(conference.upper(), year)
	return standings

def get_league_standings(year):
	response = requests.get('https://www.basketball-reference.com/leagues/NBA_{}_standings.html'.format(year))
	if response.status_code == 200:
		soup = BeautifulSoup(response.content, 'lxml')
		standings = soup.find('div', id='all_expanded_standings').find(string=lambda tag: isinstance(tag, Comment))
		standings = pd.read_html(str(standings))[0]
		standings.columns = standings.columns.droplevel()
	else:
		return "Error getting league standings for year {}.".format(year)
	return standings

def get_team_v_team(year):
	response = requests.get('https://www.basketball-reference.com/leagues/NBA_{}_standings.html'.format(year))
	if response.status_code == 200:
		soup = BeautifulSoup(response.content, 'lxml')
		standings = soup.find('div', id='all_team_vs_team').find(string=lambda tag: isinstance(tag, Comment))
		standings = pd.read_html(str(standings))[0]
	else:
		return "Error getting league standings for year {}.".format(year)
	return standings