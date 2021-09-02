## Original Split-Seq protocol

1. remove any dephased reads: last 6 bases of read did not match the expected sequence.
The 96 barcodes used by SPLiT-Seq have unique 6bp suffixes. The `filter_by_last_6.json` configuration will check (using MDD with 0 tolerance) for an exact match to one of the 96 barcode suffixes on the last 6 bases of the second read segment. Undetermined is redirected to /dev/null and the output is sent to a CRAM file. We can ignore the classifications downstream but that fulfills this requirement. For SRR6750041, for instance, that resulted in 67.30% of the reads surviving.

2. Filter based on quality score in the UMI region: Discard any read with >1 low-quality base phred <=10.

3. Filter cellular barcodes: Discard reads with more than one mismatch in any of the three 8 nt cell barcodes.

4. Align cDNA read segment (Forward) to either a combined mm10_hg19 genome or the mm10 genome using STAR.

5. Map aligned reads in the resulting bam file to exons and genes using TagReadWithGeneExon from the [drop-seq tools](https://github.com/broadinstitute/Drop-seq/releases). Only consider the primary alignments. Reads that mapped to a gene, but no exon, are considered intronic. Reads mapping to no gene were considered intergenic. TagReadWithGeneExon requires a refFlat file, which requires a .dict file to make.


The [manual for the Drop-seq tools](https://github.com/broadinstitute/Drop-seq/blob/master/doc/Drop-seq_Alignment_Cookbook.pdf) describes *TagReadWithGeneExon*:

**TagReadWithGeneExon**
This is a Drop-seq program that adds a BAM tag “GE” onto reads when the read overlaps the exon of a gene. This tag contains the name of the gene, as reported in the annotations file. You can use either a GTF or a RefFlat annotation file with this program, depending on what annotation data source you find most useful. This is used later when we extract digital gene expression (DGE) from the BAM.

Example:
```
TagReadWithGeneExon
I=merged.bam
O=star_gene_exon_tagged.bam
ANNOTATIONS_FILE=${refFlat}
TAG=GE
```
**Updates to TagReadWithGeneExon (V2)**
We have updated and re-written how reads are tagged with functional annotations in V 2.0 of the dropseq toolkit. In V1, reads received two BAM tags when a read overlapped the exon of a gene. The GE tag specified the gene that overlapped the read, while GS specified which strand the gene was on. This information allows DigitalExpression and other programs to decide if they want to consider reads that are on the same strand as the gene, or run without regard to strand.
A typical read on that overlaps a gene might have the following tags, indicating the read overlapped an exon of GENE_A, and was on the positive strand:

```
H53FWBGXX150403:1:11307:13550:9549 0 1 29658 1 60M * 0
0 CTGCCTTCCCCTCAAGCTCAGGGCCAAGCTGTCCGCCAACCTCGGCTCCTCCGGGCAGCC 7FFFFFFFFFFFFFFFFFFFF.FFFFFFFFFFFAFFFFFFFFFFA.FFFF<FFFFAAAAA XC:Z:TTGTCATGTCAC GE:Z:GENE_A XF:Z:CODING PG:Z:STAR.1 RG:Z:H53FW.1 H:i:4 NM:i:0 XM:Z:GCAAACCT UQ:i:0 AS:i:59​ GS:Z:+
```

This functionality has been retained exactly as it was implemented in a newly distributed program TagReadWithGeneExonFunction. We’ve done this in case other users need to retain backwards compatibility with any analysis they may have implemented.


6. Collapse UMIs of aligned reads that are within 1 nt mismatch of another UMI and belong to the same UBC with Starcode. a single UMI-UBC combination can have several distinct cDNA reads corresponding to different parts of the transcript. Occasionally STAR will map these different reads to different genes. choose the most frequently assigned gene as the mapping for the given UMI-UBC combination.

7. Generate a matrix of gene counts for each cell (N x K matrix, with N cells and K genes). For each gene, both intronic and exonic UMI counts were used.

## STAR source code
https://github.com/alexdobin/STAR/archive/refs/tags/2.7.9a.tar.gz

## Mouse Human merged index

The Drop-Seq tools manual offers a package with a filtered [mouse](ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE63nnn/GSE63472/suppl/GSE63472_mm10_reference_metadata.tar.gz), [human](http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM1629193) and [mixed](ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE63nnn/GSE63269/suppl/GSE63269_hg19_mm10_transgenes_reference_metadata.tar.gz) reference. It contains a .dict and .refFlat file but mostly a much smaller Fasta file probably with only transgenes. It is possible this was used with TagReadWithGeneExon.


```
STAR \
--runThreadN 12 \
--runMode genomeGenerate \
--genomeDir /media/terminus/home/lg/split-seq-data/index/GSE63269_hg19_mm10 \
--genomeFastaFiles /media/terminus/home/lg/split-seq-data/reference/GSE63269_hg19_mm10/hg19_mm10_transgenes.fasta \
--sjdbGTFfile /media/terminus/home/lg/split-seq-data/reference/GSE63269_hg19_mm10/hg19_mm10_transgenes.gtf \
--sjdbOverhang 65
```

## human reference and annotation
https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz
https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/genes/hg38.ncbiRefSeq.gtf.gz

## mouse reference and annotation
https://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/genes/mm10.ncbiRefSeq.gtf.gz
https://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/mm10.fa.gz

generate the mm10 index

```
STAR \
--runThreadN 12 \
--runMode genomeGenerate \
--genomeDir /media/terminus/home/lg/split-seq-data/index/mm10 \
--genomeFastaFiles /media/terminus/home/lg/split-seq-data/reference/mm10.fa \
--sjdbGTFfile /media/terminus/home/lg/split-seq-data/reference/mm10.ncbiRefSeq.gtf \
--sjdbOverhang 65
```

generate the hg38 index

```
STAR \
--runThreadN 12 \
--runMode genomeGenerate \
--genomeDir /media/terminus/home/lg/split-seq-data/index/hg38 \
--genomeFastaFiles /media/terminus/home/lg/split-seq-data/reference/hg38.fa \
--sjdbGTFfile /media/terminus/home/lg/split-seq-data/reference/hg38.ncbiRefSeq.gtf \
--sjdbOverhang 65
```

generate the mm10/hg38 combined index

```
STAR \
--runThreadN 12 \
--runMode genomeGenerate \
--genomeDir /media/terminus/home/lg/split-seq-data/index/mm10_hg38 \
--genomeFastaFiles /media/terminus/home/lg/split-seq-data/reference/hg38.fa \
/media/terminus/home/lg/split-seq-data/reference/mm10.fa \
--sjdbGTFfile /media/terminus/home/lg/split-seq-data/reference/hg38.ncbiRefSeq.gtf \
/media/terminus/home/lg/split-seq-data/reference/mm10.ncbiRefSeq.gtf \
--sjdbOverhang 65
```

align the output to the mouse genome with STAR

```
STAR \
--runMode alignReads \
--genomeDir /media/terminus/home/lg/split-seq-data/index/mm10 \
--outFileNamePrefix SRR6750041_ \
--readFilesType SAM SE \
--readFilesCommand samtools view \
--readFilesIn SRR6750041_decoded.cram
```

Seems like STAR will take SAM input and keep existing attributes:

```
pyxis:validation_95 lg% cat Aligned.out.sam                                                                                                                               ~/split-seq-data/validation_95
@HD	VN:1.4
@SQ	SN:chr1	LN:195471971
@SQ	SN:chr10	LN:130694993
@SQ	SN:chr11	LN:122082543
@SQ	SN:chr12	LN:120129022
@SQ	SN:chr13	LN:120421639
@SQ	SN:chr14	LN:124902244
@SQ	SN:chr15	LN:104043685
@SQ	SN:chr16	LN:98207768
@SQ	SN:chr17	LN:94987271
@SQ	SN:chr18	LN:90702639
@SQ	SN:chr19	LN:61431566
@SQ	SN:chr1_GL456210_random	LN:169725
@SQ	SN:chr1_GL456211_random	LN:241735
@SQ	SN:chr1_GL456212_random	LN:153618
@SQ	SN:chr1_GL456213_random	LN:39340
@SQ	SN:chr1_GL456221_random	LN:206961
@SQ	SN:chr2	LN:182113224
@SQ	SN:chr3	LN:160039680
@SQ	SN:chr4	LN:156508116
@SQ	SN:chr4_GL456216_random	LN:66673
@SQ	SN:chr4_JH584292_random	LN:14945
@SQ	SN:chr4_GL456350_random	LN:227966
@SQ	SN:chr4_JH584293_random	LN:207968
@SQ	SN:chr4_JH584294_random	LN:191905
@SQ	SN:chr4_JH584295_random	LN:1976
@SQ	SN:chr5	LN:151834684
@SQ	SN:chr5_JH584296_random	LN:199368
@SQ	SN:chr5_JH584297_random	LN:205776
@SQ	SN:chr5_JH584298_random	LN:184189
@SQ	SN:chr5_GL456354_random	LN:195993
@SQ	SN:chr5_JH584299_random	LN:953012
@SQ	SN:chr6	LN:149736546
@SQ	SN:chr7	LN:145441459
@SQ	SN:chr7_GL456219_random	LN:175968
@SQ	SN:chr8	LN:129401213
@SQ	SN:chr9	LN:124595110
@SQ	SN:chrM	LN:16299
@SQ	SN:chrX	LN:171031299
@SQ	SN:chrX_GL456233_random	LN:336933
@SQ	SN:chrY	LN:91744698
@SQ	SN:chrY_JH584300_random	LN:182347
@SQ	SN:chrY_JH584301_random	LN:259875
@SQ	SN:chrY_JH584302_random	LN:155838
@SQ	SN:chrY_JH584303_random	LN:158099
@SQ	SN:chrUn_GL456239	LN:40056
@SQ	SN:chrUn_GL456367	LN:42057
@SQ	SN:chrUn_GL456378	LN:31602
@SQ	SN:chrUn_GL456381	LN:25871
@SQ	SN:chrUn_GL456382	LN:23158
@SQ	SN:chrUn_GL456383	LN:38659
@SQ	SN:chrUn_GL456385	LN:35240
@SQ	SN:chrUn_GL456390	LN:24668
@SQ	SN:chrUn_GL456392	LN:23629
@SQ	SN:chrUn_GL456393	LN:55711
@SQ	SN:chrUn_GL456394	LN:24323
@SQ	SN:chrUn_GL456359	LN:22974
@SQ	SN:chrUn_GL456360	LN:31704
@SQ	SN:chrUn_GL456396	LN:21240
@SQ	SN:chrUn_GL456372	LN:28664
@SQ	SN:chrUn_GL456387	LN:24685
@SQ	SN:chrUn_GL456389	LN:28772
@SQ	SN:chrUn_GL456370	LN:26764
@SQ	SN:chrUn_GL456379	LN:72385
@SQ	SN:chrUn_GL456366	LN:47073
@SQ	SN:chrUn_GL456368	LN:20208
@SQ	SN:chrUn_JH584304	LN:114452
@PG	ID:STAR	PN:STAR	VN:2.7.9a	CL:STAR   --runMode alignReads      --genomeDir /media/terminus/home/lg/split-seq-data/index/mm10   --readFilesType SAM   SE      --readFilesIn SRR6750041_decoded.cram      --readFilesCommand samtools   view   
@CO	user command line: STAR --runMode alignReads --genomeDir /media/terminus/home/lg/split-seq-data/index/mm10 --readFilesType SAM SE --readFilesCommand samtools view --readFilesIn SRR6750041_decoded.cram
SRR6750041.46	272	chr5	69915046	0	66M	*	0	0	CCTCTTGGGTGAATTTGCTTCATTTTTCTCTAGAGCTTTTAGATGTGTTGTCAAGCTGCTAGTATG	EEEEEEE<EEEEEEEEEEEAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEAAAAA	NH:i:7	HI:i:3	AS:i:62	nM:i:1	RX:Z:NCAACGTGGG	QX:Z:#AAAAEEEEE	CB:Z:ACAGCAGA-GTACGCAA-CATCAAGT	CR:Z:ACAGCAGA-GTACGCAA-CATCAAGT	CY:Z:EEEEEEEA AEEEEEEE EEEEEEEE	XC:f:0.00134162
SRR6750041.46	272	chr16	74360898	0	66M	*	0	0	CCTCTTGGGTGAATTTGCTTCATTTTTCTCTAGAGCTTTTAGATGTGTTGTCAAGCTGCTAGTATG	EEEEEEE<EEEEEEEEEEEAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEAAAAA	NH:i:7	HI:i:4	AS:i:62	nM:i:1	RX:Z:NCAACGTGGG	QX:Z:#AAAAEEEEE	CB:Z:ACAGCAGA-GTACGCAA-CATCAAGT	CR:Z:ACAGCAGA-GTACGCAA-CATCAAGT	CY:Z:EEEEEEEA AEEEEEEE EEEEEEEE	XC:f:0.00134162
SRR6750041.46	272	chr13	87937259	0	66M	*	0	0	CCTCTTGGGTGAATTTGCTTCATTTTTCTCTAGAGCTTTTAGATGTGTTGTCAAGCTGCTAGTATG	EEEEEEE<EEEEEEEEEEEAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEAAAAA	NH:i:7	HI:i:5	AS:i:62	nM:i:1	RX:Z:NCAACGTGGG	QX:Z:#AAAAEEEEE	CB:Z:ACAGCAGA-GTACGCAA-CATCAAGT	CR:Z:ACAGCAGA-GTACGCAA-CATCAAGT	CY:Z:EEEEEEEA AEEEEEEE EEEEEEEE	XC:f:0.00134162
SRR6750041.46	256	chr8	52840320	0	66M	*	0	0	CATACTAGCAGCTTGACAACACATCTAAAAGCTCTAGAGAAAAATGAAGCAAATTCACCCAAGAGG	AAAAAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEAEEEEEEEEEEE<EEEEEEE	NH:i:7	HI:i:6	AS:i:62	nM:i:1	RX:Z:NCAACGTGGG	QX:Z:#AAAAEEEEE	CB:Z:ACAGCAGA-GTACGCAA-CATCAAGT	CR:Z:ACAGCAGA-GTACGCAA-CATCAAGT	CY:Z:EEEEEEEA AEEEEEEE EEEEEEEE	XC:f:0.00134162
SRR6750041.46	256	chr10	46383112	0	66M	*	0	0	CATACTAGCAGCTTGACAACACATCTAAAAGCTCTAGAGAAAAATGAAGCAAATTCACCCAAGAGG	AAAAAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEAEEEEEEEEEEE<EEEEEEE	NH:i:7	HI:i:7	AS:i:62	nM:i:1	RX:Z:NCAACGTGGG	QX:Z:#AAAAEEEEE	CB:Z:ACAGCAGA-GTACGCAA-CATCAAGT	CR:Z:ACAGCAGA-GTACGCAA-CATCAAGT	CY:Z:EEEEEEEA AEEEEEEE EEEEEEEE	XC:f:0.00134162
SRR6750041.50	16	chr9	62066600	255	66M	*	0	0	TCCCTGGTGCCCCAGAGCTTTAGCTTGCTTACACCTATGCTTTTAAGACAAGTCTCACCTTATCAC	EEEEEEEEEEEEEAAEEEEEAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEAAAA/A	NH:i:1	HI:i:1	AS:i:62	nM:i:1	RX:Z:NTTGTAGTAT	QX:Z:#AAAAEEEEE	CB:Z:ATTGGCTC-TGGCTTCA-TGGTGGTA	CR:Z:ATTGGCTC-TGGCTTCA-TGGTGGTA	CY:Z:EAEA/EEA AEEEA<A< EAEEEEEE	XC:f:0.000544416
SRR6750041.54	0	chr10	106651728	255	66M	*	0	0	GCATAAGAGCATGTGACAGCTAGCAGGCTTGACAACTGCCAGAGCAGTTGACATACCATACGATCA	AAAAAEEEEEEEEEEEEEEEEEEEEEEEEEEAEEEEEEEEEE6EEEEEEEEEAEEEEEEEEEAEEE	NH:i:1	HI:i:1	AS:i:62	nM:i:1	RX:Z:NAGTGCTTCC	QX:Z:#AAAAEEEEE	CB:Z:AAGGACAC-CTCAATGA-CGAACTTA	CR:Z:AAGGACAC-CTCAATGA-CGAACTTA	CY:Z:EEEAEEEE A/EEEEE/ EEEAEEEE	XC:f:0.00373491
SRR6750041.55	0	chr8	32173464	255	66M	*	0	0	AAATAAGTGCTATTGCACAACTTATCTTAATAATTTCTTGTAGATAGCCACATGTTGATCAAATTT	AAAAAEEEEEEEEEEE/EEEEEEEEEEEEEEAEEEEEEEEEEEEEEEAEE<EEAEEE/EEEEE<E<	NH:i:1	HI:i:1	AS:i:64	nM:i:0	RX:Z:NGGGAAATGG	QX:Z:#AAAAEAEEE	CB:Z:CTGAGCCA-AGTGGTCA-CTCAATGA	CR:Z:CTGAGCCA-AGTGGTCA-CTCAATGA	CY:Z:EEEEEE/E <A/A<EEE EEEEEEEE	XC:f:0.000532691
SRR6750041.58	16	chr7	59947206	255	66M	*	0	0	TACACATATCACTACATATATCTAAAAGTTTTGAATTTGAACACCAGGTTGTTTGCTCATCTAAAG	EEEEEEEEAEEE/EEAAEEEEEEEEEEE//EEEEEEEEEEEEEEEEEEE/EEEEEEEEEEEAAAAA	NH:i:1	HI:i:1	AS:i:62	nM:i:1	RX:Z:NGATGTAAAC	QX:Z:#A/A6EEEEE	CB:Z:TGGTGGTA-GTACGCAA-CATCAAGT	CR:Z:TGGTGGTA-GTACGCAA-CATCAAGT	CY:Z:EAE<EEE< EEEEEE// EEEEEEEE	XC:f:0.0011708
SRR6750041.59	16	chr17	46828218	255	66M	*	0	0	GACTCTGTCTGACTTCTGAGAGCCAGGGCCTCTCACCGAAGCTGAGCTGGGCGGGCTGTGGAGAAG	EEEEEEEAEEEEEEEEEE/EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEAAAAA	NH:i:1	HI:i:1	AS:i:64	nM:i:0	RX:Z:NTTTATATGG	QX:Z:#AAAAEEEEE	CB:Z:GGAGAACA-AAGAGATC-GGAGAACA	CR:Z:GGAGAACA-AAGAGATC-GGAGAACA	CY:Z:/EEEAEE/ AEEEE/EE EEEEEEEE	XC:f:0.00401458
SRR6750041.60	16	chr2	36128483	255	66M	*	0	0	CATAACTAATCAGGTGTCTGATATCACTCTAGAAAGATACAATACAGGTCTAGTACTGGGATAGGA	EEEEEEAEAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEAAAAA	NH:i:1	HI:i:1	AS:i:64	nM:i:0	RX:Z:NCACGGCGTT	QX:Z:#AAAAEEEEE	CB:Z:AGCCATGC-ACACAGAA-TGGAACAA	CR:Z:AGCCATGC-ACACAGAA-TGGAACAA	CY:Z:AEEEEEEE EEEEEEEE EEEEEEEE	XC:f:0.000262723
SRR6750041.61	16	chr1	124623154	255	66M	*	0	0	AGTACCCAAGGGGCTAAAGGGATCTGCAACCCTAAAGGTGTAACAACAATATGAACTAACCAGTAC	EEEEEAEEEEAAEEAEEA/EEE/EEEEEEEEEEEA/EE/6EEEEEEEEEEEEE6EE6EAAEAAAAA	NH:i:1	HI:i:1	AS:i:64	nM:i:0	RX:Z:NTATTTGGCC	QX:Z:#AAAAEEEEE	CB:Z:ATTGGCTC-CTGAGCCA-AAACATCG	CR:Z:ATTGGCTC-CTGAGCCA-AAACATCG	CY:Z:<<AE/EEE EEE/EE<E EEEEEEEE	XC:f:0.000759425
SRR6750041.62	16	chr6	77557724	255	66M	*	0	0	TCACATGTATCCCAAGAGGATTCCTCCTCTTTTGAGCTACTCTCTGTAGTTCCTACACATCTTGTG	/EEEAAE/EEEEEEEAEAE6EE/EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEAAAAA	NH:i:1	HI:i:1	AS:i:64	nM:i:0	RX:Z:NAGTTGCTTT	QX:Z:#AAAAEEEEE	CB:Z:GTGTTCTA-AGAGTCAA-ACCACTGT	CR:Z:GTGTTCTA-AGAGTCAA-ACCACTGT	CY:Z:<EEE<EEE <<EEEEAE /6EEAE/E	XC:f:0.00243744
SRR6750041.65	16	chr11	102888169	255	66M	*	0	0	GCTGCTCAGTGGGGCTGACACACTGGAGTCATCACCATGGAGGGCCCTTCAGGACTGCCTTAGTGG	AEEEEEEEE/EEEEE<EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEAAAAA	NH:i:1	HI:i:1	AS:i:62	nM:i:1	RX:Z:NCGGACCTGT	QX:Z:#AAAAEEEEE	CB:Z:ACACGACC-CGACTGGA-AGCACCTC	CR:Z:ACACGACC-CGACTGGA-AGCACCTC	CY:Z:E<EEE/EE AEEAEEEE EEEEEEEE	XC:f:0.00508981
SRR6750041.66	0	chr9	68688406	255	66M	*	0	0	CCCAGTAACCTGCTTCCTTCAGAAAGACTCTACCTTCTAAAGTTTCCACAACTTTCTCAAATGGGC	AAAAA6EEEEEEEAEEEEAA/EAEEEE6EEEE/EEAAEEE/EEEEEEEA/EAEAEEEAAE/EE/EA	NH:i:1	HI:i:1	AS:i:64	nM:i:0	RX:Z:NTAGTTGTTT	QX:Z:#AAAA/EEEE	CB:Z:GTCTGTCA-CCTCTATC-ACAGCAGA	CR:Z:GTCTGTCA-CCTCTATC-ACAGCAGA	CY:Z:EEEEE<A/ 6//6</<E EEEEEE6/	XC:f:0.00096609
SRR6750041.67	0	chr15	101029213	255	53M13S	*	0	0	GCTCTCTGAACGGAGCATATTTTGTGAGTTGGGAAAAATAAAAAAAAAAAAAAAGCCAATGTCGAA	AAAAAEEEEAEEEEEEEEEEEEEEEEEEEEEEEEEEEEE6EEEEEEEEEEEEEE/A6EEE/EA/EE	NH:i:1	HI:i:1	AS:i:52	nM:i:0	RX:Z:NGGGCATTGG	QX:Z:#AAAAEEEEE	CB:Z:ACATTGGC-AAGAGATC-GGAGAACA	CR:Z:ACATTGGC-AAGAGATC-GGAGAACA	CY:Z:EE/EEEEE EEEEEEEE EEEEEEEE	XC:f:0.00384626
```
