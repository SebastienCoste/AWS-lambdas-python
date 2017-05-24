import boto3
import json
import base64

print('Loading function')


def handler(event, context):
    
    
    conf = readJson("./conf.json")
    bucketName = conf['data']['bucket']
    name = "elephant.jpg"
    typeImg = "jpg"
    if not event == None:
        name = event['name']
        typeImg = event['type']
    
    print("name: ", name, "-", typeImg)
    
    obj = boto3.resource('s3').Object(bucketName, name)
    print("obj: " + str(obj))
    obj.download_file('./' + name)
    print("download obj" )
    encoded = base64.b64encode(open('./' + name, "rb").read())
    print("enc:", encoded)
    data = "data:image/" + typeImg + ";base64," + str(encoded)
    res = json.dumps({ "data" : data})
    print("res:", res)
    return res
    
    
    
    

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
    