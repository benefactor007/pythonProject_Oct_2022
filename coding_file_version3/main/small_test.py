import os,sys

a = 1
def a(num):
    # a = 1
    print(f"num: {num}")
    if num > 10:
        sys.exit()
    else:
        num += 1
        a(num)

if __name__ == '__main__':
    a(1)