'''
Created on 13 mai 2017

@author: static
'''
from sttc.aws.config.ConfigProvider import ConfigProvider
import boto3

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
        
        response = self.gateway.create_rest_api(
            name=conf["name"],
            description='auto generated API',
            version=conf["version"]
        )
        
        conf['apiId'] = response['id']
        code = response['ResponseMetadata']['HTTPStatusCode']
        print(self.t.getMessage("createAPI") + " " + conf['apiId'])
        
        root = self.getResourceByPath(conf['apiId'], "/")
        print(self.t.getMessage("createResource") + " " + root['id'])
        self.createResource(conf['resource'], conf['apiId'], root['id'])
        
    def createResource(self, confResource, apiId, parentId):
        
        response = self.gateway.create_resource(
            restApiId= apiId,
            parentId= parentId,
            pathPart= confResource['pathPart']
        )
        
        resourceId = response['id']
        print(self.t.getMessage("createResource") + " " + resourceId)
        
        
        if "method" in confResource.keys():
            for method in confResource['method']:
                pass
                #self.createMethod(method, apiId, resourceId)
            
        if "resource" in confResource.keys():
            self.createResource(confResource["resource"], apiId, resourceId)
        
    def createMethod(self, confMethod, apiId, resourceId):
        
        authId = ""
        if "authorizerId" in confMethod.keys():
            authId = confMethod['authorizerId']
        operationName = ""
        if "operationName" in confMethod.keys():
            operationName = confMethod['operationName']
        
        response = self.gateway.put_method(
            restApiId= apiId,
            resourceId= resourceId,
            httpMethod= confMethod['httpMethod'],
            authorizationType= confMethod['authorizationType'],
            authorizerId=authId,
            apiKeyRequired=False,
            operationName= operationName
        )
        
        
        methodId = response['id']
        print(self.t.getMessage("createMethod") + " " + methodId)
        
    
    def getResourceByPath(self, rest_api_id, path):

        resource = None
        resource_items = self.gateway.get_resources(restApiId=rest_api_id, limit=500)['items']
    
        for item in resource_items:
            if item['path'] == path:
                resource = item
                break
    
        return resource
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        