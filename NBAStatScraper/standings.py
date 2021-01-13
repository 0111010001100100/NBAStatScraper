import pandas as pd
from bs4 import BeautifulSoup, Comment
import requests
from requests_html import HTMLSession  
import pyppdf.patch_pyppeteer


def get_division_standings(conference, year):
	'''
	Scrape the division standings for a given year.
		Parameters:
			conference (string): The conference to get the division standings of. Can be either 'W' or 'E'.
			year (string): The year to get the standings of (e.g. '2020')
		Returns: 
			A Pandas dataframe containing the division standings.
	'''
	response = requests.get('https://www.basketball-reference.com/leagues/NBA_{}_standings.html'.format(year))
	if response.status_code == 200:
		soup = BeautifulSoup(response.content, 'lxml')
		standings = soup.find('table', id='divs_standings_{}'.format(conference.upper()))
		standings = pd.read_html(str(standings), header=1)[0]
	else:
		return "Error getting {} division standings for {}".format(conference.upper(), year)
	return standings

def get_conference_standings(conference, year):
	'''
	Scrape the conference standings for a given year.
		Parameters:
			conference (string): The conference to get the division standings of. Can be either 'W' or 'E'.
			year (string): The year to get the standings of (e.g. '2020')
		Returns:
			A Pandas dataframe containing the conference standings.
	note::
		The conference standings are not available on the website for each year. To get conference standings, 
		get_division_standings can be used. Must be for 2016 or later.
	'''
	if int(year) < 2016:
		return "Error: Conference standings are only available for 2016 or later. Please use division standings for earlier years."
	response = requests.get('https://www.basketball-reference.com/leagues/NBA_{}_standings.html'.format(year))
	if response.status_code == 200:
		soup = BeautifulSoup(response.content, 'lxml')
		standings = soup.find('table', id='confs_standings_{}'.format(conference.upper()))
		standings = pd.read_html(str(standings))[0]
	else:
		return "Error getting {} conference standings for {}".format(conference.upper(), year)
	return standings

def get_league_standings(year):
	'''
	Scrape the league standings for a given year.
		Parameters:
			year (string): The year to get the standings of (e.g. '2020')
		Returns:
			A Pandas dataframe containing the league standings.
	'''
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
	'''
	Scrape the team vs. team records for a given year.
		Parameters:
			year (string): The year to get the team vs. team records of (e.g. '2002')
		Returns:
			A Pandas dataframe containing the team vs. team records.
	'''
	response = requests.get('https://www.basketball-reference.com/leagues/NBA_{}_standings.html'.format(year))
	if response.status_code == 200:
		soup = BeautifulSoup(response.content, 'lxml')
		standings = soup.find('div', id='all_team_vs_team').find(string=lambda tag: isinstance(tag, Comment))
		standings = pd.read_html(str(standings))[0]
	else:
		return "Error getting league standings for year {}.".format(year)
	return standings