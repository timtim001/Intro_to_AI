import numpy as np
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class SumofGaussians:
    def __init__(self, dimensions, number_of_centers, rng):
        if dimensions < 1 or number_of_centers < 1:
            self.centers = None
            return
        self.centers = np.array([rng.uniform(0, 10, dimensions) for _ in range(number_of_centers)])

    def evaluate(self, point):
        return np.sum(np.exp(-np.sum((point - self.centers) ** 2.0, axis=1)))

    def gradient(self, point):
        return np.sum(-1.0 * np.exp(-np.sum((point - self.centers) ** 2.0, axis=1))[:, np.newaxis] * 2.0 * (point - self.centers), axis=0)

def annealing_schedule(t):
    return 1.0 / (1.0 + t) # iverse t+1 which will lower temp when given a higher input

def metropolis_criterion(energy_diff, temperature, rng):
    return energy_diff < 0 or rng.random() < np.exp(-energy_diff / temperature) #returns true if G(y) > G(x) or e ^ (G(y)-G(x)/t)

def main():
    seed = int(sys.argv[1])
    dims = int(sys.argv[2])
    ncenters = int(sys.argv[3])

    rng = np.random.default_rng(seed)
    sog = SumofGaussians(dims, ncenters, rng)

    max_iterations = 100000
    epsilon = 0.05
    current_point = rng.uniform(0, 10, dims)
    current_energy = sog.evaluate(current_point)

    # Lists to store optimization path for plotting
    path_x, path_y, path_z = [], [], []

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(max_iterations):
        temperature = annealing_schedule(i)
        new_point = current_point + epsilon * rng.uniform(-0.05, 0.05, dims)
        new_energy = sog.evaluate(new_point)

        if metropolis_criterion(new_energy - current_energy, temperature, rng):
            current_point = new_point
            current_energy = new_energy

        # Append current point to the path
        path_x.append(current_point[0])
        path_y.append(current_point[1])
        path_z.append(current_energy)

        print(f"{current_point} {current_energy:.8f}")

    print("Simulated Annealing finished.")

    # Plot optimization path
    ax.plot(path_x, path_y, path_z, c='b', marker='o', linestyle='-', label='Optimization Path')

    # Customize the plot
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Value')
    ax.set_title('Simulated Annealing Optimization')
    ax.legend()
    ax.grid()

    # Annotate the final point
    ax.text(path_x[-1], path_y[-1], path_z[-1], f'Final Point\n({path_x[-1]:.2f}, {path_y[-1]:.2f}, {path_z[-1]:.2f})', fontsize=12)

    plt.show()

if __name__ == "__main__":
    main()

