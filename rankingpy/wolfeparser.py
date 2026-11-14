
from io import StringIO
import pandas as pd
import numpy as np
import rankutils as _ru
import teamnametesting as _tnt
import os

# TODO: encapsulate this in a class for easier coherent use

def _get_current_wolfe_scores(sport):
    if sport == 'CFB':
        url = 'http://prwolfe.bol.ucla.edu/cfootball/scores.htm'
    elif sport == 'CMBB':
        url = 'http://prwolfe.bol.ucla.edu/cbasketball/scores.htm'
    else:
        print("set to CFB cause you left it blank")
        url = 'http://prwolfe.bol.ucla.edu/cfootball/scores.htm'

    
    soup = _ru.cleanhtml(url)
    games = soup.findAll("pre")
    if len(games) != 1:
        print("the format has changed!")
    game = ''
    for x in games:
        game = str(x)

    game = game.replace('\t', '    ')
    #print(game)
    TESTDATA = StringIO(game)
    df = pd.read_csv(TESTDATA, delimiter='\t')
    if sport == 'CFB':
        df = df.drop(df.index[[0, 1, 2, len(df)-1]])
    elif sport == 'CMBB':
        df = df.drop(df.index[[0, 1, 2, 3, len(df)-1]])
    df = df.reset_index(drop=True)

    df = df.rename(columns={"<pre>": "gm_str"})
    # next line is important for aligntment of the file, and must be done first!
    df["gm_str"] = df["gm_str"].str.replace('amp;', '')
    # remove games in progress
    df = df[df["gm_str"].str[37:40].str.lower().str.strip() != 'xx']
    df = df[df["gm_str"].str[68:71].str.lower().str.strip() != 'xx']
    df = df.reset_index(drop=True)
    
    return df


def _get_saved_wolfe_scores(sport, year):
    print('hard coded for football other sports not archived yet')
    sport = 'CFB'
    seasonfile = sport + '_scores\\' + sport + str(year) + 'WeekFinal.txt'
    if year == 2019:
        seasonfile = sport + '_scores\\' + sport + str(year) + 'WeekCurrent.txt'
        print("Using the current file")
    seasonfile = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..',seasonfile))
    df = pd.read_table(seasonfile, header=None)
    df = df.rename(columns={0: "gm_str"})
    # next line is important for aligntment of the file, and must be done first!
    df["gm_str"] = df["gm_str"].str.replace('amp;', '')
    # remove games in progress
    df = df[df["gm_str"].str[37:40].str.lower().str.strip() != 'xx']
    df = df[df["gm_str"].str[68:71].str.lower().str.strip() != 'xx']
    df = df.reset_index(drop=True)
    
    return df


def _parse_wolfe_text(df):
    df["date"] = df["gm_str"].str[0:9]
    df["away_team"] = df["gm_str"].str[10:37].str.lower().str.strip().str.replace('-', ' ')
    df["away_score"] = df["gm_str"].str[37:40].astype(float)
    df["home_team"] = df["gm_str"].str[41:68].str.lower().str.strip().str.replace('-', ' ')
    df["home_score"] = df["gm_str"].str[68:71].astype(float)
    df["site"] = df["gm_str"].str[72:].str.strip()

    # check for heteronyms in team names
    hc = df["home_team"].value_counts()
    ac = df["away_team"].value_counts()
    #atc is All Teams Count
    atc = hc + ac
    #run team names through teamnametesting.py to eliminate heteronmys

    heteronyms = _tnt.check_heteronyms(atc)
    for nyms in heteronyms:
        for n in range(len(nyms)-1):
            print(nyms[0])
            print("This should change from " + nyms[n+1][0] + " to " + nyms[0][0])
            df.ix[df["away_team"] == nyms[n+1][0], "away_team"] = nyms[0][0]
            df.ix[df["home_team"] == nyms[n+1][0], "home_team"] = nyms[0][0]

    df["site"] = np.where(df["site"] == '', df["home_team"], df["site"])
    df["site"] = df["site"].str.lower()
    
    #game_info = df.values

    return df


def _wolfe_scores(sport, year):
    """
    Get college football score data from peter wolfes site

    Args:
        year

    Returns:
        game_info: an dataframe containing game
    """
    if year == "current":
        df = _get_current_wolfe_scores(sport)
    else:
        df = _get_saved_wolfe_scores(sport, year)
    df = _parse_wolfe_text(df)

    return df


def _saved_scores():
    """
    Get college football score data save files from peter wolfes site

    Args:
        none

    Returns:
        df: an dataframe containing game info
    """
    #df = _get_saved_wolfe()
    #df, game_info = _parse_wolfe_text(df)
    print("the read in function hasn't been written yet")
    df = False
    return df


def get_scores(sport, year):
    print(sport + " and " + str(year))
    df = _wolfe_scores(sport, year)
    return df


if __name__ == "__main__":
    df = get_scores("CFB","2014")