#!/usr/bin/env python3

import argparse
import itertools as it

def stream_ngram(file_, chunksize=8192):
  with open(file_, "rb") as f:
    trigram = None
    while True:
      chunk = f.read(chunksize)
      if chunk:
        if trigram != None:
          # Account for ngrams split across the chunksize
          split_tri = trigram[1:] + bytes(chunk[0:1])
          yield (split_tri[:1], split_tri[:2], split_tri)
          split_tri = trigram[2:3] + bytes(chunk[:1])
          yield (split_tri[:1], split_tri[:2], split_tri)
        for i in range(chunksize-2):
          trigram = chunk[i:i+3]
          bigram  = trigram[:2]
          unigram = trigram[:1]
          yield (unigram, bigram, trigram)
        
      else:
        #the remaining bigram/uni and uni
        yield (chunk[-2:-1], chunk[-2:], None) 
        yield (chunk[-1:], None, None)
        break

if __name__ == '__main__':
  for tri in stream_ngram('starter.py', 5):
    print(tri)
