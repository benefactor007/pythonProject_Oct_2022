import os,sys,json,jsonpath,pexpect,time

# get the current path

current_working_dir = os.getcwd()

# set log path => format as logs_20221027

logPath = os.getcwd() + os.sep + "logs_" + time.strftime("%Y%m%d") + ".txt"

# get the tool's directory

tool_dir = os.path.split(os.getcwd())[0] + os.sep + "tool"


# Get the file list in the target directory.
def get_fileList(dir):
    try:
        print(os.listdir(dir))
    except FileNotFoundError:
        os.mkdir(dir)
        print(f"Now the directory path <{dir}> has been created")


# transfer files to HU



if __name__ == '__main__':
    print(f"current_working_directory: {current_working_dir}")
    print(f"log path: {logPath}")
    print(f"tool directory: {tool_dir}")
    print(f"get_fileList func. =>  {get_fileList(tool_dir)} ")
