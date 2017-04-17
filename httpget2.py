import argparse
import random
import string
from scapy.all import *

def get_packet(srcIP, dstIP, srcPort, dstPort, payload):
  iplayer=IP(src=srcIP, dst=dstIP)
  transportlayer=TCP(sport=srcPort, dport=dstPort)
  data=payload
  packet=iplayer/transportlayer/Raw(load=data)
  return packet

def main():
  parser = argparse.ArgumentParser(
      description='Send TCP/IP packets to loopback address.')
  parser.add_argument('-s', '--srcport', type=int, help='The source port')
  parser.add_argument('-d', '--dstport', type=int, help='The destination port')
  args = parser.parse_args()

  # Part 1. 
  for dst in range(3000, 3021, 1):
    packet = get_packet('127.0.0.1', '127.0.0.1', args.srcport, dst, '') 
    #packet.show()
    send(packet)
  
  # Part 2.
  for i in range(5):
    rand_string = ''.join(random.choice(string.letters) for i in range(10))
    packet = get_packet('127.0.0.1', '127.0.0.1', args.srcport, 
        args.dstport, rand_string)
    #packet.show()
    send(packet)

  return


if __name__ == '__main__':
  main()
