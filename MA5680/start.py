#!/usr/bin/python3
# encoding=utf-8

import sys
import netmiko 
from netmiko import *



#dev_info = {
#    'device_type' : 'huawei_olt',
#    'host' : 'dengzhong03.f3322.net',
#    'port' : '2014',
#    'username' : 'huawei',
#    'password' : 'huawei123',
#    'secret' : '',
#}

dev_info = {
    'device_type' : 'huawei_olt',
    'host' : '81.71.27.13',
    'port' : '24970',
    'username' : 'huawei',
    'password' : 'huawei123',
    'secret' : '',
    'conn_timeout' : 15 ,
}


if __name__ == '__main__':


    conn = ConnectHandler(**dev_info)
    conn.enable()
    commands= ['scroll 512','config','interface gpon 0/13','display ont info 1 2','quit']
    for command in commands:
        print(command)
        ont = conn.send_command_timing(command,use_textfsm=True,delay_factor=0.02,)
        print (ont)
    conn.disconnect()






