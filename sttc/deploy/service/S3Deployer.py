'''
Created on 19 mai 2017

@author: static
'''

from os.path import isdir, join
from os import listdir
from sttc.deploy.service.ConfReader import Validator
from sttc.deploy.service import ConfReader as cr

class S3Deployer():
    
    def __init__(self, translator, zone, rootS3Path, confName, confDeployer):
        self.t = translator
        self.zone = zone
        self.root = rootS3Path
        self.confName = confName
        self.confDeployer = confDeployer
        self.v = Validator(self.t)
        
    def manageS3(self):
        allMyS3 = self.getAllS3Dir(self.root)
        for myS3 in allMyS3:
            confS3 = self.v.getConfig(join(self.root, myS3), self.confDeployer)
            if not confS3 == None:
                self.deployS3(confS3, myS3)
                
    def getAllS3Dir(self, path):
        onlyDir = [f for f in listdir(path) if isdir(join(path, f))]
        if onlyDir == None or len(onlyDir) == 0:
            raise Exception(self.t.getMessage("emptyDirs"))
        return onlyDir
    
        
        
    def deployS3(self, conf, s3):
        pass
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        