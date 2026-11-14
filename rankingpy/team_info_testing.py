
import runrankings as rr

if __name__ == "__main__":


    # TODO: define needs for this part of the package

    #run the season
    trr = rr.test_run_rankings()

    # list of game values of interest
    lst = ['date','away_team','away_score','home_team','home_score','site','gof','pf','pa','sco','scd']

    #team of interest
    team = 'virginia tech'
    opps = []
    #teams opponents
    for opp in trr.teams[team].opponents:
        opps.append(opp)
    print(opps)

    # add all the relevent oppoenetns to the teams dataframe
    tmdf = trr.rankings[trr.rankings['name'].isin(opps)].sort_values(['rank'], ascending=1).copy(deep=True).reset_index(drop=True)

    # add all the relevent data to the teams dataframe
    for ky in lst:
        tmdf[ky] = 0
        for game in trr.teams[team].games:
            # TODO: fix this up for instances of playing the same opponent more than once
            #if the value we want isn't 0, then we add a new line and increment the loc variable we'll need to set
            # date is the first value, so that's what we'll check
            if 'gof' in tmdf:
                print('gof already added', tmdf['gof'])
                # tmdf.iloc[14] = tmdf.loc[0]
                tmdf.set_value(tmdf[tmdf['name'].isin([trr.df['home_team'].ix[game],trr.df['away_team'].ix[game]])].index.values.tolist(),ky,trr.df.ix[game][ky])
            else:
                tmdf.set_value(tmdf[tmdf['name'].isin([trr.df['home_team'].ix[game],trr.df['away_team'].ix[game]])].index.values.tolist(),ky,trr.df.ix[game][ky])

    # team info
    trr.rankings[trr.rankings['name'] == team]
    # teams opponent info
    tmdf

    '''
    # calc difference in ratings bin
    rb = 0.0
    for ky in trr.teams.keys():
        if trr.teams[ky].ratingbin[0]-trr.teams[ky].ratingbin[1] != 0.0:
            print((ky, (trr.teams[ky].ratingbin[0]-trr.teams[ky].ratingbin[1])))
            rb = rb + trr.teams[ky].ratingbin[0]-trr.teams[ky].ratingbin[1]
    print("rb: ", rb)
    '''

    # team rankings
    trr.rankings.sort_values('rating',ascending=0)