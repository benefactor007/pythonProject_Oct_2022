import os,sys,pprint

if __name__ == '__main__':
    # VWX9GA3644037
    # serial_list = [f"VWX9GA3644{x}\n" for x in range(37,1000)]
    serial_list = [f"VWX9GA3536%03d\n"%x for x in range(1, 1000)]
    # '%016d' % 123
    # pprint.pprint(serial_list[11])
    # sys.exit()
    print(f"os.getcwd() => {os.getcwd()}")
    with open("serialNum_5HG035866.txt","w") as file:
        file.writelines(serial_list)