from enum import Enum, IntEnum
from pydantic import BaseModel, ValidationError
import os
import requests
import json

class DataStoreTypeEnum(IntEnum):
    VectorDB = 1
    Unified = 2
    SQL = 3 
    MongoDB = 4

class DataStore(BaseModel): 
    id : str
    group : str
    workspace : str
    user_name :  str
    type : DataStoreTypeEnum
    name : str

    vectordb_profile : str
    embedding_model : str
    shared :   bool

    db_url :  str
    db_name : str
    db_table : str

class DataStoreList(BaseModel):
    data_stores : list[DataStore]

class DataStoreMessage(BaseModel):
    md_api_key : str
    name : str
    type : DataStoreTypeEnum

    vectordb_profile : str
    embedding_model :  str

    db_url : str
    db_name : str
    db_table : str

    shared : bool

def CreateOrUpdateUnifiedDataStore(create,
                                    md_api_key, 
                                    name, 
                                    vectordb_profile,
                                    embedding_model,
                                    db_url, 
                                    db_name, 
                                    db_table, 
                                    shared):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name
    json_input['type'] = DataStoreTypeEnum.Unified
    json_input['vectordb_profile'] = vectordb_profile
    json_input['embedding_model'] = embedding_model
    json_input['db_url'] = db_url
    json_input['db_name'] = db_name
    json_input['db_table'] = db_table
    json_input['shared'] = shared

    try:
        headers = {"Content-Type": "application/json"}
        if create == True:
            result = requests.post(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        else:
            result = requests.put(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def CreateVectorDBDataStore(md_api_key, 
                             name, 
                             vectordb_profile,
                             embedding_model,
                             shared):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name
    json_input['type'] = DataStoreTypeEnum.VectorDB
    json_input['embedding_model'] = embedding_model
    json_input['vectordb_profile'] = vectordb_profile
    json_input['db_url'] = ''
    json_input['db_name'] = ''
    json_input['db_table'] = ''
    json_input['shared'] = shared

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def CreateOrUpdateStructDBDataStore(create,
                             md_api_key, 
                             name, 
                             type,
                             embedding_model,
                             db_url, 
                             db_name, 
                             db_table):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name
    json_input['type'] = type
    json_input['vectordb_profile'] = ''
    json_input['embedding_model'] = embedding_model
    json_input['db_url'] = db_url
    json_input['db_name'] = db_name
    json_input['db_table'] = db_table
    json_input['shared'] = False

    try:
        headers = {"Content-Type": "application/json"}
        if create == True:
             result = requests.post(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        else:
             result = requests.put(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def DeleteDataStore(md_api_key, name):
       
    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.delete(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

