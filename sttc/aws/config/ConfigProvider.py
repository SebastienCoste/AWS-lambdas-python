from sttc.aws.config import Regions as r
from os.path import abspath
import json

DEFAULT_REGION = r.REGIONS["CA_CENTRAL_1"]

class ConfigProvider:
    
    def __init__(self, zone):
        self.region = DEFAULT_REGION
        if zone != None:
            regZone = r.REGION_GEO[zone]
            if regZone != None:
                self.region = regZone
        
        try:
            with open(abspath("../aws/resource/privateConf.json")) as private:    #For now it's a unversionned file for private data
                data = json.load(private)
                self.accountNumber = data['accountNumber']
                print(self.accountNumber)
                
            with open(abspath("../aws/resource/defaultConf.json")) as defConf:   
                data = json.load(defConf)
                for key in data.keys():
                    self.__dict__[key] = data[key]
        except:
            raise Exception()
                
    
    #TODO
    def getAccountNumber(self):
        return self.accountNumber
    
    def getRegion(self):
        return self.region