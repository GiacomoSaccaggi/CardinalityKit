# Algorithms

Core cardinality estimation algorithms implementing probabilistic counting techniques.

## Files

### flajolet_martin.py
**FlajoletMartinEstimator** - Original probabilistic counting algorithm (1985)
- `__init__()` - Initialize with 32-bit bitmap
- `update(hash_value)` - Process hash value and update bitmap
- `estimate()` - Return cardinality estimate with bias correction
- `memory_usage()` - Return memory consumption in bytes

### loglog.py
**LogLogEstimator** - Improved algorithm using bucket averaging
- `__init__(k)` - Initialize with k bits for 2^k buckets
- `update(hash_value)` - Update bucket with leading zero count
- `estimate()` - Return cardinality using arithmetic mean
- `memory_usage()` - Return memory consumption in bytes

### superloglog.py
**SuperLogLogEstimator** - Enhanced accuracy with outlier elimination
- `__init__(k)` - Initialize with k bits for 2^k buckets
- `update(hash_value)` - Update bucket with leading zero count
- `estimate()` - Return cardinality using 70% trimmed mean
- `memory_usage()` - Return memory consumption in bytes

### hyperloglog.py
**HyperLogLogEstimator** - Industry-standard algorithm (used by Redis, PostgreSQL)
- `__init__(k)` - Initialize with k bits for 2^k buckets
- `update(hash_value)` - Update bucket with leading zero count
- `estimate()` - Return cardinality using harmonic mean with bias correction
- `memory_usage()` - Return memory consumption in bytes

### hyperreal.py
**HyperRealEstimator** - Unbiased estimation for research applications
- `__init__(k)` - Initialize with k bits for 2^k buckets
- `update(hash_value)` - Update bucket with normalized hash value [0,1]
- `estimate()` - Return unbiased cardinality estimate
- `memory_usage()` - Return memory consumption in bytes

## Usage

```python
from cardinalitykit.algorithms import HyperLogLogEstimator
import hashlib

# Create estimator
hll = HyperLogLogEstimator(k=10)

# Process data
for item in data:
    hash_val = '{:32b}'.format(int(hashlib.sha256(item.encode()).hexdigest()[:8], 16))
    hll.update(hash_val)

# Get estimate
estimate = hll.estimate()
memory = hll.memory_usage()
```

## Algorithm Comparison

| Algorithm | Accuracy | Memory | Bias |
|-----------|----------|--------|------|
| Flajolet-Martin | Basic | 32 bits | High |
| LogLog | Good | 2^k bytes | Medium |
| SuperLogLog | Better | 2^k bytes | Low |
| HyperLogLog | Best | 2^k bytes | Minimal |
| HyperReal | Excellent | 2^k bytes | Unbiased |
