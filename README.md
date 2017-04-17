Michael Pinkham
UNI: mlp2185
COMS W4180
Programming Project 2
README

Project info:
 - The file `written.txt` contains all answers and required program output.

Install:
 - `$ sudo apt-get install [pkg-name]`: make, gcc, python3-pip, git,
python-pip, python-scapy
 - `$ pip3 install [module-name]`: argparse
 - `$ pip install [module-name]`: argparse

Part 1.

Run: 
 - `$ chmod 755 ngram.py`
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

Part 2.

Run:
 - The answers for part 2a. can be reproduced by copying the commands in
the relevant sections of `written.txt`.
 - Part 2b. can be run this way: `$ sudo python httpget1.py`. You may first
want to modify the source and destination IP addresses in `inpartb.txt`.
 - Part 2c. can be run via: `$ sudo python httpget2.py -s <src_port> -d
 <dst_port>`. For help/info run `$ python httpget2.py -h`. 

Output:
 - The output is as specified in the instructions.
