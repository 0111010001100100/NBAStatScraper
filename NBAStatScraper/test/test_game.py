import unittest
import sys

sys.path.append('../')
import game

class Test(unittest.TestCase):
    def test_get_date_suffix(self):
        date = game.get_date_suffix('2020-12-23')
        self.assertEqual(date, '202012230')

        date = game.get_date_suffix('2019-11-03')
        self.assertEqual(date, '20191130')

        date = game.get_date_suffix('2015-01-08')
        self.assertEqual(date, '201501080')


    @unittest.expectedFailure
    def test_get_date_suffix_fail(self):
        date = game.get_date_suffix('')
        self.assertEqual(date, '')

        date = game.get_date_suffix('hello')
        self.assertEqual(date, 'hello0')
    
    # def test_get_shot_chart(self):
        

if __name__ == '__main__':
    unittest.main()