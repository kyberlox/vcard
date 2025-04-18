from models.B24 import b24
from transliterate import translit
import qrcode
import vobject
import base64
import requests



def cyrillic_to_latin(text: str) -> str:
    return translit(text, 'ru', reversed=True)



class User:
    def __init__(self, uuid=""):
        self.uuid = uuid
    
    def findByIDdepart(self, id):
        depart = b24().getDepartByID(id)
        if depart != []:
            return depart
        else:
            return {"status" : False, "msg" : "Департамент не обнаружен"}

    def finfByUuid(self):
        titles_to_change = {'UF_USR_1696592324977' : 'Direction', 'UF_USR_1705744824758' : 'Division', 'UF_USR_1707225966581' : 'Combination'}
        search = b24().getUsersByUuid(f"ad|{self.uuid}")
        if search != []:
            for title, new_title in titles_to_change.items():
                if title in search[0].keys():
                    value = search[0].pop(title)
                    search[0][new_title] = value

            departments_id = search[0]["UF_DEPARTMENT"]
            num_to_word = []
            for department in departments_id:
                depart = self.findByIDdepart(department)
                name = depart[0]["NAME"]
                num_to_word.append(name)
            search[0]["UF_DEPARTMENT"] = num_to_word
            return search[0]
        else:
            return {"status" : False, "msg" : "Пользователь с таким uuid не обнаружен"}

    

    def create_qr(self):
        data = f'https://vcard.emk.ru/{self.uuid}'
        filename = f'{self.uuid}.png'
        img = qrcode.make(data)
        img.save(f'./static/{filename}')
        return filename

    def create_vcs(self):
        user_info = self.finfByUuid()
        filename = f'{cyrillic_to_latin(user_info['LAST_NAME'])}-{cyrillic_to_latin(user_info['NAME'])}-{cyrillic_to_latin(user_info['SECOND_NAME'])}.vcf'

        important_param = ['NAME', 'LAST_NAME', 'SECOND_NAME', 'EMAIL', "PERSONAL_MOBILE", 'WORK_PHONE', 'WORK_POSITION','Direction', "PERSONAL_PHOTO"]

        vcard = vobject.vCard()
        vcard.add("FN").value = f"{user_info['LAST_NAME']} {user_info['NAME']} {user_info['SECOND_NAME']}"
        vcard.add("N").value = vobject.vcard.Name(
            family=user_info['LAST_NAME'],
            given=user_info['NAME'],
            additional=user_info['SECOND_NAME']
        )
        user_depart = None
        user_position = None
        user_company = None
        for key in important_param:
            if key in user_info.keys():
                if key == "PERSONAL_MOBILE":                    
                    vcard.add("TEL").value = user_info["PERSONAL_MOBILE"]
                    vcard.add("TEL").type_param = "CELL"

                elif key == 'WORK_PHONE':                    
                    vcard.add("TEL").value = user_info['WORK_PHONE']
                    vcard.add("TEL").type_param = "WORK"
                
                elif key == "EMAIL":
                    vcard.add("EMAIL").value = user_info["EMAIL"]
                    domen = user_info["EMAIL"].split("@")
                    if domen[-1] == 'emk.ru':
                        user_company = 'АО "НПО "ЭМК"'

                elif key == 'Direction':                    
                    user_depart = user_info["Direction"][0]
                    
                elif key == "WORK_POSITION":
                    user_position = user_info["WORK_POSITION"]
                    
                elif key == "PERSONAL_PHOTO":
                    if user_info['PERSONAL_PHOTO'] != "":
                        user_url = user_info['PERSONAL_PHOTO']
                        response = requests.get(user_url)
                        if response.status_code == 200:
                            photo = base64.b64encode(response.content).decode("utf-8")
                            vcard.add("PHOTO").value = photo
                            vcard.add("PHOTO").type_param = "PNG"
                        else:
                            print(response.status_code)
            else:
                pass
        
        if user_company is not None:
            if len(user_position) != 0 and len(user_depart) != 0:
                vcard.add("TITLE").value = f'{user_company} - {user_depart}, {user_position}'
            elif len(user_position) != 0 and len(user_depart) == 0:
                vcard.add("TITLE").value = f"{user_company} - {user_position}"
            elif len(user_depart) != 0 and len(user_position) == 0:
                vcard.add("TITLE").value = f"{user_company} - {user_depart}"
        else:
            if len(user_position) != 0 and len(user_depart) != 0:
                vcard.add("TITLE").value = f'{user_depart}, {user_position}'
                print(3)
            elif len(user_position) != 0 and len(user_depart) == 0:
                vcard.add("TITLE").value = user_position
                print(2)
            elif len(user_depart) != 0 and len(user_position) == 0:
                vcard.add("TITLE").value = user_depart
                print(1)


        content = vcard.serialize()
        
        return content, filename


