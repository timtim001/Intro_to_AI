import numpy as np
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class SumofGaussians:
    def __init__(self, dimensions, number_of_centers, rng):
        if dimensions < 1 or number_of_centers < 1:
            self.centers = None
            return 
        self.centers = np.array([rng.uniform(0, 10, dimensions) for i in range(number_of_centers)])

    def evaluate(self, point):
        return np.sum(np.exp(-np.sum((point - self.centers) ** 2.0, axis=1)))

    def gradient(self, point):
        return np.sum(-1.0 * np.exp(-np.sum((point - self.centers) ** 2.0, axis=1))[:, np.newaxis] * 2.0 * (point - self.centers), axis=0)
def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py <seed> <dims> <ncenters>")
        sys.exit(1)

    seed = int(sys.argv[1])
    dims = int(sys.argv[2])
    ncenters = int(sys.argv[3])

    rng = np.random.default_rng(seed)
    sog = SumofGaussians(dims, ncenters, rng)

    epsilon = 1e-8

    max_iterations = 100000
    step_size = 0.1
    current_point = rng.uniform(0, 10, dims)

    # Lists to store optimization path for plotting
    path_x, path_y, path_z = [], [], []

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot Gaussian centers
    centers = sog.centers
    ax.scatter(centers[:, 0], centers[:, 1], np.zeros(centers.shape[0]), c='r', marker='o', label='Gaussian Centers')

    for i in range(max_iterations):
        sog_value = sog.evaluate(current_point)
        sog_grad = sog.gradient(current_point)

        # Append current point to the path
        path_x.append(current_point[0])
        path_y.append(current_point[1])
        path_z.append(sog_value)

        print(f"{current_point} {sog_value:.8f}")

        new_point = current_point + step_size * sog_grad

        if np.linalg.norm(new_point - current_point) < epsilon:
            break

        current_point = new_point

    print("Gradient Ascent finished")

    # Plot optimization path
    ax.plot(path_x, path_y, path_z, c='b', marker='o', linestyle='-', label='Optimization Path')

    # Customize the plot
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Value')
    ax.set_title('Gradient Ascent Optimization')
    ax.legend()
    ax.grid()

    # Annotate the final point
    ax.text(path_x[-1], path_y[-1], path_z[-1], f'Final Point\n({path_x[-1]:.2f}, {path_y[-1]:.2f}, {path_z[-1]:.2f})', fontsize=12)

    plt.show()

if __name__ == "__main__":
    main()