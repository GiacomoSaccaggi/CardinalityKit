
import math, sys

#returns an estimate of the cardinality of hashes using k bits for the buckets
def SuperLogLog(hashes, k):
  #number of buckets
  m = 2**k
  #initialize buckets to 0
  buckets = [0] * m

  #loop through all hashes
  for i in range(0, len(hashes)):
    #get bucket{j} of the hash (first k bits)
    j = str(hashes[i])[:k]
    j = int(j, 2)    

    #get remaining bits (remaining bits after bucket)
    data = hashes[i][k:]
    #get rank of the first 1 in the remaining bits (number of trailing zeros)
    rank = 1
    for c in reversed(data):
      if c == "0":
        rank += 1
      else:
        break

    #if rank is higher than the previous bucket value set it to the new rank
    buckets[j] = max(buckets[j], rank)
  
  #calculate lower and upper cutoffs
  #a cut off of ~0.7 is optimal
  cutoff = 0.7
  lower = math.floor(cutoff * m)
  upper = m - lower

  #apply cutoff
  buckets.sort()
  for i in range(upper):
    del buckets[-1]

  #get bucket average
  average = sum(buckets) / lower
  #calculate estimate
  estimate = m * 2 ** average

  #the theoretical calculation of the bias factor for SLL is unknown
  #however, rough empircal tuning gives us a coefficient of around 0.764
  BIAS = 0.764
  #correct for bias
  estimate = BIAS * estimate

  return estimate, sys.getsizeof(buckets)
