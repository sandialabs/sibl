from ptg import command_line as cl


def test_say_hello():
    known = "hello world!"
    found = cl.say_hello()
    assert known == found


def test_version():
    known = "0.0.11"
    found = cl.version()
    assert known == found
