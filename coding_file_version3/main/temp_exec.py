"""
Python3.5
"""
import binascii
import sys,os

def str_to_hexStr(str_info):
    return binascii.hexlify(str_info.encode('utf-8')).decode('utf-8')

if __name__ == '__main__':
    # persistence_list = [["0x80000008","0x00","0xe5","open read-write access"],\
    #                     ["0x3000000","0xF18C",""]]
    # pro_dir = os.path.dirname(os.getcwd())
    # with open(pro_dir + "/" + "persistenceOverview_0929.txt", "a") as file:
    #     title_list = ["Namespace_hex","Key","data","Namespace_purpose",]
    #     for i in title_list:
    #         file.write("i")
    #         file.write("\n")

    # serial_num_hex = ""
    # serial_num = "3JD035866  "
    # print(str_to_hexStr(serial_num).upper())
    while True:
        dec_str = input("please input the decimalism string:")
        print("|||{0}|||\n".format(str_to_hexStr(dec_str).upper()))