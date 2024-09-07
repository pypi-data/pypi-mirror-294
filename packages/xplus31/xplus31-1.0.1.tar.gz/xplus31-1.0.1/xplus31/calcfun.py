from .src.file5 import plus5
from .src.file7 import plus7
from .src.minus.file_1 import minus1
from .src.merge.file13 import plus13
from .src.merge.deeper.file31 import plus31
from .output import print_clr
from .src.merge.deeper import const
print_clr('''
    now you can directly use these under module 'calcfun':
    plus5,plus7,minus1,plus13,plus31,const,print_clr
''', fgclr = 5)