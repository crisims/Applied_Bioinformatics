import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
import numpy as np
from matplotlib import colors as mcolors

def genmap2array(txt, colnr):
    # Loads old refernce genome files. These contain the location of the recombinatino region in colnr=1
    # colnr=2 is the recomb rate in cM/mb
    f = open(os.path.expanduser(txt))
    linestxt = f.readlines()[1:]
    f.close()
    a = []
    chromo_len = int(linestxt[-1].split()[1])
    for line in linestxt:
        if colnr == 2:
            a.append(float(line.split()[colnr]) / chromo_len * 0.5)
        else:
            a.append(float(line.split()[colnr]))
    return a

def genmap2arrayformatted(txt):
    # The recombination rates in correct format for the newer reference files
    f = open(os.path.expanduser(txt))
    linestxt = f.readlines()
    f.close()
    a = []
    for line in linestxt:
        line = line.split()
        a.append(float(line[0][1:-1]))
        for rate in line[1:-1]:
            a.append(float(rate[:-1]))
        # print(a) #a[-1] = a[-1][:-1]
    return a

def elinChromoPlot(path_output_file, path_ref_map, numb, fig, ax1):
    # This function loads and plots the ref data against ReLERNN data
    g = open(os.path.expanduser(path_output_file))
    linesour = g.readlines()[1:]
    g.close()

    # Extracting site and recombination data from ReLERNN
    site_2_l, site_2_r, site_3_l, site_3_r, site_x = [], [], [], [], []
    rrate_2_l, rrate_2_r, rrate_3_l, rrate_3_r, rrate_x = [], [], [], [], []
    for line in linesour:
        if line.split()[0] == "2L":
            rrate_2_l.append(float(line.split()[4]))
            site_2_l.append(float(line.split()[1]) + (float(line.split()[2]) - float(line.split()[1])) / 2)

    PRM = path_ref_map
    c2L, c2R, c3L, c3R, cX = PRM + "2L_CONV.txt", PRM + "2R_CONV.txt", PRM + "3L_CONV.txt", PRM + "3R_CONV.txt", PRM + "X_CONV.txt"

    # Plotting the data
    width = 1.2  # 1.2
    sub_a = 0.28  # Alpha value for subplots (1= not transparent, 0 = 100% transparent)

  #print(numb)
    # Plotting
    fig.suptitle('Estimation of DroMel recombination rates when misspecifying demographic misspecifi \n Chromosome 2L')
    fig.text(0.5, 0.04, 'Position (bp)', ha='center', va='center')
    fig.text(0.06, 0.5, 'Recombination rate (c/bp)', ha='center', va='center', rotation='vertical')

    colours = ['g','m','y','c','m','b']

    #ax1.set_title("Chromosome 2L")
    if numb == 0:
        line_down = ax1.plot(genmap2array(PRM + "2L.txt", 1), genmap2arrayformatted(c2L), 'b', linewidth=width*2.5, alpha=0.5, label = 'True recombination rate')
    labelname = ["with misspecified demographic model ","no demographic model", "10", "1","20","14"]
    line_up = ax1.plot(site_2_l, convert2centimorgan(rrate_2_l), colours[numb], linewidth=1.0, alpha=1, label = 'ReLERNN, '+ labelname[numb] + " ")

    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(handles, labels)
    return "Done"

def elin2arraywindex(path_output_file, path_ref_map, numb):
    # This function loads and plots the ref data against ReLERNN data
    g = open(os.path.expanduser(path_output_file))
    linesour = g.readlines()[1:]
    g.close()

    # Extracting site and recombination data from ReLERNN
    site_2_l, site_2_r, site_3_l, site_3_r, site_x = [], [], [], [], []
    rrate_2_l, rrate_2_r, rrate_3_l, rrate_3_r, rrate_x = [], [], [], [], []
    for line in linesour:
        if line.split()[0] == "2L":
            rrate_2_l.append(float(line.split()[4]))
            site_2_l.append(float(line.split()[1]) + (float(line.split()[2]) - float(line.split()[1])) / 2)
        elif line.split()[0] == "2R":
            rrate_2_r.append(float(line.split()[4]))
            site_2_r.append(float(line.split()[1]) + (float(line.split()[2]) - float(line.split()[1])) / 2)
        elif line.split()[0] == "3L":
            rrate_3_l.append(float(line.split()[4]))
            site_3_l.append(float(line.split()[1]) + (float(line.split()[2]) - float(line.split()[1])) / 2)
        elif line.split()[0] == "3R":
            rrate_3_r.append(float(line.split()[4]))
            site_3_r.append(float(line.split()[1]) + (float(line.split()[2]) - float(line.split()[1])) / 2)
        elif line.split()[0] == "X":
            rrate_x.append(float(line.split()[4]))
            site_x.append((float(line.split()[1]) + (float(line.split()[2]) - float(line.split()[1])) / 2))

    PRM = path_ref_map
    c2L, c2R, c3L, c3R, cX = PRM + "2L_CONV.txt", PRM + "2R_CONV.txt", PRM + "3L_CONV.txt", PRM + "3R_CONV.txt", PRM + "X_CONV.txt"

    # Plotting the data
    width = 1.2  # 1.2
    sub_a = 0.28  # Alpha value for subplots (1= not transparent, 0 = 100% transparent)

    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex=True, sharey= True)              ####Change this for num of chromosomes

    print("Relernn" + str(site_2_l[0:10]))
    # Plotting
    fig.suptitle('Estimation of DroMel recombination with forced window size')
    fig.text(0.5, 0.04, 'Position (bp)', ha='center', va='center')
    fig.text(0.06, 0.5, 'Recombination rate (c/bp)', ha='center', va='center', rotation='vertical')

    ax1.set_title("Chromosome 2L")
    line_up = ax1.plot(site_2_l, convert2centimorgan(rrate_2_l), 'g', linewidth=width, alpha=1, label = 'ReLERNN, FWS')
    numb = 0
    if numb == 0:
        line_down = ax1.plot(genmap2array(PRM + "2L.txt", 1), genmap2arrayformatted(c2L), 'b', linewidth=width, alpha=sub_a, label = 'True recombination rate')
    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(handles, labels)

    ax2.set_title("Chromosome 2R")
    ax2.plot(genmap2array(PRM + "2R.txt", 1), genmap2arrayformatted(c2R), 'b', linewidth=width, alpha=sub_a)
    ax2.plot(site_2_r, convert2centimorgan(rrate_2_r), 'g', linewidth=width)

    ax3.set_title("Chromosome 3L")
    ax3.plot(genmap2array(PRM + "3L.txt", 1), genmap2arrayformatted(c3L), 'b', linewidth=width, alpha=sub_a)
    ax3.plot(site_3_l, convert2centimorgan(rrate_3_l), 'g', linewidth=width)

    ax4.set_title("Chromosome 3R")
    ax4.plot(genmap2array(PRM + "3R.txt", 1), genmap2arrayformatted(c3R), 'b', linewidth=width, alpha=sub_a)
    ax4.plot(site_3_r, convert2centimorgan(rrate_3_r), 'g', linewidth=width)

    ax5.set_title("Chromosome X")
    ax5.plot(genmap2array(PRM + "X.txt", 1), genmap2arrayformatted(cX), 'b', linewidth=width, alpha=sub_a)
    ax5.plot(site_x, convert2centimorgan(rrate_x), 'g', linewidth=width)

    plt.plot()

    ax5.ticklabel_format(style='sci',scilimits=(6,6),axis='x')

    if 1==1:
        genmap = genmap2array(PRM + "2L.txt", 1)
        #average error:
        r = [c2L, c2R, c3L, c3R, cX]
        filename = ["2L.txt","2R.txt", "3L.txt", "3R.txt", "X.txt"]
        relernn_sites = [site_2_l, site_2_r, site_3_l, site_3_r, site_x ]
        relernn_recombrates = [rrate_2_l, rrate_2_r, rrate_3_l, rrate_3_r, rrate_x ]

        error = []
        bars = ['2L', '2R', '3L', '3R', 'X']
        for i in range(5):
            total_error = 0
            compared_sites = 0
            recomb_rate = genmap2arrayformatted(r[i])
            genmap = genmap2array(PRM + filename[i],1)
            rel_site = relernn_sites[i]
            rel_rrate = relernn_recombrates[i]

            relernn_site_i = 0
            site_index = 0
            while site_index < len(genmap) and relernn_site_i < len(site_2_l):
                if int(genmap[site_index]-50000) < rel_site[relernn_site_i] and int(genmap[site_index]+50000) > rel_site[relernn_site_i]:
                    total_error = total_error +abs(recomb_rate[site_index]-rel_rrate[relernn_site_i])
                    compared_sites += 1
                    site_index +=1
                    relernn_site_i +=1
                elif int(genmap[site_index]-50000) < rel_site[relernn_site_i]:
                    site_index += 1
                elif int(genmap[site_index]+50000) > rel_site[relernn_site_i]:
                    relernn_site_i += 1
                else:
                    raise Exception('Value Error. Contact Jonas Engberg')
            error.append(total_error/compared_sites)
        #plt.bar(bars, error)
    print("Error" , error)
    print("ERRORS")
    plt.show()
    #plt.clf()
    return "Done"


def accuracyplot(path_output_file, path_ref_map):
    # My first try at plotting the accuracy of relern against ref data. Not finished or working
    g = open(os.path.expanduser(path_output_file))
    linesour = g.readlines()[1:]
    g.close()
    site_2L, site_2R, site_3L, site_3R, site_X = [], [], [], [], []
    rrate_2L, rrate_2R, rrate_3L, rrate_3R, rrate_X = [], [], [], [], []

    for line in linesour:
        if (line.split()[0] == "2L"):
            rrate_2L.append(float(line.split()[4]))
            site_2L.append(float(line.split()[1]) + (float(line.split()[2]) - float(line.split()[1])) / 2)
        elif (line.split()[0] == "2R"):
            rrate_2R.append(float(line.split()[4]))
            site_2R.append(float(line.split()[1]) + (float(line.split()[2]) - float(line.split()[1])) / 2)
        elif (line.split()[0] == "3L"):
            rrate_3L.append(float(line.split()[4]))
            site_3L.append(float(line.split()[1]) + (float(line.split()[2]) - float(line.split()[1])) / 2)
        elif (line.split()[0] == "3R"):
            rrate_3R.append(float(line.split()[4]))
            site_3R.append(float(line.split()[1]) + (float(line.split()[2]) - float(line.split()[1])) / 2)
        elif (line.split()[0] == "X"):
            rrate_X.append(float(line.split()[4]))
            site_X.append((float(line.split()[1]) + (float(line.split()[2]) - float(line.split()[1])) / 2))

    # True data
    c2L, c2R, c3L, c3R, cX = path_ref_map + "2L.txt", path_ref_map + "2R.txt", \
                             path_ref_map + "3L.txt", path_ref_map + "3R.txt", \
                             path_ref_map + "X.txt"

    site_2L_cam = genmap2array(c2L, 1)

    if int(site_2L[1]) - int(site_2L[0]) == int(site_2L_cam[1]) - int(site_2L_cam[0]):
        print("hello")  ##
    if int(site_2L[1]) - int(site_2L[0]) == 175000:
        print("hi")  ##

    return ""

def convert2centimorgan(recombrate):
    # Does not convert to centimorgans anymore. This functuion does nothing.
    a = []
    for rates in recombrate:
        a.append(rates)
    return a


def relernnplot(path_ref_map):
    #plot1chromo = 'False'
    plot1chromo = 'True'
    if plot1chromo == 'True':
        print("###### ONE CHROMO ######")
        n = 0
        fig, ax1 = plt.subplots(nrows=1, sharex=True, sharey=True)
        for subdir, dirs, files in os.walk(r"/home/jonas/AppliedBioinf/files_from_UPPMAX/FinalPlots/forcewindow"):
            for filename in files:
                filepath = subdir + os.sep + filename
                if filepath.endswith("PREDICT.txt"):  # BSCORRECTED.txt or PREDICT.txt
                    print(filepath)
                    #elin2arraywindex(filepath, path_ref_map, n)
                    elinChromoPlot(filepath, path_ref_map, n, fig, ax1)
                    n += 1
        plt.show()
    else:
        n= 0
        for subdir, dirs, files in os.walk(r"/home/jonas/AppliedBioinf/files_from_UPPMAX/FinalPlots/forcewindow"):
            for filename in files:
                filepath = subdir + os.sep + filename
                if filepath.endswith("PREDICT.txt"):    # BSCORRECTED.txt or PREDICT.txt
                    print(filepath)
                    elin2arraywindex(filepath, path_ref_map, n)
                    n += 1
    return ("Done")


def relernnaccuracyplot(path_ref_map):
    index = 0
    for subdir, dirs, files in os.walk(r"/home/jonas/AppliedBioinf/files_from_UPPMAX/FinalPlots/forcewindow"):
        for index, filename in enumerate(files):
            filepath = subdir + os.sep + filename
            if filepath.endswith("PREDICT.txt"):
                print(filepath)
                accuracyplot(filepath, path_ref_map)

    return ("Done")


def ldhelmetplot():
    t0 = time.time()
    chromosomes = ["1/output", "2/output", "3/output", "5/output", "6/output"]
    c2L = path_ref_map + "2L.txt"
    #fig, axes = plt.subplots(5)
    for i in range(len(chromosomes)):

        input = "/home/jonas/AppliedBioinf/LDHelmet/Plotting/output" + chromosomes[i] + ".txt"
        f = open(os.path.expanduser(input))
        linestxt = f.readlines()[3:]
        f.close()
        site, recombrate = [], []

        for index, rownum in enumerate(linestxt):
            a = rownum.split()
            site.append(int((int(a[0]) + int(a[1])) / 2))
            recombrate.append(float(a[2]))

        width, sub_a = 1.2, 0.4  # Alpha value for subplots (1= not transparent, 0 = 100% transparent)
        axes[i].set_title("Run " + str(chromosomes[i][0]))
        axes[i].plot(site, recombrate, 'g', linewidth=width, alpha=1)
        # axes[i].plot(genmap2array(c2L, 1)[:5], genmap2array(c2L, 2)[:5], 'b', linewidth=width, alpha=sub_a)
        print(len(c2L))

    print("Time taken: " + str(time.time() - t0))
    #plt.show()


if __name__ == "__main__":
    path_ref_map = "/home/jonas/AppliedBioinf/comeron2012_maps/genetic_map_comeron2012_dm6_chr"
    relernnplot(path_ref_map)


