import math, sys, random, hashlib
#returns an estimate of the cardinality of given hashes using k bits for the buckets
def HyperReal(hashes, k):
  #number of buckets
  m = 2 ** k
  #initialize buckets to 0
  buckets = [1.0] * m

  #loop through all hashes
  for i in range(0, len(hashes)):
    int_val = int(hashlib.sha256(str(hashes[i]).encode()).hexdigest()[:8], 16)
    # Normalizes the integer in the range [0, 1]
    x = int_val / (16 ** 8 - 1)
    #get bucket{j} of the hash (first k bits)
    j = str(hashes[i])[:k]
    j = int(j, 2)
    buckets[j] = min(buckets[j], x)

  # get the harmonic mean of the buckets
  #calculate estimate
  estimate = (m ** 2) / sum(buckets)

    
  return estimate, sys.getsizeof(buckets)
  
