import sys
import hashlib

class HyperRealEstimator:
    """
    HyperReal cardinality estimator
    
    An unbiased alternative to HyperLogLog that uses minimum values
    instead of maximum ranks for cardinality estimation.
    """
    
    def __init__(self, k=10):
        """
        Initialize HyperReal estimator
        
        Args:
            k (int): Number of bits for bucket indexing (2^k buckets)
        """
        self.k = k
        self.m = 2 ** k
        self.buckets = [1.0] * self.m
    
    def update(self, hash_value):
        """Update the estimator with a hash value"""
        int_val = int(hashlib.sha256(str(hash_value).encode()).hexdigest()[:8], 16)
        x = int_val / (16 ** 8 - 1)  # Normalize to [0, 1]
        
        j = str(hash_value)[:self.k]
        j = int(j, 2)
        
        self.buckets[j] = min(self.buckets[j], x)
    
    def estimate(self):
        """Get cardinality estimate"""
        return (self.m ** 2) / sum(self.buckets)
    
    def memory_usage(self):
        """Get memory usage in bytes"""
        return sys.getsizeof(self.buckets)

def HyperReal(hashes, k):
    """Legacy function for backward compatibility"""
    estimator = HyperRealEstimator(k)
    for hash_val in hashes:
        estimator.update(hash_val)
    return estimator.estimate(), estimator.memory_usage()