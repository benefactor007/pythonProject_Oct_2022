#!/usr/bin/python3

def fetcher(obj,index):
    return obj[index]


def catcher():
    try:
        fetcher(x,4)
        ...
    except IndexError:
        print("got exception")
        print("continuing")

if __name__ == '__main__':
    x = "spam"
    print(fetcher(x, 3))
    try:
        print(fetcher(x,4))
    except IndexError:
        print("got exception")
    catcher()

    try:
        raise IndexError
    except IndexError:
        print("got exception")

    assert False, "Nobody expects the Spanish Inquisition"


#Notice that there’s no way in Python to go back to the code that triggered the exception