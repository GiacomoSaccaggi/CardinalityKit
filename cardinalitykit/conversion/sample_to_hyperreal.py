import hashlib
import random
import numpy as np
from tqdm import tqdm

class ExtendedHyperRealSketchFromSample:
    """
    Extended HyperReal sketch that converts sample data to HyperReal sketches
    
    This class enables conversion from sample data (e.g., survey panels)
    to HyperReal sketches for privacy-preserving cardinality estimation.
    """
    
    def __init__(self, b_m, sample_data):
        """
        Initialize sketch from sample data
        
        Args:
            b_m (int): Number of bits for bucket indexing
            sample_data (list): List of tuples (id, weight, attribute)
        """
        self.b_m = b_m
        self.sample_data = sample_data
        self.m = 2 ** b_m
        self.registers = [1.0] * self.m
        self.frequency_counts = [0] * self.m
        self.attribute_samples = [None] * self.m

    def _hash_function(self, data):
        """Double hash for increased entropy"""
        hashed_ = '{:256b}'.format(
            int(hashlib.sha256(
                str(hashlib.sha256(str(data).encode('utf-8')).hexdigest()).encode('utf-8')
            ).hexdigest(), 16)
        ).replace(' ', '0')
        
        off = 32
        if (self.b_m) * 4 + off > 256:
            hashed = hashed_
        else:
            hashed = hashed_[1:(self.b_m) * 3]
        return hashed

    def _bit_accuracy(self, u1, u2):
        """Calculate bit accuracy between two integers"""
        bin_U1 = [i for i in bin(u1)[2:]][:8]
        bin_U2 = [i for i in bin(u2)[2:]][:8]
        accuracy = np.sum([b1 == b2 for b1, b2 in zip(bin_U1, bin_U2)]) / 9
        return accuracy

    def naive_associate(self, sum_weights=100000):
        """
        Naive association method for sample to HyperReal conversion
        
        Args:
            sum_weights (int): Total weight for virtual population
        """
        virtual_people = {id: [] for id, we, attr in self.sample_data}
        
        for virtual_person in tqdm([f"VirtualPerson_{i}" for i in range(sum_weights)]):
            # Pick sample member
            index_vp = int(hashlib.sha256(str(virtual_person).encode('utf-8')).hexdigest()[:8], 16)
            
            affinity_hashing = lambda vp, sample: self._bit_accuracy(
                vp, int(hashlib.sha256(str(sample).encode('utf-8')).hexdigest()[:8], 16)
            )
            
            ids_sample = [
                round(-np.log(affinity_hashing(index_vp, id) + 0.000001) / we) 
                for id, we, attr in self.sample_data
            ]
            user_id, weight, user_attr = self.sample_data[ids_sample.index(min(ids_sample))]
            virtual_people[user_id].append((virtual_person, user_attr))
        
        # Update sketch with virtual people
        for sample_name, virtual_people_associated in virtual_people.items():
            for user_id, user_attr in virtual_people_associated:
                x = self._hash_function(user_id)
                j = int(str(x)[:self.b_m], 2)
                int_val = int(hashlib.sha256(str(user_id).encode()).hexdigest()[:8], 16)
                w = int_val / (16 ** 8 - 1)  # Normalize to [0, 1]
                
                if self.registers[j] > w:
                    self.frequency_counts[j] = 1
                    self.attribute_samples[j] = user_attr
                elif self.registers[j] == w:
                    self.frequency_counts[j] += 1
                    if self.attribute_samples[j] != user_attr:
                        self.attribute_samples[j] = user_attr
                
                self.registers[j] = min(self.registers[j], w)

    def fast_associate(self, sum_weights=100000, D=15):
        """
        Fast association method for sample to HyperReal conversion
        
        Args:
            sum_weights (int): Total weight for virtual population
            D (int): Depth parameter for association
        """
        virtual_people = {
            id: [('sample_fake', 'Attribute_fake', 1) for i in range(D-1)] 
            for id, we, attr in self.sample_data
        }
        
        for virtual_person in tqdm([f"VirtualPerson_{i}_{random.randint(1000,9999)}" for i in range(sum_weights*D)]):
            # Pick sample member
            index_vp = int(hashlib.sha256(
                str(hashlib.sha256(str(virtual_person).encode('utf-8')).hexdigest()).encode('utf-8')
            ).hexdigest()[:8], 16)
            
            affinity_hashing = lambda vp, sample: self._bit_accuracy(
                vp, int(hashlib.sha256(
                    str(hashlib.sha256(str(sample).encode('utf-8')).hexdigest()).encode('utf-8')
                ).hexdigest()[:8], 16)
            )
            
            ids_sample = [
                round(-np.log(affinity_hashing(index_vp, id) + 0.000001) / we) 
                for id, we, attr in self.sample_data
            ]
            user_id, weight, user_attr = self.sample_data[ids_sample.index(min(ids_sample))]
            
            new_sample = []
            hashed_w = index_vp / (16 ** 8 - 1)
            flag_just_put = False
            
            for vp, attr, w in virtual_people[user_id]:
                if not flag_just_put and hashed_w < w:
                    new_sample.append((virtual_person, user_attr, hashed_w))
                    flag_just_put = True
                else:
                    new_sample.append((vp, attr, w))
            virtual_people[user_id] = new_sample
        
        # Update sketch with virtual people
        for sample_name, virtual_people_associated in tqdm(virtual_people.items()):
            ls_Sd = []
            ids_temp_saved = []
            
            for user_id, user_attr, _ in virtual_people_associated:
                x = self._hash_function(user_id)
                j = int(str(x)[:self.b_m], 2)
                ids_temp_saved.append(j)
                
                int_val = int(hashlib.sha256(
                    str(hashlib.sha256(str(user_id).encode()).hexdigest()).encode()
                ).hexdigest()[:8], 16)
                w = int_val / (16 ** 8 - 1)
                ls_Sd.append(w)
                
                if self.registers[j] > w:
                    self.frequency_counts[j] = 1
                    self.attribute_samples[j] = user_attr
                elif self.registers[j] == w:
                    self.frequency_counts[j] += 1
                    if self.attribute_samples[j] != user_attr:
                        self.attribute_samples[j] = user_attr
                
                self.registers[j] = min(self.registers[j], w)

    def get_sketch(self):
        """Get internal sketch data structures"""
        return self.registers, self.frequency_counts, self.attribute_samples

    def get_cardinality_estimate(self):
        """Get overall cardinality estimate"""
        return (self.m ** 2) / sum(self.registers)

    def get_frequency_for_attr(self, attr=None):
        """
        Get frequency estimate for specific attribute or all attributes
        
        Args:
            attr: Specific attribute to get frequency for, or None for all
            
        Returns:
            float or dict: Frequency estimate(s)
        """
        attr_distribution = {}
        for count, attr_sample in zip(self.frequency_counts, self.attribute_samples):
            if attr_sample:
                attr_distribution[attr_sample] = attr_distribution.get(attr_sample, 0) + count
        
        total = sum(attr_distribution.values())
        if total > 0:
            cardinality = self.get_cardinality_estimate()
            for attr_sample in attr_distribution:
                attr_distribution[attr_sample] = (attr_distribution[attr_sample] / total) * cardinality

        return attr_distribution.get(attr) if attr else attr_distribution