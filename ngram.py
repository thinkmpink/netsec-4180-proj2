#!/usr/bin/env python3

import argparse
import collections
import sys

#TODO: write documentation (use google format)
#TODO: reorder parameters
def stream_ngram(file_, n=3, slide=1, chunksize=8190):
  if n < 1 or n > 3:
    #TODO:Throw invalid n
    raise Exception('Bad value.', 'Unsupported n for ngram')

  if slide < 1 or slide > n:
    #TODO:Throw invalid slide
    raise Exception('Bad value.', 'Unsupported slide for ngram')

  #TODO: check default exception on file open fail
  with open(file_, "rb") as f:
    remaining_bytes = None
    #trigram = None
    while True:
      chunk = f.read(chunksize)
      if chunk:
        #if trigram != None:
        if remaining_bytes:
          # Account for ngrams split across the chunksize
          if n == 2:
            assert(len(remaining_bytes)==1)
            split_bi = remaining_bytes + bytes(chunk[0:1])
            if len(split_bi) == n:
              yield split_bi
          elif n == 3:
            assert(len(remaining_bytes)==2)
            split_tri = remaining_bytes + bytes(chunk[0:1])
            if len(split_tri) == n:
              yield split_tri
            if len(chunk) > 1 and slide == 1:
              split_tri = remaining_bytes[-1:] + bytes(chunk[0:2])
              if len(split_tri) == n:
                yield split_tri
          
        for i in range(0, chunksize-n+1, slide):
          gram = chunk[i:i+n]
          if len(gram) == n:
            yield gram
        remaining_bytes = chunk[i+slide:]
        
      else:
        break

def handle(exception_inst):
    print(exception_inst.args)
    sys.exit(1)

def count_ngrams(nbytes, slide, file_):
  chunksize = 6
  counts = collections.defaultdict(lambda: 0)
  #try:
  for gram in stream_ngram(file_, nbytes, slide, chunksize):
    counts[gram] += 1
  #except Exception as inst:
  #  handle(inst)
  return counts

def output_sorted_counts(count_dict, file_):
  #TODO:output to file
  toptwenty = [(k, count_dict[k]) for k in sorted(count_dict,
    key=count_dict.get, reverse=True)][:20]
  print(toptwenty)
  return

def main():
  parser = argparse.ArgumentParser(description="Static binary analysis by"
    "processing ngrams in the input where 1 <= n <= 3.")
  parser.add_argument('-n', '--nbytes', type=int, 
    help='The number of bytes in the ngram')
  parser.add_argument('-s', '--slidelen', type=int,
    help='The number of bytes between each ngram read from the file. s <= n.')
  parser.add_argument('-in', '--infile', help='The name of the file to analyze')
  parser.add_argument('-out', '--outfile', 
    help='The name of the file to write program results to.')
  args = parser.parse_args()

  counts = count_ngrams(args.nbytes, args.slidelen, args.infile)
  output_sorted_counts(counts, args.outfile)


if __name__ == '__main__':
  main()
