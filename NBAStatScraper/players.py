import pandas as pd
from bs4 import BeautifulSoup, Comment
import requests
import unicodedata, unidecode


def get_player_url(name):
	'''
	Builds and returns the URL extension for a given player.
		Parameters: 
			name (string): The name of an NBA player (e.g. 'James Harden')
		Returns:
			A list containing the URL extensions for the players (e.g. ['hardeja01'])
	'''
	names = []
	name = unidecode.unidecode(unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8"))
	suffix = _get_player_url(name) + '01'
	player = requests.get('https://www.basketball-reference.com/players/{}/{}.html'.format(suffix[0], suffix))
	while player.status_code == 200:
		soup = BeautifulSoup(player.content, 'lxml')
		h1 = soup.find('h1', attrs={'itemprop': 'name'})
		if h1:
			page_name = h1.find('span').text
			if unidecode.unidecode(page_name).lower() == name.lower():
				names.append(suffix)
			suffix = suffix[:-1] + str(int(suffix[-1])+1)
			player = requests.get('https://www.basketball-reference.com/players/{}/{}.html'.format(suffix[0], suffix))
	return names
	return "Error player {} not found.".format(name)

def _get_player_url(name):
	'''
	Helper function for building the URL extension for a given player.
		Parameters:
			name (string): The name of an NBA player (e.g. 'James Harden')
		Returns: 
			The base of the URL extension (e.g. 'hardeja')
	'''
	first, last = name.lower().split()
	if len(last) > 5:
		last = last[:5]
	return last + first[:2]

def get_season_projection(name):
	'''
	Scrape the current season stat projections for a player.
		Parameters:
			name (string): The first and last name of a player (e.g. 'Joel Embiid')
		Returns:
			A Pandas dataframe containing the player's stat projections for the current season.
	note::
		Only available in the offseason. 
	'''
	normalized_name = get_player_url(name)
	player_projection = requests.get('https://www.basketball-reference.com/players/{}/{}.html'.format(normalized_name[0], normalized_name))
	if player_projection.status_code == 200:
		soup = BeautifulSoup(player_projection.content, 'lxml')
		player_projection = soup.find('table', id='projection')
		player_projection = pd.read_html(str(player_projection))[0]
		player_projection.columns = player_projection.columns.droplevel()
	else:
		return "Error getting season projection for {}.".format(name)
	return player_projection

def get_career_player_stats(extension, per):
	'''
	Scrape the career stats for a given player.
		Parameters:
			extension (string): The URL extension of a given player (e.g. 'hardenja01')
			per (string): The method in which the statistics are calculated. Can be any one of:
				['game', 'total', 'min', 'pos', 'shooting', 'playoffTotal', 'playoffGame', 'playoffMin', 
				'playoffPos', 'playoffShooting', 'careerHighs', 'playoffCareerHighs', 'college', 'salary', 'contract']
		Return:
			A Pandas dataframe containing the player stats.
	'''
	per_dict = {'game': 'all_per_game', 'total': 'all_totals', 'min': 'all_per_minute', 
		'pos': 'all_per_poss', 'shooting': 'all_shooting', 'playoffTotal': 'all_playoffs_totals', 
		'playoffGame': 'all_playoffs_per_game', 'playoffMin': 'all_playoffs_per_minute', 
		'playoffPos': 'all_playoffs_per_poss', 'playoffShooting': 'all_playoffs_shooting',
		'careerHighs' : ['all_game_highs', 'all_year-and-career-highs'], 'playoffCareerHighs': ['all_game_highs_po', 'all_year-and-career-highs-po'],
		'college': 'all_all_college_stats', 'salary': 'all_all_salary', 'contract': 'all_contract'}
	
	#TODO: add name as optional parameter so this can be used optionally
	# This code is for getting the URL extension for players. Since I have them I need to think of what to do with this
	# normalized_name = get_player_url(name)
	
	player_stats = requests.get('https://www.basketball-reference.com/players/{}/{}.html'.format(extension[0],extension))

	if player_stats.status_code == 200:
		soup = BeautifulSoup(player_stats.content, 'lxml')
		if per == 'game':
			player_stats = soup.find('div', id=per_dict[per])
		else:
			if per in ['careerHighs', 'playoffCareerHighs']:
				try:
					player_stats = soup.find('div', id=per_dict[per][0]).find(string=lambda tag: isinstance(tag, Comment))
				except AttributeError:
					player_stats = soup.find('div', id=per_dict[per][1]).find(string=lambda tag: isinstance(tag, Comment))
			else:
				player_stats = soup.find('div', id=per_dict[per]).find(string=lambda tag: isinstance(tag, Comment))
		player_stats = pd.read_html(str(player_stats))[0]
		player_stats = player_stats.fillna(0)
		if per in ['shooting', 'playoffShooting', 'careerHighs', 'playoffCareerHighs']:
			player_stats.columns = player_stats.columns.droplevel()
		player_stats = player_stats.drop(player_stats[player_stats['Season'] == 0].index)
		player_stats = player_stats.drop(player_stats.columns[player_stats.columns.str.contains('unnamed',case = False)],axis = 1)
	else:
		return "Error getting {} stats for {}.".format(per, extension)
	return player_stats

def get_player_headshot(extension):
	'''
	Get the link to the headshot of a given player.
		Parameters:
			extension (string): The URL extension of a given player (e.g. 'hardenja01')
		Returns:
			The link to a player's headshot.
	'''
	return "https://d2cwpp38twqe55.cloudfront.net/req/202006192/images/players/{}.jpg".format(extension)
