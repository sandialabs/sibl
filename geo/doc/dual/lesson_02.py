import math
import matplotlib.pyplot as plt


def main():

    n_samples = 40
    radius = 2.0

    # parameterize the curve
    ts = tuple(range(n_samples))

    # create x and y points
    xs = [radius * math.cos(2.0 * math.pi * t / n_samples) for t in ts]
    ys = [radius * math.sin(2.0 * math.pi * t / n_samples) for t in ts]

    s = 6.0  # 6.0 inches
    fig = plt.figure(figsize=(s, s))

    ax = fig.gca()

    ax.plot(xs, ys, "-", alpha=0.5)
    ax.plot(xs, ys, ".")

    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    plt.axis("on")

    plt.show()


if __name__ == "__main__":
    main()
