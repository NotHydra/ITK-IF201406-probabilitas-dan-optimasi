import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

class PSO_Multivariable:
    def __init__(self, num_particles, num_iterations, c1, c2, w, x_min, x_max, y_min, y_max):
        self.num_particles = num_particles
        self.num_iterations = num_iterations
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max

        # Inisialisasi posisi (x, y) dan kecepatan (vx, vy)
        self.x = np.random.uniform(self.x_min, self.x_max, self.num_particles)
        self.y = np.random.uniform(self.y_min, self.y_max, self.num_particles)
        self.vx = np.zeros(self.num_particles)
        self.vy = np.zeros(self.num_particles)

        # Inisialisasi personal best (pBest) dan global best (gBest)
        self.pbest_x, self.pbest_y = self.x.copy(), self.y.copy()
        self.pbest_value = self.function(self.x, self.y)
        self.gbest_x = self.x[np.argmin(self.pbest_value)]
        self.gbest_y = self.y[np.argmin(self.pbest_value)]

        # Penyimpanan hasil per iterasi
        self.history = []

    @staticmethod
    def function(x, y):
        """Fungsi tujuan f(x, y)."""
        term1 = (1.25 - x + x * y)**2
        term2 = (2.5 - x + x * y**2)**2
        term3 = (0.5 - x + x * y**3)**2
        return term1 + term2 + term3

    def update_personal_best(self):
        """Memperbarui nilai pBest untuk setiap partikel."""
        current_value = self.function(self.x, self.y)
        mask = current_value < self.pbest_value
        self.pbest_x[mask] = self.x[mask]
        self.pbest_y[mask] = self.y[mask]
        self.pbest_value[mask] = current_value[mask]

    def update_global_best(self):
        """Memperbarui nilai gBest berdasarkan pBest terbaik."""
        min_index = np.argmin(self.pbest_value)
        self.gbest_x = self.pbest_x[min_index]
        self.gbest_y = self.pbest_y[min_index]

    def optimize(self):
        """Proses iterasi PSO."""
        for t in range(self.num_iterations):
            iter_data = []
            for i in range(self.num_particles):
                # Generate nilai acak r1 dan r2
                r1, r2 = np.random.uniform(0, 1, 2)

                # Update kecepatan (vx, vy)
                self.vx[i] = (
                    self.w * self.vx[i]
                    + self.c1 * r1 * (self.pbest_x[i] - self.x[i])
                    + self.c2 * r2 * (self.gbest_x - self.x[i])
                )
                self.vy[i] = (
                    self.w * self.vy[i]
                    + self.c1 * r1 * (self.pbest_y[i] - self.y[i])
                    + self.c2 * r2 * (self.gbest_y - self.y[i])
                )

                # Update posisi (x, y)
                self.x[i] += self.vx[i]
                self.y[i] += self.vy[i]

                # Batasi posisi dalam interval yang diperbolehkan
                self.x[i] = np.clip(self.x[i], self.x_min, self.x_max)
                self.y[i] = np.clip(self.y[i], self.y_min, self.y_max)

                # Simpan data per partikel
                iter_data.append([
                    t + 1,  # Iterasi
                    i + 1,  # Partikel
                    self.x[i],  # Posisi x
                    self.y[i],  # Posisi y
                    self.function(self.x[i], self.y[i]),  # Fitness f(x, y)
                    self.pbest_x[i],  # pBest_x
                    self.pbest_y[i],  # pBest_y
                    self.gbest_x,  # gBest_x
                    self.gbest_y,  # gBest_y
                    self.vx[i],  # Kecepatan vx
                    self.vy[i]  # Kecepatan vy
                ])

            # Update pBest dan gBest
            self.update_personal_best()
            self.update_global_best()

            # Simpan hasil iterasi
            self.history.extend(iter_data)

    def display_results(self):
        """Menampilkan hasil optimasi dalam bentuk tabel."""
        headers = ["Iterasi", "Partikel", "x", "y", "f(x, y)", "pBest_x", "pBest_y", "gBest_x", "gBest_y", "vx", "vy"]
        table = []
        current_iter = None

        for data in self.history:
            iterasi = data[0]
            if iterasi != current_iter:
                current_iter = iterasi
                table.append([
                    iterasi,
                    data[1],
                    f"{data[2]:.4f}",
                    f"{data[3]:.4f}",
                    f"{data[4]:.4f}",
                    f"{data[5]:.4f}",
                    f"{data[6]:.4f}",
                    f"{data[7]:.4f}",
                    f"{data[8]:.4f}",
                    f"{data[9]:.4f}",
                    f"{data[10]:.4f}"
                ])
            else:
                table.append([
                    "",
                    data[1],
                    f"{data[2]:.4f}",
                    f"{data[3]:.4f}",
                    f"{data[4]:.4f}",
                    f"{data[5]:.4f}",
                    f"{data[6]:.4f}",
                    f"{data[7]:.4f}",
                    f"{data[8]:.4f}",
                    f"{data[9]:.4f}",
                    f"{data[10]:.4f}"
                ])

        print(tabulate(table, headers=headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center", "center", "center", "center", "center", "center", "center")))

    def plot_results(self):
        """Memvisualisasikan pergerakan partikel."""
        plt.figure(figsize=(10, 6))
        for i in range(self.num_particles):
            plt.plot(
                range(1, self.num_iterations + 1),
                [data[4] for data in self.history if data[1] == i + 1],
                label=f"Partikel {i+1}"
            )

        plt.plot(
            range(1, self.num_iterations + 1),
            [data[4] for data in self.history[::self.num_particles]],
            linestyle="--", color="black", label="f(gBest)"
        )

        plt.xlabel("Iterasi")
        plt.ylabel("Fitness f(x, y)")
        plt.title("Pergerakan Nilai Fitness Partikel")
        plt.legend()
        plt.grid()
        plt.show()


# Parameter PSO
num_particles = 10
num_iterations = 10
c1 = 1.5
c2 = 1.5
w = 0.7
x_min, x_max = -3.5, 3.5
y_min, y_max = -3.5, 3.5

# Menjalankan PSO
pso = PSO_Multivariable(num_particles, num_iterations, c1, c2, w, x_min, x_max, y_min, y_max)
pso.optimize()
pso.display_results()
pso.plot_results()
