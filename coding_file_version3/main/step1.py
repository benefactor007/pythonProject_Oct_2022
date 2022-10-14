"""
python3.5
"""
import json
import os, sys
import pprint
import time

import jsonpath
import pexpect

jsonDict = {'ns': '', 'data': '', 'sendline': '', 'expect': '', 'key': ''}


# class JSON:
#     # def __init__(self, jsonDict):
#     #     self.expect = jsonDict['expect']
#     #     self.sendline = jsonDict['sendline']
#     #     self.ns = jsonDict['ns']
#     #     self.data = jsonDict['data']
#     #     self.key = jsonDict['key']
#     jsonDict = {}
#     def __init__(self,expect='',sendline=''):
#         self.expect = expect
#         self.sendline = sendline
#         # self.ns = ns
#         # self.data = data
#         # self.key = key
#
#     def dictFormat(self):
#         jsonDict['expect'] = self.expect
#         jsonDict['sendline'] = self.sendline
#         # jsonDict['ns'] = self.ns
#         # jsonDict['data'] = self.data
#         # jsonDict['key'] = self.key
#
#     def __str__(self):
#         # return "The current {0} is {1}".format("jsonDict",jsonDict)
#         # for i in JSON.args:
#         return "{0} is {1}".format("self.expect",self.expect)


class S1:
    ip, user, password, local_files_dic = "192.168.1.4", "root", "root", "tools"

    dest_dir = "/tmp"
    json_levelA = "p_Gerkey"
    key_Namehex_dict = {}
    init_dict = {
        json_levelA: [{'expect': 'password'}, {'sendline': 'root'}, {'expect': 'root@'}, {'sendline': 'cd /tmp/'},
                      {'expect': '/tmp'}]}

    def __init__(self):
        self.project_dir = ""
        self.json_dir = ""
        self.tools_dir = ""
        self.log_name = ""
        self.log_mode = "w"
        self.processList = []

    @staticmethod
    def fileInfo_to_dict(fileName):
        """
        only read first two columns, which are column 1 and column 2
        :param fileName:
        :return: dict{column2 : column1}
        """
        S1.key_Namehex_dict = {}
        with open(os.getcwd() + "/files/" + fileName, 'r') as file:
            file = file.readlines()[1:]  # way1 :  # skip the first line.
            for line in file:
                if line != "\n":
                    S1.key_Namehex_dict[line.split()[1]] = line.split()[0]
        return S1.key_Namehex_dict

    @staticmethod
    def create_json_file(RDI_list):
        for key in RDI_list:
            S1.init_dict['json_levelA'].append(
                {"sendline": "tsd.persistence.client.mib3.app.GetKey --ns {0} --key {1}".format(
                    S1.key_Namehex_dict.get(key), key)})
            S1.init_dict['json_levelA'].append({"expect": "load: ns: {0} key: {1} slot: 0 ".format(
                S1.key_Namehex_dict.get(key)[2:], str(int(key, 16)))})
        #      {"sendline": "load: ns: {0} key: {1} slot: 0 status: 0".format(ns[3:], str(int(key,16)))})
        S1.init_dict['json_levelA'].append({'sendline': 'sync'})
        S1.init_dict['json_levelA'].append({'sendline': 'exit'})
        # rename key in dictionary
        S1.init_dict['p_setGetKey_script1'] = S1.init_dict.pop('json_levelA')
        return S1.init_dict

    @staticmethod
    def deleteBlankLine(oldFile, newFile):
        """

      :param oldFile: "tempEdit.txt"
      :param newFile: "newTempEdit.txt"
      :return:
      """
        with open(os.getcwd() + '/files/' + oldFile, 'r') as fr, open(os.getcwd() + '/files/' + newFile, 'w',
                                                                      encoding='utf-8') as fd:
            for text in fr.readlines():
                if text.split() != []:
                    fd.write(text)
        print("Success to delete blank line!")



    # @staticmethod


    @staticmethod
    def greenFont(str):
        return "\033[32m" + str + "\033[0m"

    @staticmethod
    def repr_message(message: str):
        padding_len = '%' + str(int(len(message) / 2) + 35) + 's'
        return "\n"+ "=" * 70 + "\n" + padding_len % message + "\n" + "=" * 70 + "\n"

    @staticmethod
    def getFileList(fileDirPath):
        """

        :param fileDirPath:
        :return: absolute path
        """
        return [fileDirPath + "/" + x for x in os.listdir(fileDirPath)]

    def setProjectDir(self, path):
        self.project_dir = path

    def setJsonDir(self, path):
        self.json_dir = self.project_dir + path

    def setToolsDir(self, path):
        self.tools_dir = self.project_dir + path

    def setLogDir(self, path):
        self.log_name = self.project_dir + path

    @staticmethod
    def scp(file, user, host, dir):
        p_command = "scp -r {0} {1}@{2}:{3}".format(file, user, host, dir)
        return p_command

    @staticmethod
    def transfer_files(cls, fileList):
        for i in fileList:
            # print(S1.scp(i,S1.user,S1.ip,S1.dest_dir))
            print("Start to transfer {0} to HU".format(i))
            a = S1.scp(i, S1.user, S1.ip, S1.dest_dir)
            print(cls.adv_doPexpect(p_command=a, json_name="[default]transferFiles.json", jsonpath_command="$.transfer.*"))
            time.sleep(1)
        return True

    def getFilesSha1sum(self):
        # newList = []
        newDict = {}
        for x in self.getFileList(self.tools_dir):
            raw_data = os.popen("sha1sum {0}".format(x), "r").read()
            sha1sum_data = raw_data.split()[0]
            file_name = raw_data[raw_data.rindex("/") + 1:].strip()
            # sha1_List =  [os.popen("sha1sum {0}".format(x),"r").read() for x in self.getFileList(self.tools_dir)]
            # newList.append("{0}    {1}".format(sha1sum_data, file_name))
            newDict[file_name] = sha1sum_data
        return newDict

    def adv_doPexpect(self, p_command, json_name, jsonpath_command, log_name="logs.txt"):  # add on 9/19/2022
        log_name = self.log_name
        log_mode = self.log_mode
        with open(log_name, log_mode) as my_log_file:  # add on 9/19/2022
            p = pexpect.spawn(command=p_command, logfile=my_log_file, encoding='utf-8', timeout=20)
            json_list = S1.get_json_info(self.json_dir + "/" + json_name, jsonpath_command)
            # print(json_list)
            for i in json_list:
                print(i)
                # sys.exit()
                try:
                    S1.pAction(list(i.items())[0], p)
                    # sys.exit()
                except pexpect.TIMEOUT:
                    print(p.before, p.after)
                # print("%s pass"%(i))
            p.expect(pexpect.EOF)  # Add in 9/19/2022
            p.close()
            # return HU.greenFont(HU.repr_message("Success to copy file to HU"))
        return S1.greenFont(S1.repr_message("Successful"))

    # @staticmethod
    @staticmethod
    def get_json_info(json_file_name, jsonPathDesc, codingFormat=None):
        """
      :param json_file_name:
      :param jsonPathDesc:
      :return: dict(json's data)
      """
        import json, jsonpath
        print(S1.repr_message(json_file_name))
        with open(json_file_name, encoding=codingFormat) as json_file:
            data = json.load(json_file)
            res = jsonpath.jsonpath(data, jsonPathDesc)
        return res

    @staticmethod
    def pAction(Jlist, cls=None):
        if Jlist[0] == "expect":
            # print(Jlist[1])
            cls.expect(Jlist[1])
        elif Jlist[0] == "sendline":
            # print(Jlist[1])
            cls.sendline(Jlist[1])

    @staticmethod
    def pAction_v2(Jdist, cls=None, logFile = None):
        """Work way 1"""
        # print("{0}:\t{1}".format("Jdist.keys()",Jdist.keys()))
        # for i in Jdist.keys():
        #     print("{0}:\t{1}".format("i",i))
        #     if Jdist.get(i, None) != None:
        #         print("cls.{0}(\"{1}\")".format(i,Jdist[i]))
        """Work way 2"""
        if Jdist.get("sendline", None) != None:
            # print(Jdist["sendline"])
            # print("{0}.sendline(\"{1}\")\n".format(cls,Jdist["sendline"]))
            # logFile.write("{0}.sendline(\"{1}\")\n".format(cls,Jdist["sendline"]))
            cls.sendline(Jdist["sendline"])
        else:
            raise ValueError("sendline is not given")
        if Jdist.get("expect", None) != None:
            # print(Jdist["expect"])
            # print("{0}.expect(\"{1}\")\n".format(cls,Jdist["expect"]))
            # logFile.write("{0}.expect(\"{1}\")\n".format(cls,Jdist["expect"]))

            cls.expect(Jdist["expect"])
            # temp_str = cls.before
            a = cls.before[:]
            # cls.buffer = ""
            try:
                # print(a)
                # print("@@"*60)
                print("pexpect before of {0}:\t==>>{1}".format("a[a.index(\"data:\") + 5:])",\
                                                               a[a.index("data:") + 5:a.index("\n")]))
                # print("pexpect before of {0}:\t==>>{1}".format("a",\
                #                                                a))
                # sys.exit()

            except ValueError:
                pass
            # print("pexpect before of {0}:\t==>>{1}".format("cls.before[cls.before.index(\"data:\"):]", temp_str[temp_str.index("data:"):]))
        else:
            # raise ValueError("expect is not given")
            print("expect is not given, the sendline is {0}".format(Jdist.get("sendline", None)))

    @staticmethod
    def redFont(str):
        return "\033[31m" + str + "\033[0m"

    def set_pexpect_command(self,json_path,json_file,log_path):
        with open("{0}/{1}".format(json_path,json_file), encoding="utf-8") as json_data,\
                open(log_path,'a')as logs:
        # with open("{0}/{1}".format(json_path, json_file + ".json"), encoding="utf-8") as json_data:
            data = json.load(json_data)
        #     res = jsonpath.jsonpath(data, "$.body..expect")
        #     print("{0}:\n{1}",("res",res))

            spawn_command = jsonpath.jsonpath(data, "$.head..spawn_command")[0]
            logs.write(spawn_command + "\n")
            # print("{0}:\t{1}".format("spawn_command",spawn_command))
            # print("Logs : ", logs)
            if not False:
                logs.write("pexpect.spawn(command={0}, , logfile={1}, encoding={2}, timeout={3})\n".format(spawn_command,logs,"utf-8","20"))
                try:
                    # p = pexpect.spawn(command=spawn_command, logfile=sys.stdout, encoding='utf-8', timeout=10)
                    p = pexpect.spawn(command=spawn_command, logfile=logs, encoding='utf-8', timeout=10)
                    spawn_command_expect = jsonpath.jsonpath(data, "$.head..spawn_command_expect")[0]
                    # print("type of {0} is {1}".format("spawn_command_expect",type(spawn_command_expect)))
                    logs.write("p.expect({0})\n".format(spawn_command_expect))
                    p.expect(spawn_command_expect)
                    # sys.exit()
                    # print(jsonpath.jsonpath(data, "$.head[?(@.expect)]"))
                    for ele_dict in (jsonpath.jsonpath(data, "$.head[?(@.sendline)]"),jsonpath.jsonpath(data, "$.body[?(@.sendline)]"),\
                            jsonpath.jsonpath(data, "$.tail[?(@.sendline)]")):
                        for i in ele_dict:
                            # print("{0}:\t{1}".format("i", i))
                            # S1.pAction_v2(i,cls= p, logFile=sys.stdout)
                            S1.pAction_v2(i, cls=p)
                except pexpect.TIMEOUT:
                    # raise TimeoutError("timeout no match")
                    print(S1.repr_message("pexpect.TIMEOUT"))



class JSON:

    def __init__(self, json_list=[], json_dict={}):
        self.json_list = json_list
        self.json_dict = json_dict
        self.user = "root"
        self.ip = "192.168.1.4"

    def add_send_expect(self, strS, strE):
        # if not self.json_dict.get("expect",None) and not self.json_dict.get("sendline", None):
        newDict = {}
        newDict["sendline"] = strS
        newDict["expect"] = strE
        self.json_list.append(newDict)

    def combineAsJson(self, elementName):
        haed_dict = {
            "{0}".format("head"): [
                {"spawn_command": "ssh {0}@{1}".format(self.user, self.ip), 'expect': 'password'},
                {'sendline': 'root', 'expect': 'root@'},
                {'sendline': 'cd /tmp/','expect': '/tmp'}
            ]
        }
        # haed_dict = {
        #     "elementName{0}".format("head"): [
        #         {{"spawn_command": "ssh {0}@{1}".format(self.user, self.ip)}, {'expect': 'password'}},
        #         {{'sendline': 'root'}, {'expect': 'root@'}}, {{'sendline': 'cd /tmp/'},
        #                                                       {'expect': '/tmp'}}]}
        tail_dict = {'{0}'.format("tail"): [{"sendline": "sync"}, {"sendline": "exit"}]}
        print(elementName)
        self.json_dict[elementName] = self.json_list
        self.json_dict.update(haed_dict)
        self.json_dict.update(tail_dict)
        # self.json_dict[elementName].update(tail_dict)

    def combineAsJson_v2(self):
        haed_dict = {
            "{0}".format("head"): [
                {"spawn_command": "ssh {0}@{1}".format(self.user, self.ip), 'spawn_command_expect': 'password'},
                {'sendline': 'root', 'expect': 'root@'},
                {'sendline': 'cd /tmp/','expect': '/tmp'}
            ]
        }
        tail_dict = {'{0}'.format("tail"): [{"sendline": "sync"}, {"sendline": "exit"}]}
        self.json_dict["body"] = self.json_list
        self.json_dict.update(haed_dict)
        self.json_dict.update(tail_dict)
        # self.json_dict[elementName].update(tail_dict)


    def saveAsFile(self, file_path, file_name):
        json.dump(self.json_dict, open(file_path + "/" + file_name, 'w'), ensure_ascii=False,
                  indent=4, separators=(", ", " : "))
    # @staticmethod
    # def save_like_a_json(jsonData, fileName='ns1000000.json', localPath=os.getcwd() + '/json_sets/'):
    #     return json.dump(jsonData, open(localPath + fileName, 'w'), ensure_ascii=False,
    #                      indent=4, separators=(", ", " : "))




    def __str__(self):
        return "{0}\n{1}".format(self.json_list, self.json_dict)
        # return self.json_dict

if __name__ == '__main__':

    # sys.exit()
    # print(sys.version_info[:])
    # print(os.listdir(os.getcwd()))
    # print(os.path.abspath(os.listdir(os.getcwd())[0]))
    # print(os.path.abspath('tsd.persistence.client.mib3.app.SetKey'))
    #
    # print(sys.argv[0])
    # print(sys.argv[0].split('/'))
    # print(os.path.basename(sys.argv[0]))
    # sys.exit()
    HU = S1()
    # HU.setProjectDir("/home/jpcc/PycharmProjects/pythonProject_Sept_2022/coding_file_version2")
    HU.setProjectDir(os.path.dirname(os.getcwd()))
    HU.setJsonDir("/json")
    HU.setToolsDir("/tools")
    HU.setLogDir("/logs")
    HU.log_name += "/swdl_" + time.strftime("%Y%m%d_%H_%M_%S", time.localtime(time.time())) + ".txt"
    HU.log_mode = "a"
    logFile = "{0}/{1}.txt".format(HU.log_name, "logs" + time.strftime("%Y%m%d_%H_%M_%S", time.localtime(time.time())))
    HU.transfer_files(HU,HU.getFileList(HU.tools_dir))      # transfer files
    print(HU.getFileList(HU.tools_dir))

    # sys.exit()

    pprint.pprint([os.popen("sha1sum {0}".format(x), "r").read() for x in HU.getFileList(HU.tools_dir)])
    print("*" * 60)
    print(HU.getFilesSha1sum())
    # print(HU.json_dir)
    # sys.exit()
    A = JSON()
    for i in HU.getFilesSha1sum().keys():
        A.add_send_expect("sha1sum {0}".format(i), "{0}  {1}".format(HU.getFilesSha1sum()[i], i))
    # A.add_send_expect("root", "root")
    # A.add_send_expect("password", "password")
    json_name = "checksum_files_v2.json"
    # A.combineAsJson(json_name)
    A.combineAsJson_v2()
    print(A.json_dict)
    json_script1 = json.dumps(A.json_dict, indent=4, separators=(", ", " : "))
    print(json_script1)
    A.saveAsFile(HU.json_dir, json_name)
    HU.set_pexpect_command(HU.json_dir, json_name, HU.log_name)
    # print(json.load(A.json_dict))

    # print("{{}{0}{}}".format((str(A.json_dict))))
    # print(json.loads("{{}{0}{}}".format((str(A.json_dict)))))

    # pprint.pprint(HU.getFilesSha1sum())
    # import hashlib
    # pprint.pprint([hashlib.sha1(x.encode()).hexdigest() for x in HU.getFileList(HU.tools_dir)])
    # sys.exit()
