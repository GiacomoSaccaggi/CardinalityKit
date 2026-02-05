# The Evolution of the HyperLogLog Estimator

import sys, os.path, time, statistics
import math

import pandas as pd

# sys.path.append("./Articolo_DSCI_Journal/HLL_tests/")
import csv_parser, ActualCount
import FlajoletMartinEstimator, LogLogEstimator, SuperLogLogEstimator, HyperLogLogEstimator

# the file to parse for unique plates
filename = "../Parking_Violations_Issued_-_Fiscal_Year_2019.csv"


columns = ['model', 'result', 'std_estimate', 'mpe', 'mape', 'ram_used', 'std_ram_used', 'k']
ls = []

# number of runs to average with different hashes
loops_to_run = 8

print ("Cardinality Estimation Algorithm Comparison")
print ("Comparative analysis of probabilistic counting algorithms\n")

# check if the Plate ID hashes have been generated before
# if so, load them. if not, create them
plate_hashes = csv_parser.create_hashes(filename)
print(str(len(plate_hashes))+" plate hashes loaded.\n")


len(set(plate_hashes))
# directly tally the number of unique plates
print("Calculating exact amount of unique plates..")
exact_unique, ram_used = ActualCount.get_exact_unique_using_set(filename)
print("There are exactly "+str(exact_unique)+" unique plates..\n")
ls.append(('Count(distinct())', exact_unique, 0, 0, 0, ram_used, 0, None))


#run tests and store results
fm = []
fm_ram = []
for i in range(0, loops_to_run):
    #print loading message
    sys.stdout.write("Running test " + str(i + 1) + " of " + str(loops_to_run) + ".. (this may take a moment)")
    sys.stdout.flush()

    #Generate test hashes
    hashes = []
    for hash in plate_hashes:
        #encode the hash in binary
        hash = '{:256b}'.format(int(hash, 16)).replace(' ','0')

        off = i*32
        temp = hash[len(hash)-(32+off)+1:len(hash)-off]
        hashes.append(temp)

    #approximate values and add to results array
    estimate, ram_used = FlajoletMartinEstimator.FlajoletMartin(hashes)
    fm.append(estimate)
    fm_ram.append(ram_used)
    #reset line
    sys.stdout.write('\r')
ls.append(('FlajoletMartinEstimator',
          statistics.mean(fm),
          statistics.pstdev(fm),
          abs(exact_unique - statistics.mean(fm)) / exact_unique,
          (exact_unique - statistics.mean(fm)) / exact_unique,
          statistics.mean(fm_ram),
          statistics.pstdev(fm_ram),
          None))



from tqdm import tqdm
# the number of bits to use in identifying buckets
# 2**ex_buckets = number of buckets
ex_buckets = 14
for ex_buckets in tqdm(range(2, 20)):
    #run tests and store results
    ll = []
    sll = []
    hll = []
    ll_ram = []
    sll_ram = []
    hll_ram = []
    for i in range(0, loops_to_run):
        #print loading message
        sys.stdout.write("Running test " + str(i + 1) + " of " + str(loops_to_run) + ".. (this may take a moment)")
        sys.stdout.flush()

        #Generate test hashes
        hashes = []
        for hash in plate_hashes:
            #encode the hash in binary
            hash = '{:256b}'.format(int(hash, 16)).replace(' ','0')

            off = i*32
            temp = hash[len(hash)-(32+off)+1:len(hash)-off]
            hashes.append(temp)

        #approximate values and add to results array
        estimate, ram_used = LogLogEstimator.LogLog(hashes, ex_buckets)
        ll.append(estimate)
        ll_ram.append(ram_used)
        estimate, ram_used = SuperLogLogEstimator.SuperLogLog(hashes, ex_buckets)
        sll.append(estimate)
        sll_ram.append(ram_used)
        estimate, ram_used = HyperLogLogEstimator.HyperLogLog(hashes, ex_buckets)
        hll.append(estimate)
        hll_ram.append(ram_used)

        #reset line
        sys.stdout.write('\r')

    ls.append(('LogLogEstimator',
              statistics.mean(ll),
              statistics.pstdev(ll),
              abs(exact_unique - statistics.mean(ll)) / exact_unique,
              (exact_unique - statistics.mean(ll)) / exact_unique,
              statistics.mean(ll_ram),
              statistics.pstdev(ll_ram),
              ex_buckets))

    ls.append(('SuperLogLogEstimator',
              statistics.mean(sll),
              statistics.pstdev(sll),
              abs(exact_unique - statistics.mean(sll)) / exact_unique,
              (exact_unique - statistics.mean(sll)) / exact_unique,
              statistics.mean(sll_ram),
              statistics.pstdev(sll_ram),
              ex_buckets))

    ls.append(('HyperLogLogEstimator',
              statistics.mean(hll),
              statistics.pstdev(hll),
              abs(exact_unique - statistics.mean(hll)) / exact_unique,
              (exact_unique - statistics.mean(hll)) / exact_unique,
              statistics.mean(hll_ram),
              statistics.pstdev(hll_ram),
              ex_buckets))




df = pd.DataFrame(ls, columns = columns)


df.to_csv('hll_simulation.csv')
df.to_csv('hll_simulation_tableau.csv', sep = '|', decimal = ',')