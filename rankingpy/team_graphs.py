# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 21:01:29 2017

@author: Mike
"""

import networkx as nx
import matplotlib.pyplot as plt


G=nx.Graph()
G.add_edges_from([(edge.start, edge.end) for edge in trr.graph.edges if edge.start in trr.teams.keys()])
G.number_of_nodes()
G.number_of_edges()

fig, ax = plt.subplots(figsize=(36,25))

ACC = ['boston college',
 'clemson',
 'florida st',
 'louisville',
 'north carolina st',
 'syracuse',
 'wake forest',
 'duke',
 'georgia tech',
 'miami fl',
 'north carolina',
 'pittsburgh',
 'virginia',
 'virginia tech']
SEC = ['florida',
 'georgia',
 'kentucky',
 'missouri',
 'south carolina',
 'tennessee',
 'vanderbilt',
 'alabama',
 'arkansas',
 'auburn',
 'lsu',
 'mississippi',
 'mississippi st',
 'texas a&m']
PAC12 = []
BIG10 = ['indiana',
 'maryland',
 'michigan',
 'michigan st',
 'ohio state',
 'penn state',
 'rutgers',
 'illinois',
 'iowa',
 'minnesota',
 'nebraska',
 'northwestern',
 'purdue',
 'wisconsin']
BIG12 = []
BIGEAST = []

fig, ax = plt.subplots(figsize=(36,25))

cm = []
ns = []
for x in G.nodes():
    '''if x == "oklahoma":
         cm.append([1.0,0.0,0.0]) #red
         ns.append(15)
    elif x == "alabama":
         cm.append([0.0,1.0,0.0])    #green
         ns.append(15)
    elif x == "ohio state":
         cm.append([0.0,0.0,1.0])    #blue
         ns.append(15)
    elif x == "central florida":
         cm.append([1.0,1.0,0.0])    #yellow
         ns.append(15)
    el
    '''
    if x == "indiana":
        cm.append([1.0,0.0,1.0]) #magenta
        ns.append(15)
    elif x == "virginia tech":
        cm.append([1.0,0.5,0.0]) #orange
        ns.append(15)
    elif x == "notre dame":
        cm.append([1.0,1.0,0.0])    #yellow
        ns.append(15)
    elif x in ACC:
        cm.append([1.0,0.0,0.0]) #red
        ns.append(15)
    elif x in SEC:
        cm.append([0.0,1.0,0.0])    #green
        ns.append(15)
    elif x in BIG10:
        cm.append([0.0,0.0,1.0])    #blue
        ns.append(15)
    #elif trr.rankings['rank'][trr.rankings.query('name == "' + x + '"').index.values[0]] <= 25:
    #    cm.append([0.0,0.0,0.0]) #black
    #    ns.append(10)
    else:
        cm.append([0.6,0.6,0.6])
        ns.append(2)

nx.draw_spring(G, with_labels=False, node_size=ns, font_size=4, width=0.1, ax=ax, node_color=cm)
