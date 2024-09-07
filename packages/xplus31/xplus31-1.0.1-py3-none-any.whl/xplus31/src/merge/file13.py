from ..file7 import plus7
from ..minus.file_1 import minus1
from .hint import hint
def plus13(x):
    'lambda x : x+13 (with an ester-egg)'
    hint('using function plus13')
    return minus1(plus7(plus7(x)))

