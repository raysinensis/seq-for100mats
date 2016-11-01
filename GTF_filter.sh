#!/bin/bash
#simple couple lines using awk to filter GTF files to exclude or include genes/types of interest

##########################
## Usage
##########################
usage() {
  echo "Usage: `input_name $0` include/exclude `keyword` `output_name $0`"
  echo "Creates a new GTF file either excluding or including key words"
  echo ""
  echo "example: genes.gtf exclude protein_coding noncoding.gtf"
  echo ""
  echo "   The expected inputs are:"
  echo "      arg1=input name"
  echo "      arg2=include, exclude, or list (provided in arg3)"
  echo "      arg3=keyword, can be part of feature name or type"
  echo "      arg4=output name"
  echo ""
  exit 2
}

##checking for correct arguments
  if [ "$#" != "4" ]
  then
	usage
	exit 1
  fi

  export input=$1
  	 output=$4
  	 io=$2
  	 word=$3

##simple filtering using awk
##to include entries containing keyword given
  if [ $io = "include" ]
  then
	echo "filtering for $3"
	awk <$1 '/'"$word"'/ {print}' > $4
##to exclude entries containing keyword given
  elif [ $io = "exclude" ]
  then
	echo "filtering out $3"	
	awk <$1 '!/'"$word"'/ {print}' > $4
##to filter gtf with a list of genes
  elif [ $io = "list" ]
  then
 	awk -F, 'NR == FNR {list["\""$1"\""]; next}
                {for (entry in list)
                if ($0 ~ entry) 
                print $1}' $3 $1 >$4
##feature not currently covered
  else
	echo "third argument not include nor exclude"
  fi
