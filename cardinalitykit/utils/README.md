# Utils

Utility functions for data processing and validation.

## Files

### actual_count.py
**ActualCount** - Exact distinct counting for validation and benchmarking
- `get_exact_unique_using_set(filename)` - Calculate exact unique count from CSV file
- Returns tuple: (exact_count, memory_used)

### csv_parser.py
**CSV Parser** - Efficient CSV data parsing with hash generation
- `create_hashes(filename)` - Parse CSV and generate SHA-256 hashes for each row
- Returns list of hash strings

## Usage

### Exact Counting
```python
from cardinalitykit.utils import ActualCount

# Get exact unique count for validation
exact_count, memory = ActualCount.get_exact_unique_using_set('data.csv')
print(f"Exact unique: {exact_count}, Memory: {memory} bytes")
```

### CSV Parsing
```python
from cardinalitykit.utils import csv_parser

# Parse CSV and generate hashes
hashes = csv_parser.create_hashes('data.csv')
print(f"Generated {len(hashes)} hashes")
```

## Purpose

- **Validation**: Compare probabilistic estimates against exact counts
- **Benchmarking**: Measure accuracy and memory efficiency
- **Data Processing**: Efficient CSV parsing for large datasets
