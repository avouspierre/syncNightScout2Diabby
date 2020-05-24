from bs4 import BeautifulSoup
import datetime
from pytz import timezone
import enum
import jsonpickle
import requests


UTC = timezone("Europe/Paris")

class TypeInsulin(enum.Enum):
    BASAL           =   "Débit basal"
    BOLUS_SIMPLE    =   "Bolus"
    BOLUS_PROL      =   "Bolus prolongé"
    BOLUS_COMB      =   "Combinaison de bolus"
    UNKNOWN         =   "Inconnu"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, TypeInsulin))

class dataInsulin():
    def __init__(self,date, hour,type,value,unit,comm,datefin= None):
        self.date = datetime.datetime.strptime(date + " " + hour, "%d.%m.%y %H:%M").astimezone(UTC)
        self.duration = 30
        if ("Temporaire" in comm):
            self.type = TypeInsulin(type)
            time_delta = (datefin - self.date)
            self.duration = time_delta.total_seconds() /60
        elif type in TypeInsulin.list():
            self.type = TypeInsulin(type)
        else:
            self.type = TypeInsulin.UNKNOWN

        self.value = float(value.replace(",","."))
        self.unit = unit
        self.comm = comm

    def __str__(self):
        return "%s|%s|%s|%s|%s" % (self.date,self.type.name,self.value,self.unit,self.duration)

    def convertInJsonNS(self):
        pass

    def pushInNS(self,logger,token):
        response= False
        if (self.type == TypeInsulin.BOLUS_SIMPLE or self.type == TypeInsulin.BOLUS_PROL or self.type == TypeInsulin.BOLUS_COMB):
            url = "https://cgm-pierre.herokuapp.com/api/v1/treatments?token=%s" % token
            theDate = self.date.astimezone(timezone('UTC')).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            payload = "[\n    {\n        \"enteredBy\": \"MyLife\",\n        \"eventType\": \"Meal Bolus\",\n        \"reason\": \"\",\n        \"protein\": \"\",\n        \"fat\": \"\",\n        \"insulin\": %s ,\n        \"duration\": 0,\n        \"created_at\": \"%s\",\n        \"utcOffset\": 0,\n        \"carbs\": null\n    }\n    \n  \n]" % (self.value,theDate)
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data = payload).text.encode('utf8')
        elif (self.type==TypeInsulin.BASAL and "Temporaire" in self.comm):
            url = "https://cgm-pierre.herokuapp.com/api/v1/treatments?token=%s" % token
            theDate = self.date.astimezone(timezone('UTC')).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            payload = "[\n    {\n        \"enteredBy\": \"MyLife\",\n        \"eventType\": \"Temp Basal\",\n        \"reason\": \"\",\n        \"protein\": \"\",\n        \"fat\": \"\",\n        \"absolute\": %s ,\n        \"duration\": %s,\n        \"created_at\": \"%s\",\n        \"utcOffset\": 0,\n        \"carbs\": null\n    }\n    \n  \n]" % (self.value,self.duration,theDate)
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data = payload).text.encode('utf8')
        return response

class dataInsulinOp():
    @classmethod
    def convertHtml2dataInsulin(cls,htmlContent):
        soup = BeautifulSoup(htmlContent,"html.parser")
        table = soup.find("table", { "id" : "ctl00_conContent_rgLogbookGrid_ctl00" })
        listDataInsulin = []
        datefin = datetime.datetime.now()
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            if len(cells) > 0:
                di = dataInsulin(cells[1].text,cells[2].text,cells[3].find("span").text,cells[4].text,cells[5].text,cells[6].text, datefin)
                listDataInsulin.append(di)
                if (di.type==TypeInsulin.BASAL):
                    datefin = di.date
        return listDataInsulin

    @classmethod
    def saveJson(cls,listDataInsulin):
        json_obj = jsonpickle.encode(listDataInsulin)
        with open("data_file.json", "w") as write_file:
              write_file.write(json_obj)

