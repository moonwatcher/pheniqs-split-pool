# Potential Pheniqs benchmarks

To see what kind of contribution Bayesian barcode decoding can bring to RNA-Seq pipelines we want to identify a few data sets and perform an analysis with varying parameters on them for comparison.

# The basic RNA-Seq pipeline
* Barcode decoding. Filtering reads that fail decoding.
* Align reads to genes and identify the source of each transcript
* collapse reads with identical UMIs in each cell, error correct UMIs.
* Filter out reads that belong to non cell clusters.
* Produce a Digital Expression Matrix with read count for every gene in every cell.
* Perform Dimensionality reduction on the matrix
* Clusters visualization

# Interesting Parameters
Pheniqs has two parameters that effect the read yield vs confidence tradeoff. Minimum distance decoding is limited to filtering by the number of mismatches (rarely more than one and even 1 mismatch is only possible if the barcodes are far enough) or crude quality filtering (i.e. discard any barcode that has more than one base with quality lower than 10)

Pheniqs has two parameters that effect filtering: the **confidence threshold** the posterior probability of an incorrect decoding is compared to and the **noise threshold** the conditional probability is compared to.

The default 0.95 confidence threshold was shown to have far less false negatives than MDD but still less false positives. Setting it lower will probably introduce more false positives while setting it higher, for instance 0.99 or even 0.999 will reduce yield but potentially dramatically reduce false positive. It will be interesting to see the effect of more stringent confidence filtering on the final clustering.

Another important parameter is the noise threshold. The noise threshold is the probability of observing a random sequence. The default value is 1 / 4^n, with n being the length of the barcode. The default value considers every DNA sequence possible. Since sequencing noise does not actually come from a truly random distribution the number of possible combinations is **smaller** and the value should be **higher** than the default. Again, it would be interesting to explore the effect of higher values of the threshold on the final cell clustering.
