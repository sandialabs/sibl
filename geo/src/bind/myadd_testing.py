# ptgbind_testing.py

# from myadd import add
# from xybind import myadd
from xybind import add

# help(add)

known = 3
found = add(1, 2)
assert known == found
