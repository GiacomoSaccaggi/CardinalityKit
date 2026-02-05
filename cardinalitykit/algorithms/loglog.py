import sys

class LogLogEstimator:
    """
    LogLog cardinality estimator
    
    An improvement over Flajolet-Martin that uses multiple buckets
    to reduce variance in the estimate.
    """
    
    def __init__(self, k=10):
        """
        Initialize LogLog estimator
        
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
        average = sum(self.buckets) / self.m
        estimate = self.m * (2 ** average)
        BIAS = 0.397011808
        return BIAS * estimate
    
    def memory_usage(self):
        """Get memory usage in bytes"""
        return sys.getsizeof(self.buckets)

def LogLog(hashes, k):
    """Legacy function for backward compatibility"""
    estimator = LogLogEstimator(k)
    for hash_val in hashes:
        estimator.update(hash_val)
    return estimator.estimate(), estimator.memory_usage()