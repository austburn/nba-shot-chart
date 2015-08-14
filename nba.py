import requests
import json
import matplotlib.pyplot as plt
import pandas
import seaborn
from IPython.display import display
from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib.lines import Line2D

### DIMENSIONS ###
#   1 foot = 10 units
#

def draw_court(ax=None, color='black', lw=2, arc_debug=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
    restricted_area = Arc((0, -7.5), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
    arc = Arc((0, 0), 237.5*2, 237.5*2, theta1=22.8, theta2=157.2, linewidth=lw, color=color)

    boundaries = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
    key = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    paint = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
    paint_outer_arc = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color)
    paint_inner_arc = Arc((0, 142.5), 120, 120, theta1=180, theta2=360, linewidth=lw, linestyle='dashed', color=color)
    inner_circle = Circle((0, 422.5), radius=20, linewidth=lw, color=color, fill=False)
    outer_circle = Circle((0, 422.5), radius=60, linewidth=lw, color=color, fill=False)
    court_elements = [hoop, restricted_area, boundaries, arc, key, paint, paint_outer_arc,
                      paint_inner_arc, inner_circle, outer_circle]
    for element in court_elements:
        ax.add_patch(element)

    backboard = Line2D([-30, 30], [-7.5, -7.5], linewidth=lw, color=color)
    left_arc_base = Line2D([-220, -220], [-47.5, 92.5], linewidth=lw, color=color)
    right_arc_base = Line2D([220, 220], [-47.5, 92.5], linewidth=lw, color=color)

    post_lines = [
        Line2D([80, 85], [30, 30], linewidth=lw, color=color),
        Line2D([80, 85], [40, 40], linewidth=lw, color=color),
        Line2D([80, 85], [70, 70], linewidth=lw, color=color),
        Line2D([80, 85], [100, 100], linewidth=lw, color=color),

        Line2D([-80, -85], [30, 30], linewidth=lw, color=color),
        Line2D([-80, -85], [40, 40], linewidth=lw, color=color),
        Line2D([-80, -85], [70, 70], linewidth=lw, color=color),
        Line2D([-80, -85], [100, 100], linewidth=lw, color=color)
    ]

    arc_lines = []
    if arc_debug:
        arc_lines = [
            Line2D([0, 0], [0, 237.5], linewidth=lw, color='red'), # straight up
            # Second Quadrant
            Line2D([0, 218.9424985], [0, 92.03495178], linewidth=lw, color='red'), # 22.8 degrees
            Line2D([0, 196.89642348], [0, 132.80831457], linewidth=lw, color='red'), # 34 degrees
            Line2D([0, 167.35062487], [0, 168.52304993], linewidth=lw, color='red'), # 45.2 degrees
            Line2D([0, 131.43049295], [0, 197.81879467], linewidth=lw, color='red'), # 56.4 degrees
            Line2D([0, 90.50421438], [0, 219.57968298], linewidth=lw, color='red'), # 67.6 degrees
            Line2D([0, 46.13065841], [0, 232.9768494], linewidth=lw, color='red'), # 78.8 degrees
            # First Quadrant
            Line2D([0, -218.9424985], [0, 92.03495178], linewidth=lw, color='red'), # 22.8 degrees
            Line2D([0, -196.89642348], [0, 132.80831457], linewidth=lw, color='red'), # 34 degrees
            Line2D([0, -167.35062487], [0, 168.52304993], linewidth=lw, color='red'), # 45.2 degrees
            Line2D([0, -131.43049295], [0, 197.81879467], linewidth=lw, color='red'), # 56.4 degrees
            Line2D([0, -90.50421438], [0, 219.57968298], linewidth=lw, color='red'), # 67.6 degrees
            Line2D([0, -46.13065841], [0, 232.9768494], linewidth=lw, color='red') # 78.8 degrees
        ]

    court_lines = [backboard, left_arc_base, right_arc_base] + post_lines + arc_lines
    for line in court_lines:
        ax.add_line(line)

    return ax


shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS=2014-15&'\
    'ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&GameID=&GameSegment=&'\
    'LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&'\
    'Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=201935&PlusMinus=N&'\
    'Position=&Rank=N&RookieYear=&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&'\
    'TeamID=0&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0'

if __name__ == '__main__':
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
    plt.xlim(300,-300)
    plt.ylim(-100,500)
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
