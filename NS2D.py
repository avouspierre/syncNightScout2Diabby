import requests
import datetime
import pytz
import json
import os
import shutil
import logging
#import MyLifeSiteWebScrapinLastData
#import dataInsulin

from dotenv import load_dotenv
load_dotenv()
TOKEN_NS = os.getenv('TOKEN_NS')
TOKEN_DIABBY = os.getenv('TOKEN_DIABBY')
USERNAME_DIABBY = os.getenv('USERNAME_DIABBY')

baseUrlNS = os.getenv('BASEURLNS') + "/api/v1"
# 
db_file_SGV = "DB_SGV.csv"
diabbyLineTemplate = "FreeStyle LibreLink,ABAFDA43-2C2D-4F87-9847-72D3CEC39EA1,%s,0,%s,,,,,,,,,,,,,,\n"


UTC = pytz.timezone("Europe/Paris")

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

nameOfFileDiabby = os.path.join("filestorage",db_file_SGV)
nameOfFileDiabbyCp = os.path.join("filestorage","save_" + db_file_SGV)

baseUrlDiabby = "https://app.mydiabby.com/api"

# Convert Date Diabby String in DateTime
def convertDateDiabbyInDateTime(DateString):
    return datetime.datetime.strptime(DateString, "%m-%d-%Y %I:%M %p").astimezone(UTC)

# Convert DateTime in Date Diabby String 
def convertDateTimeInDateDiabby(OneDate):
    return OneDate.strftime("%m-%d-%Y %I:%M %p")

#Convert DateTime in Epoch
def convertDateTimeInEpochMms(OneDate):
    return OneDate.timestamp() * 1000 

#Convert Epoch in Epoch
def convertEpochMmsInDateTime(datestamp):
    dateFromdatestamp = datetime.datetime.fromtimestamp(datestamp / 1000)
    dateFromdatestamp.astimezone(UTC)
    return dateFromdatestamp

# Query data from NightScout
# dateFirst : dateTime of the first data
# dateEnd : dateTime of the last data
def getSGVFromNS(dateFirst,dateEnd):
    
    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    #convert date in epoch time in mms
    str_to_dt_first = convertDateTimeInEpochMms(dateFirst)
    str_to_dt_last = convertDateTimeInEpochMms(dateEnd)

    url =  "%s/entries?find[date][$gte]=%s&count=10000&find[date][$lt]=%s&token=%s" % (baseUrlNS,str_to_dt_first,str_to_dt_last,TOKEN_NS)

    response = requests.request("GET", url, headers=headers, data = payload)
    response_in_json = json.loads(response.text.encode('utf8'))
    response_in_json= sorted(response_in_json,key = lambda i: i['date'])
    return response_in_json

# Query data from NightScout
# dateFirst : dateTime of the first data
# dateEnd : dateTime of the last data
def getLastInsulinFromNS():
    
    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    url =  "%s/treatments?count=10&token=%s" % (baseUrlNS,TOKEN_NS)

    response = requests.request("GET", url, headers=headers, data = payload)
    response_in_json = json.loads(response.text.encode('utf8'))
    #response_in_json= sorted(response_in_json,key = lambda i: i['date'])
    #TODO : manage correctly !!!!!!
    if not "Sensor" in response_in_json[0]['eventType']:
        lastdate_1 = datetime.datetime.strptime(response_in_json[0]['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        timezone = pytz.utc
        lastdate = timezone.localize(lastdate_1).astimezone(UTC)
        event_type = response_in_json[0]['eventType']
        lastvalue = response_in_json[0]['insulin']
    else:
        lastdate = datetime.now - days(30)
        event_type = ""
        lastvalue = ""  
    return lastdate,event_type,lastvalue



# extract the last date/time of the data
def extractLastDateOfDiabby():
    with open(os.path.join(__location__, nameOfFileDiabby), "r") as f1:
        last_line = f1.readlines()[-1]
    
    
    return last_line.split(",")[2]


# add new data in Diabby file
def addDataInDiabbyFile(SgvDatas,fake=False):
    #copy the original file in case of issue
    shutil.copy(os.path.join(__location__, nameOfFileDiabby),os.path.join(__location__, nameOfFileDiabbyCp))

    with open(os.path.join(__location__, nameOfFileDiabby), "a") as f1:
        if not fake:
            f1.write('\n')
            for sgv in SgvDatas:
                f1.write(diabbyLineTemplate % (convertDateTimeInDateDiabby(convertEpochMmsInDateTime(sgv['date'])),sgv['sgv'])) 
                #print(diabbyLineTemplate % (convertDateTimeInDateDiabby(convertEpochMmsInDateTime(sgv['date'])),sgv['sgv'])) 
    
    return True


def getBearFromDiabbySite():
    url= baseUrlDiabby + "/getToken"
    payload = "username=%s&password=%s" % (USERNAME_DIABBY,TOKEN_DIABBY)
    headers= {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    return json.loads(response.text.encode('utf-8'))["token"]


def pushDiabbyFileInDiabby(filename):
    token = 'Bearer %s' % getBearFromDiabbySite()
    url= baseUrlDiabby + "/upload-data/freestyle"
    payload = {}
    files = [
         ('file', open(filename,'rb'))
    ]
    headers = {
        'Authorization': token
    }

    response = requests.request("POST", url, headers=headers, data = payload, files = files)
    return response.text.encode('utf8')
    

def main():
    logging.basicConfig(filename=os.path.join('filestorage','NS2D.log'),level=logging.INFO)
    logging.info("start of the process: %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    # process to collect data glycemia from NS

    dateStart = convertDateDiabbyInDateTime(extractLastDateOfDiabby())
    logging.info("date of the start Data: %s" % dateStart.strftime("%Y-%m-%d %H:%M"))
    dateEnd =  datetime.datetime.now()  # dateStart + datetime.timedelta(days=1)
    logging.info("date of the end Data: %s" % dateEnd.strftime("%Y-%m-%d %H:%M"))
    SgvDatas = getSGVFromNS(dateStart,dateEnd)
    logging.info("nb of data from NS: %s" % len(SgvDatas))

    if addDataInDiabbyFile(SgvDatas,fake=False):
        result = pushDiabbyFileInDiabby(os.path.join(__location__, nameOfFileDiabby))
        logging.info(result)
    else:
        logging.error("Issue with data loading in Diabby")

    # TODO Management of the data provided by MyLife
    # Process to push insulin to NS
    #logging.info("try to collect the last data from NS")
    #lastdate,event_type,lastvalue= getLastInsulinFromNS()
    #collect all data from MyLife
    #dataInsulin = MyLifeSiteWebScrapingLastData.ScrapMyLife()
    #last date please
    #if (dataInsulin[0].date > lastdate):
    #    #print("%s:%s" % (dataInsulin[0].date,lastdate))
                
if (__name__ == "__main__"):
    main()
