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

def getOLTinfo(conn,olt,ont) :
    infor = conn.send_command_timing('display ont autofind all')
    if re.search('not exist',infor):
        return False
    olt['gpon'] = infor.split('\n')[2].split(":")[1].split('/')[1] 
    olt['port'] = infor.split('\n')[2].split(":")[1].split('/')[2]
    ont['sn'] = infor.split('\n')[3].split(':')[1].split(' ')[1]
    return True    
def getONTid(conn,olt,ont):
    infor = conn.send_command_timing('ont add '+ olt['port']+' sn-auth '+ont['sn']+\
                             ' omci ont-lineprofile-id '+ olt['ont_line']+\
                             ' ont-srvprofile-id '+ olt['ont_srv']+'\n')
    print(infor)
    ont['ontid'] = str(infor.split("ONTID :")[1].strip())
    return True
def ontConfirm(conn,olt,ont):
    ont_comfirm_commands = ['ont port native-vlan '+ olt['port']+' '+ ont['ontid'] +' eth 1 vlan 41 priority 0' ,
                            'ont port native-vlan '+ olt['port']+' '+ ont['ontid'] +' eth 2 vlan 41 priority 0' ,
                            'ont port native-vlan '+ olt['port']+' '+ ont['ontid'] +' eth 3 vlan 41 priority 0' ,
                            'ont port native-vlan '+ olt['port']+' '+ ont['ontid'] +' eth 4 vlan 41 priority 0' ,
                            'quit',
                            ' service-port  vlan '+ olt['upvlan']+\
                            ' gpon 0/'+ olt['gpon']+'/'+ olt['port']+\
                            ' ont '+ ont['ontid'] +\
                            ' gemport 1 multi-service user-vlan 41 tag-transform translate',
                           ]
    ont_command(conn,ont_comfirm_commands)
    return True

def save(conn):
    save_command = ['return' ,'save\n' , 'quit' , 'y' ]
    ont_command(conn,save_command)

def ont_command(conn,commands): 
    for command in commands:
        print(command)
        print(conn.send_command_timing(command,use_textfsm=True,delay_factor=0.02,))

def find_ont_by_sn(conn,olt,ont):
    command = 'display ont info by-sn ' + ont['sn']
    infor = conn.send_command_timing(command)
    if not re.search("ONT-ID",infor) :
        return False
    print(infor)
    olt['gpon'] =  infor.split('\n')[1].split(":")[1].split('/')[1]
    olt['port'] =  infor.split('\n')[1].split(":")[1].split('/')[2]
    ont['ontid'] = str (infor.split('\n')[2].split(':')[1].split(' ')[1])
    return True

def deleONT(conn,olt,ont):
    commands = ['undo service-port port 0/'+ olt['gpon']+'/'+ olt['port']+\
                ' ont '+ ont['ontid']+'\n' ,
                'y' ,
                'interface gpon 0/'+ olt['gpon'] ,
                'ont delete '+ olt['port'] +' '+ ont['ontid'],
                'quit' ,
               ]
    ont_command(conn,commands)

if __name__ == '__main__':
    with ConnectHandler(**dev_info) as conn:
        conn.enable()
        commands= ['idle-timeout 200','scroll 512','config']
        ont_command(conn,commands)
        if not getOLTinfo(conn,olt,ont) :
            ont['sn'] = input("请输入sn码：")
            if not find_ont_by_sn(conn,olt,ont):
                print("输入错误sn码！")
                conn.disconnect()
                time.sleep(3)
                sys.exit(0)
            deleONT(conn,olt,ont)
            getOLTinfo(conn,olt,ont)
        print(conn.send_command_timing('interface gpon 0/'+ olt['gpon']))
        getONTid(conn,olt,ont)
        ontConfirm(conn,olt,ont)
        print(olt,'\n\n\n',ont,'\n')
        conn.disconnect()

