import numpy as np
from itertools import product

b = np.array([[1],[1]])

r=[-1,0,1];b=(2==(n:=np.array([np.roll(b,s,r[1:])for s in filter(any,product(r,r))],dtype=int).sum(0)))&b|(n==3)