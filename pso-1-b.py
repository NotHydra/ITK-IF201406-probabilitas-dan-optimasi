import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from tabulate import tabulate


class PSO_Single_Variable:
    def __init__(
        self,
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
    ):
        self.fitness_function = fitness_function
        self.parameter_minimum = parameter_minimum
        self.parameter_maximum = parameter_maximum
        self.particle_amount = particle_amount
        # self.particle_amount = 3
        self.c1 = c1
        self.c2 = c2
        self.r_minimum = r_minimum
        # self.r_minimum = 0.5
        self.r_maximum = r_maximum
        # self.r_maximum = 0.5
        self.w = w
        self.iteration_amount = iteration_amount
        # self.iteration_amount = 3

        self.x = [
            [
                round(
                    np.random.uniform(self.parameter_minimum, self.parameter_maximum), 4
                )
            ]
            for _ in range(self.particle_amount)
        ]
        # self.x = [[0], [0.5], [1]]
        self.v = [[0] for _ in range(self.particle_amount)]

        self.p_best = [[] for _ in range(self.particle_amount)]
        self.g_best = []

    def execute_fitness_function(self, x):
        return round(self.fitness_function(x), 4)

    def get_latest_p_best(self):
        return list(map(lambda arr: arr[-1], self.p_best))

    def get_latest_fitness_of_p_best(self):
        return list(map(self.execute_fitness_function, self.get_latest_p_best()))

    def get_best_value_latest_fitness_of_p_best(self):
        return min(self.get_latest_fitness_of_p_best())

    def get_latest_g_best(self):
        return self.g_best[-1]

    def get_latest_fitness_of_g_best(self):
        return self.execute_fitness_function(self.get_latest_g_best())

    def set_latest_g_best(self):
        if len(self.g_best) == 0:
            self.g_best.append(
                self.get_latest_p_best()[np.argmin(self.get_latest_fitness_of_p_best())]
            )

        else:
            if (self.get_latest_fitness_of_g_best()) <= (
                self.get_best_value_latest_fitness_of_p_best()
            ):
                self.g_best.append(
                    self.get_latest_p_best()[
                        np.argmin(self.get_latest_fitness_of_p_best())
                    ]
                )

            else:
                self.g_best.append(self.get_latest_g_best())

    def optimize(self):
        for t in range(self.iteration_amount):
            for i in range(self.particle_amount):

                if len(self.p_best[i]) == 0:
                    self.p_best[i].append(self.x[i][-1])

                else:
                    if (self.execute_fitness_function(self.p_best[i][-1])) <= (
                        self.execute_fitness_function(self.x[i][-1])
                    ):
                        self.p_best[i].append(self.p_best[i][-1])

                    else:
                        self.p_best[i].append(self.x[i][-1])

            self.set_latest_g_best()

            for i in range(self.particle_amount):
                r1 = round(np.random.uniform(self.r_minimum, self.r_maximum), 4)
                r2 = round(np.random.uniform(self.r_minimum, self.r_maximum), 4)

                self.v[i].append(
                    np.clip(
                        (
                            (self.w * self.v[i][-1])
                            + (self.c1 * r1 * (self.p_best[i][-1] - self.x[i][-1]))
                            + (self.c2 * r2 * (self.g_best[-1] - self.x[i][-1]))
                        ),
                        self.parameter_minimum,
                        self.parameter_maximum,
                    )
                )

                self.x[i].append(
                    np.clip(
                        (self.x[i][-1] + self.v[i][-1]),
                        self.parameter_minimum,
                        self.parameter_maximum,
                    )
                )

    def show_table(self):
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
                        self.execute_fitness_function(self.g_best[t]),
                        self.x[i][t + 1],
                        self.v[i][t + 1],
                    ]
                )

                first_row = False

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
        fig, ax = plt.subplots()
        ax.set_title("Pergerakan Partikel")
        ax.set_xlabel("Iterasi")
        ax.set_ylabel("Posisi Partikel")

        ax.set_xlim(
            0 - round(self.iteration_amount * 0.2),
            self.iteration_amount + round(self.iteration_amount * 0.2),
        )
        ax.set_ylim(self.parameter_minimum, self.parameter_maximum)

        lines = []
        for i in range(self.particle_amount):
            (line,) = ax.plot(
                [0],
                [self.x[i][0]],
                label=f"Partikel {i + 1}",
            )

            lines.append(line)

        (line_g_best,) = ax.plot(
            [0],
            [self.g_best[0]],
            linestyle="--",
            color="black",
            label="gBest",
        )

        def update(frame):
            for i in range(self.particle_amount):
                lines[i].set_data(list(range(frame + 1)), self.x[i][: frame + 1])

            line_g_best.set_data(list(range(frame + 1)), self.g_best[: frame + 1])

            return lines

        ani = FuncAnimation(
            fig,
            update,
            frames=range(self.iteration_amount + 1),
            interval=25,
            blit=True,
        )

        plt.legend()
        plt.show()


fitness_function = lambda x: (3 * (x**2) + (2 * x) - 2) ** 2
parameter_minimum = -2
parameter_maximum = 2
particle_amount = 10
c1 = 0.5
c2 = 1
r_minimum = 0.5
r_maximum = 0.5
w = 1
iteration_amount = 100

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
