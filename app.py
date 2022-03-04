import pandas as pd
from bs4 import BeautifulSoup
import requests
import pandas
import numpy
import pathlib
import plotly.express as px


PLOT_PATH = pathlib.Path('plots')


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


def tummy_full_histogram(data: pd.DataFrame):
    data = get_data()

    fig = px.histogram(data, x='jak_se_naji', category_orders=dict(jak_se_naji=[1, 2, 3, 4, 5]))
    fig.update_yaxes(title='počet')
    fig.update_xaxes(title='Jak dobře se v jídelně najíte (známky jako ve škole)')
    return fig


def main():
    data = get_data()
    tummy_full = tummy_full_histogram(data)
    tummy_full.write_html(PLOT_PATH / 'tummy_full.html')


if __name__ == "__main__":
    main()
