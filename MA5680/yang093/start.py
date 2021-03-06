#!/usr/bin/python3
# encoding=utf-8

import sys
import netmiko 
from netmiko import *
from OLT import OLT
from CAT import CAT
from batAddCat import batAddCat

def txtSwitchDict(filename):
    with open("./"+filename, 'rb') as f:
        lines= f.readlines()
        tmp= {}
        for l in lines:
            x=l.decode("utf-8").split(":")
            init = {x[0].strip():str(x[1].strip())}
            tmp.update(init)
    return tmp

dev_info = txtSwitchDict("cat/dev.conf")
	


if __name__ == '__main__':
    
    olt_line = str(input('请输入机框/端口/上行vlan：')).split('/')      
    olt = OLT(int(olt_line[0]),int(olt_line[1]),int(olt_line[2]))
    cat_line = str(input ("请输入批量加光猫起始位置/个数/前缀：")).split('/')
    cat = CAT(int(cat_line[0]),int(cat_line[1]),cat_line[2])
    addcat = batAddCat()
    with  ConnectHandler(**dev_info) as conn:
        conn.enable()
        commands = ["idle-timeout 200","config","interface gpon 0/"+ str(olt.getGpon_kuang())]\
                   +addcat.addCatMode(olt,cat) \
                   +['quit']+addcat.addCatser(olt,cat)\
                   +['quit','quit','y']
        for command in commands:
            print(command)
            result = conn.send_command_timing(command,use_textfsm=True,delay_factor=0.02,)
            print (result)
        conn.disconnect()






