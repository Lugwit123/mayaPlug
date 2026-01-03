import subprocess
import os


def make_txs(dir_name=r"D:\work\tx"):
    for name in os.listdir(dir_name):
        path = os.path.join(dir_name, name)
        if not os.path.isfile(path):
            continue
        _, ext = os.path.splitext(name)
        if ext == ".tx":
            continue
        command = r"C:\solidangle\mtoadeploy\2015\bin\maketx.exe "
        command += path
        print command
        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
make_txs(dir_name=r"D:\work\tx")