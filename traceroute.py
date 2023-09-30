
from scapy.all import *
import threading
import argparse
import json
import os

public_prefix = '138.238.'
internal_prefix = '10.'

class Topology(object):
  def __init__(self, is_resume, reset_flag, is_public):
    self.ips = set()
    self.links = set()
    self.flags = set()

    self.is_public = is_public
    self.prefix = public_prefix if is_public else internal_prefix

    self.bkup_ip_path = 'bkup_{}_ip.txt'.format('public' if is_public else 'internal')
    self.bkup_link_path = 'bkup_{}_link.txt'.format('public' if is_public else 'internal')
    self.bkup_flag_path = 'bkup_{}_flag.txt'.format('public' if is_public else 'internal')

    self.lock_ip = threading.Lock()
    self.lock_link = threading.Lock()
    self.lock_flag = threading.Lock()

    if is_resume:
      if os.path.exists(self.bkup_ip_path):
        with open(self.bkup_ip_path, 'r') as fp:
          for l in fp:
            self.ips.add(l.strip('\n'))          

      if os.path.exists(self.bkup_link_path):
        with open(self.bkup_link_path, 'r') as fp:
          for l in fp:
            self.links.add(tuple(l.strip('\n').split(',')))

      if not reset_flag:
        if os.path.exists(self.bkup_flag_path):
          with open(self.bkup_flag_path, 'r') as fp:
            for l in fp:
              self.flags.add(l.strip('\n'))
      else:
        if os.path.exists(self.bkup_flag_path): os.remove(self.bkup_flag_path)

      print('- resumed with {} ip\'s, {} links and {} flags'.format(len(self.ips), len(self.links), len(self.flags)))
    else:
      if os.path.exists(self.bkup_ip_path): os.remove(self.bkup_ip_path)
      if os.path.exists(self.bkup_link_path): os.remove(self.bkup_link_path)
      if os.path.exists(self.bkup_flag_path): os.remove(self.bkup_flag_path)

    print()

  def add_ip(self, ip):
    if not ip.startswith(self.prefix): return

    if ip not in self.ips:
      self.ips.add(ip)
      self.backup_ip(ip)

      print('***** added new ip: {} ({} ip\'s, {} links)'.format(ip, len(self.ips), len(self.links)))

  def add_link(self, ip1, ip2):
    if not ip1.startswith(self.prefix) or not ip2.startswith(self.prefix): return

    s_ip, e_ip = min(ip1, ip2), max(ip1, ip2)

    if (s_ip, e_ip) not in self.links:      
      self.links.add((s_ip, e_ip))
      self.backup_link((s_ip, e_ip))

  def add_flag(self, ip):
    if not ip.startswith(self.prefix): return

    self.backup_flag(ip)
    self.flags.add(ip)

    print('##### flagged new ip: {} ({} flags)'.format(ip, len(self.flags)))

  def backup_ip(self, ip):
    with self.lock_ip:
      with open(self.bkup_ip_path, 'a') as fp:
        fp.write(ip + '\n')

  def backup_link(self, ip1, ip2):
    with self.lock_link:
      with open(self.bkup_link_path, 'a') as fp:
        fp.write(ip1 + ',' + ip2 + '\n')

  def backup_flag(self, ip):
    with self.lock_flag:
      with open(self.bkup_flag_path, 'a') as fp:
        fp.write(ip + '\n')

def tuplize(ip):
  return tuple([int(x) for x in ip.split('.')])

def ping(ip):
  if ip in topology.flags: return

  r, _ = traceroute(ip, l4 = UDP(dport = 33434), verbose = 0)
  
  if len(r) == 0:
    topology.add_flag(ip)
    return

  prev = r[0][0].src
  topology.add_ip(prev)

  found = False

  for _, x in r:
    topology.add_ip(x.src)
    topology.add_link(prev, x.src)
    
    if x.src == ip: found = True
    prev = x.src

  if not found: topology.add_flag(ip)

def work(workload):
  for ip in workload:
    ping(ip)

def main(args):
  is_public = args.mode.lower() == 'public'
  global topology

  topology = Topology(is_resume = args.resume, reset_flag = args.flag, is_public = is_public)
  
  tasks = [[] for _ in range(args.thread)]
  wid = 0

  for k in range(2 ** (16 if is_public else 24)):
    if is_public:
      x = k // 256
      y = k % 256

      ip = '{}{}.{}'.format(public_prefix, x, y)
    else:
      x = k // 65536
      y = (k - x * 65536) // 256
      z = (k - x * 65536) % 256

      ip = '{}{}.{}.{}'.format(internal_prefix, x, y, z)

    if tuplize(ip) >= tuplize(args.start) and tuplize(ip) <= tuplize(args.end) and ip not in topology.flags:
      tasks[wid].append(ip)
      wid = (wid + 1) % args.thread

  for i in range(args.thread):
    t = threading.Thread(target = work, args = (tasks[i], ))
    t.start()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-m', '--mode', type = str, default = None, help = 'public or internal')
  parser.add_argument('-s', '--start', type = str, default = '0.0.0.0', help = 'start ip to scan')
  parser.add_argument('-e', '--end', type = str, default = '255.255.255.255', help = 'end ip to scan')
  parser.add_argument('-t', '--thread', type = int, default = 8, help = 'number of threads')
  parser.add_argument('-r', '--resume', action = 'store_true', default = False, help = 'resume from backup file')
  parser.add_argument('-f', '--flag', action = 'store_true', default = False, help = 'reset flags')
  args = parser.parse_args()

  if args.mode.lower() != 'public' and args.mode.lower() != 'internal':
    print('argument `mode (-m)` invalid. must be `public` or `internal`.')
    exit(-1)

  print()  
  main(args)
