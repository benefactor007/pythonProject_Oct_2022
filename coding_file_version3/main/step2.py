"""
pls use python3 or above. This program is based on Python3.5
"""
import pprint
import time

from peri_step1 import P_step1
import os, sys, pexpect, json, jsonpath

# My file: rawData_GetKey_0929.json
""" 
    "error_key_data_list" : [
        {
            "status" : " 8 ", 
            "ns" : "0x1000000", 
            "key" : "0x0501", 
            "data" : " "
        }, 
        ],

   "key_data_list" : [
        {
            "ns" : "0x1000000", 
            "key" : "0x0B39", 
            "data" : " 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 0 "
        }, 
        ]
"""


class P_step2(P_step1):
    def __init__(self):
        P_step1.__init__(self)
        self.project_folder = ""
        self.json_folder = ""
        self.codingFiles_folder = ""
        self.errors_folder = ""
        self.logs_folder = ""
        self.tools_folder = ""
        self.trash_folder = ""

    def setProjectDir(self, path):
        self.project_folder = path

    # vital_folder_list = ["codingFiles", "errors", "json", "logs", "tools", "trash"]

    def setJsonDir(self, json_folder):
        self.json_folder = self.project_folder + os.sep + json_folder

    def setCodingDir(self, codingFiles_folder):
        self.codingFiles_folder = self.project_folder + os.sep + codingFiles_folder

    def setErrorDir(self, errors_folder):
        self.errors_folder = self.project_folder + os.sep + errors_folder

    def setLogDir(self, logs_folder):
        self.logs_folder = self.project_folder + os.sep + logs_folder

    def setToolDir(self, tools_folder):
        self.tools_folder = self.project_folder + os.sep + tools_folder

    def setTrashDir(self, trash_folder):
        self.trash_folder = self.project_folder + os.sep + trash_folder

    def check_folder_exist(self, folder_name):
        if self.project_folder:
            if os.path.isdir(self.project_folder + os.sep + folder_name):
                print(f"{folder_name} is under the project directory")
            else:
                print(f"{folder_name} is not under the project directory\n"
                      f"Now, creating a new directory which named as {folder_name}")
                os.mkdir(self.project_folder + os.sep + folder_name)
        else:
            print(f"self.project_folder is {self.project_folder}\n"
                  f"pls define your project directory!!!")

    # @staticmethod
    def get_json_info(self, json_name, jsonPathDesc, codingFormat=None):
        """
      :param json_file_name:
      :param jsonPathDesc:
      :return: dict(json's data)
      """
        import json, jsonpath
        json_file_path = self.json_folder + os.sep + json_name
        print(f"{json_file_path} is a file: {os.path.isfile(json_file_path)}")
        with open(json_file_path, encoding=codingFormat) as json_file:
            data = json.load(json_file)
            res = jsonpath.jsonpath(data, jsonPathDesc)
        return res


class Scp(P_step2):
    def __init__(self):
        P_step2.__init__(self)
        self.fileList = []
        self.ip = "192.168.1.4"
        self.user = "root"
        self.hu_dir = "/tmp"

    def add_send_expect(self, strS, strE):
        # if not self.json_dict.get("expect",None) and not self.json_dict.get("sendline", None):
        newDict = {}
        newDict["sendline"] = strS
        newDict["expect"] = strE
        self.json_list.append(newDict)

    # @staticmethod
    def scp(self, file):
        p_command = "scp -r {0} {1}@{2}:{3}".format(file, self.user, self.ip, self.hu_dir)
        return p_command

    # @staticmethod
    def transfer_files(self, fileList):
        for i in fileList:
            # print(S1.scp(i,S1.user,S1.ip,S1.dest_dir))
            print("Start to transfer {0} to HU".format(i))
            # user, ip, target_dir = "root", "192.168.1.4", "/tmp"
            a = self.scp(i)
            print(self.adv_doPexpect(p_command=a, json_name="[default]transferFiles.json", jsonpath_command="$.transfer.*", log_path= self.log_path))
            time.sleep(1)
        return True

    @staticmethod
    def getFileList(fileDirPath):
        """

        :param fileDirPath:
        :return: absolute path
        """
        return [fileDirPath + "/" + x for x in os.listdir(fileDirPath)]

    def setFileList(self, path):
        self.fileList = [path + "/" + x for x in os.listdir(path)]

    # @staticmethod
    def getSha1sum(self, file):
        if isinstance(file, str):
            return os.popen("sha1sum {0}".format(file), "r").read()
        elif isinstance(file, list) and self.fileList:
            return [os.popen("sha1sum {0}".format(x), "r").read() for x in self.fileList]

    @staticmethod
    def get_json_info(json_path, jsonPathDesc, codingFormat=None):
        """
      :param json_file_name:
      :param jsonPathDesc:
      :return: dict(json's data)
      """
        import json, jsonpath
        print(Scp.repr_message(json_path))
        with open(json_path, encoding=codingFormat) as json_file:
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

    def adv_doPexpect(self, p_command, json_name, jsonpath_command, log_path):  # add on 9/19/2022
        with open(log_path, "a") as logs:  # add on 9/19/2022
            p = pexpect.spawn(command=p_command, logfile=logs, encoding='utf-8', timeout=20)
            json_list = self.get_json_info(self.json_folder + "/" + json_name, jsonpath_command)
            # print(json_list)
            for i in json_list:
                print(i)
                # sys.exit()
                try:
                    Scp.pAction(list(i.items())[0], p)
                    # sys.exit()
                except pexpect.TIMEOUT:
                    print(p.before, p.after)
                # print("%s pass"%(i))
            p.expect(pexpect.EOF)  # Add in 9/19/2022
            p.close()
            # return HU.greenFont(HU.repr_message("Success to copy file to HU"))
        return Scp.greenFont(Scp.repr_message("Successful"))

    @staticmethod
    def pAction_v2(Jdist, cls=None, logFile=None):
        if Jdist.get("sendline", None) != None:
            cls.sendline(Jdist["sendline"])
        else:
            raise ValueError("sendline is not given")
        if Jdist.get("expect", None) != None:

            print(f"Jdist.get(\"expect\") : {Jdist.get('expect')}")

            cls.expect(Jdist["expect"])
            print(P_step1.greenFont(cls.after))
        else:
            cls.buffer = ""
            print("expect is not given, the sendline is {0}".format(Jdist.get("sendline", None)))


    def set_pexpect_command(self, json_path, json_file, log_path):
        with open("{0}/{1}".format(json_path, json_file), encoding="utf-8") as json_data, \
                open(log_path, 'a')as logs:
            data = json.load(json_data)
            spawn_command = jsonpath.jsonpath(data, "$.head..spawn_command")[0]
            logs.write(spawn_command + "\n")
            if not False:
                logs.write(
                    "pexpect.spawn(command={0}, , logfile={1}, encoding={2}, timeout={3})\n".format(spawn_command, logs,
                                                                                                    "utf-8", "20"))
                try:
                    p = pexpect.spawn(command=spawn_command, logfile=logs, encoding='utf-8', timeout=10)
                    spawn_command_expect = jsonpath.jsonpath(data, "$.head..spawn_command_expect")[0]
                    logs.write("p.expect({0})\n".format(spawn_command_expect))
                    p.expect(spawn_command_expect)
                    for ele_dict in (
                            jsonpath.jsonpath(data, "$.head[?(@.sendline)]"),
                            jsonpath.jsonpath(data, "$.body[?(@.sendline)]"),
                            jsonpath.jsonpath(data, "$.tail[?(@.sendline)]")):
                        # pprint.pprint(ele_dict)
                        for i in ele_dict:
                            P_step1.pAction_v2(i, cls=p)
                except pexpect.TIMEOUT:
                    print(P_step1.repr_message("pexpect.TIMEOUT"))

if __name__ == '__main__':
    step2 = P_step2()
    step2.setProjectDir(os.path.split(os.getcwd())[0])
    step2.setJsonDir("json")
    step2.setTrashDir("trash")
    step2.setToolDir("tools")
    step2.setErrorDir("errors")
    step2.setCodingDir("codingFiles")
    step2.setLogDir("logs")
    vital_folder_list = ["codingFiles", "errors", "json", "logs", "tools", "trash"]

    """
    transfer files
    """
    tt1 = Scp()
    tt1.setProjectDir(os.path.split(os.getcwd())[0])
    tt1.setToolDir("tools")
    tt1.setJsonDir("json")
    tt1.setToolDir("tools")
    tt1.setLogDir("logs")
    tt1.setFileList(tt1.tools_folder)
    tt1.log_path = ""
    tt1.log_path = tt1.logs_folder + os.sep + "trans_task_" + time.strftime("%Y%m%d_%H_%M_%S",
                                                                            time.localtime(
                                                                                              time.time())) + ".txt"
    tt1.transfer_files(tt1.getFileList(tt1.tools_folder))             # important, copy files to HU

    for i in tt1.fileList:
        # print(f"os.path.split(i)[-1] : {os.path.split(i)[-1]}")
        # print(f"tt1.getSha1sum(i).split()[0] : {tt1.getSha1sum(i).split()[0]}")
        tt1.add_send_expect(f"sha1sum {os.path.split(i)[-1]}", f"{tt1.getSha1sum(i).split()[0]}  {os.path.split(i)[-1]}")
    tt1.combineAsJson_v2()
    pexpect_output_json = "file_checksum_expect.json"
    tt1.saveFile(tt1.json_folder, pexpect_output_json, tt1.json_dict)
    tt1.set_pexpect_command(tt1.json_folder, pexpect_output_json, tt1.log_path)
    # sys.exit()







    # sys.exit()

    for i in vital_folder_list:
        step2.check_folder_exist(i)

    print(step2.__init__.__code__.co_varnames)  # ('self',)
    # print(dir(step2))
    print(vars(step2))
    for i, j in vars(step2).items():
        print(f"{i} : {j}")

    print(__file__)
    current_file_name = os.path.basename(__file__).split(".")[0]
    print(current_file_name)
    # set auto log file generation
    step2.log_path = ""
    step2.error_path = ""
    step2.log_path = step2.logs_folder + os.sep + current_file_name + "_" + time.strftime("%Y%m%d_%H_%M_%S",
                                                                                          time.localtime(
                                                                                              time.time())) + ".txt"
    step2.error_path = step2.errors_folder + os.sep + time.strftime("%Y%m%d_%H_%M_%S",
                                                                    time.localtime(time.time())) + ".txt "
    # step2.error_name = step2.errors_folder + os.sep + "error" + "_" time.strftime("%Y%m%d_%H_%M_%S", time.localtime(time.time())) + ".txt"
    step2.error_path = f"{step2.errors_folder + os.sep}error_{time.strftime('%Y%m%d_%H_%M_%S', time.localtime(time.time()))}.txt"
    print(f"step2.log_path is {step2.log_path}\n"
          f"step2.error_path is  {step2.error_path}")
    #### Here: pls assign the value here ####
    pexpect_exec_json = "toGet_nsKey_VW_GP_v09_1013.json"
    # pexpect_output_json = "rawData_toGet_nsKey_1011.json"
    pexpect_output_json = "codingFile_GetKey_checklist.json"
    ##########################################

    step2.set_pexpect_command_v2(step2.json_folder, pexpect_exec_json, step2.log_path, step2.error_path)
    step2.json_dict = dict(
        zip(["key_data_list", "error_key_data_list"], [step2.key_data_list, step2.error_key_data_list]))
    step2.saveAsFile(step2.json_folder, pexpect_output_json, step2.json_dict)

    sys.exit()
