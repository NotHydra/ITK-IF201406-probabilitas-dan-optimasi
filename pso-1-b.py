import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from tabulate import tabulate


class PSO_Single_Variable:
    def __init__(
        self,
        fitness_function,  # Fungsi objektif yang akan dioptimasi/diminimalkan
        parameter_minimum,  # Batas minimal untuk pencarian solusi
        parameter_maximum,  # Batas maksimal untuk pencarian solusi
        particle_amount,  # Jumlah partikel dalam swarm (populasi)
        c1,  # Koefisien kognitif (learning rate personal/individu)
        c2,  # Koefisien sosial (learning rate global)
        r_minimum,  # Batas minimal bilangan acak untuk eksplorasi
        r_maximum,  # Batas maksimal bilangan acak untuk eksplorasi
        w,  # Faktor inersia untuk mengontrol dampak kecepatan sebelumnya
        iteration_amount,  # Total iterasi yang akan dilakukan dalam optimasi
    ):
        # Simpan parameter-parameter algoritma PSO untuk digunakan selama proses optimasi

        # Fungsi fitness yang menentukan kualitas solusi
        # Semakin rendah nilainya, semakin baik solusinya
        self.fitness_function = fitness_function

        # Batasan ruang pencarian solusi untuk mencegah partikel keluar dari rentang yang valid
        self.parameter_minimum = parameter_minimum
        self.parameter_maximum = parameter_maximum

        # Jumlah agen/partikel yang akan bergerak mencari solusi optimal
        # Semakin banyak partikel, semakin komprehensif pencarian
        self.particle_amount = particle_amount

        # Koefisien yang mengontrol pengaruh memori pribadi (c1) dan sosial (c2)
        # c1: seberapa kuat partikel mengikuti posisi terbaik pribadinya
        # c2: seberapa kuat partikel mengikuti posisi terbaik global
        self.c1 = c1
        self.c2 = c2

        # Rentang bilangan acak untuk memberikan variasi dan eksplorasi
        # Membantu partikel tidak terjebak di solusi lokal
        self.r_minimum = r_minimum
        self.r_maximum = r_maximum

        # Faktor inersia untuk mengontrol momentum partikel
        # Mengatur keseimbangan antara eksplorasi dan eksploitasi
        self.w = w

        # Total iterasi atau generasi dalam proses optimasi
        # Menentukan berapa lama algoritma mencari solusi optimal
        self.iteration_amount = iteration_amount

        # Inisialisasi posisi awal partikel secara acak dalam rentang parameter
        # Setiap partikel memulai dari posisi yang berbeda untuk diversitas
        self.x = [
            [
                round(
                    np.random.uniform(self.parameter_minimum, self.parameter_maximum), 4
                )
            ]
            for _ in range(self.particle_amount)
        ]

        # Inisialisasi kecepatan awal semua partikel dengan 0
        # Partikel mulai dari kondisi diam sebelum bergerak
        self.v = [[0] for _ in range(self.particle_amount)]

        # Struktur untuk menyimpan posisi terbaik pribadi setiap partikel
        # Memungkinkan pelacakan pencapaian terbaik setiap partikel
        self.p_best = [[] for _ in range(self.particle_amount)]

        # Struktur untuk menyimpan posisi terbaik global dari seluruh swarm
        # Akan diperbarui setiap iterasi jika ditemukan solusi lebih baik
        self.g_best = []

    def execute_fitness_function(self, x):
        # Menjalankan fungsi fitness dengan pembulatan hasil
        # Memastikan konsistensi presisi dalam perhitungan
        return round(self.fitness_function(x), 4)

    def get_latest_p_best(self):
        # Mengambil posisi terbaik personal terbaru dari setiap partikel
        # Berguna untuk membandingkan dan memperbarui solusi
        return list(map(lambda arr: arr[-1], self.p_best))

    def get_latest_fitness_of_p_best(self):
        # Menghitung nilai fitness dari posisi terbaik personal terbaru
        # Membantu dalam mengevaluasi kualitas solusi individu
        return list(map(self.execute_fitness_function, self.get_latest_p_best()))

    def get_best_value_latest_fitness_of_p_best(self):
        # Menemukan nilai fitness terbaik dari posisi personal terbaik
        # Digunakan untuk membandingkan dengan solusi global
        return min(self.get_latest_fitness_of_p_best())

    def get_latest_g_best(self):
        # Mengambil posisi terbaik global terbaru
        # Solusi terbaik yang ditemukan oleh seluruh swarm
        return self.g_best[-1]

    def get_latest_fitness_of_g_best(self):
        # Menghitung nilai fitness dari posisi terbaik global
        # Mengukur kualitas solusi terbaik keseluruhan
        return self.execute_fitness_function(self.get_latest_g_best())

    def set_latest_g_best(self):
        # Proses pemilihan dan pembaruan posisi terbaik global
        if len(self.g_best) == 0:
            # Pada iterasi pertama, pilih partikel dengan fitness terbaik
            self.g_best.append(
                self.get_latest_p_best()[np.argmin(self.get_latest_fitness_of_p_best())]
            )
        else:
            # Pada iterasi selanjutnya, perbarui g_best jika ditemukan solusi lebih baik
            if (self.get_latest_fitness_of_g_best()) <= (
                self.get_best_value_latest_fitness_of_p_best()
            ):
                # Pilih partikel dengan fitness terbaik sebagai g_best
                self.g_best.append(
                    self.get_latest_p_best()[
                        np.argmin(self.get_latest_fitness_of_p_best())
                    ]
                )
            else:
                # Pertahankan g_best sebelumnya jika tidak ada perbaikan
                self.g_best.append(self.get_latest_g_best())

    def optimize(self):
        # Algoritma utama Particle Swarm Optimization
        # Melakukan iterasi untuk mengeksplorasi dan mengeksploitasi ruang solusi
        for t in range(self.iteration_amount):
            # Fase 1: Update Personal Best (pBest)
            for i in range(self.particle_amount):
                if len(self.p_best[i]) == 0:
                    # Inisialisasi pBest untuk partikel pada iterasi pertama
                    self.p_best[i].append(self.x[i][-1])
                else:
                    # Perbarui pBest jika posisi saat ini memiliki fitness lebih baik
                    if (self.execute_fitness_function(self.p_best[i][-1])) <= (
                        self.execute_fitness_function(self.x[i][-1])
                    ):
                        # Pertahankan pBest sebelumnya
                        self.p_best[i].append(self.p_best[i][-1])
                    else:
                        # Update pBest dengan posisi terbaru
                        self.p_best[i].append(self.x[i][-1])

            # Fase 2: Update Global Best (gBest)
            self.set_latest_g_best()

            # Fase 3: Update Kecepatan dan Posisi Partikel
            for i in range(self.particle_amount):
                # Hasilkan bilangan acak untuk memberikan variasi
                # Membantu dalam eksplorasi ruang solusi
                r1 = round(np.random.uniform(self.r_minimum, self.r_maximum), 4)
                r2 = round(np.random.uniform(self.r_minimum, self.r_maximum), 4)

                # Perbarui kecepatan partikel dengan persamaan PSO
                # Kombinasi dari inersia, kognitif, dan komponen sosial
                self.v[i].append(
                    np.clip(
                        (
                            # Inersia: mempertahankan momentum sebelumnya
                            (self.w * self.v[i][-1])
                            # Komponen Kognitif: tarik ke posisi terbaik pribadi
                            + (self.c1 * r1 * (self.p_best[i][-1] - self.x[i][-1]))
                            # Komponen Sosial: tarik ke posisi terbaik global
                            + (self.c2 * r2 * (self.g_best[-1] - self.x[i][-1]))
                        ),
                        # Pastikan kecepatan dalam batas yang diizinkan
                        self.parameter_minimum,
                        self.parameter_maximum,
                    )
                )

                # Perbarui posisi partikel berdasarkan kecepatan baru
                # Pastikan posisi masih dalam rentang parameter
                self.x[i].append(
                    np.clip(
                        (self.x[i][-1] + self.v[i][-1]),
                        self.parameter_minimum,
                        self.parameter_maximum,
                    )
                )

    def show_table(self):
        # Fungsi untuk menampilkan rincian proses optimasi dalam tabel
        # Membantu dalam memahami evolusi setiap partikel
        headers = [
            "Iterasi",
            "Partikel",
            "x",
            "f(x)",
            "v",
            "pBest",
            "f(pBest)",
            "gBest",
            "f(gBest)",
            "Updated x",
            "Updated v",
        ]
        table = []

        # Susun data untuk setiap iterasi dan partikel
        for t in range(self.iteration_amount):
            first_row = True
            for i in range(self.particle_amount):
                table.append(
                    [
                        t + 1 if first_row else "",
                        f"Ke-{i + 1} ({i})",
                        self.x[i][t],
                        self.execute_fitness_function(self.x[i][t]),
                        self.v[i][t],
                        self.p_best[i][t],
                        self.execute_fitness_function(self.p_best[i][t]),
                        self.g_best[t] if first_row else "",
                        (
                            self.execute_fitness_function(self.g_best[t])
                            if first_row
                            else ""
                        ),
                        self.x[i][t + 1],
                        self.v[i][t + 1],
                    ]
                )

                first_row = False

        # Cetak tabel dengan format yang rapi
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
                    "center",
                    "center",
                    "center",
                ),
            )
        )

    def show_plot_per_iteration(self):
        # Fungsi untuk membuat visualisasi animasi pergerakan partikel
        # Membantu memahami dinamika pencarian solusi
        fig, ax = plt.subplots()
        ax.set_title("Pergerakan Partikel dalam Ruang Solusi")
        ax.set_xlabel("Iterasi")
        ax.set_ylabel("Posisi Partikel")

        # Atur batas plot untuk memastikan seluruh pergerakan terlihat
        ax.set_xlim(
            0 - round(self.iteration_amount * 0.2),
            self.iteration_amount + round(self.iteration_amount * 0.2),
        )
        ax.set_ylim(self.parameter_minimum, self.parameter_maximum)

        # Siapkan plot untuk melacak posisi setiap partikel
        lines = []
        for i in range(self.particle_amount):
            (line,) = ax.plot(
                [0],
                [self.x[i][0]],
                label=f"Partikel {i + 1}",
            )

            lines.append(line)

        # Plot garis untuk posisi global terbaik
        (line_g_best,) = ax.plot(
            [0],
            [self.g_best[0]],
            linestyle="--",
            color="black",
            label="Global Best",
        )

        def update(frame):
            # Fungsi update untuk animasi pergerakan
            # Memperbarui posisi setiap partikel pada setiap frame
            for i in range(self.particle_amount):
                lines[i].set_data(list(range(frame + 1)), self.x[i][: frame + 1])

            # Perbarui posisi global terbaik
            line_g_best.set_data(list(range(frame + 1)), self.g_best[: frame + 1])

            return lines

        # Buat animasi dengan interval dan frame yang ditentukan
        ani = FuncAnimation(
            fig,
            update,
            frames=range(self.iteration_amount + 1),
            interval=25,  # Kontrol kecepatan animasi
            blit=True,  # Optimasi performa animasi
        )

        plt.legend()
        plt.show()


# Definisi fungsi fitness untuk dioptimasi
# Dalam kasus ini: f(x) = (3x² + 2x - 2)²
# Fungsi ini memiliki beberapa minimum lokal dan global
fitness_function = lambda x: (3 * (x**2) + (2 * x) - 2) ** 2

# Parameter optimasi PSO yang akan digunakan
parameter_minimum = -2  # Batas minimal pencarian solusi
parameter_maximum = 2  # Batas maksimal pencarian solusi
particle_amount = 10  # Jumlah partikel dalam swarm
c1 = 0.5  # Koefisien kognitif (pengaruh memori pribadi)
c2 = 1  # Koefisien sosial (pengaruh informasi global)
r_minimum = 0  # Batas minimal bilangan acak
r_maximum = 1  # Batas maksimal bilangan acak
w = 1  # Faktor inersia
iteration_amount = 100  # Total iterasi optimasi

# Inisialisasi dan eksekusi algoritma PSO
pso_1_b = PSO_Single_Variable(
    fitness_function,
    parameter_minimum,
    parameter_maximum,
    particle_amount,
    c1,
    c2,
    r_minimum,
    r_maximum,
    w,
    iteration_amount,
)

pso_1_b.optimize()
pso_1_b.show_table()
pso_1_b.show_plot_per_iteration()
