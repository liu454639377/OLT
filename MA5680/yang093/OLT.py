#!/usr/bin/python3
# encoding=utf-8


class OLT:
    def __init__(self,Gpon_kuang,Gpon_kou,upvlan):
        self.upvlan = upvlan
        self.Gpon_kuang = Gpon_kuang
        self.Gpon_kou = Gpon_kou
    def getGpon_kuang (self):
        return self.Gpon_kuang
    def getGpon_kou(self) :
        return self.Gpon_kou
    def getUpvlan(self) :
        return self.upvlan


 
