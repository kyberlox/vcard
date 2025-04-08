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
    
    def finfByUuid(self):
        return b24().getUsersByUuid(f"ad|{self.uuid}")

    def findByIDdepart(self, id):
        return b24().getDepartByID(id)

    def create_qr(self):
        data = f'https://vcard.emk.ru/{self.uuid}'
        filename = f'{self.uuid}.png'
        img = qrcode.make(data)
        img.save(f'./static/{filename}')
        return filename

    def create_vcs(self):
        user_info = self.finfByUuid()
        filename = f'{cyrillic_to_latin(user_info[0]['LAST_NAME'])}-{cyrillic_to_latin(user_info[0]['NAME'])}-{cyrillic_to_latin(user_info[0]['SECOND_NAME'])}.vcf'

        important_param = ['NAME', 'LAST_NAME', 'SECOND_NAME', 'EMAIL', "PERSONAL_MOBILE", 'WORK_PHONE', 'WORK_POSITION','UF_DEPARTMENT', "PERSONAL_PHOTO"]

        vcard = vobject.vCard()
        vcard.add("FN").value = f"{user_info[0]['LAST_NAME']} {user_info[0]['NAME']} {user_info[0]['SECOND_NAME']}"
        vcard.add("N").value = vobject.vcard.Name(
            family=user_info[0]['LAST_NAME'],
            given=user_info[0]['NAME'],
            additional=user_info[0]['SECOND_NAME']
        )
        user_depart = None
        user_position = None
        user_company = None
        for key in important_param:
            if key in user_info[0].keys():
                if key == "PERSONAL_MOBILE":                    
                    vcard.add("TEL").value = user_info[0]["PERSONAL_MOBILE"]
                    vcard.add("TEL").type_param = "CELL"

                elif key == 'WORK_PHONE':                    
                    vcard.add("TEL").value = user_info[0]['WORK_PHONE']
                    vcard.add("TEL").type_param = "WORK"
                
                elif key == "EMAIL":
                    vcard.add("EMAIL").value = user_info[0]["EMAIL"]
                    domen = user_info[0]["EMAIL"].split("@")
                    if domen[-1] == 'emk.ru':
                        user_company = 'АО "НПО "ЭМК"'

                elif key == 'UF_DEPARTMENT':                    
                    id_depart = user_info[0]['UF_DEPARTMENT'][0]
                    res = self.findByIDdepart(id_depart)
                    if res:
                        user_depart = res[0]['NAME']
                    
                elif key == "WORK_POSITION":
                    user_position = user_info[0]["WORK_POSITION"]
                    
                elif key == "PERSONAL_PHOTO":
                    if user_info[0]['PERSONAL_PHOTO'] != "":
                        user_url = user_info[0]['PERSONAL_PHOTO']
                        response = requests.get(user_url)
                        if response.status_code == 200:
                            photo = base64.b64encode(response.content).decode("utf-8")
                            vcard.add("PHOTO").value = photo
                            vcard.add("PHOTO").type_param = "PNG"
                        else:
                            print(response.status_code)
            else:
                pass
        
        if len(user_company) != 0:
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


