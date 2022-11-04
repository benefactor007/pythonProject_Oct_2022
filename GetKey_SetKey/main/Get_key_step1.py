import os,sys,json,jsonpath,pexpect,time


import pprint
import re

"""
import os 
#1获得当前路径，cwd=current working directory
os.getcwd()

#2获得绝对路径
os.path.abspath()

#3获得当前路径的上级目录路径
os.path.dirname()

#4组合使用，获得当前**文件路径**
os.path.abspath(os.path.dirname(__file__))

#5组合使用，获得当前**工作路径**
os.path.abspath(os.getcwd())

#6**改变当前工作目录到指定路径**
os.chdir()

"""


# get the current path
current_working_dir = os.getcwd()




# set log path => format as logs_20221027

logPath = os.getcwd() + os.sep + "logs_" + time.strftime("%Y%m%d") + ".txt"




# Get the file list in the target directory.
def get_fileList(dir):
    try:
        print(os.listdir(dir))
        return os.listdir(dir)
    except FileNotFoundError:
        os.mkdir(dir)
        print(f"Now the directory path <{dir}> has been created")


# transfer files to HU





# get the main's directory

main_dir = os.path.split(os.getcwd())[0] + os.sep + "main"


# get json_data from json_file:

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




# get the unused fazit-id only without store the status


# def get_valid_fazit(jsonData, brand = "FAW"):       # verison1: use jsonData as arg.
def get_valid_fazit(jsonPath, brand = "FAW"):       # version2: use jsonPath straight.
    jsonData = get_jsonData(jsonPath)
    fazitList = jsonData.get(brand, None)
    # print(f"fazitList in {get_valid_fazit.__name__}: {fazitList}")
    if not fazitList:
        print(f"There is no {brand} fazit in jsonData")
        return None
    else:
        for x in fazitList:
            # if not x["Used"]:
            if not x.get("Used", None):
                res = True
                # x["Used"] = True
                return x["fazit"]


# create save as name
def auto_save_file(path):
    directory, file_name = os.path.split(path)
    while os.path.isfile(path):
        pattern = '(\d+)\)\.'
        if re.search(pattern, file_name) is None:
            file_name = file_name.replace('.', '(0).')
        else:
            current_number = int(re.findall(pattern, file_name)[-1])
            new_number = current_number + 1
            # file_name = file_name.replace(f'({current_number}).', f'({new_number}).')
            file_name = file_name.replace('({0}).'.format(current_number), '({0}).'.format(new_number))
            # print("{0} is {1}".format("directory",directory))
            # print("{0} is {1}".format("file_name", file_name))
        path = os.path.join(directory + os.sep + file_name)
    return path

# after use the fazit id, change the status to be occupied.

def change_fazit_status(jsonPath,fazit, brand = "FAW"):
    res = False
    jsonData = get_jsonData(jsonPath)
    fazitList = jsonData.get(brand, None)
    if not fazitList:
        print(f"There is no brand record in jsonData, jsonPath: {jsonPath}")
        return False
    else:
        for x in fazitList:
            if x.get("fazit",None) == fazit:
                x["Used"] = True
                # print(f"auto_save_file(jsonPath) => {auto_save_file(jsonPath)}")
                # return store_fazit_dict_via_dict(auto_save_file(jsonPath),jsonData)
                return save_jsonFile_via_dict(jsonPath, jsonData)
        if not res:
            print(f"There is no fazit record in jsonData, jsonPath: {jsonPath}")
            return False

# store_fazit_data via dict:
def save_jsonFile_via_dict(jsonPath, jsonData):
    json.dump(jsonData, open(jsonPath, 'w'), ensure_ascii=False,
              indent=4, separators=(", ", " : "))
    # print("{0} is {1}".format("path",path))
    return jsonPath



# stroe_fazit_data_via_txt_file
def store_fazit_data(brand_name, tmp_fileName_path = main_dir + os.sep + "temp.txt"):
    with open(tmp_fileName_path, "r") as file:
        # file = file.readlines()
        fazit = [line.strip() for line in file.readlines()[1:]]
    fazit_dict = {}
    fazit_list = []
    for fazit in fazit:
        temp_dict = {}
        temp_dict["fazit"] = fazit
        temp_dict["Used"] = False
        fazit_list.append(temp_dict)
    fazit_dict[brand_name] = fazit_list
    pprint.pprint(fazit_dict)
    return fazit_dict


# Only in test mode, reset all fazit['Used'] status to false

def reset_fazit_data(jsonPath, brand):
    jsonData = get_jsonData(jsonPath)
    # get_child_wildcard = jsonpath.jsonpath(jsonData, "$.*")[0]      # version 1: use jsonpath func.
    fazitList = jsonData.get(brand, None)
    # print("before\n")
    # pprint.pprint(fazitList)
    if fazitList:
        for x in fazitList:
            if x.get("Used", None):
                x["Used"] = False

    double_check = input("Fazit status was reset\npls yes to continue...\n")
    if double_check == "yes" and fazitList:
        return save_jsonFile_via_dict(jsonPath, jsonData)
    else:
        return "Action terminated, pls try again"

    # print("after\n")
    # pprint.pprint(jsonData)



def main_exec():
    # cwd which set via interpreter
    print(f"current_working_directory: {current_working_dir}")
    # get the cwd of current file
    print(f"the cwd of current file: {os.path.abspath(os.path.dirname(__file__))}")
    # change the cwd to the cwd of current file
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    print(f"Now the current_working_directory: {current_working_dir}")

    # get the tool's directory
    tool_dir = os.path.split(os.getcwd())[0] + os.sep + "tools"

    print(f"log path: {logPath}")
    print(f"tool directory: {tool_dir}")
    print(f"get_fileList func. =>  {get_fileList(tool_dir)} ")

    # get the fazit_clip's directory
    json_dir = os.path.split(os.getcwd())[0] + os.sep + "fazit_clip"
    print(f"json_dir => {json_dir}")

    print(f"get_json_fileList. => {get_fileList(json_dir)}")

    ## try to test in single file
    # print(get_valid_fazit(get_jsonData(json_dir + os.sep + 'svw_fazit.json')))
    # sys.exit()

    # now we try to get the jsonData from fazit_clip file
    for i in get_fileList(json_dir):
        # pprint.pprint(get_jsonData(json_dir + os.sep +i))
        # print("start" + "=" * 60 )
        # print(get_valid_fazit(json_dir + os.sep + i))
        brand = i[:3].upper()
        print(f"brand name => {brand}")
        valid_fazit = get_valid_fazit(json_dir + os.sep + i, brand = brand)
        if not valid_fazit:
            print(f"\033[31mThere is no valid {brand} fazit\033[0m")
        else:
            print(f"\033[32mfazit: {valid_fazit}\033[0m")
        # print("end" + "="*60 + "\n")
        if change_fazit_status(json_dir + os.sep + i,valid_fazit,brand = brand):
            print(f"save jsonData with the latest status, and jsonPath: {change_fazit_status(json_dir + os.sep + i,valid_fazit,brand = brand)}")


# reset all fazitData in fazit clip folder
def main_action2():
    print(f"the cwd of current file: {os.path.abspath(os.path.dirname(__file__))}")
    # change the cwd to the cwd of current file
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    print(f"os.getcwd() => {os.getcwd()}")
    fazit_clip_dir = os.path.split(os.getcwd())[0] + os.sep + "fazit_clip"
    print(f"fazit_clip_dir => {fazit_clip_dir}")
    for fileName in get_fileList(fazit_clip_dir):
        print(f"file => {fileName}")
        brand = fileName[:3].upper()
        print(f"brand name => {brand}")
        print(reset_fazit_data(fazit_clip_dir + os.sep + fileName, brand=brand))


def set_real_cwd():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    print(f"set cwd to {os.path.abspath(os.path.dirname(__file__))}")
    return True

def final_get_vaild_fazit(given_brand):
    # set_real_cwd()              # avoid os.getcwd() error
    # get the fazit_clip's directory
    fazit_clip_dir = os.path.split(os.getcwd())[0] + os.sep + "fazit_clip"
    print(f"fazit_clip_dir => {fazit_clip_dir}")
    for i in get_fileList(fazit_clip_dir):
        brand = i[:3].upper()
        if brand == given_brand:
            print(f"brand name => {brand}")
            valid_fazit = get_valid_fazit(fazit_clip_dir + os.sep + i, brand=brand)
            if not valid_fazit:
                print(f"\033[31mThere is no valid {brand} fazit\033[0m")
                return False
                # if change_fazit_status(fazit_clip_dir + os.sep + i, valid_fazit, brand=brand):
                #     print(
                #         f"save jsonData with the latest status, and jsonPath: {change_fazit_status(fazit_clip_dir + os.sep + i, valid_fazit, brand=brand)}")
            else:
                print(f"\033[32mfazit: {valid_fazit}\033[0m")
                return valid_fazit,fazit_clip_dir + os.sep + i

        else:
            print(f"There is no brand as given_brand({given_brand})")
            return False


def final_change_fazit_status(jsonPath,fazit,brand):
    res = False
    jsonData = get_jsonData(jsonPath)
    fazitList = jsonData.get(brand, None)
    if not fazitList:
        print(f"There is no brand record in jsonData, jsonPath: {jsonPath}")
        return False
    else:
        for x in fazitList:
            if x.get("fazit", None) == fazit:
                x["Used"] = True
                # print(f"auto_save_file(jsonPath) => {auto_save_file(jsonPath)}")
                # return store_fazit_dict_via_dict(auto_save_file(jsonPath),jsonData)
                return save_jsonFile_via_dict(jsonPath, jsonData)
        if not res:
            print(f"There is no fazit record in jsonData, jsonPath: {jsonPath}")
            return False


def convert_txt_to_json(root_name:str,child_name,tmpPath):
    with open(tmpPath, "r") as file:
        # file = file.readlines()
        data = [line.strip() for line in file.readlines()[:]]
    json_dict = {}
    child_list = []
    for ele in data:
        temp_dict = {}
        temp_dict[child_name] = ele
        temp_dict["Used"] = False
        child_list.append(temp_dict)
    json_dict[root_name] = child_list
    pprint.pprint(json_dict)
    return json_dict

def get_valid_data(jsonPath, root_name,child_name):       # version2: use jsonPath straight.
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
                    return x[child_name]




def final_get_vaild_data(jsonPath,root_name,child_name):
    """
    This func. is used to get valid data (e.g. fazit or serial) from json file
    :param jsonPath:
    :param root_name: input root_name as arg.
    :param child_name:
    :return:
    """
    valid_data = get_valid_data(jsonPath,root_name,child_name)
    if not valid_data:
        print(f"\033[31mThere is no valid root_name({root_name}) \033[0m")
        return False
    else:
        print(f"\033[32mdata: {valid_data}\033[0m")
        return valid_data


def final_change_data_status(jsonPath,valid_data,root_name,child_name):
    res = False
    jsonData = get_jsonData(jsonPath)
    child_list = jsonData.get(root_name, None)
    if not child_list:
        print(f"There is no root_name({root_name}) record in jsonData, jsonPath: {jsonPath}")
        return False
    else:
        for x in child_list:
            if x.get(child_name, None) == valid_data:
                x["Used"] = True
                save_jsonFile_via_dict(jsonPath, jsonData)
                return True
        if not res:
            print(f"There is no valid_data({valid_data}) record in jsonData, jsonPath: {jsonPath}")
            return False



def final_reset_data(jsonPath, root_name):
    jsonData = get_jsonData(jsonPath)
    # get_child_wildcard = jsonpath.jsonpath(jsonData, "$.*")[0]      # version 1: use jsonpath func.
    child_list = jsonData.get(root_name, None)
    # print("before\n")
    # pprint.pprint(fazitList)
    if child_list:
        for x in child_list:
            res = x.get("Used", None)
            if res ==  None:
                print(f"Cannot find the element of \"Used\"")
            else:
                if res:
                    x["Used"] = False
    else:
        raise ValueError(f"\033[31mCannot find the root_name({root_name})\033[0m")
    double_check = input("the child status of Data({root_name}) was reset\npls \"yes\" to continue...\n")
    if double_check == "yes" and child_list:
        return save_jsonFile_via_dict(jsonPath, jsonData)
    else:
        return "Action terminated, pls try again"



if __name__ == '__main__':
    # main_exec()
    # main_action2()
    # sys.exit()
    set_real_cwd()
    serialNum_clip_dir = os.path.split(os.getcwd())[0] + os.sep + "serialNum_clip"
    temp_dir = os.path.split(os.getcwd())[0] + os.sep + "temp"
    print(f"temp_dir => {temp_dir}")
    # print(convert_txt_to_json("serial_num", "serial",temp_dir + os.sep + "serialNum.txt"))
    # store_fazit_dict_via_dict(serialNum_clip_dir + os.sep + "serial_num.json",convert_txt_to_json("serial_num", "serial",temp_dir + os.sep + "serialNum.txt"))

    serialNum_jsonPath = serialNum_clip_dir + os.sep + "serial_num.json"
    valid_serial = final_get_vaild_data(serialNum_jsonPath,"serial_num","serial")
    final_change_data_status(serialNum_jsonPath,valid_serial,"serial_num","serial")
    # final_reset_data(serialNum_jsonPath,"serial_num")
    sys.exit()
    logPath = __file__.split(".")[0]
    logPath = f'{__file__.split(".")[0]}_log_{time.strftime("%Y%m%d")}.txt'

    # sys.exit()
    tempRight = sys.stdout                              # store sys.stdout as tempRight
    with open(logPath,"a") as logs:
        logs.write("\n" + "*" * 30 + time.strftime("%Y%m%d_%H_%M_%S", time.localtime(time.time())) + "*" * 30 + "\n")
        sys.stdout = logs                               # redirect the standard output to a file
        valid_fazit = final_get_vaild_fazit("FAW")
        if valid_fazit:
            final_change_fazit_status(valid_fazit[1],valid_fazit[0],"FAW")
            sys.stdout = tempRight  # reset standard output
            print(f"valid_fazit => {valid_fazit[0]}")
        else:
            sys.stdout = tempRight  # reset standard output
            print(f"The status of valid: {valid_fazit}")
        logs.write("="*30 + time.strftime("%Y%m%d_%H_%M_%S", time.localtime(time.time())) +"="*30 + "\n\n" )