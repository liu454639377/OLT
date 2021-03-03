#!/usr/bin/python3
# encoding=utf-8

import sys
import netmiko 
from netmiko import *
import re
import time
import os


def txtSwitchDict(filename):
    with open("./"+filename, 'rb') as f:
        lines= f.readlines()
        tmp= {}
        for l in lines:
            x=l.decode("utf-8").split(":")
            init = {x[0].strip():str(x[1].strip())}
            tmp.update(init)
    return tmp

dev_info = txtSwitchDict('dev.conf')
olt = txtSwitchDict('OLT.conf')
ont = txtSwitchDict('CAT.conf')


#批量执行命令
def executeCommand(conn,commands):
    result = []
    for command in commands:
        print(command)
        result.append(conn.send_command(command,expect_string='>|#|y\/n|name\:|password\:|Failure|Huawei|error'))
        print(result[len(result)-1])
    return result
#通过sn码查找ont
def findONTisonline(conn,olt,ontid):
    commands = [ 'display ont info 0 '+olt['gpon']+' ' +olt['port']+' '+str(ontid)
               ]
    result=executeCommand(conn,commands)
    loid=""
    l = result[0].split('\n')
    if len(l) > 4:
        if re.search('offline',l[4]) and re.search('loid-auth',l[14]):
            loid = l[17].split(":")[1]
            if re.search("SN",l[17].split(":")[0]) :
                loid = l[18].split(":")[1]
    return loid

  


if __name__ == '__main__':
    with ConnectHandler(**dev_info) as conn:
        conn.enable()
        commands = ['idle-timeout 200','scroll\n','config',]
        executeCommand(conn,commands)
        if os.path.exists('./loid.txt'):
            os.remove('./loid.txt')
        for i in range(128):
            ont['ontid'] = str(i)
            with open ("loid.txt","a+") as f :
                loid = findONTisonline(conn,olt,i)
                print(loid)
                if len(loid) > 10:
                    f.write(loid+'\n')
        conn.disconnect()


