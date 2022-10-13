from practice import fetcher


class AlreadyGotOne(Exception):  # User-defined exception
    pass


def grail():  # 圣杯
    raise AlreadyGotOne()  # Raise an instance


class Career(Exception):
    def __str__(self):
        return "So I became a waiter ..."


def after():
    try:
        fetcher(x, 3)
    finally:
        print("after fetch")
    print("after try?")


if __name__ == '__main__':
    try:
        grail()
    except AlreadyGotOne:  # catch class name
        print('got exception')

    x = "spam"

    try:
        fetcher(x, 3)
    finally:
        print("after fetcher")

    # we might as well have simply typed the print right after

    after()


    def after():
        try:
            fetcher(x, 4)
        finally:
            print("after fetch")
        print("after try?")


    # after()

    # For instance, you might use try/except to catch errors raised by code that you import
    # from a third-party library, and try/finally to ensure that calls to close files or terminate
    # server connections are always run.
    # raise Career()


    # Although they serve conceptually distinct purposes
    with open("lumberjack.txt","w") as file:
        file.write("the larch\n")