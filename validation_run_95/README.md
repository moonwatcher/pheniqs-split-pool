# Read layout

Forward read segment has 66 biological nucleotides

Reverse read segment is 95 nucleotides long with the following layout:
1. ```[0:10]``` is the UMI
2. ```[10:18]``` is BC3
3. ```[18:48]``` is ```GTGGCCGATGTTTCGCATCGGCGTACGACT```. Referred to in the paper as *Round 3 blocking strand* or *Oligonucleotie BC_0066*.
4. ```[48:56]``` is BC2
5. ```[56:86]``` is ```ATCCACGTGCTTGAGAGGCCAGAGCATTCG```. Referred to in the paper as *Round 2 blocking strand* or *Oligonucleotie BC_0216*.
6. ```[86:94]``` is BC3


| Data       | Experiment | Accession  | Alt ID     |Read count | Pheniqs 95%     | Original*        | Description                           |
| :--------- | :--------- | :--------- | :--------- |:--------  | :-------------  | :--------------- | :------------------------------------ |
| SRR6750041 | SRX3722697 | GSM3017260 |SAMN08567263| 77621181  | 48974827(63.09) | 51706161(66.61)  | MM 100 CNS nuclei                     |
| SRR6750056 | SRX3722699 | GSM3017262 |SAMN08567261| 218683580 |137683698(62.96) | 145809694(66.68) | HS/MM same day cells nuclei 3000 UBCs |
| SRR6750057 | SRX3722700 | GSM3017263 |SAMN08567260| 215597675 |136178474(63.16) | 82387120(38.21%) | HS/MM same day cells nuclei 300 UBCs  |
| SRR6750058 | SRX3722701 | GSM3017264 |SAMN08567259| 221577898 |125779278(56.76) | 131707053(59.44) | HS/MM frozen preserved cells nuclei 1000 UBCs |
| SRR6750059 | SRX3722702 | GSM3017265 |SAMN08567264| 241868411 |135120338(55.86) | 75844129(31.36)  | HS/MM frozen preserved cells nuclei 200 UBCs |

Experiment SRX3722697
Data: SRR6750041
Description: NextSeq 550 paired end sequencing; GSM3017260: 100_CNS_nuclei; Mus musculus; RNA-Seq

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


## Handling indels

Exploring the options for handling the indels requires understanding what actually matters.
We don't explicitly care about how the read as a whole was phased just the following questions:

1. The UMI is on the first 10 nucleotides of the reverse read segment. Has the molecular barcode been hurt in anyway? that requires to know if indeed BC3 starts on offset 10, or even better if *Oligonucleotie BC_0066* starts any earlier than position 18. If the UMI is truncated the read is potentially no longer interesting.

2. Is BC3 starting on position 10. for that we need to establish where *Oligonucleotie BC_0066* starts. If it is any earlier than 18, the UMI is damaged. if it is upstream of 18 we need to adjust the location of BC3 start position.

3. Is BC2 starting on position 48? that can be established by determining the alignment of *Oligonucleotie BC_0066* and *Oligonucleotie BC_0216*.

4. Is BC3 at position 86? That depends on the alignment of *Oligonucleotie BC_0216*.

% bzcat SRR6750041_2.fastq.bz2|grep 'GTGGCCGATGTTTCGCATCGGCGTACGACT'|wc -l
56835315
