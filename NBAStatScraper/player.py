import pandas as pd
from bs4 import BeautifulSoup, Comment
import requests
import unicodedata, unidecode

def _get_player_url(name):
	first, last = name.lower().split()
	if len(last) > 5:
		last = last[:5]
	return last + first[:2]

def get_player_url(name):
	name = unidecode.unidecode(unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8"))
	suffix = _get_player_url(name) + '01'
	player = requests.get('https://www.basketball-reference.com/players/b/{}.html'.format(suffix))
	while player.status_code == 200:
		soup = BeautifulSoup(player.content, 'lxml')
		h1 = soup.find('h1', attrs={'itemprop': 'name'})
		if h1:
			page_name = h1.find('span').text
			if unidecode.unidecode(page_name).lower() == name.lower():
				return suffix
			suffix = suffix[:-1] + str(int(suffix[-1])+1)
			player = requests.get('https://www.basketball-reference.com/players/b/{}.html'.format(suffix))
	return "Error player {} not found.".format(name)

def get_season_projection(name):
	normalized_name = get_player_url(name)
	player_projection = requests.get('https://www.basketball-reference.com/players/b/{}.html'.format(normalized_name))
	if player_projection.status_code == 200:
		soup = BeautifulSoup(player_projection.content, 'lxml')
		player_projection = soup.find('table', id='projection')
		player_projection = pd.read_html(str(player_projection))[0]
		player_projection.columns = player_projection.columns.droplevel()
	else:
		return "Error getting season projection for {}.".format(name)
	return player_projection

def get_career_player_stats(extension, per):
# per can be game, total, 36min, 100pos, shooting, playoffTotal, playoffGame, 
# playoff36min, playoff100pos, playoffShooting, careerHighs, playoffCareerHighs, college,
# salary, contract
	per_dict = {'game': 'all_per_game', 'total': 'all_totals', '36min': 'all_per_minute', 
		'100pos': 'all_per_poss', 'shooting': 'all_shooting', 'playoffTotal': 'all_playoffs_totals', 
		'playoffGame': 'playoffs_per_game', 'playoff36min': 'all_playoffs_per_minute', 
		'playoff100pos': 'all_playoffs_per_poss', 'playoffShooting': 'all_playoffs_shooting',
		'careerHighs' : 'all_year-and-career-highs', 'playoffCareerHighs':'all_year-and-career-highs-po',
		'college': 'all_all_college_stats', 'salary': 'all_all_salary', 'contract': 'all_contract'}
	
	# This code is for getting the URL extension for players. Since I have them I need to think of what to do with this
	# normalized_name = get_player_url(name)
	
	player_stats = requests.get('https://www.basketball-reference.com/players/b/{}.html'.format(extension))


	if player_stats.status_code == 200:
		soup = BeautifulSoup(player_stats.content, 'lxml')
		if per == 'game':
			player_stats = soup.find('div', id=per_dict[per])
		else:
			player_stats = soup.find('div', id=per_dict[per]).find(string=lambda tag: isinstance(tag, Comment))
		player_stats = pd.read_html(str(player_stats))[0]
		player_stats = player_stats.fillna(0)
	else:
		return "Error getting {} stats for {}.".format(per, extension)
	return player_stats

def get_player_headshot(extension):
	return "https://d2cwpp38twqe55.cloudfront.net/req/202006192/images/players/{}.jpg".format(extension)


