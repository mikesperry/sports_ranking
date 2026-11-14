
'''
import cProfile, pstats, io
pr = cProfile.Profile()
pr.enable()
'''

from datetime import datetime
import random
import numpy as np
import pandas as pd
import math as m

import wolfeparser as _wp
import dijkstra as dij



def timeDif (x, y):
    print(str(y-x))


'''
C0 = 0.0
C1 = 2.15
C2 = 1.0
C3 = 1.1
C4 = 0.25
C5 = 2.0
C6 = 1.0
C7 = 0.0
C8 = 0.0
C9 = 0.0
'''
C0 = 0.0
C1 = 2.0
C2 = 1.0
C3 = 1.0
C4 = 0.15
C5 = 2.0
C6 = 1.0
#C7 = 0.01 or 0.0
#C8 = 0.0
#C9 = 0.0



def rate(aR, oN, oR, w, l, num, wp, lp):
    """
    Args:
        aR: average rating accros connected teams
        oN: opponents strength adjusted:   oppoenetns sum(Rating)*sum(SOS)
        oR: opponent rating
        w: wins
        l: losses
        num: number of games played
        wp: some sort of win points
        lp: some sort of loss points
    Returns:
        rating

    tuning params:
        C0 = 0.0            numerator factor
        C1 = 2.0            norm/sos balancing factor
        C2 = 1.0            w-l factor
        C3 = 1.0            sos factor
        C4 = 1/15 or 0.15   wp and lp factor
        C5 = 2.0            denomiator factor
        C6 = 1.0            denom game num factor
        C7 = 0.01 or 0.0    denom inverse norm factor
        C8 = 0.0            onorm factor
        C9 = 0.0            num factor
    """

    # oN and oR are SUMS not Averages
    '''
    rating = ((1.0 / (aR)) *
              ((C0 + C1*oN / oR + C2*((w - l) / 2.0) + C3*oR + C8*oN + num*(C9/2.0 + C4*((wp + lp)))) /
               (C5 + num*(C6 + C7*num / oN))))
    
    '''
    
    #regular rating
    rating = ((1.0 / (aR)) *
              ((C0 + C1*oN / oR + C2*((w - l) / 2.0) + C3*oR + num*(C4*((wp + lp)))) /
               (C5 + num*(C6))))
    
    
    '''
    #rating = ((1 + ( (w - l)/ 2.0 ) + oR) / (2 + num))
    C0=0
    C1=1
    C2=1
    C3=1
    C4=0
    C5=2
    C6=1
    
    rating = ((1.0 / (2.0*aR)) *(C0 + C1*2.0*oN/oR + C2*((w - l) / 2.0) + C3*oR + num*(C4*((wp + lp)))) /
               (C5 + num*(C6)))
    '''
    #rating = (1 + ((w - l)/2.0) + num/2.0 ) / (2 + num)  
    
    #rating = round(rating,15)
    return rating


'''    
def prnt_gm_info(self):
    print(self.date + ", " + self.away_team + ", " + str(self.away_score) +
          ", " + self.home_team + ", " + str(self.home_score) + ", " +
          self.location + ", " + str(self.gof))
    return True
'''

class Team:
    def __init__(self, team):
        self.name = team[0]
        self.ngp = team[1]
        self.games = []
        self.opponents = []
        self.wins = 0
        self.loses = 0
        self.ties = 0
        self.ratingbin = [0.5,0.5]
        self.sosbin = [0.5,0.5]
        self.rating = 0.5
        self.sos = 0.5
        self.sosw = 0.5
        self.sosl = 0.5
        self.wpts = 0.5
        self.lpts = 0.5
        self.pf = 0.0
        self.pa = 0.0
        self.sco = 0.0
        self.scd = 0.0
        self.onorm = 0.5
        self.bw = ('',0.5)
        self.wl = ('',0.5)
        self.group = 0
        ###
        ### UNDO this!!! REWEITE teams gamedf to be a dataframe instead of a set of class objects
        ###
        self.gamedf = False # a dataframe to hold this teams games in a useful format

    def set_group(self, n):
        self.group = n
        
    def set_games_played(self,gp,tp):
        self.games = gp
        self.opponents = tp
        
    def set_df(self, df):
        self.gamedf = df
        self.gamedf.copy(deep=True)
        self.gamedf['pf'] = np.where(self.gamedf["home_team"]==self.name, self.gamedf["home_score"], self.gamedf["away_score"])
        self.gamedf['pa'] = np.where(self.gamedf["home_team"]==self.name, self.gamedf["away_score"], self.gamedf["home_score"])
        self.gamedf['opponent'] = np.where(self.gamedf["home_team"]==self.name, self.gamedf["away_team"], self.gamedf["home_team"])
        self.gamedf['gof_share'] = np.where(self.gamedf["home_team"]==self.name, self.gamedf["gof"], 1-self.gamedf["gof"])


    def return_bins(self, ooe):
        return self.ratingbin[ooe], self.sosbin[ooe]
        
    def print_team(self):
        print((self.name, self.ngp, self.wins, self.loses,self.rating,
               self.sos,self.sosw,self.sosl,self.wpts,self.lpts,self.onorm,self.bw,self.wl,self.group, self.games))
        return True



class Season:
    # read in and hold initial data
    # run games
    # create list of teams
    def __init__(self):
        self.rnk_mean = 0.5
        self.rnk_std = 0.0
        self._year = self._set_year()
        #self._year = '2016'
        self._sport = self._set_sport()
        #self._sport = 'CFB'
        
        self._even_or_odd = 0
        self._odd_or_even = 1
        self._ar = [0.0,0.5]

        
        self.teams, self.df, self.graph = self._set_season()
        self.rankings = self._process_season()
        


    def _set_sport(self):
        print("What sport would you like to run (CFB, CMBB, NFL)?")
        the_sport = input("")
        return the_sport

    def _set_year(self):
        the_year = 0
        while the_year == 0:
            print("Data currently available for the 2005-current seasons")
            print("What season would you like to run (YYYY or leave blank for current)?")
            a_year = input("")
            #print("year currently hardcoded to most recent")
            #a_year = ""
            if len(a_year) == 0:
                the_year = 'current'
            elif len(a_year) == 4:
                try:
                    a_year = int(a_year)
                    cur_year = datetime.now().year
                    if a_year >= 2005 and a_year < cur_year:
                        the_year = a_year
                    elif a_year >= cur_year:
                        print("You have picked a current or future date")
                        print("We dont have the sports almanac, and even if we did, its out of date and wheres my hoverboard")
                        print("fetching the most current data but need to retool this for season in progress file saves")
                        if a_year == 2019:
                            the_year = a_year
                        else:
                            the_year = "current"
                    else:
                        print("\nIt looks like you picked a year for which data isnt currently available.  Please try again.")
                except:
                    print("\nThat year doesn't seem to have worked.  Please try again.")
            else:
                print("\nPlease type a valid input")
        return the_year

    def _find_gp_tp(self,team,df):
        gp = df[df["away_team"] == team].index.tolist()+ df[df["home_team"] == team].index.tolist()
        #create an index of teams played
        tph = (df[df["away_team"] == team]["home_team"]).values.tolist()
        tpa = (df[df["home_team"] == team]["away_team"]).values.tolist()
        tp = tph+tpa
        return gp,tp

    def _scores_to_teams(self, df):
        hc = df["home_team"].value_counts()
        ac = df["away_team"].value_counts()

        #atc is All Teans Count
        atc = (hc + ac).fillna(hc).fillna(ac)

        teams = {}
        for team in atc.items():
            #print(team[0])
            # define team data struct here
            teams[team[0]] = Team(team)
            gp, tp = self._find_gp_tp(team[0], df)
            teams[team[0]].set_games_played(gp,tp)
        return teams


    def _gof(self, ap, hp):
        """
        Game outcome Function given the score of a game
        Args:
            ap: away points
            hp: home points
        Returns:
            gof: the value returned by the game outcome function
        """
        if hp != ap:
            ha = hp*ap
            hhh = hp*hp*hp
            gof = (49.0 + ha + hhh) / (2.0 * (49.0 + ha) + hhh + ap*ap*ap)
        else:
            gof = 0.5
        return gof


    def _findteamsgroups(self):
        #a = datetime.now()
        prototeams = []
        grpcntr = 0
        for team in self.teams:
            # just need to iterate through and compare each team with the dijkstra to the group prototype list
            if self.teams[team].group == 0:
                #set first team as prototyoe team
                if len(prototeams) == 0:
                    grpcntr +=1
                    prototeams.append([team,grpcntr,1])
                    self.teams[team].set_group(grpcntr)
                else:
                    lpt = len(prototeams)
                    forcntr = 1
                    tgl = 0
                    for l in range(lpt):
                        forcntr += 1
                        tmsgraph = self.graph.dijkstra(team,prototeams[l][0])
                        tgl = max(tgl,len(tmsgraph))
                        if tgl == 1 and lpt < forcntr:
                            #time to set a new group
                            grpcntr +=1
                            prototeams.append([team,grpcntr,1])
                            self.teams[team].set_group(grpcntr)
                        else:
                            prototeams[l][0] = tmsgraph[0]
                            for tms in tmsgraph:
                                if self.teams[tms].group != prototeams[l][1]:
                                    self.teams[tms].set_group(prototeams[l][1])
                                    prototeams[l][2] +=1
                                    for opps in self.teams[tms].opponents:
                                        if self.teams[opps].group != prototeams[l][1]:
                                            self.teams[opps].set_group(prototeams[l][1])
                                            prototeams[l][2] +=1
                            if self.teams[team].group != 0:
                                break
        #b = datetime.now()
        #timeDif(a,b)
        return prototeams


    def _team_rank_loop(self, team, final=False):
        #a = datetime.now()

        sos = 0.0
        sosw = 0.0
        sosl = 0.0
        wpts = 0.0
        lpts = 0.0
        onorm = 0.0
        bw = ('',0.0)
        wl = ('',9999.0)
        bt = ('',0.0)
        wt = ('',9999.0)
        w = 0
        l = 0
        t = 0
        lgp = self.teams[team].ngp
        ooe = self._odd_or_even
        #print(self.teams[team].gamedf['opponent'])
        #opp = self.teams[team].gamedf['opponent'].tolist()
        #print("before game loop")
        #b = datetime.now()
        #timeDif(a,b)

        for game in self.teams[team].gamedf.iterrows():
            
            opprating, oppsos = self.teams[game[1]['opponent']].return_bins(ooe)
            sos += opprating

            onorm += (oppsos*opprating)
            #onorm += (oppsos+opprating)/2
            if  game[1]['pa'] <  game[1]['pf']:
                #win
                sosw += opprating
                if opprating > bw[1]:
                    bw = (game[1]['opponent'],opprating)
                w+=1
            elif  game[1]['pa'] > game[1]['pf']:
                #loss
                sosl += opprating
                if opprating < wl[1]:
                    wl = (game[1]['opponent'],opprating)
                l+=1
            elif game[1]['pa'] ==  game[1]['pf']:
                #tie treated as half win and half loss
                sosw += opprating/2
                sosl += opprating/2
                if opprating > bt[1]:
                    bt = (game[1]['opponent'],opprating)
                if opprating < wt[1]:
                    wt = (game[1]['opponent'],opprating)
                t+=1
                '''
                    print(game[1]['opponent'],team)
                    print('there shouldnt be ties in college football')
                    print('ties may need to be handled if this is extended to other sports')
                '''
            else:
                print('this isnt a win loss or tie, weird')




        if t>0:     #if a team has no wins or loses but has ties set these values
            if w==0:
                bw = bt
            if l==0:
                wl = wt
        w_eff = (w+t/2)
        l_eff = (l+t/2)

        if lgp != w+l+t:
            #this is nothing but a sanity check
            print('something is going wrong adding up wins and losses and ties')
        if w==0:
            bw = wl
            sosw = wl[1]
            sosl /=l_eff
        elif l==0:
            wl = bw
            sosl = bw[1]
            sosw /=w_eff
        elif w == 0 and l == 0:
            print('this team hasnt played so i guess we have to handle that now')
        else:
            sosw /=w_eff
            sosl /=l_eff

        l_over_lpg = ((1.0+l_eff)/(2.0+lgp))
        w_over_lpg = ((1.0+w_eff)/(2.0+lgp))

        #try tempering these values in different ways
        wpts = l_over_lpg*sosw + w_over_lpg*bw[1]
        lpts = w_over_lpg*sosl + l_over_lpg*wl[1]

        #further refinements to try to rankings
        wp = 2.0*w_over_lpg*wpts
        lp = 2.0*l_over_lpg*lpts

        rating = rate(self._ar[self._odd_or_even], onorm, sos, w_eff, l_eff, lgp, wp, lp)
        sos /=lgp
        onorm /=lgp

        self.teams[team].sosbin[self._even_or_odd] = sos
        self.teams[team].ratingbin[self._even_or_odd] = rating
        if final:
            self.teams[team].sos = sos
            self.teams[team].sosw = sosw
            self.teams[team].sosl = sosl
            self.teams[team].wpts = wpts
            self.teams[team].lpts = lpts
            self.teams[team].onorm = onorm
            self.teams[team].bw = bw
            self.teams[team].wl = wl
            self.teams[team].wins = w
            self.teams[team].loses = l
            self.teams[team].ties = t
            self.teams[team].rating = rating
            
        rnkdff = abs(self.teams[team].ratingbin[self._even_or_odd]-self.teams[team].ratingbin[self._odd_or_even])
        #print("end of one rank loop")
        #z = datetime.now()
        #timeDif(a,z)
        return rating, rnkdff


    def _run_season_rankings(self):
        end_con = False
        ar2c = 0.0
        rank_diff = 1
        lt = len(self.teams)
        interation_counter = 0
        rtm = random.choice(list(self.teams.keys()))
        print(self.teams[rtm].name)
        team_list = list(self.teams)
        rnk_outpts = [0]*len(team_list)
        done_cntr = 0
        while (rank_diff > 1.0e-15 and interation_counter<2500 and rank_diff !=0.0) and done_cntr<25:
            x = datetime.now()
            interation_counter += 1
            rd = 0.0
            #print(self._ar[self._odd_or_even])
            #rnk_outpts = list(map( self._team_rank_loop,team_list))
            #rnk_outpts = [self._team_rank_loop(x) for x in team_list]
            
            for i in range(len(team_list)):
                rnk_outpts[i] = self._team_rank_loop(team_list[i],final=done_cntr)
            #print(rnk_outpts)
            y = datetime.now()
            timeDif(x,y)

            self._ar[self._even_or_odd] = sum(i for i, j in rnk_outpts)/lt

            rd = sum(j for i, j in rnk_outpts)
            if rd == rank_diff and self._ar[self._even_or_odd]+self._ar[self._odd_or_even] == ar2c:
                print("we should really go ahead and stop now")
                end_con = True
            ar2c = self._ar[self._even_or_odd]+self._ar[self._odd_or_even]
            self._ar[self._odd_or_even] = 0
            print((interation_counter,rd,self._ar[self._even_or_odd], done_cntr)) #,self.teams[rtm].ratingbin))
            #setting or resetting end paramster
            self._odd_or_even = (self._even_or_odd)
            self._even_or_odd = (self._odd_or_even +1)%2
            rank_diff = rd
            if end_con:
                rank_diff = 0.0
            if ((rank_diff < 1.0e-12 or  interation_counter>100000) or rank_diff ==0.0):
                done_cntr += 1
            else:
                done_cntr = 0
            #z = datetime.now()
            #timeDif(y,z)
            #timeDif(x, z)
        #set the any team properties that weren't already set
        rd = 0.0
#        for i in range(2):
#            for team in self.teams:
#                rnk, rnkdff = self._team_rank_loop(team, True)
#                self._ar[self._even_or_odd] += rnk
#                rd += rnkdff
#            print(('last',rd, self._ar[self._even_or_odd]/lt,self.teams[rtm].ratingbin))
        teamsdf = pd.DataFrame(columns=('name','rating','sos','onorm','w','l','sosw','sosl','bwop','bw','wlop','wl','wpts','lpts'), index=range(0, lt))
        n = 0
        for team in self.teams:
            teamsdf['name'][n] = self.teams[team].name
            teamsdf['rating'][n] = self.teams[team].rating
            teamsdf['sos'][n] = self.teams[team].sos
            teamsdf['onorm'][n] = self.teams[team].onorm
            teamsdf['w'][n] = self.teams[team].wins
            teamsdf['l'][n] = self.teams[team].loses
            teamsdf['sosw'][n] = self.teams[team].sosw
            teamsdf['sosl'][n] = self.teams[team].sosl
            teamsdf['bwop'][n] = self.teams[team].bw[0]
            teamsdf['bw'][n] = self.teams[team].bw[1]
            teamsdf['wlop'][n] = self.teams[team].wl[0]
            teamsdf['wl'][n] = self.teams[team].wl[1]
            teamsdf['wpts'][n] = self.teams[team].wpts
            teamsdf['lpts'][n] = self.teams[team].lpts
            n = n+1
        for dkeys in ['rating','sos','onorm','sosw','sosl','bw','wl','wpts','lpts']:
            teamsdf[dkeys] = teamsdf[dkeys].astype(float)
        for dkeys in ['w','l']:
            teamsdf[dkeys] = teamsdf[dkeys].astype(int)
        teamsdf['rank'] = teamsdf['rating'].rank(ascending=0)
        teamsdf['sos_rank'] = teamsdf['sos'].rank(ascending=0)
        teamsdf['onorm_rank'] = teamsdf['onorm'].rank(ascending=0)
        return teamsdf

    def _rel_pwr(self, R1, R2):
        #rel_pwr=(R2 - R1)/5.0
        rel_pwr=((R2 - R1)**3)/5.0
        L=1
        k=2
        rel_pwr = 2*(L/ (1+np.exp(-k*(rel_pwr)))) - 1
        print(R2 - R1)
        print(rel_pwr)
        return rel_pwr

    def _scrPwr (self, Pts, R1, R2):
        rel_rate = self._rel_pwr(R1, R2)
        return (Pts * ((m.exp(rel_rate)) / (m.cosh(rel_rate))))

    def _prdctPF (self, P1, P2, R1, R2):
        rel_rate = self._rel_pwr(R1, R2)
        #print(P1, P2, R1, R2)
        return ( 0.5 * (P1 + P2) * (m.cosh(rel_rate) / m.exp(rel_rate)))

    def std_rating(self, rating):
        return (rating - self.rnk_mean)/(self.rnk_std)

    def predict_game(self,team1,team2):
        rstd1 = self.std_rating(self.teams[team1].rating)
        rstd2 = self.std_rating(self.teams[team2].rating)
        s1 = self._prdctPF(self.teams[team1].sco,self.teams[team2].scd,rstd1,rstd2)
        s2 = self._prdctPF(self.teams[team2].sco,self.teams[team1].scd,rstd2,rstd1)
        outcome = team1 + " " + str(s1) + " v. " + team2 + " " + str(s2)
        w_bool = (s1>s2)
        l_bool = (s1 < s2)
        return outcome, w_bool, l_bool

    def _power_indexer(self):
        #for teams in list
        team_count = 0
        for team in self.teams.keys():
            sum_pf = 0.0
            sum_pa = 0.0
            sco = 0.0
            scd = 0.0
            ng = self.teams[team].ngp
            #for opponents
            own_std_rating = self.std_rating(self.teams[team].rating)
            for game in self.teams[team].gamedf.itertuples():
                #sum off and def metrics
                opp_std_rating = self.std_rating(self.teams[game.opponent].rating)
                gpf = game.pf
                gpa = game.pa
                sum_pf = sum_pf + gpf
                sum_pa = sum_pa + gpa
                sco = sco + self._scrPwr(gpf, own_std_rating, opp_std_rating)
                scd = scd + self._scrPwr(gpa, opp_std_rating, own_std_rating)
            pf = sum_pf/ng
            pa = sum_pa/ng
            sco = sco/ng
            scd = scd/ng
            self.teams[team].pf = pf
            self.teams[team].pa = pa
            self.teams[team].sco = sco
            self.teams[team].scd = scd
            team_count = team_count+1
        return team_count


    def _set_season(self):
        df = _wp.get_scores(self._sport, self._year)
        df['gof'] = df['away_score'].combine(df['home_score'], func=self._gof)
        teams = self._scores_to_teams(df)
        tg = []
        for team in teams:
            for opps in teams[team].opponents:
                tg.append((team,opps,1))
        graph = dij.Graph(tg)
        return teams, df, graph

    def _process_season(self):
        prototeams = self._findteamsgroups()
        print(str(len(prototeams)) + ' team groups found')
        #print(prototeams)
        #set which group of teams to rank
        pt = prototeams[0]
        for group in prototeams:
            if group[2] > pt[2]:
                pt = group
        #remove other teams and their games
        delteam = []
        for team in self.teams:
            tg = self.teams[team].group
            if tg != pt[1]:
                delteam.append(team)
                self.df = self.df[self.df["home_team"].str.lower().str.strip() != team]
                self.df = self.df[self.df["away_team"].str.lower().str.strip() != team]
        for dt in delteam: del(self.teams[dt])
        #reindex df and redo each teams games attribute
        self.df = self.df.reset_index(drop=True)
        for team in self.teams:
            #create list of indexes for games played
            gp, tp = self._find_gp_tp(team, self.df)
            self.teams[team].set_games_played(gp,tp)
            tdf = self.df[(self.df['home_team'] == team)].append(self.df[(self.df['away_team'] == team)])
            #print(tdf)
            self.teams[team].set_df(tdf)
        
        teamsdf = self._run_season_rankings()
        #power indexer is a measure of offensive and defensive power
        self.rnk_mean = teamsdf['rating'].mean()
        self.rnk_std = teamsdf['rating'].std()
        
        tc = self._power_indexer()
        print(tc)
        return teamsdf

    def print_games(self):
        for game in self.df.itertuples():
            print(game)
        return(True)


    def print_teams(self):
        for team in self.teams:
            self.teams[team].print_team()
        return True

if __name__ == "__main__":
    season = Season()

'''
pr.disable()
s = io.StringIO()
sortby = 'cumtime'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
f = open('stats.txt', 'w')
f.write(s.getvalue())
f.close()
print(s.getvalue())
'''
