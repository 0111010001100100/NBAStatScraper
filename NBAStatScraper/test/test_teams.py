import unittest
import sys

sys.path.append('../')
import teams

class Test(unittest.TestCase):
    def test_get_roster_standings(self):
        fields = ['Number', 'Name', 'Pos', 'Height', 'Weight', 'Birthday', 'Nationality', 'YearsExp', 'College']
        teamToTest = [('BOS', '2018'), ('TOR', '2019'), ('CHI', '2003')]
        for item in teamToTest:
            df = teams.get_roster(item[0], item[1])
            self.assertCountEqual(list(df.columns), fields)


    @unittest.expectedFailure
    def test_get_roster_standings_fail(self):
        fields = ['Number', 'Name', 'Pos', 'Height', 'Weight', 'Birthday', 'Nationality', 'YearsExp', 'College']
        df = teams.get_roster('NBA', '2019')
        self.assertCountEqual(list(df.columns), fields)

    def test_get_team_game_total_stats(self):
        fields = ['Rk', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%',
                  'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        measurements = ['game', 'playoffGame', 'total', 'playoffTotal']
        for item in measurements:
            df = teams.get_team_stats('BOS', '2019', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('GSW', '2018', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('HOU', '2017', item)
            self.assertCountEqual(list(df.columns), fields)
    
    @unittest.expectedFailure
    def test_get_team_game_total_stats_fail(self):
        fields = ['Rk', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%',
                  'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        measurements = ['game', 'playoffGame', 'total', 'playoffTotal']
        for item in measurements:
            df = teams.get_team_stats('TDD', '2019', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('GSW', '2909', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('', '', item)
            self.assertCountEqual(list(df.columns), fields)
    
    def test_team_per_min_stats(self):
        fields = ['Rk', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%',
                  'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        measurements = ['min', 'playoffMin']
        for item in measurements:
            df = teams.get_team_stats('BOS', '2019', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('GSW', '2018', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('HOU', '2017', item)
            self.assertCountEqual(list(df.columns), fields)
    
    @unittest.expectedFailure
    def test_team_per_min_stats_fail(self):
        fields = ['Rk', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%',
                  'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        measurements = ['min', 'playoffMin']
        for item in measurements:
            df = teams.get_team_stats('TDD', '2019', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('GSW', '2909', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('', '', item)
            self.assertCountEqual(list(df.columns), fields)
    
    def test_team_per_pos_stats(self):
        fields = ['Rk', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%',
                  'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'ORtg', 'DRtg']
        measurements = ['pos', 'playoffPos']
        for item in measurements:
            df = teams.get_team_stats('BOS', '2019', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('GSW', '2018', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('HOU', '2017', item)
            self.assertCountEqual(list(df.columns), fields)

    @unittest.expectedFailure
    def test_team_per_pos_stats_fail(self):
        fields = ['Rk', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%',
                  'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'ORtg', 'DRtg']
        measurements = ['pos', 'playoffPos']
        for item in measurements:
            df = teams.get_team_stats('TDD', '2019', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('GSW', '2909', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('', '', item)
            self.assertCountEqual(list(df.columns), fields)

    def test_team_shooting_stats(self):
        fields = ['Rk', 'Player', 'Age', 'G', 'MP', 'FG%', 'Dist.', '2P', '0-3', '3-10', 
                  '10-16', '16-3P', '3P', '2P', '0-3', '3-10', '10-16', '16-3P', '3P', '2P', '3P', '%FGA',
                  '#', '%3PA', '3P%', 'Att.', '#']
        measurements = ['shooting', 'playoffShooting']
        for item in measurements:
            df = teams.get_team_stats('BOS', '2019', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('GSW', '2018', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('HOU', '2017', item)
            self.assertCountEqual(list(df.columns), fields)

    @unittest.expectedFailure
    def test_team_shooting_stats_fail(self):
        fields = ['Rk', 'Player', 'Age', 'G', 'MP', 'FG%', 'Dist.', '2P', '0-3', '3-10', 
                  '10-16', '16-3P', '3P', '2P', '0-3', '3-10', '10-16', '16-3P', '3P', '2P', '3P', '%FGA',
                  '#', '%3PA', '3P%', 'Att.', '#']
        measurements = ['shooting', 'playoffShooting']
        for item in measurements:
            df = teams.get_team_stats('TDD', '2019', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('GSW', '2909', item)
            self.assertCountEqual(list(df.columns), fields)

            df = teams.get_team_stats('', '', item)
            self.assertCountEqual(list(df.columns), fields)
    
    def test_get_team_stats_per_game(self):
        fields = ['Season', 'Lg', 'Tm', 'W', 'L', 'Finish', 'Age', 'Ht.', 'Wt.', 'G', 'MP', 'FG', 'FGA', 
                  'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 
                  'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        teamsToTest = ['BOS', 'TOR', 'CHI']
        for team in teamsToTest:
            df = teams.get_team_stats_per_game(team)
            self.assertCountEqual(list(df.columns), fields)

    @unittest.expectedFailure
    def test_get_team_stats_per_game_fail(self):
        fields = ['Season', 'Lg', 'Tm', 'W', 'L', 'Finish', 'Age', 'Ht.', 'Wt.', 'G', 'MP', 'FG', 'FGA', 
                  'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 
                  'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        teamsToTest = ['TDaaaaD', '234', '']
        for team in teamsToTest:
            df = teams.get_team_stats_per_game(team)
            self.assertCountEqual(list(df.columns), fields)

if __name__ == '__main__':
    unittest.main()