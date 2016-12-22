#!/bin/bash
#extracting 5',3'UTR and splicing info from GTF annotations

##########################
## Usage
##########################
usage() {
  echo "Usage: $0 input.gtf include/exclude keyword output.gtf"
  echo "Creates a new GTF file either excluding or including key words"
  echo ""
  echo "example: genes.gtf"
  echo ""
  echo "   The expected inputs are:"
  echo "      arg1=input name"
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

##logging arguments
  export input=$1

##generate list of start and stop codon
  awk <$input -F "," '/'"start_codon"'/{print $1}' > startcodon.csv
  awk <$input -F "," '/'"stop_codon"'/{print $1}' > stopcodon.csv
  awk <$input -F "," '/'"UTR"'/{print $1}' > UTR.csv

##split out +/- strand genes
  awk <$input -F '\t' '$7 ~ /\+/ {print}' > plusstrand.csv
  awk <$input -F '\t' '$7 ~ /\-/ {print}' > minusstrand.csv

##processing + strand genes, into 2 files
  awk <plusstrand.csv -F '[\t;]' '{print $13}' > try.txt

##list of genes
  awk <plusstrand.csv -F 'gene_name \"' '{print $2}' > /tmp/genelist
  awk </tmp/genelist -F '\"; ' '{print $1}' | uniq > plusgenes.txt
  awk <minusstrand.csv -F 'gene_name \"' '{print $2}' > /tmp/genelist
  awk </tmp/genelist -F '\"; ' '{print $1}' | uniq > minusgenes.txt

##list of genes with multiple exons
  awk <$input -F 'gene_name \"' '/'"exon_number \"2\""'/{print $2}' > /tmp/genelist
  awk </tmp/genelist -F '\"; ' '{print $1}' | uniq > splicedgenes.txt

##calulating time lapsed
END=$(date +%s)
DIFF=$((END - START))
echo total runtime $DIFF"s"
