#!/usr/bin/python3
# encoding=utf-8


class batAddCat():
 
    def addCatMode (self,olt,cat):       
        catnum = cat.getcatpre()
        cataddlist=[]
        while catnum < cat.getaddnum()+cat.getcatpre():
            catid = str(catnum)
            catadd = "ont add "+str(olt.getGpon_kou())+" "+catid+\
                     " loid-auth "+str(cat.getcatprefix())+str(catnum)+\
                     " always-on omci ont-lineprofile-id 12 ont-srvprofile-id 11 \n"
            cataddlist.append(catadd)
            for catethid in range(1,5):
                cateth = "ont port native-vlan "+str(olt.getGpon_kou())+\
                         " "+catid+" eth "+str(catethid)+" vlan 41 priority 0"
                cataddlist.append(cateth)
            catnum += 1            
        return cataddlist
    def addCatser (self,olt,cat):
        catnum = cat.getcatpre()
        catserlist=[]
        while catnum < cat.getaddnum()+cat.getcatpre():
            catid = str(catnum)
            server_vlan = "service-port vlan "+str(olt.getUpvlan())+\
                          " gpon 0/"+str(olt.getGpon_kuang())+"/"+str(olt.getGpon_kou())+" ont "+\
                          catid+" gemport 1 multi-service user-vlan 41 tag-transform translate"
            catserlist.append(server_vlan)
            catnum += 1
        return catserlist

