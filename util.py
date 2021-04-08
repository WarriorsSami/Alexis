import json


def getAppConfig(path):
    inputStream = open(path, "r")
    config = json.loads(inputStream.read())

    # print(config)
    inputStream.close()
    return config
