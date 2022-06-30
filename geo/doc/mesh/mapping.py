"""This module creates specific points to generate lines from
the map from parameter space to physical space in the figure
in quad_quality.tex.
"""


def N1(a: float, b: float) -> float:
    # assert -1.0 <= a and a <= 1.0
    # assert -1.0 <= b and b <= 1.0
    value = 0.25 * (1.0 - a) * (1.0 - b)
    return value


assert N1(-1.0, -1.0) == 1.0
assert N1(1.0, -1.0) == 0.0
assert N1(1.0, 1.0) == 0.0
assert N1(-1.0, 1.0) == 0.0


def N2(a: float, b: float) -> float:
    # assert -1.0 <= a and a <= 1.0
    # assert -1.0 <= b and b <= 1.0
    value = 0.25 * (1.0 + a) * (1.0 - b)
    return value


assert N2(-1.0, -1.0) == 0.0
assert N2(1.0, -1.0) == 1.0
assert N2(1.0, 1.0) == 0.0
assert N2(-1.0, 1.0) == 0.0


def N3(a: float, b: float) -> float:
    # assert -1.0 <= a and a <= 1.0
    # assert -1.0 <= b and b <= 1.0
    value = 0.25 * (1.0 + a) * (1.0 + b)
    return value


assert N3(-1.0, -1.0) == 0.0
assert N3(1.0, -1.0) == 0.0
assert N3(1.0, 1.0) == 1.0
assert N3(-1.0, 1.0) == 0.0


def N4(a: float, b: float) -> float:
    # assert -1.0 <= a and a <= 1.0
    # assert -1.0 <= b and b <= 1.0
    value = 0.25 * (1.0 - a) * (1.0 + b)
    return value


assert N4(-1.0, -1.0) == 0.0
assert N4(1.0, -1.0) == 0.0
assert N4(1.0, 1.0) == 0.0
assert N4(-1.0, 1.0) == 1.0


def x(a: float, b: float, nodes_posn: tuple[float, float, float, float]) -> float:
    ns = [N1(a, b), N2(a, b), N3(a, b), N4(a, b)]
    es = tuple([na * xa for (na, xa) in zip(ns, nodes_posn)])
    value = sum(es)
    return value


# specific example given in the figure
node_xs = (1.0, 4.0, 5.0, 0.0)
node_ys = (1.5, 2.0, 5.0, 6.0)

# used for by xi and eta on the quad perimeter, followed by xi and eta axes
xis = (
    -1.0,
    -0.5,
    0.0,
    0.5,
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
    0.5,
    0.0,
    -0.5,
    -1.0,
    -1.0,
    -1.0,
    -1.0,
    -1.5,
    1.5,
    0.0,
    0.0,
)
yis = (
    -1.0,
    -1.0,
    -1.0,
    -1.0,
    -1.0,
    -0.5,
    0.0,
    0.5,
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
    0.5,
    0.0,
    -0.5,
    0.0,
    0.0,
    -1.5,
    1.5,
)

assert len(xis) == len(yis)

xs = tuple([x(a=xi, b=eta, nodes_posn=node_xs) for (xi, eta) in zip(xis, yis)])
ys = tuple([x(a=xi, b=eta, nodes_posn=node_ys) for (xi, eta) in zip(xis, yis)])

print(f"xi axis: from {xs[16], ys[16]} to {xs[17], ys[17]}")
print(f"eta axis: from {xs[18], ys[18]} to {xs[19], ys[19]}\n")

print(f"vertical line 1: from {xs[1], ys[1]} to {xs[11], ys[11]}")
print(f"vertical line 2: from {xs[2], ys[2]} to {xs[10], ys[10]}")
print(f"vertical line 3: from {xs[3], ys[3]} to {xs[9], ys[9]}\n")

print(f"horizontal line 1: from {xs[15], ys[15]} to {xs[5], ys[5]}")
print(f"horizontal line 2: from {xs[14], ys[14]} to {xs[6], ys[6]}")
print(f"horizontal line 3: from {xs[13], ys[13]} to {xs[7], ys[7]}")
