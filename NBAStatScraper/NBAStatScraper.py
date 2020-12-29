import pandas as pd
from requests_html import HTMLSession  
import pyppdf.patch_pyppeteer
from bs4 import BeautifulSoup, Comment
from game import *
from standings import *

def main():
    print(get_team_v_team('2019'))

if __name__ == '__main__':
    # For debugging
    pd.set_option('display.max_columns', None)
    main()
