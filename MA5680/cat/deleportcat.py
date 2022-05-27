#!/usr/bin/python3
# encoding=utf-8

import sys
import netmiko 
from netmiko import *
import re
import time



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
    l = result[0].split('\n')
    if len(l) > 4:
        if re.search('offline',l[4]) :
            return True
    else: 
        if re.search('The ONT does not exist',l[0]):
            return True
    return False

#删除ONT 
def deleONT(conn,olt,ont):
    commands = ['undo service-port port 0/'+olt['gpon']+'/'+olt['port']+\
                ' ont '+ ont['ontid']+'\n' ,
                'y' ,
                'interface gpon 0/'+olt['gpon'] ,
                'ont delete '+olt['port']+' '+ont['ontid'],
                'quit' ,
               ]
    executeCommand(conn,commands)
  


if __name__ == '__main__':
    with ConnectHandler(**dev_info) as conn:
        conn.enable()
        commands = ['idle-timeout 200','scroll\n','config',]
        executeCommand(conn,commands)
        for k in range(8):
            olt['port']= str(k)
            for i in range(32):
                ont['ontid'] = str(i)
                if findONTisonline(conn,olt,i) :
                    deleONT(conn,olt,ont)
        conn.disconnect()


