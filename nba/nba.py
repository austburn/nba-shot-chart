import requests
import json
import matplotlib
matplotlib.use('Qt4Agg')
import pandas
import seaborn
from IPython.display import display
from nba.court_utils import draw_court


shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS=2014-15&'\
    'ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&GameID=&GameSegment=&'\
    'LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&'\
    'Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=201935&PlusMinus=N&'\
    'Position=&Rank=N&RookieYear=&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&'\
    'TeamID=0&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0'


def get_shot_statistics():
    harden = open('harden.json')
    harden_json = json.loads(harden.readlines()[0])
    # # Get shot chart data
    # response = requests.get(shot_chart_url)
    # get column headers for pandas fram
    # headers = response.json()['resultSets'][0]['headers']
    # # get shot chart data
    # shots = response.json()['resultSets'][0]['rowSet']
    headers = harden_json.get('resultSets')[0].get('headers')
    shots = harden_json.get('resultSets')[0].get('rowSet')

    return shots


if __name__ == '__main__':
    shots = get_shot_statistics()
    shot_df = pandas.DataFrame(shots, columns=headers)

    with pandas.option_context('display.max_columns', None):
        display(shot_df.head())

    seaborn.set_style('white')
    seaborn.set_color_codes()

    # # Basic Graph
    plt.figure(figsize=(12, 11))
    plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)
    ## Plot Right side
    # right = shot_df[shot_df.SHOT_ZONE_AREA == 'Right Side(R)']
    # plt.figure(figsize=(12,11))
    # plt.scatter(right.LOC_X, right.LOC_Y)
    plt.xlim(300, -300)
    plt.ylim(-100, 500)
    draw_court()
    plt.show()

    # joint_shot_chart = seaborn.jointplot(shot_df.LOC_X, shot_df.LOC_Y, stat_func=None, kind='scatter', space=0, alpha=0.5)
    # joint_shot_chart.fig.set_size_inches(12,11)

    # # A joint plot has 3 Axes, the first one called ax_joint
    # # is the one we want to draw our court onto and adjust some other settings
    # ax = joint_shot_chart.ax_joint
    # draw_court(ax)

    # # Adjust the axis limits and orientation of the plot in order
    # # to plot half court, with the hoop by the top of the plot
    # ax.set_xlim(-250,250)
    # ax.set_ylim(422.5, -47.5)

    # # Get rid of axis labels and tick marks
    # ax.set_xlabel('')
    # ax.set_ylabel('')
    # ax.tick_params(labelbottom='off', labelleft='off')

    # # Add a title
    # ax.set_title('James Harden FGA \n2014-15 Reg. Season',
    #              y=1.2, fontsize=18)

    # # Add Data Scource and Author
    # ax.text(-250,445,'Data Source: stats.nba.com'
    #         '\nAuthor: Savvas Tjortjoglou (savvastjortjoglou.com)',
    #         fontsize=12)

    # plt.show()
