#!/bin/bash
#SBATCH --job-name=SRR6750046
#SBATCH --nodes=1
#SBATCH --cpus-per-task=24
#SBATCH --mem=2GB
#SBATCH --time=01:00:00

module purge

time /home/lg1883/bin/pheniqs mux \
--config /scratch/lg1883/split_seq/config/decode_cell_999.json \
--base-output /scratch/lg1883/split_seq/full_run_999 \
--base-input /scratch/lg1883/split_seq/raw \
--input SRR6750046.cram \
--input SRR6750046.cram \
--report SRR6750046_first_report.json \
--prior SRR6750046_first_adjusted.json \
--output /dev/null

time /home/lg1883/bin/pheniqs mux \
--config /scratch/lg1883/split_seq/full_run_999/SRR6750046_first_adjusted.json \
--report SRR6750046_second_report.json \
--prior SRR6750046_second_adjusted.json
