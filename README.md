# CardinalityKit

A comprehensive Python toolkit for cardinality estimation algorithms, enabling privacy-preserving analytics through probabilistic counting techniques.

## What is CardinalityKit?

CardinalityKit provides implementations of state-of-the-art algorithms for estimating the number of unique elements in large datasets without storing individual values. This is crucial for:

- **Privacy-Preserving Analytics**: Count unique users without exposing individual identifiers
- **Memory Efficiency**: Use minimal memory regardless of dataset size
- **Cross-Platform Deduplication**: Estimate unique reach across multiple platforms
- **Sample-Based Extrapolation**: Convert panel data to population-level estimates

## Features

### Core Algorithms
- **Flajolet-Martin**: Historical probabilistic counting algorithm
- **LogLog**: Improved memory efficiency with bucket averaging
- **SuperLogLog**: Enhanced accuracy with outlier elimination
- **HyperLogLog (HLL)**: Industry-standard algorithm (used by Redis, PostgreSQL)
- **HyperReal (HR)**: Unbiased estimation for research applications

### Extended Algorithms
- **Extended HyperLogLog**: HLL with demographic attribute tracking
- **Extended HyperReal**: HR with demographic attribute tracking
- Support for audience segmentation while maintaining privacy

### Sample Conversion
- **Naive Association**: Simple sample-to-population conversion
- **Fast Association**: Optimized conversion with configurable precision
- Convert survey/panel data to full population estimates

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/GiacomoSaccaggi/CardinalityKit.git
cd CardinalityKit

# Install the package
pip install -e .
```

### Requirements

- Python 3.7+
- numpy >= 1.19.0
- pandas >= 1.1.0
- tqdm >= 4.50.0
- scipy >= 1.5.0

## Quick Start

### Basic Usage: Estimate Unique Count

```python
from cardinalitykit import HyperLogLogEstimator
import hashlib

# Create estimator with k=10 (1024 buckets)
hll = HyperLogLogEstimator(k=10)

# Process your data
data = ["user_1", "user_2", "user_3", "user_1"]  # user_1 appears twice

for item in data:
    # Hash the item to binary
    hash_val = '{:32b}'.format(int(hashlib.sha256(item.encode()).hexdigest()[:8], 16))
    hll.update(hash_val)

# Get estimate
estimate = hll.estimate()
print(f"Estimated unique count: {estimate:.0f}")  # Output: ~3
print(f"Memory used: {hll.memory_usage()} bytes")  # Output: 1024 bytes
```

### Track Demographics with Extended Algorithms

```python
from cardinalitykit import ExtendedHyperLogLogSketch

# Create extended sketch
ehll = ExtendedHyperLogLogSketch(b_m=8, b_s=8)

# Process events with attributes
events = [
    {'id_to_count': 'user_1', 'attribute': 'age_18_24'},
    {'id_to_count': 'user_2', 'attribute': 'age_25_34'},
    {'id_to_count': 'user_3', 'attribute': 'age_18_24'},
]

for event in events:
    ehll.update_sketch(event)

# Get total and per-attribute estimates
total = ehll.get_cardinality_estimate()
by_age = ehll.get_frequency_for_attr()

print(f"Total unique users: {total:.0f}")
print(f"By age group: {by_age}")
```

### Convert Sample Data to Population Estimates

```python
from cardinalitykit import ExtendedHyperRealSketchFromSample

# Sample data: (id, weight, attribute)
sample_data = [
    ("panelist_1", 0.4, "demographic_A"),
    ("panelist_2", 0.6, "demographic_B")
]

# Create converter
converter = ExtendedHyperRealSketchFromSample(b_m=8, sample_data=sample_data)

# Run association (choose naive or fast)
converter.naive_associate(sum_weights=10000)
# OR for better performance:
# converter.fast_associate(sum_weights=10000, D=100)

# Get population estimates
estimate = converter.get_cardinality_estimate()
attr_freq = converter.get_frequency_for_attr()

print(f"Estimated population: {estimate:.0f}")
print(f"By demographic: {attr_freq}")
```

## Algorithm Comparison

| Algorithm | Memory | Accuracy | Error Rate | Use Case |
|-----------|--------|----------|------------|----------|
| Flajolet-Martin | Low | Basic | ~30% | Historical reference |
| LogLog | Medium | Good | ~5% | General purpose |
| SuperLogLog | Medium | Better | ~3% | Outlier elimination |
| HyperLogLog | Medium | Best | ~1.04/√m | Industry standard |
| HyperReal | Medium | Excellent | Unbiased | Research/high precision |

*Error rates are approximate and depend on the number of buckets (m = 2^k)*

## Configuration

### Precision Parameter (k)

The `k` parameter controls the number of buckets (m = 2^k) and affects accuracy vs memory:

```python
# Low memory, lower accuracy (~3.2% error)
hll = HyperLogLogEstimator(k=10)  # 1 KB

# Balanced (recommended)
hll = HyperLogLogEstimator(k=14)  # 16 KB, ~0.8% error

# High accuracy (~0.4% error)
hll = HyperLogLogEstimator(k=16)  # 64 KB
```

Standard error formula: `1.04 / sqrt(2^k)`

## Examples

Run the included examples:

```bash
python -m cardinalitykit.examples
```

Or run specific examples:

```python
from cardinalitykit.examples import *

basic_example()              # Basic HyperLogLog usage
comparison_example()         # Compare all algorithms
extended_example()           # Extended algorithms with attributes
sample_conversion_example()  # Sample data conversion
```

## Use Cases

### 1. Privacy-Preserving Analytics
Estimate unique visitors without storing user IDs:
```python
# Process millions of user IDs
for user_id in user_stream:
    hash_val = hash_function(user_id)
    hll.update(hash_val)

# Get estimate without exposing individual users
unique_visitors = hll.estimate()
```

### 2. Cross-Platform Deduplication
Combine sketches from different platforms:
```python
# Each platform creates its own sketch
mobile_hll = HyperLogLogEstimator(k=14)
web_hll = HyperLogLogEstimator(k=14)

# Merge sketches (implementation in extended algorithms)
# Get deduplicated total reach
```

### 3. Real-Time Monitoring
Stream processing with constant memory:
```python
# Memory usage stays constant regardless of stream size
for event in infinite_stream:
    hll.update(hash_function(event.user_id))
    if event.timestamp % 1000 == 0:
        print(f"Current unique users: {hll.estimate():.0f}")
```

## Documentation

Full documentation available in the `documentation/` folder:
- [Fundamentals](documentation/fundamentals.html) - Core concepts
- [HyperLogLog](documentation/hyperloglog.html) - HLL algorithm details
- [HyperReal](documentation/hyperreal.html) - HR algorithm details
- [Extended Algorithms](documentation/extended-algorithms.html) - Attribute tracking
- [Panel Conversion](documentation/panel-conversion.html) - Sample conversion guide

## Development

### Running Simulations

```bash
# Compare all algorithms
cd simulation/Simulation\ of\ the\ various\ algorithms/
python main.py

# HyperLogLog vs HyperReal comparison
cd simulation/HLL\ vs\ HR/
python main_HLL_vs_HR.py

# Sample conversion experiments
cd simulation/From\ Sample\ to\ Hr/
python From_Sample_to_HR_Fast_Association.py
```

### Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=cardinalitykit --cov-report=html
```

## Performance

- **Update**: O(1) - constant time per element
- **Estimate**: O(m) - linear in number of buckets
- **Memory**: O(m) - fixed regardless of input size
- **Streaming**: Supports unlimited input size

## License

MIT License - See LICENSE file for details

## References

- Flajolet, P., & Martin, G. N. (1985). "Probabilistic counting algorithms for data base applications"
- Durand, M., & Flajolet, P. (2003). "Loglog counting of large cardinalities"
- Flajolet, P., et al. (2007). "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm"

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

CardinalityKit - A toolkit for privacy-preserving cardinality estimation

## Support

For questions and issues, please open an issue on GitHub.
