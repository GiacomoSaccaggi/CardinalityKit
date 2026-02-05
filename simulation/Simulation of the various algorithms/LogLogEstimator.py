import sys
#returns an estimate of the cardinality of given hashes using k bits for the buckets
def LogLog(hashes, k):
  #number of buckets
  m = 2 ** k
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
  
  #get bucket average
  average = sum(buckets) / m
  #calculate estimate
  estimate = m * (2 ** average)

  #bias converges to 0.397011808 for larger numbers of buckets (k > 5)
  #since we want to be using more buckets anyways, and the percise value of the bias is costly to calculate. We will use this convergance as an estimate of the bias
  BIAS = 0.397011808
  #correct for bias
  estimate = BIAS * estimate

  return estimate, sys.getsizeof(buckets)