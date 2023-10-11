# traceroute_script.py
from scapy.all import IP, UDP, sr1

def run_traceroute(target_ip):
    hops = []
    for ttl in range(1, 30):  # Set a suitable TTL range
        pkt = IP(dst=target_ip, ttl=ttl) / UDP(dport=33434)
        reply = sr1(pkt, verbose=0, timeout=1)
        if reply is None:
            break
        elif reply.type == 3:
            hops.append(reply.src)
            break
        else:
            hops.append(reply.src)
    return hops

if __name__ == "__main__":
    target_ips = [f"10.0.0.{i}" for i in range(1, 255)]  # internal Campus routers
    target_ips2 = [f"138.238.{i}.{i}" for i in range(1, 16)]  # External public servers
    for target_ip in target_ips:
        result = run_traceroute(target_ip)
        print(f"Traceroute to {target_ip}: {result}")
