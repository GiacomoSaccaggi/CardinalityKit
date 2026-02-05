
import hashlib, random

import numpy as np


class ExtendedHyperRealSketch:
    def __init__(self, b_m, b_s):
        self.b_m = b_m
        self.b_s = b_s
        self.m = 2 ** b_m
        self.s = 2 ** b_s
        self.registers = [1.0] * self.m
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
        int_val = int(hashlib.sha256(str(user_id).encode()).hexdigest()[:8], 16)
        # Normalizes the integer in the range [0, 1]
        w = int_val / (16 ** 8 - 1)

        if self.registers[j] > w:
            self.frequency_counts[j] = 1
            self.attribute_samples[j] = user_attr
        elif self.registers[j] == w:
            self.frequency_counts[j] += 1
            if self.attribute_samples[j] != user_attr:
                # Here, the attribute is simply overwritten with the last one found
                # but functions can be created that weight which one to putFO
                self.attribute_samples[j] = user_attr

        self.registers[j] = min(self.registers[j], w)

    def get_sketch(self):
        return self.registers,  self.frequency_counts, self.attribute_samples

    def get_cardinality_estimate(self):
        estimate = (self.m ** 2) / sum(self.registers)
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

    # Example usage of ExtendedHyperRealSketch class
    ehr_sketch = ExtendedHyperRealSketch(b_m=k, b_s=k)  # Replace with desired values for b_m and b_s

    filename = "../../Parking_Violations_Issued_-_Fiscal_Year_2019.csv"
    from tqdm import tqdm
    with open(filename, 'r') as f:
        cols = f.readline().split(',')
        cols_id = ['Plate ID',  'Plate Type', 'Plate Type', 'Vehicle Body Type', 'Vehicle Make', 'Vehicle Color', 'Vehicle Year']
        attribute_col = 'Registration State'
        id_index = [cols.index(col_id) for col_id in cols_id]
        attribute_index = cols.index(attribute_col)
        id_to_count_ls = []
        attribute_ls = []
        for line in tqdm(f.readlines()):
            tmp = line.split(',')
            id_t = ''.join([tmp[i] for i in id_index])
            attr_t = tmp[attribute_index]
            ehr_sketch.update_sketch({'id_to_count': id_t,
                                       'attribute': attr_t})
            attribute_ls.append(attr_t)
            id_to_count_ls.append(id_t)

    # self = ehr_sketch
    ehr_sketch.get_sketch()

    # Estimate approximate cardinality
    cardinality_estimate = ehr_sketch.get_cardinality_estimate()
    print(f"Approximate cardinality: {cardinality_estimate}")
    print(f"True cardinality: {len(set(id_to_count_ls))}")

    ehr_res = []
    ehr_err = []
    for attr in set(attribute_ls):
        try:
            print(f"Frequency for '{attr}': {int(ehr_sketch.get_frequency_for_attr(attr))} ({(ehr_sketch.get_frequency_for_attr(attr)-len(set([(c,w) for c,w in zip(id_to_count_ls, attribute_ls) if w==attr])))/len(set([(c,w) for c,w in zip(id_to_count_ls, attribute_ls) if w==attr])))}")
            ehr_err.append((ehr_sketch.get_frequency_for_attr(attr)-len(set([(c,w) for c,w in zip(id_to_count_ls, attribute_ls) if w==attr])))/len(set([(c,w) for c,w in zip(id_to_count_ls, attribute_ls) if w==attr])))
            ehr_res.append(ehr_sketch.get_frequency_for_attr(attr))
        except:
            pass

    results[k] = {}


    results[k]['hr Error'] = (cardinality_estimate-len(set(id_to_count_ls)))/len(set(id_to_count_ls))
    results[k]['Ehr Estimate'] = ehr_res
    results[k]['Ehr Error'] = ehr_err


import pandas as pd
import numpy as np
ls = []
for k,v in results.items():
    print(k)
    print(sum([e*v for e,v in zip(v['Ehr Error'], v['Ehr Estimate'])])/(len(v['Ehr Error'])*np.mean(v['Ehr Estimate'])))
    ls.append([k, v['hr Error'], sum([e*v for e,v in zip(v['Ehr Error'], v['Ehr Estimate'])])/(len(v['Ehr Error'])*np.mean(v['Ehr Estimate']))])


df = pd.DataFrame(ls, columns = ['k', 'Percentage Error on HR', 'Percentage Error on EHR'])
df.to_csv('ExtendedHyperRealSimulation.csv', index = False)

