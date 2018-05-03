import networkx as nx
import matplotlib.pyplot as plt
import pickle

def girvan_newman(G, most_valuable_edge=None):
    if G.number_of_edges() == 0:
        yield tuple(nx.connected_components(G))
        return
    if most_valuable_edge is None:
        def most_valuable_edge(G):
            betweenness = nx.edge_betweenness_centrality(G)
            return max(betweenness, key=betweenness.get)
    g = G.copy().to_undirected()
    g.remove_edges_from(g.selfloop_edges())
    while g.number_of_edges() > 0:
        yield _without_most_central_edges(g, most_valuable_edge)



def _without_most_central_edges(G, most_valuable_edge):
    original_num_components = nx.number_connected_components(G)
    num_new_components = original_num_components
    while num_new_components <= original_num_components:
        edge = most_valuable_edge(G)
        G.remove_edge(*edge)
        new_components = tuple(nx.connected_components(G))
        num_new_components = len(new_components)
    return new_components
def main():

    graph = nx.read_edgelist("grph.txt",delimiter=",")
    components = [c for c in nx.connected_component_subgraphs(graph)]
    f2 =[]
    for c1 in components:
        k = girvan_newman(c1)
        f2.append(tuple(sorted(c) for c in next(k)))
    pickle.dump(f2, open('clstropt.pkl', 'wb'))
    nx.draw(graph)
    plt.show()
if __name__ == '__main__':
    main()