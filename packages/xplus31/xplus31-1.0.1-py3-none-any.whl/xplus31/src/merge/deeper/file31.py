from ..file13 import plus13
from ...file5 import plus5
from ....output import print_clr
import numpy as np # test requirements
import sys,os
print_clr('This is +31 imported for the first time!',__name__,sys.path[0],os.path.abspath('..'),sep='\n')
def plus31(x):
    'lambda x : x+31'
    return plus5(plus13(plus13(x)))
def matrix_2x2():
    'test numpy'
    return np.ones((2,2))