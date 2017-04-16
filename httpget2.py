import argparse
from scapy.all import *

def get_packet(srcIP, dstIP, srcPort, dstPort, payload):
  iplayer=IP(src=srcIP, dst=dstIP)
  transportlayer=TCP(sport=srcPort, dport=dstPort)
  data=payload
  packet=iplayer/transportlayer/Raw(load=data)
  return packet

def main():
  with open('inpartb.txt', 'r') as f:
    srcIP = f.readline().split(':')[1].strip()
    dstIP = f.readline().split(':')[1].strip()
    srcPort = int(f.readline().split(':')[1].strip())
    dstPort = int(f.readline().split(':')[1].strip())
    payload = f.read()
    packet = get_packet(srcIP, dstIP, srcPort, dstPort, payload)
    packet.show()
    print str(packet)
    send(packet)



if __name__ == '__main__':
  main()
