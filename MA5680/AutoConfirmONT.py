#!/usr/bin/python3
# encoding=utf-8

import sys
import netmiko 
from netmiko import *
import re
from IPy import *
import time



dev_info = {
    'device_type' : 'huawei_olt',
    'host' : 'dengzhong04.f3322.net',
    'port' : '2014',
    'username' : 'huawei',
    'password' : 'huawei123',
    'secret' : '',
}


olt = { 'gpon' : '0' ,
        'port' : '0' ,
        'upvlan' : '100' ,
        'ont_line' : '12' ,
        'ont_srv' : '11' ,
        'network' : '188.0.0.0/24'
        }
ont = { 'sn' : 'xxxxxxxxxx' ,
        'ontid': 0 ,
        'ip' : 'x.x.x.x' ,
        'loid' : 'xxxxxxxxxx',
        'type' :  'cat' ,
        'username' : 'root',
        'password' : 'mduadmin',
        'ont_config' : 'ont.txt'
        }


#批量执行命令
def executeCommand(conn,commands):
    result = []
    for command in commands:
        print(command)
        result.append(conn.send_command_timing(command))
        print(result[len(result)-1])
    return result
#通过sn码查找ont
def getONTbySN(conn,olt,ont):
    result = conn.send_command_timing('display ont info by-sn '+ ont['sn'])
    print(result)
    if not re.search('ONT-ID',result):
        return False
    olt['gpon'] = result.split('\n')[1].split(":")[1].split('/')[1]
    olt['port'] = result.split('\n')[1].split(":")[1].split('/')[2]
    ont['ontid'] = result.split('\n')[2].split(':')[1].split(' ')[1]
    return
#通过IP查出找ONT
def getONTbyIP(conn,olt,ont):
    for ip in IP(olt['network']):
        if str(ip) == '188.0.0.1' or str(ip) == '188.0.0.2' or str(ip) == '188.0.0.0':
            continue
        result = conn.send_command_timing('display ont info by-ip '+ str(ip))
        if not re.search('ONT-ID',result):
            ont['ip'] = str(ip)
            return
#删除ONT 
def deleONT(conn,olt,ont):
    commands = ['undo service-port port 0/'+olt['gpon']+'/'+olt['port']+\
                ' ont '+ str(ont['ontid'])+'\n' ,
                'y' ,
                'interface gpon 0/'+olt['gpon'] ,
                'ont delete '+olt['port']+' '+ont['ontid'],
                'quit' ,
               ]
    executeCommand(conn,commands)
#添加ONT
def addONT(conn,olt,ont):
    commands = ['interface gpon 0/'+olt['gpon'] ,
                'ont add '+olt['port']+' sn-auth '+\
                ont['sn']+' snmp ont-lineprofile-id '+olt['ont_line']+'\n' ,
               ]
    result = executeCommand(conn,commands)
    ont['ontid'] = int(result[1].split("ONTID :")[1])
    commands_confirm = ['ont ipconfig '+olt['port']+' '+str(ont['ontid']) +' static ip-address '+\
                        ont['ip'] + ' mask 255.255.255.0 vlan 99 priority 5 \n' ,
                        'quit' ,
                        'service-port vlan 99 gpon 0/'+olt['gpon']+'/'+olt['port']+' ont ' +\
                        str(ont['ontid']) + ' gemport 0 multi-service user-vlan 99 tag-transform translate \n' ,
                        'service-port vlan '+olt['upvlan']+' gpon 0/'+olt['gpon']+'/'+olt['port']+' ont ' +\
                        str(ont['ontid']) + ' gemport 0 multi-service user-vlan 1001 tag-transform translate \n' ,
                       ]
    executeCommand(conn,commands_confirm)
def getONTbyAuto():
    infor = conn.send_command_timing('display ont autofind all')
    if re.search('not exist',infor):
        return False
    olt['gpon'] = infor.split('\n')[2].split(":")[1].split('/')[1]
    olt['port'] = infor.split('\n')[2].split(":")[1].split('/')[2]
    ont['sn'] = infor.split('\n')[3].split(':')[1].split(' ')[1]
    return True
  

def configONT(conn,olt,ont):
     with open(ont['ont_config']) as f :
         commands = f.readlines()
         executeCommand(conn,commands)


if __name__ == '__main__':

    with ConnectHandler(**dev_info) as conn:
        conn.enable()
        commands = ['idle-timeout 200','scroll 512','config',]
        executeCommand(conn,commands)
        if not getONTbyAuto():
            ont['sn'] = input("没有查找到ont,请输入sn码：")
            getONTbySN(conn,olt,ont) 
            deleONT(conn,olt,ont)
        getONTbyIP(conn,olt,ont)
        addONT(conn,olt,ont)
        print(ont,'\n\n',olt,'\n')
        if not re.search('100.00%',conn.send_command_timing('ping '+ont['ip'])):
            conn.send_command_timing('telnet '+ont['ip']+' 23')
            time.sleep(2)
            executeCommand(conn,[ont['username'],ont['password']])
            configONT(conn,olt,ont)
        else:
            print("ont配置错误，但olt配置正确")
            time.sleep(10)
        conn.disconnect()


