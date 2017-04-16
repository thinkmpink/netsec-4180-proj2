Michael Pinkham
UNI: mlp2185
COMS W4180
Programming Project 2
README

Part 1

Install:
#TODO

Run: 
 - `$ ./ngram.py -n1 -s1  -out path/to/output.json -in path/to/progN`
 - These arguments can be in any order. Note that n is the n in ngram 
and s is the slide.
 - The running time of this command (for prog1, the largest executable)
is 0m0.070s on my Google Cloud environment. 
 - Note that for performance reasons I did not read the number of bytes
from the file as are in the ngram: the system call setup would make this
very slow. So I read data in ~8000 bytes at a time, and made sure to 
handle the ngrams that were split across consecutive file reads.

Output:
 - This program outputs all ngrams and their counts given the parameters 
in a JSON-format file. Specifically, the output file will contain a list
of two-element lists of the form [ngram, count]. 


