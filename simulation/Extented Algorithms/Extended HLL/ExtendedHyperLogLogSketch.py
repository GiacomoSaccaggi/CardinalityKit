
import hashlib

import numpy as np


class ExtendedHyperLogLogSketch:
    def __init__(self, b_m, b_s):
        self.b_m = b_m
        self.b_s = b_s
        self.m = 2 ** b_m
        self.s = 2 ** b_s
        self.registers = [0] * self.m
        self.indicator_space = [0] * self.m
        self.frequency_counts = [0] * self.m
        self.attribute_samples = [None] * self.m

    def _hash_function(self, data):
        # hashed two times to increase the entropy
        hashed_ = '{:256b}'.format(int(hashlib.sha256(str(hashlib.sha256(str(data).encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest(), 16)).replace(' ','0')
        off = 32
        if (self.b_m + self.b_s)*4+off > 256:
            hashed = hashed_
        else:
            hashed = hashed_[1:(self.b_m + self.b_s)*3]
        return hashed # self._decimal_to_binary(int(hashed, 2)) == hashed and int(hashed_, 2) == int(hashlib.sha256(data.encode('utf-8')).hexdigest(), 16)


    def update_sketch(self, event):
        user_id = event['id_to_count']
        user_attr = event['attribute']

        x = self._hash_function(user_id)
        j = int(str(x)[:self.b_m], 2) #  <x0, . . . , xbm−1>2; self._decimal_to_binary(x % self.b_m+1)
        i = int(str(x)[(self.b_m +1):(self.b_m + self.b_s+1)], 2)#  <xbm, . . . , xbm+bs−1>2;
        data = str(x)[(self.b_m + self.b_s+2):]
        w = 1
        for c in reversed(data):
            if c == "0":
                w += 1
            else:
                break

        if self.registers[j] < w or (self.registers[j] == w and self.indicator_space[j] < i):
            self.indicator_space[j] = i
            self.frequency_counts[j] = 1
            self.attribute_samples[j] = user_attr
        elif self.registers[j] == w and self.indicator_space[j] == i:
            self.frequency_counts[j] += 1
            if self.attribute_samples[j] != user_attr:
                # Here, the attribute is simply overwritten with the last one found
                # but functions can be created that weight which one to putFO
                self.attribute_samples[j] = user_attr

        self.registers[j] = max(self.registers[j], w)

    def get_sketch(self):
        return self.registers, self.indicator_space, self.frequency_counts, self.attribute_samples

    def get_cardinality_estimate(self):
        import math
        # get the harmonic mean of the buckets
        total = 0
        for bucket in self.registers:
            total += 2 ** (-1 * bucket)
        mean = total ** -1
        # calculate estimate
        estimate = (self.m ** 2) * mean

        # bias can be approximated with the formula 0.7213 / (1 + (1.079/2^k)) for k >= 6
        # or for values of k < 6 we can use pre-calculated bias factors
        if self.b_m <= 4:
            BIAS = 0.673
        elif self.b_m == 5:
            BIAS = 0.697
        else:
            BIAS = 0.7213 / (1 + (1.079 / self.m))

        # correct for bias
        estimate = BIAS * estimate

        # small range correction
        if estimate < ((5 / 2) * self.m):
            # get count of registers with rank of 0
            zeros = 0
            for i in self.registers:
                if self.registers[i] == 0:
                    zeros += 1
            # apply small range correction
            if not zeros == 0:
                estimate = self.m * math.log(estimate, 2)

        # large range correction
        elif estimate > ((2 ** 32) / 30):
            estimate = -1 * (2 ** 32) * math.log(1 - (estimate / (2 ** 32)))
        return estimate

    def get_frequency_for_attr(self, attr=None):
        attr_distribution = {}
        for count, attr_sample in zip(self.frequency_counts, self.attribute_samples):
            if attr_sample:
                if attr_sample in attr_distribution.keys():
                    attr_distribution[attr_sample] += count
                else:
                    attr_distribution[attr_sample] = count
        total = sum(attr_distribution.values())
        for attr_sample in attr_distribution.keys():
            attr_distribution[attr_sample] /= total
        for attr_sample in attr_distribution.keys():
            attr_distribution[attr_sample] *= self.get_cardinality_estimate()

        if attr:
            estimate = attr_distribution[attr]
        else:
            estimate = attr_distribution

        return estimate


results = {}

for k in range(5,20):

    # Example usage of ExtendedHyperLogLogSketch class
    ehll_sketch = ExtendedHyperLogLogSketch(b_m=k, b_s=k)  # Replace with desired values for b_m and b_s

    filename = "../../Parking_Violations_Issued_-_Fiscal_Year_2019.csv"
    from tqdm import tqdm
    with open(filename, 'r') as f:
        cols = f.readline().split(',')
        cols_id = ['Plate ID',  'Plate Type',  'Plate Type', 'Vehicle Body Type', 'Vehicle Make', 'Vehicle Color', 'Vehicle Year']
        attribute_col = 'Registration State'
        id_index = [cols.index(col_id) for col_id in cols_id]
        attribute_index = cols.index(attribute_col)
        id_to_count_ls = []
        attribute_ls = []
        for line in tqdm(f.readlines()):
            tmp = line.split(',')
            id_t = ''.join([tmp[i] for i in id_index])
            attr_t = tmp[attribute_index]
            ehll_sketch.update_sketch({'id_to_count':id_t,
                                       'attribute': attr_t})
            attribute_ls.append(attr_t)
            id_to_count_ls.append(id_t)

    # self = ehll_sketch
    ehll_sketch.get_sketch()

    # Estimate approximate cardinality
    cardinality_estimate = ehll_sketch.get_cardinality_estimate()
    print(f"Approximate cardinality: {cardinality_estimate}")
    print(f"True cardinality: {len(set(id_to_count_ls))}")

    ehll_res = []
    ehll_err = []
    for attr in set(attribute_ls):
        try:
            ehll_err.append((ehll_sketch.get_frequency_for_attr(attr)-len(set([(c,w) for c,w in zip(id_to_count_ls, attribute_ls) if w==attr])))/len(set([(c,w) for c,w in zip(id_to_count_ls, attribute_ls) if w==attr])))
            ehll_res.append(ehll_sketch.get_frequency_for_attr(attr))
        except:
            pass

    results[k] = {}


    results[k]['HLL Error'] = (cardinality_estimate-len(set(id_to_count_ls)))/len(set(id_to_count_ls))
    results[k]['EHLL Estimate'] = ehll_res
    results[k]['EHLL Error'] = ehll_err


import pandas as pd
import numpy as np
ls = []
for k,v in results.items():
    print(k)
    print(sum([e*v for e,v in zip(v['EHLL Error'], v['EHLL Estimate'])])/(len(v['EHLL Error'])*np.mean(v['EHLL Estimate'])))
    ls.append([k, v['HLL Error'], sum([e*v for e,v in zip(v['EHLL Error'], v['EHLL Estimate'])])/(len(v['EHLL Error'])*np.mean(v['EHLL Estimate']))])


df = pd.DataFrame(ls, columns = ['k', 'Percentage Error on HLL', 'Percentage Error on EHLL'])
df.to_csv('ExtendedHyperLogLogSimulation.csv', index = False)

