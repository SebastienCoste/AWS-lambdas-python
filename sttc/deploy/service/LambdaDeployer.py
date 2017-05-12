'''
Created on 12 mai 2017

@author: static
'''

from sttc.aws.service.LambdaManager import LambdaManager
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
        
        print (self.t.getMessage("deploying ") + " - " + myLambda)    
        self.l.createFunctionSimple(confLambda,  "./" + myLambda + ".zip")
    
    
    