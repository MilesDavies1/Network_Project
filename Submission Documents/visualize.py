
import matplotlib.pyplot as plt
import networkx as nx
import argparse

node_color = 'lightgreen'

def calc_links(output = False):
	mmm = {}

	for ip in total_ip:
		mmm[ip] = set()

	for s, e in total_link:
		mmm[s].add(e)
		mmm[e].add(s)

	if output:
		cm = {}

		for ip in total_ip:
			c = len(mmm[ip])
			if c not in cm.keys():
				cm[c] = 1
			else:
				cm[c] += 1

		cc = []

		for c, m in cm.items():
			cc.append((c, m))

		cc.sort()

		with open('dist.csv', 'w') as fp:
			for c, m in cc:
				fp.write('{},{}\n'.format(c, m))

	return mmm

def draw_internal():
	g = nx.Graph()

	mmm = calc_links()
	valid_ips = set([k for k in mmm.keys() if len(mmm[k]) >= 2 and k.startswith('10.')])

	for ip in valid_ips:
		conn = mmm[ip] & valid_ips
		if len(conn) == 0: continue

		for c in conn:
			g.add_edge(ip, c)

	print('drawing...')

	fig = plt.figure(figsize = (200, 120))
	nx.draw(g, node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig(worker_prefix + 'vis_internal.jpg')
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

	plt.savefig(worker_prefix + 'vis_isolated.jpg')
	plt.show()

def draw_public():
	g = nx.Graph()

	mmm = calc_links()
	valid_ips = set([k for k in mmm.keys() if len(mmm[k]) >= 2 and k.startswith('138.238.')])

	for ip in valid_ips:
		conn = mmm[ip] & valid_ips
		if len(conn) == 0: continue

		for c in conn:
			g.add_edge(ip, c)

	print('drawing...')

	fig = plt.figure(figsize = (200, 120))
	nx.draw(g, node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig(worker_prefix + 'vis_public.jpg')
	plt.show()

def draw_bridge():
	g = nx.Graph()

	mmm = calc_links()
	valid_ips = set([k for k in mmm.keys() if len(mmm[k]) >= 4 and (k.startswith('138.238.') or k.startswith('10.'))])

	count = 0

	for ip in valid_ips:
		conn = mmm[ip] & valid_ips		

		if ip.startswith('10.'):
			prefix = '138.238.'
		else:
			prefix = '10.'

		conn = [c for c in conn if c.startswith(prefix)]
		if len(conn) == 0: continue

		for c in conn:
			count += 1
			g.add_edge(ip, c)

	print(count)
	print('drawing...')

	fig = plt.figure(figsize = (200, 120))
	nx.draw(g, node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig(worker_prefix + 'vis_bridge.jpg')
	plt.show()

def draw_gates():
	g = nx.Graph()

	mmm = calc_links()
	gate_ips = [k for k in mmm.keys() if len(mmm[k]) >= 6]

	for s, e in total_link:
		if s in gate_ips and e in gate_ips:
			g.add_edge(s, e)

	# fig = plt.figure(figsize = (30, 18))
	# nx.draw(g, pos = nx.circular_layout(g), node_color = node_color, edge_color = 'lightgray', with_labels = True)

	fig = plt.figure(figsize = (200, 120))
	nx.draw(g, node_color = node_color, edge_color = 'lightgray', with_labels = True)

	#nx.draw(g, node_color = node_color, edge_color = 'lightgray', with_labels = True)

	plt.savefig(worker_prefix + 'vis_gate.jpg')
	plt.show()

#def draw_

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-w', '--worker', type = str, default = '', help = 'worker')
	parser.add_argument('-m', '--mode', type = str, default = None, help = 'mode')
	args = parser.parse_args()

	global total_ip, total_link, worker_prefix

	ip_path = 'total_ip.txt'
	link_path = 'total_link.txt'

	if args.worker != '':
		worker_prefix = args.worker + '_'

		ip_path = worker_prefix + ip_path
		link_path = worker_prefix + link_path
	else:
		worker_prefix = ''

	with open(ip_path, 'r') as fp:
		total_ip = [l.strip('\n') for l in fp]

	with open(link_path, 'r') as fp:
		total_link = []

		for l in fp:
			e = l.strip('\n').split(',')
			if e[0] == e[1]: continue

			total_link.append((e[0], e[1]))

	if args.mode == 'internal':
		draw_internal()
	elif args.mode == 'iso':
		draw_isolated()
	elif args.mode == 'public':
		draw_public()
	elif args.mode == 'bridge':
		draw_bridge()
	elif args.mode == 'gate':
		draw_gates()
	elif args.mode == 'calc':
		calc_links(True)
	else:
		print('invalid argument.')
		exit(-1)
