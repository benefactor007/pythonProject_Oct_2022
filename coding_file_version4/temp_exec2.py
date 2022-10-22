#! /usr/bin/env python3
import json
import os, sys, pexpect
import pprint

import subprocess
import time

import jsonpath


def check_ping(address="192.168.1.4"):
    str1 = 'ping -c 3 '
    str2 = address
    str3 = ' | grep \'0 received\' | wc -l'
    command = str1 + str2 + str3
    print(command)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    result = p.stdout.read()
    return result.strip().decode("utf-8")

def time_sleep(data):
    for x in range(data, -1, -1):
        mystr = str('休眠倒计时:') + str(x) + "S"
        print("\r", mystr, end="", flush=True)
        time.sleep(1)

def main_action():
    while True:
        if check_ping("192.168.1.4") == "0":
            break
        else:
            pass
    p = pexpect.spawn("ssh root@192.168.1.4", logfile=sys.stdout, encoding="utf-8", timeout=10)
    p.expect("password")
    p.sendline("root")
    p.expect("root@")
    # p.expect("infotainment")
    print("\n")
    print("*" * 60)
    print(f"p.buffer: {p.buffer}")
    print(f"p.before: {p.before}")
    print(f"p.after: {p.after}")
    print("*" * 60)
    p.buffer = ""
    if p.before:
        p.expect(r'.+')
    p.sendline("disable-dm-verity.sh")
    index = p.expect(["Connection to 192.168.1.4 closed.", pexpect.TIMEOUT, pexpect.EOF, "infotainment"])
    if index == 0:
        print("match connection")
        # time.sleep(20)
        time_sleep(20)
        main_action()
    elif index == 1:
        print("pexpect.TIMEOUT")
    elif index == 2:
        print("pexpect.EOF")
    elif index == 3:
        print("match infotainment, scripts should run")
        nextStep()
        # sys.exit()


from peri_step1 import P_step1


class sub_P_step1(P_step1):
    def __init__(self,logPath, errorPath):
        P_step1.__init__(self)
        self.logPath = logPath
        self.errorPath = errorPath


    def set_pexpect_command(self, json_path, log_path):
        with open(json_path, encoding="utf-8") as json_data, \
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

    def set_pexpect_command_v2(self, json_path, log_path, error_path):
        with open(json_path, encoding="utf-8") as json_data,open(log_path, 'a')as logs, open(error_path, 'a') as errors:
            data = json.load(json_data)
            spawn_command = jsonpath.jsonpath(data, "$.head..spawn_command")[0]
            logs.write(spawn_command + "\n")
            if not False:
                logs.write(
                    "pexpect.spawn(command={0}, , logfile={1}, encoding={2}, timeout={3})\n".format(spawn_command,
                                                                                                    logs,
                                                                                                    "utf-8", "20"))
                try:
                    p = pexpect.spawn(command=spawn_command, logfile=logs, encoding='utf-8', timeout=10)
                    spawn_command_expect = jsonpath.jsonpath(data, "$.head..spawn_command_expect")[0]
                    logs.write("p.expect({0})\n".format(spawn_command_expect))
                    p.expect(spawn_command_expect)

                    ele_dict = jsonpath.jsonpath(data, "$.head[?(@.sendline)]")
                    for i in range(len(ele_dict)):
                        P_step1.pAction_v2(ele_dict[i], cls=p)
                    ele_dict = jsonpath.jsonpath(data, "$.body[?(@.sendline)]")
                    for i in range(len(ele_dict)):
                        if i > 0:
                            P_step1.pAction_v2(ele_dict[i], cls=p)
                            pre_key = ele_dict[i - 1].get("key", None)
                            pre_ns = ele_dict[i - 1].get("ns", None)
                            current_key = ele_dict[i].get("key", None)
                            a = p.before[:]
                            try:
                                # print(a)
                                if current_key and a.strip().startswith("status: 0"):
                                    pre_status = a[a.index("status:") + 7:a.index("data")].strip()
                                    print("{0}:\t{1}".format("pre_state", pre_status))
                                    pre_data = a[a.index("data:") + 5:a.index("\r")]
                                    print("{0}:\t{1}".format("pre_data", pre_data))
                                    self.key_data_list.append(dict(zip(["ns", "key", "data", "status"],
                                                                       [pre_ns, pre_key, pre_data,
                                                                        pre_status])))
                                else:
                                    pre_status = a[a.index("status:") + 7:a.index("data")].strip()
                                    print("{0}:\t{1}".format("pre_state", pre_status))
                                    pre_data = a[a.index("data:") + 5:a.index("\r")]
                                    print("{0}:\t{1}".format("pre_data", pre_data))
                                    self.error_key_data_list.append(dict(zip(["ns", "key", "data", "status"],
                                                                             [pre_ns, pre_key, pre_data,
                                                                              pre_status])))
                            except ValueError:
                                errors.write(
                                    "{0}\n{1} error \n {2} \n".format("ValueError", "set_pexpect_command_v2", a))
                                print(P_step1.repr_message(a))
                        else:
                            P_step1.pAction_v2(ele_dict[i], cls=p)
                            current_key = ele_dict[i].get("key", None)
                            print("{0}:\t{1}".format("current_key", current_key))
                    ele_dict = jsonpath.jsonpath(data, "$.tail[?(@.sendline)]")
                    for i in range(len(ele_dict)):
                        P_step1.pAction_v2(ele_dict[i], cls=p)
                except pexpect.TIMEOUT:
                    print(P_step1.repr_message("pexpect.TIMEOUT"))

    def scp(self, file):
        p_command = f"scp -r {file} root@192.168.1.4:/var"
        # p_command = "scp -r {0} {1}@{2}:{3}".format(file, self.user, self.ip, self.hu_dir)
        return p_command

        # @staticmethod

    # @staticmethod
    def pAction(self,Jlist, cls=None):
        if Jlist[0] == "expect":
            # print(Jlist[1])
            cls.expect(Jlist[1])
        elif Jlist[0] == "sendline":
            # print(Jlist[1])
            cls.sendline(Jlist[1])

    # @staticmethod
    def greenFont(self,str):
        return "\033[32m" + str + "\033[0m"

    # @staticmethod
    def repr_message(self,message: str):
        padding_len = '%' + str(int(len(message) / 2) + 35) + 's'
        return "\n" + "=" * 70 + "\n" + padding_len % message + "\n" + "=" * 70 + "\n"

    def get_json_info(self,jsonPath, jsonPathDesc, codingFormat=None):
        """
      :param json_file_name:
      :param jsonPathDesc:
      :return: dict(json's data)
      """
        import json, jsonpath
        # print(P_step1.repr_message(json_file_name))
        with open(jsonPath, encoding=codingFormat) as json_file:
            data = json.load(json_file)
            res = jsonpath.jsonpath(data, jsonPathDesc)
        return res

    def adv_doPexpect(self, p_command, json_path, jsonpath_command, log_path):  # add on 9/19/2022
        with open(log_path, "a") as logs:  # add on 9/19/2022
            p = pexpect.spawn(command=p_command, logfile=logs, encoding='utf-8', timeout=20)
            json_list = self.get_json_info(json_path, jsonpath_command)
            # print(json_list)
            for i in json_list:
                print(i)
                # sys.exit()
                try:
                    self.pAction(list(i.items())[0], p)
                    # sys.exit()
                except pexpect.TIMEOUT:
                    print(p.before, p.after)
                # print("%s pass"%(i))
            p.expect(pexpect.EOF)  # Add in 9/19/2022
            p.close()
            # return HU.greenFont(HU.repr_message("Success to copy file to HU"))
        return self.greenFont(self.repr_message("Successful"))


    def transfer_files(self, fileList, jsonPath):
        for i in fileList:
            # print(S1.scp(i,S1.user,S1.ip,S1.dest_dir))
            print("Start to transfer {0} to HU".format(i))
            # user, ip, target_dir = "root", "192.168.1.4", "/tmp"
            a = self.scp(i)
            print(self.adv_doPexpect(p_command=a, json_path = jsonPath,
                                     jsonpath_command="$.transfer.*", log_path=self.logPath))
            time.sleep(1)
        return True





def nextStep():
    logPath = os.getcwd() + os.sep + "logs_" + time.strftime("%Y%m%d") + ".txt"
    errorPath = os.getcwd() + os.sep + "errors_" + time.strftime("%Y%m%d") + ".txt"
    WD_partnum = sub_P_step1(logPath,errorPath)
    # def set_pexpect_command_v2(self, json_path, log_path, error_path):
    # HU_exec.set_pexpect_command_v1(HU_exec.json_folder, "[default]transfer_files_to_var.json", HU_exec.log_path)
    toolsPath = os.getcwd() + os.sep + "tools"
    toolsPathList = [toolsPath + os.sep + file for file in os.listdir(toolsPath)]
    print(f"toolsPathList: {toolsPathList}")
    jsonPath = os.getcwd() + os.sep + "[default]transferFiles.json"
    WD_partnum.transfer_files(toolsPathList, jsonPath)
    print(WD_partnum.greenFont("Transfer was successfully finished"))
    # pprint.pprint(WD_partnum.json_dict)
    # pprint.pprint(WD_partnum.json_list)
    if WD_partnum.json_list or WD_partnum.json_dict:
        WD_partnum.json_list, WD_partnum.json_dict = [],{}
    else:
        pass
    # sys.exit()
    jsonPath = "file_checksum_expect.json"
    # logPath = os.getcwd() + os.sep + "logs_" + time.strftime("%Y%m%d") + ".txt"
    # errorPath = os.getcwd() + os.sep + "errors_" + time.strftime("%Y%m%d") + ".txt"
    WD_partnum.set_pexpect_command(jsonPath, logPath)
    if WD_partnum.json_list or WD_partnum.json_dict:
        WD_partnum.json_list, WD_partnum.json_dict = [],{}
    else:
        pass
    print(WD_partnum.greenFont("files was successfully double checked"))





    # WD_partnum.json_dict, WD_partnum.json_list = {},[]
    # print(f"os.getcwd(): {os.getcwd()}")
    # jsonPath = os.getcwd() + os.sep + "SetKey_pers_partNum_5HG035866F.json"
    #
    # # json_path = os.getcwd()
    # WD_partnum.set_pexpect_command_v2(jsonPath, logPath, errorPath)





if __name__ == '__main__':
    main_action()
    # nextStep()
    logPath = os.getcwd() + os.sep + "logs_" + time.strftime("%Y%m%d") + ".txt"
    fazitPath = os.getcwd() + os.sep + "fazit_" + time.strftime("%Y%m%d") + ".txt"
    with open(logPath, 'a') as logs, open(fazitPath,"a") as fazits:
        s = pexpect.spawn("ssh root@192.168.1.4", logfile=logs, encoding="utf-8", timeout=10)
        s.expect("password")
        s.sendline("root")
        s.expect("infotainment")
        s.sendline("mount-read-write.sh")
        s.expect("infotainment")
        s.sendline("cd /var")
        s.expect("/var")
        s.sendline("scp -r -v tsd.persistence.client.mib3.app.SetKey /usr/bin")
        s.expect("#")
        s.sendline("scp -r -v tsd.persistence.client.mib3.app.GetKey /usr/bin")
        s.expect("#")
        s.sendline("cd /usr/bin")
        s.expect("/usr/bin")
        s.sendline("sha1sum tsd.persistence.client.mib3.app.SetKey")
        s.expect("4e9d90211063684bf2ce56b3f9bf94cefc141fa4  tsd.persistence.client.mib3.app.SetKey")
        s.sendline("sha1sum tsd.persistence.client.mib3.app.GetKey")
        s.expect("880152e334d675794bea1f3616d1c94c147c1962  tsd.persistence.client.mib3.app.GetKey")
        logs.write("="*30 + "base-identification" + "="*30 + "\n")
        s.sendline("./tsd.persistence.client.mib3.app.GetKey --ns 0x3000000 --key 0xF17C")
        s.expect("load: ns: 3000000 key: 61820 slot: 0 status: 0")
        s.sendline("./tsd.persistence.client.mib3.app.GetKey --ns 0x3000000 --key 0xF1A3")
        s.expect("load: ns: 3000000 key: 61859 slot: 0 status: 0")
        # print(f"s2.before: {s.before}")
        print(s.before.split("\n")[0])
        fazits.write(s.before.split("\n")[0] + "\n")
        s.sendline("./tsd.persistence.client.mib3.app.GetKey --ns 0x3000000 --key 0xF189")
        s.expect("load: ns: 3000000 key: 61833 slot: 0 status: 0")
        logs.write("=" * 79 + "\n")
        s.sendline("./tsd.persistence.client.mib3.app.SetKey --ns 0x80000008 --key 0x00 --val 0xe5")
        # s.expect("store: ns: 80000008 key: 0 slot: 0")
        s.expect("store: ns: 80000008 key: 0 slot: 0 status: 0 data: e5")
        s.sendline("./tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF187 --val 0x3548473033353836364620")
        # s.expect("store: ns: 3000000 key: 61831 slot: 0")
        s.expect("store: ns: 3000000 key: 61831 slot: 0 status: 0 data: 35 48 47 30 33 35 38 36 36 46 20")
        s.sendline("./tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF191 --val 0x3548473033353836364620")
        # s.expect("store: ns: 3000000 key: 61841 slot: 0")
        s.expect("store: ns: 3000000 key: 61841 slot: 0 status: 0 data: 35 48 47 30 33 35 38 36 36 46 20")
        s.sendline("sync")
        s.expect("infotainment")
        s.sendline("exit")
        # s.sendline("reboot")
        s.expect("Connection to 192.168.1.4 closed")


    green_str = "\033[32m" + "Done!!!!!!" + "\033[0m"
    padding_len = '%' + str(int(len(green_str) / 2) + 35) + 's'
    print("\n" + "=" * 70 + "\n" + padding_len % green_str + "\n" + "=" * 70 + "\n")





