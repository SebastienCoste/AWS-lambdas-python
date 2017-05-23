'''
Created on 19 mai 2017

@author: static
'''

from os.path import isdir, join, isfile
from os import listdir
from sttc.deploy.service.ConfReader import Validator
from sttc.aws.service.S3Manager import S3Manager
from shutil import copyfile
import subprocess
from ntpath import relpath

class S3Deployer():
    
    def __init__(self, translator, zone, rootS3Path, confName, confDeployer):
        self.t = translator
        self.zone = zone
        self.root = rootS3Path
        self.confName = confName
        self.confDeployer = confDeployer
        self.v = Validator(self.t, self.confName, "s3")
        self.s3 = S3Manager(self.t, self.zone)
        
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
    
    
    def buildFiles(self, conf):
        
        relPath = conf['relativePath']
        if 'prepareScript' in conf.keys():
            confScript = conf['prepareScript']
            scriptLocation = join(relPath, confScript['filename'])
            shellLine = "python " + scriptLocation
            if 'arguments' in confScript.keys():
                for argument in confScript['arguments']:
                    shellLine += " " + argument['key']
                    shellLine += " " + argument['value']
            subprocess.Popen(shellLine, shell=True)
        
        if 'buildCommand' in conf.keys():
            shellBuild = "(cd " + str(conf['relativePath']) + " \&\& " + str(conf['buildCommand']) + " )"
            subprocess.Popen(shellBuild, shell=True)
        
        return join(relPath, conf['pathOfBuiltFiles'])
         
    def deployS3(self, conf, s3):
        
        self.bucketName = conf['bucketSubdomain']
        if "dnsDomain" in conf.keys():
            self.bucketName = self.bucketName + "." + conf['dnsDomain']
        
        if "sendReport" in conf.keys():
            for reportRequest in conf['sendReport']:
                name = "./" + reportRequest['type'] + "Report.json"
                relPath = reportRequest['destimation']
                if isfile(name):
                    shellCopy = "cp " + name + " " + join(relPath, reportRequest['type'] + "Report.json")
                    subprocess.Popen(shellCopy, shell=True)
        
        filesLocation = None
        if "source" in conf.keys():
            filesLocation = self.buildFiles(conf['source'])
        
        self.s3.upload(conf, self.bucketName, filesLocation)
        print (self.t.getMessage("deployedS3") +" " + self.bucketName)
        
        
        
        
        
        
        
        
        
        
        
        
        