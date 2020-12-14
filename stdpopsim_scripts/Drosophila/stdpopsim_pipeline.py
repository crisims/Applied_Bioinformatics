def format_vcf(file_dir, outfile_name):
    with open(file_dir + outfile_name + ".vcf", 'w') as outfile:
        files = [file_dir + "DroMCC2L.vcf",
            #file_dir + "DroMCC2L.vcf",
                 file_dir + "DroMCC2R.vcf",
                 file_dir + "DroMCC3L.vcf",
                 file_dir + "DroMCC3R.vcf",
                 file_dir + "DroMCCX.vcf"]
        for file in files:
            status = ( "2L" in file)
            print("Files read: " + file + "            \t  removing header: " + str(status) )
            with open(file) as infile:
                for line in infile:
                    if line[0] == "1":
                        if "2L" in file:
                            outfile.write("2L" + line[1:])
                        elif "2R" in file:
                            outfile.write("2R" + line[1:])
                        elif "3L" in file:
                            outfile.write("3L" + line[1:])
                        elif "3R" in file:
                            outfile.write("3R" + line[1:])
                        elif "X" in file:
                            outfile.write("X" + line[1:])
                    elif "2L" not in file:
                        pass
                    else:
                        outfile.write(line)


if __name__ == "__main__":
    vcf_directory = "/proj/snic2019-8-323/private/stdpopsim/3_output_20/"
    outfile_name = "DroMCC_all"
    format_vcf(vcf_directory, outfile_name)
