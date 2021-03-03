#!/usr/bin/python3
# encoding=utf-8

import sys
import netmiko 
from netmiko import *
import re



dev_info = {
    'device_type' : 'huawei_olt',
    'host' : 'dengzhong04.f3322.net',
    'port' : '2014',
    'username' : 'huawei',
    'password' : 'huawei123',
    'secret' : '',
}




olt = { 'gpon' : 0 ,
        'port' : 0 ,
        'upvlan' : 100 ,
        'ont_line' : 11 ,
        'ont_srv' : 11 ,
      }
ont = { 'sn' : 'xxxxxxxxxx' ,
        'ontid': 0 
        'ip' : 'x.x.x.x' ,
        'loid' : 'xxxxxxxxxx',
        'type' :  'cat' ,
        'username' : 'root',
        'password' : 'mduadmin',
       }
if __name__ == '__main__':
    conn = ConnectHandler(**dev_info)
    conn.enable()
    commands= ['idle-timeout 200','scroll 512','config','interface gpon 0/1','display ont info 1 1','quit','quit','y']
    #commands = ['scroll 512','telnet 10.10.10.2','root','mduadmin','N','scroll 512','enable','display current-configuration','\n','quit','y']
    for command in commands:
        print(command)
        ont = conn.send_command_timing(command,use_textfsm=True,delay_factor=0.02,)
        if re.search('ONT-ID',ont) :
            o = ont.split("\n")
            print (o[1])
            print (o[2])
            print (o[3])
            print (o[4])
    conn.disconnect()






