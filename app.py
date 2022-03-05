import pandas as pd
from bs4 import BeautifulSoup
import requests
import pandas
import numpy
import pathlib
import plotly.express as px


PLOT_PATH = pathlib.Path('plots')
HIST_COLOR = '#0d2a63'

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


def create_tummy_full_histogram(data: pd.DataFrame):
    fig = px.histogram(
        data,
        x='jak_se_naji',
        category_orders=dict(jak_se_naji=[1, 2, 3, 4, 5]),
        color_discrete_sequence=[HIST_COLOR]
    )
    fig.update_yaxes(title='počet')
    fig.update_xaxes(title='Jak dobře se v jídelně najíte (známky jako ve škole)')
    return fig


def create_how_often_you_return_hist(data):
    data_sub = data.copy()
    data_sub['jak_casto_vraci'] = data_sub['jak_casto_vraci'].replace('1', 'téměř pokaždé')
    data_sub['jak_casto_vraci'] = data_sub['jak_casto_vraci'].replace('2', '3-4×')
    data_sub['jak_casto_vraci'] = data_sub['jak_casto_vraci'].replace('3', '1-2×')
    data_sub['jak_casto_vraci'] = data_sub['jak_casto_vraci'].replace('4', 'výjimečně')
    fig = px.histogram(
        data_sub,
        x='jak_casto_vraci',
        category_orders=dict(
            jak_casto_vraci=['výjimečně', '1-2×', '3-4×', 'téměř pokaždé']),
        color_discrete_sequence=[HIST_COLOR]
    )
    fig.update_yaxes(title='počet')
    fig.update_xaxes(title='Jak často vracíte víc než polovinu jídla (z pěti obědů)')
    return fig


def create_quality_score_histogram(data):
    fig = px.histogram(
        data, x='kvalita', category_orders=dict(kvalita=[1, 2, 3, 4, 5]),  color_discrete_sequence=[HIST_COLOR]
    )
    fig.update_yaxes(title='počet')
    fig.update_xaxes(title='Jak jste spokojeni s kvalitou a chutí jídla v ŠJ (známky jako ve škole)')
    return fig


def main():
    data = get_data()
    tummy_full = create_tummy_full_histogram(data)
    tummy_full.write_html(PLOT_PATH / 'tummy_full.html')

    returns = create_how_often_you_return_hist(data)
    returns.write_html(PLOT_PATH / 'returns.html')

    quality = create_quality_score_histogram(data)
    quality.write_html(PLOT_PATH / 'quality_score.html')


if __name__ == "__main__":
    main()
