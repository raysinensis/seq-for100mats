##GTF to refFlat:
gtfToGenePred -genePredExt -geneNameAsName2 'file_name_here' refFlat.tmp.txt
paste <(cut -f 12 refFlat.tmp.txt) <(cut -f 1-10 refFlat.tmp.txt) > refFlat.txt
gzip refFlat.txt

##GTF to BED
gtf2bed <file_name.gtf> file_name.bed ##[requires BEDOPS, note: conversions for ENSEMBL/GENCODE GTFs are not accepted by RSeQC, must use line below instead]

time gtfToGenePred genes.gtf test.genePhred && genePredToBed test.genePhred genes.bed && rm test.genePhred ##[requires UCSC packages]
