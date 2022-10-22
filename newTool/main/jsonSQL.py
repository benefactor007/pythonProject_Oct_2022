import re

import json
import os, sys
import pprint


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


def saveAsFile(file_path, file_name, json_data):
    path = auto_save_file(file_path + "/" + file_name)
    json.dump(json_data, open(path, 'w'), ensure_ascii=False,
              indent=4, separators=(", ", " : "))
    # print("{0} is {1}".format("path",path))
    return path

def saveFile(folder_path, file_name, json_data):
    path = folder_path + os.sep + file_name
    json.dump(json_data, open(path, 'w'), ensure_ascii=False,
              indent=4, separators=(", ", " : "))
    # print("{0} is {1}".format("path",path))
    return path


if __name__ == '__main__':
    cwd = os.getcwd()
    print(f"cwd: {cwd}")
    print(f"os.path.split(cwd)[0]: {os.path.split(cwd)[0]}")
    # cwd: / home / jpcc / PycharmProjects / pythonProject_Oct_2022
    json_folder_path = cwd + os.sep + "json"
    print(f"json_folder_path: {json_folder_path}")
    # json_folder_path: / home / jpcc / PycharmProjects / pythonProject_Oct_2022 / json
    svw_fazit = []
    main_folder_path = cwd + os.sep + "main"


    # print(f"svw_fazit: {svw_fazit}")

    def store_fazit_data(brand_name, tmp_fileName_path = main_folder_path + os.sep + "temp.txt"):
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

    saveFile(json_folder_path,"faw_fazit.json",store_fazit_data("FAW", main_folder_path + os.sep + "tmp1.txt"))
    saveFile(json_folder_path, "svw_fazit.json", store_fazit_data("SVW",  main_folder_path + os.sep + "tmp2.txt"))

    def get_json_info(json_path, jsonPathDesc, codingFormat=None):
        """
      :param json_file_name:
      :param jsonPathDesc:
      :return: dict(json's data)
      """
        import json, jsonpath
        # print(P_step1.repr_message(json_file_name))
        with open(json_path, encoding=codingFormat) as json_file:
            data = json.load(json_file)
            res = jsonpath.jsonpath(data, jsonPathDesc)
        return data


    import glob
    print(glob.glob(json_folder_path + os.sep + "*.json"))


    def Merge_json(folder_path, codingFormat=None):
        import glob
        res = []
        for f in glob.glob(folder_path + os.sep + "*.json"):
            print(f)
            with open(f, "r") as json_data:
                res.append(json.load(json_data))
        # with open("result.json", "w",encoding = codingFormat) as res_file:
        #     json.dump(res, res_file, ensure_ascii=False)
        json.dump(res, open("res.json", 'w'), ensure_ascii=False,indent=4, separators=(", ", " : "))
        return res

    def Merge_json(folder_path, codingFormat=None):
        import glob
        res = {}
        for f in glob.glob(folder_path + os.sep + "*.json"):
            print(f)
            with open(f, "r") as json_data:
                # res.append(json.load(json_data))
                res.update(json.load(json_data))
        # with open("result.json", "w",encoding = codingFormat) as res_file:
        #     json.dump(res, res_file, ensure_ascii=False)
        json.dump(res, open("res.json", 'w'), ensure_ascii=False,indent=4, separators=(", ", " : "))
        return res

    print(Merge_json(json_folder_path))