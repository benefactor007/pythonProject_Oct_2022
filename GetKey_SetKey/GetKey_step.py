import fazit_clip
import  os, sys,time
import subprocess

import jsonpath
import pexpect


class sub_P_step1:
    def __init__(self,logPath, errorPath):
        self.logPath = logPath
        self.errorPath = errorPath

    def set_pexpect_command(self, json_path, log_path):
        with open(json_path, encoding="utf-8") as json_data, \
                open(log_path, 'a')as logs:
            data = fazit_clip.load(json_data)
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
                            self.pAction_v2(i, cls=p)
                except pexpect.TIMEOUT:
                    print(self.repr_message("pexpect.TIMEOUT"))

    def repr_message(self, message: str):
        padding_len = '%' + str(int(len(message) / 2) + 35) + 's'
        return "\n" + "=" * 70 + "\n" + padding_len % message + "\n" + "=" * 70 + "\n"

    def pAction_v2(self, Jdist, cls):
        if Jdist.get("sendline", None):
            cls.sendline(Jdist["sendline"])
        else:
            raise ValueError("sendline is not given")
        if Jdist.get("expect", None):
            cls.expect(Jdist["expect"])
        else:
            raise ValueError(f'expect is not given, the sendline is {Jdist.get("sendline", None)}')

    def scp(self, file):
        p_command = f"scp -r {file} root@192.168.1.4:/var"
        # p_command = "scp -r {0} {1}@{2}:{3}".format(file, self.user, self.ip, self.hu_dir)
        return p_command

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
    # HU_exec.set_pexpect_command_v1(HU_exec.json_folder, "[default]transfer_files_to_var.fazit_clip", HU_exec.log_path)
    toolsPath = os.getcwd() + os.sep + "tools"
    toolsPathList = [toolsPath + os.sep + file for file in os.listdir(toolsPath)]
    print(f"toolsPathList: {toolsPathList}")
    jsonPath = os.getcwd() + os.sep + "[default]transferFiles.fazit_clip"
    WD_partnum.transfer_files(toolsPathList, jsonPath)
    print(WD_partnum.greenFont("Transfer was successfully finished"))
    # pprint.pprint(WD_partnum.json_dict)
    # pprint.pprint(WD_partnum.json_list)
    if WD_partnum.json_list or WD_partnum.json_dict:
        WD_partnum.json_list, WD_partnum.json_dict = [],{}
    else:
        pass
    # sys.exit()
    jsonPath = "file_checksum_expect.fazit_clip"
    # logPath = os.getcwd() + os.sep + "logs_" + time.strftime("%Y%m%d") + ".txt"
    # errorPath = os.getcwd() + os.sep + "errors_" + time.strftime("%Y%m%d") + ".txt"
    WD_partnum.set_pexpect_command(jsonPath, logPath)
    if WD_partnum.json_list or WD_partnum.json_dict:
        WD_partnum.json_list, WD_partnum.json_dict = [],{}
    else:
        pass
    print(WD_partnum.greenFont("files was successfully double checked"))

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
        time_sleep(30)
        print()
        main_action()
    elif index == 1:
        print("pexpect.TIMEOUT")
    elif index == 2:
        print("pexpect.EOF")
    elif index == 3:
        print("match infotainment, scripts should run")
        nextStep()
        # sys.exit()


if __name__ == '__main__':
    main_action()
    # nextStep()