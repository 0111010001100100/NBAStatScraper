import pandas as pd
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession  
import pyppdf.patch_pyppeteer

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_team_season_results(team, year):
	'''
	Get the information for each game of a team in a given year.
		Parameters:
			team (string): The 3 letter abbreviation of a team (e.g. 'TOR', 'BOS')
			year (string): The year of the season to get the game scores for.
		Returns:
			A Pandas dataframe containing the information of each game for the team in the given year.	
	'''
	response = requests.get('https://d2cwpp38twqe55.cloudfront.net/teams/{}/{}_games.html'.format(team, year))
	if response.status_code == 200:
		soup = BeautifulSoup(response.content, 'lxml')
		season_results = soup.find('table', id='games')
		season_results = pd.read_html(str(season_results))[0]
		season_results = season_results[season_results.G != 'G']
		season_results = season_results.drop(season_results.columns[season_results.columns.str.contains('Unnamed',case = False)],axis = 1)
	else:
		return "Error getting {} results in year {}".format(team, year)
	return season_results

def get_team_playoff_results(team, year):
	'''
	Get the information for each playoff game of a team in a given year.
		Parameters:
			team (string): The 3 letter abbreviation of a team (e.g. 'TOR', 'BOS')
			year (string): The year of the season to get the playoff game scores for.
		Returns:
			A Pandas dataframe containing the information of each playoff game for the team in the given year.	
	'''
	response = requests.get('https://d2cwpp38twqe55.cloudfront.net/teams/{}/{}_games.html'.format(team, year))
	if response.status_code == 200:
		soup = BeautifulSoup(response.content, 'lxml')
		season_results = soup.find('table', id='games_playoffs')
		season_results = pd.read_html(str(season_results))[0]
		season_results = season_results[season_results.G != 'G']
		season_results = season_results.drop(season_results.columns[season_results.columns.str.contains('Unnamed',case = False)],axis = 1)
	else:
		return "Error getting {} results in year {}".format(team, year)
	return season_results

def render_JS(URL):
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--disable-gpu")
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
	# driver = webdriver.Chrome()
	driver.get(URL)
	return driver.page_source

# # ## Exploded for some reason
# def render_JS(URL):
# 	'''
# 	Render javascript on the page so the table can be parsed.
# 		Parameters:
# 			URL (string): The site URL to render
# 		Returns:
# 			The raw HTML that was rendered. 
# 	note::
# 		This is only needed in some cases. 
# 	'''
# 	session = HTMLSession()
# 	r = session.get(URL)
# 	r.html.render(timeout=60)
# 	return r.html.html

def get_date_suffix(date):
	'''
	Convert datetime type to website URL format.
		Parameters:
			date (string): (e.g. '2020-12-23')
		Returns:
			The date website suffix (e.g. '202012230')
	'''
	date = pd.to_datetime(date)
	if (len(str(date.month)) == 1) and (len(str(date.day)) == 1) :
		return str(date.year) + '0' + str(date.month) + '0' + str(date.day) + '0'
	if (len(str(date.month)) == 1):
		return str(date.year) + '0' + str(date.month) + str(date.day) + '0'
	if (len(str(date.day)) == 1) :
		return str(date.year) + str(date.month) + '0' + str(date.day) + '0'
	return str(date.year) + str(date.month) + str(date.day) + '0'

def get_locations(style):
	'''
	Transform the shot locations from pixels to feet.
		Parameters:
			style (string): The css style for positioning shot locations in pixels (scraped from site).
		Returns:
			The distance from the left (left) court boundary and baseline (top) in feet.
	note:: 
		Image is of half court with baseline at top.
	'''
	top, left = style[:-1].split(';')
	top = int(top.replace('top:', '').replace('px', ''))
	left = int(left.replace('left:', '').replace('px', ''))
	left = left/500.0 * 50.0
	top = top/472.0 * 47.0
	return left, top

def get_description(tip):
	'''
	Parse the description of the shot.
		tip (string): The HTML containing the description of the shot.
	Returns:
		A string containing the description of the shot.
	'''
	d = {}
	tip = tip.split()
	d['Quarter'] = int(tip[0][0])
	d['Time'] = tip[2]
	d['Player'] = tip[3].split('<br>')[1] + tip[4]
	d['Scored'] = 0 if tip[5] == 'missed' else 1
	d['Three_Pointer'] = 1 if tip[6] == '3-pointer' else 0
	d['Dist'] = tip[8]
	d['Team'] = tip[9].split('<br>')[1] + tip[10]
	#First score is the score of the team
	d['Score'] = tip[-1]
	return d

def get_shot_chart(home, away, date):
	'''
	Scrape the shot charts for each team for a given game.
		Parameters:
			home (string): The 3 letter abbreviation of the home team (e.g. 'TOR', 'BOS')
			away (string): The 3 letter abbreviation of the away team (e.g. 'TOR', 'BOS')
			date (string): The date of the game (e.g. '2020-12-23')
		Return:
			2 Pandas dataframes containing the information for every shot in the game.
	'''
	date_suffix = get_date_suffix(date)
	# shot_chart = render_JS('https://basketball-reference.com/boxscores/shot-chart/{}{}.html'.format(date_suffix, home.upper()))
	soup = BeautifulSoup(shot_chart, 'lxml')
	shot_chart_home = soup.find('div', id='shots-{}'.format(home.upper()))
	shot_chart_away = soup.find('div', id='shots-{}'.format(away.upper()))
	shot_chart_home = _get_shot_chart(shot_chart_home)
	shot_chart_away = _get_shot_chart(shot_chart_away)
	return shot_chart_away, shot_chart_home

def _get_shot_chart(chart):
	'''
	Helper function for scraping the shot charts.
		Parameters:
			chart (string): The HTML div containing the shot information.
		Returns:
			A Pandas dataframe containing the shot information.
	'''
	df = pd.DataFrame()
	for div in chart.find_all('div'):
		if 'style' not in div.attrs or 'tip' not in div.attrs:
			continue
		left, top = get_locations(div.attrs['style'])
		description = get_description(div.attrs['tip'])
		description['Dist_From_L'] = left
		description['Dist_From_T'] = top
		df = df.append(pd.DataFrame.from_dict([description]))
	return df

def get_team_shooting(home, team, date):
	'''
	Scrape the shooting stats of one of the teams in a game.
		Parameters:
			home (string): The 3 letter abbreviation of the home team (e.g. 'TOR', 'BOS')
			team (string): The 3 letter abbreviation of the team to get shooting stats for (e.g. 'TOR', 'BOS')
			date (string): The date of the game (e.g. '2020-12-23')
		Returns:
			A Pandas dataframe containing the team shooting stats for the game.
	'''
	# date_suffix = get_date_suffix(date)
	date_suffix = '202101010'
	shot_chart = render_JS('https://basketball-reference.com/boxscores/shot-chart/{}{}.html'.format(date_suffix, home.upper()))
	soup = BeautifulSoup(shot_chart, 'lxml')
	team_shooting = soup.find('table', id='shooting-{}'.format(team.upper()))
	team_shooting = pd.read_html(str(team_shooting))[0]
	return team_shooting
