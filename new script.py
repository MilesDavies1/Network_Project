# traceroute_script.py
from concurrent.futures import ThreadPoolExecutor, as_completed
from scapy.all import IP, UDP, sr1
import pandas as pd
import sys
import os

def run_traceroute(target_ip):
    hops = []
    try:
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
    except Exception as e:
        # Record the error information
        hops.append(f"Error: {str(e)}")
    return {'Target IP': target_ip, 'Traceroute Result': hops}

# multithreading function to run the ip search in parallel
def run_traceroutes(target_ips, num_threads=200):
    traceroute_data = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(run_traceroute, target_ip): target_ip for target_ip in target_ips}

        for future in as_completed(futures):
            target_ip = futures[future]
            try:
                result = future.result()
                traceroute_data.append(result)
            except Exception as e:
                print(f"Error for {target_ip}: {str(e)}")

    # Sort the results based on the original order of target_ips
    traceroute_data.sort(key=lambda x: target_ips.index(x['Target IP']))

    # Print the sorted results
    for result in traceroute_data:
        print(f"Traceroute to {result['Target IP']}: {result['Traceroute Result']}")

    return traceroute_data

if __name__ == "__main__":
    target_ips = [f"10.{k}.{j}.{i}" for k in range(0, 256) for j in range(0, 256) for i in range(1, 255, 8)]  # internal Campus routers, skipping every 8th IP
    target_ips2 = [f"138.238.{j}.{i}" for j in range(0, 256) for i in range(1, 255)]  # External public servers


    # traceroute dictionary variable
    traceroute_data = run_traceroutes(target_ips)

    # creates a pandas dataframe and adds the dictionary info
    traceroute_df = pd.DataFrame(traceroute_data)

    # pushes the collected dataframe info to an excel document named traceroute_xlsx
    traceroute_df.to_excel('traceroute_results.xlsx', index=False)

# Suggestion: use google dns to search ips
