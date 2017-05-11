from sttc.aws.config import Regions as r


DEFAULT_REGION = r.REGIONS["CA_CENTRAL_1"]

class ConfigProvider:
    
    def __init__(self):
        self.region = DEFAULT_REGION