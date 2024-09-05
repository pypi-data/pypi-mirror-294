import os
import json
import requests
from pydantic import BaseModel, ValidationError
from enum import Enum, IntEnum

from pathlib import Path

class QueryTypeEnum(IntEnum):
    Text = 1
    Image = 2

class QueryModeEnum(IntEnum):
    Refine = 1
    Compact = 2
    Accumulate = 3

class QueryPipeline(BaseModel):
    id : str
    group : str
    workspace : str
    user_name :  str
    name : str
    query_store : str
    query_type : QueryTypeEnum
    llm_model : str
    query_params : str

class QueryPipelineMessage(BaseModel):
    user_token : str
    name : str
    query_store : str
    query_type : QueryTypeEnum
    llm_model : str
    query_params : str

def CreateOrUpdateQueryPipeline(create,
                                md_api_key,
                                name,
                                query_type,
                                query_store,
                                llm_model,
                                query_params):
       

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name
    json_input['query_type'] = query_type
    json_input['query_store'] = query_store
    json_input['llm_model'] = llm_model
    json_input['query_params'] = query_params

    try:
        headers = {"Content-Type": "application/json"}
        if create == True:
            result = requests.post(director_url + '/query_pipeline', data=json.dumps(json_input), headers=headers)
        else:
            result = requests.put(director_url + '/query_pipeline', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def DeleteQueryPipeline(md_api_key, name):
       
    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.delete(director_url + '/query_pipeline', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def RunQueryPipeline(md_api_key, name, query_str):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['name'] = name
    json_input['query_str'] = query_str

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/query_pipeline_run', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise

def RunQueryPipelineQuick(md_api_key, 
                          query_store, 
                          query_type,
                          llm_model,
                          query_params,
                          query_str):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['md_api_key'] = md_api_key
    json_input['query_store'] = query_store
    json_input['query_type'] = query_type
    json_input['llm_model'] = llm_model
    json_input['query_params'] = query_params
    json_input['query_str'] = query_str

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/query_pipeline_quick', data=json.dumps(json_input), headers=headers)
        return result

    except Exception as e: raise
