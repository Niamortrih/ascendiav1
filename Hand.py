import subprocess
import os
import pathlib
import random
import math
import numpy as np
from scipy.stats import skew, kurtosis
from functions import *

def print_lines(lines):
    for line in lines:
        print(line)

class Hand(object):
    def __init__(self, parser, spot, tree, num):
        self.parser = parser
        self.spot = spot
        self.tree = tree
        self.num = num
        self.strhand = self.parser.list_hands[num]
        self.data = []

    def make(self):
        self.make_vs_ranges()
        self.make_rivers()
        # if random.randint(0,90) == 87:
        #     print(self.strhand, self.data)
        self.make_data()


    def make_vs_ranges(self):
        for i in range(len(self.tree.sepvln)):
            res = hand_vs_range(self.tree.eqs, self.num, self.tree.sepvln[i], self.parser.inter)
            self.data.append(res)
            block = blocker(self.num,self.tree.sepvln[i],self.parser.inter)
            self.data.append(block)

    def make_rivers(self):
        rivers = self.tree.rivers[:, self.num]
        self.data.append(np.nanmean(rivers))
        self.data.append(np.nanstd(rivers))
        for i in range(5,100,5):
            self.data.append(np.nanpercentile(rivers, i))
        self.data.append(skew(rivers, nan_policy='omit'))
        self.data.append(kurtosis(rivers, nan_policy='omit'))

    def make_data(self):
        for i in range(len(self.tree.actions)):
            action = self.tree.actions[i]
            bet = self.tree.bets[i]
            end = 0
            if self.tree.step != 0 and bet == 0:
                end = 1
            target = self.tree.evs[i][self.num] / self.tree.pot
            name = self.spot.filename + " " + action + " " + self.strhand
            inputs = self.tree.data + self.data + [bet,end]

            self.parser.names.append(name)
            self.parser.X.append(inputs)
            self.parser.y.append(target)
            self.spot.lines += 1
            # if random.randint(0,200) == 137:
            #     print(name, inputs, target)


