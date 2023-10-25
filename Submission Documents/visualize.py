
import matplotlib.pyplot as plt
import networkx as nx

ip_path = 'total_ip.txt'
link_path = 'total_link.txt'
out_path = 'topology.png'
node_color = 'lightgreen'

with open(ip_path, 'r') as fp:
	total_ip = [l.strip('\n') for l in fp]

with open(link_path, 'r') as fp:
	total_link = []

	for l in fp:
		e = l.strip('\n').split(',')
		total_link.append((e[0], e[1]))

def draw_whole_topology():
	g = nx.Graph()

	for ip in total_ip:
		g.add_node(ip)

	for s, e in total_link:
		g.add_edge(s, e)

	fig = plt.figure(figsize = (100, 60))
	nx.draw(g, node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig('vis_whole.png')
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

	plt.savefig('vis_isolated.png')
	plt.show()

def draw_public():
	g = nx.Graph()

	for ip in total_ip:
		if ip.startswith('138.238.'): g.add_node(ip)

	for s, e in total_link:
		if s.startswith('138.238.') and e.startswith('138.238.'):
			g.add_edge(s, e)

	fig = plt.figure(figsize = (10, 6))
	nx.draw(g, pos = nx.circular_layout(g), node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig('vis_public.png')
	plt.show()

def draw_bridge():
	g = nx.Graph()

	for s, e in total_link:
		if s.startswith('138.238.') and not e.startswith('138.238.'):
			g.add_edge(s, e)
		elif not s.startswith('138.238.') and e.startswith('138.238.'):
			g.add_edge(s, e)

	fig = plt.figure(figsize = (90, 54))
	nx.draw(g, pos = nx.random_layout(g), node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig('vis_bridge.png')
	plt.show()

def draw_gates():
	g = nx.Graph()
	gate_ips = []

	for ip in total_ip:
		link_count = 0

		for s, e in total_link:
			if s == ip or e == ip:
				link_count += 1
				if link_count > 1: break

		if link_count > 1:
			gate_ips.append(ip)
			g.add_node(ip)

	for s, e in total_link:
		if s in gate_ips and e in gate_ips:
			g.add_edge(s, e)

	fig = plt.figure(figsize = (30, 18))
	nx.draw(g, pos = nx.random_layout(g), node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig('vis_gate.png')
	plt.show()

#def draw_

if __name__ == '__main__':
	#draw_whole_topology()
	#draw_isolated()
	#draw_public()
	#draw_bridge()
	draw_gates()
