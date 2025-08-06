import subprocess
import os
import pathlib
import math
from functions import *
import time
from Hand import Hand

def fts(lst):
    return ' '.join(str(x) for x in lst)

class Tree(object):
    def __init__(self, parser, spot, node, pos, step):
        self.parser = parser
        self.connection = parser.connection
        self.spot = spot
        self.node = node
        self.step = step
        if pos == 0:
            self.poshero = "OOP"
            self.posvln = "IP"
            self.eqs = self.spot.eqs
        else:
            self.poshero = "IP"
            self.posvln = "OOP"
            self.eqs = 1 - self.spot.eqs.T
        self.data = []
        self.data.append(pos)
        # comment


    def make(self):
        self.strhero = get_range(self.connection, self.poshero, self.node)
        self.strvln = get_range(self.connection, self.posvln, self.node)
        self.tabhero = str_to_tab(self.strhero)
        self.tabvln = str_to_tab(self.strvln)
        if sum(self.tabhero) < 5 or sum(self.tabvln) < 5:
            # print(self.node,"NO")
            return
        set_range(self.connection,self.poshero,self.strhero)
        set_range(self.connection, self.posvln, self.strvln)
        self.eqhero = get_calc_eq(self.connection,self.poshero)
        self.eqvln = get_calc_eq(self.connection,self.posvln)
        self.ponderhero,self.pondervln = get_ponder(self.eqs,self.eqhero,self.tabvln,self.tabhero,self.parser.inter)
        self.make_spr()
        self.make_range_vs_range(5)

        self.sepvln = split_range(self.tabvln, self.pondervln, 12)
        self.rivers = get_rivers(self.connection, 500, self.poshero)
        self.riversvln = get_rivers(self.connection, 500, self.posvln)
        self.make_rivers()
        self.make_targets()

        self.make_hands()


    def make_range_vs_range(self, n):
        sephero = split_range(self.tabhero, self.ponderhero, n)
        sepvln = split_range(self.tabvln, self.pondervln, n)
        for i in range(n):
            for j in range(n):
                res = range_vs(self.eqs, sephero[i], sepvln[j], self.parser.inter)
                self.data.append(res)

    def make_spr(self):
        bets = self.node.split(":")
        bet = 0
        lastbet = 0
        if bets[-1][0] == "b":
            bet = float(bets[-1][1:])
        if bets[-2][0] == "b":
            lastbet = float(bets[-2][1:])
        effstack = self.spot.startstack - lastbet
        self.pot = self.spot.startpot + 2 * lastbet
        bet -= lastbet
        spr = effstack / self.pot
        self.data.append(spr)
        bpr = bet / self.pot
        self.bpr = bpr
        self.data.append(bpr)
        minbet = max(bet-lastbet,self.parser.bb)
        minbet = minbet / self.pot
        self.data.append(minbet)

    def make_hands(self):
        for i in range(1326):
            if self.tabhero[i] > 0:
                hand = Hand(self.parser, self.spot, self, i)
                hand.make()

    def make_targets(self):
        children = get_children(self.connection, self.node)
        self.bets = []
        self.actions = []
        self.evs = []
        for child in children:
            strbet = child.split(":")[-1]
            if strbet != "f":
                bet = 0
                if strbet[0] == "b":
                    bet = float(strbet[1:]) / self.pot - self.bpr
                res = self.connection.command(line="calc_ev " + self.poshero + " " + child)
                self.actions.append(child)
                self.bets.append(bet)
                self.evs.append(str_to_tab(res[0]))


    def make_rivers(self):
        moy,std = get_std_rivers(self.rivers.T)
        self.data.append(moy)
        self.data.append(std)
        if self.node == "r:0":
            print("HERO MOYENNE:", moy)
            print("HERO ECART TYPE:", std)
        moy, std = get_std_rivers(self.riversvln.T)
        self.data.append(moy)
        self.data.append(std)
        if self.node == "r:0":
            print("VLN MOYENNE:", moy)
            print("VLN ECART TYPE:", std)







