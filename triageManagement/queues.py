# -*- coding:utf-8 -*-
# __author__="Liyuanfang"
# __DATE__="2019/6/4"

class Queues():
    queues={}

    def addinq(self,doctor,patient):
        if doctor not in self.queues.keys():
            self.queues[doctor] =[]
            self.queues[doctor].append(patient)
        else:
            if patient not in self.queues[doctor]:
                self.queues[doctor].append(patient)


    def getpatient(self,doctor):
        try:
            patient = self.queues[doctor].pop(0)
            return patient
        except:
            return 0


    def adjustq(self,doctor,list):
        if self.queues[doctor].__len__() != list.__len__():
            return 0
        else:
            self.queues[doctor] = list
            return 1

    def showq(self,doctor):
        if doctor not in self.queues.keys():
            return 0
        else:
            return self.queues[doctor]
