import math
import sys

class HyperLogLogEstimator:
    """
    HyperLogLog cardinality estimator
    
    The most widely used cardinality estimation algorithm that uses
    harmonic mean instead of arithmetic mean for better accuracy.
    """
    
    def __init__(self, k=10):
        """
        Initialize HyperLogLog estimator
        
        Args:
            k (int): Number of bits for bucket indexing (2^k buckets)
        """
        self.k = k
        self.m = 2 ** k
        self.buckets = [0] * self.m
    
    def update(self, hash_value):
        """Update the estimator with a hash value"""
        j = str(hash_value)[:self.k]
        j = int(j, 2)
        
        data = hash_value[self.k:]
        rank = 1
        for c in reversed(data):
            if c == "0":
                rank += 1
            else:
                break
        
        self.buckets[j] = max(self.buckets[j], rank)
    
    def estimate(self):
        """Get cardinality estimate"""
        # Calculate harmonic mean
        total = 0
        for bucket in self.buckets:
            total += 2 ** (-1 * bucket)
        mean = total ** -1
        
        estimate = (self.m ** 2) * mean
        
        # Bias correction
        if self.k <= 4:
            BIAS = 0.673
        elif self.k == 5:
            BIAS = 0.697
        else:
            BIAS = 0.7213 / (1 + (1.079 / self.m))
        
        estimate = BIAS * estimate
        
        # Small range correction
        if estimate < ((5 / 2) * self.m):
            zeros = sum(1 for bucket in self.buckets if bucket == 0)
            if zeros > 0:
                estimate = self.m * math.log(self.m / zeros)
        
        # Large range correction
        elif estimate > ((2 ** 32) / 30):
            estimate = -1 * (2 ** 32) * math.log(1 - (estimate / (2 ** 32)))
        
        return estimate
    
    def memory_usage(self):
        """Get memory usage in bytes"""
        return sys.getsizeof(self.buckets)

def HyperLogLog(hashes, k):
    """Legacy function for backward compatibility"""
    estimator = HyperLogLogEstimator(k)
    for hash_val in hashes:
        estimator.update(hash_val)
    return estimator.estimate(), estimator.memory_usage()