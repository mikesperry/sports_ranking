
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from operator import itemgetter
import rankutils as _ru
import wolfeparser as _wp


def check_heteronyms(atc):
    teams1 = np.sort(atc.index)

    non_matches = []
    heteronyms = []
    #double_matches = []

    are_match = False
    is_checked = False
    has_a_match = False
    are_identical = False

    check_count = 0

    #last_teams = ["",""]
    # enumerating to eliminate double checking increases
    # complexity without justifyable speed increase
    for team1 in teams1:
        hetnyms = []
        has_a_match = False
        for team2 in teams1:
            are_match = False
            is_checked = False
            eob = False
            are_identical = False
            while not is_checked and not eob:
                if team1 == team2:
                    are_identical = True
                    are_match = True
                    has_a_match = True
                    is_checked = True
                elif ((team1.count(' ')) == (team2.count(' '))):
                    fr = fuzz.ratio(team1, team2)
                    fp = fuzz.partial_ratio(team1, team2)
                    if fr != 100 and fp == 100 and team1.count(' ') > 0:
                        #print(str(team1) + " " + str(team2) + " " + str(fr) + " " + str(fp))
                        w1 = team1.split()
                        w2 = team2.split()
                        are_abbrevs = True
                        for n in range(len(w1)):
                            fr = fuzz.ratio(w2[n], w1[n])
                            fp = fuzz.partial_ratio(w1[n], w2[n])
                            if _ru.is_abbrev(w2[n], w1[n]) or _ru.is_abbrev(w1[n], w2[n]):
                                pass
                                #print(str(w1[n]) + " " + str(w2[n]) + " " + str(fr) + " " + str(fp))
                            else:
                                #print(str(w1[n]) + " " + str(w2[n]) + " " + str(fr) + " " + str(fp))
                                are_match = False
                                are_abbrevs = False
                                is_checked = True
                                #print("that doesnt look like an abreviaton")
                        if are_abbrevs:
                            are_match = True
                            is_checked = True
                            has_a_match = True
                    elif fr == 100 and fp == 100:
                        are_match = True
                        is_checked = True
                        has_a_match = True
                    else:
                        are_match = False
                        is_checked = True
                else:
                    are_match = False
                    is_checked = True
                if is_checked:
                    if are_match:
                        if not are_identical:
                            #print("non-identical match " + str(team1) + " " + str(team2) + " " + str(fr) + " " + str(fp))
                            hetnyms.append(str(team1))
                            hetnyms.append(str(team2))
                        check_count = check_count + 1
                        #if str(team1) == last_teams[0] or str(team2) == last_teams[1] or str(team2) == last_teams[0] or str(team1) == last_teams[1]:
                        #    #print("double match " + str(team1) + " " + str(team2) + " and " + str(last_teams[0]) + " " + str(last_teams[1]))
                        #    double_matches.append([str(team1), str(team2), str(last_teams[0]), str(last_teams[1])])
                        # last_teams = [str(team1),str(team2)]
                    eob = True
                else:
                    print(str(team1) + " " + str(team2) + " werent checked")
                    eob = True
        if not has_a_match:
            check_count = check_count + 1
            print("nomatch " + str(team1))
            non_matches.append(str(team1))
        if len(hetnyms)>0:
            set_het = set(hetnyms)
            if set_het not in heteronyms:
                heteronyms.append(set_het)
    if len(non_matches) > 0:
        print("theres a non-match and that makes no sense")
    if len(heteronyms) > 0:
        print("extra teams likely")
    for n, nyms in enumerate(heteronyms):
        heteronyms[n] = []
        for names in nyms:
            heteronyms[n].append((names, atc[names]))
        heteronyms[n] = sorted(heteronyms[n],key=itemgetter(1), reverse=True)
    return heteronyms


if __name__ == "__main__":
    pass
