#! /usr/bin/env python3
import binascii
import json
import os, sys, pexpect
import pprint

import subprocess
import time

import jsonpath

def str_to_hexStr(str_info):
    return binascii.hexlify(str_info.encode('utf-8')).decode('utf-8')


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
    print(f"os.getcwd() => {os.getcwd()}")
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
        time_sleep(30)
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
      :return: dict(fazit_clip's data)
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
    print("to exec. os.chdir")
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    logPath = os.getcwd() + os.sep + "logs_" + time.strftime("%Y%m%d") + ".txt"
    errorPath = os.getcwd() + os.sep + "errors_" + time.strftime("%Y%m%d") + ".txt"
    WD_partnum = sub_P_step1(logPath,errorPath)
    # def set_pexpect_command_v2(self, json_path, log_path, error_path):
    # HU_exec.set_pexpect_command_v1(HU_exec.json_folder, "[default]transfer_files_to_var.fazit_clip", HU_exec.log_path)
    # toolsPath = os.getcwd() + os.sep + "tools"
    toolsPath = os.path.split(os.getcwd())[0] + os.sep + "tools"
    print(f"toolsPath => {toolsPath}")
    toolsPathList = [toolsPath + os.sep + file for file in os.listdir(toolsPath)]
    print(f"toolsPathList: {toolsPathList}")
    jsonPath = os.path.split(os.getcwd())[0] + os.sep + "[default]transferFiles.json"
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
    # jsonPath = os.getcwd() + os.sep + "SetKey_pers_partNum_5HG035866F.fazit_clip"
    #
    # # json_path = os.getcwd()
    # WD_partnum.set_pexpect_command_v2(jsonPath, logPath, errorPath)

def redFont(str):
    return "\033[31m" + str + "\033[0m"



if __name__ == '__main__':
    from Get_key_step1 import final_get_vaild_fazit,final_change_fazit_status,set_real_cwd,final_change_data_status,final_get_vaild_data,final_reset_data



    # fazitPath = os.getcwd() + os.sep + "fazit_" + time.strftime("%Y%m%d") + ".txt"
    givenBrand = "SVW"          # set before run
    givenFazitJson = "svw_fazit.json" # set before run
    # givenBrand = "FAW"  # set before run
    # givenFazitJson = "faw_fazit.json"  # set before run


    # # test, delete after success
    # os.chdir(os.path.abspath(os.path.dirname(__file__)))
    # print(f"set cwd to {os.path.abspath(os.path.dirname(__file__))}")
    # fazit_clip_dir = os.path.split(os.getcwd())[0] + os.sep + "fazit_clip"
    # fazit_jsonPath = fazit_clip_dir + os.sep + givenFazitJson
    # fazit_jsonPath = '/home/jpcc/PycharmProjects/pythonProject_Oct_2022/3GB035866D/fazit_clip/svw_fazit.json'
    # valid_fazit = final_get_vaild_data(fazit_jsonPath, givenBrand, "fazit")
    # print(f"valid_fazit : {valid_fazit}")
    # sys.exit()
    # # test, delete after success


    # """
    # Warning: reset only
    # """
    # os.chdir(os.path.abspath(os.path.dirname(__file__)))
    # print(f"set cwd to {os.path.abspath(os.path.dirname(__file__))}")
    # fazit_clip_dir = os.path.split(os.getcwd())[0] + os.sep + "fazit_clip"
    # fazit_jsonPath = fazit_clip_dir + os.sep + givenFazitJson
    # print(f"fazit_jsonPath => {fazit_jsonPath}")
    # print(final_reset_data(fazit_jsonPath,givenBrand))
    # serialNum_clip_dir = os.path.split(os.getcwd())[0] + os.sep + "serialNum_clip"
    # serialNum_jsonPath = serialNum_clip_dir + os.sep + "serial_num.json"
    # print(f"serialNum_jsonPath => {serialNum_jsonPath}")
    # print(final_reset_data(serialNum_jsonPath,"serial_num"))
    # sys.exit()
    # #############################################

    main_action()
    print(f"os.getcwd() => {os.getcwd()}")
    logPath = os.getcwd() + os.sep + "logs_" + time.strftime("%Y%m%d") + ".txt"
    fazitPath = os.getcwd() + os.sep + "fazit_" + time.strftime("%Y%m%d") + ".txt"
    removePath = os.getcwd() + os.sep + "remove_" + time.strftime("%Y%m%d") + ".txt"
    green_str = "\033[32m" + 'Write persistence data successfully!!!' + "\033[0m"
    current_time = time.strftime("%Y%m%d_%H_%M_%S", time.localtime(time.time()))
    padding_len = '%' + str(int(len(green_str) / 2) + 35) + 's'
    padding_len2 =  '%' + str(int(len(current_time) / 2) + 35) + 's'
    with open(logPath, 'a') as logs, open(fazitPath,"a") as fazits, open(removePath,"a") as remove:
        print("\n" + "=" * 70 + "\n" + padding_len2 % current_time + "\n" + "=" * 70 + "\n")
        logs.write("\n" + "=" * 70 + "\n" + padding_len2 % current_time + "\n")
        # fazit_id_char = input("pls input the fazit_id:\n")   # version 1: get fazit via keyboard input
        # set_real_cwd()
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        print(f"set cwd to {os.path.abspath(os.path.dirname(__file__))}")
        fazit_clip_dir = os.path.split(os.getcwd())[0] + os.sep + "fazit_clip"
        fazit_jsonPath = fazit_clip_dir + os.sep + givenFazitJson
        ########## important: we used 3GB035866D/fazit_clip/ as base fazit_trace directory.
        fazit_jsonPath = '/home/jpcc/PycharmProjects/pythonProject_Oct_2022/3GB035866D/fazit_clip' + os.sep + givenFazitJson
        ##########
        valid_fazit = final_get_vaild_data(fazit_jsonPath,givenBrand,"fazit")
        if valid_fazit:
            fazit_id_char = valid_fazit
            print(f"fazit_id_char => {fazit_id_char}")
        else:
            print(f"The status of valid: {valid_fazit}\nIt seems that there is no valid fazit id\n")
            sys.exit()
        serialNum_clip_dir = os.path.split(os.getcwd())[0] + os.sep + "serialNum_clip"
        serialNum_jsonPath = serialNum_clip_dir + os.sep + "serial_num_5HG035866.json"
        valid_serial = final_get_vaild_data(serialNum_jsonPath,"serial_num","serial")
        if valid_serial:
            serial_char = valid_serial
            print(f"serial_char => {serial_char}")
        else:
            print(f"The status of valid: {valid_serial}\nIt seems that there is no valid serial num\n")
            sys.exit()
        # serial_char = input("pls input the serialnum:\n")
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
        # transfer vkms scripts into HU
        s.sendline("scp -r -v vkms_import_reset_dlc.sh /usr/bin")
        s.expect("#")
        s.sendline("scp -r -v vkms_init_pss.sh /usr/bin")
        s.expect("#")
        # transfer vkms scripts into HU above
        s.sendline("cd /usr/bin")
        s.expect("/usr/bin")
        s.sendline("sha1sum tsd.persistence.client.mib3.app.SetKey")
        s.expect("4e9d90211063684bf2ce56b3f9bf94cefc141fa4  tsd.persistence.client.mib3.app.SetKey")
        s.sendline("sha1sum tsd.persistence.client.mib3.app.GetKey")
        s.expect("880152e334d675794bea1f3616d1c94c147c1962  tsd.persistence.client.mib3.app.GetKey")
        # checksum vkms scripts
        s.sendline("sha1sum vkms_import_reset_dlc.sh")
        s.expect("c388e0ef98d9fb1651fa24294090308f4d02554b  vkms_import_reset_dlc.sh")
        s.sendline("sha1sum vkms_init_pss.sh")
        s.expect("27ff76a1c36bbe2177ce3962b750d336865a20bc  vkms_init_pss.sh")
        # checksum vkms scripts above
        logs.write("="*30 + "base-identification" + "="*30 + "\n")
        # s.sendline("./tsd.persistence.client.mib3.app.GetKey --ns 0x3000000 --key 0xF17C")
        # s.expect("load: ns: 3000000 key: 61820 slot: 0 status: 0")
        # s.sendline("./tsd.persistence.client.mib3.app.GetKey --ns 0x3000000 --key 0xF1A3")
        # s.expect("load: ns: 3000000 key: 61859 slot: 0 status: 0")
        # print(f"s2.before: {s.before}")
        # print(s.before.split("\n")[0])
        # fazits.write(s.before.split("\n")[0] + "\n")
        # s.sendline("./tsd.persistence.client.mib3.app.GetKey --ns 0x3000000 --key 0xF189")
        # s.expect("load: ns: 3000000 key: 61833 slot: 0 status: 0")
        logs.write("=" * 79 + "\n")
        s.sendline("./tsd.persistence.client.mib3.app.SetKey --ns 0x80000008 --key 0x00 --val 0xe5")
        # s.expect("store: ns: 80000008 key: 0 slot: 0")
        s.expect("store: ns: 80000008 key: 0 slot: 0 status: 0 data: e5")
        # print(s.before.split("\n")[0])

        # hexadecimal_sw = s.before.split("\n")[0]
        # ascii_str_sw = bytes.fromhex("".join(hexadecimal_sw[hexadecimal_sw.index(":") + 1:].split())).decode()
        # if ascii_str_sw != "C822":
        #     print(redFont(f'pls check the SW version => {ascii_str_sw}'))
        # else:
        #     fazits.write(ascii_str_sw + "\n")


        #5HG035866  : 3548473033353836362020
        s.sendline("./tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF187 --val 0x3548473033353836362020")
        s.expect("store: ns: 3000000 key: 61831 slot: 0 status: 0 data: 35 48 47 30 33 35 38 36 36 20 20")
        s.sendline("./tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF191 --val 0x3548473033353836362020")
        s.expect("store: ns: 3000000 key: 61841 slot: 0 status: 0 data: 35 48 47 30 33 35 38 36 36 20 20")
        # set hardware version: X09
        s.sendline("./tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF1A3 --val 0x583039")
        s.expect("store: ns: 3000000 key: 61859 slot: 0 status: 0 data: 58 30 39")
        # set software version
        # C370
        s.sendline("./tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF189 --val 0x43333730")
        s.expect("store: ns: 3000000 key: 61833 slot: 0 status: 0 data: 43 33 37 30")
        # set fazit-id
        # fazit_id_char = "X9G-10103.05.2299990605"
        fazit_id_hex = str_to_hexStr(fazit_id_char)
        s.sendline(f"./tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF17C --val 0x{fazit_id_hex.upper()}")
        s.expect(f"store: ns: 3000000 key: 61820 slot: 0 status: 0 data: {' '.join([fazit_id_hex[i] + fazit_id_hex[i+1] for i in range(0,len(fazit_id_hex),2)])}")
        # ./tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF17C --val 0x5839472D31303130332E30352E32323939393930363034
        # set serial-num
        # serial_char = "VWX9GA3644002"
        serial_hex = str_to_hexStr(serial_char)
        s.sendline(f"./tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF18C --val 0x{serial_hex.upper()}")
        s.expect(
            f"store: ns: 3000000 key: 61836 slot: 0 status: 0 data: {' '.join([serial_hex[i] + serial_hex[i + 1] for i in range(0, len(serial_hex), 2)])}")
        # ./tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF18C --val 0x56575839474133363434303031
        # sys.exit()
        s.sendline("./vkms_init_pss.sh")
        s.expect("Finished")
        s.sendline("./vkms_import_reset_dlc.sh")
        s.expect("Finished")
        s.sendline("rm -rf tsd.persistence.client.mib3.app.*")
        s.expect("infotainment")
        print("remove tsd.persistence.client.mib3.app.* in /usr/bin")
        remove.write("remove tsd.persistence.client.mib3.app.* in /usr/bin" + "\n")
        s.sendline("rm -rf /usr/bin/tsd.persistence.client.mib3.app.*")
        s.expect("infotainment")
        print("remove vkms_i* in /usr/bin")
        remove.write("remove vkms_i* in /usr/bin" + "\n")
        s.sendline("rm -rf vkms_i*")
        s.expect("infotainment")
        # print(f"\n\ns.buffer: {s.buffer}\n\n")
        # print(f"\n\ns.before: {s.before}\n\n")
        # print(f"\n\ns.after: {s.after}\n\n")
        print("remove tsd.persistence.client.mib3.app.* in /var")
        remove.write("remove tsd.persistence.client.mib3.app.* in /var" + "\n")
        s.sendline("rm -rf /var/tsd.persistence.client.mib3.app.*")
        s.expect("infotainment")
        print("remove vkms_i* in /var")
        remove.write("remove vkms_i* in /var" + "\n")
        s.sendline("rm -rf /var/vkms_i*")
        s.expect("infotainment")

        s.sendline("sync")
        s.expect("infotainment")
        # s.sendline("exit")
        s.sendline("reboot")
        s.expect("Connection to 192.168.1.4 closed")
        fazits.write("start" + "*" * 60 + "\n")
        print(f"to exec. final_change_fazit_status")
        case1 = final_change_data_status(fazit_jsonPath,fazit_id_char,givenBrand,"fazit")
        print(f"to exec. final_change_data_status")
        case2 = final_change_data_status(serialNum_jsonPath,serial_char,"serial_num","serial")
        if case1 and case2:
            fazits.write(f'{time.strftime("%Y%m%d_%H_%M_%S", time.localtime(time.time()))}\n')
            fazits.write(f"fazit_id_char => {fazit_id_char}\n")
            fazits.write(f"serial_char => {serial_char}\n")
        fazits.write("end" + "=" * 60 + "\n")
        print("\n" + "=" * 70 + "\n" + padding_len % green_str + "\n" + "=" * 70 + "\n")
        logs.write("\n" + padding_len % green_str + "\n" + "=" * 70 + "\n")



    green_str = "\033[32m" + "Done!!!!!!" + "\033[0m"
    padding_len = '%' + str(int(len(green_str) / 2) + 35) + 's'
    print("\n" + "=" * 70 + "\n" + padding_len % green_str + "\n" + "=" * 70 + "\n")






