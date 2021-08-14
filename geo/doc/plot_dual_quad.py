from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import rc

import ptg.dual_quad as dq

index_x, index_y = 0, 1  # avoid magic numbers later

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

latex = True
if latex:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)


def face_coordinates(
    face: dq.Face, vertices: tuple[dq.Vertex, ...]
) -> tuple[dq.Vertex, ...]:

    bb = tuple(vertices[k] for k in face)
    return bb


def plot_template(template, *, dual_shown=False, plot_shown=False, serialize=False):
    faces_as_coordinates = tuple(
        face_coordinates(face, template.vertices) for face in template.faces
    )

    fig = plt.figure(figsize=(6.0, 6.0), dpi=100)
    ax = fig.gca()

    for face in faces_as_coordinates:
        xs = [face[k][index_x] for k in range(len(face))]
        ys = [face[k][index_y] for k in range(len(face))]
        plt.fill(
            xs, ys, linestyle="dotted", edgecolor="magenta", alpha=0.5, facecolor="gray"
        )

    if dual_shown:

        faces_as_coordinates = tuple(
            face_coordinates(face, template.vertices_dual)
            for face in template.faces_dual
        )

        for face in faces_as_coordinates:
            xs = [face[k][index_x] for k in range(len(face))]
            ys = [face[k][index_y] for k in range(len(face))]
            plt.fill(
                xs,
                ys,
                linestyle="solid",
                edgecolor="black",
                facecolor=colors[0],
                alpha=0.5,
            )

        xs = [template.ports[i][0] for i in range(len(template.ports))]
        ys = [template.ports[i][1] for i in range(len(template.ports))]
        # ax.plt(xs, ys, "o")
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
            for xys in template.vertices_revalence:
                # xys = template.vertices_revalence
                xs = [xys[k][index_x] for k in range(len(xys))]
                ys = [xys[k][index_y] for k in range(len(xys))]
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

    # ax.set_xticks([0, 1, 2, 3, 4])
    # ax.set_yticks([0, 1, 2, 3, 4])
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

    dual = False
    show = False
    save = True

    # The six unique transitions
    # plot_template(dq.Template_0000(), dual_shown=dual, plot_shown=show, serialize=save)
    # plot_template(dq.Template_0001(), dual_shown=dual, plot_shown=show, serialize=save)
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
    plot_template(dq.Template_1100(), dual_shown=dual, plot_shown=show, serialize=save)


if __name__ == "__main__":
    main()
