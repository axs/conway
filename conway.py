
"""
Conway's Game of Life (http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules)
The universe of the Game of Life is an infinite two dimensional orthogonal grid of square cells,
each of which is in one of two possible states, alive or dead. Every cell interacts with its eight
neighbors, which are the cells that are horizontally, vertically, or diagonally adjacent. At each
step in time, the following transitions occur:
Any live cell with fewer than two live neighbors dies, as if caused by under population.
Any live cell with two or three live neighbors lives on to the next generation.
Any live cell with more than three live neighbors dies, as if by overcrowding.
Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
The initial pattern constitutes the seed of the system. The first generation is created by applying
the above rules simultaneously to every cell in the seed.births and deaths occur
simultaneously, and the discrete moment at which this happens is sometimes called a tick (in
other words, each generation is a pure function of the preceding one). The rules continue to be
applied repeatedly to create further generations.
There should be some way to pass in a tab delimited file containing the list of coordinates of the initial
live cells. There should also be some way to specify the number of generations to run, after which the
program produces a similar tab delimited format describing the end state of the grid.
Sample input file:
# this is a basic glider, centered at the grid origin
# (first column is x-coord, second column is y-coord)
-1 -1
0 -1
0 1
1 -1
1 0

"""

#author:

import numpy as np
import pandas as pd


class Conway(object):
    def __init__ (self,inputfile,ngens, output):
        self.output  = output
        self.numgens = ngens
        initial      = self.parsefile(inputfile)
        self.board   = np.zeros((9,9),dtype=bool)
        origin = (4,4)
        for x,y in initial:
            self.board[origin[0]+ x , origin[0]+ y ]=True

    def parsefile(self,f):
        i = pd.read_fwf(f,header=None)
        i.dropna(inplace=True)
        return i.values.tolist()

    def generation(self):
        neighbors = sum(np.roll(np.roll(self.board, i, 0), j, 1)
                         for i in (-1, 0, 1) for j in (-1, 0, 1)
                         if (i != 0 or j != 0))
        self.board = (neighbors == 3) | (self.board & (neighbors == 2))
        return self.board

    def run(self):
        for g in range(self.numgens):
            self.generation()
        self.writeresults()

    def writeresults(self):
        pd.DataFrame(self.board.astype(int)).to_csv(self.output,sep='\t', index=False,header=False)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Conway AlphaGen')
    parser.add_argument('-f','--file',dest='file', help='Input file for initial positions', required=True)
    parser.add_argument('-N','--numgen',type=int,dest='generations', help='Number of generations to run', default=1)
    parser.add_argument('-o','--output',dest='output', help='Output file', required=True)
    args = parser.parse_args()

    c = Conway(args.file, args.generations,args.output)
    c.run()

