from fastapi import FastAPI, status, HTTPException
from fastapi.requests import Request
from models import Multipli2,Medie2,Fasce2,Multipli4,Medie4,Fasce4
from database import engine
from sqlmodel import Session,select
from typing import Optional,List
import uvicorn
from fastapi.params import Depends
import pandas as pd
import os

app = FastAPI(title="InfoValuationAPI", description="made by Daniele Grotti - InfoManager SRL", version="1.0")

session=Session(bind=engine)

############################################  AUTH  ############################################################
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import uvicorn

SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 6000000 #16/02/2023 --> 6 anni

db_auth = {
    "info": {
        "username": "info", #passw:info1234
        "full_name": "Daniele Grotti",
        "email": "d.grotti@infomanager.com",
        "hashed_password": "$2b$12$c5yKOY4AT2IYtZU4AcDIyuxbuJRwWxXytSZrkXvFE3uLBBvzdY3jW",
        "disabled": False
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None


class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None


class UserInDB(User):
    hashed_password: str

#########################################################################

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db_auth, username: str):
    if username in db_auth:
        user_data = db_auth[username]
        return UserInDB(**user_data)


def authenticate_user(db_auth, username: str, password: str):
    user = get_user(db_auth, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_user(db_auth, username=token_data.username)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

#### to generate hashed_passw
# pwd = get_password_hash("frenz1234") #password
# print(pwd)

#############################################################################################################################

@app.post("/token", response_model=Token,tags=["OAuth2"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db_auth, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/auth/", response_model=User,tags=["OAuth2"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/auth/info/",tags=["OAuth2"])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]

##############################################################################################################
##############################################################################################################

@app.get('/',status_code=status.HTTP_200_OK)
def home():
    return{"hello":"world"}

## GET complete list of sectors
@app.get('/list_sectors',status_code=status.HTTP_200_OK,)
async def get_sectors_list(current_user: User = Depends(get_current_active_user)):
    print(current_user)
    statement = select(Multipli2.settore).distinct()
    result = session.exec(statement).all()
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result

################################################################################
######################### SQLMODEL ---> PANDAS #################################
from sqlmodel import Field, SQLModel

def sqlmodel_to_df(objects: List[SQLModel], set_index: bool = True) -> pd.DataFrame:
    """Converts SQLModel objects into a Pandas DataFrame.
    Usage
    ----------
    df = sqlmodel_to_df(list_of_sqlmodels)
    Parameters
    ----------
    :param objects: List[SQLModel]: List of SQLModel objects to be converted.
    :param set_index: bool: Sets the first column, usually the primary key, to dataframe index."""

    records = [obj.dict() for obj in objects]
    columns = list(objects[0].schema()["properties"].keys())
    df = pd.DataFrame.from_records(records, columns=columns)
    return df.set_index(columns[0]) if set_index else df

################################################################################
######################### PUBLISH TO GOOGLESHEET #################################

import gspread as gs
from datetime import datetime

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

######## append  to google sheet###
# installare nel progetto GCP googlesheetAPI e googledriveAPI
#condivedere il google sheet con la mail:"test-79@bifornew2022.iam.gserviceaccount.com"
## tecnicoinfo-->Infovaluationapi/UtilizzoChiamate
def append_googlesheet(endpoint:str,sector:str,user:str):
    gsheetId = '1AP4EdCoBq5Su3R9NOEPiKSBRaeaQS_JrbisIAfUQQfA'
    gc = gs.service_account(filename=BASE_DIR + "/new_bigquery.json")
    sh = gc.open_by_key(gsheetId)
    worksheet = sh.sheet1
    #ogni lista è una riga
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    worksheet.append_rows([[dt_string,endpoint,sector,user,1]])

    #worksheet.clear() #clear sheet
    #replace all values
    #worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print('Published_google_sheet!')

######################################################################################
########################### MULTIPLI #################################################

# ## GET complete Table infovaluation
# @app.get('/settori', response_model=List[Multipli],status_code=status.HTTP_200_OK,tags=["Multipli"])
# async def get_all_sectors():
#     statement = select(Multipli)
#     results = session.exec(statement).all()
#     return results

# ## POST sector data inside DB
# @app.post('/settori', response_model=Multipli,status_code=status.HTTP_201_CREATED,tags=["Multipli"])
# async def create_a_sector(multipli:Multipli=Depends()):
#     new_sector = Multipli(anno=multipli.anno, settore=multipli.settore)
#     session.add(new_sector)
#     session.commit()
#     return new_sector

## GET a sector by ID (only first one)
@app.get('/settori/{settore_id}', response_model=Multipli2,tags=["Multipli"])
async def get_a_sector_byid(settore_id:int):
    statement = select(Multipli2).where(Multipli2.id==settore_id)
    result = session.exec(statement).first()
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result

# ## CHANGE a sector by ID (only first one)
# @app.put('/record/{primary}', response_model=Multipli,tags=["Multipli"])
# async def update_a_sector(primary:int,settore:Multipli=Depends()):
#     statement = select(Multipli).where(Multipli.primary==primary)
#     result = session.exec(statement).first()
#     session.commit()
#     return result

# ## DELETE a sector by ID (only first one) 
# @app.delete('/settori/{primary}', status_code=status.HTTP_204_NO_CONTENT,tags=["Multipli"])
# async def delete_a_sector(primary:int):
#     statement = select(Multipli).where(Multipli.primary==primary)
#     result = session.exec(statement).one_or_none()
#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
#     session.delete(result)
#     return result

# ## GET all years data by one sector
# @app.get('/settorecomplete',tags=["Multipli"])
# async def get_a_sector(settore:str):
#     statement = select(Multipli).where(Multipli.settore == settore)
#     result = session.exec(statement).all()
#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return result

# ## GET data by one sector by one year
# @app.get('/settoreyear',tags=["Multipli"])
# async def get_a_sector_year(anno:int,settore:str):
#     statement = select(Multipli).where(Multipli.anno == anno).where(Multipli.settore == settore)
#     result = session.exec(statement).all()
#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return result

selection_multipli = ["Descrizione_settore","EnterpriseValue_ratio_Sales","EnterpriseValue_ratio_Ebitda","EnterpriseValue_ratio_Ebit","Price_ratio_Earning",
                    "Price_ratio_BookValue","Beta_activity","Operazioniautoliquidanti","Operazioni_scadenza_entro_anno","Operazioni_scadenza_1_5_anni",
                    "Operazioni_scadenza_oltre_5_anni","Operazioni_revoca","BTP15anni","BTP10anni","BTP5anni","Premio_rischio_suggerito_perc"]
def all_multipli(df):
    d= json.loads(df.groupby(['anno','settore'])[selection_multipli] \
                                    .apply(lambda x: x.to_dict('r')) \
                                    .reset_index(name='data') \
                                    .groupby(['anno'])['settore','data'] \
                                    .apply(lambda x: x.set_index('settore')['data'].to_dict()).to_json())
    json_data = json.dumps(d)
    return json_data
    
def multipli_year(df,year):
    d= json.loads(df[df["anno"]==year].groupby(['anno','settore'])[selection_multipli] \
                                    .apply(lambda x: x.to_dict('r')) \
                                    .reset_index(name='data') \
                                    .groupby(['anno'])['settore','data'] \
                                    .apply(lambda x: x.set_index('settore')['data'].to_dict()).to_json())

    json_data = json.dumps(d)
    return json_data

def multipli_year_sector(df,year,sector):
    d= json.loads(df.loc[(df['anno'] == year) & (df['settore'] ==sector)].groupby(['anno','settore'])[selection_multipli] \
                                    .apply(lambda x: x.to_dict('r')) \
                                    .reset_index(name='data') \
                                    .groupby(['anno'])['settore','data'] \
                                    .apply(lambda x: x.set_index('settore')['data'].to_dict()).to_json())

    json_data = json.dumps(d)
    return json_data

# ## GET data by one sector by one year
# @app.get('/MULTIPLI',tags=["Multipli2"])
# async def get_all_multipli():
#     statement = select(Multipli2)
#     obj = session.exec(statement).all()
#     df = sqlmodel_to_df(obj)
#     result = all_multipli(df)
#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return json.loads(result)

# ## GET all sectors by one year
# @app.get('/MULTIPLIyear',tags=["Multipli2"])
# async def get_all_multipli_year(anno:int= 2020):
#     statement = select(Multipli2)
#     obj = session.exec(statement).all()
#     df = sqlmodel_to_df(obj)
#     result = multipli_year(df,anno)
#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return json.loads(result)

# ## GET all sectors by one year
# @app.get('/MULTIPLIyearsector',tags=["Multipli2"])
# async def get_all_multipli_year_sector(anno:int= 2020,settore:str="01"):
#     statement = select(Multipli2)
#     obj = session.exec(statement).all()
#     df = sqlmodel_to_df(obj)
#     result = multipli_year_sector(df,anno,settore)
#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return json.loads(result)

@app.get('/EARMULTIPLIyearsectorsecond',tags=["Multipli2"],)
async def get_all_multipli_year_sectorsecond(requests:Request,user:str="EARnext",anno:int= 2021,settore:str="01",
                                            current_user: User = Depends(get_current_active_user)):
    statement = select(Multipli2)
    obj = session.exec(statement).all()
    df = sqlmodel_to_df(obj)
    result = multipli_year_sector(df,anno,settore)
    req_url = requests.url.path
    append_googlesheet(req_url,settore,user)
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    j = json.loads(result)
    return j[str(anno)][settore]

@app.get('/EARMULTIPLIyearsectorfourth',tags=["Multipli4"],)
async def get_all_multipli_year_sectorearfour(requests:Request,user:str="EARnext",anno:int= 2021,settore:str="0210",
                                            current_user: User = Depends(get_current_active_user)):
    statement = select(Multipli4)
    obj = session.exec(statement).all()
    df = sqlmodel_to_df(obj)
    result = multipli_year_sector(df,anno,settore)
    req_url = requests.url.path
    append_googlesheet(req_url,settore,user)
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    j = json.loads(result)
    return j[str(anno)][settore]

###########################################################################################################################################
########################### MEDIE ######################################################################################################

#from models import Medie
import json
import pandas as pd

selection_medie = ["Descrizione_settore","classe","Roe_perc","Roi_perc","Ros_perc","Indice_liq_primaria","Indice_margine","Rapporto_indebitamento",
                    "Oneri_finanziari_div_Valore_produzione_perc","Durata_scorte_giorni","Valore_aggiunto_per_addetto","Rotazione_capitale_investito"]


def all_nested_database(df):
    d= json.loads(df.groupby(['riferimento','settore','anno'])[selection_medie] \
                                    .apply(lambda x: x.to_dict('r')) \
                                    .reset_index(name='triennio')\
                                    .groupby(['riferimento','settore'])['anno','triennio']\
                                    .apply(lambda x: x.to_dict('r')) \
                                    .reset_index(name='classi').to_json(orient = 'records'))
    return json.dumps(d)


def all_nested_json_year(df,year):
    d= json.loads(df[df["riferimento"]==year].groupby(['riferimento','settore','anno'])[selection_medie] \
                                    .apply(lambda x: x.to_dict('r')) \
                                    .reset_index(name='data') \
                                    .groupby(['settore'])['anno','data'] \
                                    .apply(lambda x: x.set_index('anno')['data'].to_dict()).to_json())
    data = {}
    data[year] = d
    json_data = json.dumps(data)
    return json_data

def sector_year_nested_json(df,sector,year):
    d= json.loads(df.loc[(df['riferimento'] == year) & (df['settore'] ==sector)]\
                                    .groupby(['riferimento','settore','anno'])[selection_medie] \
                                    .apply(lambda x: x.to_dict('r')) \
                                    .reset_index(name='data') \
                                    .groupby(['settore'])['anno','data'] \
                                    .apply(lambda x: x.set_index('anno')['data'].to_dict()).to_json())
    data = {}
    data[year] = d
    json_data = json.dumps(data)
    return json_data

## GET all the data
# @app.get('/MEDIE',tags=["Medie2"])
# async def get_all_avg():
#     statement = select(Medie2)
#     obj = session.exec(statement).all()
#     df = sqlmodel_to_df(obj)
#     result = all_nested_database(df)
#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return json.loads(result)


# ## GET all sectors by one year
# @app.get('/MEDIEyear',tags=["Medie2"])
# async def get_all_sector_avg(anno:int= 2021):
#     statement = select(Medie2)
#     obj = session.exec(statement).all()
#     df = sqlmodel_to_df(obj)
#     result = all_nested_json_year(df,anno)
#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return json.loads(result)


# ## GET data by one sector by one year
# @app.get('/MEDIEyearsector',tags=["Medie2"])
# async def get_all_sector_year_avg(anno:int= 2021,settore: str="01",):
#     statement = select(Medie2)
#     obj = session.exec(statement).all()
#     df = sqlmodel_to_df(obj)
#     result = sector_year_nested_json(df,settore,anno)
#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return json.loads(result)

## GET data by one sector by one year
@app.get('/EARMEDIEyearsectorsecond',tags=["Medie2"])
async def get_all_sector_year_second(requests:Request,user:str="EARnext",anno:int= 2021,settore: str="01",
                                    current_user: User = Depends(get_current_active_user)):
    statement = select(Medie2)
    obj = session.exec(statement).all()
    df = sqlmodel_to_df(obj)
    result = sector_year_nested_json(df,settore,anno)
    req_url = requests.url.path
    append_googlesheet(req_url,settore,user)
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    j = json.loads(result)
    return j[str(anno)][settore]

@app.get('/EARMEDIEyearsectorfourth',tags=["Medie4"])
async def get_all_sector_year_four(requests:Request,user:str="EARnext",anno:int= 2021,settore: str="0210",
                                    current_user: User = Depends(get_current_active_user)):
    statement = select(Medie4)
    obj = session.exec(statement).all()
    df = sqlmodel_to_df(obj)
    result = sector_year_nested_json(df,settore,anno)
    req_url = requests.url.path
    append_googlesheet(req_url,settore,user)
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    j = json.loads(result)
    return j[str(anno)][settore]

#############################################################################################
########################### FASCE FATTURATO #################################################

selection_fasce =["riferimento","Descrizione_settore","Ricavi_netti","Addetti","Roi_perc","Ebitda_su_Ricavi","Ebit_su_Ricavi","Rapporto_indebitamento","Indice_liquidita_primaria","Aziende_considerate","Valore_produzione",
"di_cui_Ricavi_netti","Totale_costi_operativi","Consumi","Costi_servizi_godimento_bt","Costo_lavoro","Ammortamenti_accantonamenti","Reddito_operativo_car","Valore_produzione_",
"di_cui_Ricavi_netti_","Consumi_","Costi_servizi_godimento_bt_","Valore_aggiunto","Costo_lavoro_","Margine_operativo_lordo_Ebitda","Ammortamenti_accantonamenti_",
"Totale_costi_operativi_","Reddito_operativo_caratteristico_Ebit","Proventi_accessori","Saldo_ricavi_oneri_diversi","Reddito_operativo_globale","Oneri_finanziari",
"Reddito_competenza","Risultato_gestione_straordinaria","Reddito_pre_imposte","Imposte","Reddito_netto_esercizio","Disponibilita_Liquide","Attivita_finanziarie_non_immobilizzate",
"Liquidita_immediate","Crediti_commerciali_bte","Crediti_diversi_breve_termine","Liquidita_differite","Rimanenze_finali","Attivo_corrente","Immobilizzazioni_immateriali","Immobilizzazioni_materiali",
"di_cui_Terreni_fabbricati","Partecipazioni_titoli","Crediti_commerciali_lungo_termine","Crediti_diversi_lungotermine","Immobilizzazioni_finanziarie","Attivo_immobilizzato",
"Capitale_investito","Debiti_finanziari_bter","Debiti_commerciali_bter","Debiti_diversi_breve_termine","Fondo_rischi_oneri","Passivo_corrente","Debiti_finanziari_lungotermine",
"Debiti_commerciali_lungotermine","Debiti_diversi_lungotermine","FondoTFR","Passivo_consolidato","Capitale","Riserve","Azioni_proprie","Risultato_esercizio","Patrimonio_netto",
"Passivo_e_netto","Var_perc_Ricavi","Var_perc_Capitale_investito","Var_perc_Addetti","Roe_perc","Roi_perc_","Roi_tipico_perc","Ros_perc","Redditivita_gestione_acc",
"Tigec","Ricavi_per_addetto","Valore_aggiunto_per_addetto","Costo_lavoro_per_addetto","Rotazione_capitale_investito","Rotazione_crediti_commerciali","Rotazione_scorte",
"Rotazione_debiti_commerciali","Grado_leva_operativa","Rapporto_corrente","Indice_liquidita_primaria_","Indice_margine_struttura","Indice_margine_struttura_all","Rapporto_indebitamento_",
"Oneri_finanziari_su_Reddito_op_glob_perc","Durata_crediti_commerciali_g","Durata_scorte_g","Durata_debiti_commerciali_g","Durata_ciclo_finanziario_g",]

def all_fasce(df):
    d= json.loads(df.groupby(['anno','settore'])[selection_fasce] \
                                    .apply(lambda x: x.to_dict('r')) \
                                    .reset_index(name='data') \
                                    .groupby(['anno'])['settore','data'] \
                                    .apply(lambda x: x.set_index('settore')['data'].to_dict()).to_json())
    json_data = json.dumps(d)
    return json_data

def all_fasce_year(df,year):
    d= json.loads(df[df["anno"]==year].groupby(['anno','settore'])[selection_fasce] \
                                    .apply(lambda x: x.to_dict('r')) \
                                    .reset_index(name='data') \
                                    .groupby(['anno'])['settore','data'] \
                                    .apply(lambda x: x.set_index('settore')['data'].to_dict()).to_json())
    json_data = json.dumps(d)
    return json_data

def all_fasce_year_sector(df,year,sector):
    d= json.loads(df.loc[(df['anno'] == year) & (df['settore'] ==sector)].groupby(['anno','settore'])[selection_fasce] \
                                    .apply(lambda x: x.to_dict('r')) \
                                    .reset_index(name='data') \
                                    .groupby(['anno'])['settore','data'] \
                                    .apply(lambda x: x.set_index('settore')['data'].to_dict()).to_json())
    json_data = json.dumps(d)
    return json_data

#from models import Fasce

## GET all the database
# @app.get('/FASCE',tags=["Fasce2"])
# async def get_all_branches():
#     statement = select(Fasce2)
#     obj = session.exec(statement).all()
#     df = sqlmodel_to_df(obj)
#     result = all_fasce(df)
#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return json.loads(result)

# ## GET all the data by year
# @app.get('/FASCEyear',tags=["Fasce2"])
# async def get_all_branches_years(anno:int= 2020):
#     statement = select(Fasce2)
#     obj = session.exec(statement).all()
#     df = sqlmodel_to_df(obj)
#     result = all_fasce_year(df,anno)
#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return json.loads(result)

# ## GET all the data by year
# @app.get('/FASCEyearsector',tags=["Fasce2"])
# async def get_all_branches_years_sector(anno:int= 2021,settore:str="01"):
#     statement = select(Fasce2)
#     obj = session.exec(statement).all()
#     df = sqlmodel_to_df(obj)
#     result = all_fasce_year_sector(df,anno,settore)
#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return json.loads(result)

## GET all the data by year
@app.get('/EARFASCEyearsectorsecond',tags=["Fasce2"])
async def get_all_branches_years_sectorsecond(requests:Request,user:str="EARnext",anno:int= 2021,settore:str="01",
                                            current_user: User = Depends(get_current_active_user)):
    statement = select(Fasce2)
    obj = session.exec(statement).all()
    df = sqlmodel_to_df(obj)
    result = all_fasce_year_sector(df,anno,settore)
    req_url = requests.url.path
    append_googlesheet(req_url,settore,user)
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    j = json.loads(result)
    return j[str(anno)][settore]

@app.get('/EARFASCEyearsectorfourth',tags=["Fasce4"])
async def get_all_branches_years_sectorfouth(requests:Request,user:str="EARnext",anno:int= 2021,settore:str="0111",
                                            current_user: User = Depends(get_current_active_user)):
    statement = select(Fasce4)
    obj = session.exec(statement).all()
    df = sqlmodel_to_df(obj)
    result = all_fasce_year_sector(df,anno,settore)
    req_url = requests.url.path
    append_googlesheet(req_url,settore,user)
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    j = json.loads(result)
    return j[str(anno)][settore]

##############################################################################################################################à

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
