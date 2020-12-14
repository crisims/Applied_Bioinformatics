#!/bin/bash
#SBATCH -A snic2019-8-323
#SBATCH -p core
#SBATCH -n 16
#SBATCH --time=48:00:00
#SBATCH -D /proj/snic2019-8-323/private/stdpopsim/09_output_20/
#SBATCH -M snowy
#SBATCH -J STD_1_20rep
#SBATCH --mail-type=ALL
#SBATCH --mail-user cristinadiazubieta@gmail.com

module load python

#Commands to write

python -m stdpopsim AraTha -c chr1 -g SalomeAveraged_TAIR7 -o Ara1.ts -d SouthMiddleAtlas_1D17 20
python -m tskit vcf Ara1.ts > Ara1.vcf

