import argparse
import random
import os

parser = argparse.ArgumentParser(description='Creates networks.')
parser.add_argument(
    '-n',
    type=int,
    help='amount of replicas',
    required=True,
)

args = parser.parse_args()


def cliques(start, end):
    f = open("nets/cliques.txt", "w")

    links = set()
    for i in range(start, end + 1):
        for j in range(start, end + 1):
            links.add('{},{}\n'.format(i, j))

    sorted_links = list(links)
    sorted_links.sort()
    f.writelines(sorted_links)
    f.close()


def cliques_timed(start, end, start_t, end_t):
    f = open("nets/cliques_timed.txt", "w")

    links = []
    existing = set()

    nodes = end - start
    time_range = end_t - start_t
    interval_size = int(time_range / (end - start))

    curr_time = start_t
    for i in range(start, end + 1):
        for j in range(start, end + 1):
            if i == j:
                pass
            action = "open" if random.random() > 0.1 or len(links) < 5 else "close"
            curr_time += interval_size
            if action == "open":
                line = '{},{}'.format(min(i, j), max(i, j))
                if not line in existing:
                    existing.add(line)
                    links.append('{},{},{},{}\n'.format(i, j, curr_time, action))

            else:
                rand_pos = int(random.random() * len(links))
                prev = links[rand_pos].split(",")
                links.append('{},{},{},{}\n'.format(prev[0], prev[1], curr_time, action))

    f.writelines(links)
    f.close()


def circle(start, end):
    f = open("nets/circle.txt", "w")

    links = set()
    for i in range(start, end):
        links.add('{},{}\n'.format(i, i + 1))

    links.add('{},{}\n'.format(end, start))
    sorted_links = list(links)
    sorted_links.sort()
    f.writelines(sorted_links)
    f.close()


def rg(start, end):
    f = open("nets/rg.txt", "w")

    links = set()
    for i in range(start, end + 1):
        links.add('{},{}\n'.format(i, i + 1))
        for j in range(0, int(random.random() * (end - start))):
            pos = int(random.random() * (end - start)) + start
            while pos == i:
                pos = int(random.random() * (end - start))

            links.add('{},{}\n'.format(min(i, pos), max(i, pos)))

    links.add('{},{}\n'.format(min(start, end), max(start, end)))
    sorted_links = list(links)
    sorted_links.sort()
    f.writelines(sorted_links)
    f.close()


print('Making networks for {} nodes in ./nets.'.format(args.n))
os.mkdir("nets")
cliques(1, 1 + args.n)
cliques_timed(1, 1 + args.n, 1, args.n * 101)
circle(1, 1 + args.n)
rg(1, 1 + args.n)
