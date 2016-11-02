#!/bin/bash
#simple couple lines using awk to filter GTF files to exclude or include genes/types of interest

##########################
## Usage
##########################
usage() {
  echo "Usage: $0 input_name $0 output_name  on/off genome"
  echo "Creates rRNA.interval_list with GTF file plus UCSC database or genome.fa"
  echo ""
  echo "example: genes.gtf rRNA.interval_list on hg38"
  echo ""
  echo "   The expected inputs are:"
  echo "      arg1=input name"
  echo "      arg2=output name"
  echo "      arg3=on (from UCSC server) or off (from local .fa file)"
  echo "      arg4=genome name (if arg3=on) or .fa file name (if arg3=off)"
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
  	 output=$2
  	 onoff=$3
  	 key=$4

##create temp file with chromosome lengths information
  if [ $onoff = "on" ]
  then
	echo "downloading $4 info"
	mysql  --user=genome --host=genome-mysql.cse.ucsc.edu -A -D $4 -e 'select chrom,size from chromInfo' > /tmp/chromesome_sizes
	awk 'NR>1' /tmp/chromesome_sizes > chromesome_sizes

##genome.fa file looks like this: >chr1  AC:CM000663.2  gi:568336023  LN:248956422  rl:Chromosome  M5:6aef897c3d6ff0c78aff06ac189178dd  AS:GRCh38
  elif [ $onoff = "off" ]
  then
	echo "extracting chromosome lengths info from .fa file"
  	awk < $4 '/>/ {print substr($1,2) "\t" substr($4,4)}' > chromesome_sizes
  else
	echo "wrong parameters"
  fi

##putting chromosome lengths info into file
  awk <chromesome_sizes '// {print "@SQ\tSN:" $1 "\tLN:" $2}' > /tmp/$2

##filtering rRNA entries in the GTF file
  awk <$1 '/rRNA/ && ($3 == "transcript") {print $1 "\t" $4 "\t" $5 "\t" $7 "\t" substr($10,2, length($10)-3)}' >> /tmp/$2

##remove alternate chromosomes if needed
  awk </tmp/$2 '!/_/ {print}' >$2
