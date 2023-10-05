
import matplotlib.pyplot as plt
import networkx as nx
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', type = str, default = None, help = 'public or internal')
args = parser.parse_args()

if args.mode.lower() != 'public' and args.mode.lower() != 'internal':
	print('argument `mode (-m)` invalid. must be `public` or `internal`.')
	exit(-1)

if args.mode.lower() == 'public':
	ip_path = 'bkup_public_ip.txt'
	link_path = 'bkup_public_link.txt'
	out_path = 'graph_public.png'
	node_color = 'pink'
else:
	ip_path = 'bkup_internal_ip.txt'
	link_path = 'bkup_internal_link.txt'
	out_path = 'graph_internal.png'
	node_color = 'lightgreen'	

g = nx.Graph()

with open(ip_path, 'r') as fp:
	for l in fp:
		g.add_node(l.strip('\n'))

with open(link_path, 'r') as fp:
	for l in fp:
		e = l.strip('\n').split(',')
		g.add_edge(e[0], e[1])

fig = plt.figure(figsize = (20, 12))

nx.draw(g, pos = nx.circular_layout(g), node_color = node_color, edge_color = 'lightgray', with_labels = True)

plt.savefig(out_path)
plt.show()