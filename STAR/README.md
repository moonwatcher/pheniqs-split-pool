
First run with barcodes anchored to the read coordinate system

```
STAR \
--readFilesCommand bzcat \
--genomeDir /media/terminus/home/lg/split-seq-data/index/mm10_hg38 \
--soloFeatures Gene \
--readFilesPrefix /home/lg/split-seq-data/raw_fastq/ \
--readFilesIn SRR6750041_1.fastq.bz2 SRR6750041_2.fastq.bz2 \
--soloType CB_UMI_Complex \
--soloCBwhitelist /home/lg/code/moonwatcher/pheniqs-split-pool/raw/cb_whitelist /home/lg/code/moonwatcher/pheniqs-split-pool/raw/cb_whitelist /home/lg/code/moonwatcher/pheniqs-split-pool/raw/cb_whitelist \
--soloCBposition 0_10_0_17 0_48_0_55 0_86_0_93 \
--soloUMIposition 0_0_0_9 \
--soloCBmatchWLtype 1MM \
--outSAMtype BAM SortedByCoordinate \
--readFilesSAMattrKeep RX QX CB CR CY XC \
--outSAMattributes CR CY UR UY GX GN CB UB sM sS sQ \
```

SPLiTSeq read segment 2 has the following layout:

1. ```[0:10]``` is the UMI
2. ```[10:18]``` is BC3
3. ```[18:48]``` is ```GTGGCCGATGTTTCGCATCGGCGTACGACT```. Referred to in the paper as *Round 3 blocking strand* or *Oligonucleotie BC_0066*.
4. ```[48:56]``` is BC2
5. ```[56:86]``` is ```ATCCACGTGCTTGAGAGGCCAGAGCATTCG```. Referred to in the paper as *Round 2 blocking strand* or *Oligonucleotie BC_0216*.
6. ```[86:94]``` is BC1

```
UUUUUUUUUU33333333GTGGCCGATGTTTCGCATCGGCGTACGACT22222222ATCCACGTGCTTGAGAGGCCAGAGCATTCG11111111
```

Now try to anchor against the first adapter. UMI is at position 0 so anchor to the adaptor start.

```
STAR \
--readFilesCommand bzcat \
--genomeDir /media/terminus/home/lg/split-seq-data/index/mm10_hg38 \
--soloFeatures Gene \
--readFilesPrefix /home/lg/split-seq-data/raw_fastq/ \
--readFilesIn SRR6750041_1.fastq.bz2 SRR6750041_2.fastq.bz2 \
--soloType CB_UMI_Complex \
--soloCBwhitelist /home/lg/code/moonwatcher/pheniqs-split-pool/raw/cb_whitelist /home/lg/code/moonwatcher/pheniqs-split-pool/raw/cb_whitelist /home/lg/code/moonwatcher/pheniqs-split-pool/raw/cb_whitelist \
--soloAdapterSequence GTGGCCGATGTTTCGCATCGGCGTACGACT \
--soloCBposition 2_-8_2_-1 3_1_3_8 3_39_3_46 \
--soloUMIposition 2_-18_2_-9 \
--soloCBmatchWLtype 1MM \
--outSAMtype BAM SortedByCoordinate \
--readFilesSAMattrKeep RX QX CB CR CY XC \
--outSAMattributes CR CY UR UY GX GN CB UB sM sS sQ \
```
