from sttc.aws.config.ConfigProvider import ConfigProvider
import boto3
import gzip

class LambdaManager:
    
    def __init__(self, translator, zone):
        self.conf = ConfigProvider(zone)
        self.t = translator
        self.client = boto3.client('lambda', region_name=self.conf.region)
        
    
    
    def deleteFunction(self, lambdaConf):
        
        response = self.client.delete_function(
            FunctionName=lambdaConf['name']
        )
        code = response['ResponseMetadata']['HTTPStatusCode']
        print(self.t.getMessage("deleteFunction") + " " + str(code))
        
    '''
        Only the mandatory fields
    '''
        
                
    def createFunctionSimpleDeleteIfExists(self, lambdaConf, pathToZip):
        try:
            self.deleteFunction(lambdaConf)
        except:
            pass
        self.createFunctionSimple(lambdaConf, pathToZip)
        
            
                
    def createFunctionSimple(self, lambdaConf, pathToZip):
        
        with open(pathToZip, 'rb') as f:
            zipLambda = f.read()
    
        role = lambdaConf['role']
        accNum = self.conf.getAccountNumber() 
        role = role.replace("<AccountNumber>", accNum)
        
        response = self.client.create_function(
            FunctionName=lambdaConf['name'],
            Runtime='python3.6',
            Role=role,
            Handler=lambdaConf['handler'],
            Code={
                'ZipFile': zipLambda
            }
        )
        code = response['ResponseMetadata']['HTTPStatusCode']
        print(self.t.getMessage("createFunctionSimple") + " " + str(code))










