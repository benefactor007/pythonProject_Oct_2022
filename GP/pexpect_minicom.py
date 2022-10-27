import os
import pprint
import sys
import time

import pexpect
from temp_exec2 import main_action,check_ping

def doPexpect(p_command):
    # with open("minicom_log.txt", 'w') as my_log_file:
    p = pexpect.spawn(command=p_command, logfile=sys.stdout, encoding='utf-8', timeout=30)
    # json_list = HU.get_json_info("p_script1.json", "$.p_script1.*")
    p.expect("password")
    p.sendline("jpcc")
    p.expect("Welcome to minicom")
    time.sleep(2)
    p.sendline("PWC:")
    p.sendline("cS 1 88")
    p.sendcontrol("a")
    # p.sendcontrol("m")
    p.sendline("x")
    p.sendcontrol("m")
    # if p ==
    # p.close()
    p.expect(pexpect.EOF)
    print("eof")
    # return HU.greenFont(HU.repr_message("Success to copy file to HU"))
    return "Successful"


def set_backup(file):
    with open(file, "r") as file1, open(file + "_bak", "w") as file2:
        file2.write(file1.read())


def insert_line_into_file(file="hmi-keypanel.service", words_below="WorkingDirectory=/tsd/bin",
                          insert_words="Environment=\"SCALE_HACK=hack\""):
    with open(file, "r") as file1:
        f = file1.read()
        each_f = f.split("\n")
        for i in range(len(each_f)):
            if words_below in each_f[i] and insert_words not in each_f[i + 1]:
                print(f"each_f[i] : {each_f[i]}")
                print(f" each_f[i + 1] : {each_f[i + 1]}")
                print(f"we found the line[i]: {i}")
                target_line = i
                each_f.insert(target_line + 1, insert_words)
                # pprint.pprint(each_f)
                print("Success to insert info!!!")
                break
            elif words_below in each_f[i] and insert_words in each_f[i + 1]:
                print(f"each_f[i] : {each_f[i]}")
                print(f" each_f[i + 1] : {each_f[i + 1]}")
                print("insert_words already in the file, pls do not insert again")
                break
        each_f = "\n".join(each_f)
    with open(file, "w") as file2:
        file2.write(each_f)


if __name__ == '__main__':
    a = [str(x) * 10 + "\n" for x in range(10)]
    print(a)


    logPath = os.getcwd() + os.sep + "logs_minicom_" + time.strftime("%Y%m%d") + ".txt"
    print(f"logPath: {logPath}")
    with open(logPath, "a") as logs:
        logs.write("here is log from minicom\n")
        m = pexpect.spawn(command="sudo minicom", logfile=logs, encoding='utf-8', timeout=30)
        # json_list = HU.get_json_info("p_script1.json", "$.p_script1.*")
        m.expect("password")
        m.sendline("jpcc")
        m.expect("Welcome to minicom")
        print(f"m.before:{m.before}")
        print(f"m.buffer:{m.buffer}")
        print(f"m.after:{m.before}")
        time.sleep(2)
        m.sendline("PWC:")
        # m.sendline("cS 1 88")
        m.expect("pwc")
        print(f"m.before1:{m.before}")
        print(f"m.after1:{m.before}")
        m.sendline("fx  17  80  1")
        m.expect("displayType")
        print(f"m.before2:{m.before}")
        print(f"m.after2:{m.before}")
        m.sendcontrol("a")
        # p.sendcontrol("m")
        m.sendline("x")
        m.sendcontrol("m")
        # if p ==
        # p.close()
        m.expect(pexpect.EOF)
        print("eof")
        # return HU.greenFont(HU.repr_message("Success to copy file to HU"))
        print("Successful")
        sys.exit()


    while True:
        if check_ping("192.168.1.4") == "0":
            break
        else:
            pass
    logPath = os.getcwd() + os.sep + "logs_" + time.strftime("%Y%m%d") + ".txt"
    with open(logPath, "a") as logs:
        p = pexpect.spawn(command = "scp root@192.168.1.4:/usr/lib/systemd/system/hmi-keypanel.service "
                                    "/home/jpcc/PycharmProjects/pythonProject_Oct_2022/GP",
                          logfile= logs,encoding="utf-8",timeout=10)
        p.expect("password")
        p.sendline("root")
        p.expect("100%")
        p.expect(pexpect.EOF)
        print("Done!!!")

        file_name = "hmi-keypanel.service"
        set_backup(file_name)
        insert_line_into_file(file=os.getcwd() + os.sep + file_name, words_below="WorkingDirectory=/tsd/bin",
                              insert_words="Environment=\"SCALE_HACK=hack\"")
        file_to_hu_tmp = f"scp {os.getcwd()+ os.sep +file_name} root@192.168.1.4:/tmp/"
        print(f"file_to_hu : {file_to_hu_tmp}")
        # sys.exit()
        p = pexpect.spawn(command=file_to_hu_tmp,
                          logfile=logs, encoding="utf-8", timeout=10)
        p.expect("password")
        p.sendline("root")
        p.expect("100%")
        s = pexpect.spawn("ssh root@192.168.1.4", logfile=logs, encoding="utf-8", timeout=10)
        s.expect("password")
        s.sendline("root")
        s.expect("infotainment")
        s.sendline("mount-read-write.sh")
        s.expect("infotainment")
        s.sendline("cd /tmp")
        s.expect("/tmp")
        s.sendline("mv hmi-keypanel.service /usr/lib/systemd/system")
        pprint.pprint(f"s.buffer: {s.buffer}")
        s.expect("#")
        # p.buffer = ""
        # if p.before:
        #     p.expect(r'.+')
        pprint.pprint(f"s.buffer: {s.buffer}")
        expect_index = s.expect(["#", "mv: overwrite '/usr/lib/systemd/system/hmi-keypanel.service'"])
        if expect_index == 0:
            print("expect_index 0 run")
            pass
        elif expect_index == 1:
            s.sendline("y")
            s.expect("#")
            print("expect_index 1 run")
        s.sendline("cat /usr/lib/systemd/system/hmi-keypanel.service |grep \"Environment=\\\"SCALE_HACK=hack\\\"\"")
        # s.expect("#")
        expect_index = s.expect(["#", "Environment=\"SCALE_HACK=hack\""])
        if expect_index == 0:
            print("There is no match message, pls check it!!!")
            raise ValueError()
        elif expect_index == 1:
            print("Matched!!!")
            pass
        s.sendline("sync")
        s.expect("infotainment")
        s.sendline("exit")
        # s.sendline("reboot")
        s.expect("Connection to 192.168.1.4 closed")


        # time.sleep(2)
        # p.buffer = ""
        # if p.before:
        #     p.expect(r'.+')
        # print(f"s.before: {s.before}")
        # print(f"s.after: {s.after}")
        # print(f"s.buffer: {s.buffer}")

        s.sendline("cat /usr/lib/systemd/system/hmi-keypanel.service |grep \"Environment=\\\"SCALE_HACK=hack\\\"\"")
        sys.exit()


    # with open("123.txt","w") as file:
    #     file.writelines(a)
    # # sys.exit()
    # with open("123.txt","r") as file:
    #     lines = file.read()
    #     lines_list = lines.split("\n")
    #     lines_list.insert(1,"new line inserted")
    #     pprint.pprint(lines_list)
    #     lines_list = "\n".join(lines_list)
    # with open("123.txt","w") as new_file:
    #     new_file.writelines(lines_list)
