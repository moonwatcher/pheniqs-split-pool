#!/bin/bash
#SBATCH --job-name=SRR6750058
#SBATCH --nodes=1
#SBATCH --cpus-per-task=24
#SBATCH --mem=2GB
#SBATCH --time=01:00:00

module purge

time /home/lg1883/bin/pheniqs mux \
--config /scratch/lg1883/split_seq/config/decode_cell.json \
--base-output /scratch/lg1883/split_seq/full_run_99 \
--base-input /scratch/lg1883/split_seq/raw \
--input SRR6750058.cram \
--input SRR6750058.cram \
--report SRR6750058_first_report.json \
--prior SRR6750058_first_adjusted.json \
--output /dev/null

time /home/lg1883/bin/pheniqs mux \
--config /scratch/lg1883/split_seq/full_run_99/SRR6750058_first_adjusted.json \
--report SRR6750058_second_report.json \
--prior SRR6750058_second_adjusted.json
