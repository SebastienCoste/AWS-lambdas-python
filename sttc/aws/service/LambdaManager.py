from sttc.aws.config.ConfigProvider import ConfigProvider
import boto3

class LambdaManager:
    
    def __init__(self):
        conf = ConfigProvider()
        client = boto3.client('lambda')
        
    
    #TODO
    def createFunction(self, lambdaName, pathToZip):
        
        response = self.client.create_function(
            FunctionName=lambdaName,
            Runtime='python3.6',
            Role='string',
            Handler='string',
            Code={
                'ZipFile': b'bytes',
                'S3Bucket': 'string',
                'S3Key': 'string',
                'S3ObjectVersion': 'string'
            },
            Description='string',
            Timeout=123,
            MemorySize=123,
            Publish=True|False,
            VpcConfig={
                'SubnetIds': [
                    'string',
                ],
                'SecurityGroupIds': [
                    'string',
                ]
            },
            DeadLetterConfig={
                'TargetArn': 'string'
            },
            Environment={
                'Variables': {
                    'string': 'string'
                }
            },
            KMSKeyArn='string',
            TracingConfig={
                'Mode': 'Active'|'PassThrough'
            },
            Tags={
                'string': 'string'
            }
)