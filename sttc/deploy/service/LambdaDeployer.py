'''
Created on 12 mai 2017

@author: static
'''

from sttc.aws.service.LambdaManager import LambdaManager
from sttc.aws.service.APIGatewayManager import APIGatewayManager
from sttc.deploy.service.IAMDeployer import IAMDeployer
from sttc.deploy.service import ConfReader as cr
from sttc.deploy.service.ConfReader import Validator

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
        self.v = Validator(self.t, self.confName, "lambda")
        
        
    def manageLambda(self):
        allMyLambda = self.getAllLambdaDir(self.root)
        fullReport = []
        for myLambda in allMyLambda:
            confLambda = self.v.getConfig(join(self.root, myLambda), self.confDeployer)
            if not confLambda == None:
                report = self.deployLambda(confLambda, myLambda)
                fullReport.append(report)
        return fullReport

    def getAllLambdaDir(self, path):
        onlyDir = [f for f in listdir(path) if isdir(join(path, f))]
        if onlyDir == None or len(onlyDir) == 0:
            raise Exception(self.t.getMessage("emptyDirs"))
        return onlyDir
    
    
        
    def deployLambda(self, confLambda, myLambda):
        
        report = {}
        
        print (self.t.getMessage("zipping ") + " - " + myLambda)     
        pathToLambdaZip = '../lambdas/' + myLambda + '/'
        shutil.make_archive(myLambda, "zip", pathToLambdaZip)
        report['name'] = myLambda
        
        lambdaVersion = self.l.getLambdaVersion()
        
        if "APIGatewayConf" in confLambda.keys():
            confGateway = confLambda["APIGatewayConf"]
            print (self.t.getMessage("manageAPIGateway") + " - " + confGateway['name'])          
            self.gateway.createAPI(confGateway, lambdaVersion)
                
        roleName = confLambda['role'].split(":role/",1)[1]
        print (self.t.getMessage("manageRole ") + " - " + roleName)  
        self.iamd.manageRole(roleName, confLambda["rolePolicy"])  
        
        print (self.t.getMessage("deploying ") + " - " + myLambda)  
        self.l.createFunctionSimpleDeleteIfExists(confLambda,  "./" + myLambda + ".zip")
        
        if "APIGatewayConf" in confLambda.keys():
            confGateway = confLambda["APIGatewayConf"]
            confLG = self.confDeployer['lambdaGateway']
            path, method = cr.getPathAndMethodMatchingKeyValue(confGateway, confLG['keyLink'], confLG['valueLink'])
            if path != None and method != None:
                print (self.t.getMessage("linkLambdaAPIGateway") + " - " + confGateway['name'] + ":" + path + "-" + method)  
                apiId = self.gateway.getApiByNameOrId(name=confGateway['name'])['id']
                
                self.gateway.linkMethodAndLambda(confGateway['name'], path, method, confLambda, confLG['lambdaUri'], lambdaVersion)
                
                self.gateway.linkToIntegration(confGateway)
                
                self.l.linkTogatewayPath(confLambda['name'], apiId, path, method, confLG['lambdaGatewayPermission'], path)
            
                self.gateway.deployStage(apiId, confGateway['stageName'])
            
                rest = self.l.client.get_policy(
                    FunctionName=confLambda['name']
                )
                url = "https://" + apiId + ".execute-api." + self.gateway.getRegion() + ".amazonaws.com/" + confGateway['stageName'] + path
                print(url)
                report['url'] = url
        return report
            
            
            
            
    
    
    
    '''
    def getLambdaDir(self, path):
        onlyDir = [f for f in listdir(path) if isdir(join(path, f))]
        if onlyDir == None or len(onlyDir) == 0:
            raise Exception(self.t.getMessage("emptyDirs"))
        print (self.t.getMessage("chooseLambda"))
        number = 0
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
    '''        
            
    
            
            
    
    
    