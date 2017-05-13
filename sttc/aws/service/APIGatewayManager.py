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
       '''
       
    def createAPI(self, confGateway):
        
        response = self.gateway.create_rest_api(
            name=confGateway["name"],
            description='auto generated API',
            version=confGateway["version"]
        )
        
        code = response['ResponseMetadata']['HTTPStatusCode']
        print(self.t.getMessage("createAPI") + " " + str(code))
        
        