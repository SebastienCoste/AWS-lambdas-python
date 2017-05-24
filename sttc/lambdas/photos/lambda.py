import boto3
import json
from pprint import pprint

print('Loading function')




def handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    '''print("value1 = " + event['key1'])
    print("value2 = " + event['key2'])
    print("value3 = " + event['key3'])
    print(listBuckets())
    return event['key1']'''  # Echo back the first key value
    #raise Exception('Something went wrong')
    
    conf = readJson("./conf.json")
    bucketName = conf['data']['bucket']
    region = conf['data']['region']
    
    '''
    s3res = boto3.resource('s3')
    bucket = s3res.Bucket(bucketName)
    res = bucket.get_available_subresources()
    pprint(res)
    '''
    
    s3cl = boto3.client('s3')
    listObject =s3cl.list_objects(Bucket=bucketName)
    report = {}
    pics = []
    for elmt in listObject['Contents']:
        pic = {}
        pic['name'] = elmt['Key'].split(".")[0]
        pic['link'] =  "https://s3-" + region + ".amazonaws.com/" + bucketName + "/" + elmt['Key']
        pics.append(pic)
    report['pics'] = pics
    
    pprint(report)
    
    return report
    
def listBuckets():

    s3 = boto3.resource('s3')
    result = []
    for bucket in s3.buckets.all():
        result.append(bucket.name)

    return result


def readJson(filepath):
    
    try:
        with open(filepath) as data_file:    
            data = json.load(data_file)
            return data
    except:
        print ("errorLoadingJson")
        return None
    
    
if __name__ == '__main__':
    handler(None, None)
    