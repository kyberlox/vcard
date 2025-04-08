from bitrix24 import Bitrix24

class b24:
    def __init__(self):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/qunp7dwdrwwhsh1w/")
        

    def getUsersByUuid(self, uuid):
        
        filter = {
                "XML_ID" : uuid
        }
        result = self.bx24.callMethod('user.search', filter=filter)
        return result

    def getDepartByID(self, id):

        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/wk7uewb9l4xjo0xc/")

        result = self.bx24.callMethod('department.get', ID=id)
    
        return result
