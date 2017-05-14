'''
Created on 13 mai 2017

@author: static
'''
from sttc.aws.config.ConfigProvider import ConfigProvider
import boto3
from os.path import join

class APIGatewayManager:

    def __init__(self, zone, translator):
        self.conf = ConfigProvider(zone)
        self.t = translator
        self.gateway = boto3.client('apigateway', region_name=self.conf.region)
        
        '''
       create a new REST API, 
       add a Resource, 
       and add a method to that Resource.
       give the role to call lambdas
       '''
       
    def createAPI(self, conf):
        
        api = self.getApiByNameOrId(name=conf['name'])
        if api == None:
            response = self.gateway.create_rest_api(
                name=conf["name"],
                description='auto generated API',
                version=conf["version"]
            )
            conf['apiId'] = response['id']
            code = response['ResponseMetadata']['HTTPStatusCode']
            print(self.t.getMessage("createAPI") + " " + conf['apiId'] + "(" + code + ")")
        else:
            if not 'apiId' in conf.keys():
                conf['apiId'] = api['id']
                
        root = self.getResourceByPath(conf['apiId'], "/")
        print(self.t.getMessage("createResource") + " " + root['id'])
        
        if "resource" in conf.keys():
            for resource in conf['resource']:
                self.createResource(resource, conf['apiId'], root['id'], "/")
        
        
    def createResource(self, confResource, apiId, parentId, absoluteParentPath):
        
        absolutePath = join(absoluteParentPath, confResource['pathPart'])
        resource = self.getResourceByPath(apiId, absolutePath)
        resourceId = None
        
        if resource == None:
            response = self.gateway.create_resource(
                restApiId= apiId,
                parentId= parentId,
                pathPart= confResource['pathPart']
            )
            resourceId = response['id']
            print(self.t.getMessage("createResource") + " " + resourceId)
        else:
            resourceId = resource['id']
        
        if "method" in confResource.keys():
            for method in confResource['method']:
                #pass
                self.createMethod(method, apiId, resourceId)
            
        if "resource" in confResource.keys():
            for resource in confResource['resource']:
                self.createResource(resource, apiId, resourceId, absolutePath)
        
        
    def createMethod(self, confMethod, apiId, resourceId):
        
        method = self.getMethodOfResource(apiId, resourceId, confMethod['httpMethod'])
        createMethod = method == None or method['authorizationType'] != confMethod['authorizationType']
        if not createMethod:
            if "authorizerId" in method.keys() and not "authorizerId" in confMethod.keys():
                createMethod = True
            if not "authorizerId" in method.keys() and "authorizerId" in confMethod.keys():
                createMethod = True
            
        if createMethod:
            if method != None:
                self.removeMethod(confMethod['httpMethod'], apiId, resourceId)
            
            authId = ""
            if "authorizerId" in confMethod.keys():
                authId = confMethod['authorizerId']
            
            response = self.gateway.put_method(
                restApiId= apiId,
                resourceId= resourceId,
                httpMethod= confMethod['httpMethod'],
                authorizationType= confMethod['authorizationType'],
                authorizerId=authId,
                apiKeyRequired=False
            )
            print(self.t.getMessage("createMethod") + " " + resourceId + " : " +confMethod['httpMethod'])
        
        
        
        
    def removeMethod(self, httpMethod, apiId, resourceId):
        
        self.gateway.delete_method(
            restApiId=apiId,
            resourceId=resourceId,
            httpMethod=httpMethod
        )
    
    
    def getResourceByPath(self, apiId, path):

        resource = None
        try:
            resourceItems = self.gateway.get_resources(restApiId=apiId, limit=500)['items']
        
            for item in resourceItems:
                if item['path'] == path:
                    resource = item
                    break
        
            return resource
        except:
            return None
        
    
    def getApiByNameOrId(self, name=None, apiId=None ):
        
        if name == None and apiId == None:
            return False
        
        response = self.gateway.get_rest_apis()
        
        for item in response['items']:
            if name != None:
                if item['name'] == name:
                    return item
            if apiId != None:
                if item['id'] == apiId:
                    return item
        
        return None
                
    
    def getMethodOfResource(self, apiId, resourceId, httpMethod):
        
        try:
            return self.gateway.get_method(
                restApiId= apiId,
                resourceId= resourceId,
                httpMethod= httpMethod
            )
        except:
            return None
        
        
    def linkMethodAndLambda(self, apiName, path, httpMethod, confLambda):
        
        api = self.getApiByName(apiName)
        resource = self.getResourceByPath(api['id'], path)
        method = self.getMethodOfResource(api['id'], resource['id'], httpMethod)
        #TODO next
        
        
        
        
        
        
        
        
        
        
        
        
        
        