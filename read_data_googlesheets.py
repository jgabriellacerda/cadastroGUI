from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import sys
import time
import firebase_connection as fc

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def create_client():
    creds = ServiceAccountCredentials.from_json_keyfile_name('sheets_creds.json',SCOPES)
    client = gspread.authorize(creds)
    return client


def read_google_sheet(client):

    cadastro = client.open("Cadastro de Membros 2021").worksheet("Cadastro de Membros")
    
    data = cadastro.get_all_values()
    return data
        


client = create_client()
data = read_google_sheet(client)

fb_con = fc.FirebaseConnection()

fb_con.login('gabriel.lacerda@engenharia.ufjf.br','654321')

var_keys = {'ID':0,'nome':3, 'email':12, 'dataNascimento':6, 'cargo':4, 'categoria_area':1, 'dataIngresso':5,
                         'cidadeOrigem':7, 'curso':8, 'previsaoConclusao':9, 'cidadeAtual':10, 'tamCamisa':11, 'celular':13}

data.pop(0)
data.pop()

for linha in data:
    membro = {}
    for var_key in var_keys:
        membro[var_key] = linha[var_keys[var_key]]
    print(membro)
    # fb_con.new_person(membro)