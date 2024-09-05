import os
import json
import requests
from pydantic import BaseModel, ValidationError
from enum import Enum, IntEnum
import majordomo_ai as md

from pathlib import Path

class TextIngestionType(IntEnum):
    Base = 1 
    Summary = 2

class PDFExtractorTypeEnum(IntEnum):
    LlamaParse = 1
    PyMuPDF = 2
    PDF2Image = 3

class IngestionTypeEnum(IntEnum):
    Text = 1
    Image = 2
    Custom = 3

class DocStoreTypeEnum(IntEnum):
    AWSS3 = 1
    AzureBlob = 2
    Webpage = 3
    Local = 4
    SQL = 5

class DataPipeline(BaseModel):
    id : str
    group : str
    workspace : str
    user_name :  str
    name : str
    query_store : str
    doc_store_type : DocStoreTypeEnum
    doc_store_info : str
    ingestion_type : IngestionTypeEnum
    ingestion_params : str
    timer_interval : int
    timer_on : int

class DataPipelineMessage(BaseModel):
    md_api_key : str
    name : str
    query_store : str
    doc_store_type : DocStoreTypeEnum
    doc_store_info : str
    ingestion_type : IngestionTypeEnum
    ingestion_params : str
    timer_interval : int
    timer_on : int

class DataPipelineRunMessage(BaseModel):
    md_api_key : str
    query_store : str
    name : str

def CreateDataPipeline(md_api_key,
                       name,
                       query_store,
                       doc_store_type,
                       doc_store_info,
                       ingestion_type,
                       ingestion_params,
                       timer_interval,
                       timer_on):
       

    #embedding_model : str
    #ingestion_type : TextIngestionType | None = "Base"
    #output_store : DataStore | None = DataStore(location='local', info=LocalDataStore(file_name=''))
    #pdf_extractor: PDFExtractorTypeEnum | None = "PyMuPDF"
    #chunking_type : str | None = 'normal'
    #chunk_size : int | None = 1024
    #llm_model : str | None = ''

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name
    json_input['query_store'] = query_store
    json_input['doc_store_type'] = doc_store_type
    json_input['doc_store_info'] = doc_store_info
    json_input['ingestion_type'] = ingestion_type
    json_input['ingestion_params'] = ingestion_params
    json_input['timer_interval'] = timer_interval
    json_input['timer_on'] = timer_on

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/data_pipeline', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def UpdateDataPipeline(md_api_key,
                       name,
                       doc_store_info,
                       ingestion_params,
                       timer_interval,
                       timer_on):
       

    #embedding_model : str
    #ingestion_type : TextIngestionType | None = "Base"
    #output_store : DataStore | None = DataStore(location='local', info=LocalDataStore(file_name=''))
    #pdf_extractor: PDFExtractorTypeEnum | None = "PyMuPDF"
    #chunking_type : str | None = 'normal'
    #chunk_size : int | None = 1024
    #llm_model : str | None = ''

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name
    json_input['query_store'] = ''
    json_input['doc_store_type'] = 0
    json_input['doc_store_info'] = doc_store_info
    json_input['ingestion_type'] = 0
    json_input['ingestion_params'] = ingestion_params
    json_input['timer_interval'] = timer_interval
    json_input['timer_on'] = timer_on

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.put(director_url + '/data_pipeline', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def DeleteDataPipeline(md_api_key, name):
       
    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.delete(director_url + '/data_pipeline', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def DataPipelineRun(md_api_key, query_store, data_pipeline):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['query_store'] = query_store
    json_input['name'] = data_pipeline

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/data_pipeline_run', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def QueryStoreAddDocument(md_api_key, query_store, doc_store_type, doc_store_info, ingestion_type, ingestion_params):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = ''
    json_input['doc_store_type'] = doc_store_type
    json_input['doc_store_info'] = doc_store_info
    json_input['query_store'] = query_store
    json_input['ingestion_type'] = ingestion_type
    json_input['ingestion_params'] = ingestion_params

    try:
        infoMap = json.loads(doc_store_info)
    except Exception as e: raise

    try:
        "files" in infoMap
    except Exception as e: raise

    files = {'file': open(infoMap["files"],'rb')}
    values = {'md_api_key': md_api_key}

    try:
        result = requests.post(director_url + '/file_upload', files=files, data=values)
    except Exception as e: raise

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/query_store_add', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise
