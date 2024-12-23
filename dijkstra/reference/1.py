import time
from copy import copy
from prettytable import PrettyTable


class Dijkstra:
    def __init__(self):
        self.graph = {}
        self.distance = {}
        self.path = {}

        self.start = ""
        self.end = ""

        self.distancewNode = {}
        self.table = PrettyTable()
        self.tableData = []
        self.firstColData = []

    # Menampilkan table
    def showTable(self, i, shortestNode, notVisited):
        self.field = [node for node in self.graph]
        self.table.clear()
        self.table.field_names = self.field

        if i >= len(self.tableData) or i >= len(self.firstColData):
            self.tableData.append([0 for m in range(len(self.graph))])
            self.firstColData.append("-")

        for x, y in self.distancewNode.items():
            if x not in notVisited:
                y = f"\033[31m{y}\033[0m"

            self.tableData[i][self.field.index(x)] = y

        self.table.add_rows(self.tableData[:i])

        self.firstColData[i] = shortestNode

        self.table._field_names.insert(0, "/")
        self.table._align["/"] = "c"
        self.table._valign["/"] = "v"

        for j, x in enumerate(self.table._rows):
            self.table._rows[j].insert(0, self.firstColData[j])

        print(self.table) if i > 0 else ""

    # Menambahkan node/titik baru
    def insertNewNode(self, node):
        if not node.isalpha():
            print("Harap masukan berupa karakter")

            return False

        self.graph[node] = {}

        return True

    # Menambahkan rute/jarak yang dimiliki node/titik ke node/titik lainnya
    def insertNodePath(self, node, path, distance):
        if node in self.graph:
            self.graph[node][path] = distance

            return True

        print(f"Tidak ditemukan Node {node} di dalam graph")

        return False

    # Menginisialisasi jarak rute, titik mulai, dan titik akhir
    def initDistancePath(self, start, end):
        # membuat seluruh nilai distance menjadi infinity (99) kecuali jarak di titik awal, yaitu 0
        for node in self.graph:
            self.distance[node] = 99
            self.path[node] = {}

        self.distance[start] = 0
        self.start = start
        self.end = end
        self.distancewNode = copy(self.distance)

    # Mencari node dengan jarak terpendek
    def findShortestNode(self, notVisited):
        lowestDistance = 99
        shortestNode = ""
        for node in self.distance:
            # jika node ada di dalam variable notVisited dan jarak dari node lebih rendah atau sama dengan dari lowestDistance
            if node in notVisited and self.distance[node] <= lowestDistance:
                lowestDistance = self.distance[node]
                shortestNode = node

        return shortestNode

    # Mencari rute terpendek dari titik awal ke titik akhir
    def route(self, start, end, showAllRoute=False):
        if start not in self.graph:
            print(f"{start} tidak ada di dalam Graph!")

            return

        if end not in self.graph:
            print(f"{end} tidak ada di dalam Graph!")

            return

        if self.graph == {}:
            print("Graph kosong!")

            return ValueError

        self.initDistancePath(start, end)
        notVisited = [node for node in self.distance]
        shortestNode = self.findShortestNode(notVisited)
        i = 0

        # akan melakukan perulangan selama notVisited masih mempunyai nilai
        while notVisited:
            shortestNodeDistance = self.distance[shortestNode]
            destination = self.graph[shortestNode]

            for node in destination:
                # memperbaharui jarak yang dimiliki node dalam variabel distance dan rute yang dimiliki node
                if self.distance[node] > shortestNodeDistance + destination[node]:
                    self.distance[node] = shortestNodeDistance + destination[node]
                    self.distancewNode[node] = f"{self.distance[node]}/{shortestNode}"
                    self.path[node] = shortestNode

            self.showTable(i, shortestNode, notVisited)
            print(f"Menuju ke node {shortestNode}")
            print("")

            notVisited.pop(notVisited.index(shortestNode))
            shortestNode = self.findShortestNode(notVisited)
            i += 1

            time.sleep(0.2)

        self.showTable(i, shortestNode, notVisited)

        # Menampilkan seluruh rute dari titik awal ke seluruh titik yang ada dalam graf jika showAllRoute bernilai True
        if showAllRoute:
            for j, node in enumerate(self.graph):
                i = 0
                self.end = node

                if self.start == self.end:
                    continue

                # Pengkondisian penentuan alur, jika jarak menuju node tujuan lebih dari/sama dengan 99, maka artinya node awal tidak memiliki akses/jalur menuju ke node akhir melalui jalur apapun
                if self.distance[self.end] < 99:
                    # Mencari rute berdasarkan susunan rute terpendek yang telah dihitung
                    pathList = [self.end]
                    while start not in pathList:
                        pathList.append(self.path[pathList[i]])
                        i += 1

                    print(
                        f"{j} - Jarak terpendek dari {start} menuju {self.end} adalah {self.distance[self.end]}"
                    )
                    print(" ", end=" ")
                    print(" -> ".join(reversed(pathList)))

                else:
                    print(
                        f"{j} - Alur tidak ditemukan dari {start} menuju ke {self.end}"
                    )

                return

            # Mencari rute berdasarkan susunan rute terpendek yang telah dihitung
            if self.distance[self.end] < 99:
                pathList = [self.end]
                i = 0

                while start not in pathList:
                    pathList.append(self.path[pathList[i]])
                    i += 1

                print(
                    f"\nJarak terpendek dari {start} menuju {self.end} adalah {self.distance[self.end]}"
                )
                print(" -> ".join(reversed(pathList)))

            else:
                print("\nAlur tidak ditemukan!")

            return


dijkstra = Dijkstra()
dijkstra.insertNewNode("A")
dijkstra.insertNodePath("A", "B", 3)
dijkstra.insertNodePath("A", "C", 10)

dijkstra.insertNewNode("B")
dijkstra.insertNodePath("B", "D", 7)
dijkstra.insertNodePath("B", "E", 3)

dijkstra.insertNewNode("C")
dijkstra.insertNodePath("C", "F", 8)

dijkstra.insertNewNode("D")
dijkstra.insertNodePath("D", "E", 6)
dijkstra.insertNodePath("D", "G", 1)
dijkstra.insertNodePath("D", "H", 4)
dijkstra.insertNodePath("D", "J", 8)

dijkstra.insertNewNode("E")
dijkstra.insertNodePath("E", "I", 7)
dijkstra.insertNodePath("E", "C", 2)

dijkstra.insertNewNode("F")
dijkstra.insertNodePath("F", "I", 6)

dijkstra.insertNewNode("G")
dijkstra.insertNodePath("G", "F", 5)
dijkstra.insertNodePath("G", "I", 2)
dijkstra.insertNodePath("G", "H", 1)

dijkstra.insertNewNode("H")
dijkstra.insertNodePath("H", "J", 2)

dijkstra.insertNewNode("I")
dijkstra.insertNodePath("I", "J", 5)

dijkstra.insertNewNode("J")

dijkstra.route("A", "J")
# dijkstra.route("A", "J", showAllRoute=True)
