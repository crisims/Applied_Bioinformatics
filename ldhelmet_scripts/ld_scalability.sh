#!/bin/bash
#SBATCH -A snic2019-8-323
#SBATCH -p core
#SBATCH -n 4
#SBATCH -M snowy
#SBATCH --time=48:00:00
#SBATCH -D /proj/snic2019-8-323/private/ldhelmet/scalability_test/strong/04cores
#SBATCH -J Ldhelmet_sca4
#SBATCH --mail-type=ALL
#SBATCH --mail-user cristinadiazubieta@gmail.com

module load bioinfo-tools
module load LDhelmet

#Commands to write


#Examples on how to run ldhelmet, we have to do 5 steps
ldhelmet find_confs --num_threads 4 -w 50 -o output.conf input.fasta

#-t is the mutation rate and -r is the grid of p-values. They changed t, the default was 0.1
ldhelmet table_gen --num_threads 4 -t 0.01 -r 0.0 0.1 10.0 1.0 100.0 -c output.conf -o output.lk

#here they changed x, it was 11 by default, and added the threshold
ldhelmet pade --num_threads 4 -t 0.01 -x 12 --defect_threshold 40 -c output.conf -o output.pade

#mutMat.txt and ancPriors.txt are optional files
ldhelmet rjmcmc --num_threads 4 -l output.lk -p output.pade -s input.fasta -b 50 --burn_in 10000 -n 100000 -o output.post


ldhelmet post_to_text -m -p 0.025 -p 0.50 -p 0.975 -o output.txt output.post

ldhelmet max_lk --num_threads 4 -l output.lk -p output.pade -s input.fasta
