
import time
import csv_parser
import sys
# this function is O(n^2). this would take a *very* long time to run on our dataset
# we will not use this, except for subsets
def count_all_unique_plates(filename, total_entries):
    unique = []

    for plate in csv_parser.get_plates(filename):
        if plate not in unique:
            unique.append(plate)

    return len(unique), sys.getsizeof(unique)

# determines the exact amount of unique elements using set() to remove duplicates
# this is **much** faster than count_all_unique_plates()
def get_exact_unique_using_set(filename):
    #to sort we must load all entries into an array
    entries = []
    for plate in csv_parser.get_plates(filename):
        entries.append(plate)

    #use set() to remove duplicates
    entries = set(entries)

    #return the number of elements that aren't duplicates
    return len(entries), sys.getsizeof(entries)