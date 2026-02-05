# Documentation

HTML documentation pages for CardinalityKit algorithms and concepts.

## Files

### fundamentals.html
Core concepts and mathematical foundations of cardinality estimation algorithms.

### hyperloglog.html
Detailed documentation of the HyperLogLog algorithm, including:
- Algorithm description
- Mathematical formulas
- Implementation details
- Accuracy analysis

### hyperreal.html
Detailed documentation of the HyperReal algorithm, including:
- Unbiased estimation approach
- Comparison with HyperLogLog
- Use cases for research applications

### extended-algorithms.html
Documentation for extended algorithms with attribute tracking:
- Extended HyperLogLog
- Extended HyperReal
- Audience segmentation capabilities

### panel-conversion.html
Guide for converting sample/panel data to population estimates:
- Naive association method
- Fast association method
- Parameter tuning

### algorithm-evolution.html
Historical evolution of cardinality estimation algorithms from Flajolet-Martin to HyperReal.

### applications.html
Real-world applications and use cases for cardinality estimation.

### implementation.html
Implementation details and best practices.

### package.html
Package structure and API reference.

### simulations.html
Documentation of simulation experiments and results.

### sketch-operations.html
Operations on sketches including merging and serialization.

## Viewing Documentation

Open any HTML file in a web browser:
```bash
open documentation/fundamentals.html
```

Or start a local server:
```bash
cd documentation
python -m http.server 8000
# Visit http://localhost:8000
```

## Style

All documentation uses:
- Bootstrap 3.3.7 framework
- Google Fonts (Open Sans, Lora)
- Font Awesome 4.7.0 icons
- Custom gradient styling
