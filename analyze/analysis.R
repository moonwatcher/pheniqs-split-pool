#!/usr/bin/env Rscript

library(ggplot2)
library(grid)
library(gridExtra)

# base_folder = '/Users/lg/code/moonwatcher/pheniqs-split-pool/analyze/'
setwd(base_folder)

noise_and_confidence = read.table('noise_and_confidence.tsv', header=T, sep="\t")
noise_and_confidence$confidence = factor(noise_and_confidence$confidence)
noise_and_confidence$sample = factor(noise_and_confidence$sample)
noise_and_confidence$iteration = factor(noise_and_confidence$iteration)
noise_and_confidence$decoder = factor(noise_and_confidence$decoder)

barcode_noise_and_confidence = read.table('barcode_noise_and_confidence.tsv', header=T, sep="\t")
barcode_noise_and_confidence$confidence = factor(barcode_noise_and_confidence$confidence)
barcode_noise_and_confidence$sample = factor(barcode_noise_and_confidence$sample)
barcode_noise_and_confidence$iteration = factor(barcode_noise_and_confidence$iteration)
barcode_noise_and_confidence$decoder = factor(barcode_noise_and_confidence$decoder)

priors = read.table('priors.tsv', header=T, sep="\t")
priors$confidence = factor(priors$confidence)
priors$sample = factor(priors$sample)
priors$decoder = factor(priors$decoder)
priors$well = factor(priors$well)
priors$barcode = factor(priors$barcode)

overall = read.table('overall.tsv', header=T, sep="\t")
overall$confidence = factor(overall$confidence)
overall$sample = factor(overall$sample)
overall$iteration = factor(overall$iteration)

ggplot(noise_and_confidence) + geom_point(data=noise_and_confidence, aes(y = low_confidence, x = noise, color = iteration)) + facet_wrap(~confidence)
ggplot(overall) + geom_point(data=overall, aes(y = count, x = pf_count, color = iteration)) + facet_wrap(~decoder) + facet_wrap(~confidence)
