'''
Created on 12 mai 2017

@author: static
'''
from sttc.aws.service.IAMManager import IAMManager

class IAMDeployer():


    def __init__(self, translator, zone):
        self.zone = zone 
        self.t = translator
        self.iam = IAMManager(self.zone, self.t)
    
    def manageIAM(self):
        pass
    
    def manageRole(self, rolename):
        self.iam.createRoleIfNotExists(rolename)