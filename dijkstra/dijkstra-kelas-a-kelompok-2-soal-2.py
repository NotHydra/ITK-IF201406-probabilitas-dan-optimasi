import networkx as nx

from matplotlib import pyplot as plt
from tabulate import tabulate
from typing import Dict, List, Tuple


class Dijkstra_Graph:
    def __init__(self) -> None:
        self.vertices: Dict[str, Dict[str, int | Dict[str, float]]] = {}

    def add_vertex(self, vertex: str, position_x: int, position_y: int) -> None:
        if vertex not in self.vertices:
            self.vertices[vertex] = {
                "edges": {},
                "position_x": position_x,
                "position_y": position_y,
            }

    def add_edge(self, from_vertex: str, to_vertex: str, weight: float) -> None:
        if from_vertex not in self.vertices or to_vertex not in self.vertices:
            return

        self.vertices[from_vertex]["edges"][to_vertex] = weight

    def display_dijkstra(
        self, start_vertex: str, end_vertex: str
    ) -> Tuple[float, List[str]]:
        headers: list[str] = ["V"] + list(self.vertices.keys())
        table: list[str] = []

        distances: Dict[str, float] = {vertex: float("inf") for vertex in self.vertices}
        distances[start_vertex] = 0

        previous_vertices: Dict[str, None | float] = {
            vertex: None for vertex in self.vertices
        }

        unvisited: list[str] = list(self.vertices.keys())

        count: int = 0
        while unvisited:
            current_vertex: str = min(unvisited, key=lambda vertex: distances[vertex])

            if distances[current_vertex] == float("inf"):
                break

            for neighbor in self.vertices[current_vertex]["edges"].keys():
                new_distance: float = (
                    distances[current_vertex]
                    + self.vertices[current_vertex]["edges"][neighbor]
                )

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_vertices[neighbor] = current_vertex

            table.append(
                [f"{current_vertex}\n(step {count})"]
                + [
                    (
                        (
                            (
                                (
                                    f"{distances[vertex]}"
                                    + (
                                        f" ({previous_vertices[vertex]})"
                                        if previous_vertices[vertex] != None
                                        else ""
                                    )
                                )
                                if vertex != current_vertex
                                else (
                                    "\033[93m"
                                    + (
                                        f"{distances[vertex]}"
                                        + (
                                            f" ({previous_vertices[vertex]})"
                                            if previous_vertices[vertex] != None
                                            else ""
                                        )
                                    )
                                    + "\033[0m"
                                )
                            )
                            if vertex in unvisited
                            else ""
                        )
                        if distances[vertex] != float("inf")
                        else "∞"
                    )
                    for vertex in self.vertices
                ]
            )

            print(f"Langkah {count} - Vertex yang Sedang Dikunjugi: {current_vertex}")
            print(
                tabulate(
                    table,
                    headers=headers,
                    tablefmt="fancy_grid",
                    colalign=(
                        "center",
                        "center",
                        "center",
                        "center",
                        "center",
                        "center",
                        "center",
                        "center",
                    ),
                )
            )
            print()

            unvisited.remove(current_vertex)
            count += 1

        if end_vertex is None:
            return distances

        path: list[str] = []
        current_vertex = end_vertex
        while current_vertex is not None:
            path.insert(0, current_vertex)
            current_vertex = previous_vertices[current_vertex]

        return distances[end_vertex], (
            path if distances[end_vertex] != float("inf") else (float("inf"), [])
        )

    def visualize_graph(
        self, start_vertex: str, end_vertex: str, path: List[str]
    ) -> None:
        G: nx.DiGraph = nx.DiGraph()
        for vertex in self.vertices.keys():
            for edge in self.vertices[vertex]["edges"].keys():
                G.add_edge(vertex, edge, weight=self.vertices[vertex]["edges"][edge])

        plt.figure(figsize=(15, 5))

        position: Dict[str, Tuple[int, int]] = {}
        for vertex in self.vertices:
            position[vertex] = (
                self.vertices[vertex]["position_x"],
                self.vertices[vertex]["position_y"],
            )

        layout = position or nx.spring_layout(G, seed=42)
        label_edge = nx.get_edge_attributes(G, "weight")
        node_color: List[str] = []
        for node in G.nodes:
            if node == start_vertex:
                node_color.append("yellow")

            elif node == end_vertex:
                node_color.append("red")

            else:
                node_color.append("lightblue")

        plt.subplot(121)
        plt.title("Proses Sebelum Dijkstra")
        nx.draw(
            G,
            pos=layout,
            with_labels=True,
            node_color=node_color,
            node_size=2000,
            font_size=9,
            font_weight="bold",
            edge_color="gray",
            width=2,
        )
        nx.draw_networkx_edge_labels(
            G, pos=layout, edge_labels=label_edge, font_size=10
        )

        edge_list: List[Tuple[str, str]] = []
        for vertex in path:
            if path.index(vertex) == 0:
                continue

            edge_list.append((path[path.index(vertex) - 1], vertex))

        plt.subplot(122)
        plt.title("Proses Setelah Dijkstra")
        nx.draw(
            G,
            pos=layout,
            with_labels=True,
            node_color=node_color,
            node_size=2000,
            font_size=9,
            font_weight="bold",
            edge_color="gray",
            width=2,
        )
        nx.draw_networkx_edges(
            G, pos=layout, edgelist=edge_list, edge_color="red", width=3
        )
        nx.draw_networkx_nodes(
            G, pos=layout, nodelist=[end_vertex], node_color="red", node_size=2000
        )
        nx.draw_networkx_edge_labels(
            G, pos=layout, edge_labels=label_edge, font_size=10
        )

        plt.tight_layout()
        plt.show()


dijkstra_kelas_a_kelompok_2_soal_2: Dijkstra_Graph = Dijkstra_Graph()
dijkstra_kelas_a_kelompok_2_soal_2.add_vertex("Perum Kariangau", 0, -1)
dijkstra_kelas_a_kelompok_2_soal_2.add_vertex("WR", 0, 2)
dijkstra_kelas_a_kelompok_2_soal_2.add_vertex("Pawon", 1, 0)
dijkstra_kelas_a_kelompok_2_soal_2.add_vertex("Bang John", 1, 1)
dijkstra_kelas_a_kelompok_2_soal_2.add_vertex("Boyolali", 2, 1)
dijkstra_kelas_a_kelompok_2_soal_2.add_vertex("Riski", 3, 0)
dijkstra_kelas_a_kelompok_2_soal_2.add_vertex("Labter 2", 2, 2)

dijkstra_kelas_a_kelompok_2_soal_2.add_edge("Perum Kariangau", "WR", 16)
dijkstra_kelas_a_kelompok_2_soal_2.add_edge("Perum Kariangau", "Pawon", 6)
dijkstra_kelas_a_kelompok_2_soal_2.add_edge("Pawon", "WR", 11)
dijkstra_kelas_a_kelompok_2_soal_2.add_edge("Pawon", "Bang John", 6)
dijkstra_kelas_a_kelompok_2_soal_2.add_edge("Pawon", "Boyolali", 14)
dijkstra_kelas_a_kelompok_2_soal_2.add_edge("Pawon", "Riski", 10)
dijkstra_kelas_a_kelompok_2_soal_2.add_edge("Bang John", "WR", 4)
dijkstra_kelas_a_kelompok_2_soal_2.add_edge("Bang John", "Labter 2", 8)
dijkstra_kelas_a_kelompok_2_soal_2.add_edge("WR", "Labter 2", 3)
dijkstra_kelas_a_kelompok_2_soal_2.add_edge("Boyolali", "Labter 2", 2)
dijkstra_kelas_a_kelompok_2_soal_2.add_edge("Riski", "Boyolali", 3)

start: str = "Perum Kariangau"
end: str = "Labter 2"
distance, path = dijkstra_kelas_a_kelompok_2_soal_2.display_dijkstra(start, end)

formatted_path: str = " -> ".join(map(lambda text: f"'{text}'", path))

print(
    f"Rute terdekat dari '{start}' ke '{end}' adalah {formatted_path} dengan jarak {distance}"
)

dijkstra_kelas_a_kelompok_2_soal_2.visualize_graph(start, end, path)
