import hashlib
import math

class ExtendedHyperLogLogSketch:
    """
    Extended HyperLogLog with demographic attribute tracking
    
    Enhances standard HyperLogLog to track frequency counts and
    attribute samples for demographic analysis.
    """
    
    def __init__(self, b_m, b_s=None):
        """
        Initialize Extended HyperLogLog sketch
        
        Args:
            b_m (int): Number of bits for bucket indexing
            b_s (int): Number of bits for indicator space (optional)
        """
        self.b_m = b_m
        self.b_s = b_s or b_m
        self.m = 2 ** b_m
        self.s = 2 ** self.b_s
        self.registers = [0] * self.m
        self.indicator_space = [0] * self.m
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
        if (self.b_m + self.b_s) * 4 + off > 256:
            hashed = hashed_
        else:
            hashed = hashed_[1:(self.b_m + self.b_s) * 3]
        return hashed

    def update_sketch(self, event):
        """
        Update sketch with new event
        
        Args:
            event (dict): Event with 'id_to_count' and 'attribute' keys
        """
        user_id = event['id_to_count']
        user_attr = event['attribute']

        x = self._hash_function(user_id)
        j = int(str(x)[:self.b_m], 2)
        i = int(str(x)[(self.b_m + 1):(self.b_m + self.b_s + 1)], 2)
        data = str(x)[(self.b_m + self.b_s + 2):]
        
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
                self.attribute_samples[j] = user_attr

        self.registers[j] = max(self.registers[j], w)

    def get_sketch(self):
        """Get internal sketch data structures"""
        return self.registers, self.indicator_space, self.frequency_counts, self.attribute_samples

    def get_cardinality_estimate(self):
        """Get overall cardinality estimate"""
        total = sum(2 ** (-1 * bucket) for bucket in self.registers)
        mean = total ** -1
        estimate = (self.m ** 2) * mean

        # Bias correction
        if self.b_m <= 4:
            BIAS = 0.673
        elif self.b_m == 5:
            BIAS = 0.697
        else:
            BIAS = 0.7213 / (1 + (1.079 / self.m))

        estimate = BIAS * estimate

        # Small range correction
        if estimate < ((5 / 2) * self.m):
            zeros = sum(1 for reg in self.registers if reg == 0)
            if zeros > 0:
                estimate = self.m * math.log(self.m / zeros)

        # Large range correction
        elif estimate > ((2 ** 32) / 30):
            estimate = -1 * (2 ** 32) * math.log(1 - (estimate / (2 ** 32)))
            
        return estimate

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