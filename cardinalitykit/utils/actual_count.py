import sys
from .csv_parser import CSVParser

def count_all_unique_values(filename, column_index):
    """
    Count unique values using O(n^2) approach - slow but accurate
    
    Args:
        filename (str): Path to CSV file
        column_index (int): Index of column to count
        
    Returns:
        tuple: (unique_count, memory_usage)
    """
    parser = CSVParser()
    unique = []

    for value in parser.get_column_values(filename, column_index):
        if value not in unique:
            unique.append(value)

    return len(unique), sys.getsizeof(unique)

def get_exact_unique_using_set(filename, column_index=1):
    """
    Get exact count of unique values using set() - fast and memory efficient
    
    Args:
        filename (str): Path to CSV file
        column_index (int): Index of column to count (default: 1 for plates)
        
    Returns:
        tuple: (unique_count, memory_usage)
    """
    parser = CSVParser()
    entries = []
    
    for value in parser.get_column_values(filename, column_index):
        entries.append(value)

    # Use set() to remove duplicates
    unique_entries = set(entries)

    return len(unique_entries), sys.getsizeof(unique_entries)

def get_unique_count_from_list(data_list):
    """
    Get unique count from a list of values
    
    Args:
        data_list (list): List of values to count
        
    Returns:
        tuple: (unique_count, memory_usage)
    """
    unique_entries = set(data_list)
    return len(unique_entries), sys.getsizeof(unique_entries)