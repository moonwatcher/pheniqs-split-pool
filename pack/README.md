# Download and package

## FASTQ file from SRA

Raw FASTQ files downloaded from EBI ftp site. The Nextera barcode on the i7 index segment has already been decoded prior to the file being uploaded to SRA.

```
Project: PRJNA434658
To facilitate scalable profiling of single cells, we developed Split Pool Ligation-based Transcriptome sequencing (SPLiT-seq), a single-cell RNA-seq (scRNA-seq) method that labels the cellular origin of RNA through combinatorial barcoding. SPLiT-seq is compatible with fixed cells or nuclei, allows efficient sample multiplexing and requires no customized equipment. We used SPLiT-seq to analyze 156,049 single-nucleus transcriptomes from postnatal day 2 and 11 mouse brains and spinal cords. Over 100 cell types were identified, with gene expression patterns corresponding to cellular function, regional specificity, and stage of differentiation. Pseudotime analysis revealed transcriptional programs driving four developmental lineages, providing a snapshot of early postnatal development in the murine central nervous system. SPLiT-seq provides a path towards comprehensive single-cell transcriptomic analysis of other similarly complex multicellular systems. Overall design: Single-cell/nucleus RNA-seq was performed using SPLiT-seq This code explains how to read the data from the paper into python: https://gist.github.com/Alex-Rosenberg/5ee8b14ea580144facad9c2b87cebf10
```
[Project metadata in JSON ](https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA434658&result=read_run&fields=study_accession,secondary_study_accession,sample_accession,secondary_sample_accession,experiment_accession,run_accession,submission_accession,tax_id,scientific_name,instrument_platform,instrument_model,library_layout,library_strategy,library_source,library_selection,read_count,base_count,center_name,first_public,last_updated,experiment_title,study_title,study_alias,experiment_alias,run_alias,fastq_bytes,fastq_md5,fastq_ftp,fastq_aspera,fastq_galaxy,sra_bytes,sra_md5,sra_ftp,sra_aspera,sra_galaxy,sample_alias,sample_title,first_created&format=json&download=true)

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/001/SRR6750041/SRR6750041_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/001/SRR6750041/SRR6750041_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/002/SRR6750042/SRR6750042_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/002/SRR6750042/SRR6750042_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/003/SRR6750043/SRR6750043_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/003/SRR6750043/SRR6750043_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/004/SRR6750044/SRR6750044_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/004/SRR6750044/SRR6750044_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/005/SRR6750045/SRR6750045_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/005/SRR6750045/SRR6750045_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/006/SRR6750046/SRR6750046_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/006/SRR6750046/SRR6750046_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/007/SRR6750047/SRR6750047_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/007/SRR6750047/SRR6750047_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/008/SRR6750048/SRR6750048_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/008/SRR6750048/SRR6750048_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/009/SRR6750049/SRR6750049_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/009/SRR6750049/SRR6750049_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/000/SRR6750050/SRR6750050_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/000/SRR6750050/SRR6750050_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/001/SRR6750051/SRR6750051_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/001/SRR6750051/SRR6750051_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/002/SRR6750052/SRR6750052_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/002/SRR6750052/SRR6750052_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/003/SRR6750053/SRR6750053_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/003/SRR6750053/SRR6750053_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/004/SRR6750054/SRR6750054_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/004/SRR6750054/SRR6750054_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/005/SRR6750055/SRR6750055_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/005/SRR6750055/SRR6750055_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/006/SRR6750056/SRR6750056_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/006/SRR6750056/SRR6750056_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/007/SRR6750057/SRR6750057_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/007/SRR6750057/SRR6750057_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/008/SRR6750058/SRR6750058_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/008/SRR6750058/SRR6750058_2.fastq.gz

ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/009/SRR6750059/SRR6750059_1.fastq.gz
ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR675/009/SRR6750059/SRR6750059_2.fastq.gz

each pair of FASTQ file is packaged into an interleaved CRAM file to simplify and accelerate downstream processing.

Experiment SRX3722697
Data: SRR6750041
Description: NextSeq 550 paired end sequencing; GSM3017260: 100_CNS_nuclei; Mus musculus; RNA-Seq

Experiment SRX3722698
Data: SRR6750042, SRR6750043, SRR6750044, SRR6750045, SRR6750046, SRR6750047, SRR6750048, SRR6750049, SRR6750050, SRR6750051, SRR6750052, SRR6750053, SRR6750054, SRR6750055
Description: NextSeq 550 paired end sequencing; GSM3017261: 150000_CNS_nuclei; Mus musculus; RNA-Seq

Experiment SRX3722699
Data: SRR6750056
Description: NextSeq 550 paired end sequencing; GSM3017262: same_day_cells_nuclei_3000_UBCs; Homo sapiens; Mus musculus; RNA-Seq

Experiment SRX3722700
Data: SRR6750057
Description: NextSeq 550 paired end sequencing; GSM3017263: same_day_cells_nuclei_300_UBCs; Homo sapiens; Mus musculus; RNA-Seq

Experiment: SRX3722701
Data: SRR6750058
Description: NextSeq 550 paired end sequencing; GSM3017264: frozen_preserved_cells_nuclei_1000_UBCs; Homo sapiens; Mus musculus; RNA-Seq

Experiment SRX3722702
Data: SRR6750059
Description: NextSeq 550 paired end sequencing; GSM3017265: frozen_preserved_cells_nuclei_200_UBCs; Homo sapiens; Mus musculus; RNA-Seq
