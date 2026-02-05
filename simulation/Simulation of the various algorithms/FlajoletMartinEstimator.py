import sys

#returns an estimate of the cardinality of given hashes using k bits for the buckets
def FlajoletMartin(hashes):
  #initialize a 32 bit long bitmap
  bitMap = ["0"] * 32

  #loop through all hashes
  for i in range(0, len(hashes)):
  #get rank of the first 1 in the hash (number of trailing zeros)
    rank = 0
    for c in reversed(str(hashes[i])):
      if c == "0":
        rank += 1
      else:
        break

    #set the corresponding index of the bitmap to 1
    bitMap[rank] = "1"
  
  #get the lowest index of 0
  r = 0
  for i in bitMap:
    if i == "1":
      r += 1
    else:
      break
  #calculate estimate
  estimate = 2 ** r

  #there is a predictible bias in the average case which is corrected by this bias factor
  BIAS = 0.77351
  #correct for bias
  estimate = estimate / BIAS

  return estimate, sys.getsizeof(bitMap)