c0<-read.table("C:/Users/Rui/Desktop/nc0.csv",sep=",",header=TRUE)
c0$Freq=c0$Freq/100
c0vec=rep(c0$Val,c0$Freq)
c2<-read.table("C:/Users/Rui/Desktop/nc2.csv",sep=",",header=TRUE)
c2$Freq=c2$Freq/100
c2vec=rep(c2$Val,c2$Freq)
cresult=ks.test(c0vec,c2vec,exact=TRUE)
cresult$p.value
