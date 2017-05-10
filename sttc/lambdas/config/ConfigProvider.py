from sttc.lambdas.config.Regions import REGIONS


DEFAULT_REGION = REGIONS["CA_CENTRAL_1"]

class ConfigProvider:
    
    def __init__(self):
        self.region = DEFAULT_REGION