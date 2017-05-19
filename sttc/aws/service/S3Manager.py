'''
Created on 19 mai 2017

@author: static
'''

from sttc.aws.config.ConfigProvider import ConfigProvider
import boto3
import json
import os

class S3Manager():
    
    def __init__(self, translator, zone):
        self.conf = ConfigProvider(zone)
        self.t = translator
        self.client = boto3.client('s3', region_name=self.conf.region)
        self.resource = boto3.resource('s3', region_name=self.conf.region)
        
    
    def upload(self, conf, bucketName, filesLocation):
        
        bucket = self.createBucketIfNotExist(conf, bucketName)
        
        if 'corsConfiguration' in conf.keys():
            cors = conf['corsConfiguration']
            self.client.put_bucket_cors(Bucket=bucketName, CORSConfiguration = cors)
        
        if 'bucketPolicy' in conf.keys():
            self.setPolicy(bucketName, conf['bucketPolicy'])
        
        if 'bucketHosting' in conf.keys():
            self.setWebHosting(bucketName, conf['bucketHosting'])
        
        #TODO copy files
        if filesLocation != None:
            self.uploadFiles(filesLocation, bucketName)
        
    def createBucketIfNotExist(self, conf, bucketName):
        
        try:
            self.resource.meta.client.head_bucket(Bucket=bucketName)
        except:
            self.client.create_bucket(
                ACL=conf['bucketPermissions']['ACL'],
                Bucket=bucketName,
                CreateBucketConfiguration={
                    'LocationConstraint': self.conf.region
                }
            )
        return self.resource.Bucket(bucketName)
        
    
    def setPolicy(self, bucketName, conf):
        
        fullPolicy = json.dumps(conf).replace("<bucketName>", bucketName)
        
        self.client.put_bucket_policy(
            Bucket=bucketName, 
            Policy = fullPolicy
            )
        
    def setWebHosting(self, bucketName, conf):
        
        websiteConf={}
        
        if 'errorDocument' in conf.keys():
            websiteConf["ErrorDocument"] = {"Key": conf['errorDocument']}
            
        if 'indexDocument' in conf.keys():
            websiteConf["IndexDocument"] = {"Suffix": conf['indexDocument']}

        if "routingRules" in conf.keys():
            routingRules = []
            for routingRule in conf["routingRules"]:
                routingRule["Redirect"]["HostName"] = routingRule["Redirect"]["HostName"].replace("<bucketName>", bucketName)
                routingRules.append(routingRule)
            websiteConf["RoutingRules"] = routingRules
        
        if "RedirectAllRequestsTo" in conf.keys():
            
            redirectAllRequestsTo = conf["RedirectAllRequestsTo"]
            redirectAllRequestsTo["HostName"] = redirectAllRequestsTo["HostName"].replace("<bucketName>", bucketName)
            websiteConf["RedirectAllRequestsTo"] = redirectAllRequestsTo
        
        
        
        self.client.put_bucket_website(
            Bucket=bucketName,
            WebsiteConfiguration=websiteConf
        )
        
        
        
    def uploadFiles(self, path, bucketName):
        
        for root, dirs, files in os.walk(path):

            for filename in files:
        
                # construct the full local path
                local_path = os.path.join(root, filename)
            
                # construct the full Dropbox path
                relative_path = os.path.relpath(local_path, path)
            
                # relative_path = os.path.relpath(os.path.join(root, filename))
                try:
                    self.client.delete_object(Bucket=bucketName, Key=relative_path)
                except:
                    pass
                self.client.upload_file(local_path, bucketName, relative_path)
        
        
        
        
        
        
        
        
        
        