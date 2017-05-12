from sttc.aws.config.ConfigProvider import ConfigProvider
import boto3
import gzip

class LambdaManager:
    
    def __init__(self, zone):
        self.conf = ConfigProvider(zone)
        self.client = boto3.client('lambda')
        
    
    '''
        Only the mandatory fields
    '''
    def createFunctionSimple(self, lambdaConf, pathToZip):
        
        with open(pathToZip, 'rb') as f:
            zipLambda = f.read()
    
        role = lambdaConf['role']
        accNum = self.conf.getAccountNumber() 
        role.replace("<AccountNumber>", accNum)
        
        response = self.client.create_function(
            FunctionName=lambdaConf['name'],
            Runtime='python3.6',
            Role=role,
            Handler=lambdaConf['handler'],
            Code={
                'ZipFile': zipLambda,
                'S3Bucket': lambdaConf['S3Bucket'],
                'S3Key': lambdaConf['S3Key'],
                'S3ObjectVersion': lambdaConf['S3ObjectVersion']
            }
        )