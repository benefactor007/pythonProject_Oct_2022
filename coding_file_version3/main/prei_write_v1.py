import json
import os
import pprint
import sys
import time

import jsonpath
import pexpect

from peri_step1 import P_step1
from step2 import Scp

class P_step1_v2(Scp):
    def __init__(self, json_list=[], json_dict={}):
        Scp.__init__(self)
        self.json_list = json_list
        self.json_dict = json_dict
    # @staticmethod
    # def saveAsFile(file_path, file_name, json_data):
    #     path = P_step1_v2.auto_save_file(file_path + "/" + file_name)
    #     json.dump(json_data, open(path, 'w'), ensure_ascii=False,
    #               indent=4, separators=(", ", " : "))
    #     # print("{0} is {1}".format("path",path))
    #     return path
    #
    # @staticmethod
    # def saveFile(file_path, file_name, json_data):
    #     path = file_path + os.sep + file_name
    #     json.dump(json_data, open(path, 'w'), ensure_ascii=False,
    #               indent=4, separators=(", ", " : "))
    #     # print("{0} is {1}".format("path",path))
    #     return path

    def add_send_expect_v2(self, strS, strE):
        # exec script only:
        newDict = {}
        newDict["sendline"] = strS
        newDict["expect"] = strE
        self.json_list.append(newDict)

    def set_pexpect_command_v1(self, json_path, json_file, log_path):
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
                    p = pexpect.spawn(command=spawn_command, logfile=sys.stdout, encoding='utf-8', timeout=10)
                    spawn_command_expect = jsonpath.jsonpath(data, "$.head..spawn_command_expect")[0]
                    logs.write("p.expect({0})\n".format(spawn_command_expect))
                    p.expect(spawn_command_expect)
                    for ele_dict in (
                            jsonpath.jsonpath(data, "$.head[?(@.sendline)]"),
                            jsonpath.jsonpath(data, "$.body[?(@.sendline)]"), \
                            jsonpath.jsonpath(data, "$.tail[?(@.sendline)]")):
                        for i in range(len(ele_dict)):
                            P_step1_v2.pAction_v3(ele_dict[i], cls=p)
                except pexpect.TIMEOUT:
                    print(P_step1_v2.repr_message("pexpect.TIMEOUT"))

    @staticmethod
    def pAction_v3(Jdist, cls=None, logFile=None):
        if Jdist.get("sendline", None) != None:
            cls.sendline(Jdist["sendline"])
        else:
            raise ValueError("sendline is not given")
        if Jdist.get("expect", None) != None:
            if isinstance(Jdist.get("expect", None), list) == True: # check if the given is list
                print(f'Jdist[\"expect\"]: {Jdist["expect"]}')
                index = cls.expect([Jdist["expect"][0],pexpect.TIMEOUT,pexpect.EOF,Jdist["expect"][1]])
                if index == 0:
                    print(f"index: {index}")
                    print("We're in status 0")
                    pass
                elif index == 1:
                    print(f"index: {index}")
                    print("pexpect.TIMEOUT")
                elif index == 2:
                    print(f"index: {index}")
                    print("pexpect.EOF")
                elif index == 3:
                    print(f"index: {index}")
                    print("We're in status 3")
                    pass
            else:
                cls.expect(Jdist["expect"])
        else:
            cls.buffer = ""
            print("expect is not given, the sendline is {0}".format(Jdist.get("sendline", None)))


def persistence_set_key():
    HU_set = P_step1()
    # print("*"*60)
    # print(HU_set.json_dict)
    # print("*"*60)
    # print("*" * 60)
    # print(HU_set.json_list)
    # print("*" * 60)
    HU_set.json_list = []
    HU_set.setProjectDir(os.path.dirname(os.getcwd()))
    HU_set.setJsonDir("/json")
    HU_set.set_codingFiles("/codingFiles")
    HU_set.setLogDir("/logs")
    HU_set.log_name += "/step2_" + time.strftime("%Y%m%d_%H_%M_%S", time.localtime(time.time())) + ".txt"
    HU_set.setErrorDir("/errors")
    HU_set.error_name += "/error_" + time.strftime("%Y%m%d_%H_%M_%S", time.localtime(time.time())) + ".txt"
    print("{0}:\t{1}".format("HU_set.codingFiles_dir", HU_set.codingFiles_dir))
    # json_name = "persistence.json"
    ####HERE: pls assign value here####
    # HU_set.set_nsKey_dict("persistenceOverview_wData_0929.txt")

    HU_set.set_nsKey_dict("pers_partNum_5HG035866F.txt")
    ####pls assign value above####
    HU_set.setJsonDir("/json")
    print("{0}:\t{1}".format("HU.json_dir", HU_set.json_dir))
    HU_set.saveFile(HU_set.json_dir, "pers_partNum_5HG035866F.json", HU_set.nsKey_dict_list)
    # sys.exit()
    rawDataFile = HU_set.json_dir + "/" + "pers_partNum_5HG035866F.json"
    ns_list = HU_set.get_json_info(rawDataFile, "$..Namespace_hex", codingFormat="utf_8_sig")
    key_list = HU_set.get_json_info(rawDataFile, "$..Key", codingFormat="utf_8_sig")
    data_list = HU_set.get_json_info(rawDataFile, "$..Data", codingFormat="utf_8_sig")
    for ns, key, data in zip(ns_list, key_list, data_list):
        if ns.startswith("0x") and key.startswith("0x"):
            HU_set.add_send_expect(
                strS="./tsd.persistence.client.mib3.app.SetKey --ns {0} --key {1} --val 0x{2}".format(ns, key, data) \
                , strE="store: ns: {0} key: {1} slot: 0".format(ns[2:], int(key, 16)), \
                str_ns=ns, str_key=key, str_data=data)
    HU_set.combineAsJson_v2("/usr/bin")  # In this func, it sets the self.json_dict
    HU_set.saveFile(HU_set.json_dir, "SetKey_" + "pers_partNum_5HG035866F.json", HU_set.json_dict)
    HU_set.set_pexpect_command_v2(HU_set.json_dir, "SetKey_" + "pers_partNum_5HG035866F.json", HU_set.log_name, HU_set.error_name)
    pprint.pprint(HU_set.key_data_list)

if __name__ == '__main__':
    import subprocess



    def check_ping(address = "192.168.1.4"):
        str1 = 'ping -c 3 '
        str2 = address
        str3 = ' | grep \'0 received\' | wc -l'
        command = str1 + str2 + str3
        print(command)
        p = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
        result = p.stdout.read()
        return result.strip().decode("utf-8")


    while True:
        if check_ping("192.168.1.4") == "0":
            break
        else:
            pass

    from step2 import transfer
    transfer("/var")

    # sys.exit()
    HU_exec = P_step1_v2()
    HU_exec.setProjectDir(os.path.dirname(os.getcwd()))
    HU_exec.setJsonDir("json")
    HU_exec.setLogDir("logs")
    HU_exec.log_path = HU_exec.logs_folder + "/HU_exec_" + time.strftime("%Y%m%d_%H_%M_%S",
                                                                         time.localtime(time.time())) + ".txt"
    HU_exec.add_send_expect_v2(strS = "disable-dm-verity.sh", strE = ["Connection","infotainment"])
    HU_exec.combineAsJson_v2("/var")
    HU_exec.saveFile(HU_exec.json_folder, "[default]exec_disable-dm-verity.json", HU_exec.json_dict)
    HU_exec.set_pexpect_command_v1(HU_exec.json_folder, "[default]exec_disable-dm-verity.json", HU_exec.log_path)
    # sys.exit()

    HU_exec = P_step1_v2()
    HU_exec.json_list = []
    HU_exec.setProjectDir(os.path.dirname(os.getcwd()))
    HU_exec.setJsonDir("json")
    HU_exec.setLogDir("logs")
    HU_exec.log_path = HU_exec.logs_folder +  "/HU_exec_" + time.strftime("%Y%m%d_%H_%M_%S", time.localtime(time.time())) + ".txt"
    HU_exec.add_send_expect_v2(strS="mount-read-write.sh", strE = "infotainment")
    HU_exec.add_send_expect_v2(strS="scp -r tsd.persistence.client.mib3.app.* /usr/bin", strE="infotainment")
    HU_exec.add_send_expect_v2(strS="cd /usr/bin", strE="/usr/bin")
    HU_exec.setToolDir("tools")
    HU_exec.setFileList(HU_exec.tools_folder)
    for i in HU_exec.fileList:
        HU_exec.add_send_expect(f"sha1sum {os.path.split(i)[-1]}",
                            f"{HU_exec.getSha1sum(i).split()[0]}  {os.path.split(i)[-1]}")
    HU_exec.combineAsJson_v2("/var")
    HU_exec.saveFile(HU_exec.json_folder, "[default]transfer_files_to_var.json", HU_exec.json_dict)
    HU_exec.set_pexpect_command_v1(HU_exec.json_folder, "[default]transfer_files_to_var.json", HU_exec.log_path)
    # sys.exit()

    persistence_set_key()
    os.system("rm -rf /home/jpcc/PycharmProjects/pythonProject_Oct_2022/coding_file_version3/logs/*")

