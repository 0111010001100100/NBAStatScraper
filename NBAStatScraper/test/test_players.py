import unittest
import sys

sys.path.append('../')
import players

class Test(unittest.TestCase):
    def test_get_player_url(self):
        '''
        Test for a player who exists with no duplicate name.
        '''
        name = "James Harden"
        extension = players.get_player_url(name)
        self.assertEqual(extension, ['hardeja01'])
        '''
        Test for a player who exists and name is shorter than 5 characters.
        '''
        name = "Bol Bol"
        extension = players.get_player_url(name)
        self.assertEqual(extension, ['bolbo01'])
        '''
        Test name with multiple results.
        '''
        name = "Chris Johnson"
        extension = players.get_player_url(name)
        self.assertEqual(extension, ['johnsch03', 'johnsch04'])

    @unittest.expectedFailure
    def test_get_player_url_fail(self):
        name = "James Harden"
        extension = players.get_player_url(name)
        self.assertEqual(extension, ['hardeja01', 'hardeja02'])
    
    def test_get_game_stats(self):
        fields = ['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
                  '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
                  'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        measurements = ['game', 'playoffGame']
        for item in measurements:
            name = "tatumja01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

            name = "jordami01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

            name = "jamesle01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

    @unittest.expectedFailure
    def test_game_stats_fail(self):
        name = "dowhyt01"
        fields = ['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
                  '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
                  'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        measurements = ['game','playoffGame']
        for item in measurements:
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)
    
    def test_total_stats(self):
        fields = ['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
                  '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
                  'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Trp Dbl']
        measurements = ['total', 'playoffTotal']
        for item in measurements:
            name = "hardeja01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

            name = "jordami01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

            name = "jamesle01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

    @unittest.expectedFailure
    def test_total_stats_fail(self):
        name = "dowhyt01"
        fields = ['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
                  '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
                  'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Trp Dbl']
        measurements = ['total', 'playoffTotal']
        for item in measurements:
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)
    
    def test_min_stats(self):
        fields = ['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
                  '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB',
                  'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        measurements = ['min', 'playoffMin']
        for item in measurements:
            name = "bealbr01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

            name = "jordami01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

            name = "jamesle01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

    @unittest.expectedFailure
    def test_min_stats_fail(self):
        name = "dowhyt01"
        fields = ['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
                  '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB',
                  'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        measurements = ['min', 'playoffMin']
        for item in measurements:
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

    def test_pos_stats(self):
        fields = ['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
                  '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB',
                  'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'ORtg', 'DRtg']
        measurements = ['pos', 'playoffPos']
        for item in measurements:
            name = "bealbr01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

            name = "jordami01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

            name = "jamesle01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

    @unittest.expectedFailure
    def test_pos_stats_fail(self):
        name = "dowhyt01"
        fields = ['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
                  '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB',
                  'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'ORtg', 'DRtg']
        measurements = ['min', 'playoffMin']
        for item in measurements:
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

    def test_shooting_stats(self):
        fields = ['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'MP', 'FG%', 'Dist.', '2P', '0-3', '3-10', 
                  '10-16', '16-3P', '3P', '2P', '0-3', '3-10', '10-16', '16-3P', '3P', '2P', '3P', '%FGA',
                  '#', '%3PA', '3P%', 'Att.', '#']
        measurements = ['shooting', 'playoffShooting']
        for item in measurements:
            name = "bealbr01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

            name = "jordami01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

            name = "jamesle01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

    @unittest.expectedFailure
    def test_shooting_stats_fail(self):
        name = "dowhyt01"
        fields = ['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'MP', 'FG%', 'Dist', '2P', '0-3', '3-10', 
                  '10-16', '16-3P', '3P', '2P', '0-3', '3-10', '10-16', '16-3P', '3P', '2P', '3P', '%FGA',
                  '#', '%3PA', '3P%', 'Att.', '#']
        measurements = ['shooting', 'playoffShooting']
        for item in measurements:
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

    def test_career_highs(self):
        fields = ['Season', 'Age', 'Tm', 'Lg', 'MP', 'FG', 'FGA',
                  '3P', '3PA', '2P', '2PA', 'FT', 'FTA', 'ORB',
                  'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc']
        measurements = ['careerHighs', 'playoffCareerHighs']
        for item in measurements:
            name = "bealbr01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

            name = "jordami01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

            name = "jamesle01"
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

    @unittest.expectedFailure
    def test_career_highs_fail(self):
        name = "dowhyt01"
        fields = ['Season', 'Age', 'Tm', 'Lg', 'MP', 'FG', 'FGA',
                  '3P', '3PA', '2P', '2PA', 'FT', 'FTA', 'ORB',
                  'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc']
        measurements = ['careerHighs', 'playoffCareerHighs']
        for item in measurements:
            df = players.get_career_player_stats(name, item)
            self.assertCountEqual(list(df.columns), fields)

    
if __name__ == '__main__':
    unittest.main()