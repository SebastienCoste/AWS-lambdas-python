import json
from os.path import join

def readJson(t, filepath):
    
    try:
        with open(filepath) as data_file:    
            data = json.load(data_file)
            return data
    except:
        print (t.getMessage("errorLoadingJson") + " " + filepath)
        return None
    
    
def getPathAndMethodFromResource(path, resource, key, value):
    
    subPath = join(path, resource['pathPart'])
    if "method" in resource.keys():
        for method in resource['method']:
            if key in method.keys() and value == method[key]:
                return subPath, method['httpMethod']
    if "resource" in resource.keys():
            for subResource in resource['resource']:
                fullPath, httpMethod = getPathAndMethodFromResource(subPath, subResource, key, value)
                if fullPath != None and httpMethod != None:
                    return fullPath, httpMethod
    
    return None, None


def getPathAndMethodMatchingKeyValue(conf, key, value):
    
    if "resource" in conf.keys():
            for resource in conf['resource']:
                return getPathAndMethodFromResource("/", resource, key, value)


class Validator():
    
    def __init__(self, translator, confName, typeSource):
        self.t = translator
        self.confName = confName
        self.type = typeSource
    
    def getConfig(self, directory, confDeployer):
        confpath = join(directory, self.confName)
        conf = readJson(self.t, confpath)
        if self.validateConf(conf, confDeployer):
            return conf
        else:
            return None
        
    def validateConf(self, conf, confDeployer):
        
        for item in confDeployer["mandatory"][self.type]:
            try:
                if conf[item] == None:
                    print (self.t.getMessage("missingMandatoryArtifact") + " " + item)
                    return False
            except: 
                print (self.t.getMessage("missingMandatoryArtifact") + " " + item)
                return False
        for item in confDeployer["conditionnalMandatory"][self.type]:
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
    