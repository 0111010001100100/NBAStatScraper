import pandas as pd
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession  
import pyppdf.patch_pyppeteer

def render_JS(URL):
    session = HTMLSession()
    r = session.get(URL)
    r.html.render(timeout=60)
    return r.html.raw_html

def get_date_suffix(date):
	date = pd.to_datetime(date)
	return str(date.year) + str(date.month) + str(date.day) + '0'

def get_locations(style):
	top, left = style[:-1].split(';')
	top = int(top.replace('top:', '').replace('px', ''))
	left = int(left.replace('left:', '').replace('px', ''))
	left = left/500.0 * 50.0
	top = top/472.0 * 47.0
	return left, top

def get_description(tip):
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

def _get_shot_chart(chart):
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

def get_shot_chart(home, away, date):
	date_suffix = get_date_suffix(date)
	shot_chart = render_JS('https://basketball-reference.com/boxscores/shot-chart/{}{}.html'.format(date_suffix, home.upper()))
	soup = BeautifulSoup(shot_chart, 'lxml')
	shot_chart_home = soup.find('div', id='shots-{}'.format(home.upper()))
	shot_chart_away = soup.find('div', id='shots-{}'.format(away.upper()))
	shot_chart_home = _get_shot_chart(shot_chart_home)
	shot_chart_away = _get_shot_chart(shot_chart_away)
	return shot_chart_away

def get_team_shooting(home, team, date):
	date_suffix = get_date_suffix(date)
	shot_chart = render_JS('https://basketball-reference.com/boxscores/shot-chart/{}{}.html'.format(date_suffix, home.upper()))
	soup = BeautifulSoup(shot_chart, 'lxml')
	team_shooting = soup.find('table', id='shooting-{}'.format(team.upper()))
	team_shooting = pd.read_html(str(team_shooting))[0]
	return team_shooting