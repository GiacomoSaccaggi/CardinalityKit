

# Importing packages
import json
import math
import logging
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import OrderedDict
from scipy.optimize import minimize
pd.options.display.float_format = "{:.5f}".format
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 10000)
pd.set_option('display.max_colwidth', 1000)
import hashlib, random

import numpy as np
import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))



class ExtendedHyperRealSketchFromSample:
    def __init__(self, b_m, sample_data):
        self.b_m = b_m
        self.sample_data = sample_data
        self.m = 2 ** b_m
        self.registers = [1.0] * self.m
        self.frequency_counts = [0] * self.m
        self.attribute_samples = [None] * self.m

    def _hash_function(self, data):
        # hashed two times to increase the entropy
        hashed_ = '{:256b}'.format(int(hashlib.sha256(str(hashlib.sha256(str(data).encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest(), 16)).replace(' ','0')
        off = 32
        if (self.b_m)*4+off > 256:
            hashed = hashed_
        else:
            hashed = hashed_[1:(self.b_m)*3]
        return hashed # self._decimal_to_binary(int(hashed, 2)) == hashed and int(hashed_, 2) == int(hashlib.sha256(data.encode('utf-8')).hexdigest(), 16)


    def FastAssociate(self, sum_weights=100000, D=15):
        import math

        def bit_accuracy(u1, u2):
            bin_U1 = [i for i in bin(u1)[2:]][:8]
            bin_U2 = [i for i in bin(u2)[2:]][:8]
            accuracy = np.sum([b1 == b2 for b1, b2 in zip(bin_U1, bin_U2)]) / 9
            return accuracy

        virtual_people = {id:[('sample_fake', 'Attribute_fake', 1) for i in range(D-1)] for id, we, attr in self.sample_data}
        for virtual_person in tqdm([f"VirtualPerson_{i}_"+generate_random_string(10) for i in range(sum_weights*D)]):
            #### PICK PANELIST
            index_vp = int(hashlib.sha256(str(hashlib.sha256(str(virtual_person).encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()[:8], 16)
            affinity_hashing = lambda vp, pan: bit_accuracy(vp, int(hashlib.sha256(str(hashlib.sha256(str(pan).encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()[:8], 16))
            ids_sample = [round(-np.log(affinity_hashing(index_vp,id)+0.000001) / we) for id, we, attr in self.sample_data]
            user_id, weight, user_attr = self.sample_data[ids_sample.index(min(ids_sample))]
            new_sample = []
            hashed_w =  index_vp / (16 ** 8 - 1)
            flag_just_put = False
            for vp, attr, w in virtual_people[user_id]:
                if not flag_just_put and hashed_w < w:
                    new_sample.append((virtual_person, user_attr, hashed_w))
                    flag_just_put = True
                else:
                    new_sample.append((vp, attr, w))
            virtual_people[user_id] = new_sample
        result = []
        result_with_name = {}
        for i in tqdm(range(len(sample_data))):
            result.append((len(virtual_people[sample_data[i][0]])-round(sample_data[i][1]*sum_weights)))
            result_with_name[sample_data[i][0]] = f"{len(virtual_people[sample_data[i][0]])} ({(len(virtual_people[sample_data[i][0]])-round(sample_data[i][1]*sum_weights))/sum_weights})"
        print(sum([abs(i/sum_weights) for i in result])/len(result))
        for sample_name, virtual_people_associated in tqdm(virtual_people.items()):
            ls_Sd = []
            ids_temp_saved = []
            for user_id, user_attr, _ in virtual_people_associated:
                x = self._hash_function(user_id)
                j = int(str(x)[:self.b_m], 2) #  <x0, . . . , xbm−1>2; self._decimal_to_binary(x % self.b_m+1)
                ids_temp_saved.append(j)
                int_val = int(hashlib.sha256(str(hashlib.sha256(str(user_id).encode()).hexdigest()).encode()).hexdigest()[:8], 16)
                # Normalizes the integer in the range [0, 1]
                w = int_val / (16 ** 8 - 1)
                ls_Sd.append(w)
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
            Sd = min(ls_Sd)
            count_sample = int(sum_weights*[i for i in self.sample_data if i[0] == sample_name][0][1] - D)
            remain_sample = 1
            for n, [w, fr, attr] in tqdm(enumerate(zip(reversed(self.registers), reversed(self.frequency_counts), reversed(self.attribute_samples)))):
                if remain_sample >= count_sample:
                    print(remain_sample)
                    break
                if (len(self.registers)-n)>max(ids_temp_saved):
                    weights = [tupla[1] for tupla in self.sample_data]
                    # Calculate total weight sum
                    total_sum = sum(weights)
                    # Calculate normalized probabilities
                    normalized_probs = [weight / total_sum for weight in weights]
                    # Extract index based on normalized probabilities
                    extraction_index = random.choices(range(len(self.sample_data)), weights = normalized_probs)[0]
                    # Extract values from tuple corresponding to extracted index
                    name, weight, attr = self.sample_data[extraction_index]
                    int_val = int(hashlib.sha256(str(hashlib.sha256(str(name).encode()).hexdigest()).encode()).hexdigest()[:8], 16)
                    w = int_val / (16 ** 8 - 1)
                    final_w = Sd+(1-Sd)*(1-(w**(1/(count_sample))))
                    if self.registers[n]>final_w and n not in ids_temp_saved:
                        remain_sample += 1
                        self.registers[n] = final_w # probabilita_normalizzate[indice_estrazione]
                        self.frequency_counts[n] = 1
                        self.attribute_samples[n] = attr


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






df = pd.read_csv('characters.csv', sep = ';')
df['email'] = [n.replace(' ', '_').lower()+'@'+w.replace(' ', '_').lower()+'.com' for i, [n,w] in df[['Nome', 'World']].iterrows()]


# Generate random probabilities
np.random.seed(42)  # To make results reproducible
df['Weight'] = np.random.rand(len(df))

# Normalize probabilities so that the sum is 1 for each row
df['Weight'] /= df['Weight'].sum()

results = {}
k=14
sum_weights = 100000
rappr = 1
replicate_sample = 40*rappr
random_strings = [generate_random_string(10) for i in range(replicate_sample)]
sample_data = [(e,w/(replicate_sample+1),d) for n, [w, e, d] in df[['Weight', 'email', 'demo_buckets']].reset_index(drop = True).iterrows()]
for rs in random_strings:
    sample_data.extend([(rs+'_'+e, w/(11), d) for n, [w, e, d] in df[['Weight', 'email', 'demo_buckets']].reset_index(drop = True).iterrows()])

ehr_sketch = ExtendedHyperRealSketchFromSample(b_m=k, sample_data=sample_data)
ehr_sketch.FastAssociate(sum_weights=sum_weights)

# self = ehr_sketch
ehr_sketch.get_sketch()

# Estimate approximate cardinality
cardinality_estimate = ehr_sketch.get_cardinality_estimate()
print(f"Approximate cardinality: {cardinality_estimate}")
print(f"True cardinality: {sum_weights}")

ehr_res = []
ehr_err = []
for attr in df['demo_buckets'].unique():
    try:
        real=df[(df['demo_buckets']==attr)]['Weight'].sum()*sum_weights
        print(f"Frequency for '{attr}': {int(ehr_sketch.get_frequency_for_attr(attr))} ({(ehr_sketch.get_frequency_for_attr(attr) - real) / real})")
        ehr_err.append((ehr_sketch.get_frequency_for_attr(attr) - real) / real)
        ehr_res.append(ehr_sketch.get_frequency_for_attr(attr))
    except:
        pass
sample_representativity = (32*(replicate_sample+1))/sum_weights
results[sample_representativity] = {}

results[sample_representativity]['hr Error'] = (cardinality_estimate - sum_weights) / sum_weights
results[sample_representativity]['Ehr Estimate'] = ehr_res
results[sample_representativity]['Ehr Error'] = ehr_err






import pandas as pd
import numpy as np
ls = []
for k,v in results.items():
    print(k)
    print(sum([e*v for e,v in zip(v['Ehr Error'], v['Ehr Estimate'])])/(len(v['Ehr Error'])*np.mean(v['Ehr Estimate'])))
    ls.append([k, v['hr Error'], sum([e*v for e,v in zip(v['Ehr Error'], v['Ehr Estimate'])])/(len(v['Ehr Error'])*np.mean(v['Ehr Estimate']))])





