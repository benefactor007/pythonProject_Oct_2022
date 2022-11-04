#! /usr/bin/env python3
import json
import os, sys, pexpect

import subprocess

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
    index = p.expect(["Connection", pexpect.TIMEOUT, pexpect.EOF, "infotainment"])
    if index == 0:
        print("match connection")
        return main_action()
    elif index == 1:
        print("pexpect.TIMEOUT")
    elif index == 2:
        print("pexpect.EOF")
    elif index == 3:
        print("match infotainment, scripts should run")
        # sys.exit()


from peri_step1 import P_step1


class sub_P_step1(P_step1):
    def set_pexpect_command_v2(self, json_path, json_file, log_path, error_path):
        with open("{0}/{1}".format(json_path, json_file), encoding="utf-8") as json_data, \
                open(log_path, 'a')as logs, open(error_path, 'a') as errors:
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
                    # for ele_dict in (
                    #         jsonpath.jsonpath(data, "$.head[?(@.sendline)]"),
                    #         jsonpath.jsonpath(data, "$.body[?(@.sendline)]"), \
                    #         jsonpath.jsonpath(data, "$.tail[?(@.sendline)]")):
                    ele_dict = jsonpath.jsonpath(data, "$.head[?(@.sendline)]")
                    for i in range(len(ele_dict)):
                        P_step1.pAction_v2(ele_dict[i], cls=p)
                    ele_dict = jsonpath.jsonpath(data, "$.body[?(@.sendline)]")
                    for i in range(len(ele_dict)):
                        if i > 0:
                            # print(ele_dict[i])
                            P_step1.pAction_v2(ele_dict[i], cls=p)
                            pre_key = ele_dict[i - 1].get("key", None)
                            pre_ns = ele_dict[i - 1].get("ns", None)
                            current_key = ele_dict[i].get("key", None)
                            # print("{0}:\t{1}".format("pre_key", pre_key))
                            # print("{0}:\t{1}".format("current_key", current_key))
                            a = p.before[:]
                            try:
                                # print(a)
                                if current_key and a.strip().startswith("status: 0"):
                                    # pre_data = a[a.index("data:") + 5:a.index("\r")]
                                    # self.key_data_list.append(
                                    #     dict(zip(["ns", "key", "data"], [pre_ns, pre_key, pre_data])))
                                    pre_status = a[a.index("status:") + 7:a.index("data")].strip()
                                    print("{0}:\t{1}".format("pre_state", pre_status))
                                    pre_data = a[a.index("data:") + 5:a.index("\r")]
                                    print("{0}:\t{1}".format("pre_data", pre_data))
                                    self.key_data_list.append(dict(zip(["ns", "key", "data", "status"],
                                                                       [pre_ns, pre_key, pre_data,
                                                                        pre_status])))
                                else:
                                    # errors.write("{0} error \n {1} \n".format("set_pexpect_command_v2", a))
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


if __name__ == '__main__':
    main_action()

    WD_partnum = P_step1()
    WD_partnum.setJsonDir()

    WD_partnum.set_pexpect_command_v2(WD_partnum.json_dir, "persistence_wDat.fazit_clip", WD_partnum.log_name,
                                      WD_partnum.error_name)
