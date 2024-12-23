import networkx as nx
from matplotlib import pyplot as plt
from tabulate import tabulate


class Dijkstra:
    """
    Kelas untuk implementasi algoritma Dijkstra
    Algoritma ini digunakan untuk mencari jalur terpendek antara dua titik dalam graf
    """

    def __init__(self, graph):
        # Memastikan parameter graph adalah instance dari kelas Graph
        if not isinstance(graph, Graph):
            raise Exception("Graph must be an instance of the Graph class.")

        # Inisialisasi atribut-atribut yang diperlukan
        self.graph = graph
        self.distances = {}  # Menyimpan jarak terpendek ke setiap vertex
        self.previous = {}  # Menyimpan vertex sebelumnya dalam jalur terpendek
        self.visited = set()  # Menyimpan vertex yang sudah dikunjungi
        self.paths = {}  # Menyimpan jalur ke setiap vertex
        self.table_data = []  # Menyimpan data untuk ditampilkan dalam bentuk tabel
        self.node_weights = {}  # Menyimpan bobot setiap node

    def find_path(self, start, finish):
        """
        Mencari jalur terpendek dari vertex awal ke vertex tujuan
        menggunakan algoritma Dijkstra
        """

        # Inisialisasi nilai awal
        self.__initialize(start)

        # Selama masih ada vertex yang belum dikunjungi
        while self.visited != set(self.graph.get_vertices()):
            # Pilih vertex dengan jarak terpendek yang belum dikunjungi
            current_vertex = min(
                (v for v in self.distances if v not in self.visited),
                key=lambda x: (self.distances[x], -len(self.paths[x])),
            )

            # Periksa semua tetangga dari vertex saat ini
            for edge in self.graph.get_edges()[current_vertex]:
                neighbor, weight = edge["to"], edge["weight"]

                # Hitung jarak baru ke tetangga melalui vertex saat ini
                new_distance = self.distances[current_vertex] + weight

                # Jika ditemukan jalur yang lebih pendek
                if new_distance < self.distances[neighbor]:
                    # Perbarui jarak, vertex sebelumnya, dan jalur
                    self.distances[neighbor] = new_distance
                    self.previous[neighbor] = current_vertex
                    self.paths[neighbor] = self.paths[current_vertex] + [neighbor]

                    # Perbarui bobot node
                    self.node_weights[neighbor] = (
                        self.node_weights.get(current_vertex, 0) + 1
                    )

            # Tandai vertex saat ini sebagai sudah dikunjungi
            self.visited.add(current_vertex)

            # Catat informasi untuk tabel
            self.__record_table(current_vertex)

        # Kembalikan hasil dalam format yang mudah dibaca
        return self.__format_path(start, finish)

    def visualize_graph(self, finish, positions=None):
        """
        Membuat visualisasi graf menggunakan matplotlib
        Menampilkan dua gambar: graf awal dan graf dengan jalur terpendek
        """

        # Buat graf menggunakan networkx
        G = self.__build_nx_graph()
        plt.figure(figsize=(15, 5))

        # Atur posisi node-node dalam graf
        layout = positions or nx.spring_layout(G, seed=42)
        edge_labels = nx.get_edge_attributes(G, "weight")

        # Gambar graf sebelum algoritma Dijkstra
        plt.subplot(121)
        plt.title("Grafik Sebelum Dijkstra")
        nx.draw(G, pos=layout, with_labels=True, node_color="lightblue")
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels)

        # Gambar graf setelah algoritma Dijkstra
        plt.subplot(122)
        plt.title("Graph Setelah Dijkstra")
        shortest_path = self.__get_shortest_path_edges(finish)
        nx.draw(G, pos=layout, with_labels=True, node_color="lightgreen")
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels)

        # Tandai jalur terpendek dengan warna merah
        nx.draw_networkx_edges(
            G, pos=layout, edgelist=shortest_path, edge_color="red", width=2
        )
        nx.draw_networkx_nodes(G, pos=layout, nodelist=[finish], node_color="red")

        plt.tight_layout()
        plt.show()

    def __initialize(self, start):
        """
        Menyiapkan nilai awal untuk algoritma Dijkstra
        """

        # Atur jarak awal ke semua vertex menjadi tak hingga
        self.distances = {v: float("inf") for v in self.graph.get_vertices()}

        # Atur vertex sebelumnya untuk semua vertex menjadi None
        self.previous = {v: None for v in self.graph.get_vertices()}

        # Bersihkan kumpulan vertex yang sudah dikunjungi
        self.visited = set()

        # Siapkan jalur kosong untuk setiap vertex
        self.paths = {v: [] for v in self.graph.get_vertices()}

        # Bersihkan data tabel
        self.table_data = []

        # Atur jarak ke vertex awal menjadi 0
        self.distances[start] = 0

    def __record_table(self, current_vertex):
        """
        Mencatat informasi untuk ditampilkan dalam bentuk tabel
        Informasi berisi vertex yang dikunjungi dan jarak terkini ke semua vertex
        """

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
        """
        Menyusun hasil pencarian jalur dalam format yang mudah dibaca
        Menampilkan tabel proses dan jalur terpendek yang ditemukan
        """

        # Susun jalur dari finish ke start
        path = []
        current = finish
        while current:
            path.insert(0, current)
            current = self.previous[current]

        # Buat tabel dengan format yang rapi
        table = tabulate(
            self.table_data,
            headers=["Dikunjungi"] + self.graph.get_vertices(),
            tablefmt="fancy_grid",
        )

        return f"{table}\n\nJalur Terpendek: {' -> '.join(path)}"

    def __build_nx_graph(self):
        """
        Membuat objek graf NetworkX dari data graf yang ada
        Digunakan untuk keperluan visualisasi dengan matplotlib
        """

        # Buat objek DirectedGraph (graf berarah) kosong dari NetworkX
        G = nx.DiGraph()

        # Iterasi setiap vertex dalam graf
        for vertex in self.graph.get_vertices():
            # Iterasi setiap edge yang berawal dari vertex tersebut
            for edge in self.graph.get_edges()[vertex]:
                # Tambahkan edge ke graf NetworkX dengan bobotnya
                # vertex: titik asal
                # edge["to"]: titik tujuan
                # weight: bobot/jarak edge
                G.add_edge(vertex, edge["to"], weight=edge["weight"])

        return G

    def __get_shortest_path_edges(self, finish):
        """
        Mendapatkan daftar edge (pasangan vertex) yang membentuk jalur terpendek
        Digunakan untuk mewarnai jalur terpendek dalam visualisasi

        Parameters:
            finish: vertex tujuan yang ingin dicari jalur terpendeknya

        Returns:
            path: list berisi tuple (vertex_asal, vertex_tujuan) yang membentuk jalur terpendek
        """

        # Inisialisasi list kosong untuk menyimpan edge-edge jalur terpendek
        path = []

        # Mulai dari vertex tujuan
        current = finish

        # Telusuri balik jalur dari finish ke start menggunakan informasi vertex sebelumnya
        while self.previous[current]:
            # Tambahkan edge (vertex_sebelumnya, vertex_saat_ini) ke dalam path
            path.append((self.previous[current], current))
            # Pindah ke vertex sebelumnya
            current = self.previous[current]

        return path


class Graph:
    """
    Kelas untuk merepresentasikan graf berarah dengan bobot
    Graf ini menyimpan vertex (titik) dan edge (garis) dengan bobotnya
    """

    def __init__(self):
        # Inisialisasi list vertex dan dictionary edges kosong
        self.__vertices = []
        self.__edges = {}

    def get_vertices(self):
        """Mengembalikan daftar vertex dalam graf"""

        return self.__vertices

    def get_edges(self):
        """Mengembalikan daftar edge dalam graf"""

        return self.__edges

    def add_vertex(self, *vertices):
        """
        Menambahkan satu atau lebih vertex ke dalam graf
        Akan menimbulkan error jika vertex sudah ada dalam graf
        """

        for vertex in vertices:
            if vertex in self.__vertices:
                raise Exception(f"Vertex {vertex} sudah ada dalam graf.")

            self.__vertices.append(vertex)
            self.__edges[vertex] = []

    def add_edge(self, from_vertex, to_vertex, weight):
        """
        Menambahkan edge berarah dengan bobot ke dalam graf
        from_vertex: vertex asal
        to_vertex: vertex tujuan
        weight: bobot/jarak edge
        """

        if from_vertex not in self.__vertices or to_vertex not in self.__vertices:
            raise Exception(
                "Edge tidak valid. Satu atau lebih vertex tidak ada dalam graf."
            )

        self.__edges[from_vertex].append({"to": to_vertex, "weight": weight})

    def __str__(self):
        """Mengembalikan representasi string dari graf"""

        return str(self.__edges)


# Program utama
if __name__ == "__main__":
    # Buat objek graf baru
    graph = Graph()

    # Tambahkan vertex-vertex yang merepresentasikan lokasi
    graph.add_vertex(
        "Perum Kariangau", "WR", "Pawon", "Bang John", "Boyolali", "Riski", "Labter 2"
    )

    # Tambahkan edge-edge dengan bobot yang merepresentasikan jarak antar lokasi
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

    # Buat objek Dijkstra dan cari jalur terpendek
    dijkstra = Dijkstra(graph)
    result = dijkstra.find_path("Perum Kariangau", "Labter 2")
    print(result)

    # Tentukan posisi vertex untuk visualisasi
    graph_positions = {
        "Perum Kariangau": (0, -1),
        "WR": (0, 2),
        "Pawon": (1, 0),
        "Bang John": (1, 1),
        "Boyolali": (2, 1),
        "Riski": (3, 0),
        "Labter 2": (2, 2),
    }

    # Tampilkan visualisasi graf
    dijkstra.visualize_graph("Labter 2", positions=graph_positions)
