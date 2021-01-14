# NBA Stat Scraper 
-----------------------------------------------------------------------------------------------------------------------------
This project has two main components: a web scraper and a database for the scraped data.

The web scraper is for NBA statistics on games, players, standings, and teams. This project uses information available on [Basketball Reference](https://basketball-reference.com). I wrote this module to learn BeautifulSoup, and use it for analytics to annoy friends with stats nobody asked for. 

The database uses the stores the scraped data. There are currently 5 tables: players, players.perGame, teams, teams.perGame, standings.


## Usage
This section describes the methods supported by this project. 

### Installation
Clone the repository:
`$ git clone https://github.com/NBAStatScraper.git`
Install the requirements:
`$ pip install -r requirements.txt`

### Player
#### `get_season_projection(name)`
Parameters:
  - `name`: The first and last name of a player (e.g. `'Joel Embiid'`)

Returns:

A Pandas dataframe containing the player's stat projections for the current season.

#### `get_career_player_stats(name, per):`
Parameters:
  - `name`: The first and last name of a player (e.g. `OG Anunoby`)
  - `per`: The method in which the statistics are calculated. Can be any one of:
  ```
  ['game', 'total', 'min', 'pos', 'shooting', 'playoffTotal', 'playoffGame', 'playoffMin', 'playoffPos', 'playoffShooting', 'careerHighs', 'playoffCareerHighs', 'college', 'salary', 'contract']
  ```
  
Returns:
  
A Pandas dataframe containing the player stats. 
  
### Team
#### `get_roster(team, year)`
Parameters:
  - `team`: The 3 letter abbreviation of an NBA team (e.g. `'TOR'`, `'POR'`)
  - `year`: The year for the roster to get (e.g. 2020)
    
Returns:
  
A Pandas dataframe containing the roster and player information for the year.
  
#### `get_team_stats(team, year, per)`
Parameters:
  - `team`: The 3 letter abbreviation of an NBA team (e.g. `'TOR'`, `'POR'`)
  - `year`: The year for the roster to get (e.g. 2020)
  - `per`: The method in which the statistics are calculated. Can be any one of:
```
['game', 'total', 'min', 'pos', 'shooting', 'playoffTotal', 'playoffGame', 'playoffMin', 'playoffPos', 'playoffShooting']
```

Returns:

A Pandas dataframe containing the team stats for a chosen year.

### Game
These two are currently broken. I suspect it is an issue with WSL.
#### `get_shot_chart(home, away, date)`
Parameters:
  - `home`: The 3 letter abbreviation of the home team (e.g. `'TOR'`, `'BOS'`)
  - `away`: The 3 letter abbreviation of the away team (e.g. `'TOR'`, `'BOS'`)
  - `date`: The date of the game (e.g. `2020-12-23`)
  
Returns:

A Pandas dataframe containing the locations and information of each shot taken in the game.

#### `get_team_shooting(home, team, date)`
Parameters: 
  - `home`: The 3 letter abbreviation of the home team (e.g. `'TOR'`, `'BOS'`)
  - `team`: The 3 letter abbreviation of the team to get the shooting stats for (e.g. `'TOR'`, `'BOS'`)
  - `date`: The date of the game (e.g. `2018-11-20`)

Returns:

A Pandas dataframe containing the team's shooting information for the game.

### Standings
#### `get_conference_standings(conference, year)`
Parameters:
  - `conference`: The conference to get the standings for. Can be one of `['E', 'W']`
  - `year`: The year to get the conference standings for (e.g. '2019`)

Returns:

A Pandas dataframe containing the conference standings.

#### `get_league_standings(year)`
Parameters:
  - `year`: The year to get the league standings for (e.g. '2000')
  
Returns:

A Pandas dataframe containing the league standings for a year.

#### `get_team_v_team(year)`
Parameters:
  - `year`: The year to get the team vs. team records (e.g. '2018')
  
Returns:
  - A Pandas dataframe containing the records of each team against every other team.
