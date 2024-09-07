def print_clr(*args,sep=' ',fgclr=3,bgclr=3):
    'make your print colorful!'
    clrfmt = '\033['+str(bgclr)+str(fgclr)+'m'
    print(clrfmt+sep.join([str(s) for s in args])+'\033[0m')