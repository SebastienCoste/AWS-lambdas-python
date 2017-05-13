'''
Created on 12 mai 2017

@author: static
'''

from sttc.aws.service.LambdaManager import LambdaManager
from sttc.aws.service.APIGatewayManager import APIGatewayManager
from sttc.deploy.service.IAMDeployer import IAMDeployer
from sttc.deploy.service import ConfReader as cr

from os.path import isdir, join
from os import listdir
import shutil


class LambdaDeployer:
    
    def __init__(self, translator, zone, rootLambdaPath, confName, confDeployer):
        self.t = translator
        self.zone = zone
        self.root = rootLambdaPath
        self.confName = confName
        self.confDeployer = confDeployer
        self.l = LambdaManager(self.t, self.zone)
        self.iamd = IAMDeployer(self.zone, self.t)
        self.gateway = APIGatewayManager(self.zone, self.t)
        
        
    def manageLambda(self):
        confLambda = None
        while confLambda == None:
            myLambda = self.getLambdaDir(self.root)
            confLambda = self.getConfig(join(self.root, myLambda), self.confDeployer)
        
        self.deployLambda(confLambda, myLambda)
      

    def getLambdaDir(self, path):
        onlyDir = [f for f in listdir(path) if isdir(join(path, f))]
        if onlyDir == None or len(onlyDir) == 0:
            raise Exception(self.t.getMessage("emptyDirs"))
        number = 1
        print (self.t.getMessage("chooseLambda"))
        for dir in onlyDir:
            print (str(number) + " - " + dir)
            number +=1
        res = 1
        while res <= 0 or res > number:
            resStr = input(self.t.getMessage("chooseNumber") + '\n')
            try:
                res = int(resStr)
            except: 
                res = 0
        return onlyDir[res -1]
    
    
    def validateConf(self, conf, confDeployer):
        for item in confDeployer["mandatory"]:
            try:
                if conf[item] == None:
                    print (self.t.getMessage("missingMandatoryArtifact") + " " + item)
                    return False
            except: 
                print (self.t.getMessage("missingMandatoryArtifact") + " " + item)
                return False
        for item in confDeployer["conditionnalMandatory"]:
            if item['name'] in conf.keys():
                toValidate = conf[item['name']]
                for subitem in item["mandatory"]:
                    try:
                        if toValidate[subitem] == None:
                            print (self.t.getMessage("missingMandatoryArtifact") + " " + item['name'] + "/"+ subitem)
                            return False
                    except: 
                        print (self.t.getMessage("missingMandatoryArtifact") + " " + item['name'] + "/"+ subitem)
                        return False
        return True
    
    
    def getConfig(self, lambdaDir, confDeployer):
        confpath = join(lambdaDir, self.confName)
        conf = cr.readJson(self.t, confpath)
        if self.validateConf( conf, confDeployer):
            return conf
        else:
            return None
        
        
    def deployLambda(self, confLambda, myLambda):
        
        print (self.t.getMessage("zipping ") + " - " + myLambda)     
        pathToLambdaZip = '../lambdas/' + myLambda + '/'
        shutil.make_archive(myLambda, "zip", pathToLambdaZip)
        
        if "APIGatewayConf" in confLambda.keys():
            confGateway = confLambda["APIGatewayConf"]
            print (self.t.getMessage("manageAPIGateway ") + " - " + confGateway['name'])          
            self.gateway.createAPI(confGateway)
                
        roleName = confLambda['role'].split(":role/",1)[1]
        print (self.t.getMessage("manageRole ") + " - " + roleName)  
        self.iamd.manageRole(roleName, confLambda["rolePolicy"])  
        
        print (self.t.getMessage("deploying ") + " - " + myLambda)  
        self.l.createFunctionSimpleDeleteIfExists(confLambda,  "./" + myLambda + ".zip")
    
    
    