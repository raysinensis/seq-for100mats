#!/bin/bash
#converting a list of target genes as DEseq2 generated csv file into RNK file the GSEA software requires

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

awk -F "," <$1 '$'$foldcol'<0 {print $'$genecol' "\t" $'$foldcol'}' >/tmp/out
sort -k2 /tmp/out >output.txt
