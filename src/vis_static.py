import argparse
import networkx as nx
import matplotlib.pyplot as plt
import os

parser = argparse.ArgumentParser(description='Visualizes networks static.')
parser.add_argument(
    '-s',
    type=int,
    help='figure size',
    required=False,
    default=5
)
parser.add_argument(
    '-f',
    type=str,
    help='file',
    required=False,
    default=None
)
parser.add_argument(
    '-t',
    type=str,
    help='out file type',
    required=False,
    default="pdf"
)
parser.add_argument(
    '-g',
    choices=['circ', 'fruc', 'rand'],
    required=False,
    default=None,
    help="Choose only one graph type"
)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser.add_argument(
    '-v',
    type=str2bool,
    help='create images',
    required=False,
    default=True
)

args = parser.parse_args()
fig_size = args.s
fig_type = args.t
file = args.f
graph = args.g
make_images = args.v


def print_text_and_images(file_name, nodes, connections_g):
    G = nx.MultiGraph(name=file_name)
    G.add_nodes_from(nodes)
    G.add_edges_from(connections_g)
    print(nx.info(G))
    print("Graph density:", nx.density(G))
    print("Connections Histogram:", nx.degree_histogram(G))
    print("Connections Histogram count:", len(nx.degree_histogram(G)))
    try:
        print("DIAMETER:", nx.diameter(G))
    except:
        print("Graph is not connected.")

    print(make_images)
    if not make_images:
        return

    def start():
        fig = plt.figure(figsize=(fig_size, fig_size))
        plt.gca().get_xaxis().set_visible(False)
        plt.gca().get_yaxis().set_visible(False)
        return fig

    def end(filename):
        nx.draw(G, pos=pos, with_labels=True)
        fig.savefig(filename, dpi=fig.dpi)
        pass

    if (not graph or graph == 'circ'):
        fig = start()
        pos = nx.circular_layout(G)
        end('{}-circular.{}'.format(file_name, fig_type))

        print("Drawn circular.")

    if (not graph or graph == 'fruc'):
        fig = start()
        pos = nx.fruchterman_reingold_layout(G)
        end('{}-frl.{}'.format(file_name, fig_type))
        print("Drawn fruchterman reingold.")

    if (not graph or graph == 'rand'):
        fig = start()
        pos = nx.random_layout(G)
        end('{}-rand.{}'.format(file_name, fig_type))
        print("Drawn random.")


def print_file(file_name):
    nodes = set()
    connections = list()

    for line in open(file_name, "r").readlines():
        if not line[0] == "#":
        	try:
            	parsed = line[:-1]
            	parsed = parsed.split(",")
            	nodes.add(int(parsed[0]))
            	nodes.add(int(parsed[1]))
            	connections.append([int(parsed[0]), int(parsed[1])])
        	except:
            	print("Cant parse line: ", line)
    nodes = list(nodes)
    nodes.sort()

    print_text_and_images(file_name, nodes, connections)


if not file:
    done = False
    if os.path.isfile("nets/circle.txt"):
        print_file("nets/circle.txt")
        done = True
    if os.path.isfile("nets/cliques.txt"):
        print_file("nets/cliques.txt")
        done = True
    if os.path.isfile("nets/rg.txt"):
        print_file("nets/rg.txt")
        done = True
    if not done:
        print("No example file exists. Run 'python "
              "example_nets.py'")
else:
    print_file(file)
