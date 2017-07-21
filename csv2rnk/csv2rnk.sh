#!/bin/bash
#converting a list of target genes as DEseq2 generated csv file into RNK file the GSEA software requires
export LC_ALL=C

usage(){
echo "Usage: input.csv"
echo ""
exit 2
}

START=$(date +%s)
##checking for correct arguments
  if [ "$#" != "1" ]
  then
	usage
	exit 1
  fi

  export filename=$1

##parameters for DEseq2 output
genecol=1
foldcol=3
pvalcol=7

##parameters for edgeR, unhide if needed
##genecol=1
##foldcol=2
##pvalcol=5

##parameters for sleuth, unhide if needed
##genecol=2
##foldcol=5 ##"b"
##pvalcol=4

##remove NA pval (DEseq2 independent filtering)
awk -F "," <$1 '($'$pvalcol' ~ !/NA/) {print}' >/tmp/out

##sorting by foldchange, can also be done with pval, or combination
awk -F "," </tmp/out '{print $'$genecol' "\t" $'$foldcol'}' >/tmp/out2
sort -k2 -n /tmp/out2 > /tmp/out
awk -F "\"" </tmp/out '{print $2 $3}' >output.rnk
