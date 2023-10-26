
import matplotlib.pyplot as plt
import networkx as nx
import argparse

ip_path = 'total_ip.txt'
link_path = 'total_link.txt'
out_path = 'topology.jpg'
node_color = 'lightgreen'

with open(ip_path, 'r') as fp:
	total_ip = [l.strip('\n') for l in fp]

with open(link_path, 'r') as fp:
	total_link = []

	for l in fp:
		e = l.strip('\n').split(',')
		if e[0] == e[1]: continue

		total_link.append((e[0], e[1]))

def calc_links():
	mmm = {}

	for ip in total_ip:
		mmm[ip] = set()

	for s, e in total_link:
		mmm[s].add(e)
		mmm[e].add(e)

	cm = {}

	for ip in total_ip:
		c = len(mmm[ip])
		if c not in cm.keys():
			cm[c] = 1
		else:
			cm[c] += 1

	print(cm)	
	return mmm

def draw_whole_topology():
	g = nx.Graph()

	mmm = calc_links()
	invalid_ips = [k for k in mmm.keys() if len(mmm[k]) < 2]

	for ip in total_ip:
		if ip in invalid_ips: continue
		g.add_node(ip)

	for s, e in total_link:
		if s in invalid_ips or e in invalid_ips: continue
		g.add_edge(s, e)

	fig = plt.figure(figsize = (200, 120))
	nx.draw(g, node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig('vis_whole.jpg')
	plt.show()

def draw_isolated():
	g = nx.Graph()
	iso_ip = []

	for ip in total_ip:
		isolated = True

		for s, e in total_link:
			if ip == s or ip == e:
				isolated = False
				break

		if isolated: iso_ip.append(ip)

	for ip in iso_ip:
		g.add_node(ip)

	fig = plt.figure(figsize = (100, 60))
	nx.draw(g, node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig('vis_isolated.jpg')
	plt.show()

def draw_public():
	g = nx.Graph()

	mmm = calc_links()
	invalid_ips = [k for k in mmm.keys() if len(mmm[k]) < 2]

	for ip in total_ip:
		if ip.startswith('138.238.'):
			if ip in invalid_ips: continue
			g.add_node(ip)

	for s, e in total_link:
		if s.startswith('138.238.') and e.startswith('138.238.'):
			if s in invalid_ips or e in invalid_ips: continue
			g.add_edge(s, e)

	fig = plt.figure(figsize = (40, 24))
	#nx.draw(g, pos = nx.circular_layout(g), node_color = node_color, edge_color = 'lightgray', with_labels = True)
	#nx.draw(g, node_color = node_color, edge_color = 'lightgray', with_labels = True)
	nx.draw(g, pos = nx.planar_layout(g), node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig('vis_public.jpg')
	plt.show()

def draw_bridge():
	g = nx.Graph()

	mmm = calc_links()
	invalid_ips = [k for k in mmm.keys() if len(mmm[k]) < 2]

	for s, e in total_link:
		if s.startswith('138.238.') and not e.startswith('138.238.'):
			if s in invalid_ips or e in invalid_ips: continue
			g.add_edge(s, e)
		elif not s.startswith('138.238.') and e.startswith('138.238.'):
			if s in invalid_ips or e in invalid_ips: continue
			g.add_edge(s, e)

	fig = plt.figure(figsize = (90, 54))
	nx.draw(g, pos = nx.random_layout(g), node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig('vis_bridge.jpg')
	plt.show()

def draw_gates():
	g = nx.Graph()

	mmm = calc_links()
	gate_ips = [k for k in mmm.keys() if len(mmm[k]) > 3]

	# for ip in total_ip:
	# 	link_count = 0

	# 	for s, e in total_link:
	# 		if s == ip or e == ip:
	# 			link_count += 1
	# 			if link_count > 1: break

	# 	if link_count > 1:
	# 		gate_ips.append(ip)
	# 		g.add_node(ip)

	for s, e in total_link:
		if s in gate_ips and e in gate_ips:
			g.add_edge(s, e)

	fig = plt.figure(figsize = (30, 18))
	nx.draw(g, pos = nx.random_layout(g), node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig('vis_gate.jpg')
	plt.show()

#def draw_

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--mode', type = str, default = None, help = 'mode')
	args = parser.parse_args()

	if args.mode == 'whole':
		draw_whole_topology()
	elif args.mode == 'iso':
		draw_isolated()
	elif args.mode == 'pub':
		draw_public()
	elif args.mode == 'bridge':
		draw_bridge()
	elif args.mode == 'gate':
		draw_gates()
	elif args.mode == 'calc':
		calc_links()
	else:
		print('invalid argument.')
		exit(-1)
