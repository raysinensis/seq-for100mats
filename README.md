# seq-for100mats
command lines and scripts for converting between formats required by various RNA-seq software packages

Unfortuantely different RNA-seq software, from QC to steps in the analysis pipeline, often require different reference formats. The problem is further exacerbated by how different reference assemblies can differ in their column arrangements.

Collected here are simple command lines and scripts related to my own work for converting between the (way too many!) different formats. Reinventing the wheels a bit, perhaps.

# GTF_filter
For editing GTF files, used for RNAseq alignment. Gencode GTF files are recommended over UCSC ones for noncoding RNA annotations. Depending on specific needs, customized GTF may be required, hence this utility to select or filter out entries.

# GTF_info
Further separation of subgroups, such as UTRs, or first/final exons. Currently required for the UTR python scripts.

# UTR.py
Generating two GTF files, with either 5'UTR or 3'UTR annotations.

# UTRexon.py
Similar to the previous, but exons (including those that span the start or stop codons).

# mk_rRNA_interval
RNA-SeQC requires rRNA interval file for quality control analysis. The file, not readily available from iGenome download packages, can be generated directly from GTF annotations. The interval file from human GRch38 is also uploaded.

# csv2rnk
GSEA from the Broad Institute is widely used for enrichment analysis. An RNK file containing significant target genes is required, which can be generated from the CSV output file of differential analysis packages such as DEseq2 (also added default settings for edgeR and sleuth). Classic mode (unweighted) in GSEA is recommended with this pipeline.

# other notes
containing other simple lines, and details to know about compatibility issues regarding various formats in RNA seq analysis

examples (csv starting file, and generated rnk for csv2rnk) and gene files from GRCh38 (gencode) are supplied for those interested
