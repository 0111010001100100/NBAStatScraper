import unittest
import sys

sys.path.append('../')
import standings
import database.databasePrep.prep_standings as prep

class Test(unittest.TestCase):
    def test_get_division_standings(self):
        fields = ['teamId', 'wins', 'losses', 'ratio', 'ppg', 'oppg', 'year', 'conference']
        yearsToTest = ['2019', '2010', '2002']
        for year in yearsToTest:
            df = prep.prep_standings(year)
            self.assertCountEqual(list(df.columns), fields)

    @unittest.expectedFailure
    def test_get_division_standings_fail(self):
        fields = ['teamId', 'wins', 'losses', 'ratio', 'ppg', 'oppg', 'year', 'conference']
        yearsToTest = ['2222', '3333', 'asfd']
        for year in yearsToTest:
            df = prep.prep_standings(year)
            self.assertCountEqual(list(df.columns), fields)

    def test_get_conference_standings(self):
        conferences = ['W', 'E']
        yearsToTest = ['2019', '2017', '2016']
        for c in conferences:
            for year in yearsToTest:
                if c == 'W':
                    fields = ['Western Conference', 'W', 'L', 'W/L%', 'GB', 'PS/G', 'PA/G', 'SRS']
                else:
                    fields = ['Eastern Conference', 'W', 'L', 'W/L%', 'GB', 'PS/G', 'PA/G', 'SRS']
                df = standings.get_conference_standings(c, year)
                self.assertCountEqual(list(df.columns), fields)
    
    @unittest.expectedFailure
    def test_get_conference_standings_fail(self):
        fields = ['teamId', 'wins', 'losses', 'ratio', 'ppg', 'oppg', 'year', 'conference']
        yearsToTest = ['2222', '3333', 'asfd']
        for year in yearsToTest:
            df = standings.get_conference_standings('W',year)
            self.assertCountEqual(list(df.columns), fields)

    def test_get_league_standings(self):
        fields = ['Rk', 'Team', 'Overall', 'Home', 'Road', 'E', 'W', 'A', 'C', 'SE', 'NW', 'P', 'SW', 'Pre',
                  'Post', '≤3', '≥10', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr']
        yearsToTest = ['2019', '2010']
        for year in yearsToTest:
            df = standings.get_league_standings(year)
            self.assertCountEqual(list(df.columns), fields)

        fields = ['Rk', 'Team', 'Overall', 'Home', 'Road', 'E', 'W', 'A', 'C', 'M', 'P', 'Pre',
                  'Post', '≤3', '≥10', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr']
        df = standings.get_league_standings('2002')
        self.assertCountEqual(list(df.columns), fields)

    @unittest.expectedFailure
    def test_get_league_standings_fail(self):
        fields = ['Rk', 'Team', 'Overall', 'Home', 'Road', 'E', 'W', 'A', 'C', 'SE', 'NW', 'P', 'SW', 'Pre',
                  'Post', '≤3', '≥10', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr']
        yearsToTest = ['2222', '3333', 'asfd']
        for year in yearsToTest:
            df = standings.get_league_standings(year)
            self.assertCountEqual(list(df.columns), fields)

    
if __name__ == '__main__':
    unittest.main()