# Conversion

Sample data to HyperReal sketch conversion algorithms.

## Files

### sample_to_hyperreal.py
**ExtendedHyperRealSketchFromSample** - Convert sample/panel data to HyperReal sketches

#### Methods
- `__init__(b_m, sample_data)` - Initialize with bucket bits and sample data (id, weight, attribute)
- `naive_associate(sum_weights)` - Simple conversion method for sample to population
- `fast_associate(sum_weights, D)` - Optimized conversion with precision parameter D
- `get_cardinality_estimate()` - Return overall population cardinality estimate
- `get_frequency_for_attr(attr)` - Return frequency for specific attribute or all attributes
- `get_sketch()` - Return internal sketch data structures

#### Private Methods
- `_hash_function(data)` - Double hash for increased entropy
- `_bit_accuracy(u1, u2)` - Calculate bit accuracy between two integers

## Usage

```python
from cardinalitykit.conversion import ExtendedHyperRealSketchFromSample

# Sample data: (id, weight, attribute)
sample_data = [
    ("panelist_1", 0.4, "demographic_A"),
    ("panelist_2", 0.6, "demographic_B")
]

# Create converter
converter = ExtendedHyperRealSketchFromSample(b_m=8, sample_data=sample_data)

# Run association
converter.naive_associate(sum_weights=10000)
# OR for better performance:
# converter.fast_associate(sum_weights=10000, D=100)

# Get population estimates
estimate = converter.get_cardinality_estimate()
attr_freq = converter.get_frequency_for_attr()
```

## Use Cases

- **Panel Extrapolation**: Convert survey panel data to population estimates
- **Sample-Based Analytics**: Extrapolate full population from representative samples
- **Hybrid Measurement**: Combine sample data with online measurement systems

## Parameters

- **sum_weights**: Total population size to extrapolate to
- **D**: Depth parameter for fast association (higher = more accurate but slower)
