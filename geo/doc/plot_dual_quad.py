from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
from matplotlib import rc

import ptg.dual_quad as dq

colors = (
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
    "tab:purple",
    "tab:brown",
    "tab:pink",
    "tab:gray",
    "tab:olive",
    "tab:cyan",
)

latex: Final = True
if latex:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)


def plot_template(template, *, dual_shown=False, plot_shown=False, serialize=False):
    xs, ys = zip(*template.vertices)

    fig = plt.figure(figsize=(6.0, 6.0), dpi=100)
    ax = fig.gca()

    for face in template.faces:
        xf = [xs[k] for k in face]
        yf = [ys[k] for k in face]
        plt.fill(
            xf, yf, linestyle="dotted", edgecolor="magenta", alpha=0.5, facecolor="gray"
        )

    if dual_shown:

        xs, ys = zip(*template.vertices_dual)

        for face in template.faces_dual:
            xf = [xs[k] for k in face]
            yf = [ys[k] for k in face]
            plt.fill(
                xf,
                yf,
                linestyle="solid",
                edgecolor="black",
                facecolor=colors[0],
                alpha=0.5,
            )

        xs, ys = zip(*template.ports)
        ax.scatter(
            xs,
            ys,
            edgecolor="black",
            facecolor="white",
            alpha=0.7,
            marker="o",
            s=20,  # markersize
        )

    # finally, show the hanging nodes if any, and the revalence path
    try:
        if template.vertices_revalence is not None:
            for reval_path in template.vertices_revalence:
                xs, ys = zip(*reval_path)
                plt.plot(
                    xs, ys, linestyle="dotted", linewidth=1.0, color="black", alpha=0.3
                )
                ax.scatter(
                    [xs[0], xs[-1]],
                    [ys[0], ys[-1]],
                    edgecolor="magenta",
                    facecolor="magenta",
                    alpha=1.0,
                    marker="o",
                    s=20,  # markersize
                )
    except AttributeError as e:
        print(e)
        print("Warning: this template must specify hanging vertices or None.")

    # ax.set_ylim([0.0 - 2 * _eps, 1.0 + 2 * _eps])
    # ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

    ax.set_aspect("equal")
    # ax.grid(True, which="major", linestyle="-")
    # ax.grid(True, which="minor", linestyle=":")

    # ax.xaxis.set_major_locator(MultipleLocator(1.0))
    # ax.xaxis.set_minor_locator(MultipleLocator(0.25))
    # ax.yaxis.set_major_locator(MultipleLocator(1.0))
    # ax.yaxis.set_minor_locator(MultipleLocator(0.25))

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])

    if plot_shown:
        plt.show()

    if serialize:

        extension = "_" + template.name + ".png"  # or '.'.png' | '.pdf' | '.svg'
        filename = Path(__file__).stem + extension
        fig.savefig(filename, bbox_inches="tight", pad_inches=0)
        print(f"Serialized to {filename}")


def main():

    dual: Final = True
    show: Final = False
    save: Final = True

    # The six unique transitions
    # plot_template(dq.Template_0000(), dual_shown=dual, plot_shown=show, serialize=save)
    plot_template(dq.Template_0001(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_0011(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_0110(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_0111(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_1111(), dual_shown=dual, plot_shown=show, serialize=save)

    # The remaining (non-unique) transitions
    #
    # based on Template_0001
    # plot_template(dq.Template_0010(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_0100(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_1000(), dual_shown=dual, plot_shown=show, serialize=save)
    #
    # based on Template_0011
    # plot_template(dq.Template_0101(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_1010(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_1100(), dual_shown=dual, plot_shown=show, serialize=save)
    #
    # based on Template_0110
    # plot_template(dq.Template_1001(), dual_shown=dual, plot_shown=show, serialize=save)
    #
    # based on Template_0111
    # plot_template(dq.Template_1011(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_1101(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_1110(), dual_shown=dual, plot_shown=show, serialize=save)

    # The weakly balanced transition
    # plot_template(dq.Template_0112(), dual_shown=dual, plot_shown=show, serialize=save)
    #
    # based on Template_0112
    # plot_template(dq.Template_1021(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_1201(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_2110(), dual_shown=dual, plot_shown=show, serialize=save)


if __name__ == "__main__":
    main()
