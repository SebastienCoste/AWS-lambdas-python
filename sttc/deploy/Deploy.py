#!/usr/bin/env python3

from os.path import join
import argparse
from sttc.deploy.service import Messages as m
from sttc.aws.config import Regions as r
from sttc.deploy.service.Translator import Translator
from sttc.deploy.service import ConfReader as cr
from sttc.deploy.service.LambdaDeployer import LambdaDeployer
from sttc.deploy.service.IAMDeployer import IAMDeployer


DEPLOY_CONFIG_NAME = "deployConfig.json"
DEPLOY_CONFIG_FILEPATH = "./resource"
    
def loadConfigDeployer():
    deployerConf = join(DEPLOY_CONFIG_FILEPATH, DEPLOY_CONFIG_NAME)
    return cr.readJson(t, deployerConf)

        
    
if __name__ == '__main__':
    
    ''' parsing parameters'''
    parser = argparse.ArgumentParser()
    parser.parse_args()
    parser.add_argument("-l", "--lan", help="language: 'fr'(default) or 'en'")
    parser.add_argument("-r", "--region", help="region: 'IRL'(default). Available: NYC: us-east-2 SF: us-west-1 IRL: eu-west-1 ALL: eu-central-1 CAN: ca-central-1")
    parser.add_argument("-fp", "--filepath", help="filepath: relative or absolute filepath to the root directory of all lambdas. Default : ../lambdas")
    args = parser.parse_args()
    lan = "EN"
    region = "IRL"
    rootLambdaPath = "../lambdas"
    if args.lan:
        if args.lan.upper() in m.authorizedLan:
            lan = args.lan.upper()
        else:
            raise Exception("Unrecognized language")
    if args.filepath:
        rootLambdaPath = args.filepath.lower()
    if args.region:
        region = args.region.upper()
        if not region in r.REGION_GEO.keys():
            raise Exception("Unrecognized region")
            
        
    ''' loading tools'''
    t = Translator(lan)    
    confDeployer = loadConfigDeployer()
    if confDeployer == None:
        print (t.getMessage("errorLoadingDeployerConfig"))
        exit(1)
        
    ''' working on lambdas'''
    ld = LambdaDeployer(t, region, rootLambdaPath, DEPLOY_CONFIG_NAME, confDeployer)
    ld.manageLambda()
    
    
    
            
            
       
       
       
       
       
       
       
       
       
       
       
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            