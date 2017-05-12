import boto3
from sttc.lambdas.config.ConfigProvider import ConfigProvider


def handlerMethod():
    conf = ConfigProvider()

    s3 = boto3.resource('s3')
    
    for bucket in s3.buckets.all():
        print(bucket.name)
    
