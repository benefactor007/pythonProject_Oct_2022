import json
import os,sys,pprint

import jsonpath


def get_jsonData(filePath):
    """

    :param filePath:
    :return: jsonData: type(jsonData): dict
    """
    with open(filePath) as jsonFile:
        jsonData = json.load(jsonFile)
        # pprint.pprint(jsonData)
        res = jsonpath.jsonpath(jsonData, "$.*")
        # pprint.pprint(res)
        return jsonData


def get_valid_data_list(jsonPath, root_name,child_name):       # version2: use jsonPath straight.
    unused_child_list = []
    jsonData = get_jsonData(jsonPath)
    child_list = jsonData.get(root_name, None)
    if not child_list:
        print(f"There is no root_name({root_name}) in jsonData")
        return None
    else:
        for x in child_list:
            res = x.get("Used", None)
            if res == None:
                print(f"Cannot find the \"Used\" as element ")
            else:
                if not res:         # cuz the type of res is boolean
                    unused_child_list.append(x[child_name])
    return unused_child_list




if __name__ == '__main__':
    print(f"os.getcwd() => {os.getcwd()}")
    fazit_clip_dir = os.path.split(os.getcwd())[0] + os.sep + "fazit_clip"
    serialNum_clip_dir = os.path.split(os.getcwd())[0] + os.sep + "serialNum_clip"
    # unused_list = get_valid_data_list(fazit_clip_dir + os.sep + "svw_fazit.json", "SVW", "fazit")
    # unused_list = get_valid_data_list(fazit_clip_dir + os.sep + "faw_fazit.json", "FAW", "fazit")
    unused_list = get_valid_data_list(serialNum_clip_dir + os.sep + "serial_num.json", "serial_num", "serial")
    for i in range(0,30):
        print(unused_list[i])

    sys.exit()
    # VWX9GA3644037
    # serial_list = [f"VWX9GA3644{x}\n" for x in range(37,1000)]
    serial_list = [f"VWX9GA3644%03d\n"%x for x in range(37, 1000)]
    # '%016d' % 123
    # pprint.pprint(serial_list[11])
    # sys.exit()
    print(f"os.getcwd() => {os.getcwd()}")
    with open("serialNum.txt","w") as file:
        file.writelines(serial_list)

