import logging
import os


def getABI(abiName):
    currPath = os.path.dirname(os.path.abspath(__file__))
    abiFile = "{}/{}.json".format(currPath, abiName, abiName)
    try:
        with open(abiFile) as file_object:
            return file_object.read()
    except Exception as e:
        logging.error("getABI error:", e)
        return None
