import pandas
import numpy
from scipy import stats
c0=pandas.read_csv("C:/Users/Rui/Desktop/nc0.csv")
V=c0['Val'].as_matrix()
c0F=c0['Freq'].tolist()
c0F=[int(x/250) for x in c0F]
c0=numpy.repeat(V,c0F,axis=0)
c2=pandas.read_csv("C:/Users/Rui/Desktop/nc2.csv")
c2F=c2['Freq'].tolist()
c2F=[int(x/250) for x in c2F]
c2=numpy.repeat(V,c2F,axis=0)
print(stats.ks_2samp(c0,c2))
#1000 for coding
