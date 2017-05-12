#!/usr/bin/env python3
import shutil

from os import listdir
from os.path import isdir, join
import argparse
from sttc.deploy.service import Messages as m
from sttc.deploy.service.Translator import Translator
from sttc.deploy.service import ConfReader as cr
from sttc.aws.service.LambdaManager import LambdaManager
from pprint import pprint

DEPLOY_CONFIG_NAME = "deployConfig.json"
DEPLOY_CONFIG_FILEPATH = "./resource"
DEPLOY_REGION_ZONE = "IRL"
        
def getLambdaDir(t, path):
    onlyDir = [f for f in listdir(path) if isdir(join(path, f))]
    if onlyDir == None or len(onlyDir) == 0:
        raise Exception(t.getMessage("emptyDirs"))
    number = 1
    print (t.getMessage("chooseLambda"))
    for dir in onlyDir:
        print (str(number) + " - " + dir)
        number +=1
    res = 1
    while res <= 0 or res > number:
        resStr = input(t.getMessage("chooseNumber") + '\n')
        try:
            res = int(resStr)
        except: 
            res = 0
    return onlyDir[res -1]

def validateConf(t, conf, confDeployer):
    for item in confDeployer["mandatory"]:
        try:
            if conf[item] == None:
                print (t.getMessage("missingMandatoryArtifact") + " " + item)
                return False
        except: 
            print (t.getMessage("missingMandatoryArtifact") + " " + item)
            return False
    return True

def getConfig(t, lambdaDir, confDeployer):
    confpath = join(lambdaDir, DEPLOY_CONFIG_NAME)
    conf = cr.readJson(t, confpath)
    if validateConf(t, conf, confDeployer):
        return conf
    else:
        return None

def loadConfigDeployer(t):
    deployerConf = join(DEPLOY_CONFIG_FILEPATH, DEPLOY_CONFIG_NAME)
    return cr.readJson(t, deployerConf)
    
    
if __name__ == '__main__':
    
    ''' parsing parameters'''
    parser = argparse.ArgumentParser()
    parser.parse_args()
    parser.add_argument("-l", "--lan", help="language: 'fr'(default) or 'en'")
    parser.add_argument("-fp", "--filepath", help="filepath: relative or absolute filepath to the root directory of all lambdas. Default : ../lambdas")
    args = parser.parse_args()
    lan = "EN"
    rootLambdaPath = "../lambdas"
    if args.lan:
        if args.lan.upper() in m.authorizedLan:
            lan = args.lan.upper()
        else:
            raise Exception("Unrecognized language")
    if args.filepath:
        rootLambdaPath = args.filepath.lower()
        
        
    ''' loading tools'''
    t = Translator(lan)    
    l = LambdaManager(DEPLOY_REGION_ZONE)
    confDeployer = loadConfigDeployer(t)
    if confDeployer == None:
        print (t.getMessage("errorLoadingDeployerConfig"))
        exit(1)
     
    '''working on lambdas'''
    confLambda = None
    while confLambda == None:
        myLambda = getLambdaDir(t, rootLambdaPath)
        confLambda = getConfig(t, join(rootLambdaPath, myLambda), confDeployer)
        
    
    
    print (t.getMessage("zipping ") + " - " + myLambda)     
    pathToLambdaZip = '../lambdas/' + myLambda + '/'
    shutil.make_archive(myLambda, "zip", pathToLambdaZip)
    
    print (t.getMessage("deploying ") + " - " + myLambda)    
    l.createFunctionSimple(confLambda, join(pathToLambdaZip, myLambda)) 
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            