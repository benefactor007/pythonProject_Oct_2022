import os,sys

from Get_key_step1 import convert_txt_to_json,save_jsonFile_via_dict

def reload_fazit_json_file(jsonFileName,root_name:str,child_name,tmpPath):
    print(f"os.getcwd() => {os.getcwd()}")
    # jsonData = convert_txt_to_json("FAW","fazit","faw_fazit.txt")
    jsonData = convert_txt_to_json(root_name,child_name,tmpPath)
    # save_jsonFile_via_dict("faw_fazit.json",jsonData)
    save_jsonFile_via_dict(jsonFileName, jsonData)


if __name__ == '__main__':
    reload_fazit_json_file("faw_fazit.json","FAW","fazit","faw_fazit.txt")
    reload_fazit_json_file("svw_fazit.json","SVW", "fazit", "svw_fazit.txt")
    sys.exit()