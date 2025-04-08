from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models.Users import User
import os




app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/api/by_uuid/{uuid}", tags=["VCard"])
def root(uuid):
    return User(uuid).finfByUuid()

@app.get("/api/{uuid}/qr", tags=["VCard"])
def dowload_file(uuid):
    current_file_path = f'./static/{uuid}.png'
    file_exist = os.path.isfile(current_file_path)
    
    if file_exist:
        return FileResponse(current_file_path, media_type="image/png")
    else:
        
        filename = User(uuid).create_qr()
        file_path = f'./static/{filename}'
        return FileResponse(file_path, media_type="image/png")

@app.get("/api/{uuid}/get", tags=["VCard"])
def download_contact(uuid):
    content, filename = User(uuid).create_vcs() 
    return Response(content=content, media_type="text/vcard",  headers={"Content-Disposition": f"attachment; filename={filename}"})



