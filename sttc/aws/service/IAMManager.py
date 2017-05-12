from sttc.aws.config.ConfigProvider import ConfigProvider
import boto3

class IAMManager:
    
    def __init__(self, zone, conf):
        if conf == None:
            self.conf = ConfigProvider(zone)
        else:
            self.conf = conf 
        self.iam = boto3.resource('iam')
        
    #TODO
    def createRoleIfNotExists(self, rolename, arn):
        role = self.iam.Role(rolename)
