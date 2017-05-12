from sttc.aws.config.ConfigProvider import ConfigProvider
import boto3
import json

class IAMManager:
    
    def __init__(self, translator, zone):
        self.conf = ConfigProvider(zone)
        self.t = translator
        self.iam = boto3.resource('iam', region_name=self.conf.region)
        
    #TODO
    def createRoleIfNotExists(self, rolename):
        
        try:
            role = self.iam.Role(rolename)
            role.load()
            print(role.AssumeRolePolicy())
        except:
            policyDocument = json.dumps(self.conf.lambdaRole)
            roleCreated = self.iam.create_role(
                RoleName = rolename,
                Path = "/",
                AssumeRolePolicyDocument = policyDocument
            )
            response = roleCreated.attach_policy(
                PolicyArn=self.conf.lambdaPolicyArn
            )
                
            code = response['ResponseMetadata']['HTTPStatusCode']
            print(self.t.getMessage("createRole") + " " + str(code))
        
        
        
