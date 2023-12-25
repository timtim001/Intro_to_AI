import numpy as np
import sys


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

    for i in range(max_iterations):
        sog_value = sog.evaluate(current_point)
        sog_grad = sog.gradient(current_point)

        new_point = current_point + step_size * sog_grad

        if np.linalg.norm(new_point - current_point) < epsilon: #finds if the differnce in the current point and the next point are smaller than the tollerance
            break

        current_point = new_point

    point_str = ' '.join(map(str, current_point))
    print(f"{current_point} {sog_value:.8f}")
    return current_point
if __name__ == "__main__":
    main()

