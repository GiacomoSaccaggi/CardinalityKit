import csv
import hashlib

class CSVParser:
    """Utility class for parsing CSV files and creating hashes"""
    
    def __init__(self, row_limit=-1):
        """
        Initialize CSV parser
        
        Args:
            row_limit (int): Limit number of rows to parse (-1 for no limit)
        """
        self.row_limit = row_limit
    
    def count_lines(self, filename):
        """Count total number of rows in CSV file"""
        with open(filename, "r") as csvfile:
            return sum(1 for row in csvfile) - 1
    
    def get_column_values(self, filename, column_index):
        """
        Generator that yields values from specified column
        
        Args:
            filename (str): Path to CSV file
            column_index (int): Index of column to extract
        """
        with open(filename, "r") as csvfile:
            datareader = csv.reader(csvfile)
            count = -1
            for row in datareader:
                if count == -1:
                    # Skip header row
                    count += 1
                elif self.row_limit == -1 or count < self.row_limit:
                    yield row[column_index]
                    count += 1
                else:
                    return
    
    def create_hashes_from_column(self, filename, column_index, output_file=None):
        """
        Create SHA256 hashes from specified column
        
        Args:
            filename (str): Path to CSV file
            column_index (int): Index of column to hash
            output_file (str): Optional file to save hashes
            
        Returns:
            list: List of hash strings
        """
        hashes = []
        
        if output_file:
            with open(output_file, 'w') as file:
                for value in self.get_column_values(filename, column_index):
                    hash_obj = hashlib.sha256(str(value).encode('utf-8'))
                    hash_str = hash_obj.hexdigest()
                    hashes.append(hash_str)
                    file.write(hash_str + "\n")
        else:
            for value in self.get_column_values(filename, column_index):
                hash_obj = hashlib.sha256(str(value).encode('utf-8'))
                hashes.append(hash_obj.hexdigest())
        
        return hashes

# Legacy functions for backward compatibility
def get_plates(filename):
    """Legacy function - get plate IDs from column 1"""
    parser = CSVParser()
    return parser.get_column_values(filename, 1)

def create_hashes(filename):
    """Legacy function - create hashes from plate IDs"""
    parser = CSVParser()
    return parser.create_hashes_from_column(filename, 1, 'hashes.csv')

def parse_csv(filename, columns=None):
    """
    Parse CSV file and return specified columns
    
    Args:
        filename (str): Path to CSV file
        columns (list): List of column indices to extract
        
    Returns:
        list: List of rows with specified columns
    """
    data = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header
        
        for row in reader:
            if columns:
                data.append([row[i] for i in columns])
            else:
                data.append(row)
    
    return data