from bs4 import BeautifulSoup
import datetime
from pytz import timezone
import enum 
import jsonpickle


UTC = timezone("Europe/Paris")

class TypeInsulin(enum.Enum):
    BASAL           =  "Débit basal"
    BOLUS_SIMPLE    = "Bolus"
    BOLUS_PROL      = "Bolus prolongé"
    UNKNOWN         = "Inconnu"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, TypeInsulin))

class dataInsulin():
    def __init__(self,date, hour,type,value,unit,comm):
        self.date = datetime.datetime.strptime(date + " " + hour, "%d.%m.%y %H:%M").astimezone(UTC)
        if type in TypeInsulin.list():
            self.type = TypeInsulin(type)
        else:
            self.type = TypeInsulin.UNKNOWN


        self.value = float(value.replace(",","."))
        self.unit = unit
        self.comm = comm

    def __str__(self):
        return "%s|%s|%s|%s|" % (self.date,self.type.name,self.value,self.unit)

    def convertInJsonNS(self):
        pass

class dataInsulinOp():
    @classmethod
    def convertHtml2dataInsulin(cls,htmlContent):
        soup = BeautifulSoup(htmlContent,"html.parser")
        table = soup.find("table", { "id" : "ctl00_conContent_rgLogbookGrid_ctl00" })
        listDataInsulin = []
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            if len(cells) > 0:
                listDataInsulin.append(dataInsulin(cells[1].text,cells[2].text,cells[3].find("span").text,cells[4].text,cells[5].text,cells[6].text))
        return listDataInsulin


    @classmethod
    def saveJson(cls,listDataInsulin):
        json_obj = jsonpickle.encode(listDataInsulin)
        with open("data_file.json", "w") as write_file:
              write_file.write(json_obj)
        

