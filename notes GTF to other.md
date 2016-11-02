#GTF to refFlat:
$ gtfToGenePred -genePredExt -geneNameAsName2 'file_name_here' refFlat.tmp.txt

$ paste <(cut -f 12 refFlat.tmp.txt) <(cut -f 1-10 refFlat.tmp.txt) > refFlat.txt

$ gzip refFlat.txt

#GTF to BED
$ gtf2bed < 'file_name.gtf' > file_name.bed 
[requires BEDOPS, note: conversions for ENSEMBL/GENCODE GTFs are not accepted by RSeQC, must use line below instead]

$ time gtfToGenePred genes.gtf test.genePhred && genePredToBed test.genePhred genes.bed && rm test.genePhred
[requires UCSC packages]

#tophat BAM edits to work with RNA-SeQC
java -jar picard.jar AddOrReplaceReadGroups  INPUT="input_name"  RGLB=LaneX RGPU=NONE RGSM=Any RGPL=illumina

java -jar picard.jar ReorderSam  Input=input_name  OUTPUT=output_name  REFERENCE=genome.fa


java -jar RNA-SeQC_v1.1.8.jar -r 'genome.fa' -s "TestID|BAM_name|TestDesc" -t 'reference.gtf' -singleEnd -n 3000 -o output_name
