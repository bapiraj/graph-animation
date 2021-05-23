import pygame
import random
import json
from collections import deque

# Set LOAD_EXISTING_GRAPH to True, if you want to use the graph predefined in the json files.
LOAD_EXISTING_GRAPH = False
if LOAD_EXISTING_GRAPH:
    # Changing the below values when LOAD_EXISTING_GRAPH is set to True might cause errors
    WIDTH, HEIGHT = 1920, 1080
    NODE_RADIUS = 2
    N_NODES = 20000
    MIN_DIST_NODES = 3
    MIN_EDGES = 3
else:
    # If you want to experiment with different number of nodes and edges,
    # or if the your screen resolution is different from 1920x1080,
    # set LOAD_EXISTING_GRAPH to False and experiment by changing the below variables.
    WIDTH, HEIGHT = 1920, 1080
    NODE_RADIUS = 5
    N_NODES = 4000
    MIN_DIST_NODES = 3
    MIN_EDGES = 3
ALGORITHM = "DFS"
pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Graph")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("bahnschrift", 25)


def display_msg(msg):
    SCREEN.blit(msg, [200, 200])
    pygame.display.update()
    SCREEN.fill((0, 0, 0))

def generate_edges(nodes):
    graph = [[] for i in range(N_NODES)]
    if LOAD_EXISTING_GRAPH:
        with open("edges.json", "r") as fp:
            edges = json.load(fp)
    
        for i, e in enumerate(edges):
            edges[i] = tuple(e)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
    else:
        edges = []
        for i, node in enumerate(nodes):
            x, y = node
            sorted_indices = [enum[0] for enum in sorted(enumerate(nodes), key=lambda e: ((e[1][0]-x)**2 + (e[1][1]-y)**2)**0.5)]
            j = 1
            max_rem = MIN_EDGES - len(graph[i])
            while max_rem > 0:
                if sorted_indices[j] not in graph[i]:
                    p = tuple(sorted((i, sorted_indices[j])))
                    if p not in edges:
                        edges.append(p)
                    graph[i].append(sorted_indices[j])
                    graph[sorted_indices[j]].append(i)
                    max_rem -= 1
                j += 1
            msg = FONT.render("Nodes Processed to create edges: {}/{}".format(i, N_NODES), True, (255, 255, 255))
            display_msg(msg)
            
    return graph, edges

def generate_nodes():
    nodes = []
    if LOAD_EXISTING_GRAPH:
        with open("nodes.json", "r") as fp:
            nodes = json.load(fp)
        for i, e in enumerate(nodes):
            nodes[i] = tuple(e)
    count = len(nodes)
    while count < N_NODES:
        x = random.randint(NODE_RADIUS, WIDTH-NODE_RADIUS)
        y = random.randint(NODE_RADIUS, HEIGHT-NODE_RADIUS)
        flag = False
        for x1, y1 in nodes:
            distance = ((x-x1)**2 + (y-y1)**2)**0.5
            if distance < MIN_DIST_NODES:
                flag = True
        if flag:
            continue
        nodes.append((x, y))
        count += 1
        msg = FONT.render("Nodes Created:{}/{}".format(count, N_NODES), True, (255, 255, 255))
        display_msg(msg)
    return nodes


def display(visited_nodes, visited_edges, nodes, edges):
    for i, edge in enumerate(edges):
        u, v = edge
        if visited_edges[i]:
            pygame.draw.line(SCREEN, (255, 0, 0), nodes[u], nodes[v])
        else:
            pygame.draw.line(SCREEN, (255, 255, 0), nodes[u], nodes[v])
    
    for i, node in enumerate(nodes):
        if visited_nodes[i]:
            pygame.draw.circle(SCREEN, (255, 0, 0), node, NODE_RADIUS)
        else:
            pygame.draw.circle(SCREEN, (255, 255, 255), node, NODE_RADIUS)
    pygame.display.update()

def dfs(n_nodes, graph, visited_nodes, visited_edges, nodes, edges):
    for i in range(n_nodes):
        if not visited_nodes[i]:
            stack = deque([i])
            visited_nodes[i] = True
            while stack:
                u = stack.pop()
                display(visited_nodes, visited_edges, nodes, edges)
                for v in graph[u]:
                    if not visited_nodes[v]:
                        stack.append(v)
                        visited_nodes[v] = True
                        edge = tuple(sorted([u, v]))
                        edge_index = edges.index(edge)
                        visited_edges[edge_index] = True 

def bfs(n_nodes, graph, visited_nodes, visited_edges, nodes, edges):
    for i in range(n_nodes):
        if not visited_nodes[i]:
            stack = deque([i])
            visited_nodes[i] = True
            while stack:
                u = stack.popleft()
                display(visited_nodes, visited_edges, nodes, edges)
                for v in graph[u]:
                    if not visited_nodes[v]:
                        stack.append(v)
                        visited_nodes[v] = True
                        edge = tuple(sorted([u, v]))
                        edge_index = edges.index(edge)
                        visited_edges[edge_index] = True    


def run():
    nodes = generate_nodes()
    graph, edges = generate_edges(nodes)
    n_edges = len(edges)
    visited_nodes = [False]*N_NODES
    visited_edges = [False]*n_edges
    if ALGORITHM == "DFS":
        dfs(N_NODES, graph, visited_nodes, visited_edges, nodes, edges)
    else:
        bfs(N_NODES, graph, visited_nodes, visited_edges, nodes, edges)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()

run()
