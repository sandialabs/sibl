"""
For coverage:
pytest geo/tests/test_hello.py -v --cov=geo/src/ptg --cov-report term-missing
"""

# import .hello as hh
# import hello as hh
from ptg import hello as hh


def test_one():
    assert True


def test_two():
    known = "Hello world!"
    found = hh.hello()

    assert found == known


def test_adios():
    known = "Bye"
    found = hh.adios()

    assert found == known


def test_bubble_sort():
    assert hh.bubble_sort()


"""
Copyright 2023 Sandia National Laboratories

Notice: This computer software was prepared by National Technology and Engineering Solutions of
Sandia, LLC, hereinafter the Contractor, under Contract DE-NA0003525 with the Department of Energy
(DOE). All rights in the computer software are reserved by DOE on behalf of the United States
Government and the Contractor as provided in the Contract. You are authorized to use this computer
software for Governmental purposes but it is not to be released or distributed to the public.
NEITHER THE U.S. GOVERNMENT NOR THE CONTRACTOR MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES
ANY LIABILITY FOR THE USE OF THIS SOFTWARE. This notice including this sentence must appear on any
copies of this computer software. Export of this data may require a license from the United States
Government.
"""
