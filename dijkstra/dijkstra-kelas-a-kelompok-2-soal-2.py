import networkx as nx
from matplotlib import pyplot as plt
from tabulate import tabulate


class Dijkstra:
    def __init__(self, graph):
        if not isinstance(graph, Graph):
            raise Exception("Graph must be an instance of the Graph class.")

        self.graph = graph
        self.distances = {}
        self.previous = {}
        self.visited = set()
        self.paths = {}
        self.table_data = []
        self.node_weights = {}

    def find_path(self, start, finish):
        self.__initialize(start)

        while self.visited != set(self.graph.get_vertices()):
            current_vertex = min(
                (v for v in self.distances if v not in self.visited),
                key=lambda x: (self.distances[x], -len(self.paths[x])),
            )

            for edge in self.graph.get_edges()[current_vertex]:
                neighbor, weight = edge["to"], edge["weight"]
                new_distance = self.distances[current_vertex] + weight
                if new_distance < self.distances[neighbor]:
                    self.distances[neighbor] = new_distance
                    self.previous[neighbor] = current_vertex
                    self.paths[neighbor] = self.paths[current_vertex] + [neighbor]

                    self.node_weights[neighbor] = (
                        self.node_weights.get(current_vertex, 0) + 1
                    )

            self.visited.add(current_vertex)
            self.__record_table(current_vertex)

        return self.__format_path(start, finish)

    def visualize_graph(self, finish, positions=None):
        G = self.__build_nx_graph()
        plt.figure(figsize=(15, 5))

        layout = positions or nx.spring_layout(G, seed=42)
        edge_labels = nx.get_edge_attributes(G, "weight")

        plt.subplot(121)
        plt.title("Grafik Sebelum Djikstra")
        nx.draw(G, pos=layout, with_labels=True, node_color="lightblue")
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels)

        plt.subplot(122)
        plt.title("Graph Setelah Djikstra")
        shortest_path = self.__get_shortest_path_edges(finish)
        nx.draw(G, pos=layout, with_labels=True, node_color="lightgreen")
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels)
        nx.draw_networkx_edges(
            G, pos=layout, edgelist=shortest_path, edge_color="red", width=2
        )
        nx.draw_networkx_nodes(G, pos=layout, nodelist=[finish], node_color="red")

        plt.tight_layout()
        plt.show()

    def __initialize(self, start):
        self.distances = {v: float("inf") for v in self.graph.get_vertices()}
        self.previous = {v: None for v in self.graph.get_vertices()}
        self.visited = set()
        self.paths = {v: [] for v in self.graph.get_vertices()}
        self.table_data = []
        self.distances[start] = 0

    def __record_table(self, current_vertex):
        row = [current_vertex] + [
            (
                f"{self.distances[v]} ({self.previous[v]})"
                if self.distances[v] != float("inf")
                else "∞"
            )
            for v in self.graph.get_vertices()
        ]

        self.table_data.append(row)

    def __format_path(self, start, finish):
        path = []
        current = finish
        while current:
            path.insert(0, current)
            current = self.previous[current]

        table = tabulate(
            self.table_data,
            headers=["Visited"] + self.graph.get_vertices(),
            tablefmt="fancy_grid",
        )

        return f"{table}\n\nShortest Path: {' -> '.join(path)}"

    def __build_nx_graph(self):
        G = nx.DiGraph()
        for vertex in self.graph.get_vertices():
            for edge in self.graph.get_edges()[vertex]:
                G.add_edge(vertex, edge["to"], weight=edge["weight"])

        return G

    def __get_shortest_path_edges(self, finish):
        path = []
        current = finish
        while self.previous[current]:
            path.append((self.previous[current], current))
            current = self.previous[current]

        return path


class Graph:
    def __init__(self):
        self.__vertices = []
        self.__edges = {}

    def get_vertices(self):
        return self.__vertices

    def get_edges(self):
        return self.__edges

    def add_vertex(self, *vertices):
        for vertex in vertices:
            if vertex in self.__vertices:
                raise Exception(
                    f"The vertex {vertex} is already within the graph's vertices."
                )

            self.__vertices.append(vertex)
            self.__edges[vertex] = []

    def add_edge(self, from_vertex, to_vertex, weight):
        if from_vertex not in self.__vertices or to_vertex not in self.__vertices:
            raise Exception(
                "Invalid edge. One or more vertices do not exist in the graph."
            )

        self.__edges[from_vertex].append({"to": to_vertex, "weight": weight})

    def __str__(self):
        return str(self.__edges)


if __name__ == "__main__":
    graph = Graph()
    graph.add_vertex(
        "Perum Kariangau", "WR", "Pawon", "Bang John", "Boyolali", "Riski", "Labter 2"
    )

    graph.add_edge("Perum Kariangau", "WR", 16)
    graph.add_edge("Perum Kariangau", "Pawon", 6)
    graph.add_edge("Pawon", "WR", 11)
    graph.add_edge("Pawon", "Bang John", 6)
    graph.add_edge("Pawon", "Boyolali", 14)
    graph.add_edge("Pawon", "Riski", 10)
    graph.add_edge("Bang John", "WR", 4)
    graph.add_edge("Bang John", "Labter 2", 8)
    graph.add_edge("WR", "Labter 2", 3)
    graph.add_edge("Boyolali", "Labter 2", 2)
    graph.add_edge("Riski", "Boyolali", 3)

    dijkstra = Dijkstra(graph)
    result = dijkstra.find_path("Perum Kariangau", "Labter 2")
    print(result)

    graph_positions = {
        "Perum Kariangau": (0, -1),
        "WR": (0, 2),
        "Pawon": (1, 0),
        "Bang John": (1, 1),
        "Boyolali": (2, 1),
        "Riski": (3, 0),
        "Labter 2": (2, 2),
    }
    dijkstra.visualize_graph("Labter 2", positions=graph_positions)
