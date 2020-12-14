#!/bin/bash
#SBATCH -A snic2019-8-323
#SBATCH -p core
#SBATCH -n 16
#SBATCH --time=48:00:00
#SBATCH -D /proj/snic2019-8-323/private/stdpopsim/3_output/
#SBATCH -M snowy
#SBATCH -J STD_2L_20rep
#SBATCH --mail-type=ALL
#SBATCH --mail-user cristinadiazubieta@gmail.com

module load python

#Commands to write

python -m stdpopsim DroMel -c chr2L -g ComeronCrossover_dm6 -o DroMCC2L.ts -d African3Epoch_1S16 20
python -m tskit vcf DroMCC2L.ts > DroMCC2L.vcf

