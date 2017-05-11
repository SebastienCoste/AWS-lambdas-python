#!/usr/bin/env python3
import shutil

from os import listdir
from os.path import isdir, join
import argparse
from sttc.deploy.service import Messages as m
from sttc.deploy.service.Translator import Translator

        
def getLambdaDir(t):
    onlyDir = [f for f in listdir("../lambdas") if isdir(join("../lambdas", f))]
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


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.parse_args()
    parser.add_argument("-l", "--lan", help="language: 'fr'(default) or 'en'")
    args = parser.parse_args()
    lan = "EN"
    if args.lan:
        if args.lan.upper() in m.authorizedLan:
            lan = args.lan.upper()
        else:
            raise Exception("Unrecognized language")
    t = Translator(lan)    
            
    myLambda = getLambdaDir(t)
    
    print (t.getMessage("deploying") + " - " + myLambda)      
    
    shutil.make_archive(myLambda, "zip", '../lambdas/' + myLambda + '/')
    
            