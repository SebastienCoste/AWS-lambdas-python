import json


def readJson(t, filepath):
    
    try:
        with open(filepath) as data_file:    
            data = json.load(data_file)
            return data
    except:
        print (t.getMessage("errorLoadingJson"))
        return None