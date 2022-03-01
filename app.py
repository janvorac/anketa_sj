import pandas as pd
from bs4 import BeautifulSoup
import requests
import pandas
import numpy


def get_data() -> pd.DataFrame:
    html = requests.get(
        'https://docs.google.com/spreadsheets/d/1OpuaqjYhXeoR1jAZTbT07NBuL0ijEeZjbSTtR3zDNoU/edit?usp=sharing'
    ).text
    soup = BeautifulSoup(html, 'lxml')
    html_tab = soup.find_all("table")[0]

    data_rows = [[td.text for td in row.find_all("td")] for row in html_tab.find_all("tr")]

    data = pandas.DataFrame(data_rows[2:], columns=data_rows[1])

    data[data == ''] = numpy.nan

    data.set_index(keys=['id'], inplace=True)

    return data.dropna(how='all', axis='index').dropna(how='all', axis='columns')

