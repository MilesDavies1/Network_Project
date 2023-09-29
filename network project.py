from scapy.all import IP, UDP, sr1

ipaddr = "1.2.3.4"

for i in range(1, 28):
    pkt = IP(dst=ipaddr, ttl=i) / UDP(dport=33434)
    reply = sr1(pkt, verbose=0, timeout=1)
    
    if reply is None:
        break
    elif reply.type == 3:
        print("Done!", reply.src)
        break
    else:
        print(f"{i} hops away:", reply.src)
