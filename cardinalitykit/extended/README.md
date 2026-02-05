# Extended Algorithms

Extended cardinality estimation algorithms with demographic attribute tracking.

## Files

### extended_hyperloglog.py
**ExtendedHyperLogLogSketch** - HyperLogLog with attribute frequency tracking
- `__init__(b_m, b_s)` - Initialize main sketch (b_m bits) and sub-sketches (b_s bits)
- `update_sketch(event)` - Process event with id and attribute
- `get_cardinality_estimate()` - Return overall cardinality estimate
- `get_frequency_for_attr(attr)` - Return frequency for specific attribute or all attributes
- `get_sketch()` - Return internal sketch data structures

### extended_hyperreal.py
**ExtendedHyperRealSketch** - HyperReal with attribute frequency tracking
- `__init__(b_m, b_s)` - Initialize main sketch (b_m bits) and sub-sketches (b_s bits)
- `update_sketch(event)` - Process event with id and attribute
- `get_cardinality_estimate()` - Return overall cardinality estimate
- `get_frequency_for_attr(attr)` - Return frequency for specific attribute or all attributes
- `get_sketch()` - Return internal sketch data structures

## Usage

```python
from cardinalitykit.extended import ExtendedHyperLogLogSketch

# Create extended sketch
ehll = ExtendedHyperLogLogSketch(b_m=8, b_s=8)

# Process events with attributes
events = [
    {'id_to_count': 'user_1', 'attribute': 'age_18_24'},
    {'id_to_count': 'user_2', 'attribute': 'age_25_34'},
    {'id_to_count': 'user_3', 'attribute': 'age_18_24'}
]

for event in events:
    ehll.update_sketch(event)

# Get results
total = ehll.get_cardinality_estimate()
by_age = ehll.get_frequency_for_attr()
specific = ehll.get_frequency_for_attr('age_18_24')
```

## Features

- **Attribute Tracking**: Maintain per-attribute frequency estimates
- **Privacy-Preserving**: No individual identifiers stored
- **Audience Segmentation**: Estimate unique counts by demographic groups
- **Sketch Merging**: Combine sketches from different sources
