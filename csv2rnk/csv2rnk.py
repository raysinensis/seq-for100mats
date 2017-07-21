import pandas as pd
import numpy as np

df=pd.read_csv("C:/Users/Rui/Desktop/test-DEseq2.csv")
df['sign']=np.where(df['log2FoldChange']>0, 1, -1)
df['metric']=-np.log10(df['padj'])*df['sign']
df2=df[['Unnamed: 0', 'metric']]
df2=df2.fillna(value=0)
df3=df2.sort(columns='metric')
df3.to_csv("file.rnk", sep='\t', header=False, index=False)
