# Simulations

Research simulations and experiments demonstrating algorithm behavior and accuracy.

## Directories

### Simulation of the various algorithms/
Comparative analysis of all five core cardinality estimation algorithms.

**Files:**
- `main.py` - Main simulation script comparing FM, LogLog, SuperLogLog, HLL
- `FlajoletMartinEstimator.py` - Standalone FM implementation
- `LogLogEstimator.py` - Standalone LogLog implementation
- `SuperLogLogEstimator.py` - Standalone SuperLogLog implementation
- `HyperLogLogEstimator.py` - Standalone HLL implementation
- `ActualCount.py` - Exact counting for validation
- `csv_parser.py` - CSV parsing utilities

**Usage:**
```bash
cd "Simulation of the various algorithms"
python main.py
```

**Output:** CSV files with accuracy metrics across different k values

### HLL vs HR/
Detailed comparison between HyperLogLog and HyperReal algorithms.

**Files:**
- `main_HLL_vs_HR.py` - Main comparison script
- `HyperLogLogEstimator.py` - HLL implementation
- `HyperReal.py` - HyperReal implementation
- `ActualCount.py` - Exact counting
- `csv_parser.py` - CSV parsing

**Usage:**
```bash
cd "HLL vs HR"
python main_HLL_vs_HR.py
```

**Output:** Comparative analysis of HLL vs HR accuracy and bias

### From Sample to Hr/
Sample data conversion experiments using HyperReal sketches.

**Files:**
- `From_Sample_to_HR_Naive_Association.py` - Naive conversion method
- `From_Sample_to_HR_Fast_Association.py` - Optimized conversion method
- `characters.csv` - Sample dataset

**Usage:**
```bash
cd "From Sample to Hr"
python From_Sample_to_HR_Fast_Association.py
```

**Output:** Population estimates from sample data with error metrics

### Extented Algorithms/
Experiments with extended HLL and HR algorithms for attribute tracking.

**Subdirectories:**
- `Extended HLL/` - Extended HyperLogLog experiments
- `Extended HR/` - Extended HyperReal experiments

## Data

### Parking_Violations_Issued_-_Fiscal_Year_2019.csv
Large real-world dataset used for algorithm validation and benchmarking.

## Running Simulations

All simulations follow a similar pattern:
1. Load or generate test data
2. Run algorithm multiple times with different hash offsets
3. Calculate mean, standard deviation, and error metrics
4. Export results to CSV

## Output Metrics

- **Estimate**: Mean cardinality estimate
- **Std**: Standard deviation across runs
- **MPE**: Mean Percentage Error
- **MAPE**: Mean Absolute Percentage Error
- **RAM**: Memory usage in bytes
