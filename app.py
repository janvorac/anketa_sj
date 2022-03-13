import numpy as np
import pandas as pd
import pathlib
import plotly.express as px


PLOT_PATH = pathlib.Path('plots')
HIST_COLOR = '#0d2a63'


def download_csv():
    url = r'https://docs.google.com/spreadsheets/d/1OpuaqjYhXeoR1jAZTbT07NBuL0ijEeZjbSTtR3zDNoU/export?format=csv'
    data = pd.read_csv(url)
    data[data == ''] = np.nan
    data.set_index(keys=['id'], inplace=True)
    data = data.dropna(how='all', axis='index').dropna(how='all', axis='columns')
    return data


def create_tummy_full_histogram(data: pd.DataFrame):
    data = data[~data['jak_se_naji'].isnull()]
    data['jak_se_naji'] = data['jak_se_naji'].astype(int).astype(str)
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
    data_sub.loc[:, 'jak_casto_vraci'] = data_sub['jak_casto_vraci'].replace(1, 'téměř pokaždé')
    data_sub.loc[:, 'jak_casto_vraci'] = data_sub['jak_casto_vraci'].replace(2, '3-4×')
    data_sub.loc[:, 'jak_casto_vraci'] = data_sub['jak_casto_vraci'].replace(3, '1-2×')
    data_sub.loc[:, 'jak_casto_vraci'] = data_sub['jak_casto_vraci'].replace(4, 'výjimečně')
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
    data = data[~data['kvalita'].isnull()]
    data['kvalita'] = data['kvalita'].astype(int).astype(str)
    fig = px.histogram(
        data, x='kvalita', category_orders=dict(kvalita=[1, 2, 3, 4, 5]),  color_discrete_sequence=[HIST_COLOR]
    )
    fig.update_yaxes(title='počet')
    fig.update_xaxes(title='Jak jste spokojeni s kvalitou a chutí jídla v ŠJ (známky jako ve škole)')
    return fig


def create_experience_plot(data):
    counts = experience_counts(data)
    fig = px.bar(counts, orientation='h', color_discrete_sequence=[HIST_COLOR])
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title='Problémy s jídelnou')
    return fig


def experience_counts(data):
    exp = pd.Series(
        data['zkusenost'].str.split(
            ';', expand=True
        ).to_numpy().flatten()
    )
    exp = exp.str.strip()
    exp[exp == ''] = np.nan
    exp[exp.str.isspace().fillna(True)] = np.nan
    counts = exp.dropna().value_counts()
    return counts.sort_values()


def main():
    data = download_csv()

    tummy_full = create_tummy_full_histogram(data)
    tummy_full.write_html(PLOT_PATH / 'tummy_full.html')

    returns = create_how_often_you_return_hist(data)
    returns.write_html(PLOT_PATH / 'returns.html')

    quality = create_quality_score_histogram(data)
    quality.write_html(PLOT_PATH / 'quality_score.html')

    exp = create_experience_plot(data)
    exp.write_html(PLOT_PATH / 'experience.html')


if __name__ == "__main__":
    main()
