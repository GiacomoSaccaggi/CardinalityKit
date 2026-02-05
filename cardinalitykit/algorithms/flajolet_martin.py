import sys

class FlajoletMartinEstimator:
    """
    Flajolet-Martin cardinality estimator (1985)
    
    The original probabilistic counting algorithm that uses a bitmap
    to estimate the number of distinct elements in a data stream.
    """
    
    def __init__(self):
        self.bitmap = ["0"] * 32
    
    def update(self, hash_value):
        """Update the estimator with a hash value"""
        rank = 0
        for c in reversed(str(hash_value)):
            if c == "0":
                rank += 1
            else:
                break
        self.bitmap[rank] = "1"
    
    def estimate(self):
        """Get cardinality estimate"""
        r = 0
        for i in self.bitmap:
            if i == "1":
                r += 1
            else:
                break
        
        estimate = 2 ** r
        BIAS = 0.77351
        return estimate / BIAS
    
    def memory_usage(self):
        """Get memory usage in bytes"""
        return sys.getsizeof(self.bitmap)

def FlajoletMartin(hashes):
    """Legacy function for backward compatibility"""
    estimator = FlajoletMartinEstimator()
    for hash_val in hashes:
        estimator.update(hash_val)
    return estimator.estimate(), estimator.memory_usage()