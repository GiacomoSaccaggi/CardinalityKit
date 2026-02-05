import math, sys
#returns an estimate of the cardinality of given hashes using k bits for the buckets
def HyperLogLog(hashes, k):
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

  # get the harmonic mean of the buckets
  total = 0
  for bucket in buckets:
    total += 2 ** (-1 * bucket)
  mean = total ** -1
  #calculate estimate
  estimate = (m ** 2) * mean

  #bias can be approximated with the formula 0.7213 / (1 + (1.079/2^k)) for k >= 6
  #or for values of k < 6 we can use pre-calculated bias factors
  if k <= 4:
    BIAS = 0.673
  elif k == 5:
    BIAS = 0.697
  else:
    BIAS = 0.7213 / (1 + (1.079 / m))

  #correct for bias
  estimate = BIAS * estimate

  #small range correction
  if estimate < ((5 / 2) * m):
    #get count of registers with rank of 0
    zeros = 0
    for i in buckets:
      if buckets[i] == 0:
        zeros += 1
    #apply small range correction
    if not zeros == 0:
      estimate = m * math.log(estimate, 2)

  #large range correction
  elif estimate > ((2 ** 32) / 30):
    estimate = -1 * (2 ** 32) * math.log(1 - (estimate / (2 ** 32)))
    
  return estimate, sys.getsizeof(buckets)
  
