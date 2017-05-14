import json
from os.path import join

def readJson(t, filepath):
    
    try:
        with open(filepath) as data_file:    
            data = json.load(data_file)
            return data
    except:
        print (t.getMessage("errorLoadingJson"))
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


    
    