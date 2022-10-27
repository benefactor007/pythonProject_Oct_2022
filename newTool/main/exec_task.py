import json
import os,sys
import pprint

import jsonpath

if __name__ == '__main__':
    print(f"os.getcwd():{os.getcwd()}")
    print(os.path.split(os.getcwd())[0])
    json_folder = os.path.split(os.getcwd())[0] + os.sep + "json"
    print(os.listdir(json_folder))
    json_path_list = [json_folder + os.sep + x for x in os.listdir(json_folder)]
    print(json_path_list)
    # sys.exit()
    # with open(json_file_name, encoding=codingFormat) as json_file:
    #         data = json.load(json_file)
    #         res = jsonpath.jsonpath(data, jsonPathDesc)
    #     return res
    with open(json_path_list[0]) as jsonFile:
        jsonData = json.load(jsonFile)
        res = jsonpath.jsonpath(jsonData,"$.FAW.*")
        pprint.pprint(jsonData)
        pprint.pprint(res)

    print(f"type of jsonData: {type(jsonData)}")
    print(f"type of res: {type(res)}")
    print(jsonData.get("FAW"))
    for x in jsonData.get("FAW"):
        print(f'x[\"used\"]: {x["Used"]}')
        if x["Used"]:
            print(x["fazit"])


    def get_valid_fazit(jsonData):
        # res = False
        for x in jsonData.get("FAW"):
            # print(f'x[\"used\"]: {x["Used"]}')
            if not x["Used"]:
                res = True
                x["Used"] = True
                return x["fazit"]
        # if not res:
        #     print("There is no more valid Fazit")


    # print(f"get_valid_fazit(jsonData): {get_valid_fazit(jsonData)}")
    # print(jsonData["FAW"]["get_valid_fazit(jsonData)"])

    def saveFile(filePath, json_data):
        json.dump(json_data, open(filePath, 'w'), ensure_ascii=False,
                  indent=4, separators=(", ", " : "))
        # print("{0} is {1}".format("path",path))
        return filePath


    pprint.pprint(jsonData)
    print(len(jsonData["FAW"]))
    # for i in range(10,len(jsonData["FAW"])):
    print(f"get_valid_fazit(jsonData): {get_valid_fazit(jsonData)}")
    if not get_valid_fazit(jsonData):
        print("There is no more valid fazit")
    saveFile(json_path_list[0],jsonData)
    # pprint.pprint(jsonData)