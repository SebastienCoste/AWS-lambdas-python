import boto3
import json

print('Loading function')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    '''print("value1 = " + event['key1'])
    print("value2 = " + event['key2'])
    print("value3 = " + event['key3'])
    print(listBuckets())
    return event['key1']'''  # Echo back the first key value
    #raise Exception('Something went wrong')
    list = readJson("./phones.json")
    return list
    
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
    