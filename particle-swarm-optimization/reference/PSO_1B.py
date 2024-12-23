import numpy as np
import matplotlib.pyplot as plt

from tabulate import tabulate


class PSO_SingleVariable:
    def __init__(self, num_particles, num_iterations, c1, c2, w, x_min, x_max):
        self.num_particles = num_particles
        self.num_iterations = num_iterations
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.x_min = x_min
        self.x_max = x_max

        # Inisialisasi posisi dan kecepatan partikel
        self.x = np.random.uniform(self.x_min, self.x_max, self.num_particles)
        self.v = np.zeros(self.num_particles)
        self.pbest = self.x.copy()  # Personal best (pBest) untuk setiap partikel
        self.gbest = self.x[np.argmin(self.function(self.x))]  # Global best (gBest)

        # Penyimpanan hasil per iterasi
        self.history = []  # Untuk menyimpan data per partikel
        self.gbest_history = []  # Untuk menyimpan nilai gBest setiap iterasi

    @staticmethod
    def function(x):
        """Fungsi tujuan untuk optimasi."""
        return 3 * x**2 + 2 * x - 2

    def findPBest(self, i):
        """Memperbarui nilai pBest untuk partikel ke-i."""
        if self.function(self.x[i]) < self.function(self.pbest[i]):
            self.pbest[i] = self.x[i]

    def findGBest(self):
        """Memperbarui nilai gBest berdasarkan pBest terbaik."""
        self.gbest = self.pbest[np.argmin(self.function(self.pbest))]

    def optimize(self):
        """Proses iterasi PSO."""
        for t in range(self.num_iterations):
            for i in range(self.num_particles):
                # Generate nilai acak r1 dan r2 untuk setiap partikel di iterasi ini
                r1 = np.random.uniform(0, 1)
                r2 = np.random.uniform(0, 1)

                # Update kecepatan partikel
                self.v[i] = (
                    self.w * self.v[i]
                    + self.c1 * r1 * (self.pbest[i] - self.x[i])
                    + self.c2 * r2 * (self.gbest - self.x[i])
                )
                
                # Batasi kecepatan (velocity clamping) jika diperlukan
                self.v[i] = np.clip(self.v[i], -2, 2)

                # Update posisi partikel
                self.x[i] += self.v[i]
                self.x[i] = np.clip(self.x[i], self.x_min, self.x_max)  # Batasi posisi

                # Update pBest untuk partikel ini
                self.findPBest(i)

            # Update gBest setelah semua partikel diperbarui
            self.findGBest()
            self.gbest_history.append(self.gbest)

            # Simpan data setiap iterasi untuk semua partikel
            for i in range(self.num_particles):
                self.history.append(
                    [
                        t + 1,  # Iterasi ke-t
                        i + 1,  # Partikel ke-i
                        self.x[i],  # Posisi xi
                        self.function(self.x[i]),  # Nilai fitness f(xi)
                        self.pbest[i],  # pBest
                        self.gbest,  # gBest
                        self.v[i],  # Kecepatan v
                    ]
                )

    def display_results(self):
        """Menampilkan hasil optimasi dalam bentuk tabel."""
        headers = ["Iterasi", "Partikel", "Posisi xi", "f(xi)", "pBest", "gBest", "v"]
        table = []
        current_iter = None  # Untuk menyimpan iterasi yang sedang diproses

        for data in self.history:
            iterasi = data[0]
            if iterasi != current_iter:
                current_iter = iterasi
                table.append(
                    [
                        iterasi,  # Iterasi ditampilkan hanya sekali
                        data[1],  # Partikel ke-i
                        f"{data[2]:.4f}",  # Posisi xi
                        f"{data[3]:.4f}",  # Fitness f(xi)
                        f"{data[4]:.4f}",  # pBest
                        f"{data[5]:.4f}",  # gBest
                        f"{data[6]:.4f}",  # Kecepatan v
                    ]
                )
            else:
                table.append(
                    [
                        "",  # Iterasi dikosongkan untuk baris berikutnya
                        data[1],
                        f"{data[2]:.4f}",
                        f"{data[3]:.4f}",
                        f"{data[4]:.4f}",
                        f"{data[5]:.4f}",
                        f"{data[6]:.4f}",
                    ]
                )

        print(
            tabulate(
                table,
                headers=headers,
                tablefmt="fancy_grid",
                colalign=(
                    "center",
                    "center",
                    "left",
                    "center",
                    "center",
                    "center",
                    "center",
                ),
            )
        )

    def plot_results(self):
        """Memvisualisasikan hasil optimasi."""
        plt.figure(figsize=(10, 6))

        # Plot pergerakan setiap partikel
        for i in range(self.num_particles):
            plt.plot(
                range(1, self.num_iterations + 1),
                [data[2] for data in self.history if data[1] == i + 1],
                label=f"Partikel {i+1}",
            )

        # Plot nilai gBest
        plt.plot(
            range(1, self.num_iterations + 1),
            self.gbest_history,
            linestyle="--",
            color="black",
            label="gBest",
        )
        plt.xlabel("Iterasi")
        plt.ylabel("Posisi Partikel")
        plt.title("Pergerakan Partikel Selama Iterasi PSO")
        plt.legend()
        plt.grid()
        plt.show()


# Parameter PSO
num_particles = 10
num_iterations = 100
c1 = 1.5
c2 = 1.5
w = 1
x_min, x_max = -2, 2

# Menjalankan PSO
pso = PSO_SingleVariable(num_particles, num_iterations, c1, c2, w, x_min, x_max)
pso.optimize()
pso.display_results()
pso.plot_results()
