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
    target_ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]  # Example target IPs
    for target_ip in target_ips:
        result = run_traceroute(target_ip)
        print(f"Traceroute to {target_ip}: {result}")
