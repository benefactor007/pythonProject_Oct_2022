import os,sys

from Get_key_step1 import convert_txt_to_json,save_jsonFile_via_dict
import binascii

def str_to_hexStr(str_info):
    return binascii.hexlify(str_info.encode('utf-8')).decode('utf-8')

def reload_fazit_json_file(jsonFileName,root_name:str,child_name,tmpPath):
    print(f"os.getcwd() => {os.getcwd()}")
    # jsonData = convert_txt_to_json("FAW","fazit","faw_fazit.txt")
    jsonData = convert_txt_to_json(root_name,child_name,tmpPath)
    # save_jsonFile_via_dict("faw_fazit.json",jsonData)
    save_jsonFile_via_dict(jsonFileName, jsonData)


def temp_func():
    ascii_hex = str_to_hexStr("5HG035866  ")
    # print([i for i in range(1,len(ascii_hex),2)])
    print(f"ascii_hex = {ascii_hex}")
    ascii_hex_w_space = " ".join([ascii_hex[i] + ascii_hex[i+1] for i in range(0,len(ascii_hex),2)])
    print(f"ascii_hex_w_space = {ascii_hex_w_space}")


def temp_func2(ascii_char):
    ascii_hex = str_to_hexStr(ascii_char)
    # print([i for i in range(1,len(ascii_hex),2)])
    print(f"ascii_hex = 0x{ascii_hex}")
    ascii_hex_w_space = " ".join([ascii_hex[i] + ascii_hex[i+1] for i in range(0,len(ascii_hex),2)])
    print(f"ascii_hex_w_space = {ascii_hex_w_space}")


if __name__ == '__main__':
    # temp_func()
    temp_func2("C370")
    temp_func2("X09")

    # reload_fazit_json_file("serialNum_5HG035866.json","serial_num","serial","serialNum_5HG035866.txt")
    # reload_fazit_json_file("faw_fazit.json","FAW","fazit","faw_fazit.txt")
    # reload_fazit_json_file("svw_fazit.json","SVW", "fazit", "svw_fazit.txt")
    # sys.exit()