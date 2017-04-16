#!/usr/bin/env python3

import argparse
import collections
import json
import sys

#TODO: write documentation (use google format)
def stream_ngram(file_, n=3, slide=1, chunksize=8190):
  """
  Given a binary file to read, a value of n, and a slide value, 
  `stream_ngram` generates all the ngrams in the file, returning
  an iterator over them.

  Args:
      file_     (unicode): A file name to open
      n         (int):     The number of bytes to return each iteration
      slide     (int):     The number of bytes to slide forward in the 
                           file at each iteration. assert slide <= n
      chunksize (int):     A number of bytes to read from the file at a 
                           time. Since the program only supports 
                           unigrams, bigrams, and trigrams, the chunksize
                           should be divisible by 6. The program quits 
                           otherwise.
  
  Yields:
      (bytearray): the next n-byte bytearray
  
  Raises:
      Mildly descriptive bad value exceptions for unsupported parameter
      values, specifically an error will be thrown if n < 1, n > 3, slide < 1, 
      slide > n, chunksize % 6 != 0, or the program cannot find or open the 
      file.
  """
  if n < 1 or n > 3:
    raise Exception('Bad value.', 'Unsupported n for ngram')

  if slide < 1 or slide > n:
    raise Exception('Bad value.', 'Unsupported slide for ngram')

  if chunksize % 6:
    raise Exception('Bad value.', 'Unsupported chunksize for file read.')

  try:
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
    
  except Exception as inst:
    handle(inst)


def handle(exception_inst):
  """
  Print an error and exit.

  Args:
      exception_inst (Exception object): the Exception that was raised.

  Returns:
      (void) System exits with return value of 1 (error).
  """
  print(exception_inst.args)
  sys.exit(1)

def count_ngrams(nbytes, slide, file_):
  """
  Return a dictionary mapping bytearrays to counts.

  Args:
      nbytes (int): the size of the bytearray i.e. ngram
      slide  (int): the size of the slide value
      file_  (unicode): the name of the file to analyze

  Returns:
      (dict[bytearray]:int): a mapping of each ngram to the number of times
                             the ngram appeared in the file (given the slide)
                             Exits the program on failure.
  """
  counts = collections.defaultdict(lambda: 0)
  try:
    for gram in stream_ngram(file_, nbytes, slide):
      counts[gram] += 1
  except Exception as inst:
    handle(inst)
  return counts

def output_sorted_counts(count_dict, file_):
  """
  Writes the count dictionary to a json file.

  Args:
      count_dict (dict[bytearray]:int): see `count_ngrams`
      file_      (unicode)            : the name of the file to write to
  
  Returns:
      (void)
  """
  counts = [(k.hex(), count_dict[k]) for k in sorted(count_dict,
    key=count_dict.get, reverse=True)]
  with open(file_, 'w') as f:
    json.dump(counts, f)
  return

def main():
  """
  See the README. Run `$ ./ngram.py -h` to see options.
  """
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
