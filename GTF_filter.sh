#!/bin/bash
#simple couple lines using awk to filter GTF files to exclude or include genes/types of interest

##########################
## Usage
##########################
usage() {
  echo "Usage: $0 input.gtf include/exclude keyword output.gtf"
  echo "Creates a new GTF file either excluding or including key words"
  echo ""
  echo "example: genes.gtf exclude protein_coding noncoding.gtf"
  echo ""
  echo "   The expected inputs are:"
  echo "      arg1=input name"
  echo "      arg2=include/exclude, or list/delist/append (provided in arg3)"
  echo "      arg3=keyword, can be part of feature name or type"
  echo "      arg4=output name"
  echo ""
  exit 2
}

START=$(date +%s)
##checking for correct arguments
  if [ "$#" != "4" ]
  then
	usage
	exit 1
  fi

##logging arguments
  export input=$1
  	 output=$4
  	 io=$2
  	 word=$3

##for list formats that are not plain text
##for CSV tab-deliminated
  name=$3
  format="${name##*.}"
  if [ $format = "csv" ]
  then echo "coverting csv..."
  awk <$3 -F "," '{print $1}' > /tmp/csv
  word=/tmp/csv
  count=$(wc -l < /tmp/csv)
  counter=1
  echo $count "genes..."
  fi

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
##in cases where genes with additional characters are not wanted, e.g. RN7SL1, but not RN7SL186, use: sh GTF_filter.sh genes.gtf include RN7SL1\" temp
  elif [ $io = "list" ]
  then
 	if [ $count -lt 10 ]
	then    
		echo "in simple mode..."
		awk -F, 'NR == FNR {list["\""$1"\""]; next}
                {for (entry in list)
                if ($0 ~ entry) 
                print $1}' $word $1 > $4
	else    
		echo "in complex mode..."
		while [ "$counter" -le "$count" ]
		do
			word=$(awk 'FNR=='"$counter"' {print}' /tmp/csv)
  			counter=$((counter+1))
			awk <$1 '/'\""$word"\"'/ {print}' >> $4
		done
	fi

##to filter out a list of genes
  elif [ $io = "delist" ]
  then
 	awk -F, 'NR == FNR {list["\""$1"\""]; next}
                {for (entry in list)
                if ($0 ~ entry) 
		$mark="\"true\""}
                {print}' $word $1 > /tmp/log
	echo "outputting..."
	awk -F, < /tmp/log '!/"true"/ {print}' > $4

##append list to gtf, can be combined with include function to move entries between gtf files
##depending on downstream application, may require additional step: bedtools sort -i in.gtf > out.gtf
  elif [ $io = "append" ]
  then
	awk < $word '{print}' >> $4

##feature not currently covered
  else
	echo "third argument not supported"
  fi

##calulating time lapsed
END=$(date +%s)
DIFF=$((END - START))
echo total runtime $DIFF"s"
