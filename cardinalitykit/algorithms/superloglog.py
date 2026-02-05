import math
import sys

class SuperLogLogEstimator:
    """
    SuperLogLog cardinality estimator
    
    An improvement over LogLog that uses outlier elimination
    to further reduce variance in the estimate.
    """
    
    def __init__(self, k=10, cutoff=0.7):
        """
        Initialize SuperLogLog estimator
        
        Args:
            k (int): Number of bits for bucket indexing (2^k buckets)
            cutoff (float): Fraction of buckets to keep after sorting
        """
        self.k = k
        self.m = 2 ** k
        self.cutoff = cutoff
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
        lower = math.floor(self.cutoff * self.m)
        
        # Apply cutoff by sorting and removing outliers
        sorted_buckets = sorted(self.buckets)
        trimmed_buckets = sorted_buckets[:lower]
        
        average = sum(trimmed_buckets) / lower
        estimate = self.m * 2 ** average
        
        BIAS = 0.764
        return BIAS * estimate
    
    def memory_usage(self):
        """Get memory usage in bytes"""
        return sys.getsizeof(self.buckets)

def SuperLogLog(hashes, k):
    """Legacy function for backward compatibility"""
    estimator = SuperLogLogEstimator(k)
    for hash_val in hashes:
        estimator.update(hash_val)
    return estimator.estimate(), estimator.memory_usage()