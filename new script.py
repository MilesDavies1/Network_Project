# traceroute_script.py
from scapy.all import IP, UDP, sr1
import pandas as pd
import os 

def run_traceroute(target_ip):
    hops = []
    for ttl in range(1, 30):  # Set a suitable TTL range
        pkt = IP(dst=target_ip, ttl=ttl) / UDP(dport=33434)
        reply = sr1(pkt, verbose=0, timeout=1)
        if reply is None: # Note: Breaking after no reply is undescriptive 
            break # changed it to pass, had no effect
        elif reply.type == 3:
            hops.append(reply.src)
            break
        else:
            hops.append(reply.src)
    return hops

if __name__ == "__main__":
    target_ips = [f"10.{k}.{j}.{i}" for k in range(0, 256) for j in range(0, 256) for i in range(1, 255, 8)]  # internal Campus routers, skipping every 8th IP
    target_ips2 = [f"138.238.{i}.{j}" for i in range(0, 256) for j in range(1, 255)]  # External public servers

    #create an empty dictionary to store traceroute info
    traceroute_data = []

    for target_ip in target_ips:
        result = run_traceroute(target_ip)
        traceroute_data.append({'Target IP': target_ip, 'Traceroute Result': result}) # adds tracerouts data to the dictionary
        traceroute_df = pd.DataFrame(traceroute_data) # creates a pandas dataframe and adds the dictionary info
        traceroute_df.to_excel('traceroute_results.xlsx', index=False)  # pushes the collected dataframe info to an excel document named traceroute_xlsx
        print(f"Traceroute to {target_ip}: {result}")

#Todo: use google dns ips, remove duplicate excel results, use multithreading(200 threads), split ranges per group member, write seperate program to merge all results
