import os

def chromosomechange(vcf, refseq, colnr, outfile):
    #VCF
    f = open(os.path.expanduser(vcf))
    vcf = f.readlines()
    f.close()
    vcf_split = vcf[5].split("\t")
    print("Number of replicates:", len(vcf_split)-9)
    text_file = open(outfile, "w")

    for cur_colnr in range(colnr,len(vcf_split)):
        print("Current replicate: " + vcf_split[cur_colnr] + "\t Current Progress: " + str((cur_colnr-9)/(len(vcf_split)-9)*100) + "%")

        #Formating vcf_file
        m_bases = []
        for line in vcf[6:]:
            line_split = line.split("\t")
            if str(line_split[cur_colnr]) != "1":
                m_bases.append(int(line_split[1]))

        #Fasta
        g = open(os.path.expanduser(refseq))
        lines = g.readlines()
        g.close()
        fasta_seq = lines[0].split(".")
        sequence = fasta_seq[-1]
        a=0
        output_bases = []*len(sequence)
        for base in range(len(sequence)):
            if base != m_bases[a]:
                output_bases.append(sequence[base])
            else:
                a=a+1
                if sequence[int(base)] == 'A':
                    output_bases.append('T')
                elif sequence[int(base)] == 'T':
                    output_bases.append('A')
                elif sequence[int(base)] == 'C':
                    output_bases.append('G')
                elif sequence[int(base)] == 'G':
                    output_bases.append('C')
                elif sequence[int(base)] == 'N':
                    output_bases.append('A')
                else:
                    raise Exception("No base valid. Expected A,T,C or G. Got: ", sequence[int(base)])
        output_seq = "".join(output_bases)
        header = fasta_seq[0] + fasta_seq[1] + "."

        #Writing to output file
        text_file = open(outfile, "a")
        text_file.write(header)
        text_file.write("\n")
        text_file.write(output_seq)
        text_file.write("\n")
        text_file.close()
    print("Current Progress: 100%")
    return((header +  str(output_seq)))

# fasta files contain 62 letters per line
if (__name__ == "__main__"):
    chromosomes = ["1", "2", "3", "4", "5"]
    sequences = ["1","2","3","4","5"]
    foldernam = "16_output_100"
    outputfolder = "LDhelmetAra_100Rep_16"
    reps = "4"

    ## only change the parameters below
    colnr= 9
    for i in range(len(chromosomes)):
        vcf = "/home/jonas/AppliedBioinf/LDHelmet/" + foldernam + "/Ara" + chromosomes[i] + ".vcf"
        refseq = "/home/jonas/AppliedBioinf/raw_fasta/Arabidopsis_thaliana/seq_oneline_chr_" + sequences[i] + ".fasta"
        outfile = "/home/jonas/AppliedBioinf/LDHelmet/" + outputfolder + "/" + chromosomes[i] + "_" + foldernam + ".fasta"
        print("###### Chromosome " + chromosomes[i] + "\t , " + str(i+1) + " out of " + str(len(chromosomes)) + " chromosomes ###### " +  outputfolder + " ######")
        chromosomechange(vcf, refseq, colnr, outfile)



