import argparse
import networkx as nx
from pylab import *
from matplotlib.animation import FuncAnimation
import os

parser = argparse.ArgumentParser(description='Visualizes networks dynamic.')
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
    '-a',
    type=str,
    help='alpha tester',
    required=True,
    default=""
)

args = parser.parse_args()
fig_size = args.s
fig_type = args.t
file = args.f


def print_text_and_images(file_name, nodes, connections_g, events):
    G = nx.MultiGraph(name=file_name)
    G.add_nodes_from(nodes)
    G.add_edges_from(connections_g)

    fig = plt.figure(figsize=(fig_size, fig_size))
    pos = nx.circular_layout(G)
    nodes = nx.draw_networkx_nodes(G, pos, labels=True, alpha=1, node_color="cyan")

    nx.draw_networkx_labels(G, pos)

    global idx
    idx = -1

    def get_for(n):
        # TODO: must cut out closed connections.
        return connections_g[:n]

    def update(n):
        global idx
        idx += 1
        edges = nx.draw_networkx_edges(G, pos, edgelist=get_for(n), alpha=1)
        print("Done {} of {}".format(idx, len(connections_g)))
        return edges, nodes

    animation = FuncAnimation(fig, update, interval=50, blit=False, save_count=len(connections_g) - 0)
    print("Saving .gif")
    animation.save('nets/anim.gif', writer='imagemagick', fps=25, )


def print_file(file_name):
    nodes = set()
    connections = list()
    events = list()

    for line in open(file_name, "r").readlines():
        try:
            parsed = line[:-1]
            parsed = parsed.split(",")
            parsed = [int(s) if s != "open" and s != "close" else s for s in parsed]
            nodes.add(parsed[0])
            nodes.add(parsed[1])
            connections.append([parsed[0], parsed[1]])
            events.append([parsed[0], parsed[1], parsed[2], parsed[3]])
        except:
            print("Cant parse line: ", line)

    nodes = list(nodes)
    nodes.sort()
    print_text_and_images(file_name, nodes, connections, events)


if file == None:
    done = False
    if os.path.isfile("nets/cliques_timed.txt"):
        print_file("nets/cliques_timed.txt")
        done = True
    if not done:
        print("No example file exists. Run 'python "
              "example_nets.py'")
else:
    print_file(file)
