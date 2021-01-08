#!/bin/bash
#SBATCH -A snic2019-8-323
#SBATCH -J 250e_10rho_100r
#SBATCH --time=48:00:00
#SBATCH -p node
#SBATCH -N 1
#SBATCH -M snowy
#SBATCH --exclusive
#SBATCH --gres=gpu:1
#SBATCH --gpus-per-node=4


module load conda
source conda_init.sh

conda activate 


# Simulate data
${SIMULATE} \
    --vcf ${VCF} \
    --genome ${GENOME} \
    --mask ${MASK} \
    --projectDir ${DIR} \
    --assumedMu ${MU} \
    --upperRhoThetaRatio ${URTR} \
    --nTrain 13000 \
    --nVali 2000 \
    --nTest 100 \
    --forceWinSize 100000 \
    --seed ${SEED}

# Train network
${TRAIN} \
    --projectDir ${DIR} \
    --nEpochs 250 \
    --nValSteps 2 \
    --seed ${SEED}

# Predict
${PREDICT} \
    --vcf ${VCF} \
    --projectDir ${DIR} \
    --seed ${SEED}

# Parametric Bootstrapping
${BSCORRECT} \
    --projectDir ${DIR} \
    --nSlice 10 \
    --nReps 10\
    --seed ${SEED}