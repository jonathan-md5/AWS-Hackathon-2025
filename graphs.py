import csv

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px

from college_conversion import college_conversion_list

games_file: str = "nfl-big-data-bowl-2023/games.csv"
players_file: str = "nfl-big-data-bowl-2023/players.csv"


def games_played() -> None:
    df = pd.read_csv(games_file)
    teams = pd.concat([df["homeTeamAbbr"], df["visitorTeamAbbr"]])
    counts = teams.value_counts().sort_index()

    counts.plot(
        kind="bar",
        figsize=(10, 5),
        xlabel="Team",
        ylabel="Games Played",
        title="Number of Games Played by Each Team",
        rot=45
    )

    plt.tight_layout()


def matchups() -> None:
    df = pd.read_csv(games_file, usecols=["homeTeamAbbr", "visitorTeamAbbr"])
    match_counts = pd.crosstab(df["homeTeamAbbr"], df["visitorTeamAbbr"])

    plt.figure(figsize=(12, 10))
    sns.heatmap(match_counts, cmap="coolwarm")
    plt.title("Home vs Visitor Matchups")
    plt.xlabel("Visitor Team")
    plt.ylabel("Home Team")


def age_to_weight() -> None:
    df = pd.read_csv(players_file)

    df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
    df = df.dropna(subset=['birthDate', 'weight', 'officialPosition'])

    today = pd.Timestamp('today')
    df['age'] = (today - df['birthDate']).dt.days / 365.25

    positions = df['officialPosition'].unique()
    colors = plt.cm.tab20.colors  # Up to 20 distinct colors
    position_color_map = {pos: colors[i % 20] for i, pos in enumerate(positions)}

    plt.figure(figsize=(12, 6))
    for pos in positions:
        subset = df[df['officialPosition'] == pos]
        plt.scatter(subset['age'], subset['weight'],
                    color=position_color_map[pos], label=pos, alpha=0.9)

    plt.xlabel("Age (years)")
    plt.ylabel("Weight (lbs)")
    plt.title("Player Age vs Weight by Position")
    plt.legend()


def player_stats():
    stats1: list = []
    stats2: list = []
    with open(players_file, 'r') as csv_file:
        player_csv = csv.reader(csv_file)
        columns = next(player_csv)

        index_type = input("input index type: ")
        index_type2 = input("input 2nd index type: ")

        column_index = columns.index(index_type)
        column_index2 = columns.index(index_type2)
        for row in player_csv:
            print(row[column_index], row[column_index2])
            # stats1.append(float(donut[column_index]))
            # stats2.append(float(donut[column_index2]))
        x = stats1
        y = stats2
        plt.scatter(x, y)
        plt.show()


def heatmaps():
    # Uses pandas the read file
    df = pd.read_csv("nfl-big-data-bowl-2023/players.csv")

    # Converts from college to state location
    df['location'] = df['collegeName'].map(college_conversion_list)
    location_counter = df['location'].value_counts().reset_index()
    location_counter.columns = ['location', 'location_counter']

    # plots map
    fig = px.choropleth(
        location_counter,
        locations='location',
        locationmode='USA-states',

        color='location_counter',
        color_continuous_scale='blues',
        scope='usa'

    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()
