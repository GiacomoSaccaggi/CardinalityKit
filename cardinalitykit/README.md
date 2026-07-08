# CardinalityKit

A comprehensive Python package for cardinality estimation algorithms, providing implementations of various probabilistic counting techniques including HyperLogLog, HyperReal, and their extended versions.

## Features

- **Core Algorithms**: Flajolet-Martin, LogLog, SuperLogLog, HyperLogLog, HyperReal
- **Extended Algorithms**: Enhanced versions with demographic attribute tracking
- **Sample Conversion**: Convert sample data to HyperReal sketches
- **Utilities**: CSV parsing, hash generation, exact counting for validation

## Installation

```bash
pip install cardinalitykit
```

Or install from source:

```bash
git clone https://github.com/GiacomoSaccaggi/CardinalityKit.git
cd CardinalityKit
pip install -e .
```

## Quick Start

### Basic Usage

```python
from cardinalitykit import HyperLogLogEstimator
import hashlib

# Create estimator
hll = HyperLogLogEstimator(k=10)

# Process data
data = ["user_1", "user_2", "user_3", "user_1"]  # user_1 appears twice
for item in data:
    hash_val = '{:32b}'.format(int(hashlib.sha256(item.encode()).hexdigest()[:8], 16))
    hll.update(hash_val)

# Get estimate
estimate = hll.estimate()
print(f"Estimated cardinality: {estimate}")
```

### Extended Algorithms with Attributes

```python
from cardinalitykit import ExtendedHyperLogLogSketch

# Create extended sketch
ehll = ExtendedHyperLogLogSketch(b_m=8, b_s=8)

# Process events with attributes
events = [
    {'id_to_count': 'user_1', 'attribute': 'group_A'},
    {'id_to_count': 'user_2', 'attribute': 'group_B'},
    {'id_to_count': 'user_3', 'attribute': 'group_A'}
]

for event in events:
    ehll.update_sketch(event)

# Get results
total = ehll.get_cardinality_estimate()
by_attribute = ehll.get_frequency_for_attr()
print(f"Total: {total}, By attribute: {by_attribute}")
```

### Sample Data Conversion

```python
from cardinalitykit import ExtendedHyperRealSketchFromSample

# Sample data: (id, weight, attribute)
sample_data = [
    ("sample_1", 0.4, "demographic_A"),
    ("sample_2", 0.6, "demographic_B")
]

# Convert to HyperReal sketch
converter = ExtendedHyperRealSketchFromSample(b_m=8, sample_data=sample_data)
converter.naive_associate(sum_weights=10000)

estimate = converter.get_cardinality_estimate()
print(f"Converted estimate: {estimate}")
```

## Algorithm Comparison

| Algorithm | Memory | Accuracy | Use Case |
|-----------|--------|----------|----------|
| Flajolet-Martin | Low | Basic | Historical reference |
| LogLog | Medium | Good | General purpose |
| SuperLogLog | Medium | Better | Outlier elimination |
| HyperLogLog | Medium | Best | Industry standard |
| HyperReal | Medium | Unbiased | Research applications |

## Package Structure

```
cardinalitykit/
├── algorithms/          # Core estimation algorithms
├── extended/           # Extended algorithms with attributes
├── conversion/         # Sample to sketch conversion
├── utils/             # Utility functions
└── examples.py        # Usage examples
```

## Examples

Run the examples to see all algorithms in action:

```python
from cardinalitykit.examples import *

basic_example()          # Basic HyperLogLog usage
comparison_example()     # Compare all algorithms
extended_example()       # Extended algorithms with attributes
sample_conversion_example()  # Sample data conversion
```

## API Reference

### Core Algorithms

All core algorithms follow the same interface:

- `__init__(k)`: Initialize with k bits for buckets
- `update(hash_value)`: Process a hash value
- `estimate()`: Get cardinality estimate
- `memory_usage()`: Get memory usage in bytes

### Extended Algorithms

Extended algorithms add attribute tracking:

- `update_sketch(event)`: Process event with id and attribute
- `get_cardinality_estimate()`: Get total cardinality
- `get_frequency_for_attr(attr)`: Get frequency for specific attribute

### Conversion Algorithms

Sample conversion algorithms:

- `naive_associate(sum_weights)`: Simple conversion method
- `fast_associate(sum_weights, D)`: Optimized conversion method

## Contributing

This package is organized from research implementations. Each algorithm maintains compatibility with the original simulation code while providing a clean, object-oriented interface.