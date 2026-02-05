"""
Example usage of CardinalityKit algorithms
"""

from cardinalitykit import *
import hashlib

def basic_example():
    """Basic example using HyperLogLog"""
    print("=== Basic HyperLogLog Example ===")
    
    # Create some sample data
    data = [f"user_{i}" for i in range(10000)]
    
    # Create HyperLogLog estimator
    hll = HyperLogLogEstimator(k=10)
    
    # Process data
    for item in data:
        # Create hash
        hash_val = '{:32b}'.format(int(hashlib.sha256(item.encode()).hexdigest()[:8], 16))
        hll.update(hash_val)
    
    # Get estimate
    estimate = hll.estimate()
    actual = len(set(data))
    
    print(f"Actual unique count: {actual}")
    print(f"HLL estimate: {estimate:.0f}")
    print(f"Error: {abs(estimate - actual) / actual * 100:.2f}%")
    print(f"Memory usage: {hll.memory_usage()} bytes")

def comparison_example():
    """Compare different algorithms"""
    print("\n=== Algorithm Comparison ===")
    
    # Create sample data
    data = [f"item_{i}" for i in range(5000)]
    
    # Initialize algorithms
    algorithms = {
        'Flajolet-Martin': FlajoletMartinEstimator(),
        'LogLog': LogLogEstimator(k=8),
        'SuperLogLog': SuperLogLogEstimator(k=8),
        'HyperLogLog': HyperLogLogEstimator(k=8),
        'HyperReal': HyperRealEstimator(k=8)
    }
    
    # Process data
    for name, alg in algorithms.items():
        for item in data:
            hash_val = '{:32b}'.format(int(hashlib.sha256(item.encode()).hexdigest()[:8], 16))
            alg.update(hash_val)
    
    # Compare results
    actual = len(set(data))
    print(f"Actual unique count: {actual}")
    print("-" * 50)
    
    for name, alg in algorithms.items():
        estimate = alg.estimate()
        error = abs(estimate - actual) / actual * 100
        memory = alg.memory_usage()
        print(f"{name:15}: {estimate:8.0f} ({error:5.2f}% error, {memory:4d} bytes)")

def extended_example():
    """Example using extended algorithms with attributes"""
    print("\n=== Extended Algorithm Example ===")
    
    # Create sample data with attributes
    events = []
    for i in range(1000):
        events.append({
            'id_to_count': f"user_{i}",
            'attribute': f"group_{i % 5}"  # 5 different groups
        })
    
    # Create extended HyperLogLog
    ehll = ExtendedHyperLogLogSketch(b_m=8, b_s=8)
    
    # Process events
    for event in events:
        ehll.update_sketch(event)
    
    # Get results
    total_estimate = ehll.get_cardinality_estimate()
    attr_estimates = ehll.get_frequency_for_attr()
    
    print(f"Total cardinality estimate: {total_estimate:.0f}")
    print("Attribute frequencies:")
    for attr, freq in attr_estimates.items():
        print(f"  {attr}: {freq:.0f}")

def sample_conversion_example():
    """Example of sample to HyperReal conversion"""
    print("\n=== Sample Conversion Example ===")
    
    # Create sample data (id, weight, attribute)
    sample_data = [
        ("sample_1", 0.3, "demographic_A"),
        ("sample_2", 0.4, "demographic_B"), 
        ("sample_3", 0.3, "demographic_A")
    ]
    
    # Create converter
    converter = ExtendedHyperRealSketchFromSample(b_m=8, sample_data=sample_data)
    
    # Run naive association
    converter.naive_associate(sum_weights=1000)
    
    # Get results
    estimate = converter.get_cardinality_estimate()
    attr_freq = converter.get_frequency_for_attr()
    
    print(f"Converted cardinality estimate: {estimate:.0f}")
    print("Attribute frequencies:")
    for attr, freq in attr_freq.items():
        print(f"  {attr}: {freq:.0f}")

if __name__ == "__main__":
    basic_example()
    comparison_example()
    extended_example()
    sample_conversion_example()