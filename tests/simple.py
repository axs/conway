
import sys
sys.path.append('../')
from nose.tools import *
import numpy as np
from conway import *

"""
Usage:  nosetests -v --nocapture simple.py
author:
"""

start = np.array([[False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False],
       [False, False, False,  True, False, False, False, False, False],
       [False, False, False,  True, False,  True, False, False, False],
       [False, False, False,  True,  True, False, False, False, False],
       [False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False]], dtype=bool)


c = Conway('test_input.tsv',1,'output.tsv')


def test_initial():
    assert_true( np.array_equal(c.board , start) )


def test_livecell_fewer_two_live_neighbors_dies():
    #Any live cell with fewer than two live neighbors dies, as if caused by under population.
    begin = np.array([ [False,  False, False, False ],
                       [False,  False, False, False ],
                       [False,  False,  True, False ],
                       [False,   True, False, False ],
                       [False,  False, False, False ],
                       [False,  False, False, False ]], dtype=bool)
    end =   np.array([ [False,  False, False, False ],
                       [False,  False, False, False ],
                       [False,  False, False, False ],
                       [False,  False, False, False ],
                       [False,  False, False, False ],
                       [False,  False, False, False ]], dtype=bool)
    c.board = begin
    c.generation()
    assert_true( np.array_equal(c.board , end) )




def  test_livecell_twoORthree_live_neighbors_lives():
    #Any live cell with two or three live neighbors lives on to the next generation.
    begin = np.array([ [False,  False, False, False ],
                       [False,  False, False, False ],
                       [False,  False,  True, False ],
                       [False,   True, False, False ],
                       [False,  True, False, False ],
                       [False,  False, False, False ]], dtype=bool)
    c.board = begin
    result = c.generation()
    assert_true( result[3][1] )



def test_livecell_morethree_live_neighbors_dies():
    #Any live cell with more than three live neighbors dies, as if by overcrowding.
    begin = np.array([ [False,  False, False, False ],
                       [False,  False, False, False ],
                       [True,  False,  True, False ],
                       [True,   True, False, False ],
                       [False,  True, False, False ],
                       [False,  False, False, False ]], dtype=bool)
    c.board = begin
    result = c.generation()
    assert_false( result[3][1] )


def test_deadcell_exactly_three_live_neighbors_alive():
    #Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
    begin = np.array([ [False,  False, False, False ],
                       [False,  False, False, False ],
                       [True,  False,  True, False ],
                       [True,   True, False, False ],
                       [False,  True, False, False ],
                       [False,  False, False, False ]], dtype=bool)
    c.board = begin
    result = c.generation()
    assert_true( result[3][2] )



def test_deadcell_exactly_three_live_neighbors_alive_NOT4():
    #Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
    begin = np.array([ [False,  False, False, False ],
                       [False,  False, False, False ],
                       [True,  False,  True,True ],
                       [True,   True, False, False ],
                       [False,  True, False, False ],
                       [False,  False, False, False ]], dtype=bool)
    c.board = begin
    result = c.generation()
    assert_false( result[3][2] )



